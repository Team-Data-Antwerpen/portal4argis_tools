import arcpy, os
from portal import additem, shareItem, generateToken, getUserContent, updateItem, getGroupID, deleteItem, getGroupContent
from metadata import metadata
from ESRImapservice import ESRImapservice

class metadata2portal(object):
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
        """refresh the token, might be nessary if becomes invalid"""
        self.token = generateToken(self.user, self.password, self.portal)
        return self.token

    def uploadEveryLayerInMxd(self, mxdFile, service, deleteRemaining=True):
        """Parse every layer in a *mxdFile* that corresponds with *service*
           and upload it as a item to portal"""
        mxd = arcpy.mapping.MapDocument(mxdFile)
        lyrs = arcpy.mapping.ListLayers( mxd )
        ms = ESRImapservice(service)

        for nr in range( len(lyrs)):
            lyr = lyrs[nr]
            if not hasattr(lyr, "dataSource"): continue

            if self.ws:
               ds = os.path.join(self.ws , os.path.basename(lyr.dataSource) )
            else:
               ds = lyr.dataSource

            if arcpy.Exists(ds):
                id = ms.findLayerID( lyr.name )
                if id >= 0: self.addLyr(ds, lyr.name, id, service, self.groupIDs)
                else: arcpy.AddWarning("could not find "+ lyr.name +" with mapservice: "+ service )
            else:
                arcpy.AddMessage( lyr.name + " has no valid datasource " )

            #generate new token every 50 uses
            if not nr%50 :
                self.token = generateToken(self.user, self.password, self.portal)
        
        if len(self.groupIDs) and deleteRemaining: #can only savely delete from group.
            layersRemaining = [i for i in self.existingIDs.keys() if i not in self.LayersFoundinMXD]
            for lr in layersRemaining:
               self.delLyr(lr)
        else:
            print ("no leyers to delete")

    def addLyr(self, dataSource, name, nr, service, groupIDs=[]):
        """Add *dataSource* to *portal* for *user* , as a item with *name*
           representing a layer in *service* with id *nr*."""
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
            item = updateItem(self.user, self.token, self.portal, self.existingIDs[name], service + str(nr),
                  title=name, summary=meta.purpose, description=descrip, author=author, tags=",".join(meta.tags))
        else:
            arcpy.AddMessage( "adding " + name )
            item = additem(self.user, self.token, self.portal, service + str(nr),
                 title=name, summary=meta.purpose, description=descrip, author=author, tags=",".join(meta.tags) )

        if "success" in item.keys() and item["success"]:
            id = item["id"]
            arcpy.AddMessage( shareItem(id, self.token, self.portal, True, True, groupIDs) )
        else:
            raise Exception( "Error uploading "+ name +" : "+ str(item) )
      

    def delLyr(self, name, onlyIfinMS=None):
        if name in self.existingIDs.keys():
           if onlyIfinMS:
              pass #TODO
           else:
               result = deleteItem( self.existingIDs[name] , self.token, self.portal)
           if "success" in result.keys() and result["success"]:
                arcpy.AddMessage("Deleted layer: " + name )
           else:
                raise Exception( "Error deleting "+ name  )