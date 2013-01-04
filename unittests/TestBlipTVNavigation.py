# -*- coding: utf-8 -*-
import nose
import BaseTestCase
from mock import Mock
import sys
from BlipTVNavigation import BlipTVNavigation


class TestBlipTVNavigation(BaseTestCase.BaseTestCase):
    def test_listMenu_should_traverse_menustructure_correctly(self):
        sys.argv = ["something", -1, "something_else"]
        sys.modules["__main__"].settings.getSetting.return_value = "true"
        navigation = BlipTVNavigation()
        navigation.list = Mock()
        navigation.addListItem = Mock()

        navigation.listMenu()

        args = navigation.addListItem.call_args_list

        for arg in args:
            assert(arg[0][1]["path"].replace('/root/', '').find('/') < 0)
        assert(navigation.addListItem.call_count > 1)

    def test_listMenu_should_only_list_subfolders_to_a_path(self):
        sys.argv = ["something", -1, "something_else"]
        list = ["", "", "", ""]
        sys.modules["__main__"].settings.getSetting.side_effect = lambda x: list.pop()
        navigation = BlipTVNavigation()
        navigation.categories = ({"path": "/root/my_first_level"}, {"path": "/root/my_first_level/my_second_level"}, {"path": "/root/my_other_first_level"}, {"path": "/root/my_other_first_level/my_other_second_level"})
        navigation.list = Mock()
        navigation.addListItem = Mock()

        navigation.listMenu({"path": "/root/my_first_level"})

        navigation.addListItem.assert_called_with({"path": "/root/my_first_level"}, {"path": "/root/my_first_level/my_second_level"})

    def test_listMenu_should_use_visibility_from_settings_to_decide_if_items_are_displayed(self):
        sys.argv = ["something", -1, "something_else"]
        list = ["false", "true", "false", "true"]
        sys.modules["__main__"].settings.getSetting.side_effect = lambda x: list.pop()
        navigation = BlipTVNavigation()
        navigation.categories = ({"path": "/root/my_first_level"}, {"path": "/root/my_first_level/my_second_level1"}, {"path": "/root/my_first_level/my_second_level2"}, {"path": "/root/my_first_level/my_second_level3"})
        navigation.list = Mock()
        navigation.addListItem = Mock()

        navigation.listMenu({"path": "/root/my_first_level"})

        navigation.addListItem.assert_any_call({"path": "/root/my_first_level"}, {"path": "/root/my_first_level/my_second_level1"})
        navigation.addListItem.assert_any_call({"path": "/root/my_first_level"}, {"path": "/root/my_first_level/my_second_level3"})

    def test_listMenu_should_check_if_download_path_is_set_to_decide_if_download_folder_is_visible(self):
        sys.argv = ["something", -1, "something_else"]
        list = ["true", "true", "true", "", "true"]
        sys.modules["__main__"].settings.getSetting.side_effect = lambda x: list.pop()
        navigation = BlipTVNavigation()
        navigation.categories = ({"path": "/root/my_first_level/my_second_level1", "feed": "downloads"}, {"path": "/root/my_first_level/my_second_level2", "feed": "downloads"})
        navigation.list = Mock()
        navigation.addListItem = Mock()

        navigation.listMenu({"path": "/root/my_first_level", "feed": "downloads"})

        navigation.addListItem.assert_called_with({'feed': 'downloads', 'path': '/root/my_first_level'}, {'feed': 'downloads', 'path': '/root/my_first_level/my_second_level1'})

    def test_listMenu_should_call_list_if_store_in_params(self):
        sys.argv = ["something", -1, "something_else"]
        navigation = BlipTVNavigation()
        navigation.list = Mock()
        navigation.addListItem = Mock()
        navigation.listMenu({"path": "/root/some_other_path", "store": "some_store"})

        navigation.list.assert_called_with({"path": "/root/some_other_path", "store": "some_store"})

    def test_listMenu_should_call_list_if_scraper_in_params(self):
        sys.argv = ["something", -1, "something_else"]
        navigation = BlipTVNavigation()
        navigation.list = Mock()
        navigation.addListItem = Mock()

        navigation.listMenu({"path": "/root/some_other_path", "scraper": "some_scraper"})

        navigation.list.assert_called_with({"path": "/root/some_other_path", "scraper": "some_scraper"})

    def test_listMenu_should_call_settings_getSetting_to_get_listview(self):
        sys.argv = ["something", -1, "something_else"]
        navigation = BlipTVNavigation()
        navigation.list = Mock()
        navigation.addListItem = Mock()

        navigation.listMenu({"path": "/root/some_other_path"})

        sys.modules["__main__"].settings.getSetting.assert_called_with("list_view")

    def test_listMenu_should_call_settings_getSetting_to_get_listview_twice(self):
        sys.argv = ["something", -1, "something_else"]
        settings = ["0", "0", "true"]
        sys.modules["__main__"].settings.getSetting.side_effect = lambda x: settings.pop()
        navigation = BlipTVNavigation()
        navigation.list = Mock()
        navigation.addListItem = Mock()

        navigation.listMenu({"path": "/root/some_other_path"})

        sys.modules["__main__"].settings.getSetting.assert_called_with("list_view")
        counter = 0
        for arg in sys.modules["__main__"].settings.getSetting.call_args_list:
            if arg[0][0] == "list_view":
                counter += 1
        assert(counter == 1)

    def test_listMenu_should_call_xbmc_executeBuiltin_correctly_if_list_view_is_set(self):
        sys.argv = ["something", -1, "something_else"]
        settings = ["1", "true", "1"]
        sys.modules["__main__"].settings.getSetting.side_effect = lambda x: settings.pop()
        navigation = BlipTVNavigation()
        navigation.list = Mock()
        navigation.addListItem = Mock()

        navigation.listMenu({"path": "/root/some_other_path"})

        sys.modules["__main__"].xbmc.executebuiltin.assert_called_with('Container.SetViewMode(500)')

    def test_listMenu_should_call_xbmc_plugin_end_of_directory_correctly(self):
        sys.argv = ["something", -1, "something_else"]
        settings = ["1", "true", "1"]
        sys.modules["__main__"].settings.getSetting.side_effect = lambda x: settings.pop()
        navigation = BlipTVNavigation()
        navigation.list = Mock()
        navigation.addListItem = Mock()

        navigation.listMenu({"path": "/root/some_other_path"})

        sys.modules["__main__"].xbmcplugin.endOfDirectory.assert_called_with(cacheToDisc=True, handle=-1, succeeded=True)

    def test_executeAction_should_call_storage_deleteStoredSearch_if_action_is_delete_search(self):
        navigation = BlipTVNavigation()

        navigation.executeAction({"action": "delete_search"})

        sys.modules["__main__"].storage.deleteStoredSearch.assert_called_with({"action": "delete_search"})

    def test_executeAction_should_call_storage_editStoredSearch_if_action_is_edit_search(self):
        navigation = BlipTVNavigation()
        navigation.listMenu = Mock()

        navigation.executeAction({"action": "edit_search"})

        sys.modules["__main__"].storage.editStoredSearch.assert_called_with({"action": "edit_search"})

    def test_executeAction_should_call_listMenu_if_action_is_edit_search(self):
        navigation = BlipTVNavigation()
        navigation.listMenu = Mock()

        navigation.executeAction({"action": "edit_search"})

        navigation.listMenu.assert_called_with({"action": "edit_search"})

    def test_executeAction_should_call_removeFromFavorites_if_action_is_remove_favorite(self):
        sys.modules["__main__"].storage.deleteFromMyFavoriteShows = Mock()
        navigation = BlipTVNavigation()
        navigation.removeFromFavorites = Mock()

        navigation.executeAction({"action": "delete_favorite"})

        sys.modules["__main__"].storage.deleteFromMyFavoriteShows.assert_called_with({"action": "delete_favorite"})

    def test_executeAction_should_open_settings_if_action_is_settings(self):
        sys.modules["__main__"].storage.deleteFromMyFavoriteShows = Mock()
        navigation = BlipTVNavigation()
        navigation.removeFromFavorites = Mock()

        navigation.executeAction({"action": "settings"})

        sys.modules["__main__"].settings.openSettings.assert_called_with()

    def test_executeAction_should_call_addToFavorites_if_action_is_add_favorite(self):
        sys.modules["__main__"].scraper.addShowToMyFavorites = Mock()
        navigation = BlipTVNavigation()
        navigation.addToFavorites = Mock()

        navigation.executeAction({"action": "add_favorite"})

        sys.modules["__main__"].scraper.addShowToMyFavorites.assert_called_with({"action": "add_favorite"})

    def test_executeAction_should_call_downloader_downloadVideo_if_action_is_download(self):
        sys.modules["__main__"].player.getVideoObject = Mock()
        sys.modules["__main__"].player.getVideoObject.return_value = {"videoid": "video1", "video_url": "Mock url", "Title": "Mock Title"}
        sys.modules["__main__"].settings.getSetting.return_value = "some_path"

        navigation = BlipTVNavigation()

        navigation.executeAction({"action": "download"})

        sys.modules["__main__"].downloader.download.assert_called_with("Mock Title-[video1].mp4", {"action": "download", "url": "Mock url", "download_path": "some_path", "useragent": "curl/7.22.0 (x86_64-pc-linux-gnu) libcurl/7.22.0 OpenSSL/1.0.1 zlib/1.2.3.4 libidn/1.23 librtmp/2.3"})

    def test_executeAction_should_call_player_playVideo_if_action_is_play_video(self):
        navigation = BlipTVNavigation()

        navigation.executeAction({"action": "play_video"})

        sys.modules["__main__"].player.playVideo.assert_called_with({"action": "play_video"})

    def ttest_executeAction_should_call_playlist_queueVideo_if_action_is_queue_video(self):
        navigation = BlipTVNavigation()

        navigation.executeAction({"action": "queue_video"})

        sys.modules["__main__"].playlist.queueVideo.assert_called_with({"action": "queue_video"})

    def ttest_executeAction_should_call_playlist_playAll_if_action_is_play_all(self):
        navigation = BlipTVNavigation()

        navigation.executeAction({"action": "play_all"})

        sys.modules["__main__"].playlist.playAll.assert_called_with({"action": "play_all"})

    def test_list_should_ask_user_for_input_if_scraper_is_search_and_search_is_missing_from_params(self):
        sys.modules["__main__"].scraper.scrape.return_value = ([], 200)
        sys.modules["__main__"].language.return_value = "some_string"
        navigation = BlipTVNavigation()
        navigation.parseVideoList = Mock()
        navigation.parseFolderList = Mock()
        navigation.showListingError = Mock()

        navigation.list({"scraper": "search"})

        sys.modules["__main__"].common.getUserInput.assert_called_with("some_string", "")

    def test_list_should_ask_user_for_input_if_scraper_is_show_search_and_search_is_missing_from_params(self):
        sys.modules["__main__"].scraper.scrape.return_value = ([], 200)
        sys.modules["__main__"].language.return_value = "some_string"
        navigation = BlipTVNavigation()
        navigation.parseVideoList = Mock()
        navigation.parseFolderList = Mock()
        navigation.showListingError = Mock()

        navigation.list({"scraper": "show_search"})

        sys.modules["__main__"].common.getUserInput.assert_called_with("some_string", "")

    def test_list_should_call_scraper_scrape_if_scraper_is_in_params(self):
        sys.modules["__main__"].scraper.scrape.return_value = ([], 200)
        navigation = BlipTVNavigation()
        navigation.parseVideoList = Mock()
        navigation.parseFolderList = Mock()
        navigation.showListingError = Mock()

        navigation.list({"scraper": "some_scraper"})

        sys.modules["__main__"].scraper.scrape.assert_called_with({"scraper": "some_scraper"})

    def test_list_should_call_storage_list_if_store_is_in_params(self):
        sys.modules["__main__"].storage.list.return_value = ([], 200)
        navigation = BlipTVNavigation()
        navigation.parseVideoList = Mock()
        navigation.parseFolderList = Mock()
        navigation.showListingError = Mock()

        navigation.list({"store": "some_store"})

        sys.modules["__main__"].storage.list.assert_called_with({"store": "some_store"})

    def test_list_should_call_parseFolderList_if_list_was_successfull_and_folder_is_in_params(self):
        sys.modules["__main__"].scraper.scrape.return_value = ["folders"]
        navigation = BlipTVNavigation()
        navigation.parseVideoList = Mock()
        navigation.parseFolderList = Mock()
        navigation.showListingError = Mock()

        navigation.list({"folder": "true", "scraper": "some_scraper"})

        navigation.parseFolderList.assert_called_with({"folder": "true", "scraper": "some_scraper"}, ["folders"])

    def test_list_should_call_parseVideoList_if_list_was_successfull_and_folder_is_not_in_params(self):
        sys.modules["__main__"].scraper.scrape.return_value = ["videos"]
        navigation = BlipTVNavigation()
        navigation.parseVideoList = Mock()
        navigation.parseFolderList = Mock()
        navigation.showListingError = Mock()

        navigation.list({"scraper": "some_scraper"})

        navigation.parseVideoList.assert_called_with({"scraper": "some_scraper"}, ["videos"])

    def test_list_should_call_showListingError_on_listing_error(self):
        sys.modules["__main__"].scraper.scrape.return_value = []
        sys.modules["__main__"].language.return_value = "some_string"
        navigation = BlipTVNavigation()
        navigation.parseVideoList = Mock()
        navigation.parseFolderList = Mock()
        navigation.showListingError = Mock()

        navigation.list({"scraper": "staff_picks"})

        navigation.showListingError.assert_any_call({"scraper": "staff_picks"})

    def test_showListingError_should_call_showMessage_on_listing_error_with_proper_label(self):
        sys.modules["__main__"].scraper.scrape.return_value = []
        sys.modules["__main__"].language.return_value = "some_string"
        navigation = BlipTVNavigation()

        navigation.showListingError({"scraper": "staff_picks"})

        sys.modules["__main__"].utils.showMessage.assert_any_call("some_string", "some_string")
        sys.modules["__main__"].language.assert_any_call(30601)

    def test_addListItem_should_call_addVideoListItem_if_item_action_is_play_video(self):
        navigation = BlipTVNavigation()
        navigation.addVideoListItem = Mock()

        navigation.addListItem({}, {"action": "play_video"})

        navigation.addVideoListItem.assert_called_with({}, {"action": "play_video"}, 0)
    
    def test_addListItem_should_call_addActionListItem_if_item_has_action(self):
        navigation = BlipTVNavigation()
        navigation.addActionListItem = Mock()
        
        navigation.addListItem({}, {"action": "some_action"})
        
        navigation.addActionListItem.assert_called_with({}, {"action": "some_action"})
    
    def test_addListItem_should_call_addFolderListItem_if_item_doesnt_have_an_action(self):
        navigation = BlipTVNavigation()
        navigation.addFolderListItem = Mock()
        
        navigation.addListItem({}, {})
        
        navigation.addFolderListItem.assert_called_with({}, {})

    def test_addFolderListItem_should_call_utils_get_thumbnail_to_get_icon_path(self):
        sys.argv = ["some_path", -1, "some_params"]
        navigation = BlipTVNavigation()
        navigation.addFolderContextMenuItems = Mock()
        navigation.addFolderContextMenuItems.return_value = []
        
        navigation.addFolderListItem({}, {"action": "some_action", "icon": "some_icon"})
        
        sys.modules["__main__"].utils.getThumbnail("some_icon")
    
    def test_addFolderListItem_should_call_addFolderContextMenuItems_to_get_context_menu_items(self):
        sys.argv = ["some_path", -1, "some_params"]
        navigation = BlipTVNavigation()
        navigation.addFolderContextMenuItems = Mock()
        navigation.addFolderContextMenuItems.return_value = []
        
        navigation.addFolderListItem({}, {"action": "some_action", "icon": "some_icon"})
        
        navigation.addFolderContextMenuItems.assert_called_with({}, {"action": "some_action", "icon": "some_icon"})
    
    def test_addFolderListItem_should_call_utils_get_thumbnail_to_get_thumbnail_path(self):
        sys.argv = ["some_path", -1, "some_params"]
        navigation = BlipTVNavigation()
        navigation.addFolderContextMenuItems = Mock()
        navigation.addFolderContextMenuItems.return_value = []
        
        navigation.addFolderListItem({}, {"action": "some_action", "icon": "some_icon", "thumbnail": "some_thumbnail"})
        
        sys.modules["__main__"].utils.getThumbnail.assert_called_with("some_thumbnail")
    
    def test_addFolderListItem_should_call_xbmcgui_ListItem_to_fetch_xbmc_listitem_object(self):
        sys.argv = ["some_path", -1, "some_params"]
        sys.modules["__main__"].utils.getThumbnail.return_value = "some_image_path"
        navigation = BlipTVNavigation()
        navigation.addFolderContextMenuItems = Mock()
        navigation.addFolderContextMenuItems.return_value = []
        
        navigation.addFolderListItem({}, {"action": "some_action", "Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail"})
        
        sys.modules["__main__"].xbmcgui.ListItem.assert_called_with("some_title", iconImage='some_icon', thumbnailImage='some_image_path')
    
    def test_addFolderListItem_should_call_utils_buildItemUrl_to_get_proper_item_url(self):
        sys.argv = ["some_path", -1, "some_params"]
        sys.modules["__main__"].utils.getThumbnail.return_value = "some_image_path"
        navigation = BlipTVNavigation()
        navigation.addFolderContextMenuItems = Mock()
        navigation.addFolderContextMenuItems.return_value = []
        
        navigation.addFolderListItem({}, {"action": "some_action", "Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail"})
        
        sys.modules["__main__"].utils.buildItemUrl({"action": "some_action", "Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail"})
    
    def test_addFolderListItem_should_call_listitem_addContextMenuItems_to_add_context_menu(self):
        sys.argv = ["some_path", -1, "some_params"]
        sys.modules["__main__"].utils.getThumbnail.return_value = "some_image_path"
        navigation = BlipTVNavigation()
        navigation.addFolderContextMenuItems = Mock()
        navigation.addFolderContextMenuItems.return_value = [1, 2]
        
        navigation.addFolderListItem({}, {"action": "some_action", "Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail"})
        
        sys.modules["__main__"].xbmcgui.ListItem().addContextMenuItems.assert_called_with([1, 2], replaceItems=False)
    
    def test_addFolderListItem_should_call_listitem_setProperty_to_inidicate_item_is_a_folder(self):
        sys.argv = ["some_path", -1, "some_params"]
        navigation = BlipTVNavigation()
        navigation.addFolderContextMenuItems = Mock()
        navigation.addFolderContextMenuItems.return_value = []
        
        navigation.addFolderListItem({}, {"action": "some_action", "Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail"})
        
        sys.modules["__main__"].xbmcgui.ListItem().setProperty.assert_called_with('Folder', 'true')
    
    def test_addFolderListItem_should_call_settings_getSetting_to_fetch_downloadPath_if_item_feed_is_downloads(self):
        sys.argv = ["some_path", -1, "some_params"]
        navigation = BlipTVNavigation()
        navigation.addFolderContextMenuItems = Mock()
        navigation.addFolderContextMenuItems.return_value = []
        
        navigation.addFolderListItem({}, {"feed": "downloads", "Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail"})
        
        sys.modules["__main__"].settings.getSetting.assert_called_with("downloadPath")
    
    def test_addFolderListItem_should_call_xbmcplugin_addDirectoryItem_correctly(self):
        sys.argv = ["some_path", -1, "some_params"]
        navigation = BlipTVNavigation()
        navigation.addFolderContextMenuItems = Mock()
        navigation.addFolderContextMenuItems.return_value = []
        
        navigation.addFolderListItem({}, {"feed": "downloads", "Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail"})
        
        sys.modules["__main__"].settings.getSetting.assert_called_with("downloadPath")
        
    def test_addActionListItem_should_call_utils_get_thumbnail_to_get_thumbnail_path(self):
        sys.argv = ["some_path", -1, "some_params"]
        navigation = BlipTVNavigation()
        
        navigation.addActionListItem({}, {"action": "some_action", "Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail"})
        
        sys.modules["__main__"].utils.getThumbnail.assert_called_with("some_thumbnail")

    def test_addActionListItem_should_call_xbmcgui_ListItem_to_fetch_xbmc_listitem_object(self):
        sys.argv = ["some_path", -1, "some_params"]
        sys.modules["__main__"].utils.getThumbnail.return_value = "some_image_path"
        navigation = BlipTVNavigation()
        
        navigation.addActionListItem({}, {"action": "some_action", "Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail"})
        
        sys.modules["__main__"].xbmcgui.ListItem.assert_called_with("some_title",iconImage='DefaultFolder.png', thumbnailImage='some_image_path')

    def test_addActionListItem_should_call_listitem_setProperty_to_inidicate_item_is_playable_if_item_action_is_playbyid(self):
        sys.argv = ["some_path", -1, "some_params"]
        sys.modules["__main__"].utils.getThumbnail.return_value = "some_image_path"
        navigation = BlipTVNavigation()
        
        navigation.addActionListItem({}, {"action": "playbyid", "Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail"})
        
        sys.modules["__main__"].xbmcgui.ListItem().setProperty.assert_called_with("IsPlayable", "true")

    def test_addActionListItem_should_call_xbmcplugin_addDirectoryItem_correctly(self):
        sys.argv = ["some_path", -1, "some_params"]
        sys.modules["__main__"].xbmcgui.ListItem.return_value = []
        sys.modules["__main__"].utils.getThumbnail.return_value = "some_image_path"
        navigation = BlipTVNavigation()
        
        navigation.addActionListItem({}, {"action": "some_action", "Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail"})
        
        sys.modules["__main__"].xbmcplugin.addDirectoryItem.assert_called_with(totalItems = 0, url="some_path?path=None&action=some_action&", isFolder=True, listitem = [], handle=-1)

    def test_addVideoListItem_should_call_utils_get_thumbnail_to_get_icon_path(self):
        sys.argv = ["some_path", -1, "some_params"]
        sys.modules["__main__"].utils.getThumbnail.return_value = "some_image_path"
        navigation = BlipTVNavigation()
        navigation.addVideoContextMenuItems = Mock()
        
        navigation.addVideoListItem({}, {"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail"})
        
        sys.modules["__main__"].utils.getThumbnail.assert_called_with("some_icon")

    def test_addVideoListItem_should_call_xbmcgui_ListItem_to_fetch_xbmc_listitem_object(self):
        sys.argv = ["some_path", -1, "some_params"]
        sys.modules["__main__"].utils.getThumbnail.return_value = "some_image_path"
        navigation = BlipTVNavigation()
        navigation.addVideoContextMenuItems = Mock()
        
        navigation.addVideoListItem({}, {"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail"})
        
        sys.modules["__main__"].xbmcgui.ListItem.assert_called_with("some_title", iconImage="some_image_path", thumbnailImage="some_thumbnail")

    def test_addVideoListItem_should_call_addVideoContextMenuItems_to_get_context_menu_items(self):
        sys.argv = ["some_path", -1, "some_params"]
        sys.modules["__main__"].utils.getThumbnail.return_value = "some_image_path"
        navigation = BlipTVNavigation()
        navigation.addVideoContextMenuItems = Mock()
        
        navigation.addVideoListItem({}, {"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail"})
        
        navigation.addVideoContextMenuItems.assert_called_with({}, {"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail"})

    def test_addVideoListItem_should_call_listitem_addContextMenuItems_to_add_context_menu(self):
        sys.argv = ["some_path", -1, "some_params"]
        sys.modules["__main__"].utils.getThumbnail.return_value = "some_image_path"
        navigation = BlipTVNavigation()
        navigation.addVideoContextMenuItems = Mock()
        navigation.addVideoContextMenuItems.return_value = []
        
        navigation.addVideoListItem({}, {"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail"})
        
        sys.modules["__main__"].xbmcgui.ListItem().addContextMenuItems.assert_called_with([], replaceItems=True)

    def test_addVideoListItem_should_call_listitem_setProperty_to_indicate_listitem_is_video(self):
        sys.argv = ["some_path", -1, "some_params"]
        sys.modules["__main__"].utils.getThumbnail.return_value = "some_image_path"
        navigation = BlipTVNavigation()
        navigation.addVideoContextMenuItems = Mock()
        navigation.addVideoContextMenuItems.return_value = []
        
        navigation.addVideoListItem({}, {"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail"})
        
        sys.modules["__main__"].xbmcgui.ListItem().setProperty.assert_any_call("Video", "true")
        sys.modules["__main__"].xbmcgui.ListItem().setProperty.assert_any_call("IsPlayable", "true")

    def test_addVideoListItem_should_call_listitem_setInfo_to_allow_xbmc_to_sort_and_display_video_info(self):
        sys.argv = ["some_path", -1, "some_params"]
        sys.modules["__main__"].utils.getThumbnail.return_value = "some_image_path"
        navigation = BlipTVNavigation()
        navigation.addVideoContextMenuItems = Mock()
        navigation.addVideoContextMenuItems.return_value = []
        
        navigation.addVideoListItem({}, {"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail"})
        
        sys.modules["__main__"].xbmcgui.ListItem().setInfo.assert_called_with(infoLabels={'icon': 'some_icon', 'thumbnail': 'some_thumbnail', 'Title': 'some_title'}, type='Video')

    def test_addVideoListItem_should_call_xbmcplugin_addDirectoryItem_correctly(self):
        sys.argv = ["some_path", -1, "some_params"]
        sys.modules["__main__"].utils.getThumbnail.return_value = "some_image_path"
        list_item = Mock()
        sys.modules["__main__"].xbmcgui.ListItem.return_value = list_item 
        navigation = BlipTVNavigation()
        navigation.addVideoContextMenuItems = Mock()
        navigation.addVideoContextMenuItems.return_value = []
        
        navigation.addVideoListItem({}, {"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail"})
        
        sys.modules["__main__"].xbmcplugin.addDirectoryItem.assert_called_with(handle=-1, url="some_path?path=/root/video&action=play_video&videoid=None", listitem=list_item, isFolder=False, totalItems=1)

    def test_parseFolderList_should_set_cache_false_if_item_is_store_og_user_feed(self):
        sys.argv = ["some_path", -1, "some_params"]
        sys.modules["__main__"].utils.getThumbnail.return_value = "some_image_path"
        navigation = BlipTVNavigation()
        navigation.addVideoContextMenuItems = Mock()
        navigation.addFolderListItem = Mock()
        
        navigation.parseFolderList({"user_feed": "some_feed", "path": "some_path"}, [{"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail"}])
        
        sys.modules["__main__"].xbmcplugin.endOfDirectory.assert_called_with(handle=-1, succeeded=True, cacheToDisc=False)

    def test_parseFolderList_should_call_addFolderListItem_for_each_item(self):
        sys.argv = ["some_path", -1, "some_params"]
        sys.modules["__main__"].utils.getThumbnail.return_value = "some_image_path"
        navigation = BlipTVNavigation()
        navigation.addVideoContextMenuItems = Mock()
        navigation.addFolderListItem = Mock()
        
        navigation.parseFolderList({"user_feed": "some_feed", "path": "some_path"}, [{"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail"}, {"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail"}, {"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail"}])
        
        assert(navigation.addFolderListItem.call_count == 3)

    def test_parseFolderList_should_call_xbmcplugin_endOfDirectory_correctly(self):
        sys.argv = ["some_path", -1, "some_params"]
        sys.modules["__main__"].utils.getThumbnail.return_value = "some_image_path"
        navigation = BlipTVNavigation()
        navigation.addVideoContextMenuItems = Mock()
        navigation.addFolderListItem = Mock()
        
        navigation.parseFolderList({"user_feed": "some_feed", "path": "some_path"}, [{"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail"}, {"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail"}, {"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail"}])
        
        sys.modules["__main__"].xbmcplugin.endOfDirectory.assert_called_with(handle=-1, succeeded=True, cacheToDisc=False)

    def test_parseVideoList_should_skip_items_where_videoid_is_false(self):
        sys.argv = ["some_path", -1, "some_params"]
        sys.modules["__main__"].utils.getThumbnail.return_value = "some_image_path"
        sys.modules["__main__"].settings.getSetting.return_value = 0
        navigation = BlipTVNavigation()
        navigation.addVideoContextMenuItems = Mock()
        navigation.addVideoListItem = Mock()
        
        navigation.parseVideoList({"user_feed": "some_feed", "path": "some_path"}, [{"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail"}, {"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail", "videoid": "false"}, {"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail"}])
        
        assert(navigation.addVideoListItem.call_count == 2)

    def ttest_parseVideoList_should_call_addFolderListItem_to_next_item(self):
        sys.argv = ["some_path", -1, "some_params"]
        sys.modules["__main__"].utils.getThumbnail.return_value = "some_image_path"
        sys.modules["__main__"].settings.getSetting.return_value = 0
        navigation = BlipTVNavigation()
        navigation.addVideoContextMenuItems = Mock()
        navigation.addVideoListItem = Mock()
        navigation.addFolderListItem = Mock()
        
        navigation.parseVideoList({"scraper": "watch_later", "path": "some_path"}, [{"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail"}, {"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail", "videoid": "false"}, {"next": "true", "Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail"}])
        
        navigation.addFolderListItem.assert_called_with({"scraper": "watch_later", "path": "some_path"}, {"next": "true", 'path': 'some_path', 'icon': 'some_icon', 'index': '3', 'thumbnail': 'some_thumbnail', 'Title': 'some_title'}, 3)

    def ttest_parseVideoList_should_call_addVideoListItem_if_item_is_not_next_item(self):
        sys.argv = ["some_path", -1, "some_params"]
        sys.modules["__main__"].utils.getThumbnail.return_value = "some_image_path"
        sys.modules["__main__"].settings.getSetting.return_value = 0
        navigation = BlipTVNavigation()
        navigation.addVideoContextMenuItems = Mock()
        navigation.addVideoListItem = Mock()
        navigation.addFolderListItem = Mock()
        
        navigation.parseVideoList({"scraper": "watch_later", "path": "some_path"}, [{"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail"}, {"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail", "videoid": "false"}, {"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail", "next": "true"}])
        
        navigation.addVideoListItem.assert_called_once_with({'path': 'some_path', 'scraper': 'watch_later'}, {'path': 'some_path', 'icon': 'some_icon', 'index': '1', 'thumbnail': 'some_thumbnail', 'Title': 'some_title'}, 3)

    def test_parseVideoList_should_call_settings_getSetting_to_get_list_view(self):
        sys.argv = ["some_path", -1, "some_params"]
        sys.modules["__main__"].utils.getThumbnail.return_value = "some_image_path"
        sys.modules["__main__"].settings.getSetting.return_value = 0
        navigation = BlipTVNavigation()
        navigation.addVideoContextMenuItems = Mock()
        navigation.addVideoListItem = Mock()
        navigation.addFolderListItem = Mock()
        
        navigation.parseVideoList({"scraper": "watch_later", "path": "some_path"}, [{"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail"}, {"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail", "videoid": "false"}, {"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail", "next": "true"}])
        
        sys.modules["__main__"].settings.getSetting.assert_called_with("list_view")

    def test_parseVideoList_should_call_xbmc_executebuiltin_if_list_view_is_set(self):
        sys.argv = ["some_path", -1, "some_params"]
        sys.modules["__main__"].utils.getThumbnail.return_value = "some_image_path"
        sys.modules["__main__"].settings.getSetting.return_value = 1
        navigation = BlipTVNavigation()
        navigation.addVideoContextMenuItems = Mock()
        navigation.addVideoListItem = Mock()
        navigation.addFolderListItem = Mock()
        
        navigation.parseVideoList({"scraper": "watch_later", "path": "some_path"}, [{"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail"}, {"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail", "videoid": "false"}, {"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail", "next": "true"}])
        
        sys.modules["__main__"].xbmc.executebuiltin.assert_called_with('Container.SetViewMode(500)')
        
    def test_parseVideoList_should_call_xbmcplugin_addSortMethod_for_valid_sort_methods(self):
        sys.argv = ["some_path", -1, "some_params"]
        sys.modules["__main__"].utils.getThumbnail.return_value = "some_image_path"
        sys.modules["__main__"].settings.getSetting.return_value = 1
        navigation = BlipTVNavigation()
        navigation.addVideoContextMenuItems = Mock()
        navigation.addVideoListItem = Mock()
        navigation.addFolderListItem = Mock()
        
        navigation.parseVideoList({"scraper": "watch_later", "path": "some_path"}, [{"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail"}, {"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail", "videoid": "false"}, {"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail", "next": "true"}])
        
        sys.modules["__main__"].xbmcplugin.addSortMethod.assert_any_call(handle=-1, sortMethod=sys.modules["__main__"].xbmcplugin.SORT_METHOD_UNSORTED)
        sys.modules["__main__"].xbmcplugin.addSortMethod.assert_any_call(handle=-1, sortMethod=sys.modules["__main__"].xbmcplugin.SORT_METHOD_LABEL)
        sys.modules["__main__"].xbmcplugin.addSortMethod.assert_any_call(handle=-1, sortMethod=sys.modules["__main__"].xbmcplugin.SORT_METHOD_VIDEO_RATING)
        sys.modules["__main__"].xbmcplugin.addSortMethod.assert_any_call(handle=-1, sortMethod=sys.modules["__main__"].xbmcplugin.SORT_METHOD_DATE)
        sys.modules["__main__"].xbmcplugin.addSortMethod.assert_any_call(handle=-1, sortMethod=sys.modules["__main__"].xbmcplugin.SORT_METHOD_PROGRAM_COUNT)
        sys.modules["__main__"].xbmcplugin.addSortMethod.assert_any_call(handle=-1, sortMethod=sys.modules["__main__"].xbmcplugin.SORT_METHOD_VIDEO_RUNTIME)
        sys.modules["__main__"].xbmcplugin.addSortMethod.assert_any_call(handle=-1, sortMethod=sys.modules["__main__"].xbmcplugin.SORT_METHOD_GENRE)

    def test_parseVideoList_should_call_xbmcplugin_endOfDirectory_correctly(self):
        sys.modules["__main__"].utils.getThumbnail.return_value = "some_image_path"
        sys.modules["__main__"].settings.getSetting.return_value = 1
        navigation = BlipTVNavigation()
        navigation.addVideoContextMenuItems = Mock()
        navigation.addVideoListItem = Mock()
        navigation.addFolderListItem = Mock()
        
        navigation.parseVideoList({"scraper": "watch_later", "path": "some_path"}, [{"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail"}, {"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail", "videoid": "false"}, {"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail", "next": "true"}])
        
        sys.modules["__main__"].xbmcplugin.endOfDirectory.assert_called_with(cacheToDisc=True, handle=-1, succeeded=True)
    
    def test_addVideoContextMenuItems_should_call_utils_makeAscii_on_Title(self):
        sys.argv = ["some_plugin", -1, "some_path"]
        sys.modules["__main__"].language.return_value = "some_button_string %s"
        sys.modules["__main__"].common.makeAscii.side_effect = lambda x: x
        navigation = BlipTVNavigation()
        path_params = {}
        item_params = {"Title": "some_title", "path": "some_path", "icon": "some_icon", "thumbnail": "some_thumbnail"}
        
        navigation.addVideoContextMenuItems(path_params,item_params)
        
        sys.modules["__main__"].common.makeAscii.assert_any_call("some_title")
        
    def ttest_addVideoContextMenuItems_should_call_utils_makeAscii_on_Studio(self):  # Disabled in function
        sys.argv = ["some_plugin", -1, "some_path"]
        sys.modules["__main__"].language.return_value = "some_button_string %s"
        sys.modules["__main__"].common.makeAscii.side_effect = lambda x: x
        navigation = BlipTVNavigation()
        path_params = {}
        item_params = {"Title": "some_title", "path": "some_path", "icon": "some_icon", "thumbnail": "some_thumbnail"}
        
        #cm = navigation.addVideoContextMenuItems(path_params, item_params)
        
        sys.modules["__main__"].common.makeAscii.assert_called_with("Unknown Author")
        
    def prepareContestMenu(self):
        sys.argv = ["some_plugin", -1, "some_path"]
        sys.modules["__main__"].language.return_value = "some_button_string %s"
        sys.modules["__main__"].common.makeAscii.side_effect = lambda x: x
        
    def assert_context_menu_contains(self, cm, title, path):
        found = False
        for (ititle, ipath) in cm:
            if ititle == title and ipath == path:
                    found = True

        if found == False:
            print "Failed to find item in context menu: " + title + " - " + path + "\r\n"
            
            for (title, path) in cm:
                print "item " + str(cm.index((title, path))) + ": " + title + " - " + path
                    
        assert(found)

    def assert_context_menu_doesnt_contain(self, cm, title, path):
        found = False
        for (ititle, ipath) in cm:
            if ititle == title and ipath == path:
                    found = True

        if found == True:
            print "Failed to find item in context menu: " + title + " - " + path + "\r\n"
            
            for (title, path) in cm:
                print "item " + str(cm.index((title, path))) + ": " + title + " - " + path
                    
        assert(found == False)

    def test_addVideoContextMenuItems_should_add_download_video_to_all_video_items(self):
        self.prepareContestMenu()
        navigation = BlipTVNavigation()
        path_params = {}
        item_params = {"Title": "some_title", "path": "some_path", "icon": "some_icon", "thumbnail": "some_thumbnail", "videoid": "some_id"}
        
        cm = navigation.addVideoContextMenuItems(path_params, item_params)
        
        sys.modules["__main__"].language.assert_any_call(30501)
        self.assert_context_menu_contains(cm, "some_button_string %s", 'XBMC.RunPlugin(some_plugin?path=some_path&action=download&videoid=some_id)')

    def ttest_addVideoContextMenuItems_should_add_add_favorite_option_if_user_is_logged_in_and_item_is_not_in_favorites_feed(self):
        self.prepareContestMenu()
        sys.modules["__main__"].settings.getSetting.return_value = "something"
        navigation = BlipTVNavigation()
        path_params = {}
        item_params = {"Title": "some_title", "path": "some_path", "icon": "some_icon", "thumbnail": "some_thumbnail", "videoid": "some_id"}
        
        cm = navigation.addVideoContextMenuItems(path_params, item_params)
        
        sys.modules["__main__"].language.assert_any_call(30503)
        sys.modules["__main__"].settings.getSetting.assert_any_call("username")
        sys.modules["__main__"].settings.getSetting.assert_any_call("oauth2_access_token")
        self.assert_context_menu_contains(cm, "some_button_string %s", 'XBMC.RunPlugin(some_plugin?path=some_path&action=add_favorite&videoid=some_id&)')

    def test_addVideoContextMenuItems_should_not_add_more_videos_by_user_if_item_is_in_uploads_feed(self):
        self.prepareContestMenu()
        sys.modules["__main__"].settings.getSetting.return_value = "something"
        navigation = BlipTVNavigation()
        path_params = {"user_feed": "uploads"}
        item_params = {"Title": "some_title", "path": "some_path", "icon": "some_icon", "thumbnail": "some_thumbnail"}
        
        cm = navigation.addVideoContextMenuItems(path_params, item_params)
        
        self.assert_context_menu_doesnt_contain(cm, "some_button_string Unknown Author", 'XBMC.Container.Update(some_plugin?path=/root/video&feed=uploads&channel=Unknown+Author)')
        
    def test_addVideoContextMenuItems_should_add_now_playing_option_to_video_items(self):
        self.prepareContestMenu()
        sys.modules["__main__"].settings.getSetting.return_value = "something"
        navigation = BlipTVNavigation()
        path_params = {}
        item_params = {"Title": "some_title", "path": "some_path", "icon": "some_icon", "thumbnail": "some_thumbnail", "videoid": "someid"}
        
        cm = navigation.addVideoContextMenuItems(path_params, item_params)
        
        sys.modules["__main__"].language.assert_any_call(30523)
        self.assert_context_menu_contains(cm, "some_button_string %s", 'XBMC.ActivateWindow(VideoPlaylist)')

    def test_addVideoContextMenuItems_should_add_video_info_option_to_video_items(self):
        self.prepareContestMenu()
        sys.modules["__main__"].settings.getSetting.return_value = "something"
        navigation = BlipTVNavigation()
        path_params = {}
        item_params = {"Title": "some_title", "path": "some_path", "icon": "some_icon", "thumbnail": "some_thumbnail", "videoid": "someid"}
        
        cm = navigation.addVideoContextMenuItems(path_params, item_params)
        
        sys.modules["__main__"].language.assert_any_call(30523)
        self.assert_context_menu_contains(cm, "some_button_string %s", 'XBMC.Action(Info)')

    def test_addFolderContextMenuItems_should_not_add_any_options_to_next_folders(self):
        self.prepareContestMenu()
        sys.modules["__main__"].settings.getSetting.return_value = "something"
        navigation = BlipTVNavigation()
        path_params = {}
        item_params = {"Title": "some_title", "path": "some_path", "icon": "some_icon", "thumbnail": "some_thumbnail", "next": "true"}
        
        cm = navigation.addFolderContextMenuItems(path_params, item_params)
        
        assert(cm == [])

    def test_addFolderContextMenuItems_should_add_edit_and_delete_options_to_searches(self):
        self.prepareContestMenu()
        sys.modules["__main__"].settings.getSetting.return_value = "something"
        navigation = BlipTVNavigation()
        path_params = {}
        item_params = {"Title": "some_title", "path": "some_path", "icon": "some_icon", "thumbnail": "some_thumbnail", "videoid": "someid", "scraper": "search", "search": "some_search"}
        
        cm = navigation.addFolderContextMenuItems(path_params, item_params)
        
        sys.modules["__main__"].language.assert_any_call(30515)
        sys.modules["__main__"].language.assert_any_call(30508)
        self.assert_context_menu_contains(cm, "some_button_string %s", 'XBMC.Container.Update(some_plugin?path=some_path&action=edit_search&search=some_search&)')
        self.assert_context_menu_contains(cm, "some_button_string %s", 'XBMC.RunPlugin(some_plugin?path=some_path&action=delete_search&delete=some_search&)')
        
    def test_addFolderContextMenuItems_should_add_now_playing_option_to_folder_items(self):
        self.prepareContestMenu()
        sys.modules["__main__"].settings.getSetting.return_value = "something"
        navigation = BlipTVNavigation()
        path_params = {}
        item_params = {"Title": "some_title", "path": "some_path", "icon": "some_icon", "thumbnail": "some_thumbnail"}
        
        cm = navigation.addFolderContextMenuItems(path_params, item_params)
        
        sys.modules["__main__"].language.assert_any_call(30523)
        self.assert_context_menu_contains(cm, "some_button_string %s", 'XBMC.ActivateWindow(VideoPlaylist)')

    def test_addFolderContextMenuItems_should_add_add_to_favorites(self):
        self.prepareContestMenu()
        sys.modules["__main__"].settings.getSetting.return_value = "something"
        navigation = BlipTVNavigation()
        path_params = {}
        item_params = {"Title": "some_title", "path": "some_path", "icon": "some_icon", "thumbnail": "some_thumbnail", "show": "some_show"}
        
        cm = navigation.addFolderContextMenuItems(path_params, item_params)
        
        self.assert_context_menu_contains(cm, "some_button_string %s", 'XBMC.ActivateWindow(VideoPlaylist)')
        self.assert_context_menu_contains(cm, "some_button_string %s", 'XBMC.RunPlugin(some_plugin?path=some_path&action=add_favorite&show=some_show&)')

    def test_addFolderContextMenuItems_should_add_delete_from_favorites(self):
        self.prepareContestMenu()
        sys.modules["__main__"].settings.getSetting.return_value = "something"
        navigation = BlipTVNavigation()
        path_params = {"store": "favorites"}
        item_params = {"Title": "some_title", "path": "some_path", "icon": "some_icon", "thumbnail": "some_thumbnail", "show": "some_show"}
        
        cm = navigation.addFolderContextMenuItems(path_params, item_params)
        
        self.assert_context_menu_contains(cm, "some_button_string %s", 'XBMC.ActivateWindow(VideoPlaylist)')
        self.assert_context_menu_contains(cm, "some_button_string %s", 'XBMC.RunPlugin(some_plugin?path=some_path&action=delete_favorite&show=some_show&)')
        
if __name__ == '__main__':
    nose.runmodule()
