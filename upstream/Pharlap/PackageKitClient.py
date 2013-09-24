#!/usr/bin/python
#
# (c) 2008 Canonical Ltd.
# Author: Martin Pitt <martin.pitt@ubuntu.com>
# License: LGPL 2.1 or later
#
# Synchronous PackageKit client wrapper for Python.

import gobject
import dbus
from packagekit.package import PackageKitEnum

class PackageKitError(Exception):
  '''PackageKit error.

  This class mainly wraps a PackageKit "error enum". See
  http://www.packagekit.org/pk-reference.html#introduction-errors for details
  and possible values.
  '''
  def __init__(self, error):
    try:
      error = int(error)
      self.error = PackageKitEnum.error[error]
    except:
      self.error = str(error)

  def __str__(self):
    return self.error

class DBUSPkFilter(dbus.UInt64):
  def __new__(cls, filters):
    _filter = 0

    if isinstance(filters, str):
      for f in filters.split(';'):
        try:
          _filter |= ( 1 << PackageKitEnum.filter.index(f) )
        except:
          pass

    return super(DBUSPkFilter, cls).__new__(cls, _filter)

class DBUSPkTransactionFlag(dbus.UInt64):
  def __new__(cls, filters):
    _filter = 0

    if isinstance(filters, str):
      for f in filters.split(';'):
        try:
          _filter |= ( 1 << PackageKitEnum.transaction_flag.index(f) )
        except:
          pass

    return super(DBUSPkTransactionFlag, cls).__new__(cls, _filter)



class PackageKitClient:
  '''PackageKit client wrapper class.

  This exclusively uses synchonous calls. Functions which take a long time
  (install/remove packages) have callbacks for progress feedback.
  '''
  def __init__(self, main_loop=None):
    '''Initialize a PackageKit client.

    If main_loop is None, this sets up its own gobject.MainLoop(),
    otherwise it attaches to the specified one.
    '''
    self.pk_control = None
    if main_loop is None:
      import dbus.mainloop.glib
      main_loop = gobject.MainLoop()
      dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    self.main_loop = main_loop

    self.bus = dbus.SystemBus()

  def SuggestDaemonQuit(self):
    '''Ask the PackageKit daemon to shutdown.'''

    try:
      self.pk_control.SuggestDaemonQuit()
    except (AttributeError, dbus.DBusException), e:
      # not initialized, or daemon timed out
      pass

  def Resolve(self, filter, package):
    '''Resolve a package name to a PackageKit package_id.

    filter and package are directly passed to the PackageKit transaction D-BUS
    method Resolve().

    Return List of (installed, id, short_description) triples for all matches,
    where installed is a boolean and id and short_description are strings.
    '''
    result = []
    pk_xn = self._get_xn()
    pk_xn.connect_to_signal('Package',
        lambda i, p_id, summary: result.append((i == 'installed', str(p_id), str(summary))))
    pk_xn.connect_to_signal('Finished', self._h_finished)
    pk_xn.connect_to_signal('ErrorCode', self._h_error)
    pk_xn.Resolve(filter, package)
    self._wait()
    return result

  def GetDetails(self, package_id):
    '''Get details about a PackageKit package_id.

    Return tuple (license, group, description, upstream_url, size).
    '''
    result = []
    pk_xn = self._get_xn()
    pk_xn.connect_to_signal('Details', lambda *args: result.extend(args))
    pk_xn.connect_to_signal('Finished', self._h_finished)
    pk_xn.connect_to_signal('ErrorCode', self._h_error)
    pk_xn.GetDetails(package_id)
    self._wait()

    if self._error_enum:
      raise PackageKitError(self._error_enum)

    return (str(result[1]), str(result[2]), str(result[3]), str(result[4]), int(result[5]))

  def GetPackages(self, filter):
    '''Get details about a PackageKit package_id.

    Return tuple (license, group, description, upstream_url, size).
    '''
    result = []
    pk_xn = self._get_xn()
    pk_xn.connect_to_signal('Package',
        lambda i, p_id, summary: result.append((str(p_id))))
    pk_xn.connect_to_signal('ItemProgress', self._h_progress)
    pk_xn.connect_to_signal('Finished', self._h_finished)
    pk_xn.connect_to_signal('ErrorCode', self._h_error)
    pk_xn.GetPackages(filter)
    self._wait()

    if self._error_enum:
      raise PackageKitError(self._error_enum)

    return result

  def SearchNames(self, filter, name):
    '''Search a package by name.

    Return a list of (installed, package_id, short_description) triples,
    where installed is a boolean and package_id/short_description are
    strings.
    '''
    result = []
    pk_xn = self._get_xn()
    pk_xn.connect_to_signal('Package',
        lambda i, id, summary: result.extend((str(id), str(summary))))
    pk_xn.connect_to_signal('Finished', self._h_finished)
    pk_xn.connect_to_signal('ErrorCode', self._h_error)
    pk_xn.SearchNames(filter, name)
    self._wait()
    return result

  def InstallPackages(self, package_ids, progress_cb=None):
    '''Install a list of package IDs.

    progress_cb is a function taking arguments (status, percentage,
    subpercentage, elapsed, remaining, allow_cancel). If it returns False,
    the action is cancelled (if allow_cancel == True), otherwise it
    continues.

    On failure this throws a PackageKitError or a DBusException.
    '''
    self._InstRemovePackages(package_ids, progress_cb, True, None, None)

  def RemovePackages(self, package_ids, progress_cb=None, allow_deps=False,
    auto_remove=True):
    '''Remove a list of package IDs.

    progress_cb is a function taking arguments (status, percentage,
    subpercentage, elapsed, remaining, allow_cancel). If it returns False,
    the action is cancelled (if allow_cancel == True), otherwise it
    continues.

    allow_deps and auto_remove are passed to the PackageKit function.

    On failure this throws a PackageKitError or a DBusException.
    '''
    self._InstRemovePackages(package_ids, progress_cb, False, allow_deps,
        auto_remove)

  #
  # Internal helper functions
  #

  def _wait(self):
    '''Wait until an async PK operation finishes.'''
    self.main_loop.run()

  def _h_status(self, status):
    self._status = status

  def _h_allowcancel(self, allow):
    self._allow_cancel = allow

  def _h_error(self, enum, desc):
    print desc
    self._error_enum = enum

  def _h_finished(self, status, code):
    self._finished_status = PackageKitEnum.exit[status]
    self.main_loop.quit()

  def _h_progress(self, _id, status, percentage):
    def _cancel(xn):
      try:
        xn.Cancel()
      except dbus.DBusException, e:
        if e._dbus_error_name == 'org.freedesktop.PackageKit.Transaction.CannotCancel':
          pass
        else:
          raise

    ret = self._progress_cb(status, _id, int(percentage), self._allow_cancel)

    if not ret:
      # we get backend timeout exceptions more likely when we call this
      # directly, so delay it a bit
      gobject.timeout_add(10, _cancel, pk_xn)

  def _InstRemovePackages(self, package_ids, progress_cb, install, allow_deps, auto_remove):
    '''Shared implementation of InstallPackages and RemovePackages.'''

    self._status = None
    self._allow_cancel = False

    pk_xn = self._get_xn()
    if progress_cb:
      pk_xn.connect_to_signal('StatusChanged', self._h_status)
      pk_xn.connect_to_signal('AllowCancel', self._h_allowcancel)
      pk_xn.connect_to_signal('ItemProgress', self._h_progress)
      self._progress_cb = progress_cb

    pk_xn.connect_to_signal('ErrorCode', self._h_error)
    pk_xn.connect_to_signal('Finished', self._h_finished)

    if install:
      pk_xn.InstallPackages(DBUSPkTransactionFlag('none'), package_ids)
    else:
      pk_xn.RemovePackages(DBUSPkTransactionFlag('none'), package_ids, allow_deps, auto_remove)

    self._wait()

    if self._error_enum:
      raise PackageKitError(self._error_enum)

    if self._finished_status != 'success':
      raise PackageKitError('internal-error')

  def _get_xn(self):
    '''Create a new PackageKit Transaction object.'''

    self._error_enum = None
    self._finished_status = None
    try:
      tid = self.pk_control.CreateTransaction()
    except (AttributeError, dbus.DBusException), e:
      if self.pk_control == None or (hasattr(e, '_dbus_error_name') and \
        e._dbus_error_name == 'org.freedesktop.DBus.Error.ServiceUnknown'):
        # first initialization (lazy) or timeout
        self.pk_control = dbus.Interface(self.bus.get_object(
            'org.freedesktop.PackageKit', '/org/freedesktop/PackageKit',
            False), 'org.freedesktop.PackageKit')
        tid = self.pk_control.CreateTransaction()
      else:
        raise

    return dbus.Interface(self.bus.get_object('org.freedesktop.PackageKit',
        tid, False), 'org.freedesktop.PackageKit.Transaction')
