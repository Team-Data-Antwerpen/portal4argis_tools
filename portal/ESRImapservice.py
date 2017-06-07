import urllib, json, ssl
from urllib2 import Request, urlopen

NOSSL  = True

class ESRImapservice(object):
    """work with ESRI mapservices"""
    def __init__(self, msUrl=""):
        self.url = msUrl.split("?")[0] #http://geodata.antwerpen.be/arcgissql/rest/services/P_Publiek/OpenDataAntwerpen/MapServer

    def getMSdescription(self):
       """get de description of the mapservice """
       params =  urllib.urlencode({'f': 'json'})
       context = ssl._create_unverified_context() if NOSSL else None
       request = self.url + '?'+ params
       response = json.load( urllib.urlopen(request, context=context) )
       return response

    def findLayerID(self, layerName ):
       """returns the id of the layer with *layername* if none find """
       MSdescripton = self.getMSdescription()

       results = [n['id'] for n in MSdescripton["layers"] if n['name'].lower() == layerName.lower() ]
       if len(results) > 0:
          return results[0]
       else:
          return -1
