# Magyar TVk - by gm74 2010.
print 'Script execution: plugin.video.magyartvk.hu started'

##################################################
#
# Python/XBMC libraries used
#
##################################################

from urllib import quote, unquote
from re import search, compile, sub
from urllib2 import Request, urlopen
from urlparse import urlparse
from htmlentitydefs import entitydefs, codepoint2name
import xbmcplugin, xbmcgui, xbmcaddon

##################################################
#
# Function definitions - START
#
##################################################

#
# Manually added entry points
#
def CATEGORIES( sFeedType ):
  if sFeedType == 'live':
    addLink('HírTV',            'mms://stream3.hirtv.net/hirtv.asf',         ''.join([imageDir, 'hirtv.gif']))
    addLink('DunaTV',           'mms://80.249.172.27/dunatv',                ''.join([imageDir, 'dunatv_logo_blue.jpg']))
    addLink('Duna Autonómia',   'mms://80.249.172.27/autonomia',             ''.join([imageDir, 'duna_autonomia_uj_logo.jpg']))
    addLink('m1',               'http://streamer.carnation.hu/mtvonlinem1',  ''.join([imageDir, 'm1.jpg']))
    addLink('m2',               'http://streamer.carnation.hu/mtvonlinem2',  ''.join([imageDir, 'm2.jpg']))
    addLink('ATV',              'mms://broadcast.line.hu/atvlive',           ''.join([imageDir, 'atv_logo.png']))
  elif sFeedType == 'vod':
    addDir('MTV Videótár',      'http://videotar.mtv.hu',               '1',  ''.join([imageDir, 'mtv_vid_logo.png']),     'mtv')
    addDir('TV2 Videótár',      'http://tv2.hu/videok',                 '1',  ''.join([imageDir, 'tv2logo.png']),          'tv2')
    addDir('ATV Videótár',      'http://atv.hu/videok',                 '1',  ''.join([imageDir, 'atv_logo.png']),          'atv')

#
# Parses the VOD categories on the individual VOD sites
#
def MAININDEX( url, vod ):
  
  #
  # Get the main page content
  #
  link = getURLContent( url )
  
  #
  # MTV videótár
  #
  if vod == 'mtv':
    
    # First find and add a dir for parent categories
    match = compile('<li class=\'haschild\'><span><a href=\'(.+?)\' class=\'maincategory\'>(.+?)</a></span>').findall(link)
    for url, name in match:
      addDir( name, url, '11', '', vod )
    
    # Then add a dir for parsed leaf categories
    match = compile('<li class=\'\'><span><a href=\'(.+?)\' class=\'maincategory\'>(.+?)</a></span>').findall(link)
    for url, name in match:
      addDir( name, url, '2', '', vod)
  
  #
  # TV2 videók
  #
  elif vod == 'tv2':
    match = compile('<option value="(.+?)">(.+?)</option>').findall(link)
    for url, name in match:
      if url != '-1':
        addDir( name, ''.join(['http://tv2.hu/videok?c=', url]), '11', '', vod)
  
  #
  # ATV videótár
  #
  if vod == 'atv':
    aPages = link.split('<select name="programsId" id="filterProgram">')
    aPages = aPages[1].split('<input type="submit" class="button" value= "" />')
    match = compile('<option value="(.+?)".*>(.+?)</option>').findall(aPages[0])
    for url, name in match:
      addDir( name, 'http://atv.hu/videok/0/0/0/'+url, '11', '', vod )
  
  #
  # VIASAT3 videók
  #
  elif vod == 'via3':
    match = compile('<li><a class="serie" title=".*" href="(.+?)" tabindex="0"><span class="img"><img alt="" src="(.+?)" /></span> <span><strong>(.+?)</strong></span></a></li>').findall(link)
    for url, thumb, name in match:
      addDir( name, ''.join(['http://video.viasat3.hu', url]), '2', thumb, vod )
  
  elif vod == 'duna':
    match = compile('<div class="Text Text." id="cb(.)" onmousedown="menuDeactivate\(\)">(.+?)</div>').findall(link)
    for id, name in match:
      if bDebug == 1:
        print ''.join(["id: ", id, " -- name: ", name])
      if int( id ) > 1:
        addDir( name, id, '11', '', vod)

