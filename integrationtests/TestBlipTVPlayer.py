import BaseTestCase
import nose
import sys


class TestBlipTVPlayer(BaseTestCase.BaseTestCase):
        def test_plugin_should_play_standard_videos(self):
                self.navigation.executeAction({"action": "play_video", "videoid": "5753829"})

                args = sys.modules["__main__"].xbmcplugin.setResolvedUrl.call_args_list
                print "Args: " + repr(args)
                print repr("listitem" in args[0][1])
                print repr(args[0][1]["handle"] == -1)
                print repr(args[0][1]["succeeded"] == True)

                assert("listitem" in args[0][1])
                assert(args[0][1]["handle"] == -1)
                assert(args[0][1]["succeeded"] == True)

        def ttest_plugin_should_play_videos_with_subtitles_when_available(self):
                import os
                sys.modules["__main__"].xbmcvfs.exists.side_effect = os.path.exists
                self.navigation.executeAction({"action": "play_video", "videoid": "bUcszN8jRB8"})

                args = sys.modules["__main__"].xbmcplugin.setResolvedUrl.call_args_list
                args2 = sys.modules["__main__"].xbmc.Player().setSubtitles.call_args_list
                print "Args: " + repr(args)
                print "Args2: " + repr(args2[0][0][0])
                print repr("listitem" in args[0][1])
                print repr(args[0][1]["handle"] == -1)
                print repr(args[0][1]["succeeded"] == True)
                print repr(args2[0][0][0] == './tmp/Morning Dew  a bad lip reading of Bruno Mars, feat. Lady Gaga and Jay-Z-[bUcszN8jRB8].ssa')

                assert("listitem" in args[0][1])
                assert(args[0][1]["handle"] == -1)
                assert(args[0][1]["succeeded"] == True)
                assert(args2[0][0][0] == './tmp/Morning Dew  a bad lip reading of Bruno Mars, feat. Lady Gaga and Jay-Z-[bUcszN8jRB8].ssa')

if __name__ == "__main__":
        nose.runmodule()
