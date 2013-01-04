import BaseTestCase
import nose


class TestBlipTVShowFeedsScraper(BaseTestCase.BaseTestCase):
        def test_plugin_should_list_browse_shows_categories_folder_correctly(self):
                self.navigation.listMenu({"scraper": "browse_shows", "path": "/root/explore/browse"})

                self.assert_directory_count_greater_than_or_equals(10)
                self.assert_directory_count_less_than_or_equals(51)
                self.assert_directory_is_a_folder_list()
                self.assert_directory_item_urls_contain("category")

        def test_plugin_should_list_browse_show_category_show_list_correctly(self):
                self.navigation.listMenu({"scraper": "browse_shows", "path": "/root/explore/browse", "category": "/home-and-family-videos"})

                self.assert_directory_count_greater_than_or_equals(10)
                self.assert_directory_contains_only_unique_item_urls()
                self.assert_directory_is_a_folder_list()
                self.assert_directory_items_should_have_external_thumbnails()
                self.assert_directory_item_urls_contain("show")

        def test_plugin_should_list_staff_picks_category_list_correctly(self):
                self.navigation.listMenu({"scraper": "staff_picks", "path": "/root/explore/staffpicks"})

                self.assert_directory_count_greater_than_or_equals(10)
                self.assert_directory_count_less_than_or_equals(51)
                self.assert_directory_is_a_folder_list()
                self.assert_directory_item_urls_contain("category")

        def test_plugin_should_list_staff_picks_category_show_list_correctly(self):
                self.navigation.listMenu({"scraper": "staff_picks", "path": "/root/explore/staffpicks", "category": "/comedy-videos"})

                self.assert_directory_count_greater_than_or_equals(10)
                self.assert_directory_count_less_than_or_equals(51)
                self.assert_directory_contains_almost_only_unique_item_urls()
                self.assert_directory_is_a_folder_list()
                self.assert_directory_items_should_have_external_thumbnails()
                self.assert_directory_item_urls_contain("show")

        def test_plugin_should_list_new_shows_show_list_correctly(self):
                self.navigation.listMenu({"scraper": "new_shows", "path": "/root/explore/newshows"})

                self.assert_directory_count_greater_than_or_equals(10)
                self.assert_directory_count_less_than_or_equals(51)
                self.assert_directory_contains_only_unique_item_urls()
                self.assert_directory_is_a_folder_list()
                self.assert_directory_items_should_have_external_thumbnails()
                self.assert_directory_item_urls_contain("show")

        def test_plugin_should_list_popular_shows_show_list_correctly(self):
                self.navigation.listMenu({"scraper": "popular_shows", "path": "/root/explore/newshows"})

                self.assert_directory_count_greater_than_or_equals(10)
                self.assert_directory_count_less_than_or_equals(51)
                self.assert_directory_contains_only_unique_item_urls()
                self.assert_directory_is_a_folder_list()
                self.assert_directory_items_should_have_external_thumbnails()
                self.assert_directory_item_urls_contain("show")

        def test_plugin_should_list_trending_shows_show_list_correctly(self):
                self.navigation.listMenu({"scraper": "trending_shows", "path": "/root/explore/newshows"})

                self.assert_directory_count_greater_than_or_equals(10)
                self.assert_directory_count_less_than_or_equals(51)
                self.assert_directory_contains_only_unique_item_urls()
                self.assert_directory_is_a_folder_list()
                self.assert_directory_items_should_have_external_thumbnails()
                self.assert_directory_item_urls_contain("show")

if __name__ == "__main__":
        nose.runmodule()
