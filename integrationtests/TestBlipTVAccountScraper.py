# -*- coding: utf-8 -*-
import BaseTestCase
import nose
import sys
import os
from mock import Mock


class TestBlipTVAccount(BaseTestCase.BaseTestCase):
# Todo:
# http://blip.tv/viewers/love/5843147
# http://blip.tv/viewers/unlove/5843147
# http://blip.tv/viewers/follow_show/906537
# http://blip.tv/viewers/unfollow_show/906537
# Login
# Relogin
# Pagination

    def ttest_plugin_should_login_through_facebook(self):
        #self.navigation.executeAction({"action": "download", "videoid": "5779197", "async": "false"})
        assert(False)

    def test_plugin_should_fetch_following_shows(self):
        self.navigation.listMenu({"path":"/root/my_followed", "scraper": "my_followed" , "login": "true", "folder": "true"})
        self.assert_directory_count_greater_than_or_equals(1)
        self.assert_directory_count_less_than_or_equals(51)
        self.assert_directory_is_a_folder_list()
        self.assert_directory_items_should_have_external_thumbnails() # Two internal!
        #self.assert_directory_item_urls_contain("show")

    def test_plugin_should_fetch_loved_episodes(self):
        self.navigation.listMenu({"path":"/root/my_loved", "scraper": "my_loved" , "login": "true"})
        self.assert_directory_count_greater_than_or_equals(1)
        self.assert_directory_count_less_than_or_equals(51)
        self.assert_directory_is_a_video_list()
        self.assert_directory_items_should_have_external_thumbnails()

    def ttest_plugin_should_fetch_new_episodes(self):
        self.navigation.listMenu({"path":"/root/my_followed", "scraper": "my_followed_new_episodes" , "login": "true", "folder": "true"})
        self.assert_directory_count_greater_than_or_equals(1)
        self.assert_directory_count_less_than_or_equals(51)
        self.assert_directory_is_a_video_list()
        self.assert_directory_items_should_have_external_thumbnails()

    def ttest_plugin_should_fetch_new_shows(self):
        self.navigation.listMenu({"path":"/root/my_followed", "scraper": "my_followed_new_shows" , "login": "true", "folder": "true"})
        self.assert_directory_count_greater_than_or_equals(1)
        self.assert_directory_count_less_than_or_equals(51)
        self.assert_directory_is_a_folder_list()
        self.assert_directory_items_should_have_external_thumbnails()

        assert(False)

if __name__ == "__main__":
        nose.runmodule()
