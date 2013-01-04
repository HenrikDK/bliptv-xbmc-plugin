'''
   BlipTV plugin for XBMC
   Copyright (C) 2010-2011 Tobias Ussing And Henrik Mosgaard Jensen

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import sys
import urllib


class BlipTVStorage():
    def __init__(self):
        self.settings = sys.modules["__main__"].settings
        self.language = sys.modules["__main__"].language
        self.common = sys.modules["__main__"].common
        self.utils = sys.modules["__main__"].utils
        self.xbmc = sys.modules["__main__"].xbmc

    def list(self, params={}):
        self.common.log("")
        get = params.get
        if get("store") == "searches":
            return self.getStoredSearches(params)

        return self.retrieve(params)

    def deleteFromMyFavoriteShows(self, params):
        self.common.log("")
        get = params.get

        params["store"] = "favorites"
        favorites = self.retrieve(params)

        for count, favorite in enumerate(favorites):
            if (favorite.get("show") == get("show")):
                del(favorites[count])
                break

        self.store(params, favorites)

        self.xbmc.executebuiltin("Container.Refresh")

    def addToMyFavoritesShow(self, params={}, item={}):
        self.common.log("")

        params["store"] = "favorites"
        favorites = self.retrieve(params)

        favorites.append(item)
        favorites = sorted(favorites, key=lambda k: k['Title'])

        self.store(params, favorites)
        del params["store"]

    def getStoredSearches(self, params={}):
        self.common.log(repr(params))
        get = params.get

        searches = self.retrieve(params)

        result = []
        for search in searches:
            item = {}
            item["path"] = get("path")
            item["Title"] = search
            item["search"] = urllib.quote_plus(search)

            if (get("store") == "searches"):
                item["feed"] = "search"
                item["icon"] = "search"
                item["scraper"] = "search"

            thumbnail = self.retrieve(params, "thumbnail", item)
            if thumbnail:
                item["thumbnail"] = thumbnail
            else:
                item["thumbnail"] = item["icon"]

            result.append(item)

        self.common.log("Done: " + repr(result), 5)
        return result

    def deleteStoredSearch(self, params={}):
        self.common.log("")
        get = params.get
        params["store"] = "searches"

        query = urllib.unquote_plus(get("delete"))

        searches = self.retrieve(params)

        for count, search in enumerate(searches):
            if (search.lower() == query.lower()):
                del(searches[count])
                break

        self.store(params, searches)

        self.xbmc.executebuiltin("Container.Refresh")

    def saveSearch(self, params={}):
        self.common.log("")
        get = params.get

        if get("search") and get("scraper") == "search":
            params["store"] = "searches"

            searches = self.retrieve(params)

            new_query = urllib.unquote_plus(get("search"))
            old_query = new_query

            if get("old_search"):
                old_query = urllib.unquote_plus(get("old_search"))

            for count, search in enumerate(searches):
                if (search.lower() == old_query.lower()):
                    del(searches[count])
                    break

            searchCount = (10, 20, 30, 40)[int(self.settings.getSetting("saved_searches"))]
            searches = [new_query] + searches[:searchCount]
            self.store(params, searches)
            del params["store"]

    def editStoredSearch(self, params={}):
        self.common.log("")
        get = params.get
        params["store"] = "searches"

        if (get("search")):
            old_query = urllib.unquote_plus(get("search"))
            new_query = self.common.getUserInput(self.language(30515), old_query)
            params["search"] = new_query
            params["old_search"] = old_query

            if (get("action") == "edit_search"):
                params["store"] = "searches"
                self.saveSearch(params)
                params["feed"] = "search"
            params["search"] = urllib.quote_plus(new_query)

        if "old_search" in params:
            del params["old_search"]

        if "store" in params:
            del params["store"]

        if "action" in params:
            del params["action"]

    #=================================== Storage Key ========================================
    def getStorageKey(self, params={}, storage_type="", item={}):
        self.common.log("")

        if storage_type == "value":
            return self._getValueStorageKey(params, item)
        elif storage_type == "thumbnail":
            return self._getThumbnailStorageKey(params, item)

        return self._getResultSetStorageKey(params)

    def _getThumbnailStorageKey(self, params={}, item={}):
        self.common.log("")
        get = params.get
        iget = item.get
        key = ""

        if get("search") or iget("search"):
            key = "search_"

            if get("search"):
                key += urllib.unquote_plus(get("search", ""))

            if iget("search"):
                key += urllib.unquote_plus(iget("search", ""))

        if key:
            key += "_thumb"

        return key

    def _getValueStorageKey(self, params={}, item={}):
        self.common.log("")
        get = params.get
        iget = item.get
        key = ""

        if (get("action") == "reverse_order" and iget("playlist")):
            key = "reverse_playlist_" + iget("playlist")
            self.common.log(key)
            if (get("external")):
                key += "_external_" + get("contact")

        return key

    def _getResultSetStorageKey(self, params={}):
        self.common.log("")
        get = params.get

        key = ""

        if get("scraper"):
            key = "s_" + get("scraper")

            if get("category"):
                key += "_" + get("category")

            if get("show"):
                key += "_" + get("show")

        if get("store"):
            key = "store_" + get("store")

        self.common.log(key, 4)
        return key

    #============================= Storage Functions =================================
    def store(self, params={}, results=[], store_type="", item={}):
        self.common.log("")
        key = self.getStorageKey(params, store_type, item)

        if store_type == "thumbnail" or store_type == "viewmode" or store_type == "value":
            self.storeValue(key, results)
        else:
            self.storeResultSet(key, results)

    def storeValue(self, key, value):
        self.common.log("")
        if value:
            self.settings.setSetting(key, value)

    def storeResultSet(self, key, results=[], params={}):
        self.common.log("" + repr(params))
        get = params.get

        if results:
            if get("prepend"):
                searchCount = (10, 20, 30, 40)[int(self.settings.getSetting("saved_searches"))]
                existing = self.retrieveResultSet(key)
                existing = results + existing[:searchCount]
                self.settings.setSetting(key, repr(existing))
            elif get("append"):
                existing = self.retrieveResultSet(key)
                existing = existing + results
                self.settings.setSetting(key, repr(existing))
            else:
                value = repr(results)
                self.settings.setSetting(key, value)

    #============================= Retrieval Functions =================================
    def retrieve(self, params={}, retrieve_type="", item={}):
        self.common.log("")
        key = self.getStorageKey(params, retrieve_type, item)

        if retrieve_type == "thumbnail" or retrieve_type == "viewmode" or retrieve_type == "value":
            return self.retrieveValue(key)
        else:
            return self.retrieveResultSet(key)

    def retrieveValue(self, key):
        self.common.log("")
        value = ""
        if key:
            value = self.settings.getSetting(key)

        return value

    def retrieveResultSet(self, key):
        self.common.log("")
        results = []

        value = self.settings.getSetting(key)
        if value:
            try:
                results = eval(value)
            except:
                results = []

        return results
