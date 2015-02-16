import collections
import itertools
import json
import operator #itemgetter for advanced nestled sorting
import sys
import urllib
import urllib2
import urlparse
import xbmcgui
import xbmcplugin
import xbmcaddon

# ADDON DATA
plugin = 'plugin.audio.beets'
beets = xbmcaddon.Addon(plugin)
addon_handle = int(sys.argv[1])
xbmcplugin.setContent(addon_handle, 'audio')

# SETTINGS

ip_address = beets.getSetting('ip')
port = beets.getSetting('port')

# PRESENTATION CONSTANTS

ARTISTS 		= 0		# All artists
ALBUMS 			= 1		# All albums
SONGS 			= 2		# All songs
ARTIST_ALBUMS 		= 3		# All albums by an artist
ARTIST_SONGS		= 4		# All songs by an artist
ALBUM_SONGS		= 5		# All song on an album

# SESSION

args = urlparse.parse_qs(sys.argv[2][1:])

# DEBUG

print(args)

# META DATA

def getMetaDataListItem(song):
	metaDataDict = {'title': song['title']}
	if (song['artist'] != None):
		metaDataDict['artist'] = str(song['artist'].encode('UTF-8'))
	if (song['album'] != None):
		metaDataDict['album'] = str(song['album'].encode('UTF-8'))
	if (song['genre'] != None):
		metaDataDict['genre'] = str(song['genre'].encode('UTF-8'))
	if (song['year'] != None):
		metaDataDict['year'] = int(song['year'])
	if (song['track'] != None):
		metaDataDict['tracknumber'] = int(song['track'])
        if (song['length'] != None):
	        metaDataDict['duration'] = int(song['length'])

	print(metaDataDict)
	li = xbmcgui.ListItem(metaDataDict['title'], iconImage='DefaultAudio.png')
	li.setInfo(type='music', infoLabels = metaDataDict)
	return li

# DIRECTORY POPULATION

def presentData(data):
	if (data[0] == ARTISTS):
		for element in data[1]:
			li = xbmcgui.ListItem(element, iconImage='DefaultAudio.png')
			url = "plugin://" + plugin + "?view=" + str(ARTIST_ALBUMS) + "&artist=" + urllib.pathname2url(element)
			#li.setProperty('fanart_image', beets.getAddonInfo('fanart'))
			xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
	elif (data[0] == ALBUMS):
		for element in data[1]:
			li = xbmcgui.ListItem(element[0], iconImage='DefaultAudio.png')
			url = "plugin://" + plugin + "?view=" + str(ALBUM_SONGS) + "&album_id=" + str(element[1])
			#li.setProperty('fanart_image', beets.getAddonInfo('fanart'))
			xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
	elif (data[0] == SONGS):
		for element in data[1][0][2]:
			label = element['title']
			if (element['artist'] != None):
				label = label + ' - ' + element['artist']
			li = xbmcgui.ListItem(label, iconImage='DefaultAudio.png')
			url = "plugin://"
			#li.setProperty('fanart_image', beets.getAddonInfo('fanart'))
			xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
	elif (data[0] == ARTIST_ALBUMS):
		for element in data[1]:
			li = xbmcgui.ListItem(element[0], iconImage='DefaultAudio.png')
			url = "plugin://" + plugin + "?view=" + str(ALBUM_SONGS) + "&album_id=" + str(element[1])
			#li.setProperty('fanart_image', beets.getAddonInfo('fanart'))
			xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
		li = xbmcgui.ListItem('All songs by ' + args.get('artist', None)[0], iconImage='DefaultAudio.png')
		url = "plugin://" + plugin + "?view=" + str(ARTIST_SONGS) + '&artist=' + args.get('artist', None)[0]
		#li.setProperty('fanart_image', beets.getAddonInfo('fanart'))
		xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
	elif (data[0] == ALBUM_SONGS):
		for element in data[1][0][2]:
			#li = xbmcgui.ListItem(element['title'].encode('UTF-8'), iconImage='DefaultAudio.png')
			li = getMetaDataListItem(element)
			url = 'http://' + ip_address + ':' + port + '/item/' + str(element['id']) + '/file'
			li.setProperty('fanart_image', beets.getAddonInfo('fanart'))
			xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
	elif (data[0] == ARTIST_SONGS):
		for element in data[1]:
			li = xbmcgui.ListItem(element[0], iconImage='DefaultAudio.png')
			url = 'http://' + ip_address + ':' + port + '/item/' + str(element[1]) + '/file'
			#li.setProperty('fanart_image', beets.getAddonInfo('fanart'))
			xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
	xbmcplugin.endOfDirectory(addon_handle)

