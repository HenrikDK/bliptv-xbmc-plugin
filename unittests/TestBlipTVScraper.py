# -*- coding: utf-8 -*-
import nose
import BaseTestCase
from mock import Mock
import sys
from  BlipTVScraper import BlipTVScraper


class TestBlipTVUtils(BaseTestCase.BaseTestCase):
    scraper = ""

    def setUp(self):
        super(self.__class__, self).setUp()
        sys.modules["__main__"].common.parseDOM.return_value = ["some_string", "some_string", "some_string"]
        sys.modules["__main__"].common.fetchPage.return_value = {"content": "some_content", "status": 200}
        sys.modules["__main__"].common.makeAscii.return_value = "some_ascii_string"
        sys.modules["__main__"].common.replaceHTMLCodes.return_value = "some_html_free_string"
        sys.modules["__main__"].language.return_value = "some_language_string %s"
        sys.modules["__main__"].common.stripTags.return_value = "some_tag_less_string"
        sys.modules["__main__"].settings.getSetting.return_value = "1"
        sys.modules["__main__"].cache.cacheFunction.return_value = ["some_cached_string"]

        self.scraper = BlipTVScraper()
        self.scraper.createUrl = Mock()
        self.scraper.scrapeChannelId = Mock()
        self.scraper.scrapeUserId = Mock()
        self.scraper.createUrl.return_value = "some_url"

    def test_searchShow_should_call_createUrl_to_get_proper_url(self):
        sys.modules["__main__"].common.parseDOM.side_effect = ["", "some_string", "some_string"]

        self.scraper.searchShow()

        self.scraper.createUrl.assert_any_call({'page': '1'}, 1)

    def test_searchShow_should_call_fetchPage_to_get_html_contents(self):
        sys.modules["__main__"].common.parseDOM.side_effect = ["", "some_string", "some_string"]

        self.scraper.searchShow()

        sys.modules["__main__"].common.fetchPage.assert_any_call({"link": "some_url"})

    def test_searchShow_should_use_parseDOM_to_scrape_page(self):
        self.scraper.extractAndResizeThumbnail = Mock()
        sys.modules["__main__"].common.parseDOM.side_effect = [["some_string"], "some_string", "some_string", ""]
        self.scraper.searchShow()

        assert(sys.modules["__main__"].common.parseDOM.call_count > 2)

    def test_searchShow_should_call_utils_replaceHTMLCodes_to_remove_html_char_codes_from_strings(self):
        self.scraper.extractAndResizeThumbnail = Mock()
        sys.modules["__main__"].common.parseDOM.side_effect = [["some_string"], "some_string", "some_string", ""]

        self.scraper.searchShow()

        assert(sys.modules["__main__"].common.replaceHTMLCodes.call_count > 0)

    def test_searchEpisodes_should_call_createUrl_to_get_proper_url(self):
        sys.modules["__main__"].common.parseDOM.side_effect = ["", "some_string", "some_string"]

        self.scraper.searchEpisodes()

        self.scraper.createUrl.assert_any_call({}, 1)

    def test_searchEpisodes_should_call_fetchPage_to_get_html_contents(self):
        sys.modules["__main__"].common.parseDOM.side_effect = ["", "some_string", "some_string"]

        self.scraper.searchEpisodes()

        sys.modules["__main__"].common.fetchPage.assert_any_call({"link": "some_url"})

    def test_searchEpisodes_should_use_parseDOM_to_scrape_page(self):
        sys.modules["__main__"].common.parseDOM.side_effect = [["some_string"], "some_string", ["some_string - some_id"], "some_string", "", "", "", "", ""]

        self.scraper.searchEpisodes()

        assert(sys.modules["__main__"].common.parseDOM.call_count > 2)

    def test_searchEpisodes_should_call_utils_replaceHTMLCodes_to_remove_html_char_codes_from_strings(self):
        sys.modules["__main__"].common.parseDOM.side_effect = [["some_string"], "some_string",["some_string - some_id"], "some_string", "", "", "", "", ""]
        
        self.scraper.searchEpisodes()
        
        assert(sys.modules["__main__"].common.replaceHTMLCodes.call_count > 0)

    def test_scrapeCategories_should_call_createUrl_to_get_proper_url(self):
        sys.modules["__main__"].common.parseDOM.side_effect = ["", "",["some_string"],["some_string"]]
        
        self.scraper.scrapeCategories()
        
        self.scraper.createUrl.assert_any_call({})
        
    def test_scrapeCategories_should_call_fetchPage_to_get_html_contents(self):
        sys.modules["__main__"].common.parseDOM.side_effect = ["", "",["some_string"],["some_string"]]
        
        self.scraper.scrapeCategories()
        
        sys.modules["__main__"].common.fetchPage.assert_any_call({"link": "some_url"})
        
    def test_scrapeCategories_should_use_parseDOM_to_scrape_page(self):
        sys.modules["__main__"].common.parseDOM.side_effect = ["", "",["some_string"],["some_string"]]
        
        self.scraper.scrapeCategories()
        
        assert(sys.modules["__main__"].common.parseDOM.call_count > 2)
            
    def test_scrapeCategories_should_call_utils_replaceHTMLCodes_to_remove_html_char_codes_from_strings(self):
        sys.modules["__main__"].common.parseDOM.side_effect = ["", "",["some_string"],["some_string"]]
        
        self.scraper.scrapeCategories()
        
        assert(sys.modules["__main__"].common.replaceHTMLCodes.call_count > 0)
    
    def test_scrapeCategoryVideos_should_call_createUrl_to_get_proper_url(self):
        sys.modules["__main__"].common.parseDOM.side_effect = ["", "",["some_string"],["some_string"]]
        
        self.scraper.scrapeCategoryVideos({"category": "some_category"})
        
        self.scraper.createUrl.assert_any_call({"category": "some_category"}, 1)
    
    def test_scrapeCategoryVideos_should_call_scrapeChannelId_to_get_channel_id(self):
        sys.modules["__main__"].common.parseDOM.side_effect = ["", "",["some_string"],["some_string"]]
        
        self.scraper.scrapeCategoryVideos({"category": "some_category"})
        
        self.scraper.scrapeChannelId.assert_any_call({"category": "some_category"})

    def test_scrapeCategoryVideos_should_call_fetchPage_to_get_html_contents(self):
        sys.modules["__main__"].common.parseDOM.side_effect = ["", "",["some_string"],["some_string"]]
        
        self.scraper.scrapeCategoryVideos()
        
        sys.modules["__main__"].common.fetchPage.assert_any_call({"link": "some_url"})
    
    def test_scrapeCategoryVideos_should_use_parseDOM_to_scrape_page(self):
        sys.modules["__main__"].common.parseDOM.side_effect = [["some_string"], "",["some_string - some_id"],["some_string"],["some_string"], ""]
        
        self.scraper.scrapeCategoryVideos({"category": "some_category"})
        
        assert(sys.modules["__main__"].common.parseDOM.call_count > 2)
    
    def test_scrapeCategoryVideos_should_delete_channel_id_when_done_if_present(self):
        sys.modules["__main__"].common.parseDOM.side_effect = [["some_string"], "",["some_string - some_id"],["some_string"],["some_string"], ""]
        params = {"category": "some_category", "channel_id": "some_chanel"}
        
        self.scraper.scrapeCategoryVideos(params)
        
        assert(params.has_key("channel_id") == False)

    def test_scrapeCategoryVideos_should_call_utils_replaceHTMLCodes_to_remove_html_char_codes_from_strings(self):
        sys.modules["__main__"].common.parseDOM.side_effect = [["some_string"], "",["some_string - some_id"],["some_string"],["some_string"], ""]
        
        self.scraper.scrapeCategoryVideos({"category": "some_category"})
        
        assert(sys.modules["__main__"].common.replaceHTMLCodes.call_count > 0)
    
    def test_scrapeCategoryFeaturedShows_should_call_createUrl_to_get_proper_url(self):
        sys.modules["__main__"].common.parseDOM.side_effect = ["", "some_string", "some_string"]
        
        self.scraper.scrapeCategoryFeaturedShows()
        
        self.scraper.createUrl.assert_any_call({}, 1)
        
    def test_scrapeCategoryFeaturedShows_should_call_fetchPage_to_get_html_contents(self):
        sys.modules["__main__"].common.parseDOM.side_effect = ["", "some_string", "some_string"]
        
        self.scraper.scrapeCategoryFeaturedShows()
        
        sys.modules["__main__"].common.fetchPage.assert_any_call({"link": "some_url"})
        
    def test_scrapeCategoryFeaturedShows_should_use_parseDOM_to_scrape_page(self):
        self.scraper.extractAndResizeThumbnail = Mock()
        sys.modules["__main__"].common.parseDOM.side_effect = [["some_string"], ["some_string"], ["some_string"], []]

        self.scraper.scrapeCategoryFeaturedShows()
        
        assert(sys.modules["__main__"].common.parseDOM.call_count > 2)
            
    def test_scrapeCategoryFeaturedShows_should_call_utils_replaceHTMLCodes_to_remove_html_char_codes_from_strings(self):
        self.scraper.extractAndResizeThumbnail = Mock()
        sys.modules["__main__"].common.parseDOM.side_effect = [["some_string"], ["some_string"], ["some_string"], []]
        
        self.scraper.scrapeCategoryFeaturedShows()
        
        assert(sys.modules["__main__"].common.replaceHTMLCodes.call_count > 0)
    
    def test_scrapeCategoryFeaturedShows_should_delete_channel_id_when_done_if_present(self):
        self.scraper.extractAndResizeThumbnail = Mock()
        sys.modules["__main__"].common.parseDOM.side_effect = [["some_string"], ["some_string"], ["some_string"], []]
        params = {"category": "some_category", "channel_id": "some_chanel"}
        
        self.scraper.scrapeCategoryFeaturedShows(params)
        
        assert(params.has_key("channel_id") == False)
    
    def test_scrapeChannelId_should_call_createUrl_to_get_proper_url(self):
        sys.modules["__main__"].common.parseDOM.side_effect = ["", "some_string", "some_string"]
        scraper = BlipTVScraper()
        scraper.createUrl = Mock()
        
        scraper.scrapeChannelId()
        
        scraper.createUrl.assert_any_call({})
        
    def test_scrapeChannelId_should_fetchPage_to_get_html_contents(self):
        sys.modules["__main__"].common.parseDOM.side_effect = ["", "some_string", "some_string"]
        scraper = BlipTVScraper()
        scraper.createUrl = Mock()
        scraper.createUrl.return_value = "some_url"
        
        scraper.scrapeChannelId()
                
        sys.modules["__main__"].common.fetchPage.assert_any_call({"link": "some_url"})
        
    def test_scrapeChannelId_should_use_parseDOM_to_scrape_page(self):
        sys.modules["__main__"].common.parseDOM.side_effect = [["some_string"], "some_string", "some_string", "some_string", "some_string", ""]        
        scraper = BlipTVScraper()
        scraper.createUrl = Mock()
        
        scraper.scrapeChannelId({"category": "somecategory"})
                
        assert(sys.modules["__main__"].common.parseDOM.call_count > 0)

    def test_scrapeChannelId_should_remove_category_when_done(self):
        sys.modules["__main__"].common.parseDOM.side_effect = [["some_string"], "some_string", "some_string", "some_string", "some_string", ""]        
        scraper = BlipTVScraper()
        scraper.createUrl = Mock()
        params = {"category": "somecategory"}
        
        scraper.scrapeChannelId(params)
                
        assert(params.has_key("category") == False)

    def test_scrapeChannelId_should_set_channel_id_when_done(self):
        sys.modules["__main__"].common.parseDOM.side_effect = [["some_string"], "some_string", "some_string", "some_string", "some_string", ""]        
        scraper = BlipTVScraper()
        scraper.createUrl = Mock()
        params = {"category": "somecategory"}
        
        scraper.scrapeChannelId(params)
                
        assert(params.has_key("channel_id") == True)

    def test_scrapeCategoryShows_should_call_createUrl_to_get_proper_url(self):
        sys.modules["__main__"].common.parseDOM.side_effect = ["", "some_string", "some_string"]
        
        self.scraper.scrapeCategoryShows()
        
        self.scraper.createUrl.assert_any_call({}, 1)
        
    def test_scrapeCategoryShows_should_call_fetchPage_to_get_html_contents(self):
        sys.modules["__main__"].common.parseDOM.side_effect = ["", "some_string", "some_string"]
        
        self.scraper.scrapeCategoryShows()
        
        sys.modules["__main__"].common.fetchPage.assert_any_call({"link": "some_url"})
        
    def test_scrapeCategoryShows_should_use_parseDOM_to_scrape_page(self):
        sys.modules["__main__"].common.parseDOM.side_effect = [["some_string"], "some_string", "some_string", "some_string", "some_string", ""]
        
        self.scraper.scrapeCategoryShows()
        
        assert(sys.modules["__main__"].common.parseDOM.call_count > 2)
            
    def test_scrapeCategoryShows_should_call_utils_replaceHTMLCodes_to_remove_html_char_codes_from_strings(self):
        sys.modules["__main__"].common.parseDOM.side_effect = [["some_string"], "some_string", "some_string", "some_string", "some_string", ""]
        
        self.scraper.scrapeCategoryShows()
        
        assert(sys.modules["__main__"].common.replaceHTMLCodes.call_count > 0)

    def test_scrapeCategoryShows_should_should_delete_channel_id_when_done_if_present(self):
        sys.modules["__main__"].common.parseDOM.side_effect = [["some_string"], "some_string", "some_string", "some_string", "some_string", ""]
        params = {"category": "some_category", "channel_id": "some_chanel"}
        
        self.scraper.scrapeCategoryShows(params)
        
        assert(params.has_key("channel_id") == False)

    def test_scrapeUserId_should_call_createUrl_to_get_proper_url(self):
        sys.modules["__main__"].common.parseDOM.side_effect = ["", "some_string", "some_string"]
        scraper = BlipTVScraper()
        scraper.createUrl = Mock()
        
        scraper.scrapeUserId()
        
        scraper.createUrl.assert_any_call({})
        
    def test_scrapeUserId_should_fetchPage_to_get_html_contents(self):
        sys.modules["__main__"].common.parseDOM.side_effect = ["", "some_string", "some_string"]
        scraper = BlipTVScraper()
        scraper.createUrl = Mock()
        scraper.createUrl.return_value = "some_url"
        
        scraper.scrapeUserId()
                
        sys.modules["__main__"].common.fetchPage.assert_any_call({"link": "some_url"})
        
    def test_scrapeUserId_should_use_parseDOM_to_scrape_page(self):
        sys.modules["__main__"].common.parseDOM.side_effect = [["some_string"], "some_string", "some_string", "some_string", "some_string", ""]        
        scraper = BlipTVScraper()
        scraper.createUrl = Mock()
        
        scraper.scrapeUserId()
                
        assert(sys.modules["__main__"].common.parseDOM.call_count > 0)

    def test_scrapeUserId_should_set_channel_id_when_done(self):
        sys.modules["__main__"].common.parseDOM.side_effect = [["some_string"], "some_string", "some_string", "some_string", "some_string", ""]        
        scraper = BlipTVScraper()
        scraper.createUrl = Mock()
        params = {}
        
        scraper.scrapeUserId(params)
                
        assert(params.has_key("user_id") == True)

    def test_addShowToMyFavorites_should_call_createUrl_to_get_proper_url(self):
        sys.modules["__main__"].common.parseDOM.side_effect = ["", "some_string", "some_string", "some_string"]
        
        self.scraper.addShowToMyFavorites()
        
        self.scraper.createUrl.assert_any_call({"scraper": "show"})
        
    def test_addShowToMyFavorites_should_call_fetchPage_to_get_html_contents(self):
        sys.modules["__main__"].common.parseDOM.side_effect = ["", "some_string", "some_string", "some_string"]
        
        self.scraper.addShowToMyFavorites()
        
        sys.modules["__main__"].common.fetchPage.assert_any_call({"link": "some_url"})
        
    def test_addShowToMyFavorites_should_use_parseDOM_to_scrape_page(self):
        sys.modules["__main__"].common.parseDOM.side_effect = [["some_string"], "some_string", "some_string", "some_string", "some_string", ""]
        
        self.scraper.addShowToMyFavorites()
        
        assert(sys.modules["__main__"].common.parseDOM.call_count > 2)
            
    def test_addShowToMyFavorites_should_call_utils_replaceHTMLCodes_to_remove_html_char_codes_from_strings(self):
        sys.modules["__main__"].common.parseDOM.side_effect = [["some_string"], "some_string", "some_string", "some_string", "some_string", ""]
        
        self.scraper.addShowToMyFavorites()
        
        assert(sys.modules["__main__"].common.replaceHTMLCodes.call_count > 0)

    def test_addShowToMyFavorites_should_should_call_storage_addToMyFavoritesShow(self):
        sys.modules["__main__"].common.parseDOM.side_effect = [["some_string"], "some_string", "some_string", "some_string", "some_string", ""]
        params = { "show": "some_show", "user_id": "some_user"}
        
        self.scraper.addShowToMyFavorites(params)
        
        sys.modules["__main__"].storage.addToMyFavoritesShow.assert_any_call({'user_id': 'some_user', 'scraper': 'show', 'show': 'some_show'}, {'scraper': 'show', 'show': 'some_show', 'thumbnail': 's', 'Title': 'some_html_free_string'})

    def test_scrapeShowVideos_should_call_createUrl_to_get_proper_url(self):
        sys.modules["__main__"].common.parseDOM.side_effect = [["some_string"],["some_string"],["some_string"], "some_string", "some_string", "some_string", "", "", ""]

        self.scraper.scrapeUserId = Mock()
        self.scraper.scrapeShowVideos({"user_id":"123"})

        self.scraper.createUrl.assert_any_call({}, 1)
        
    def test_scrapeShowVideos_should_call_fetchPage_to_get_html_contents(self):
        sys.modules["__main__"].common.parseDOM.side_effect = [["some_string"],["some_string"],["some_string"], "some_string", "some_string", "some_string", "", "", ""]

        self.scraper.scrapeUserId = Mock()
        self.scraper.scrapeShowVideos({"user_id":"123"})

        sys.modules["__main__"].common.fetchPage.assert_any_call({"link": "some_url"})
        
    def test_scrapeShowVideos_should_use_parseDOM_to_scrape_page(self):
        sys.modules["__main__"].common.parseDOM.side_effect = [["some_string"],["some_string"],["some_string"], "some_string", "some_string", "some_string", "", "", ""]

        self.scraper.scrapeUserId = Mock()
        self.scraper.scrapeShowVideos({"user_id":"123"})
        
        assert(sys.modules["__main__"].common.parseDOM.call_count > 2)
            
    def test_scrapeShowVideos_should_call_utils_replaceHTMLCodes_to_remove_html_char_codes_from_strings(self):
        sys.modules["__main__"].common.parseDOM.side_effect = [["some_string"],["some_string"],["some_string"], "some_string", "some_string", "some_string", "", "", ""]

        self.scraper.scrapeUserId = Mock()
        self.scraper.scrapeShowVideos({"user_id":"123"})

        assert(sys.modules["__main__"].common.replaceHTMLCodes.call_count > 0)

    def test_scrapeShowVideos_should_should_delete_user_id_when_done_if_present(self):
        sys.modules["__main__"].common.parseDOM.side_effect = [["some_string"],["some_string"],["some_string"], "some_string", "some_string", "some_string", "", "", ""]
        params = {"category": "some_category", "user_id": "some_user"}
        
        self.scraper.scrapeShowVideos(params)
        
        assert(params.has_key("user_id") == False)

    def test_scrapeShowsHomepageFeed_should_call_createUrl_to_get_proper_url(self):
        sys.modules["__main__"].common.parseDOM.side_effect = [["some_string"],["some_string"],["some_string"], "some_string", "some_string", "", "", "", ""]
        
        self.scraper.scrapeShowsHomepageFeed()
        
        self.scraper.createUrl.assert_any_call({}, 1)
        
    def test_scrapeShowsHomepageFeed_should_call_fetchPage_to_get_html_contents(self):
        sys.modules["__main__"].common.parseDOM.side_effect = [["some_string"],["some_string"],["some_string"], "some_string", "some_string", "", "", "", ""]
        
        self.scraper.scrapeShowsHomepageFeed()
        
        sys.modules["__main__"].common.fetchPage.assert_any_call({"link": "some_url"})
        
    def test_scrapeShowsHomepageFeed_should_use_parseDOM_to_scrape_page(self):
        sys.modules["__main__"].common.parseDOM.side_effect = [["some_string"],["some_string"],["some_string"], "some_string", "some_string", "", "", "", ""]
        
        self.scraper.scrapeShowsHomepageFeed()
        
        assert(sys.modules["__main__"].common.parseDOM.call_count > 2)
            
    def test_scrapeShowsHomepageFeed_should_call_utils_replaceHTMLCodes_to_remove_html_char_codes_from_strings(self):
        sys.modules["__main__"].common.parseDOM.side_effect = [["some_string"],["some_string"],["some_string"], "some_string", "some_string", "", "", "", ""]
        
        self.scraper.scrapeShowsHomepageFeed()
        
        assert(sys.modules["__main__"].common.replaceHTMLCodes.call_count > 0)
        
    def test_scrape_should_call_getNewResultsFunction(self):
        scraper = BlipTVScraper()
        scraper.getNewResultsFunction = Mock()
        scraper.paginator = Mock()
        
        scraper.scrape({})
        
        scraper.getNewResultsFunction.assert_any_call({})        
        
    def test_scrape_should_call_paginator(self):
        scraper = BlipTVScraper()
        scraper.getNewResultsFunction = Mock()
        scraper.paginator = Mock()
        
        scraper.scrape({})
        
        scraper.paginator.assert_any_call({})

    def test_getNewResultsFunction_should_set_proper_params_for_scrapeCategories_if_scraper_is_browse_shows(self):
        params = {"scraper": "browse_shows"}
        
        self.scraper.getNewResultsFunction(params)
        
        assert(params["folder"] == "true")
        assert(params["new_results_function"] == self.scraper.scrapeCategories)

    def test_getNewResultsFunction_should_set_proper_params_for_scrapeCategories_if_scraper_is_staff_picks(self):
        params = {"scraper": "staff_picks"}
        
        self.scraper.getNewResultsFunction(params)
        
        assert(params["folder"] == "true")
        assert(params["new_results_function"] == self.scraper.scrapeCategories)

    def test_getNewResultsFunction_should_set_proper_params_for_scrapeCategories_if_scraper_is_favorites(self):
        params = {"scraper": "favorites"}
        
        self.scraper.getNewResultsFunction(params)
        
        assert(params["folder"] == "true")
        assert(params["new_results_function"] == self.scraper.scrapeCategories)

    def test_getNewResultsFunction_should_set_proper_params_for_scrapeCategories_if_scraper_is_new_episodes(self):
        params = {"scraper": "new_episodes"}
        
        self.scraper.getNewResultsFunction(params)
        
        assert(params["folder"] == "true")
        assert(params["new_results_function"] == self.scraper.scrapeCategories)

    def test_getNewResultsFunction_should_set_proper_params_for_scrapeCategories_if_scraper_is_popular_episodes(self):
        params = {"scraper": "popular_episodes"}
        
        self.scraper.getNewResultsFunction(params)
        
        assert(params["folder"] == "true")
        assert(params["new_results_function"] == self.scraper.scrapeCategories)

    def test_getNewResultsFunction_should_set_proper_params_for_scrapeCategories_if_scraper_is_trending_episodes(self):
        params = {"scraper": "trending_episodes"}
        
        self.scraper.getNewResultsFunction(params)
        
        assert(params["folder"] == "true")
        assert(params["new_results_function"] == self.scraper.scrapeCategories)

    def test_getNewResultsFunction_should_set_proper_params_for_scrapeCategories_if_scraper_is_browse_shows_and_category(self):
        params = {"scraper": "browse_shows", "category": "some_category"}
        
        self.scraper.getNewResultsFunction(params)
        
        assert(params["folder"] == "true")
        assert(params["new_results_function"] == self.scraper.scrapeCategoryShows)

    def test_getNewResultsFunction_should_set_proper_params_for_scrapeCategories_if_scraper_is_staff_picks_and_category(self):
        params = {"scraper": "staff_picks", "category": "some_category"}
        
        self.scraper.getNewResultsFunction(params)
        
        assert(params["folder"] == "true")
        assert(params["new_results_function"] == self.scraper.scrapeCategoryFeaturedShows)

    def test_getNewResultsFunction_should_set_proper_params_for_scrapeCategories_if_scraper_is_favorites_and_category(self):
        params = {"scraper": "favorites", "category": "some_category"}
        
        self.scraper.getNewResultsFunction(params)
        
        assert(params["folder"] == "true")
        assert(params["new_results_function"] == self.scraper.scrapeCategoryFeaturedShows)

    def test_getNewResultsFunction_should_set_proper_params_for_scrapeCategories_if_scraper_is_new_episodes_and_category(self):
        params = {"scraper": "new_episodes", "category": "some_category"}
        
        self.scraper.getNewResultsFunction(params)
        
        assert(params["new_results_function"] == self.scraper.scrapeCategoryVideos)

    def test_getNewResultsFunction_should_set_proper_params_for_scrapeCategories_if_scraper_is_popular_episodes_and_category(self):
        params = {"scraper": "popular_episodes", "category": "some_category"}
        
        self.scraper.getNewResultsFunction(params)
        
        assert(params["new_results_function"] == self.scraper.scrapeCategoryVideos)
        
    def test_getNewResultsFunction_should_set_proper_params_for_scrapeCategories_if_scraper_is_trending_episodes_and_category(self):
        params = {"scraper": "trending_episodes", "category": "some_category"}
        
        self.scraper.getNewResultsFunction(params)
        
        assert(params["new_results_function"] == self.scraper.scrapeCategoryVideos)
    
    def test_getNewResultsFunction_should_set_proper_params_for_searchEpisodes_if_scraper_is_search(self):
        params = {"scraper": "search"}
        
        self.scraper.getNewResultsFunction(params)
        
        assert(params["new_results_function"] == self.scraper.searchEpisodes)
        
    def test_getNewResultsFunction_should_set_proper_params_for_searchShow_if_scraper_is_show_search(self):
        params = {"scraper": "show_search"}
        
        self.scraper.getNewResultsFunction(params)
        
        assert(params["folder"] == "true")
        assert(params["new_results_function"] == self.scraper.searchShow)
        
    def test_getNewResultsFunction_should_set_proper_params_for_scrapeShowVideos_if_scraper_is_show(self):
        params = {"scraper": "show"}
        
        self.scraper.getNewResultsFunction(params)
        
        assert(params["new_results_function"] == self.scraper.scrapeShowVideos)
        
    def test_getNewResultsFunction_should_set_proper_params_for_scrapeShowsHomepageFeed_if_scraper_is_new_shows(self):
        params = {"scraper": "new_shows"}
        
        self.scraper.getNewResultsFunction(params)
        
        assert(params["folder"] == "true")
        assert(params["new_results_function"] == self.scraper.scrapeShowsHomepageFeed)
        
    def test_getNewResultsFunction_should_set_proper_params_for_scrapeShowsHomepageFeed_if_scraper_is_popular_shows(self):
        params = {"scraper": "popular_shows"}
        
        self.scraper.getNewResultsFunction(params)
        
        assert(params["folder"] == "true")
        assert(params["new_results_function"] == self.scraper.scrapeShowsHomepageFeed)

    def test_getNewResultsFunction_should_set_proper_params_for_scrapeShowsHomepageFeed_if_scraper_is_trending_shows(self):
        params = {"scraper": "trending_shows"}
        
        self.scraper.getNewResultsFunction(params)
        
        assert(params["folder"] == "true")
        assert(params["new_results_function"] == self.scraper.scrapeShowsHomepageFeed)
    
    def test_createUrl_should_return_a_default_url_if_no_scraper_is_given(self):
        self.scraper = BlipTVScraper()
        
        url = self.scraper.createUrl()
        
        assert(url == self.scraper.urls["main"])

    def test_createUrl_should_return_proper_url_for_browse_shows_scraper(self):
        self.scraper = BlipTVScraper()
        
        url = self.scraper.createUrl({"scraper": "browse_shows", "channel_id": "some_channel"})
        
        assert(url == self.scraper.urls["category_az_listing"] % ("some_channel", "1"))
    
    def test_createUrl_should_return_proper_url_for_staff_picks_scraper(self):
        self.scraper = BlipTVScraper()
        
        url = self.scraper.createUrl({"scraper": "staff_picks", "channel_id": "some_channel"})
        
        assert(url == self.scraper.urls["category_staff_picks"] % ("some_channel", "1"))
        
    def test_createUrl_should_return_proper_url_for_favorites_scraper(self):
        self.scraper = BlipTVScraper()
        
        url = self.scraper.createUrl({"scraper": "favorites", "channel_id": "some_channel"})
        
        assert(url == self.scraper.urls["category_audience_favs"] % ("some_channel", "1"))
                
    def test_createUrl_should_return_proper_url_for_popular_episodes_scraper(self):
        self.scraper = BlipTVScraper()
        
        url = self.scraper.createUrl({"scraper": "popular_episodes", "channel_id": "some_channel"})
        
        assert(url == self.scraper.urls["category_popular_videos"] % ("some_channel", "1"))

    def test_createUrl_should_return_proper_url_for_trending_episodes_scraper(self):
        self.scraper = BlipTVScraper()
        
        url = self.scraper.createUrl({"scraper": "trending_episodes", "channel_id": "some_channel"})
        
        assert(url == self.scraper.urls["category_trending_videos"] % ("some_channel", "1"))
            
    def test_createUrl_should_return_proper_url_for_new_episodes_scraper(self):
        self.scraper = BlipTVScraper()
        
        url = self.scraper.createUrl({"scraper": "new_episodes", "channel_id": "some_channel"})
        
        assert(url == self.scraper.urls["category_recent_videos"] % ("some_channel", "1"))
    
    def test_createUrl_should_return_proper_url_for_category_scraper(self):
        self.scraper = BlipTVScraper()
        
        url = self.scraper.createUrl({"category": "some_category"})
        
        assert(url == self.scraper.urls["main"] + "some_category")
    
    def test_createUrl_should_return_proper_url_for_popular_shows_scraper(self):
        self.scraper = BlipTVScraper()
        
        url = self.scraper.createUrl({"scraper": "popular_shows"})
        
        assert(url == self.scraper.urls["home_popular"] % "1")
        
    def test_createUrl_should_return_proper_url_for_trending_shows_scraper(self):
        self.scraper = BlipTVScraper()
        
        url = self.scraper.createUrl({"scraper": "trending_shows"})
        
        assert(url == self.scraper.urls["home_trending"] % "1")
        
    def test_createUrl_should_return_proper_url_for_new_shows_scraper(self):
        self.scraper = BlipTVScraper()
        
        url = self.scraper.createUrl({"scraper": "new_shows"})
        
        assert(url == self.scraper.urls["home_new"] % "1")
        
    def test_createUrl_should_return_proper_url_for_show_scraper_with_show(self):
        self.scraper = BlipTVScraper()
        
        url = self.scraper.createUrl({"scraper": "show", "show": "some_show"})
        
        assert(url == self.scraper.urls["main"] + "some_show")
        
    def test_createUrl_should_return_proper_url_for_show_scraper_user_id(self):
        self.scraper = BlipTVScraper()
        
        url = self.scraper.createUrl({"scraper": "show", "user_id": "some_user_id"})
        
        assert(url == self.scraper.urls["show_episodes"] % ("some_user_id", "1"))
        
    def test_createUrl_should_return_proper_url_for_search_scraper(self):
        self.scraper = BlipTVScraper()
        
        url = self.scraper.createUrl({"scraper": "search", "search": "some_search"})
        
        assert(url == self.scraper.urls["search_episodes"] % ("some_search", "1"))

    def test_createUrl_should_return_proper_url_for_show_search_scraper(self):
        self.scraper = BlipTVScraper()

        url = self.scraper.createUrl({"scraper": "show_search", "search": "some_search"})

        assert(url == self.scraper.urls["search_shows"] % ("some_search", "1"))

    def test_paginator_should_call_cache_function_with_pointer_to_new_results_function_if_scraper_is_not_show(self):
        result = self.scraper.paginator({"scraper": "some_scraper", "new_results_function": "some_function_pointer"})

        print repr(result)
        sys.modules["__main__"].cache.cacheFunction.assert_called_with("some_function_pointer", {"scraper": "some_scraper", "path": "/root", "new_results_function": "some_function_pointer", "page": "0"})

    def test_paginator_should_call_new_results_function_pointer_if_scraper_is_show_and_show_is_in_params(self):
        self.scraper.scrapeShow = Mock()
        self.scraper.scrapeShow.return_value = ["some_string"]
        params = {"scraper": "show", "new_results_function": self.scraper.scrapeShow, "show": "some_show"}

        result = self.scraper.paginator(params)

        print repr(result)
        sys.modules["__main__"].cache.cacheFunction.assert_called_with(self.scraper.scrapeShow, params)

    def test_paginator_should_return_error_if_no_results_are_found(self):
        sys.modules["__main__"].cache.cacheFunction.return_value = []

        result = self.scraper.paginator({"scraper": "some_scraper", "new_results_function": "some_function_pointer"})

        assert(result == [])

    def test_paginator_should_call_utils_addNextFolder_if_item_list_is_longer_than_per_page_count(self):
        videos = []
        i = 0
        while i < 50:
            videos.append("some_cached_string_" + str(i))
            i += 1

        sys.modules["__main__"].cache.cacheFunction.return_value = videos

        result = self.scraper.paginator({"scraper": "some_scraper", "new_results_function": "some_function_pointer", "batch": "true"})

        assert(sys.modules["__main__"].utils.addNextFolder.call_count > 0)

    def test_paginator_should_limit_list_length_if_its_longer_than_perpage(self):
        videos = []
        i = 0
        while i < 50:
            videos.append("some_cached_string_" + str(i))
            i += 1

        sys.modules["__main__"].cache.cacheFunction.return_value = videos

        result = self.scraper.paginator({"scraper": "some_scraper", "new_results_function": "some_function_pointer"})
        print repr(len(result))
        assert(len(result) == 15)

    def test_paginator_should_not_limit_list_length_if_fetch_all_is_set(self):
        videos = []
        i = 0
        while i < 50:
            videos.append("some_cached_string_" + str(i))
            i += 1

        sys.modules["__main__"].cache.cacheFunction.return_value = (videos, 200)

        result, status = self.scraper.paginator({"scraper": "some_scraper", "new_results_function": "some_function_pointer", "fetch_all": "true"})

        assert(len(result) == 50)

    def test_paginator_should_begin_list_at_correct_count_if_page_is_set(self):
        videos = []
        i = 0
        while i < 50:
            videos.append("some_cached_string_" + str(i))
            i += 1

        sys.modules["__main__"].cache.cacheFunction.return_value = videos

        result = self.scraper.paginator({"scraper": "some_scraper", "new_results_function": "some_function_pointer", "page": "1"})

        assert(result[0] == "some_cached_string_15")
        assert(result[14] == "some_cached_string_29")

if __name__ == '__main__':
    nose.runmodule()
