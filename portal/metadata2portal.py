import arcpy
from portal import additem, shareItem, generateToken, getUserContent, updateItem
from metadata import metadata


class metadata2portal(object):
    def __init__(self, user, password, portal, mxd, service):
        self.user = user
        self.password = password
        self.mxdFile = mxd
        self.portal = portal
        self.service = service
        self.token = generateToken(self.user, self.password, self.portal)
        self.userContent = getUserContent(user, '', self.token, self.portal )
        self.existingIDs = { n['title'] : n['id'] for n in self.userContent["items"]}

    def uploadEveryLayerInMxd(self):
        """Parse every layer in a *mxdFile* that corresponds with *service*
           and upload it as a item to portal"""
        mxd = arcpy.mapping.MapDocument(self.mxdFile)
        lyrs = arcpy.mapping.ListLayers( mxd )

        for nr in range( len(lyrs)):
            lyr = lyrs[nr]
            if hasattr(lyr, "dataSource") and arcpy.Exists(lyr.dataSource):
                self.addLyr(lyr.dataSource, lyr.name, nr)
            else:
                print( lyr.name + " has no valid datasource " )

            #genatate new token every 50 uses
            if not nr%50 :
                self.token = generateToken(self.user, self.password, self.portal)

    def addLyr(self, dataSource, name, nr):
        """Add *dataSource* to *portal* for *user* , as a item with *name*
           reprsenting a layer  in *service* with id *nr*."""
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
            print( "updating " + name )
            item = updateItem(self.user, self.token, self.portal, self.existingIDs[name], self.service + str(nr),
                     title=name, summary=meta.purpose, description=descrip, author=author)
        else:
            print( "adding " + name )
            item = additem(self.user, self.token, self.portal, self.service + str(nr),
                 title=name, summary=meta.purpose, description=descrip, author=author)

        if "success" in item.keys() and item["success"]:
            id = item["id"]
            print( shareItem(id, self.token, self.portal, True, True, []) )
        else:
            raise Exception( "Error uploading "+ name +" : "+ str(item) )