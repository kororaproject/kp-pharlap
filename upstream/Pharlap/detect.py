'''Hardware and driver package detection functionality for Ubuntu systems.'''

# (C) 2012 Canonical Ltd.
# Author: Martin Pitt <martin.pitt@ubuntu.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

import dnf
import fnmatch
import functools
import hawkey
import json
import logging
import os
import rpm
import subprocess

from Pharlap import kerneldetection
from Pharlap.dnfcache import DNFCache
from Pharlap.hwdata import PCI, USB

db = dnf.Base()
system_architecture = dnf.rpm.basearch( hawkey.detect_arch() )

device_pci = PCI()
device_usb = USB()


def load_modalias_map():
    maps = ['./pharlap-modalias.map',
            '/usr/share/pharlap/pharlap-modalias.map']

    modalias_map = {}

    for m in maps:
        try:
            raw_data = open(m)
            modalias_map = json.load(raw_data)
            break
        except Exception:
            pass

    return modalias_map



def loaded_modules_for_modaliases(modaliases=None):
    ''' Get the loaded modules for the modalias list provided.

    '''
    if not modaliases:
        modaliases = system_modaliases()

    loaded_modules = {}

    # get generic loaded module information
    with open('/proc/modules', 'r') as f:
        lsmod = f.read()

        module_deps = []
        for l in lsmod.split('\n'):
            if not len(l):
                continue

            # ebtables 30758 3 ebtable_nat,ebtable_broute,ebtable_filter, Live 0xffffffffa07b8000
            m = l.strip().split(' ')
            loaded_modules[m[0]] = []

            # check for dependencies
            if m[3] != '-':
                loaded_modules[m[0]] += m[3].strip(',').split(',')


    loaded = {}

    for alias in modaliases:
        alias_info = modaliases[ alias ]

        # check lspci
        lspci_slot = modaliases[alias]['syspath'].split('/')[-1]
        m = subprocess.check_output("lspci -kmvvD -s %s | awk '/Driver:/ { print $2 }'" % (lspci_slot), shell=True).decode('UTF-8').strip().replace('-', '_').split('\n')

        modules = []
        if len(m):
            for _m in m:
                modules += loaded_modules.get(_m, []) + [_m]

        else:
            # check loaded module
            module_path = os.path.join(alias_info['syspath'], 'driver', 'module')

            if os.path.exists(module_path):
                # TODO: get package info for loaded module
                # rpm -qf --queryformat "$%{name}" $(modinfo -F filename module_name)
                module = os.path.basename(os.path.realpath(module_path))
                modules = loaded_modules.get(module, []) + [module]

        if len(modules):
            loaded[ alias ] = {
                'module':  list(set(modules)),
                'package': ''
            }

    return loaded


def system_modaliases():
    '''Get modaliases present in the system.

    This ignores devices whose drivers are statically built into the kernel, as
    you cannot replace them with other driver packages anyway.

    This also ignores devices where the model and vendor can not be determined.

    Return a modalias -> sysfs path map. The keys of the returned map are
    suitable for a PackageKit WhatProvides(MODALIAS) call.
    '''
    aliases = {}
    # $SYSFS_PATH is compatible with libudev
    sysfs_dir = os.environ.get('SYSFS_PATH', '/sys')
    for path, dirs, files in os.walk(os.path.join(sysfs_dir, 'devices')):
        modalias = None

        # most devices have modalias files
        if 'modalias' in files:
            try:
                with open(os.path.join(path, 'modalias')) as f:
                    modalias = f.read().strip()
            except IOError as e:
                logging.warning('system_modaliases(): Cannot read %s/modalias: %s',
                        path, e)
                continue

        # devices on SSB bus only mention the modalias in the uevent file (as
        # of 2.6.24)
        elif 'ssb' in path and 'uevent' in files:
            with open(os.path.join(path, 'uevent')) as f:
                for l in f:
                    if l.startswith('MODALIAS='):
                        modalias = l.split('=', 1)[1].strip()
                        break

        if not modalias:
            continue

        (vendor, model) = _get_db_name(path, modalias)

        if vendor is None or model is None:
            continue

        # ignore drivers which are statically built into the kernel
        driverlink =  os.path.join(path, 'driver')
        modlink = os.path.join(driverlink, 'module')
        if os.path.islink(driverlink) and not os.path.islink(modlink):
            #logging.debug('system_modaliases(): ignoring device %s which has no module (built into kernel)', path)
            continue

        aliases[modalias] = {
            'syspath': path,
            'vendor':  vendor,
            'model':   model
        }

        # check loaded module
        module_path = os.path.join(path, 'driver', 'module')
        if os.path.exists(module_path):
            # TODO: get package info for loaded module
            # rpm -qf --queryformat "$%{name}" $(modinfo -F filename module_name)
            aliases[modalias]['module'] = os.path.basename(os.path.realpath(module_path))


    return aliases



