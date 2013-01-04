import sys
import time
import inspect

class MockBlipTVDepends:
    common = ""

    def mock(self):
        import sys
        import string
        from mock import Mock
        sys.path.append("../plugin/")

        # Setup default test various values
        sys.modules["__main__"].plugin = "BlipTV - Unittest"
        sys.modules["__main__"].dbg = True
        try:
            plat = sys.platform.uname()
        except:
            plat = ('', '', '', '', '', '')

        if plat[0] == "FreeBSD":
            sys.modules["__main__"].dbglevel = 5
        else:
            sys.modules["__main__"].dbglevel = 3
        sys.modules["__main__"].login = ""
        sys.modules["__main__"].language = Mock()

        import BlipTVUtils
        sys.modules["__main__"].utils = Mock(spec=BlipTVUtils.BlipTVUtils)
        sys.modules["__main__"].utils.VALID_CHARS = "-_.() %s%s" % (string.ascii_letters, string.digits)
        sys.modules[ "__main__" ].utils.INVALID_CHARS = "\\/:*?\"<>|"
        sys.modules["__main__"].utils.USERAGENT = "Mozilla/5.0 (MOCK)"

        sys.modules["__main__"].common = Mock()
        sys.modules["__main__"].common.USERAGENT = "Mozilla/5.0 (MOCK)"
        sys.modules["__main__"].log_override = self
        sys.modules["__main__"].common.log.side_effect = sys.modules["__main__"].log_override.log

        sys.modules["__main__"].cache = Mock()

        import BlipTVStorage
        sys.modules["__main__"].storage = Mock(spec=BlipTVStorage.BlipTVStorage)
        import BlipTVScraper
        sys.modules["__main__"].scraper = Mock(spec=BlipTVScraper.BlipTVScraper)
        import BlipTVPlayer
        sys.modules["__main__"].player = Mock(spec=BlipTVPlayer.BlipTVPlayer)
        sys.modules["__main__"].downloader = Mock()
        import BlipTVNavigation
        sys.modules["__main__"].navigation = Mock(spec=BlipTVNavigation.BlipTVNavigation)

    def mockXBMC(self):
        import sys
        from mock import Mock
        sys.path.append("../xbmc-mocks/")
        import xbmc
        import xbmcaddon
        import xbmcgui
        import xbmcplugin
        import xbmcvfs

        #Setup basic xbmc dependencies
        sys.modules["__main__"].xbmc = Mock(spec=xbmc)
        sys.modules["__main__"].xbmc.translatePath = Mock()
        sys.modules["__main__"].xbmc.translatePath.return_value = "testing"
        sys.modules["__main__"].xbmc.getSkinDir = Mock()
        sys.modules["__main__"].xbmc.getSkinDir.return_value = "testSkinPath"
        sys.modules["__main__"].xbmc.getInfoLabel.return_value = "some_info_label"
        sys.modules["__main__"].xbmcaddon = Mock(spec=xbmcaddon)
        sys.modules["__main__"].xbmcgui = Mock(spec=xbmcgui)
        sys.modules["__main__"].xbmcgui.WindowXMLDialog.return_value = "testWindowXML"

        sys.modules["__main__"].xbmcplugin = Mock(spec=xbmcplugin)
        sys.modules["__main__"].xbmcvfs = Mock(spec=xbmcvfs)
        sys.modules["__main__"].settings = Mock(spec=xbmcaddon.Addon())
        sys.modules["__main__"].settings.getAddonInfo.return_value = "somepath"

        sys.modules["DialogDownloadProgress"] = __import__("mock")
        sys.modules["DialogDownloadProgress"].DownloadProgress = Mock()

    def log(self, description, level = 0):
        if sys.modules["__main__"].dbg and sys.modules["__main__"].dbglevel > level:
            try:
                print "%s [%s] %s : '%s'" % (time.strftime("%H:%M:%S"), sys.modules["__main__"].plugin, inspect.stack()[1][3] , description.decode("utf-8","ignore"))
            except:
                print "%s [%s] %s : '%s'" % (time.strftime("%H:%M:%S"), sys.modules["__main__"].plugin, inspect.stack()[1][3] , description)
