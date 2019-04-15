# ex:ts=4:sw=4:sts=4:et
# -*- tab-width: 4; c-basic-offset: 4; indent-tabs-mode: nil -*-
from __future__ import absolute_import, unicode_literals
import re
import json
from datetime import datetime, timedelta
from urllib.parse import urlparse

from svtplay_dl.service import Service, OpenGraphThumbMixin
from svtplay_dl.fetcher.hls import hlsparse
from svtplay_dl.error import ServiceError


class Tv4play(Service, OpenGraphThumbMixin):
    supported_domains = ['tv4play.se']

    def get(self):
        parse = urlparse(self.url)
        if parse.path[:8] == "/kanaler":
            end_time_stamp = (datetime.utcnow() - timedelta(minutes=1, seconds=20)).replace(microsecond=0)
            start_time_stamp = end_time_stamp - timedelta(minutes=1)

            url = "https://bbr-l2v.akamaized.net/live/{0}/master.m3u8?in={1}&out={2}?".format(parse.path[9:],
                                                                                              start_time_stamp.isoformat(),
                                                                                              end_time_stamp.isoformat())

            self.config.set("live", True)
            streams = hlsparse(self.config, self.http.request("get", url), url, output=self.output, hls_time_stamp=True)
            for n in list(streams.keys()):
                yield streams[n]
            return

        match = self._getjson()
        if not match:
            yield ServiceError("Can't find json data")
            return

        jansson = json.loads(match.group(1))

#        print(jansson)
#       https://www.tv4play.se/program/stieg-larsson-mannen-som-lekte-med-elden/11956126

#        vid = self._get_vid()
#        s = 'The vid ' + vid + ' ...'
#        print(s)

#        yield ServiceError("Test completed!")
#        return



#        vid = "11956126"
#        self.output["id"] = str(vid)
#        self.output["episodename"] = "det.enda.jag.har"
#        self.output["title"] = "stieg.larsson-mannen.som.lekte.med.elden"
#        self.output["season"] = 1
#        self.output["episode"] = 4

#       https://www.tv4play.se/program/lets-dance/11976963
#        vid = "11976963"
#        self.output["id"] = str(vid)
#        self.output["episodename"] = "test"
#        self.output["title"] = "after-dance"
#        self.output["season"] = 14
#        self.output["episode"] = 2
       
        print('-------------------------------------')
        print(jansson)
        print('-------------------------------------')
        for i in jansson:
            print(i)
        print('-------------------------------------')
        
        vid = None
        title = None

#        vid = jansson["props"]["pageProps"]["assetId"]

        if "pageProps" in jansson["props"]:            
            pageProps = jansson["props"]["pageProps"]
            if "nid" in pageProps:
                title = pageProps["nid"]
            if "assetId" in pageProps:
                vid = pageProps["assetId"]

        if "query" in jansson["props"]:
            query = jansson["props"]["query"]
            if "nid" in query:
                title = query["nid"]
            if "assetId" in query:
                vid = query["assetId"]

        print(vid)
        print(title)
        
        self.output["id"] = str(vid)
        self.output["title"] = title

        if "apolloState" in jansson["props"]:
            apolloState = jansson["props"]["apolloState"]          
#            for i in jansson["props"]["apolloState"]:
            for i in apolloState:
#               if "__typename" in jansson["props"]["apolloState"][i] and "VideoAsset" in jansson["props"]["apolloState"][i]["__typename"]:
#               print(">> " + i)
#               if "id" in jansson["props"]["apolloState"][i] and int(vid) == jansson["props"]["apolloState"][i]["id"]:
               if "id" in apolloState[i] and int(vid) == apolloState[i]["id"]:
                  print("#### " + i)
#                  if jansson["props"]["apolloState"][i]["is_drm_protected"]:
                  if apolloState[i]["is_drm_protected"]:
                    yield ServiceError("We can't download DRM protected content from this site.")
                    return
#                  if jansson["props"]["apolloState"][i]["live"]:
                  if apolloState[i]["live"]:
                      self.config.set("live", True)
