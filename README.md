# plugin.audio.beets
<img src="https://raw.githubusercontent.com/HugoMillwood/plugin.audio.beets/master/icon.png"  width="192" height="250" alt="Such a nifty logo.">

A Kodi add-on for streaming music from a [Beets](https://github.com/sampsyo/beets) library using the Beets web plugin.

##Installation

The easiest way to install this add-on at the moment is to ```git clone``` this repository into your add-on directory of your Kodi installation.

Like so:

```shell
$ git clone https://github.com/HugoMillwood/plugin.audio.beets.git <addon directory>/plugin.audio.beets
```

For example:

```shell
$ git clone https://github.com/HugoMillwood/plugin.audio.beets.git /usr/share/kodi/addons/plugin.audio.beets
```

Or you can just ``cd`` into your add-on directory and run:

```shell
$ git clone https://github.com/HugoMillwood/plugin.audio.beets.git
```

The add-on directory is located in different places depending on your platform.

| OS       | Path							|
|----------|------------------------------------------------------------|
| Linux    | ``/usr/share/kodi/addons`` 				|
| OS X     | ``/Applications/Kodi.app/Contents/Resources/Kodi/addons`` 	|
| Windows  | ``%PROGRAMFILES(x86)%\XBMC\addons`` 			|
| OpenELEC | ``/storage/.kodi/addons`` 					|

To update the add-on you just have to ``git pull`` in the cloned directory.

Like so:

```shell
$ git -C <addon directory>/plugin.audio.beets pull
```

Or you can just ``cd`` into your cloned directory and run:

```shell
$ git pull
```

##Configuration

There are two necessary settings for the add-on to function properly:

| Setting    | Description							|
|------------|------------------------------------------------------------------|
| IP Address | The IP address of the host running Beets and the web plugin. 	|
| Port       | The port of the Beets web plugin server.				|

*Note that you only have to change the port if you're not using the default* ``8337`` *port.*

Make sure you are [using](http://beets.readthedocs.org/en/latest/plugins/index.html#using-plugins) the [web plugin](http://beets.readthedocs.org/en/latest/plugins/web.html) on your server running Beets. If you want album art to be displayed in Kodi you must also use the [fetchart](http://beets.readthedocs.org/en/latest/plugins/fetchart.html) plugin.

The web plugin for Beets needs to be running on the server you want to stream from.

On your server:

```shell
$ beet web &
```

This creates a web server session detached from your shell. Skip the ``&`` if you want the session attached.

Configure the add-on using the Kodi user interface:

**System ➜ Settings ➜ Add-ons ➜ Enabled Add-ons ➜ Music Add-ons ➜ Beets ➜ Configure**

###**_Important!_**

We [haven't](http://forum.kodi.tv/showthread.php?tid=218576) been able to get things working with PAPlayer (the default audio player in Kodi) with streaming FLAC. This plugin uses the DVDPlayer which does not have the curl buffer issues that we have been experiencing.

*Note that the directories listed in this README are bound to change. Check yourself before you wreck yourself.*

## Authors
[Hugo Millwood](https://github.com/HugoMillwood) and [Pär Strindevall](https://github.com/parski).

## License
plugin.audio.beets is distributed under the Simplified BSD license. See [LICENSE](https://github.com/HugoMillwood/plugin.audio.beets/blob/master/LICENSE).
