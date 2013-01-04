import BaseTestCase
import nose


class TestBlipTVFolderStructure(BaseTestCase.BaseTestCase):
        def test_plugin_should_list_main_folder_structure_correctly(self):
                self.navigation.listMenu({})

                self.assert_directory_count_greater_than_or_equals(5)
                self.assert_directory_count_less_than_or_equals(51)
                self.assert_directory_is_a_folder_list()

        def test_plugin_should_list_explore_folder_structure_correctly(self):
                self.navigation.listMenu({"path": "/root/explore"})

                self.assert_directory_count_greater_than_or_equals(8)
                self.assert_directory_count_less_than_or_equals(51)
                self.assert_directory_is_a_folder_list()
                self.assert_directory_item_urls_contain("scraper")

if __name__ == "__main__":
        nose.runmodule()