def _check_video_abi_compat(cache, record):
    xorg_video_abi = None

    # determine current X.org video driver ABI
    try:
        for p in cache['xserver-xorg-core'].candidate.provides:
            if p.startswith('xorg-video-abi-'):
                xorg_video_abi = p
                #logging.debug('_check_video_abi_compat(): Current X.org video abi: %s', xorg_video_abi)
                break
    except (AttributeError, KeyError):
        logging.debug('_check_video_abi_compat(): xserver-xorg-core not available, cannot check ABI')
        return True
    if not xorg_video_abi:
        return False

    try:
        deps = record['Depends']
    except KeyError:
        return True
    if 'xorg-video-abi-' in deps and xorg_video_abi not in deps:
        logging.debug('Driver package %s is incompatible with current X.org server ABI %s',
                record['Package'], xorg_video_abi)
        return False

    # Current X.org/nvidia proprietary drivers do not work on hybrid
    # Intel/NVidia systems; disable the driver for now
    if 'nvidia' in record['Package']:
        xorg_log = os.environ.get('UBUNTU_DRIVERS_XORG_LOG', '/var/log/Xorg.0.log')
        try:
            with open(xorg_log, 'rb') as f:
                if b'drivers/intel_drv.so' in f.read():
                    logging.debug('X.org log reports loaded intel driver, disabling driver %s for hybrid system',
                            record['Package'])
                    return False
        except IOError:
            logging.debug('Cannot open X.org log %s, cannot determine hybrid state', xorg_log)

    return True

def _cache_modalias_map(cache):
    '''Build a modalias map from an DNFCache object.

    This filters out uninstallable video drivers (i. e. which depend on a video
    ABI that xserver-xorg-core does not provide).

    Return a map bus -> modalias -> [package, ...], where "bus" is the prefix of
    the modalias up to the first ':' (e. g. "pci" or "usb").
    '''
    result = {}

    for p in cache.package_list():
        # skip foreign architectures, we usually only want native
        # driver packages

        if not (p.candidate and p.candidate.arch in ('noarch', system_architecture)):
            continue

        # skip packages without a modalias field
        try:
            m = package.record('modaliases')
        except (KeyError, AttributeError, UnicodeDecodeError):
            continue

        # skip incompatible video drivers
#        if not _check_video_abi_compat(cache, package.candidate.record):
#            continue

        try:
            for l in m:
                alias = l['alias']
                bus = alias.split(':', 1)[0]
                result.setdefault(bus, {}).setdefault(alias, set()).add(package.name)
        except ValueError:
            logging.error('Package %s has invalid modalias header: %s' % (
                package.name, m))

    return result

def packages_for_modalias(cache, modalias_map, modalias):
    '''Search packages which match the given modalias.

    Return a list of DNFCachePackage objects.
    '''
    pkgs = set()

    bus = modalias.split(':')[0]

    for alias in modalias_map.setdefault(bus, {}):
        try:
            if fnmatch.fnmatch(modalias, alias):
                for p in modalias_map[bus][alias]:
                    pkgs.add( p )
        except:
            print('No match for: %s' % modalias)

    return [cache[p] for p in pkgs]

