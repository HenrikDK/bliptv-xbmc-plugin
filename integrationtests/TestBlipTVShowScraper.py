import BaseTestCase
import nose
import sys


class TestBlipTVShowScraper(BaseTestCase.BaseTestCase):

    def test_plugin_should_scrape_show_videos_list_correctly(self):
        self.navigation.listMenu({"scraper": "show", "show": "/redlettermedia", "path": "/root/shows/something"})

        self.assert_directory_count_greater_than_or_equals(10)
        self.assert_directory_count_less_than_or_equals(51)
        self.assert_directory_is_a_video_list()
        self.assert_directory_contains_only_unique_video_items()
        self.assert_directory_items_should_have_external_thumbnails()

    def test_plugin_should_scrape_show_videos_list_page_2_correctly(self):
        self.navigation.listMenu({"scraper": "show", "show": "/redlettermedia", "page": "1", "path": "/root/shows/something"})

        self.assert_directory_count_greater_than_or_equals(10)
        self.assert_directory_count_less_than_or_equals(51)
        self.assert_directory_is_a_video_list()
        self.assert_directory_contains_only_unique_video_items()
        self.assert_directory_items_should_have_external_thumbnails()

    def test_plugin_should_scrape_show_video_list_page_in_under_20_seconds(self):
        sys.modules["__main__"].dbglevel = 1
        self.navigation.listMenu({"scraper": "show", "show": "/redlettermedia", "path": "/root/shows/something"})

        self.assert_run_time_is_less_than_or_equal_to(20)
        self.assert_directory_count_greater_than_or_equals(10)
        self.assert_directory_count_less_than_or_equals(51)
        self.assert_directory_is_a_video_list()
        self.assert_directory_contains_only_unique_video_items()
        self.assert_directory_items_should_have_external_thumbnails()

if __name__ == "__main__":
    nose.runmodule()