def SUBINDEX( url, vod ):
  
  #
  # MTV sub-category
  #
  if vod == 'mtv':
    link = getURLContent( url )
    match = compile('<a href=\'(.+?)\' class=\'subcategory\'>(.+?)</a></li>').findall(link)
    for url, name in match:
      addDir( name, url, '2', '', vod )

  #
  # TV2 video stream links
  #
  if vod == 'tv2':
    link = getURLContent( url )
    match = compile('<a href="(.+?)" >&raquo;</a>').findall(link)
    if len( match ) > 0:
      aPages = match[0].split('href="')
      addDir( "--> Következő oldal", aPages[len(aPages)-1], '11', '', vod )
    match = compile('<div class="videothumbnail"><a href="(.+?)" title="(.+?)"><img src="(.+?)" alt="(.+?)" /></a></div>').findall(link)
    for url, dummy, thumb, name in match:
      addDir( name, url, '2', thumb, vod )

  #
  # ATV video stream links
  #
  if vod == 'atv':
    link = getURLContent( url )
    match = compile('<a href="(.+?)">></a>').findall(link)
    if len( match ) > 0:
      aPages = match[0].split('href="')
      addDir( "--> Következő oldal", aPages[len(aPages)-1], '11', '', vod )
    match = compile('<li>\r\n.*<div class="list-left" >\r\n.*<a href="(.+?)">\r\n.*<img src="(.+?)" alt=""/>\r\n.*</a>.*\r\n.*</div>\r\n.*<div class="list-right">\r\n\r\n.*<div class="date">(.+?) (.+?)</div>\r\n.*<a href=".*" class="prg-type">.*</a>\r\n.*<h3>\r\n.*<a href=".*">\r\n\s*(.+?)\s*\r\n.*</a>\r\n.*</h3>\r\n.*</div>.*\r\n.*<div class="clear"></div>.*\r\n.*</li>').findall(link)
    for url, thumb, date, length, name in match:
      addDir( name+'('+length+')', url, '2', thumb, vod )

  #
  # DUNA TV sub-category
  #
  if vod == 'duna':
    id = url
    url = 'http://www.dunatv.hu/musor/videotar'
    req = urllib2.Request(url)
    req.add_header('User-Agent', userAgent)
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('<select class="Select" id="cbs'+id+'" onclick="comboSelect\(\'cb'+id+'\', \'cbs'+id+'\'\);" onkeypress="comboKey\(\'cb'+id+'\', \'cbs'+id+'\'\);" size="10">(.+?)</select>').findall(link)
    match=re.compile('<option value="(.+?)">(.+?)</option>').findall(match[0])
    for url,name in match:
      addDir(name,url,2,'',vod)

def VIDEOLINKS( url, name, vod ):
  
  #
  # MTV video links
  #
  if vod == 'mtv':
    link = getURLContent( url )
    aNextLinkMatch = compile('<a id="ucVideoList_lbNext"').findall(link)
    if len( aNextLinkMatch ) > 0:
      getNextPageLink( link, url, vod )
    aVideoMatches = compile('<a href=\'.*\'><img src=\'(.+?)\' alt="" /></a>\r\n\t\t\t\t\t\t\t<a href=\'(.+?)\'>\r\n\t\t\t\t\t\t\t(.+?)</a>').findall(link)
    for sLinkThumb, sLinkURL, sLinkName in aVideoMatches:
      sVideoLinks = getURLContent( sLinkURL )
      aLinkMatches = compile('System.insertVideo\(\'divPlayer\', \'(.+?)\'').findall( sVideoLinks )
      addLink( sLinkName, aLinkMatches[0], ''.join(['http://videotar.mtv.hu', sLinkThumb]) )
  
  #
  # TV2 video links
  #
  elif vod == 'tv2':
    link = getURLContent( ''.join([url, '/player/xml']) )
    match = compile('<!\[CDATA\[http://stream2.tv2.hu(.+?)\]\]>').findall(link)      
    addLink( name, ''.join(['http://stream2.tv2.hu', match[0]]), '' )
  
  #
  # ATV video links
  #
  elif vod == 'atv':
    link = getURLContent( url )
    match = compile('flashRouter.php\?stream_url=(.+?)\';').findall(link)
    if len( match ) > 0:
      addLink( name, ''.join([match[0], ' pageURL=http://atv.hu/flashRouter.php swfurl=http://static.atv.hu/flashes/ATV_Videoplayer_v2.swf swfvfy=true']), ''.join([imageDir, 'atv_logo.png']))
    else:
      addLink( 'Nincs match', '', '' )
  
  #
  # Duna TV video links
  #
  elif vod == 'duna':
    url = 'http://www.dunatv.hu/video/videobrowser?pid='+url
    req = urllib2.Request(url)
    req.add_header('Cookie', 'p_tz=GMT+01:00; WACID=1269463899000A700219900; JSESSIONID=F99657A4BF558CCEA807BA620D5415D3')
    match=re.search('<a href="http://www.dunatv.hu/video/videobrowser\?pid=(.+?)"><img alt=">>" border="0" src="/sites/dunatv/images/stepNext.gif"></a>', link)
    if match != None:
      addDir("--> Következő oldal", match.group(1), 2, "", vod)
    match=re.compile('<div class="Video">\n<a href="(.+?)" target="videoplayer">\n<div class="Image">\n<img src="(.+?)"></div>\n<div class="Title">(.+?)<br>\n<span style="padding-top:5px; display:block;">(.+?)</span>').findall(link)
    for url, thumb, name, date in match:
      req1 = urllib2.Request(url)
      req1.add_header('User-Agent', userAgent)
      response1 = urllib2.urlopen(req1)
      link=response1.read()
      response1.close()
      vidlink=re.search("document\.writeln\(getPlayerCode\('(.+?)',", link)
      if vidlink != None:
        addLink(name+" ("+date+")",vidlink.group(1),'http://www.dunatv.hu'+thumb)
  
  #elif vod == 'via3':
  #  match = compile('<a tabindex="0" href="(.+?)">következő</a>').findall(link)
  #  if len( match ) > 0:
  #    aPages = match[0].split('href="')
  #    addDir("--> Következő oldal", 'http://video.viasat3.hu/'+aPages[len(aPages)-1], '2', "", vod)
  #  match = compile('<a href=".*" tabindex="0"><img alt="(.+?)" src="(.+?)preview1.jpg" /></a>').findall(link)
  #  for name, url in match:
  #    addLink(name,url+'video.mp4?wuplayer_h264capable=true','')

