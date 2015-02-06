import sys
import xbmcgui
import xbmcplugin
import xbmcaddon

import json
import urllib2
import urllib
import itertools, collections

# ADDON DATA
beets = xbmcaddon.Addon('plugin.audio.beets')
addon_handle = int(sys.argv[1])
xbmcplugin.setContent(addon_handle, 'audio')

# SETTINGS

ip_address = beets.getSetting('ip')
port = beets.getSetting('port')

# ??

args = urlparse.parse_qs(sys.argv[2][1:])

# FUNCTIONS
def consume(iterator, n):
	collections.deque(itertools.islice(iterator, n))
	
#def presentData(dataList):

def getArtists():
	print("DEBUG: Fetching artist data.")
	data = json.load(urllib2.urlopen('http://'+ip_address+':'+port+'/artist/'))
	result = data.get('artist_names')
	if (result != None):
		iterator = range(1, len(result)).__iter__()
		previousArtist = ""
		for number in iterator:
			artist = result[number].encode("UTF-8") #THIS IS HILAAAAR
			#artist = result[number].get().encode("UTF-8")
			#id = result[number].get('id')
			#url = 'http://'+ip_address+':'+str(port)+'/item/'+str(id)+'/file'
			url = "doubleyoudoubleyoudoubleyoudotwhatevermandotcom"
			li = xbmcgui.ListItem(artist, iconImage='DefaultAudio.png')
			#li.setProperty('fanart_image', beets.getAddonInfo('fanart'))
			if (artist != previousArtist):
				xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
				previousArtist = artist
		xbmcplugin.endOfDirectory(addon_handle)

# MAIN
getArtists()