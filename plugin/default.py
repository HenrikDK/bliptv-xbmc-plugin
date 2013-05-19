'''
    BlipTV plugin for XBMC
    Copyright (C) 2010-2011 Tobias Ussing And Henrik Mosgaard Jensen

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import sys
import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin
import urllib2
import cookielib

try: import xbmcvfs
except: import xbmcvfsdummy as xbmcvfs

# plugin constants
version = "0.8.0"
plugin = "BlipTV Beta-" + version
author = "TheCollective"
url = "www.xbmc.com"

# xbmc hooks
settings = xbmcaddon.Addon(id='plugin.video.bliptv.beta')
language = settings.getLocalizedString
dbg = settings.getSetting("debug") == "true"
dbglevel = 3

# plugin structure 
scraper = ""
navigation = ""
downloader = ""
storage = ""
player = ""
common = ""
utils = ""

cookiejar = cookielib.LWPCookieJar()
cookie_handler = urllib2.HTTPCookieProcessor(cookiejar)
opener = urllib2.build_opener(cookie_handler)

if (__name__ == "__main__" ):
    if dbg:
        print plugin + " ARGV: " + repr(sys.argv)
    else:
        print plugin

    try:
        import StorageServer
        cache = StorageServer.StorageServer("BlipTV")
    except:
        import storageserverdummy as StorageServer
        cache = StorageServer.StorageServer("BlipTV")

    import CommonFunctions as common
    common.plugin = plugin
    import BlipTVUtils as utils
    utils = utils.BlipTVUtils()
    import BlipTVStorage as storage
    storage = storage.BlipTVStorage()
    import BlipTVPlayer as player
    player = player.BlipTVPlayer()
    import SimpleDownloader as downloader
    downloader = downloader.SimpleDownloader()
    import BlipTVScraper as scraper
    scraper = scraper.BlipTVScraper()
    import BlipTVNavigation as navigation
    navigation = navigation.BlipTVNavigation()

    if (not settings.getSetting("firstrun")):
        settings.setSetting("firstrun", "1")

    if (not sys.argv[2]):
        navigation.listMenu()
    else:
        params = common.getParameters(sys.argv[2])
        get = params.get
        if (get("action")):
            navigation.executeAction(params)
        elif (get("path")):
            navigation.listMenu(params)

    #import fbLogin
    #oauth_url = "https://www.facebook.com/dialog/oauth?display=popup&domain=blip.tv&scope=email&e2e=%7B%7D&app_id=136482209767138&locale=en_US&sdk=joey&client_id=136482209767138&redirect_uri=http%3A%2F%2Fstatic.ak.facebook.com%2Fconnect%2Fxd_arbiter.php%3Fversion%3D24%23cb%3Df1ec7ef034f6e36%26origin%3Dhttp%253A%252F%252Fblip.tv%252Ff19fa655d24faaa%26domain%3Dblip.tv%26relation%3Dopener%26frame%3Df4a8273bce9c22&origin=1&response_type=token%2Csigned_request"
    #callback_url = "http://blip.tv/facebook/verify_viewer_user"
    #fbLogin.login(oauth_url, callback_url)