def VIDEOLINKSNEXT(url,name,vod,post):
  if vod == 'mtv':
    req = urllib2.Request(urllib.quote(url, safe=':/'))
    req.add_header('User-Agent', userAgent)
    req.add_header('X-MicrosoftAjax', 'Delta=true')
    req.add_header('Cache-Control', 'no-cache')
    req.add_header('Content-Type', 'application/x-www-form-urlencoded; charset=utf-8')
    response = urllib2.urlopen(req,post.replace('|',''))
    link=response.read()
    response.close()
    aResponse = link.split('|')
    sContent = aResponse[3]
    aPost = post.split('|')
    aPost[3] = '&__VIEWSTATE='+urllib.quote_plus(aResponse[15])
    post = '|'.join(aPost)
    match=re.compile('<a id="ucVideoList_lbNext"').findall(sContent)
    if len(match) > 0:
      addDir("--> Következő oldal", url, 21, "", vod, post)
    match=re.compile('<a href=\'.*\'><img src=\'(.+?)\' alt="" /></a>\r\n\t\t\t\t\t\t\t<a href=\'(.+?)\'>\r\n\t\t\t\t\t\t\t(.+?)</a>').findall(sContent)
    for thumb, url, name in match:
      req1 = urllib2.Request(urllib.quote(url, safe=':/'))
      req1.add_header('User-Agent', userAgent)
      response1 = urllib2.urlopen(req1)
      link=response1.read()
      response1.close()
      match1=re.compile('System.insertVideo\(\'divPlayer\', \'(.+?)\'').findall(link)
      addLink(name,match1[0],'http://videotar.mtv.hu' + thumb)