#                  if "program_nid" in jansson["props"]["apolloState"][i]:
                  if "program_nid" in apolloState[i]:
                      self.output["title"] = apolloState[i]["program_nid"]
                      print("############## >> " + self.output["title"])
#                      self.output["title"] = jansson["props"]["apolloState"][i]["program_nid"]
                  if "season" in apolloState[i] and apolloState[i]["season"] > 0:
#                  if "season" in jansson["props"]["apolloState"][i] and jansson["props"]["apolloState"][i]["season"] > 0:
                      self.output["season"] = apolloState[i]["season"]
#                      self.output["season"] = jansson["props"]["apolloState"][i]["season"]
                  if "episode" in apolloState[i] and apolloState[i]["episode"] > 0:
#                  if "episode" in jansson["props"]["apolloState"][i] and jansson["props"]["apolloState"][i]["episode"] > 0:
                      self.output["episode"] = apolloState[i]["episode"]
#                      self.output["episode"] = jansson["props"]["apolloState"][i]["episode"]
                  if "slug" in apolloState[i]:
#                  if "slug" in jansson["props"]["apolloState"][i]:
                      self.output["episodename"] = apolloState[i]["slug"]
#                      self.output["episodename"] = jansson["props"]["apolloState"][i]["slug"]

        print(self.output["id"])
        print(self.output["title"])
        print(self.output["season"])
        print(self.output["episode"])
        print(self.output["episodename"])

#SuggestedEpisode
# "is_drm_protected": false,

#        yield ServiceError("Test Completed")
#        return

#        vid = None
#        for i in jansson:
#            print(i)
#            janson2 = json.loads(i["data"])
#            janson2 = json.loads(i["props"])
#            json.dumps(janson2)
#            if "videoAsset" in janson2["data"] and vid is None:
#                vid = janson2["data"]["videoAsset"]["id"]
#                if janson2["data"]["videoAsset"]["is_drm_protected"]:
#                    yield ServiceError("We can't download DRM protected content from this site.")
#                    return
#                if janson2["data"]["videoAsset"]["is_live"]:
#                    self.config.set("live", True)
#                if janson2["data"]["videoAsset"]["season"] > 0:
#                    self.output["season"] = janson2["data"]["videoAsset"]["season"]
#                if janson2["data"]["videoAsset"]["episode"] > 0:
#                    self.output["episode"] = janson2["data"]["videoAsset"]["episode"]
#                self.output["title"] = janson2["data"]["videoAsset"]["program"]["name"]
#                self.output["episodename"] = janson2["data"]["videoAsset"]["title"]
#                vid = str(vid)
#                self.output["id"] = str(vid)
#            if "program" in janson2["data"] and vid is None:
#                if "contentfulPanels" in janson2["data"]["program"]:
#                    match = re.search(r"[\/-](\d+)$", self.url)
#                    if match and "panels" in janson2["data"]["program"]:
#                        for n in janson2["data"]["program"]["panels"]:
#                            for z in n["videoList"]["videoAssets"]:
#                                if z["id"] == int(match.group(1)):
#                                    vid = z["id"]
#                                    self.output["id"] = str(vid)
#                                    self.output["episodename"] = z["title"]
#                                    self.output["title"] = z["program"]["name"]


