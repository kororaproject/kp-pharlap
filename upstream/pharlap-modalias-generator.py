#!/usr/bin/python3

import argparse
import json
import os
import pprint
import re
import subprocess
import shutil


exclude_list = ['kmod-xtables-addons', 'akmod-xtables-addons']

output_dir = '/tmp/pharlap'
json_path = '/tmp/pharlap-modalias.map'

MODULE_CLASS_RE = re.compile('.*/kernel/drivers/([^/]+)')

def module_class(ko, package=None):
  c = 'other'

  # classify on package provided
  if package:
    if package.startswith('kmod'):
      if ('-nvidia' in package) or ('-catalyst' in package):
        c = 'graphics'
      elif '-wl' in package:
        c = 'network'

  # classify based on file path
  if 'kernel/drivers/gpu' in ko:
    c = 'graphics'
  elif 'kernel/drivers/net' in ko:
    c = 'network'
  elif 'kernel/drivers/input' in ko:
    c = 'input'
  elif 'kernel/sound' in ko:
    c = 'sound'

  print("ko: %s, class: %s" % (ko, c))

  return c

# download if directory doesn't exist
if not os.path.exists(output_dir):
  os.mkdir(output_dir)
  os.chdir(output_dir)
  ret = subprocess.call(['yumdownloader', 'kernel']);
  ret = subprocess.call(['yumdownloader', 'kmod-*']);
  ret = subprocess.call(['yumdownloader', 'akmod-*']);
else:
  os.chdir(output_dir)

# determine current running kernel version
running_kernel_version = subprocess.check_output("uname -r | cut -f1-1 -d'-'", shell=True).rstrip().decode('utf-8')

modalias_map = {}
available_rpms = os.listdir(output_dir)

# loop through all downloaded RPMs
for f in available_rpms:
  # query the RPM for the name
  rpm_name, rpm_summary = subprocess.check_output('rpm -qp --queryformat "%{name}||%{summary}" ' + f, shell=True).decode('utf8').split('||')

  # skip if item is in excluded list
  if [ x for x in exclude_list if rpm_name.startswith(x) ]:
    continue

  print(rpm_name)

  # default rpm type is kernel
  rpm_type = 'kernel'

  # find the equivalent kmod if we're an akmod
  if rpm_name.startswith('akmod'):
    rpm_type = 'akmod'
    continue

  if rpm_name.startswith('kmod'):
    rpm_type = 'kmod'

  # account for kmod-staging metapackages
  if rpm_name.startswith('kmod-staging'):
    rpm_name = 'kmod-staging'

  pkg_dir = os.path.join(output_dir, f[:-4])

  print(pkg_dir)

  # extract the RPM tree
  print('Expanding ...')
  ret = subprocess.call('rpmdev-extract ' + f, shell=True)

  cmd = 'find ' + pkg_dir + ' -name "*ko"'
  print('Finding: %s' % cmd)
  available_ko = subprocess.check_output(cmd, shell=True).rstrip().decode('utf-8').split('\n')

  for ko in available_ko:
    # grab the name of the base filename sans the extension [.ko]
    ko_name = os.path.basename(ko)[:-3]
    print('KO: %s' % (ko_name))

    cmd = 'modinfo ' + ko + " | awk '/alias:/ {print $2}'"
    available_aliases = subprocess.check_output(cmd, shell=True).rstrip().decode('utf-8').split('\n')

    print("Found %d aliases" % len(available_aliases))

    for alias in available_aliases:
      # skip blank aliases
      if not len(alias):
        continue

      bus = alias.split(':')[0]

      modalias_map.setdefault(bus, {}).setdefault(alias, {}).setdefault(rpm_name, {
        'type': rpm_type,
        'module': ko_name,
        'class': module_class(ko, rpm_name),
        'summary': rpm_summary,
        'package': []
      })['package'].append(f)

  # cleanup the extracted RPM tree
  print('Cleaning ...')
  shutil.rmtree(pkg_dir)

# TODO: error check

f = open(json_path, 'w')
f.write( json.dumps(modalias_map) )
f.close()

pp = pprint.PrettyPrinter(indent=2)
pp.pprint(modalias_map)
