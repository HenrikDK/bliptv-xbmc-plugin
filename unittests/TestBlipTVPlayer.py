import nose
import BaseTestCase
from mock import Mock, patch
import sys
from BlipTVPlayer import BlipTVPlayer


class TestBlipTVPlayer(BaseTestCase.BaseTestCase):
    def test_playVideo_should_call_getVideoObject(self):
        player = BlipTVPlayer()
        player.getVideoObject = Mock()
        player.getVideoObject.return_value = []

        player.playVideo({"apierror": "some error"})

        assert(player.getVideoObject.call_count == 1)

    def test_playVideo_should_log_and_fail_gracefully_on_apierror(self):
        player = BlipTVPlayer()
        player.getVideoObject = Mock()
        player.getVideoObject.return_value = []

        result = player.playVideo({"apierror": "some error"})

        assert(result == False)
        sys.modules["__main__"].common.log.assert_called_with("construct video url failed contents of video item []")

    def test_playVideo_should_call_xbmc_setResolvedUrl(self):
        sys.modules["__main__"].settings.getSetting.return_value = "0"
        sys.modules["__main__"].common.makeAscii.return_value = "ascii"
        sys.modules["__main__"].xbmcgui.ListItem = Mock()
        player = BlipTVPlayer()
        player.addSubtitles = Mock()
        player.getVideoObject = Mock()
        player.getVideoObject.return_value = {"Title": "someTitle", "videoid": "some_id", "thumbnail": "someThumbnail", "video_url": "someUrl"}
        sys.argv = ["test1", "1", "test2"]

        player.playVideo({"videoid": "some_id"})

        assert(sys.modules["__main__"].xbmcplugin.setResolvedUrl.call_count > 0)

    def test_playVideo_should_update_locally_stored_watched_status(self):
        sys.modules["__main__"].common.makeAscii.return_value = "ascii"
        sys.modules["__main__"].settings.getSetting.return_value = "0"
        sys.modules["__main__"].common.log = Mock()
        sys.argv = ["test1", "1", "test2"]
        player = BlipTVPlayer()
        player.getVideoObject = Mock()
        player.getVideoObject.return_value = {"Title": "someTitle", "videoid": "some_id", "thumbnail": "someThumbnail", "video_url": "someUrl"}
        player.addSubtitles = Mock()

        player.playVideo({"videoid": "some_id"})

        sys.modules["__main__"].settings.setSetting.assert_called_with("vidstatus-some_id", "7" )

    def test_getInfo_should_call_core_getVideoInfo_to_parse_bliptv_data(self):
        sys.modules["__main__"].cache.sqlGet.return_value = {}
        sys.modules["__main__"].common.fetchPage.return_value = {"status": 200, "content": "something"}
        sys.modules["__main__"].player.getVideoInfo.return_value = [{"videoid": "some_id"}]
        player = BlipTVPlayer()
        player.getVideoInfo = Mock()
        player.getVideoInfo.return_value = {"id": "some_id"}

        player.getInfo({"content": "content", "status": 200})

        player.getVideoInfo.assert_called_with('content', {})

    def test_getInfo_should_call_log_error_if_getVideoInfo_fails(self):
        sys.modules["__main__"].cache.sqlGet.return_value = {}
        sys.modules["__main__"].common.fetchPage.return_value = {"status": 200, "content": "something"}
        player = BlipTVPlayer()
        player.getVideoInfo = Mock()
        player.getVideoInfo.return_value = {}

        player.getInfo({"content": "content", "status": 200})

        sys.modules["__main__"].common.log.assert_any_call("Couldn't parse API output, BlipTV doesn't seem to know this video id?")

    def test_getInfo_should_call_report_error_correctly(self):
        sys.modules["__main__"].cache.sqlGet.return_value = {}
        sys.modules["__main__"].common.fetchPage.return_value = {"status": 200, "content": "something"}
        sys.modules["__main__"].player.getVideoInfo.return_value = []
        player = BlipTVPlayer()

        params = {}
        print repr(params)
        video = player.getInfo({"content": "content", "status": 303}, params)
        print repr(video)
        print repr(params)
        assert(video == {})
        assert(params["apierror"] == "content")

    def test_getVideoInfo_calls_minidom(self):
        patcher = patch("xml.dom.minidom.parseString")
        patcher.start()
        import xml.dom.minidom
        dom = Mock()
        xml.dom.minidom.parseString = Mock()
        xml.dom.minidom.parseString.return_value = dom
        dom.getElementsByTagName.return_value = [{}]
        player = BlipTVPlayer()
        player._getNodeValue = Mock()
        player.storage = Mock()
        player.storage.retrieveValue.return_value = "0"

        result = player.getVideoInfo("xml", {"videoid": "vidid"})
        patcher.stop()

        print repr(result)
        print repr(player._getNodeValue.call_count)
        assert(player._getNodeValue.call_count == 6)

    def test_getVideoInfo_calls_storage(self):
        patcher = patch("xml.dom.minidom.parseString")
        patcher.start()
        import xml.dom.minidom
        dom = Mock()
        xml.dom.minidom.parseString = Mock()
        xml.dom.minidom.parseString.return_value = dom
        dom.getElementsByTagName.return_value = [{}]
        player = BlipTVPlayer()
        player._getNodeValue = Mock()
        player.storage = Mock()
        player.storage.retrieveValue.return_value = "0"

        player.getVideoInfo("xml", {"videoid": "vidid"})
        patcher.stop()

        player.storage.retrieveValue.assert_called_with("vidstatus-vidid")
        
    def test_selectVideoQuality_should_get_sd(self):
        sys.modules["__main__"].settings.getSetting.return_value = "0"
        player = BlipTVPlayer()
        
        video_url = player.selectVideoQuality({"SD": "sd-url"}, {"action": "play"})
        
        sys.modules["__main__"].settings.getSetting.assert_called_with("hd_videos")
        assert(video_url == "sd-url | Mozilla/5.0 (MOCK)")

    def test_selectVideoQuality_should_get_720p(self):
        sys.modules["__main__"].settings.getSetting.return_value = "0"
        player = BlipTVPlayer()
        
        video_url = player.selectVideoQuality({"720p": "720p-url"}, {"action": "play", "quality": "720p"})
        
        assert(video_url == "720p-url | Mozilla/5.0 (MOCK)")

    def test_selectVideoQuality_should_get_1080p(self):
        sys.modules["__main__"].settings.getSetting.return_value = "0"
        player = BlipTVPlayer()
        
        video_url = player.selectVideoQuality({"1080p": "1080p-url"}, {"action": "play", "quality": "1080p"})
        
        assert(video_url == "1080p-url | Mozilla/5.0 (MOCK)")

    def test_selectVideoQuality_should_get_download_quality(self):
        sys.modules["__main__"].settings.getSetting.return_value = "2"
        player = BlipTVPlayer()
        
        video_url = player.selectVideoQuality({"720p": "720p-url"}, {"action": "download"})
        
        sys.modules["__main__"].settings.getSetting.assert_called_with("hd_videos_download")
        assert(video_url == "720p-url")

    def test_selectVideoQuality_should_download_with_view_quality(self):
        settings = ["3", "0"]
        sys.modules["__main__"].settings.getSetting.side_effect = lambda x: settings.pop()
        player = BlipTVPlayer()
        
        video_url = player.selectVideoQuality({"1080p": "1080p-url"}, {"action": "download"})
        
        sys.modules["__main__"].settings.getSetting.assert_called_with("hd_videos")
        assert(video_url == "1080p-url")

    def test_selectVideoQuality_should_get_quality_from_settings(self):
        sys.modules["__main__"].settings.getSetting.return_value = "3"
        player = BlipTVPlayer()
        
        video_url = player.selectVideoQuality({"1080p": "1080p-url"}, {"action": "play"})
        
        sys.modules["__main__"].settings.getSetting.assert_called_with("hd_videos")
        assert(video_url == "1080p-url | Mozilla/5.0 (MOCK)")

    def test_selectVideoQuality_should_fail(self):
        sys.modules["__main__"].settings.getSetting.return_value = "0"
        player = BlipTVPlayer()
        
        video_url = player.selectVideoQuality({"1080p": "1080p-url"}, {"action": "fail"})
        
        assert(video_url == "")

    def test_getVideoObject_should_return_correctly(self):
        patcher = patch("urllib2.urlopen")
        patcher.start()
        import urllib2
        urllib2.urlopen().geturl = Mock(return_value="real-video-url")
        player = BlipTVPlayer()
        player.selectVideoQuality = Mock()
        player.selectVideoQuality.return_value = "video-url"
        player._getVideoLinks = Mock()
        player.getInfo = Mock()
        player.getInfo.return_value = {"Title": "mock"}

        video = player.getVideoObject({"action": "download"})
        patcher.stop()

        print "A : " + repr(video)
        assert(video["Title"] == "mock")
        assert(video["video_url"] == "real-video-url")

    def test_getVideoObject_should_test_local_file(self):
        sys.modules["__main__"].xbmcvfs.exists.return_value = True
        sys.modules["__main__"].xbmcvfs.exists.return_value
        sys.modules["__main__"].settings.getSetting.return_value = "mock_path/"
        player = BlipTVPlayer()
        player.selectVideoQuality = Mock()
        player.selectVideoQuality.return_value = "video-url"
        player._getVideoLinks = Mock()
        player.getInfo = Mock()
        player.getInfo.return_value = {"Title": "mock"}
        
        (video, status) = player.getVideoObject({"action": "check-local", "videoid": "mockid"})

        sys.modules["__main__"].xbmcvfs.exists.assert_called_with('mock_path/mock-[mockid].mp4')

    def test_getVideoObject_should_fail(self):
        sys.modules["__main__"].xbmcvfs.exists.return_value = True
        sys.modules["__main__"].settings.getSetting.return_value = "mock_path/"
        sys.modules["__main__"].language.return_value = "mock error"
        player = BlipTVPlayer()
        player.selectVideoQuality = Mock()
        player.selectVideoQuality.return_value = "video-url"
        player._getVideoLinks = Mock()
        player._getVideoLinks.return_value = False
        player.getInfo = Mock()
        player.getInfo.return_value = {}

        params = {"action": "play", "videoid": "mockid"}
        video = player.getVideoObject(params)
        print "A : " + repr(video)
        print "B : " + repr(params)
        assert(params["apierror"] == "mock error")

    def test__getVideoLinks_should_return_720p(self):
        patcher = patch("xml.dom.minidom.parseString")
        patcher.start()
        import xml.dom.minidom
        node = Mock()
        node.getAttribute = Mock()
        node_ret = ["720", "720-url","something_video"]
        node.getAttribute.side_effect = lambda x: node_ret.pop()
        dom = Mock()
        dom.getElementsByTagName.return_value = [node]
        xml.dom.minidom.parseString = Mock()
        xml.dom.minidom.parseString.return_value = dom

        player = BlipTVPlayer()
        links = player._getVideoLinks({"status": 200, "content": "content"}, {})
        print repr(links)
        assert(links["720p"] == "720-url")

    def test__getVideoLinks_should_return_1080p(self):
        patcher = patch("xml.dom.minidom.parseString")
        patcher.start()
        import xml.dom.minidom
        node = Mock()
        node.getAttribute = Mock()
        node_ret = ["1080", "1080-url","something_video"]
        node.getAttribute.side_effect = lambda x: node_ret.pop()
        dom = Mock()
        dom.getElementsByTagName.return_value = [node]
        xml.dom.minidom.parseString = Mock()
        xml.dom.minidom.parseString.return_value = dom
        player = BlipTVPlayer()
        
        links = player._getVideoLinks({"status": 200, "content": "content"}, {})

        assert(links["1080p"] == "1080-url")

    def test_getNodeAttribute_should_parse_node_structure_correctly(self):
        settings = ["3"]
        sys.modules["__main__"].settings.getSetting.side_effect = lambda x: settings.pop()
        player = BlipTVPlayer()
        node = Mock()
        
        player._getNodeAttribute(node, "tag", "attribute", "default")

        node.getElementsByTagName.assert_called_with("tag")
        node.getElementsByTagName().item.assert_called_with(0)
        node.getElementsByTagName().item().hasAttribute.assert_called_with("attribute")
        node.getElementsByTagName().item().getAttribute.assert_called_with("attribute")

    def test_getNodeValue_should_parse_node_structure_correctly(self):
        settings = ["3"]
        sys.modules["__main__"].settings.getSetting.side_effect = lambda x: settings.pop()
        player = BlipTVPlayer()
        node = Mock()
        node.getElementsByTagName().item().firstChild.nodeValue = 5

        result = player._getNodeValue(node, "tag", "default")

        node.getElementsByTagName.assert_called_with("tag")
        node.getElementsByTagName().item.assert_called_with(0)
        assert(result == 5)

if __name__ == '__main__':
    nose.runmodule()
