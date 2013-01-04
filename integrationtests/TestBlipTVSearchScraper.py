import BaseTestCase
import nose


class TestBlipTVSearchScraper(BaseTestCase.BaseTestCase):
        def test_plugin_should_scrape_show_search_folder_list_correctly(self):
                self.navigation.listMenu({"scraper": "show_search", "search": "Critic", "path": "/root/searches/something"})

                self.assert_directory_count_greater_than_or_equals(10)
                self.assert_directory_count_less_than_or_equals(51)
                self.assert_directory_is_a_folder_list()
                self.assert_directory_contains_only_unique_item_urls()
                self.assert_directory_items_should_have_external_thumbnails()

        def test_plugin_should_scrape_episode_search_videos_list_page_correctly(self):
                self.navigation.listMenu({"scraper": "search", "search": "RedLetterMedia", "path": "/root/searches/something"})

                self.assert_directory_count_greater_than_or_equals(10)
                self.assert_directory_count_less_than_or_equals(51)
                self.assert_directory_is_a_video_list()
                self.assert_directory_contains_only_unique_video_items()
                self.assert_directory_items_should_have_external_thumbnails()
                self.assert_directory_should_have_next_folder()

        def test_plugin_should_scrape_episode_search_videos_list_page_2_correctly(self):
                self.navigation.listMenu({"scraper": "search", "search": "RedLetterMedia", "page": "1", "path": "/root/searches/something"})

                self.assert_directory_count_greater_than_or_equals(10)
                self.assert_directory_count_less_than_or_equals(51)
                self.assert_directory_is_a_video_list()
                self.assert_directory_contains_only_unique_video_items()
                self.assert_directory_items_should_have_external_thumbnails()

if __name__ == "__main__":
        nose.runmodule()
