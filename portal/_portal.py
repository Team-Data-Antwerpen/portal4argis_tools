# util labrary to work with portal, like: http://server.arcgis.com/en/portal/latest/administer/linux/example-transfer-item-ownership.htm

import urllib, json, ssl
from urllib2 import Request, urlopen

NOSSL  = True

def generateToken(username, password, portalUrl):
    'Retrieves a token to be used with API requests.'
    context = ssl._create_unverified_context() if NOSSL else None
    params = urllib.urlencode({'username' : username,
            'password' : password, 'client' : 'referer',
            'referer': portalUrl, 'expiration': 60, 'f' : 'json'})
    resp = urlopen(portalUrl + '/sharing/rest/generateToken?', params, context=context)
    jsonResponse = json.load(resp)
    if 'token' in jsonResponse:
        return jsonResponse['token']
    elif 'error' in jsonResponse:
        errMsg =  jsonResponse['error']['message']
        for detail in jsonResponse['error']['details']:
            errMsg += "\n"+ detail
        raise Exception( errMsg )

def getUserContent(username, folder, token, portalUrl):
    'Returns a list of all folders for the specified user.'
    context = ssl._create_unverified_context() if NOSSL else None
    params =  urllib.urlencode({'token': token, 'f': 'json'})
    request = portalUrl + '/sharing/rest/content/users/' + username +'/'+ folder +'?'+ params
    userContent = json.load( urllib.urlopen(request, context=context) )
    return userContent

def getItemInfo(itemId, token, portalUrl):
    'Returns general information about the item.'
    context = ssl._create_unverified_context() if NOSSL else None
    params = urllib.urlencode({'token' : token,'f' : 'json'})
    request = portalUrl +'/sharing/content/items/'+ itemId +'?'+ params
    itemInfo = json.load( urlopen(request, context=context) )
    return itemInfo

def additem(user, token, portalUrl, url, title, summary="", description="",
                             dtype="Map Service", tags="web", author="Stad Antwerpen"):
    '''POST a new item to the portal:
        <PORTAL>/arcgis/portalhelp/apidocs/rest/index.html?groupsearch.html#/Add_Item/02t600000022000000/'''
    context = ssl._create_unverified_context() if NOSSL else None
    requestUrl = portalUrl +'/sharing/rest/content/users/'+ user +'/addItem'
    params = urllib.urlencode({
        'token' : token, 'f': 'json',
        'URL': url, 'title': title.encode('utf-8').strip(),
        'snippet': summary[:250].encode('utf-8').strip(),
        'description': description.encode('utf-8').strip(),
        'type': dtype, 'tags': tags.encode('utf-8').strip(),
        'accessInformation': author.encode('utf-8').strip(),
        "access": "public"
    }).encode()

    request = Request(requestUrl, params)
    item = json.load( urlopen(request, context=context) )
    return item

def updateItem(user, token, portalUrl, itemID, url=None, title=None, summary=None,
               description=None, tags=None, author=None):
    '''modify a existing item: https://devas1179.dev.digant.antwerpen.local/arcgis/portalhelp/apidocs/rest/index.html?groupsearch.html#/Update_Item/02t60000000z000000/'''
    context = ssl._create_unverified_context() if NOSSL else None
    data = {'token' : token,'f' : 'json', "access": "public"}
    if url: data["URL"] = url
    if title: data["title"] = title.encode('utf-8').strip()
    if summary: data["snippet"] = summary[:250].encode('utf-8').strip(),
    if description: data["description"] = description.encode('utf-8').strip()
    if tags: data["tags"] = tags.encode('utf-8').strip()
    if author: data["accessInformation"] = author.encode('utf-8').strip()

    requestUrl = portalUrl +'/sharing/rest/content/users/'+ user +'/items/' + itemID + "/update"
    request = Request(requestUrl, urllib.urlencode(data).encode())
    item = json.load( urlopen(request, context=context) )
    return item

def shareItem(itemId, token, portalUrl, everyone=True, organistion=True, groups=[]):
    """share a item"""
    context = ssl._create_unverified_context() if NOSSL else None
    public = 'true' if everyone else 'false'
    org = 'true' if organistion else 'false'

    params = urllib.urlencode({'token' : token, 'f' : 'json', 'org': org,
                               'everyone': public, 'groups': ",".join(groups).encode('utf-8').strip() }).encode()

    requestUrl = portalUrl +'/sharing/content/items/'+ itemId + '/share'
    request = Request(requestUrl, params)
    item = json.load( urlopen(request, context=context) )
    return item