def drivers_for_modalias(cache, modalias_map, modalias):
    '''Search packages which match the given modalias.

    Return a list of DNFCachePackage objects.
    '''
    bus = modalias.split(':')[0]
    bus_map = modalias_map.setdefault(bus, {})

    return [ alias for alias in bus_map  if fnmatch.fnmatch(modalias, alias) ]

def _is_package_free(pkg):
    assert pkg.candidate is not None

    free_licenses = set(('GPL', 'GPL v2', 'GPL and additional rights', 'Dual BSD/GPL', 'Dual MIT/GPL', 'Dual MPL/GPL', 'BSD', 'GPLv2', 'GPLv2+', 'GPLv3', 'GPLv3+'))

    license = set([ p.strip() for p in pkg.candidate.license.split('and') ])
    return len(license.intersection(free_licenses)) > 0

def _is_package_from_distro(pkg):
    if pkg.candidate is None:
        return False

    repoid = pkg.candidate.repoid.lower()

    return repoid.startswith('fedora') or \
           repoid.startswith('updates') or \
           repoid.startswith('korora')

def _pkg_get_module(pkg):
    '''Determine module name from apt Package object'''

    try:
        m = pkg.record('modaliases')
    except (KeyError, AttributeError):
        logging.debug('_pkg_get_module %s: package has no Modaliases header, cannot determine module', pkg.name)
        return None

    z = set()

    for l in m:
      z.add( l['module'] )

    if len(z) > 1:
        logging.warning('_pkg_get_module %s: package has multiple modaliases, cannot determine module', pkg.name)
        return None

    return z.pop()

