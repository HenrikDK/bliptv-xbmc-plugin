# -*- coding: utf-8 -*-
import BaseTestCase
import nose
import sys
import os
from mock import Mock


class TestBlipTVDownloader(BaseTestCase.BaseTestCase):

    def test_plugin_should_download_standard_videos(self):
        sys.modules["__main__"].xbmcvfs.rename.side_effect = os.rename
        sys.modules["__main__"].downloader._getNextItemFromQueue = Mock()
        video = sys.modules["__main__"].player.getVideoObject({"action": "download", "videoid": "5779197"})
        video["download_path"] = "./tmp/"
        video["url"] = video["video_url"]
        sys.modules["__main__"].downloader._getNextItemFromQueue.side_effect = [("iFanboy - 2011 Hiatus Announcement-[5779197].mp4", video), {}]

        self.navigation.executeAction({"action": "download", "videoid": "5779197", "async": "false"})

        assert(os.path.exists('./tmp/iFanboy - 2011 Hiatus Announcement-[5779197].mp4'))
        assert(os.path.getsize('./tmp/iFanboy - 2011 Hiatus Announcement-[5779197].mp4') > 100)

if __name__ == "__main__":
        nose.runmodule()
