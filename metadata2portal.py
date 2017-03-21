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
# usage: metadata2portal.py [-h] [--portal PORTAL] [--user USER] [--mxd MXD] 
#                                [--password PASSWORD] [--service SERVICE]
#
# optional arguments:
# -h                   show this help message and exit
# --portal PORTAL      the link to the ESRI argis Portal
# --user USER          the username of the ESRI argis Portal
# --password PASSWORD  the password of the ESRI argis Portal
# --mxd MXD            the mxd with sync with the ESRI argis Portal
# --service SERVICE    the link to !CORRESPONDING! mapservice of the mxd
#-------------------------------------------------------------------------------
import argparse, arcpy
from portal import additem, shareItem, generateToken, getUserContent, updateItem
from portal.metadata import metadata

def listLayersInMxd(mxdFile, token, service, user, portal):
    mxd = arcpy.mapping.MapDocument(mxdFile)
    lyrs = arcpy.mapping.ListLayers( mxd )
    for nr in range( len(lyrs)):
        lyr = lyrs[nr]
        if hasattr(lyr, "dataSource") and arcpy.Exists(lyr.dataSource):
            addLyr(lyr.dataSource, lyr.name, nr, token, service, user, portal)
        else:
            print( lyr.name + " has no valid datasource " )

def addLyr(dataSource, name, nr, token, service, user, portal):
    meta = metadata.metadataFromArcgis( dataSource )
    author = meta.credits if len( meta.credits ) else "Stad Antwerpen"

    userContent = getUserContent(user, '', token, portal )
    existingIDs = { n['title'] : n['id'] for n in userContent["items"]}

    if name in existingIDs.keys():
        print "updating " + name
        item = updateItem(user, token, portal, existingIDs[name], service + str(nr),
                 title=name, summary=meta.purpose, description=meta.description, author=author)
    else:
        print "adding " + name
        item = additem( user, token, portal, service + str(nr),
             title=name, summary=meta.purpose, description=meta.description, author=author)

    if "success" in item.keys() and item["success"]:
        id = item["id"]
        print shareItem(id, token, portal, True, True, [] )
    else:
        raise Exception( "Error uploading "+ name +" : "+ str(item) )


def main():
    #Defaults
    PORTAL = "https://devas1179.dev.digant.antwerpen.local/arcgis"
    USER   = "JoostSchouppe"
    PASS   = "schouppe1"
    MXD = r"I:\2_05_06_Publicatie\Geoportaal_projectmap\script\testdata\data.mxd"
    SERVICE = "http://geodata.antwerpen.be/arcgissql/rest/services/P_Publiek/OpenDataAntwerpen/MapServer/"
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--portal",   help="the link to the ESRI argis Portal", default=PORTAL)
    parser.add_argument("--user",     help="the username of the ESRI argis Portal", default=USER)
    parser.add_argument("--password", help="the password of the ESRI argis Portal", default=PASS)
    parser.add_argument("--mxd",      help="the mxd with sync with the ESRI argis Portal", default=MXD)
    parser.add_argument("--service",  help="the link to !CORRESPONDING! mapservice of the mxd", default=SERVICE)
    args = parser.parse_args()

    token = generateToken(args.user, args.password, args.portal)
    listLayersInMxd(args.mxd, token, args.service, args.user, args.portal)

if __name__ == '__main__':
    main()