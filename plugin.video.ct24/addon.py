# coding: utf-8
# pylint: disable=import-error

import json
import sys
import urllib.request
from urllib.parse import parse_qsl

import xbmcaddon
import xbmcplugin
import xbmcgui


addon = xbmcaddon.Addon()
addon_id = addon.getAddonInfo("id")
handle = int(sys.argv[1])

def route(paramstring):
    li = xbmcgui.ListItem(label="ČT24 Živé vysílání")
    li.setProperty("IsPlayable", "true")
    li.setArt({
        "icon": f"special://home/addons/{addon_id}/icon.png",
        "thumb": f"special://home/addons/{addon_id}/icon.png",
        "clearlogo": f"special://home/addons/{addon_id}/resources/d9de0907-7dd6-4ce4-aceb-f0c6c4ae9a29.png"
        })
    it = li.getVideoInfoTag(offscreen=True)
    it.setTitle("ČT24")
    it.setStudios(["Česká televize"])
    it.setGenres(["News"])
    it.setPlot(addon.getAddonInfo("description"))
    it.setPlaycount(0)

    # plugin://plugin.video.ct24/?action=play
    params = dict(parse_qsl(paramstring[1:]))

    if not params:
        xbmcplugin.addDirectoryItem(handle, f"{sys.argv[0]}?action=play", li, False)
        xbmcplugin.endOfDirectory(handle)
    elif params.get("action") == "play":
        URL = "https://api.ceskatelevize.cz/video/v1/playlist-live/v1/stream-data/channel/CH_24?canPlayDrm=false&streamType=flash&quality=web&maxQualityCount=2"
        with urllib.request.urlopen(URL) as res:
            content = res.read()
        data = json.loads(content)
        stream_url = data["streamUrls"]["main"]

        li.setPath(stream_url)
        xbmcplugin.setResolvedUrl(handle, True, listitem=li)
    else:
        raise ValueError(f"Invalid url for plugin:// protocol. Unknown action param: {paramstring}")


if __name__ == "__main__":
    route(sys.argv[2])
