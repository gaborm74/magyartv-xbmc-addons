import urllib,urllib2,re,xbmcplugin,xbmcgui

# Magyar TVk - by gm74 2010.

userAgent = 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7 (.NET CLR 3.5.30729)'

def CATEGORIES(url):
	if url == 'live':
		addLink('HírTV','mms://stream3.hirtv.net/hirtv.asf',imageDir + 'hirtv.gif')
		addLink('DunaTV','mms://80.249.172.27/dunatv',imageDir + 'dunatv_logo_blue.jpg')
		addLink('Duna Autonómia','mms://80.249.172.27/autonomia',imageDir + 'duna_autonomia_uj_logo.jpg')
		addLink('m1','http://streamer.carnation.hu/mtvonlinem1',imageDir + 'm1.jpg')
		addLink('m2','http://streamer.carnation.hu/mtvonlinem2',imageDir + 'm2.jpg')
		addLink('ATV','mms://broadcast.line.hu/atvlive',imageDir + 'atv_logo.png')
	elif url == 'vod':
		addDir('MTV Videótár','http://videotar.mtv.hu',1,imageDir + 'mtv_vid_logo.png','mtv')
		addDir('TV2 Videótár','http://tv2.hu/videok',1,imageDir + 'tv2logo.png','tv2')
		addDir('Viasat3 Videótár','http://video.viasat3.hu',1,imageDir + 'viasat3.jpg','via3')
		addDir('DunaTV Videótár','http://www.dunatv.hu/musor/videotar',1,imageDir + 'dunatv_logo_blue.jpg','duna')
		
                       
def MAININDEX(url,vod):
	req = urllib2.Request(url)
	req.add_header('User-Agent', userAgent)
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	if vod == 'mtv':
		match=re.compile('<li class=\'haschild\'><span><a href=\'(.+?)\' class=\'maincategory\'>(.+?)</a></span>').findall(link)
		for url,name in match:
			addDir(name,url,11,'',vod)
		match=re.compile('<li class=\'\'><span><a href=\'(.+?)\' class=\'maincategory\'>(.+?)</a></span>').findall(link)
		for url,name in match:
			addDir(name,url,2,'',vod)
	elif vod == 'tv2':
		match=re.compile('<option value="(.+?)">(.+?)</option>').findall(link)
		for url,name in match:
			if url != '-1':
				addDir(name,'http://tv2.hu/videok?c='+url,2,'',vod)
	elif vod == 'via3':
		match=re.compile('<li><a class="serie" title=".*" href="(.+?)" tabindex="0"><span class="img"><img alt="" src="(.+?)" /></span> <span><strong>(.+?)</strong></span></a></li>').findall(link)
		for url,thumb,name in match:
			addDir(name,'http://video.viasat3.hu'+url,2,thumb,vod)
	elif vod == 'duna':
		match=re.compile('<div class="Text Text." id="cb(.)" onmousedown="menuDeactivate\(\)">(.+?)</div>').findall(link)
		for id,name in match:
			print "id: "+id+" -- name: "+name
			if int(id) > 1:
				addDir(name,id,11,'',vod)

def SUBINDEX(url,vod):
	if vod == 'mtv':
		req = urllib2.Request(url.replace(" ","%20"))
		req.add_header('User-Agent', userAgent)
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
		match=re.compile('<a href=\'(.+?)\' class=\'subcategory\'>(.+?)</a></li>').findall(link)
		for url,name in match:
			addDir(name,url,2,'',vod)
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

