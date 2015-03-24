import collections
import httplib
import itertools
import json
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
version = beets.getAddonInfo('version')
addon_handle = int(sys.argv[1])
xbmcplugin.setContent(addon_handle, 'audio')
xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER)

# SETTINGS

ip_address = beets.getSetting('ip')
port = beets.getSetting('port')

tls_ssl = False
if (beets.getSetting('tls_ssl') == 'true'):
	tls_ssl = True

debug = False
if (beets.getSetting('debug') == 'true'):
	debug = True

protocol = 'http://'
if (tls_ssl):
	protocol = 'https://'

# PRESENTATION CONSTANTS

ARTISTS 		= 0		# All artists
ALBUMS 			= 1		# All albums
SONGS 			= 2		# All songs
ARTIST_ALBUMS 		= 3		# All albums by an artist
ARTIST_SONGS		= 4		# All songs by an artist
ALBUM_SONGS		= 5		# All songs on an album
PLAY_SONG     = 6   # Play the selected song

# SESSION

args = urlparse.parse_qs(sys.argv[2][1:])

# DEBUG

def printdbg(message):
	if (debug):
		print('Add-on ' + plugin + '.' + version + ': ' + str(message))

# META DATA

def trackNumberComparator():
	def compare_two_dicts(x, y):
		return cmp(x['track'], y['track'])
	return compare_two_dicts
	
def trackTitleComparator():
	def compare_two_dicts(x, y):
		return cmp(x['title'], y['title'])
	return compare_two_dicts

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
	albumID = str(song['album_id'])
	albumArt = getAlbumArt(albumID)
	li = xbmcgui.ListItem(metaDataDict['title'], iconImage=albumArt, thumbnailImage=albumArt)
	li.setInfo(type='music', infoLabels = metaDataDict)
	return li
	
def getMetaDataListItemWithArtist(song):
	li = getMetaDataListItem(song)
	li.setLabel(song['title'] + ' - ' + song['artist'])
	return li

confirmedMissing = confirmedExist = set()

def getAlbumArt(album):
	albumArtURI = '/album/' + str(album) + '/art'
	if (str(album) not in confirmedMissing | confirmedExist):
		printdbg('Fetching album art for album ' + str(album) + '.')
		probe = httplib.HTTPConnection(ip_address, port)
		probe.request('GET', albumArtURI)
		response = probe.getresponse()
		if (response.status == 200):
			printdbg('Caching album art for album ' + str(album) + '.')
			confirmedExist.add(str(album))
			albumArt = protocol + ip_address + ':' + port + albumArtURI
		else:
			printdbg('Album art for album ' + str(album) + ' is missing.')
			confirmedMissing.add(str(album))
			albumArt = 'DefaultAudio.png'
	elif (str(album) in confirmedExist):
		albumArt = protocol + ip_address + ':' + port + albumArtURI
	else:
		albumArt = 'DefaultAudio.png'
	return albumArt

# DIRECTORY POPULATION

def presentData(data):
	if (data[0] == ARTISTS):
		for element in data[1]:
			li = xbmcgui.ListItem(element, iconImage='DefaultAudio.png')
			url = 'plugin://' + plugin + '?view=' + str(ARTIST_ALBUMS) + '&artist=' + urllib.pathname2url(element)
			xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
	elif (data[0] == ALBUMS):
		data[1].sort(key=lambda x: x[0].lower())
		for element in data[1]:
			albumID = element[1]
			albumArt = getAlbumArt(albumID)
			li = xbmcgui.ListItem(element[0], iconImage=albumArt)
			url = 'plugin://' + plugin + '?view=' + str(ALBUM_SONGS) + '&album_id=' + str(albumID)
			xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
	elif (data[0] == SONGS):
		songs = data[1][0][2]
		songs.sort(trackTitleComparator())
		for song in songs:
			li = getMetaDataListItemWithArtist(song)
			url = 'plugin://' + plugin + '?view=' + str(PLAY_SONG) + '&song_id=' + str(song['id'])
			#url = protocol + ip_address + ':' + port + '/item/' + str(song['id']) + '/file'
			xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
	elif (data[0] == ARTIST_ALBUMS):
		data[1].sort(key=lambda x: int(x[2]))
		data[1].reverse()
		for element in data[1]:
			albumID = element[1]
			albumArt = getAlbumArt(albumID)
			li = xbmcgui.ListItem(element[0], iconImage=albumArt)
			url = 'plugin://' + plugin + '?view=' + str(ALBUM_SONGS) + '&album_id=' + str(albumID)
			xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
		li = xbmcgui.ListItem('All songs by ' + args.get('artist', None)[0], iconImage='DefaultAudio.png')
		url = 'plugin://' + plugin + '?view=' + str(ARTIST_SONGS) + '&artist=' + args.get('artist', None)[0]
		xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
	elif (data[0] == ALBUM_SONGS):
		songs = data[1][0][2]
		songs.sort(trackNumberComparator())
		for song in songs:
			li = getMetaDataListItem(song)
			url = 'plugin://' + plugin + '?view=' + str(PLAY_SONG) + '&song_id=' + str(song['id'])
			#url = protocol + ip_address + ':' + port + '/item/' + str(song['id']) + '/file'
			xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
	elif (data[0] == ARTIST_SONGS):
		songs = data[1][0][2]
		songs.sort(trackTitleComparator())
		for song in songs:
			li = getMetaDataListItem(song)
			url = 'plugin://' + plugin + '?view=' + str(PLAY_SONG) + '&song_id=' + str(song['id'])
			#url = protocol + ip_address + ':' + port + '/item/' + str(song['id']) + '/file'
			#li.setProperty('fanart_image', beets.getAddonInfo('fanart'))
			xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
	xbmcplugin.endOfDirectory(addon_handle)