# BEETS WEB API CALLS

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

def getAllSongs():
	apiRequest = json.load(urllib2.urlopen('http://' + ip_address + ':' + port + '/item/'))
	result = apiRequest.get('items')
	songs = [];
	if (result != None):
		iterator = range(0, len(result)).__iter__()
		for number in iterator:
			title = result[number].get('title').encode("UTF-8")
			song_id = result[number].get('id')
			songs.append([title, song_id, result])
			songs.sort()
	return SONGS, songs

# TODO
# - Sort after track number
def getAlbumSongs(albumID):
	apiRequest = json.load(urllib2.urlopen('http://' + ip_address + ':' + port + '/item/query/album_id:' + str(albumID)))
	result = apiRequest.get('results')
	songs = [];
	if (result != None):
		iterator = range(0, len(result)).__iter__()
		for number in iterator:
			title = result[number].get('title').encode("UTF-8")
			song_id = result[number].get('id')
			songs.append([title, song_id, result])
	return ALBUM_SONGS, songs

def getArtistAlbums(artist):
	apiRequest = json.load(urllib2.urlopen('http://' + ip_address + ':' + port + '/album/query/albumartist:' + urllib.pathname2url(artist)))
	result = apiRequest.get('results')
	albums = [];
	if (result != None):
		iterator = range(0, len(result)).__iter__()
		for number in iterator:
			albumArtist = result[number].get('albumartist').encode("UTF-8")
			if (albumArtist == artist):
				album = result[number].get('album').encode("UTF-8")
				album_id = result[number].get('id')
				albums.append([album, album_id])
	albums.sort()
	return ARTIST_ALBUMS, albums
	
def getArtistSongs(artist):
	apiRequest = json.load(urllib2.urlopen('http://' + ip_address + ':' + port + '/item/query/artist:' + urllib.pathname2url(artist)))
	result = apiRequest.get('results')
	songs = [];
	if (result != None):
		iterator = range(0, len(result)).__iter__()
		for number in iterator:
			title = result[number].get('title').encode("UTF-8")
			song_id = result[number].get('id')
			songs.append([title, song_id])
	return ARTIST_SONGS, songs
	
def getAlbums():
	apiRequest = json.load(urllib2.urlopen('http://' + ip_address + ':' + port + '/album/'))
	result = apiRequest.get('albums')
	albums = [];
	if (result != None):
		iterator = range(0, len(result)).__iter__()
		for number in iterator:
			album = result[number].get('album').encode("UTF-8")
			album_id = result[number].get('id')
			albums.append([album, album_id])
	albums.sort()
	return ALBUMS, albums

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
	return ARTISTS, artists

# NAVIGATION

if (args.get('view', None) == None):
	li = xbmcgui.ListItem('Artists', iconImage='DefaultAudio.png')
	url = "plugin://" + plugin + '?view=' + str(ARTISTS)
	xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
	li = xbmcgui.ListItem('Albums', iconImage='DefaultAudio.png')
	url = "plugin://" + plugin + '?view=' + str(ALBUMS)
	xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
	li = xbmcgui.ListItem('Songs', iconImage='DefaultAudio.png')
	url = "plugin://" + plugin + '?view=' + str(SONGS)
	xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
	'''
	li = xbmcgui.ListItem('Search...', iconImage='DefaultAudio.png')
	url = "plugin://" + plugin
	xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
	'''
	xbmcplugin.endOfDirectory(addon_handle)
elif (int(args.get('view', None)[0]) == ARTISTS):
	presentData(getArtists())
elif (int(args.get('view', None)[0]) == ALBUMS):
	presentData(getAlbums())
elif (int(args.get('view', None)[0]) == ARTIST_ALBUMS):
	presentData(getArtistAlbums(str(args.get('artist', None)[0])))
elif (int(args.get('view', None)[0]) == ALBUM_SONGS):
	presentData(getAlbumSongs(str(args.get('album_id', None)[0])))
elif (int(args.get('view', None)[0]) == ARTIST_SONGS):
	presentData(getArtistSongs(str(args.get('artist', None)[0])))
elif (int(args.get('view', None)[0]) == SONGS):
	presentData(getAllSongs())
else:
	print('DEBUG: Whatever happened to view? Get your args straight.')

#searchList = getSearchSongs("light")
#songList = getAllSongs()
#presentData(searchList)
#presentData(songList)
