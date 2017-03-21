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
from portal import additem, shareItem
from portal.metadata import metadata

PORTAL = "https://devas1179.dev.digant.antwerpen.local/arcgis"
USER   = "JoostSchouppe"
PASS   = "schouppe1"

MXD = r"I:\2_05_06_Publicatie\Geoportaal_projectmap\script\testdata\OpenDataAntwerpen.mxd"

def listLayersInMxd(mxdFile):
    mxd = arcpy.mapping.MapDocument(mxdFile)
    lyrs = arcpy.mapping.ListLayers( mxd )
    for lyr in lyrs:
        if hasattr(lyr, "datasource"):
            print lyr.datasource



def addNewItem():
    pass


def main():
    token = generateToken(USER, PASS, PORTAL)
#example:
##     item = additem( USER, token, PORTAL,
##            "https://geoint.antwerpen.be/arcgissql/rest/services/P_Stad/Economie/MapServer/3",
##            "bedrijventerrein_perceel ",
##            "nventarisatie van de bedrijventerreinen op perceelsniveau in het Vlaams Gewest.",
##            """SSamenvatting: Inventarisatie van de bedrijventerreinen op perceelsniveau in het Vlaams Gewest. Aan deze laag wordt door het Agentschap Ondernemen informatie gerelateerd inzake het al dan niet gebruik (incl. het type gebruik) en inzake het al dan niet beschikbaar zijn van percelen voor bedrijfsaanwending. Met gebruikspercelen wordt bedoeld de visueel waarneembare (al dan niet bebouwde) kavel, die uit een deel of uit meerdere kadastrale percelen kan bestaan. Doel: 1) Inventarisatie in functie van ruimtebalans en behoefteramingen conform het Ruimtelijk Structuurplan Vlaanderen. 2) Opbouw van promotie-instrument voor begeleiding van potentiële investeerders en (her)lokaliserende bedrijven. """,
##            "Map Service", "application, antwerpen" , "Kay Warrie")
##    if item['success']:
##        id = item["id"]
##        print shareItem(id, token, PORTAL, True, True, [] )
##    else:
##        print str(item)
    listLayersInMxd(MXD)

if __name__ == '__main__':
    main()