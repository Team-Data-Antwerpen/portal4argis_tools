#!/usr/local/bin/python
# -*- coding: utf-8 -*
#-------------------------------------------------------------------------------
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
#       -h                   show this help message and exit
#       --portal PORTAL      the link to the ESRI argis Portal
#       --user USER          the username of the ESRI argis Portal
#       --password PASSWORD  the password of the ESRI argis Portal
#       --mxd MXD            the mxd to with sync with the ESRI argis Portal
#       --service SERVICE    the link to !CORRESPONDING! mapservice of the mxd
#-------------------------------------------------------------------------------
import argparse
from portal.metadata2portal import metadata2portal

#BEGIN Default globals
PORTAL  = "https://devas1179.dev.digant.antwerpen.local/arcgis"
USER    = "JoostSchouppe"
PASS    = "schouppe1"
MXD     = r"I:\2_05_06_Publicatie\Geoportaal_projectmap\testdata\data.mxd"
SERVICE = "http://geodata.antwerpen.be/arcgissql/rest/services/P_Publiek/OpenDataAntwerpen/MapServer/"
#END globals


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--portal", help="the link to the ESRI argis Portal", default=PORTAL)
    parser.add_argument("--user", help="the username of the ESRI argis Portal", default=USER)
    parser.add_argument("--password", help="the password of the ESRI argis Portal", default=PASS)
    parser.add_argument("--mxd", help="the mxd to with sync with the ESRI argis Portal", default=MXD)
    parser.add_argument("--service", help="the link to !CORRESPONDING! mapservice of the mxd", default=SERVICE)
    args = parser.parse_args()

    #make sure service end with a slash
    service = args.service if args.service.endswith("/") else args.service + "/"

    m2p = metadata2portal(args.user, args.password, args.portal, args.mxd, service)
    m2p.uploadEveryLayerInMxd()

if __name__ == '__main__':
    main()