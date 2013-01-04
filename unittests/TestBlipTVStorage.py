# -*- coding: utf-8 -*-
import nose
import BaseTestCase
from mock import Mock, patch
import sys
from BlipTVStorage import BlipTVStorage 


class TestBlipTVStorage(BaseTestCase.BaseTestCase):
    def test_list_should_call_getStoredSearches_if_store_is_searches(self):
        storage = BlipTVStorage()
        storage.getStoredSearches = Mock()
        storage.getStoredSearches.return_value = ""

        storage.list({"store": "searches"})

        storage.getStoredSearches.assert_called_with({"store": "searches"})

    def test_getStoredSearches_should_call_retrieve_to_get_searches(self):
        storage = BlipTVStorage()
        storage.retrieveValue = Mock()
        storage.retrieveValue.return_value = repr(["some_search"])
        storage.retrieve = Mock()
        storage.retrieve.return_value = ["some_search"]
        storage.store = Mock()

        storage.getStoredSearches({"path": "some_path"})

        assert(storage.retrieve.call_count > 0)

    def test_getStoredSearches_should_call_retrieve_to_get_thumbnail_collection(self):
        storage = BlipTVStorage()
        storage.retrieveValue = Mock()
        storage.retrieveValue.return_value = ["some_search"]
        storage.retrieve = Mock()
        storage.retrieve.return_value = ["some_search"]
        storage.store = Mock()

        storage.getStoredSearches({"path": "some_path"})
        assert(storage.retrieve.call_args[0][0] == {"path": "some_path"})
        assert(storage.retrieve.call_args[0][1] == "thumbnail")
        print repr(storage.retrieve.call_args[0][2])
        assert(storage.retrieve.call_args[0][2] == {'path': 'some_path', 'search': 'some_search', 'thumbnail': ['some_search'], 'Title': 'some_search'})
        assert(storage.retrieve.call_count == 2)

    def test_getStoredSearches_should_return_proper_list_structure(self):
        storage = BlipTVStorage()
        storage.retrieveValue = Mock()
        storage.retrieveValue.return_value = ["some_search"]
        storage.retrieve = Mock()
        storage.retrieve.return_value = ["some_search"]
        storage.store = Mock()

        result = storage.getStoredSearches({"path": "some_path"})

        print repr(result)
        assert(result == [{'path': 'some_path', 'search': 'some_search', 'thumbnail': ['some_search'], 'Title': 'some_search'}])

    def test_getStoredSearches_should_call_quote_plus_on_search_items(self):
        patcher = patch("urllib.quote_plus")
        patcher.start()
        import urllib
        urllib.quote_plus.return_value = "some_quoted_search"
        storage = BlipTVStorage()
        storage.retrieveValue = Mock()
        storage.retrieveValue.return_value = ["some_search"]
        storage.retrieve = Mock()
        storage.retrieve.return_value = ["some_search"]
        storage.store = Mock()
        
        result = storage.getStoredSearches({"path": "some_path"})

        args = urllib.quote_plus.call_args
        patcher.stop()

        assert(args[0][0] == "some_search")
        assert(result == [{'path': 'some_path', 'search': 'some_quoted_search', 'thumbnail': ['some_search'], 'Title': 'some_search'}])

    def test_getStoredSearches_should_fill_item_for_store_search(self):
        patcher = patch("urllib.quote_plus")
        patcher.start()
        import urllib
        urllib.quote_plus.return_value = "some_quoted_search"
        storage = BlipTVStorage()
        storage.retrieveValue = Mock()
        storage.retrieveValue.return_value = ["some_search"]
        storage.retrieve = Mock()
        storage.retrieve.return_value = ["some_search"]
        storage.store = Mock()

        result = storage.getStoredSearches({"path": "some_path", "store": "searches"})

        args = urllib.quote_plus.call_args
        patcher.stop()
        print repr(result)
        assert(args[0][0] == "some_search")
        assert(result == [{'feed': 'search', 'search': 'some_quoted_search', 'Title': 'some_search', 'scraper': 'search', 'path': 'some_path', 'thumbnail': ['some_search'], 'icon': 'search'}])
                
    def test_deleteStoredSearch_should_call_unquote_on_delete_param(self):
        patcher = patch("urllib.unquote_plus")
        patcher.start()
        import urllib
        urllib.unquote_plus.return_value = "some_unquoted_search"
        storage = BlipTVStorage()
        storage.retrieveValue = Mock()
        storage.retrieveValue.return_value = repr(["some_search"])
        storage.retrieve = Mock()
        storage.retrieve.return_value = ["some_search1"]
        storage.store = Mock()
        
        storage.deleteStoredSearch({"delete": "some_search2"})
        args = urllib.unquote_plus.call_args
        patcher.stop()
        
        assert(args[0][0] == "some_search2")

    def test_deleteStoredSearch_should_call_retrieve_to_get_searches(self):
        storage = BlipTVStorage()
        storage.retrieve = Mock()
        storage.retrieve.return_value = ["some_search1", "some_search2"]
        storage.store = Mock()
        
        storage.deleteStoredSearch({"delete": "some_search2"})
        
        storage.retrieve.assert_called_with({"store": "searches", "delete": "some_search2"})
        assert(storage.retrieve.call_count == 1)

    def test_deleteStoredSearch_should_remove_search_from_list_before_calling_store(self):
        storage = BlipTVStorage()
        storage.retrieve = Mock()
        storage.retrieve.return_value = ["some_search", "some_search2"]
        storage.store = Mock()
        
        storage.deleteStoredSearch({"delete": "some_search2"})
        
        storage.store.assert_called_with({"store": "searches", "delete": "some_search2"}, ['some_search'])

    def test_deleteStoredSearch_should_call_executebuiltin(self):
        storage = BlipTVStorage()
        storage.retrieveValue = Mock()
        storage.retrieveValue.return_value = repr(["some_search"])
        storage.store = Mock()
        
        storage.deleteStoredSearch({"delete": "some_search2"})
        
        sys.modules["__main__"].xbmc.executebuiltin.assert_called_with('Container.Refresh')

    def test_saveSearch_should_call_storeValue(self):
        sys.modules["__main__"].settings.getSetting.return_value = "0"
        storage = BlipTVStorage()
        storage.retrieve = Mock()
        storage.store = Mock()
        storage.retrieve.return_value = ["some_search", "some_search2", "some_search3"]
        
        storage.saveSearch({"scraper":"search","search": "some_search2"})
        
        storage.store.assert_called_with({"scraper":"search", "search": "some_search2"}, ['some_search2', 'some_search', 'some_search3'])

    def test_editStoredSearch_should_exit_cleanly_if_search_param_is_missing(self):
        sys.modules["__main__"].settings.getSetting.return_value = "0"
        sys.modules["__main__"].common.getUserInput.return_value = "some_search3"
        storage = BlipTVStorage()
        storage.retrieve = Mock()
        storage.retrieve.return_value = ["some_search2"]
        storage.saveSearch = Mock()
        
        storage.editStoredSearch({})
        
        assert(storage.saveSearch.call_count == 0)
        assert(storage.retrieve.call_count == 0)

    def test_editStoredSearch_should_ask_user_for_new_search_phrase(self):
        sys.modules["__main__"].settings.getSetting.return_value = "0"
        sys.modules["__main__"].language.return_value = "some_title"
        sys.modules["__main__"].common.getUserInput.return_value = "some_search3"
        storage = BlipTVStorage()
        storage.retrieve = Mock()
        storage.retrieve.return_value = ["some_search2"]
        storage.saveSearch = Mock()
        
        storage.editStoredSearch({"search": "some_search1"})
        
        sys.modules["__main__"].common.getUserInput.assert_called_with('some_title', 'some_search1')

    def test_editStoredSearch_should_save_search(self):
        sys.modules["__main__"].settings.getSetting.return_value = "0"
        sys.modules["__main__"].language.return_value = "some_title"
        sys.modules["__main__"].common.getUserInput.return_value = "some_search3"
        storage = BlipTVStorage()
        storage.retrieve = Mock()
        storage.retrieve.return_value = ["some_search2"]
        storage.saveSearch = Mock()
        
        storage.editStoredSearch({"search": "some_search1", "action": "edit_search"})
        
        sys.modules["__main__"].common.getUserInput.assert_called_with('some_title', 'some_search1')
        storage.saveSearch.assert_called_with({'search': 'some_search3', 'feed': 'search'})

    def test_getStorageKey_should_call_getValueStorageKey_if_type_is_value(self):
        storage = BlipTVStorage()
        storage._getValueStorageKey = Mock()
        
        result = storage.getStorageKey({"some_param": "param_value"},"value")
        
        storage._getValueStorageKey.assert_called_with({"some_param": "param_value"},{})

    def test_getStorageKey_should_call_getThumbnailStorageKey_if_type_is_thumbnail(self):
        storage = BlipTVStorage()
        storage._getThumbnailStorageKey = Mock()
        
        result = storage.getStorageKey({"some_param": "param_value"}, "thumbnail")
        
        storage._getThumbnailStorageKey.assert_called_with({"some_param": "param_value"},{})        
        
    def test_getStorageKey_should_call_getResultSetStorageKey_if_type_is_not_set(self):
        storage = BlipTVStorage()
        storage._getResultSetStorageKey = Mock()
        
        result = storage.getStorageKey({"some_param": "param_value"})
        
        storage._getResultSetStorageKey.assert_called_with({"some_param": "param_value"})
        
    def test_getThumbnailStorageKey_should_return_correct_key_for_search_path(self):
        storage = BlipTVStorage()
        
        result = storage._getThumbnailStorageKey({"search": "some_search","feed": "search"})
        
        assert(result == "search_some_search_thumb")

    def test_getThumbnailStorageKey_should_return_correct_key_for_search_item(self):
        storage = BlipTVStorage()
        
        result = storage._getThumbnailStorageKey({"some_param": "something"}, {"search": "some_search", "feed": "search"})
        
        assert(result == "search_some_search_thumb")
    
    def test_getThumbnailStorageKey_should_appen_thumb_to_key(self):
        storage = BlipTVStorage()
        
        result = storage._getThumbnailStorageKey({"some_param": "something"}, {"search": "some_search"})
    
        assert(result[result.rfind("_"):] == "_thumb")
        
    def test_getValueStorageKey_should_handle_reverse_order(self):
        storage = BlipTVStorage()
        
        result = storage._getValueStorageKey({"action": "reverse_order"}, {"playlist": "some_playlist"})
        print repr(result)
        assert(result == "reverse_playlist_some_playlist")

    def test_getValueStorageKey_should_handle_reverse_order_external_contact(self):
        storage = BlipTVStorage()
        
        result = storage._getValueStorageKey({"action": "reverse_order", "external": "true", "contact": "some_contact"}, {"playlist": "some_playlist"})
        print repr(result)
        assert(result == "reverse_playlist_some_playlist_external_some_contact")

    def test_getResultSetStorageKey_should_return_correct_key_for_category_path(self):
        storage = BlipTVStorage()
        
        result = storage._getResultSetStorageKey({"scraper": "categories", "category": "some_category"})
        
        assert(result == "s_categories_some_category")

    def test_getResultSetStorageKey_should_return_correct_key_for_for_show_scraper(self):
        storage = BlipTVStorage()
        
        result = storage._getResultSetStorageKey({"scraper": "show", "show": "some_show"})
        
        assert(result == "s_show_some_show")

    def test_getResultSetStorageKey_should_return_correct_key_for_generic_stores(self):
        storage = BlipTVStorage()
        
        result = storage._getResultSetStorageKey({"store": "pokeystore"})
        
        assert(result == "store_pokeystore")

    def test_store_should_call_getStorageKey_to_fetch_correct_storage_key(self):
        storage = BlipTVStorage()
        storage.getStorageKey = Mock()
        
        result = storage.store({"store": "pokeystore"})
        
        storage.getStorageKey.assert_called_with({'store': 'pokeystore'}, '', {})

    def test_store_should_call_storeValue_if_type_is_set(self):
        storage = BlipTVStorage()
        storage.storeValue = Mock()
        storage.getStorageKey = Mock()
        storage.getStorageKey.return_value = "key"
        
        result = storage.store({}, {"store": "pokeystore"},  "value")
        
        storage.storeValue.assert_called_with("key", {"store": "pokeystore"})
    
    def test_store_should_call_storeResultSet_if_type_is_not_set(self):
        storage = BlipTVStorage()
        storage.storeResultSet = Mock()
        storage.getStorageKey = Mock()
        storage.getStorageKey.return_value = "key"
        
        storage.store({}, {"store": "pokeystore"})
        
        storage.storeResultSet.assert_called_with("key", {"store": "pokeystore"})
        
    def test_storeValue_should_call_setsetting_with_correct_params(self):
        storage = BlipTVStorage()
        storage.storeResultSet = Mock()
        storage.getStorageKey = Mock()
        storage.getStorageKey.return_value = "key"
        
        storage.storeValue("some_key", "some_value")
        
        sys.modules["__main__"].settings.setSetting.assert_called_with("some_key","some_value")

    def test_storeResultSet_should_call_setsetting_with_correct_params_by_default(self):
        storage = BlipTVStorage()
        
        storage.storeResultSet("some_key", ["some_value"])
        
        sys.modules["__main__"].settings.setSetting.assert_called_with("some_key",repr(["some_value"]))
    
    def test_storeResultSet_should_call_retrieveResultSet_if_prepend_is_in_params(self):
        sys.modules["__main__"].settings.getSetting.return_value = "0"
        storage = BlipTVStorage()
        storage.retrieveResultSet = Mock()
        storage.retrieveResultSet.return_value = []
        
        storage.storeResultSet("some_key", ["some_value"], {"prepend": "true"})
        
        storage.retrieveResultSet.assert_called_with("some_key")

    def test_storeResultSet_should_call_settings_getSetting_to_get_stored_searches_limit_if_prepend_is_params(self):
        sys.modules["__main__"].settings.getSetting.return_value = "0"
        storage = BlipTVStorage()
        storage.retrieveResultSet = Mock()
        storage.retrieveResultSet.return_value = []
        
        storage.storeResultSet("some_key", ["some_value"], {"prepend": "true"})
        
        sys.modules["__main__"].settings.getSetting.assert_called_with("saved_searches")
        
    def test_storeResultSet_should_call_retrieveResultSet_if_append_is_in_params(self):
        sys.modules["__main__"].settings.getSetting.return_value = "0"
        storage = BlipTVStorage()
        storage.retrieveResultSet = Mock()
        storage.retrieveResultSet.return_value = []
        
        storage.storeResultSet("some_key", ["some_value"], {"append": "true"})
        
        storage.retrieveResultSet.assert_called_with("some_key")
                
    def test_storeResultSet_should_call_setsetting_if_prepend_is_in_params(self):
        sys.modules["__main__"].settings.getSetting.return_value = "0"
        storage = BlipTVStorage()
        storage.retrieveResultSet = Mock()
        storage.retrieveResultSet.return_value = []
        
        storage.storeResultSet("some_key", ["some_value"], {"prepend": "true"})
        
        sys.modules["__main__"].settings.setSetting.assert_called_with("some_key",repr(["some_value"]))
        
    def test_storeResultSet_should_call_setsetting_correctly_if_append_is_in_params(self):
        sys.modules["__main__"].settings.getSetting.return_value = "0"
        storage = BlipTVStorage()
        storage.retrieveResultSet = Mock()
        storage.retrieveResultSet.return_value = ["smokey"]
        
        storage.storeResultSet("some_key", ["some_value"], {"append": "true"})
        
        sys.modules["__main__"].settings.setSetting.assert_called_with("some_key",repr(["smokey","some_value"]))
        
    def test_storeResultSet_should_append_item_to_collection_if_append_is_in_params(self):
        sys.modules["__main__"].settings.getSetting.return_value = "0"
        storage = BlipTVStorage()
        storage.retrieveResultSet = Mock()
        storage.retrieveResultSet.return_value = ["smokey"]
        
        storage.storeResultSet("some_key", ["some_value"], {"append": "true"})
        
        sys.modules["__main__"].settings.setSetting.assert_called_with("some_key",repr(["smokey","some_value"]))
        
    def test_storeResultSet_should_prepend_item_to_collection_if_prepend_is_in_params(self):
        sys.modules["__main__"].settings.getSetting.return_value = "0"
        storage = BlipTVStorage()
        storage.retrieveResultSet = Mock()
        storage.retrieveResultSet.return_value = ["some_default"]
        
        storage.storeResultSet("some_key", ["some_value"], {"prepend": "true"})
        
        sys.modules["__main__"].settings.setSetting.assert_called_with("some_key",repr(["some_value","some_default"]))
        
    def test_retrieve_should_call_getStorageKey_to_fetch_correct_storage_key(self):
        sys.modules["__main__"].settings.getSetting.return_value = "0"
        storage = BlipTVStorage()
        storage.getStorageKey = Mock()
        storage.getStorageKey.return_value = "some_key"
        
        storage.retrieve("some_key", "some_value", {"prepend": "true"})
        
        storage.getStorageKey.assert_called_with("some_key", "some_value", {"prepend": "true"})

    def test_retrieve_should_call_retrieveValue_if_type_is_set(self):
        sys.modules["__main__"].settings.getSetting.return_value = "0"
        storage = BlipTVStorage()
        storage.getStorageKey = Mock()
        storage.getStorageKey.return_value = "some_key"
        storage.retrieveValue = Mock()
        
        storage.retrieve("some_key", "thumbnail")
        
        storage.retrieveValue.assert_called_with("some_key")
    
    def test_retrieve_should_call_retrieveResultSet_if_type_is_not_set(self):
        sys.modules["__main__"].settings.getSetting.return_value = "0"
        storage = BlipTVStorage()
        storage.getStorageKey = Mock()
        storage.getStorageKey.return_value = "some_key"
        storage.retrieveResultSet = Mock()
        
        storage.retrieve("some_key")
        
        storage.retrieveResultSet.assert_called_with("some_key")
    
    def test_retrieveValue_should_call_getsetting_with_correct_params(self):
        storage = BlipTVStorage()
        
        storage.retrieveValue("some_key")
        
        sys.modules["__main__"].settings.getSetting.assert_called_with("some_key")
        
    def test_retrieveResultSet_should_call_getsetting_with_correct_params(self):
        storage = BlipTVStorage()
        
        storage.retrieveResultSet("some_key")
        
        sys.modules["__main__"].settings.getSetting.assert_called_with("some_key")

    def test_retrieveResultSet_should_evaluate_content_from_sql_get(self):
        storage = BlipTVStorage()
        sys.modules["__main__"].settings.getSetting.return_value = "['some_value']"
        
        result = storage.retrieveResultSet("some_key")
        
        assert(result == ['some_value']) 

    def test_addToMyFavoritesShow_should_work(self):
        storage = BlipTVStorage()
        storage.retrieve = Mock()
        storage.retrieve.return_value = [ {'item': 'mock', 'Title': 'Second'} ] 
        storage.store = Mock()
        
        storage.addToMyFavoritesShow({}, { "Title": "First", "item": "mock" })

        storage.retrieve.assert_called_with({})
        storage.store.assert_called_with({}, [{'item': 'mock', 'Title': 'First'}, {'item': 'mock', 'Title': 'Second'}])

    def test_deleteFromMyFavoriteShows_should_work(self):
        storage = BlipTVStorage()
        storage.retrieve = Mock()
        storage.retrieve.return_value = [ { 'show': 'show_name', 'item': 'mock', 'Title': 'First'}, { 'show': 'other_name', 'item': 'mock', 'Title': 'Second'} ] 
        storage.store = Mock()
        sys.modules["__main__"].cache.get.return_value = "['some_id']"
        
        storage.deleteFromMyFavoriteShows({ "show": "show_name"} )

        storage.retrieve.assert_called_with({'store': 'favorites', 'show': 'show_name'})
        storage.store.assert_called_with({'store': 'favorites', 'show': 'show_name'}, [{'item': 'mock', 'Title': 'Second', 'show': 'other_name'}])
    
if __name__ == '__main__':
    nose.runmodule()
