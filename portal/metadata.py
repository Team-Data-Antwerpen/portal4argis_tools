import xml.etree.ElementTree as xml
import os, tempfile, arcpy


class metadata (object):
    __updateFreqCL = {
    '001':	'continual',
    '002':	'daily',
    '003':	'weekly',
    '004':	'fortnightly',
    '005':	'monthly',
    '006':	'quarterly',
    '007':	'biannually',
    '008':	'annually',
    '009':	'asNeeded',
    '010':	'irregular',
    '011':	'notPlanned',
    '012':	'unknown'}

    def __init__(self, inXML=None, isTemp=False):
        self.metaDataXML = inXML
        self.isTemp = isTemp
        self.title = None
        self.description = None
        self.purpose = None
        self.credits = None
        self.contacts = None
        self.eMails = None
        self.orgname = None
        self.tags = []
        self.metauri = None
        self.createDate = None
        self.pubDate = None
        self.reviseDate = None
        self.MaintFreq = 'unknown'
        self._getMetaData()

    @staticmethod
    def metadataFromArcgis(arcgisDatasource):
        "return a metadata object for the arcgisDatasource"
        tempXML = tempfile.NamedTemporaryFile(suffix=".xml", delete=False)
        tempXML.file.write(r'<?xml version="1.0"?><metadata xml:lang="nl"></metadata>')
        tempXML.file.close()

        arcpy.ImportMetadata_conversion(arcgisDatasource, "FROM_ARCGIS" , tempXML.name)
        arcpy.AddMessage("created tempfile: "+   tempXML.name )
        return metadata( tempXML.name , True)

    def _csvComp(self, inTxt ):
        return inTxt.replace("\n"," ").replace("\r"," ").strip('(,) ')

    def _getMetaData(self):
        if self.metaDataXML == None: return

        doc = xml.parse( self.metaDataXML  )
        root = doc.getroot()

        titleNode = root.find(".//resTitle")
        if titleNode <> None: self.title = self._csvComp( titleNode.text )
        else: self.title = ''

        titleNode = root.find(".//idAbs")
        if titleNode <> None: self.description = self._csvComp( titleNode.text )
        else: self.description = ''

        titleNode = root.find(".//idPurp")
        if titleNode <> None: self.purpose = self._csvComp( titleNode.text )
        else: self.purpose = ''

        credNode = root.find(".//idCredit")
        if credNode <> None: self.credits = self._csvComp( credNode.text )
        else: self.credits = ''

        contNodes = root.findall(".//rpIndName")
        self.contacts = " - ".join(  set([self._csvComp( contNode.text ) for contNode in contNodes]) )

        eMailAddNodes = root.findall(".//rpCntInfo/cntAddress/eMailAdd")
        self.eMails = " - ".join(  set([self._csvComp( eMailAddNode.text ) for eMailAddNode in eMailAddNodes]) )

        orgNode = root.find(".//rpOrgName")
        if orgNode <> None: self.orgname  = self._csvComp( orgNode.text )
        else: self.orgname = ''

        self.tags = [k.text for k in root.findall(".//keyword")]

        uriNode = root.find(".//dataSetURI")
        if uriNode <> None:self.metauri = self._csvComp( uriNode.text )
        else: self.metauri = ''

        createDateNode = root.find(".//createDate")
        if createDateNode <> None: self.createDate = self._csvComp( createDateNode.text )
        else: self.createDate = ''

        pubDateNode = root.find(".//pubDate")
        if pubDateNode <> None: self.pubDate = self._csvComp( pubDateNode.text )
        else: self.pubDate = ''

        reviseDateNode = root.find(".//reviseDate")
        if reviseDateNode <> None: self.reviseDate  = self._csvComp( reviseDateNode.text )
        else: self.reviseDate = ''

        upDateNode = root.find(".//resMaint/maintFreq/MaintFreqCd")
        if upDateNode <> None and 'value' in upDateNode.attrib:
            self.MaintFreq = self.__updateFreqCL[ upDateNode.attrib['value'] ]
        else:
            self.MaintFreq = ''

        if self.isTemp:
            os.remove( self.metaDataXML )