#        vid = None
#        for i in jansson:
#            janson2 = json.loads(i["data"])
#            json.dumps(janson2)
#            if "videoAsset" in janson2["data"]:
#                vid = janson2["data"]["videoAsset"]["id"]
#                if janson2["data"]["videoAsset"]["is_drm_protected"]:
#                    yield ServiceError("We can't download DRM protected content from this site.")
#                    return
#                if janson2["data"]["videoAsset"]["is_live"]:
#                    self.config.set("live", True)
#                if janson2["data"]["videoAsset"]["season"] > 0:
#                    self.output["season"] = janson2["data"]["videoAsset"]["season"]
#                if janson2["data"]["videoAsset"]["episode"] > 0:
#                    self.output["episode"] = janson2["data"]["videoAsset"]["episode"]
#                self.output["title"] = janson2["data"]["videoAsset"]["program"]["name"]
#                self.output["episodename"] = janson2["data"]["videoAsset"]["title"]
#                vid = str(vid)
#                self.output["id"] = str(vid)
#            if "program" in janson2["data"] and vid is None:
#                if "contentfulPanels" in janson2["data"]["program"]:
#                    match = re.search(r"[\/-](\d+)$", self.url)
#                    if match and "panels" in janson2["data"]["program"]:
#                        for n in janson2["data"]["program"]["panels"]:
#                            for z in n["videoList"]["videoAssets"]:
#                                if z["id"] == int(match.group(1)):
#                                    vid = z["id"]
#                                    self.output["id"] = str(vid)
#                                    self.output["episodename"] = z["title"]
#                                    self.output["title"] = z["program"]["name"]

        if vid is None:
            yield ServiceError("Cant find video id for the video")
            return

        url = "https://playback-api.b17g.net/media/{}?service=tv4&device=browser&protocol=hls%2Cdash&drm=widevine".format(vid)
        res = self.http.request("get", url, cookies=self.cookies)
        if res.status_code > 200:
            yield ServiceError("Can't play this because the video is geoblocked or not available.")
            return
        if res.json()["playbackItem"]["type"] == "hls":
            streams = hlsparse(self.config, self.http.request("get", res.json()["playbackItem"]["manifestUrl"]),
                               res.json()["playbackItem"]["manifestUrl"], output=self.output, httpobject=self.http)
            for n in list(streams.keys()):
                yield streams[n]

    def _getjson(self):
#        match = re.search(r".prefetched = (\[.*\]);", self.get_urldata())
        match = re.search(r"<script id=\"__NEXT_DATA__\" type=\"application/json\">(\{.*\})</script>", self.get_urldata())
        return match

    def find_all_episodes(self, config):
        episodes = []
        items = []
        show = None
        match = self._getjson()
        jansson = json.loads(match.group(1))
        for i in jansson:
            janson2 = json.loads(i["data"])
            if "program" in janson2["data"]:
                if "programPanels" in janson2["data"]["program"]:
                    for n in janson2["data"]["program"]["programPanels"]["panels"]:
                        if n.get("assetType", None) == "EPISODE":
                            for z in n["videoList"]["videoAssets"]:
                                show = z["program_nid"]
                                items.append(z["id"])
                        if n.get("assetType", None) == "CLIP" and config.get("include_clips"):
                            for z in n["videoList"]["videoAssets"]:
                                show = z["program_nid"]
                                items.append(z["id"])

        items = sorted(items)
        for item in items:
            episodes.append("https://www.tv4play.se/program/{}/{}".format(show, item))

        if config.get("all_last") > 0:
            return episodes[-config.get("all_last"):]
        return episodes


class Tv4(Service, OpenGraphThumbMixin):
    supported_domains = ['tv4.se']

    def get(self):
        match = re.search(r"[\/-](\d+)$", self.url)
        if not match:
            yield ServiceError("Cant find video id")
            return
        self.output["id"] = match.group(1)

        match = re.search("data-program-format='([^']+)'", self.get_urldata())
        if not match:
            yield ServiceError("Cant find program name")
            return
        self.output["title"] = match.group(1)

        match = re.search('img alt="([^"]+)" class="video-image responsive"', self.get_urldata())
        if not match:
            yield ServiceError("Cant find title of the video")
            return
        self.output["episodename"] = match.group(1)

        url = "https://playback-api.b17g.net/media/{}?service=tv4&device=browser&protocol=hls%2Cdash&drm=widevine".format(self.output["id"])
        res = self.http.request("get", url, cookies=self.cookies)
        if res.status_code > 200:
            yield ServiceError("Can't play this because the video is geoblocked.")
            return
        if res.json()["playbackItem"]["type"] == "hls":
            streams = hlsparse(self.config, self.http.request("get", res.json()["playbackItem"]["manifestUrl"]),
                               res.json()["playbackItem"]["manifestUrl"], output=self.output)
            for n in list(streams.keys()):
                yield streams[n]
