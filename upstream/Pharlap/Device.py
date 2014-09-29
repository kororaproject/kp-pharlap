#
# Copyright 2012-2014 "Korora Project" <dev@kororaproject.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the temms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

import re
import subprocess

LSPCI_BDKMMNNV_RE = re.compile(r'^(?:Slot|Device):\s+(?P<slot>.*)$\n^Class:\s+(?P<class_name>.+)\s+\[(?P<class>[0-9a-fA-F]{4})]$\n^Vendor:\s+(?P<vendor_name>.+)\s+\[(?P<vendor>[0-9a-fA-F]{4})]$\n^Device:\s+(?P<device_name>.+)\s+\[(?P<device>[0-9a-fA-F]{4})]$\n^SVendor:\s+(?P<svendor_name>[^\[]+)\s+\[(?P<svendor>[0-9a-fA-F]{4})]$\n^SDevice:\s+(?P<sdevice_name>.+)\s+\[(?P<sdevice>[0-9a-fA-F]{4})]$\n^Rev:\s+(?P<revision>[0-9a-fA-F]+)$\n(?:^ProgIf:\s+(?P<progif>[0-9]+)$\n)?^Driver:\s+(?P<driver>\S+)$\n^Module:\s+(?P<module>\S+)$\n', re.MULTILINE)

class Device(object):
  def __init__(self, slot=None, class_name=None, class_type=None, vendor_name=None, vendor=None, device_name=None, device=None,
      svendor_name=None, svendor=None, revision=None, progif=None, driver=None, module=None, parse=None):
    self._slot = slot
    self._class_name = class_name
    self._class = class_type

    self._vendor_name = vendor_name
    self._vendor = vendor
    self._device_name = device_name
    self._device = device
    self._svendor_name = svendor_name
    self._svendor = svendor
    self._sdevice_name = device_name
    self._sdevice = device

    self._revision = revision
    self._progif = progif
    self._driver = driver
    self._module = module

    if ( (parse is not None) and len(parse) == 15):
      self._slot = parse[0]
      self._class_name = parse[1]
      self._class = parse[2]
      self._vendor_name = parse[3]
      self._vendor = parse[4]
      self._device_name = parse[5]
      self._device = parse[6]
      self._svendor_name = parse[7]
      self._svendor = parse[8]
      self._sdevice_name = parse[9]
      self._sdevice = parse[10]
      self._revision = parse[11]
      self._progif = parse[12]
      self._driver = parse[13]
      self._module = parse[14]


  def __str__(self):
    return "Device(%s) - %s %s" % (self._slot, self._vendor_name, self._device_name)

  @property
  def slot(self):
    return self._slot

  @property
  def class_name(self):
    return self._class_name

  @property
  def class_type(self):
    return self._class

  @property
  def vendor_name(self):
    return self._vendor_name

  @property
  def vendor(self):
    return self._vendor

  @property
  def device_name(self):
    return self._device_name

  @property
  def device(self):
    return self._device_name

  @property
  def svendor_name(self):
    return self._svendor_name

  @property
  def svendor(self):
    return self._svendor

  @property
  def sdevice_name(self):
    return self._sdevice_name

  @property
  def sdevice(self):
    return self._sdevice_name





def parse_pci_devices():
  data = subprocess.check_output(["lspci", "-bDkmmnnv"]).decot('UTF-8')
  matches = LSPCI_DKMMNNV_RE.findall(data)

  return [Device(parse=x) for x in matches]




def parse_devices():
  pass