#
# Test code
#

if __name__ == '__main__':
  import subprocess, sys

  pk = PackageKitClient()

  print '---- Resolve() -----'
  print pk.Resolve(DBUSPkFilter('none'), ['pmount', 'quilt', 'foobar'])
  print pk.Resolve(DBUSPkFilter('none'), ['coreutils', 'pmount'])
  print pk.Resolve(DBUSPkFilter('installed'), ['gnash'])

  print '---- GetDetails() -----'
#    print pk.GetDetails('installation-guide-powerpc;20080520ubuntu1;all;Ubuntu')

  print '---- GetPackages() -----'
  a = pk.GetPackages(DBUSPkFilter('available'))
  i = pk.GetPackages(DBUSPkFilter('installed'))
  print i

  print('installed: %d, available: %d' %( len(i), len(a) ))

  sys.exit(0)

  print '---- SearchNames() -----'
  print pk.SearchNames(DBUSPkFilter('installed'), ['coreutils'])

  def cb(status, _id, pc, c):
      print 'install pkg: %s %s, %i%%, cancel allowed: %s' % (status, _id,  pc, str(c))
      return True

#  print '---- InstallPackages() -----'
#  pk.InstallPackages(['gnash;1:0.8.10-4.fc18;x86_64;fedora'], cb)

#    subprocess.call(['dpkg', '-l', 'pmount', 'quilt'])

  print '---- RemovePackages() -----'
  pk.RemovePackages(['gnash;1:0.8.10-4.fc18;x86_64;installed:fedora'], cb, allow_deps=True)
#    pk.RemovePackages(['pmount;0.9.17-2;i386;Ubuntu', 'quilt;0.46-6;all;Ubuntu'], cb)

#    subprocess.call(['dpkg', '-l', 'pmount', 'quilt'])

  pk.SuggestDaemonQuit()
