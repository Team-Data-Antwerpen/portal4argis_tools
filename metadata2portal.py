#!/usr/local/bin/python
# -*- coding: utf-8 -*
#-------------------------------------------------------------------------------
# Name:        metadata2portal.py
# Purpose:     parse a mxd and upload all layers with metadata to a Arcgis portal.
#
# Author:      Kay Warrie
#
# Created:     20/03/2017
# Copyright:   (c) Kay Warrie 2017
# Licence:     MIT
#-------------------------------------------------------------------------------

import sys, os, arcpy, json
from portal import additem, shareItem, generateToken
from portal.metadata import metadata

PORTAL = "https://devas1179.dev.digant.antwerpen.local/arcgis"
USER   = "JoostSchouppe"
PASS   = "schouppe1"

#MXD and !CORRESPONDING! SERVICE
MXD = r"I:\2_05_06_Publicatie\Geoportaal_projectmap\script\testdata\OpenDataAntwerpen.mxd"
SERVICE = "http://geodata.antwerpen.be/arcgissql/rest/services/P_Publiek/OpenDataAntwerpen/MapServer/"

def listLayersInMxd(mxdFile, token):
    mxd = arcpy.mapping.MapDocument(mxdFile)
    lyrs = arcpy.mapping.ListLayers( mxd )
    for lyr in lyrs:
        n = 0
        if hasattr(lyr, "dataSource") and arcpy.Exists(lyr.dataSource):
            addNewItem(lyr.dataSource, lyr.name, n )
        else:
            print( lyr.name + " has no valid datasource " )
        n += 1

def addNewItem(datasource, name, nr):
    meta = metadata.metadataFromArcgis( dataSource )
    author = meta.credits if len( meta.credits ) else "Stad Antwerpen"
    item = additem( USER, token, PORTAL, SERVICE + str(n),
             title=name, summary=meta.purpose, description=meta.description, author=author)
    if "success" in item.keys() and item["success"]:
        id = item["id"]
        print shareItem(id, token, PORTAL, True, True, [] )
    else:
        raise Exception( "Error uploading "+ name +" : "+ str(item) )

def main():
    token = generateToken(USER, PASS, PORTAL)
    listLayersInMxd(MXD, token)

if __name__ == '__main__':
    main()