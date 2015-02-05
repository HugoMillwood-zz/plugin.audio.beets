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

data = json.load(urllib2.urlopen('http://'+ip_address+':'+port+'/item/query/Battles'))

result = data.get('results')
iterator = range(1, len(result)).__iter__()

for number in iterator:
        artist = result[number].get('artist')                                                                                       
        title = result[number].get('title')                                                                                         
        album = result[number].get('album')                                                                                         
        genre = result[number].get('genre')                                                                                         
        year = result[number].get('year')                                                                                           
        track = result[number].get('track')                                                                                         
        id = result[number].get('id')                                                                                               
        url = 'http://'+ip_address+':'+str(port)+'/item/'+str(id)+'/file'                                                           
        li = xbmcgui.ListItem(artist+' - '+title, iconImage='DefaultAudio.png')                                                     
        li.setProperty('fanart_image', beets.getAddonInfo('fanart'))                                                                
        li.setInfo('music', { 'genre': genre, 'album': album, 'artist': artist, 'title': title, 'year': year, 'tracknumber': track})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

xbmcplugin.endOfDirectory(addon_handle)