def VIDEOLINKS(url,name,vod):
 	if vod == 'duna':
		url = 'http://www.dunatv.hu/video/videobrowser?pid='+url
		req = urllib2.Request(url)
		req.add_header('Cookie', 'p_tz=GMT+01:00; WACID=1269463899000A700219900; JSESSIONID=F99657A4BF558CCEA807BA620D5415D3')
	else:
		req = urllib2.Request(urllib.quote(url, safe=':/'))
	req.add_header('User-Agent', userAgent)
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
 	if vod == 'mtv':
		match=re.compile('<a id="ucVideoList_lbNext"').findall(link)
		if len(match) > 0:
			getNextPageLink(link,url,vod)
		match=re.compile('<a href=\'.*\'><img src=\'(.+?)\' alt="" /></a>\r\n\t\t\t\t\t\t\t<a href=\'(.+?)\'>\r\n\t\t\t\t\t\t\t(.+?)</a>').findall(link)
		for thumb, url, name in match:
			req1 = urllib2.Request(urllib.quote(url, safe=':/'))
			req1.add_header('User-Agent', userAgent)
			response1 = urllib2.urlopen(req1)
			link=response1.read()
			response1.close()
			match1=re.compile('System.insertVideo\(\'divPlayer\', \'(.+?)\'').findall(link)
			addLink(name,match1[0],'http://videotar.mtv.hu' + thumb)
 	elif vod == 'tv2':
		match=re.compile('<a href="(.+?)" >&raquo;</a>').findall(link)
		if len(match) > 0:
			aPages = match[0].split('href="')
			addDir("--> Következő oldal", aPages[len(aPages)-1], 2, "", vod)
		match=re.compile('<div class="videothumbnail"><a href="(.+?)" title="(.+?)"><img src="(.+?)" alt="(.+?)" /></a></div>').findall(link)
		for url, dummy, thumb, name in match:
			req1 = urllib2.Request(url+'/player/xml')
			req1.add_header('User-Agent', userAgent)
			response1 = urllib2.urlopen(req1)
			link=response1.read()
			response1.close()
			match1=re.compile('<!\[CDATA\[http://stream2.tv2.hu(.+?)\]\]>').findall(link)			
			addLink(name,'http://stream2.tv2.hu'+match1[0],thumb)
 	elif vod == 'via3':
		match=re.compile('<a tabindex="0" href="(.+?)">következő</a>').findall(link)
		if len(match) > 0:
			aPages = match[0].split('href="')
			addDir("--> Következő oldal", 'http://video.viasat3.hu/'+aPages[len(aPages)-1], 2, "", vod)
		match=re.compile('<a href=".*" tabindex="0"><img alt="(.+?)" src="(.+?)preview1.jpg" /></a>').findall(link)
		for name, url in match:
			addLink(name,url+'video.mp4?wuplayer_h264capable=true','')
 	elif vod == 'duna':
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

def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param




def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(htmlEntityDecode(name), iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok


def addDir(name,url,mode,iconimage,vod,post=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&vod="+str(vod)+"&name="+urllib.quote_plus(name)+"&post="+urllib.quote_plus(post)
        ok=True
        liz=xbmcgui.ListItem(htmlEntityDecode(name), iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        
def getNextPageLink(link,url,vod):
 	if vod == 'mtv':
		match=re.compile('"ChallengeScript":"~(\d+)').findall(link)
		if len(match) > 0:
			noBot = '&ucVideo%24ucPageTools%24nbNoBot%24nbNoBot_NoBotExtender_ClientState=-'+match[0]
			match=re.compile('<input type="hidden" name="ucVideo\$ucPageTools\$PageToolsVideoID" id="ucVideo_ucPageTools_PageToolsVideoID" value="{(.+?)}"').findall(link)
			if len(match) > 0:
				videoID = '&ucVideo%24ucPageTools%24PageToolsVideoID=%7B'+match[0]+'%7D'
				match=re.compile('<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="(.+?)" />').findall(link)
				if len(match) > 0:
					viewState = '&__VIEWSTATE='+urllib.quote_plus(match[0])
					smAjax = 'smAjax=ucVideoList%24upRelatedList%7CucVideoList%24lbNext'
					eventTarget = '&__EVENTTARGET=ucVideoList%24lbNext'
					post = smAjax+'|'+noBot+'|'+videoID+'|'+viewState+'|'+eventTarget
					addDir("--> Következő oldal", url, 21, "", vod, post)
	
def htmlEntityDecode(s):
	aEntities = {
		"aacute": "á", 
		"Aacute": "Á", 
		"eacute": "é", 
		"Eacute": "É", 
		"iacute": "í", 
		"Iacute": "Í", 
		"oacute": "ó", 
		"Oacute": "Ó", 
		"ouml": "ö", 
		"Ouml": "Ö", 
		"uacute": "ú", 
		"Uacute": "Ú", 
		"uuml": "ü", 
		"Uuml": "Ü",
		"bdquo": "\"",
		"rdquo": "\"",
		"ndash": "-"
	}
	match=re.compile('&(\w+?);').findall(s)
	for entity in match:
		s = s.replace("&"+entity+";", aEntities[entity])
	return s

params=get_params()

vod=None
post=None
url=None
name=None
mode=None
imageDir = 'special://home/plugins/video/Magyar TV/resources/images/'

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass
try:
        vod=str(params["vod"])
except:
        pass
try:
        post=urllib.unquote_plus(params["post"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "VOD: "+str(vod)
print "post: "+str(post)

if mode==0:
        #print ""+url
        CATEGORIES(url)
       
elif mode==1:
        #print ""+url
        #print ""+vod
        MAININDEX(url,vod)
        
elif mode==11:
        #print ""+url
        #print ""+vod
        SUBINDEX(url,vod)
        
elif mode==2:
        #print ""+url
        #print ""+vod
        VIDEOLINKS(url,name,vod)
        
elif mode==21:
        #print ""+url
        #print ""+str(name)
        #print ""+vod
        #print ""+post
        VIDEOLINKSNEXT(url,name,vod,post)
else:
	addDir('Élő','live',0,imageDir+'tv_stream.jpg','')
	addDir('Videótár','vod',0,'','')



xbmcplugin.endOfDirectory(int(sys.argv[1]))