#
# Adds a direct stream link link to the XBMC link container window
#
def addLink( name, url, iconimage):
        ok=True
        liz=xbmcgui.ListItem( htmlEntityDecode( unquote( name ) ), iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": unquote( name ) } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok

#
# Adds a directory link to the XBMC link container window
#
def addDir( sName, sURL, sMode, iconImage, sVOD, sPost=''):
  sParametersURL = ''.join( [sys.argv[0], '?url=', quote( sURL, safe=':/' ), '&mode=', sMode, '&vod=', sVOD, '&name=', quote( sName ), '&post=', quote( sPost ) ])
  if bDebug == 1:
    print ''.join(['sParametersURL: ', sParametersURL])
    #print sName
    #print htmlEntityDecode(sName)
  oListItem = xbmcgui.ListItem( htmlEntityDecode(sName), iconImage="DefaultFolder.png", thumbnailImage=iconImage)
  oListItem.setInfo( type="Video", infoLabels={ "Title": sName } )
  return xbmcplugin.addDirectoryItem( handle=int(sys.argv[1]), url=sParametersURL, listitem=oListItem, isFolder=True)
        
def getNextPageLink( link, url, vod ):
  #
  # MTV next page link for video list
  #
  if vod == 'mtv':
    match = compile('"ChallengeScript":"~(\d+)').findall(link)
    if len( match ) > 0:
      noBot = ''.join(['&ucVideo%24ucPageTools%24nbNoBot%24nbNoBot_NoBotExtender_ClientState=-', match[0]])
      match = compile('<input type="hidden" name="ucVideo\$ucPageTools\$PageToolsVideoID" id="ucVideo_ucPageTools_PageToolsVideoID" value="{(.+?)}"').findall(link)
      if len( match ) > 0:
        videoID = ''.join(['&ucVideo%24ucPageTools%24PageToolsVideoID=%7B', match[0], '%7D'])
        match = compile('<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="(.+?)" />').findall(link)
        if len( match ) > 0:
          viewState = ''.join(['&__VIEWSTATE=', quote(match[0])])
          smAjax = 'smAjax=ucVideoList%24upRelatedList%7CucVideoList%24lbNext'
          eventTarget = '&__EVENTTARGET=ucVideoList%24lbNext'
          post = ''.join([smAjax, '|', noBot, '|', videoID, '|', viewState, '|', eventTarget])
          addDir( "--> Következő oldal", url, '21', "", vod, post )

#
# Opens the sURL and returns the server's response content
#
# arg sURL (str)          :: The URL to open
#
# return sContent (str)   :: The returned content of the opened sURL
#
def getURLContent( sURL ):
  sContent = ''
  oRequest = Request( sURL )
  oRequest.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.7) Gecko/20091221 Firefox/3.6.8 (.NET CLR 3.5.30729)')
  oResponse = urlopen( oRequest )
  sContent = oResponse.read()
  oResponse.close()
  return sContent

#
# Callback function for htmlEntityDecode()
#
def htmlEntityDecodeChar( m, defs = entitydefs ):
  try:
    return defs[m.group(1)]
  except KeyError:
    return m.group(0)

#
# Decode HTML entities in the URL content/address
#
def htmlEntityDecode( sString ):
  sString = sString.replace('&#8211;', '-')
  return sub( '&(#?\w+?);', htmlEntityDecodeChar, sString )

##################################################
#
# Function definitions - END
#
##################################################


##################################################
##################################################
#
# Start MAIN
#

bDebug = 1

__settings__ = xbmcaddon.Addon(id='plugin.video.magyartvk.hu')
userAgent = 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.7) Gecko/20091221 Firefox/3.6.8 (.NET CLR 3.5.30729)'

if bDebug == 1:
  print ''.join(['Sys arg #2: ', sys.argv[2]])

try:
  aParameters = dict( [ part.split('=') for part in urlparse( sys.argv[2] )[4].split('&') ] )
except:
  aParameters = {'mode': '', 'name': ''}

imageDir = ''.join([ __settings__.getAddonInfo('path'), '/resources/images/' ])

if bDebug == 1:
  try:
    print ''.join(['Mode: ', aParameters['mode']])
  except:
    print 'Mode: '
  try:
    print ''.join(['URL: ', aParameters['url']])
  except:
    print 'URL: '
  try:
    print ''.join(['Name: ', aParameters['name']])
  except:
    print 'Name: '
  try:
    print ''.join(['VOD: ', aParameters['vod']])
  except:
    print 'VOD: '
  try:
    print ''.join(['post: ', aParameters['post']])
  except:
    print 'Post: '

if aParameters['mode']=='0':
  CATEGORIES( aParameters['url'] )
elif aParameters['mode']=='1':
  MAININDEX( aParameters['url'], aParameters['vod'] )
elif aParameters['mode']=='11':
  SUBINDEX( aParameters['url'], aParameters['vod'] )
elif aParameters['mode']=='2':
  VIDEOLINKS( aParameters['url'], aParameters['name'], aParameters['vod'] )
elif aParameters['mode']=='21':
  VIDEOLINKSNEXT( aParameters['url'], aParameters['name'], aParameters['vod'], aParameters['post'] )
else:
  #
  # Entry point of the add-on
  #
  addDir( 'Élő', 'live', '0', ''.join([imageDir,'tv_stream.jpg']), '')
  addDir( 'Videótár', 'vod', '0', '', '')

xbmcplugin.endOfDirectory( int( sys.argv[1 ] ) )

print 'Script execution: plugin.video.magyartvk.hu end'
