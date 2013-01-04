import BaseTestCase
import nose


class TestBlipTVEpisodeFeedsScraper(BaseTestCase.BaseTestCase):
        def test_plugin_should_list_browse_show_category_show_list_correctly(self):
                self.navigation.listMenu({"scraper": "browse_shows", "path": "/root/explore/browse", "category": "/drama-videos"})

                self.assert_directory_count_greater_than_or_equals(10)
                #self.assert_directory_count_less_than_or_equals(51)
                self.assert_directory_is_a_folder_list()
                self.assert_directory_items_should_have_external_thumbnails()
                self.assert_directory_item_urls_contain("show")

        def test_plugin_should_list_new_shows_show_list_correctly(self):
                self.navigation.listMenu({"scraper": "new_shows", "path": "/root/explore/newshows"})

                self.assert_directory_count_greater_than_or_equals(10)
                self.assert_directory_count_less_than_or_equals(51)
                self.assert_directory_is_a_folder_list()
                self.assert_directory_items_should_have_external_thumbnails()
                self.assert_directory_item_urls_contain("show")

        def test_plugin_should_list_popular_shows_show_list_correctly(self):
                self.navigation.listMenu({"scraper": "popular_shows", "path": "/root/explore/newshows"})

                self.assert_directory_count_greater_than_or_equals(10)
                self.assert_directory_count_less_than_or_equals(51)
                self.assert_directory_is_a_folder_list()
                self.assert_directory_items_should_have_external_thumbnails()
                self.assert_directory_item_urls_contain("show")

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

if __name__ == "__main__":
        nose.runmodule()
