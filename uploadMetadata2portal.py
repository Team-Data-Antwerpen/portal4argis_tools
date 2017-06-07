#!/usr/local/bin/python
# -*- coding: utf-8 -*
#---------------------------------------------------------------------------------
# Name:        uploadMetadata2portal.py
# Purpose:     parse a mxd and upload all layers with metadata to a Arcgis portal.
#
# Author:      Kay Warrie
#
# Created:     20/03/2017
# Copyright:   (c) Kay Warrie 2017
# Licence:     MIT
#
# usage: uploadMetadata2portal.py [-h] [--portal PORTAL] [--user USER] [--mxd MXD]
#                                [--password PASSWORD] [--service SERVICE]
#
# optional arguments:
#       -h --help            show this help message and exit
#       --portal PORTAL      the link to the ESRI argis Portal
#       --user USER          the username of the ESRI argis Portal
#       --password PASSWORD  the password of the ESRI argis Portal
#       --mxd MXD            the mxd to with sync with the ESRI argis Portal
#       --service SERVICE    the link to !CORRESPONDING! mapservice of the mxd
#       --group GROUP        add all layers to this group
#---------------------------------------------------------------------------------
import argparse
import getpass
from   portal.metadata2portal import metadata2portal

#add your portal-url, username and pasword, mxd and corresponding mapservice
#if you dont want to use comamndline parameters:
PORTAL  = "https://ras1453.rte.antwerpen.local:7443/arcgis"
USER    = "PortalAdmin"
PASS    = "nimdaPortal.1"
MXD     = r"\\antwerpen.local\Doc\OD_IF_AUD\2_05_GIS\2_05_06_Publicatie\mapservice\P_Portal\portal_stad.mxd"
SERVICE = "https://geoint.antwerpen.be/arcgissql/rest/services/P_Portal/portal_stad/MapServer"
GROUP   = "Basisdata"
WS = "D:\sdedgeo.sde"
#For Example:
##PORTAL = "https://devas1179.dev.digant.antwerpen.local/arcgis"
##USER = "JoostSchouppe"
##PASS = "schouppe1"
##MXD = r"\\antwerpen.local\Doc\OD_IF_AUD\2_05_GIS\2_05_06_Publicatie\Geoportaal_projectmap\testdata\data.mxd"
##SERVICE =
##"http://geodata.antwerpen.be/arcgissql/rest/services/P_Publiek/OpenDataAntwerpen/MapServer/"
##GROUP = "Basisdata"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--portal",  help="the link to the ESRI argis Portal, default is Arcgis online", default=PORTAL)
    parser.add_argument("--user",    help="the username of the ESRI argis Portal", default=USER)
    parser.add_argument("--password",help="the password of the ESRI argis Portal", default=PASS)
    parser.add_argument("--mxd",     help="the mxd to with sync with the ESRI argis Portal", default=MXD)
    parser.add_argument("--service", help="the link to !CORRESPONDING! mapservice of the mxd", default=SERVICE)
    parser.add_argument("--group",   help="add all layers to this group", default=GROUP)
    parser.add_argument("--ws",   help="override workspace, for example .sde file", default=WS)
    args = parser.parse_args()

    if not args.user: user = raw_input("Username: ")
    else: user = args.user

    if not args.password: password = getpass.getpass()
    else: password = args.password

    if not args.mxd: mxd = raw_input("ESRI mapdocument (*mxd): ")
    else: mxd = args.mxd

    if not args.service: service = raw_input("ESRI mapservice (url): ")
    else: service = args.service
    #make sure service ends with a slash
    service = service if args.service.endswith("/") else service + "/"

    if not args.group: groups = []
    else: groups = [args.group]

    if not args.ws: ws = None
    else: ws = args.ws

    m2p = metadata2portal(user, password, args.portal, ws)
    print groups
    m2p.uploadEveryLayerInMxd(mxd, service, groups)

if __name__ == '__main__':
    main()