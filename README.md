Upload Metadata to ESRI Arcgis Portal 
===================

One the problems with the portal for arcgis is that the metadata of a dataset in the geodatabase, isn't uploaded to the  server. So the user needs to manualy copy paste the description of the layer, author, ... from metadata to the portal every time he edits the metadata.

This script will upload created a item in the portal with the correct metadata for every item in a Arcgis mapdocument. The user needs to provide the link to the service. If a item already exists with the same name t will be overwriten. 

So you can run this script daily to update changes in the metadata. 

    usage: uploadMetadata2portal.py [-h] [--portal PORTAL] [--user USER]
                              [--password PASSWORD] [--mxd MXD]
                              [--service SERVICE]

    optional arguments:
      -h, --help           show this help message and exit
      --portal PORTAL      the link to the ESRI argis Portal
      --user USER          the username of the ESRI argis Portal
      --password PASSWORD  the password of the ESRI argis Portal
      --mxd MXD            the mxd with sync with the ESRI argis Portal
      --service SERVICE    the link to !CORRESPONDING! mapservice of the mxd