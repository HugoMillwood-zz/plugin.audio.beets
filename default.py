import collections
import itertools
import json
import sys
import urllib
import urllib2
import xbmcgui
import xbmcplugin
import xbmcaddon

# ADDON DATA
beets = xbmcaddon.Addon('plugin.audio.beets')
addon_handle = int(sys.argv[1])
xbmcplugin.setContent(addon_handle, 'audio')

# SETTINGS

ip_address = beets.getSetting('ip')
port = beets.getSetting('port')

# ??

#args = urlparse.parse_qs(sys.argv[2][1:])

# FUNCTIONS
def consume(iterator, n):
	collections.deque(itertools.islice(iterator, n))

# TODO
# Figure out how to make navigation work
def presentData(data):
	for element in data:
		li = xbmcgui.ListItem(element, iconImage='DefaultAudio.png')
		url = "plugin://"
		#li.setProperty('fanart_image', beets.getAddonInfo('fanart'))
		xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
	xbmcplugin.endOfDirectory(addon_handle)

# TODO - API
# - Get all songs by artist
# - Get all albums

# TODO
# - Return some sort of tuple with track ID so the API call can be generated
# - Might want to return artist as well so songs with the same name can be distinguished from one another
def getSearchSongs(query):
	apiRequest = json.load(urllib2.urlopen('http://' + ip_address + ':' + port + '/item/query/title:' + query))
	result = apiRequest.get('results')
	songs = [];
	if (result != None):
		iterator = range(0, len(result)).__iter__()
		for number in iterator:
			title = result[number].get('title').encode("UTF-8")
			songs.append(title)
			songs.sort()
	return songs
	
# TODO
# - Return some sort of tuple with track ID so the API call can be generated
# Who would use this?
def getAllSongs():
	apiRequest = json.load(urllib2.urlopen('http://' + ip_address + ':' + port + '/item/'))
	result = apiRequest.get('items')
	songs = [];
	if (result != None):
		iterator = range(0, len(result)).__iter__()
		for number in iterator:
			title = result[number].get('title').encode("UTF-8")
			songs.append(title)
			songs.sort()
	return songs

# TODO
# - Sort after track id
# - Return some sort of tuple with track ID so the API call can be generated
def getAlbumSongs(albumID):
	apiRequest = json.load(urllib2.urlopen('http://' + ip_address + ':' + port + '/item/query/album_id:' + str(albumID)))
	result = apiRequest.get('results')
	songs = [];
	if (result != None):
		iterator = range(0, len(result)).__iter__()
		for number in iterator:
			title = result[number].get('title').encode("UTF-8")
			songs.append(title)
	return songs

# TODO
# - Return some sort of tuple with album ID so the next API call can be generated
def getArtistAlbums(artist):
	apiRequest = json.load(urllib2.urlopen('http://' + ip_address + ':' + port + '/album/'))
	result = apiRequest.get('albums')
	albums = [];
	if (result != None):
		iterator = range(0, len(result)).__iter__()
		for number in iterator:
			albumArtist = result[number].get('albumartist').encode("UTF-8")
			if (albumArtist == artist):
				album = result[number].get('album').encode("UTF-8")
				albums.append(album)
	albums.sort()
	return albums

# TODO
# - Return some sort of tuple with artist ID so the next API call can be generated
def getArtists():
	apiRequest = json.load(urllib2.urlopen('http://' + ip_address + ':' + port + '/artist/'))
	result = apiRequest.get('artist_names')
	artists = [];
	if (result != None):
		iterator = range(0, len(result)).__iter__()
		for number in iterator:
			artist = result[number].encode("UTF-8")
			artists.append(artist)
	artists.sort()
	return artists

# MAIN
searchList = getSearchSongs("light")
songList = getAllSongs()
artistList = getArtists()
artistAlbumList = getArtistAlbums("Blackalicious")
albumSongs = getAlbumSongs(2)

#presentData(searchList)
#presentData(songList)
#presentData(artistAlbumList)
#presentData(artistList)
#presentData(albumSongs)