# BEETS WEB API CALLS

# TODO
# - Return some sort of tuple with track ID so the API call can be generated
# - Might want to return artist as well so songs with the same name can be distinguished from one another
def getSearchSongs(query):
	apiRequest = json.load(urllib2.urlopen(protocol + ip_address + ':' + port + '/item/query/title:' + query))
	result = apiRequest.get('results')
	songs = [];
	if (result != None):
		iterator = range(0, len(result)).__iter__()
		for number in iterator:
			title = result[number].get('title').encode('UTF-8')
			songs.append(title)
			songs.sort()
	return songs

def getSong(songID):
	printdbg("URL: " + protocol + ip_address + ':' + port + '/item/' + songID)
	apiRequest = json.load(urllib2.urlopen(protocol + ip_address + ':' + port + '/item/' + songID))
	result = apiRequest
	return result

def getAllSongs():
	apiRequest = json.load(urllib2.urlopen(protocol + ip_address + ':' + port + '/item/'))
	result = apiRequest.get('items')
	songs = [];
	if (result != None):
		iterator = range(0, len(result)).__iter__()
		for number in iterator:
			title = result[number].get('title').encode('UTF-8')
			song_id = result[number].get('id')
			songs.append([title, song_id, result])
			songs.sort()
	return SONGS, songs

def getAlbumSongs(albumID):
	apiRequest = json.load(urllib2.urlopen(protocol + ip_address + ':' + port + '/item/query/album_id:' + str(albumID)))
	result = apiRequest.get('results')
	songs = [];
	if (result != None):
		iterator = range(0, len(result)).__iter__()
		for number in iterator:
			title = result[number].get('title').encode('UTF-8')
			song_id = result[number].get('id')
			songs.append([title, song_id, result])
	return ALBUM_SONGS, songs

def playSong(songID):
	song = getSong(songID)
	li = getMetaDataListItem(song)
	url = protocol + ip_address + ':' + port + '/item/' + songID + '/file'
	xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play(url, li)

def getArtistAlbums(artist):
	apiRequest = json.load(urllib2.urlopen(protocol + ip_address + ':' + port + '/album/query/albumartist:' + urllib.pathname2url(artist)))
	result = apiRequest.get('results')
	albums = [];
	if (result != None):
		iterator = range(0, len(result)).__iter__()
		for number in iterator:
			albumArtist = result[number].get('albumartist').encode('UTF-8')
			if (albumArtist == artist):
				album = result[number].get('album').encode('UTF-8')
				album_id = result[number].get('id')
				album_year = result[number].get('year')
				albums.append([album, album_id, album_year])
	albums.sort()
	return ARTIST_ALBUMS, albums
	
def getArtistSongs(artist):
	apiRequest = json.load(urllib2.urlopen(protocol + ip_address + ':' + port + '/item/query/artist:' + urllib.pathname2url(artist)))
	result = apiRequest.get('results')
	songs = [];
	if (result != None):
		iterator = range(0, len(result)).__iter__()
		for number in iterator:
			title = result[number].get('title').encode('UTF-8')
			song_id = result[number].get('id')
			songs.append([title, song_id, result])
	return ARTIST_SONGS, songs
	
def getAlbums():
	apiRequest = json.load(urllib2.urlopen(protocol + ip_address + ':' + port + '/album/'))
	result = apiRequest.get('albums')
	albums = [];
	if (result != None):
		iterator = range(0, len(result)).__iter__()
		for number in iterator:
			album = result[number].get('album').encode('UTF-8')
			album_id = result[number].get('id')
			albums.append([album, album_id])
	albums.sort()
	return ALBUMS, albums

def getArtists():
	apiRequest = json.load(urllib2.urlopen(protocol + ip_address + ':' + port + '/artist/'))
	result = apiRequest.get('artist_names')
	artists = [];
	if (result != None):
		iterator = range(0, len(result)).__iter__()
		for number in iterator:
			artist = result[number].encode('UTF-8')
			artists.append(artist)
	artists.sort()
	return ARTISTS, artists

# NAVIGATION

'''
#if plugin just started, run these:
# if connection to beets cannot be established
#	show modal pointing out the absense of a connection
#	debug print stuff
# else
	printdbg('Add-on started in debug mode.')
	if (tls_ssl):
		printdbg('TLS/SSL protocol enabled.')
	printdbg('Arguments: ' + str(args))
'''

if (args.get('view', None) == None):
	li = xbmcgui.ListItem('Artists', iconImage='DefaultAudio.png')
	url = 'plugin://' + plugin + '?view=' + str(ARTISTS)
	xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
	li = xbmcgui.ListItem('Albums', iconImage='DefaultAudio.png')
	url = 'plugin://' + plugin + '?view=' + str(ALBUMS)
	xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
	li = xbmcgui.ListItem('Songs', iconImage='DefaultAudio.png')
	url = 'plugin://' + plugin + '?view=' + str(SONGS)
	xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
	'''
	li = xbmcgui.ListItem('Search...', iconImage='DefaultAudio.png')
	url = 'plugin://' + plugin
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
elif (int(args.get('view', None)[0]) == PLAY_SONG):
	playSong(str(args.get('song_id', None)[0]))
else:
	printdbg('Invalid view argument. Arguments: ' + str(args))
