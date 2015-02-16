# plugin.audio.beets
A Kodi add-on for streaming music from a [beets](https://github.com/sampsyo/beets) library using the beets web plugin.

#Installation

The web plugin for beets needs to be running on the server you want to stream from. Make sure you have it installed and run:

	# beet web &

This creates a web server session detached from your shell. Skip the ``&`` if you want the session to stay in your shell to see the API calls.

Now install the add-on in Kodi. For now you have to install it from the .zip archive. Configure the server settings via Kodi as you need to specify the host address and port. The default port for beets web plugin is ``8337``.

*We don't even provide a .zip archive yet. The development is at a very early stage but if you're eager to try it out you can install it manually.*

# Authors
[Hugo Millwood](https://github.com/HugoMillwood) and [Pär Strindevall](https://github.com/parski). Feel free to fork!

#License
plugin.audio.beets is distributed under the Simplified BSD license. See [LICENSE](https://github.com/HugoMillwood/plugin.audio.beets/blob/master/LICENSE) for more information.
