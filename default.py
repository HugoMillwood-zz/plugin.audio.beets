import sys
import xbmcgui
import xbmcplugin
import xbmcaddon

import json
import urllib2
import urllib
import itertools, collections

beets = xbmcaddon.Addon('plugin.audio.beets')
addon_handle = int(sys.argv[1])
xbmcplugin.setContent(addon_handle, 'audio')

def consume(iterator, n):
	collections.deque(itertools.islice(iterator, n))

ip_address = "192.168.1.2"
port = "8337"

data = json.load(urllib2.urlopen('http://'+ip_address+':'+port+'/album/'))
#print(data)
result = data.get('albums')
print("BEGIN")
if (result != None):
	iterator = range(1, len(result)).__iter__()
	previousArtist = ""
	for number in iterator:
		artist = result[number].get('albumartist').encode("UTF-8") #THIS IS HILAAAAR
		print("iterates")
		print(artist)
		id = result[number].get('id')
		url = 'http://'+ip_address+':'+str(port)+'/item/'+str(id)+'/file'
		li = xbmcgui.ListItem(artist, iconImage='DefaultAudio.png')
		li.setProperty('fanart_image', beets.getAddonInfo('fanart'))
		if (artist != previousArtist):
			xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
			previousArtist = artist
print("FIN")
xbmcplugin.endOfDirectory(addon_handle)

