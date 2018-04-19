import arcpy, os, json, csv
from portal import additem, shareItem, generateToken, getUserContent, updateItem, getGroupID, deleteItem, getGroupContent
from metadata import metadata
from ESRImapservice import ESRImapservice


class csvportal(object):
    def __init__(self, user, password, portal, worksspace, groups=[]):
        """Connect to portal with username and pasword, also set the local workspace"""
        self.user = user
        self.password = password
        self.portal = portal
        self.groups = groups
        self.token = generateToken(self.user, self.password, self.portal)
        self.groupIDs = [getGroupID(g, self.token, self.portal) for g in self.groups]
        if len(self.groupIDs) == 0:
            self.userContent = getUserContent(user, '', self.token, self.portal )
        else:
            self.userContent = getGroupContent(self.groups[0], self.token, self.portal)
        
        self.existingIDs = { n['title'] : n['id'] for n in self.userContent["items"]}
        self.LayersFoundinMXD = []
        self.ws = worksspace
        if worksspace: arcpy.env.workspace = worksspace

    def updateToken(self):
        """refresh the token, might be necessary if becomes invalid"""
        self.token = generateToken(self.user, self.password, self.portal)
        return self.token

    def uploadCsv(self, csvpath, sep=";", headerlines=1, nameCol=0, pathCol=1, urlCol=2):
        """upload every row in a csv"""
        with open( csvpath , 'rb') as csvfile:
            nr = 0
            csv_reader = csv.reader(csvfile, dialect=csv.excel, delimiter=sep)
            for n in range(headerlines): csv_reader.next()
            for row in csv_reader:
               line =  [unicode(cell, 'latin-1') for cell in row]
               name, ds, url = (line[nameCol], line[pathCol], line[urlCol])
               if self.ws and os.path.dirname(ds).endswith('.sde'):
                  ds = os.path.join(self.ws , os.path.basename(ds) )
               
               self.addLyr(ds, name, url, self.groupIDs)

               #generate new token every 50 uses
               if not nr%50 : self.token = generateToken(self.user, self.password, self.portal)
               nr += 1
         ##TODO: DELETE layers in group and not in csv      

    def addLyr(self, dataSource, name, serviceUrl, groupIDs=[]):
        """Add *dataSource* to *portal* for *user* , as a item with *name*
           representing a layer in *service* """
        meta = metadata.metadataFromArcgis( dataSource )
        author = meta.credits if len( meta.credits ) else "Stad Antwerpen"

        descrip = ( "<strong>"+ meta.title +"</strong>&nbsp;<div><em>"+
                    meta.orgname + "</em></div>&nbsp;" + meta.description +
                    "\n<br/>&nbsp;Creatiedatum: " + meta.createDate +
                    "\n<br/>&nbsp;Publicatiedatum: " + meta.pubDate +
                    "\n<br/>&nbsp;Revisiedatum: " + meta.reviseDate +
                    "\n<br/>&nbsp;Beheer: " + meta.contacts +
                    "\n<br/>&nbsp;Contact: " + meta.eMails )

        if name in self.existingIDs.keys():
            self.LayersFoundinMXD.append(name)
            arcpy.AddMessage( "updating " + name )
            item = updateItem(self.user, self.token, self.portal, self.existingIDs[name], serviceUrl,
                  title=name, summary=meta.purpose, description=descrip, author=author, tags=",".join(meta.tags))
        else:
            arcpy.AddMessage( "adding " + name )
            item = additem(self.user, self.token, self.portal, serviceUrl,
                 title=name, summary=meta.purpose, description=descrip, author=author, tags=",".join(meta.tags) )

        if "success" in item.keys() and item["success"]:
            id = item["id"]
            arcpy.AddMessage( shareItem(id, self.token, self.portal, True, True, groupIDs) )
        elif "success" in item.keys() and not item["success"]:
            raise Exception( "Error uploading "+ name +" "+ json.dumps(result))
        else:
            arcpy.AddMessage("unsure of success for layer "+ name +" "+ json.dumps(result)) 
      
    def delLyr(self, name):
        if name in self.existingIDs.keys():
           result = deleteItem(self.existingIDs[name] , self.token, self.portal, self.user)
           if "success" in result.keys() and result["success"]:
               arcpy.AddMessage("Deleted layer: " + name )
           elif "success" in result.keys() and not result["success"]:
               raise Exception( "Error deleting "+ name +" "+ json.dumps(result))
           else:
               arcpy.AddMessage("unsure of success for layer "+ name +" "+ json.dumps(result)) 