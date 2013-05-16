
import json
import yum

class YumCache(object):

  def __init__(self, yb=yum.YumBase()):
    self._yb = yb

    # we're a cache after all
    self._yb.conf.cache = 1

    self._candidate = self._yb.pkgSack.returnNewestByNameArch()
    self._installed = self._yb.rpmdb.returnPackages()

    self._c = {}

    for p in self._candidate:
      self._c[p.name] = YumCachePackage(name=p.name, candidate=p)
      
    for p in self._installed:
      if not p.name in self._c:
        self._c[p.name] = YumCachePackage(name=p.name)

      self._c[p.name].installed = p

    json_data = open('/tmp/modaliases.json')

    _data = json.load(json_data)

    for p,v in _data.iteritems():
      if p in self._c:
        self._c[p].record_set('modaliases',  v['modaliases'])


  def total_candidates(self):
    return len(self._candidates)

  def total_installed(self):
    return len(self._installed)

  def package_list(self):
    return self._c.values()
    
  def package(self, name):
    if not name in self._c:
      return None

    return self._c[name]

  def is_installed(self, name):
    if not name in self._c:
      return False
   
    return self._c[name]['installed'] is not None 



class YumCachePackage(object):
  def __init__(self, name='', candidate=None, installed=None):
    self._name = name
    self._candidate = candidate
    self._installed = installed
    self._records = {}

  @property
  def name(self):
    return self._name

  @name.setter
  def name(self, name):
    self._name = name

  @property
  def candidate(self):
    return self._candidate

  @candidate.setter
  def candidate(self, candidate):
    self._candidate = candidate

  @property
  def installed(self):
    return self._installed

  @installed.setter
  def installed(self, installed):
    self._installed = installed

  def record(self, name):
    if not name in self._records:
      raise KeyError('%s not a valid record' % (name))

    return self._records[name]

  def record_set(self, name, value):
    self._records[name] = value

