import BaseTestCase
import nose
import sys


class TestBlipTVStorageFolders(BaseTestCase.BaseTestCase):

    def test_plugin_should_list_stored_searches_folder_list_correctly(self):
        self.navigation.listMenu({"path": "/root/search/new", "scraper": "search", "search": "Critic"})
        self.navigation.listMenu({"path": "/root/search/new", "scraper": "search", "search": "RedLetterMedia"})
        self.navigation.listMenu({"path": "/root/search/new", "scraper": "search", "search": "Chick"})
        self.reset_xbmc_mocks()

        self.navigation.listMenu({"path": "/root/search/", "store": "searches", "folder": "true"})

        print repr(sys.modules["__main__"].xbmcplugin.addDirectoryItem.call_args_list)
        self.assert_directory_item_urls_contain_at_least_one("Critic")
        self.assert_directory_item_urls_contain_at_least_one("RedLetterMedia")
        self.assert_directory_item_urls_contain_at_least_one("Chick")
        self.assert_directory_count_less_than_or_equals(4)
        self.assert_directory_count_greater_than_or_equals(3)
        self.assert_directory_is_a_folder_list()

    def test_plugin_should_list_stored_favorite_shows_folder_list_correctly(self):
        self.navigation.executeAction({"path": "/root/something/new", "action": "add_favorite", "show": "/nostalgia-chick"})
        self.navigation.executeAction({"path": "/root/something/new", "action": "add_favorite", "show": "/redlettermedia"})
        self.navigation.executeAction({"path": "/root/something/new", "action": "add_favorite", "show": "/nostalgiacritic"})
        self.reset_xbmc_mocks()

        self.navigation.listMenu({"path": "/root/search/", "store": "favorites", "folder": "true"})

        print repr(sys.modules["__main__"].xbmcplugin.addDirectoryItem.call_args_list)
        self.assert_directory_item_urls_contain_at_least_one("nostalgia-chick")
        self.assert_directory_item_urls_contain_at_least_one("redlettermedia")
        self.assert_directory_item_urls_contain_at_least_one("nostalgiacritic")
        self.assert_directory_count_less_than_or_equals(4)
        self.assert_directory_count_greater_than_or_equals(3)
        self.assert_directory_is_a_folder_list()

if __name__ == "__main__":
    nose.runmodule()