def _is_manual_install(pkg):
    '''Determine if the kernel module from an apt.Package is manually installed.'''

    if pkg.installed:
        return False

    # special case, as our packages suffix the kmod with _version
    if pkg.name.endswith('nvidia'):
        module = 'nvidia'
    elif pkg.name.endswith('fglrx'):
        module = 'fglrx'
    else:
        module = _pkg_get_module(pkg)

    if not module:
        return False

    modinfo = subprocess.Popen(['modinfo', module], stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    modinfo.communicate()
    if modinfo.returncode == 0:
        logging.debug('_is_manual_install %s: builds module %s which is available, manual install',
                      pkg.name, module)
        return True

    logging.debug('_is_manual_install %s: builds module %s which is not available, no manual install',
                  pkg.name, module)
    return False


def _get_db_name(syspath, alias):
    '''Return (vendor, model) names for given device.

    Values are None if unknown.
    '''

    device_type = alias.split(':')[0]
    db = '/usr/share/hwdata/%s.ids' % device_type
    if not os.path.exists(db):
#        logging.debug('DB doesn\'t exists: %s' % (db))
        return (None, None)

    vendor = None
    device = None
    subsystem_vendor = None
    subsystem_device = None

    vendor_name = None
    device_name = None

    try:
        vendor = open('%s/vendor' % syspath).read()[2:6]
        device = open('%s/device' % syspath).read()[2:6]
        subsystem_vendor = open('%s/subsystem_vendor' % syspath).read()[2:6]
        subsystem_device = open('%s/subsystem_device' % syspath).read()[2:6]

        if device_type == 'pci':
          vendor_name = device_pci.get_vendor(vendor)
          device_name = device_pci.get_device(vendor, device)
        elif device_type == 'usb':
          vendor_name = device_usb.get_vendor(vendor)
          device_name = device_usb.get_device(vendor, device)
    except:
        pass

    logging.debug('_get_db_name(%s, %s): vendor "%s", device "%s"', syspath,
                  alias, vendor_name, device_name)
    return (vendor_name, device_name)

def system_driver_packages(cache=None, modaliases=None, progress_cb=None):
    '''Get driver packages that are available for the system.

    This calls system_modaliases() to determine the system's hardware and then
    queries yum about which packages provide drivers for those. It also adds
    available packages from detect_plugin_packages().

    If you already have a DNFCache() object, you should pass it as an
    argument for efficiency. If not given, this function creates a temporary
    one by itself.

    Return a dictionary which maps package names to information about them:

      driver_package -> {'modalias': 'pci:...', ...}

    Available information keys are:
      'modalias':    Modalias for the device that needs this driver (not for
                     drivers from detect plugins)
      'syspath':     sysfs directory for the device that needs this driver
                     (not for drivers from detect plugins)
      'plugin':      Name of plugin that detected this package (only for
                     drivers from detect plugins)
      'free':        Boolean flag whether driver is free, i. e. in the "main"
                     or "universe" component.
      'from_distro': Boolean flag whether the driver is shipped by the distro;
                     if not, it comes from a (potentially less tested/trusted)
                     third party source.
      'vendor':      Human readable vendor name, if available.
      'model':       Human readable product name, if available.
      'recommended': Some drivers (nvidia, fglrx) come in multiple variants and
                     versions; these have this flag, where exactly one has
                     recommended == True, and all others False.
    '''
    modalias_map = load_modalias_map()

    if not cache:
        cache = DNFCache(db)

    if not modaliases:
        modaliases = system_modaliases()

    devices = {}

    modaliases_items = modaliases.items()

    if progress_cb is None:
      progress_cb = lambda *x, **y: None

    total_items = len(modaliases_items)
    item_count = 0.0

    for alias, alias_info in modaliases_items:
        # show some progress love
        item_count += 0.5
        progress_cb(int(item_count * 100 / total_items), alias)

        print("Checking alias %s (%d%%) ..." % (alias, (100 * item_count / total_items)))

        matched_aliases   = drivers_for_modalias(cache, modalias_map, alias)

        # continue if not matches found
        if not matched_aliases:
            item_count += 0.5
            continue

        item_count += 0.5

        bus = alias.split(':')[0]

        # add device since we have some matches
        device = devices.setdefault(alias_info['syspath'], {
            'modalias': alias,
            'vendor': alias_info['vendor'],
            'model': alias_info['model'],
            'drivers': {}
        })

        suitable_packages = set()
        modules_classes = []

        for m in matched_aliases:
            for p in modalias_map[bus][m].keys():
                package = cache.get(p)

                # ensure package still exists
                if package is None:
                    continue

                p_details = modalias_map[bus][m][p]

                suitable_packages.add(p)

                modules_classes.append(p_details.get('class', 'other'))

                driver = device['drivers'].setdefault(package.name, {
                    'version': package.version,
                    'summary': package.summary,
                    'free': _is_package_free(package),
                    'from_distro': _is_package_from_distro(package),
                    'modules': []
                })

                modules = driver.get('modules', [])
                module = p_details['module']

                if module not in modules:
                    modules.append(module)

        device.setdefault('class', max(set(modules_classes), key=modules_classes.count))

        # show some progress love
        progress_cb(int(item_count * 100 / total_items), alias)

#    # Add "recommended" flags for NVidia alternatives
#    nvidia_packages = [p for p in packages if p.endswith('kmod-nvidia')]
#    if nvidia_packages:
#        nvidia_packages.sort(key=functools.cmp_to_key(_cmp_gfx_alternatives))
#        recommended = nvidia_packages[-1]
#        for p in nvidia_packages:
#            packages[p]['recommended'] = (p == recommended)
#
#    # Add "recommended" flags for fglrx alternatives
#    fglrx_packages = [p for p in packages if p.endswith('kmod-catalyst')]
#    if fglrx_packages:
#        fglrx_packages.sort(key=functools.cmp_to_key(_cmp_gfx_alternatives))
#        recommended = fglrx_packages[-1]
#        for p in fglrx_packages:
#            packages[p]['recommended'] = (p == recommended)
#
#    # add available packages which need custom detection code
#    for plugin, pkgs in detect_plugin_packages(cache).items():
#        for p in pkgs:
#            yum_p = cache[p]
#            packages[p] = {
#                    'free': _is_package_free(yum_p),
#                    'from_distro': _is_package_from_distro(yum_p),
#                    'plugin': plugin,
#                }
#
    return devices

def system_device_drivers(cache=None):
    '''Get by-device driver packages that are available for the system.

    This calls system_modaliases() to determine the system's hardware and then
    queries DNF about which packages provide drivers for each of those. It also
    adds available packages from detect_plugin_packages(), using the name of
    the detction plugin as device name.

    If you already have a DNFCache() object, you should pass it as an
    argument for efficiency. If not given, this function creates a temporary
    one by itself.

    Return a dictionary which maps devices to available drivers:

      device_name -> {'modalias': 'pci:...', <device info>,
                      'drivers': {'pkgname': {<driver package info>}}

    A key (device name) is either the sysfs path (for drivers detected through
    modaliases) or the detect plugin name (without the full path).

    Available keys in <device info>:
      'modalias':    Modalias for the device that needs this driver (not for
                     drivers from detect plugins)
      'vendor':      Human readable vendor name, if available.
      'model':       Human readable product name, if available.
      'drivers':     Driver package map for this device, see below. Installing any
                     of the drivers in that map will make this particular
                     device work. The keys are the package names of the driver
                     packages; note that this can be an already installed
                     default package such as xserver-xorg-video-nouveau which
                     provides a free alternative to the proprietary NVidia
                     driver; these will have the 'builtin' flag set.
      'manual_install':
                     None of the driver packages are installed, but the kernel
                     module that it provides is available; this usually means
                     that the user manually installed the driver from upstream.

    Aavailable keys in <driver package info>:
      'builtin':     The package is shipped by default in Fedora/Korora and MUST
                     NOT be uninstalled. This usually applies to free
                     drivers like xserver-xorg-video-nouveau.
      'free':        Boolean flag whether driver is free, i. e. in the "main"
                     or "universe" component.
      'from_distro': Boolean flag whether the driver is shipped by the distro;
                     if not, it comes from a (potentially less tested/trusted)
                     third party source.
      'recommended': Some drivers (nvidia, fglrx) come in multiple variants and
                     versions; these have this flag, where exactly one has
                     recommended == True, and all others False.
      'activated':   Boolean flag whether the driver is currently loaded into
                     the kernel or not.
      'blacklisted': Boolean flag whether the driver is currently blacklisted
                     or not.
    '''
    result = {}
    if not cache:
        cache = DNFCache(db)

    # copy the system_driver_packages() structure into the by-device structure
    for pkg, pkginfo in system_driver_packages(cache).items():
        if 'syspath' in pkginfo:
            device_name = pkginfo['syspath']
        else:
            device_name = pkginfo['plugin']

        result.setdefault(device_name, {})

        for opt_key in ('modalias', 'vendor', 'model'):
            if opt_key in pkginfo:
                result[device_name][opt_key] = pkginfo[opt_key]

        drivers = result[device_name].setdefault('drivers', {})
        drivers[pkg] = {'free': pkginfo['free'], 'from_distro': pkginfo['from_distro']}

        if 'recommended' in pkginfo:
            drivers[pkg]['recommended'] = pkginfo['recommended']

    # now determine the manual_install device flag: this is true iff all driver
    # packages are "manually installed"
    for driver, info in result.items():
        for pkg in info['drivers']:
            if not _is_manual_install(cache[pkg]):
                break
        else:
            info['manual_install'] = True

    # add OS builtin free alternatives to proprietary drivers
    _add_builtins(result)

    return result

def auto_install_filter(packages):
    '''Get packages which are appropriate for automatic installation.

    Return the subset of the given list of packages which are appropriate for
    automatic installation by the installer. This applies to e. g. the Broadcom
    Wifi driver (as there is no alternative), but not to the FGLRX proprietary
    graphics driver (as the free driver works well and FGLRX does not provide
    KMS).
    '''
    # any package which matches any of those globs will be accepted
    whitelist = ['bcmwl*', 'pvr-omap*', 'virtualbox-guest*', 'nvidia-*']
    allow = []
    for pattern in whitelist:
        allow.extend(fnmatch.filter(packages, pattern))

    result = {}
    for p in allow:
        if 'recommended' not in packages[p] or packages[p]['recommended']:
            result[p] = packages[p]
    return result

def detect_plugin_packages(cache=None):
    '''Get driver packages from custom detection plugins.

    Some driver packages cannot be identified by modaliases, but need some
    custom code for determining whether they apply to the system. Read all *.py
    files in /usr/share/korora-drivers-common/detect/ or
    $KORORA_DRIVERS_DETECT_DIR and call detect(cache) on them. Filter the
    returned lists for packages which are available for installation, and
    return the joined results.

    If you already have an existing DNFCache() object, you can pass it as an
    argument for efficiency.

    Return pluginname -> [package, ...] map.
    '''
    packages = {}
    plugindir = os.environ.get('KORORA_DRIVERS_DETECT_DIR',
            '/usr/share/korora-drivers-common/detect/')
    if not os.path.isdir(plugindir):
        logging.debug('Custom detection plugin directory %s does not exist', plugindir)
        return packages

    if cache is None:
        cache = DNFCache(db)

    for fname in os.listdir(plugindir):
        if not fname.endswith('.py'):
            continue
        plugin = os.path.join(plugindir, fname)
        logging.debug('Loading custom detection plugin %s', plugin)

        symb = {}
        with open(plugin) as f:
            try:
                exec(compile(f.read(), plugin, 'exec'), symb)
                result = symb['detect'](cache)
                logging.debug('plugin %s return value: %s', plugin, result)
            except Exception as e:
                logging.exception('plugin %s failed:', plugin)
                continue

            if result is None:
                continue
            if type(result) not in (list, set):
                logging.error('plugin %s returned a bad type %s (must be list or set)', plugin, type(result))
                continue

            for pkg in result:
                if pkg in cache and cache[pkg].candidate:
                    if _check_video_abi_compat(cache, cache[pkg].candidate.record):
                        packages.setdefault(fname, []).append(pkg)
                else:
                    logging.debug('Ignoring unavailable package %s from plugin %s', pkg, plugin)

    return packages

def _cmp_gfx_alternatives(x, y):
    '''Compare two graphics driver names in terms of preference.

    -updates always sort after non-updates, as we prefer the stable driver and
    only want to offer -updates when the one from release does not support the
    card. We never want to recommend -experimental unless it's the only one
    available, so sort this last.
    '''
    if x.endswith('-updates') and not y.endswith('-updates'):
        return -1
    if not x.endswith('-updates') and y.endswith('-updates'):
        return 1
    if 'experiment' in x and 'experiment' not in y:
        return -1
    if 'experiment' not in x and 'experiment' in y:
        return 1
    if x < y:
        return -1
    if x > y:
        return 1
    assert x == y
    return 0

def _add_builtins(drivers):
    '''Add builtin driver alternatives'''

    for device, info in drivers.items():
        for pkg in info['drivers']:
            # nouveau is good enough for recommended
            if pkg.endswith('kmod-nvidia'):
                for d in info['drivers']:
                    info['drivers'][d]['recommended'] = False
                info['drivers']['xorg-x11-drv-nouveau'] = {
                    'free': True, 'builtin': True, 'from_distro': True, 'recommended': False}
                break

            # radeon is working well for recommended
            if pkg.endswith('kmod-catalyst'):
                for d in info['drivers']:
                    info['drivers'][d]['recommended'] = False
                info['drivers']['xorg-x11-drv-ati'] = {
                    'free': True, 'builtin': True, 'from_distro': True, 'recommended': True}
                break

def get_linux_headers(cache):
    '''Return the linux headers for the system's kernel'''
    kernel_detection = kerneldetection.KernelDetection(cache)
    return kernel_detection.get_linux_headers_metapackage()

def get_linux(cache):
    '''Return the linux metapackage for the system's kernel'''
    kernel_detection = kerneldetection.KernelDetection(cache)
    return kernel_detection.get_linux_metapackage()
