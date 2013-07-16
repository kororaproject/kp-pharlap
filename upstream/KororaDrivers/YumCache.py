import fnmatch
import json
import yum

class YumCache(object):
  def __init__(self, yb=yum.YumBase()):
    if not isinstance(yb, yum.YumBase):
      raise Exception('Expected YumBase object.')

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

    maps = ['/usr/share/korora-drivers-common/yum-modalias.map',
            '/tmp/modaliases.json']

    _map_data = None
    for m in maps:
      try:
        raw_data = open(m)
        _map_data = json.load(raw_data)
        break
      except Exception:
        pass

    if _map_data is not None:
      for p,v in _map_data.iteritems():
        if p in self._c:
          self._c[p].record_set('modaliases',  v['modaliases'])
    else:
      print "No modalias maps available."

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

    return self._c[name].installed is not None

  def search_installed(self, name):
    found = []

    for p in self._installed:
      if fnmatch.fnmatch(p.name, name):
        found.append( self._c[p.name] )

    return found

  def __len__(self):
    return len(self._c)

  def __contains__(self, key):
    return key in self._c

  def __getitem__(self, key):
    if not key in self._c:
      raise KeyError('Package %s not found in cache.' % key)

    return self._c[key]

  def __iter__(self):
    return iter(self._c)

  def items():
    return self._c.items()

  def itervalues(self):
    return iter(self._c)

  def keys(self):
    return self._c.keys()

  def values(self):
    return self._c.values()

  def itervalues(self):
    return self._c.itervalues()


class YumCachePackage(object):
  def __init__(self, name='', candidate=None, installed=None):
    self._name = name
    self._candidate = candidate
    self._installed = installed
    self._records = {}

  def __str__(self):
    return self._name

  @property
  def name(self):
    return self._name

  @property
  def shortname(self):
    return self._name

  @property
  def pkname(self):
    repo = 'installed'
    if self._installed is None:
      repo = self.candidate.repoid

    return '%s;%s-%s;%s;%s' % (self._name, self.candidate.version, self.candidate.release, self.candidate.arch, repo)

  @property
  def ycname(self):
    repo = 'installed'
    if self._installed is None:
      repo = self.candidate.repoid

    return '%s,%s,%s,%s,%s,%s' % (self._name, self.candidate.epoch, self.candidate.version, self.candidate.release, self.candidate.arch, repo)

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

  def has_record(self, name):
    return name in self._records

  def record_set(self, name, value):
    self._records[name] = value

  def is_installed(self):
    return self._installed is not None

