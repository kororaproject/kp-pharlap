

import pprint
import json

class YumModaliasInfo(object):

  _data = None

  def __init__(self):
    json_data=open('/tmp/modmap.json')

    self._data = json.load(json_data)

    #pprint.pprint(data)
    json_data.close()


  def getModalias(self, package):
    if( not self.hasModalias(package) ):
        return []

    return self._data[package]['modaliases']


  def hasModalias(self, package):
    return ( package in self._data )
