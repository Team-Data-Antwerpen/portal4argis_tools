import arcpy
from portal import additem, shareItem, generateToken, getUserContent, updateItem
from metadata import metadata


class metadata2portal(object):
    def __init__(self, user, password, portal):
        self.user = user
        self.password = password
        self.portal = portal
        self.userContent = getUserContent(user, '', self.updateToken(), self.portal )
        self.existingIDs = { n['title'] : n['id'] for n in self.userContent["items"]}

    def updateToken(self):
        """refresh the token, might be nessary if becomes invalid"""
        self.token = generateToken(self.user, self.password, self.portal)
        return self.token

    def uploadEveryLayerInMxd(self, mxdFile, service):
        """Parse every layer in a *mxdFile* that corresponds with *service*
           and upload it as a item to portal"""
        mxd = arcpy.mapping.MapDocument(mxdFile)
        lyrs = arcpy.mapping.ListLayers( mxd )

        for nr in range( len(lyrs)):
            lyr = lyrs[nr]
            if hasattr(lyr, "dataSource") and arcpy.Exists(lyr.dataSource):
                self.addLyr(lyr.dataSource, lyr.name, nr, service)
            else:
                arcpy.AddMessage( lyr.name + " has no valid datasource " )

            #generate new token every 50 uses
            if not nr%50 :
                self.token = generateToken(self.user, self.password, self.portal)

    def addLyr(self, dataSource, name, nr, service):
        """Add *dataSource* to *portal* for *user* , as a item with *name*
           representing a layer in *service* with id *nr*."""
        meta = metadata.metadataFromArcgis( dataSource )
        author = meta.credits if len( meta.credits ) else "Stad Antwerpen"

        descrip = ( "<strong>"+ meta.title +"</strong><div><em>"+
                    meta.orgname + "</em></div>" + meta.description +
                    "\n<br/>Creatiedatum: " + meta.createDate +
                    "\n<br/>Publicatiedatum: " + meta.pubDate +
                    "\n<br/>Revisiedatum: " + meta.reviseDate +
                    "\n<br/>Beheer: " + meta.contacts +
                    "\n<br/>Contact: " + meta.eMails )

        if name in self.existingIDs.keys():
            arcpy.AddMessage( "updating " + name )
            item = updateItem(self.user, self.token, self.portal, self.existingIDs[name], service + str(nr),
                    title=name, summary=meta.purpose, description=descrip, author=author, tags=",".join(meta.tags))
        else:
            arcpy.AddMessage( "adding " + name )
            item = additem(self.user, self.token, self.portal, service + str(nr),
                 title=name, summary=meta.purpose, description=descrip, author=author, tags=",".join(meta.tags) )

        if "success" in item.keys() and item["success"]:
            id = item["id"]
            arcpy.AddMessage( shareItem(id, self.token, self.portal, True, True, []) )
        else:
            raise Exception( "Error uploading "+ name +" : "+ str(item) )