# plugin.audio.beets
<img src="https://raw.githubusercontent.com/HugoMillwood/plugin.audio.beets/master/icon.png"  width="192" height="250" alt="Such a nifty logo.">

A Kodi add-on for streaming music from a [beets](https://github.com/sampsyo/beets) library using the beets web plugin.

#Installation

The web plugin for beets needs to be running on the server you want to stream from. Make sure you have it installed and run:

	# beet web &

This creates a web server session detached from your shell. Skip the ``&`` if you want the session to stay in your shell to see the API calls.

Now install the add-on in Kodi. For now you have to install it from the .zip archive. Configure the server settings via Kodi as you need to specify the host address and port. The default port for beets web plugin is ``8337``.

*We don't even provide a .zip archive yet. The development is at a very early stage but if you're eager to try it out you can install it manually.*

###**_Important!_**

We haven't been able to get things working with Kodi's PAPlayer (the default audio player in Kodi) with streaming FLAC. This plugin will at the moment not work without switching the default audio player to DVDPlayer. This is easy to do, just add the following as a setting in the audio tag of your ``<userdata>/advancedsettings.xml``:

	  <defaultplayer>dvdplayer</defaultplayer>

If you don't have a ``advancedsettings.xml`` you can create one containing the following:

	<advancedsettings>
    	<audio>
	  		<defaultplayer>dvdplayer</defaultplayer>
		</audio>
	</advancedsettings>
	
This will set the default audio player to DVDPlayer and allow you to stream FLAC (among other supported formats) with metadata.

The userdata directory is located in different places depending on your platform. The most common places:

- Linux: ``~/.kodi/userdata/``
- OS X: ``/Users/<your_user_name>/Library/Application Support/kodi/userdata/``
- Windows: ``%APPDATA%\kodi\userdata``
- OpenELEC: ``/storage/.kodi/userdata/`` 

More information regarding [userdata](http://kodi.wiki/view/Userdata) and [advancedsettings.xml](http://kodi.wiki/view/Advancedsettings.xml).

# Authors
[Hugo Millwood](https://github.com/HugoMillwood) and [Pär Strindevall](https://github.com/parski). Feel free to fork!

#License
plugin.audio.beets is distributed under the Simplified BSD license. See [LICENSE](https://github.com/HugoMillwood/plugin.audio.beets/blob/master/LICENSE) for more information.
