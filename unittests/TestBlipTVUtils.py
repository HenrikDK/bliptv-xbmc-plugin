# -*- coding: utf-8 -*-
import nose
import BaseTestCase
from mock import Mock, patch
import sys
from  BlipTVUtils import BlipTVUtils 

class TestBlipTVUtils(BaseTestCase.BaseTestCase):
        def test_showMessage_should_call_xbmc_execute_builtin_correctly(self):
                sys.modules["__main__"].settings.getSetting.return_value = "3"
                utils = BlipTVUtils()
                
                utils.showMessage("someHeading","someMessage")

                sys.modules["__main__"].xbmc.executebuiltin.assert_called_with('XBMC.Notification("someHeading", "someMessage", 4000)')
                
        def test_getThumbnail_should_call_xbmc_skinHasImage(self):
                sys.modules["__main__"].xbmc.skinHasImage = Mock()
                utils = BlipTVUtils()
                
                result = utils.getThumbnail("someTeading")

                sys.modules["__main__"].xbmc.skinHasImage.assert_called_with('BlipTV - Unittest/someTeading.png')
                
        def test_getThumbnail_should_user_default_folder_image_if_no_title_is_given(self):
                sys.modules["__main__"].xbmc.skinHasImage.return_value = False
                utils = BlipTVUtils()
                
                result = utils.getThumbnail("")
                
                sys.modules["__main__"].xbmc.skinHasImage.assert_called_with('BlipTV - Unittest/DefaultFolder.png')
                assert(result == "DefaultFolder.png")
                
        
        def test_getThumbnail_should_user_thumbnail_path_to_resolve_file_paths(self):
                sys.modules["__main__"].settings.getAddonInfo.return_value = "testingPath/"
                sys.modules["__main__"].xbmc.skinHasImage.return_value = False                
                patcher = patch("os.path")
                patcher.start()
                import os
                utils = BlipTVUtils()
                
                result = utils.getThumbnail("")
                call = os.path.join.call_args_list[0]
                patcher.stop()
                
                assert(call == (('testingPath/', 'thumbnails'), {}))
                
        def test_showErrorMessage_should_call_showMessage(self):
                sys.modules["__main__"].language.return_value = "ERROR"
                utils = BlipTVUtils()
                utils.showMessage = Mock()        
                
                result = utils.showErrorMessage("someTitle","someResult",303)
                
                utils.showMessage.assert_called_with("someTitle","someResult")

        def test_showErrorMessage_should_call_showMessage_with_default_message_if_error_is_not_303(self):
                sys.modules["__main__"].language.return_value = "ERROR"
                utils = BlipTVUtils()
                utils.showMessage = Mock()        
                
                result = utils.showErrorMessage("someTitle","someResult")
                
                utils.showMessage.assert_called_with("someTitle","ERROR")
        
        def test_showErrorMessage_should_use_default_title_if_non_is_present(self):
                sys.modules["__main__"].language.return_value = "ERROR"
                utils = BlipTVUtils()
                utils.showMessage = Mock()        
                
                result = utils.showErrorMessage("someTitle","")
                
                sys.modules["__main__"].language.assert_any_call(30617)

        def test_showErrorMessage_should_use_default_message_if_non_is_present(self):
                sys.modules["__main__"].language.return_value = "ERROR"
                utils = BlipTVUtils()
                utils.showMessage = Mock()        
                
                result = utils.showErrorMessage("","someResult")
                
                sys.modules["__main__"].language.assert_any_call(30600)
        
        def test_buildItemUrl_should_ignore_items_in_blacklist(self):
                input = {"path":"FAIL","thumbnail":"FAIL", "Overlay":"FAIL", "icon":"FAIL", "next":"FAIL", "content":"FAIL" , "editid":"FAIL", "summary":"FAIL", "published":"FAIL","count":"FAIL","Rating":"FAIL","Plot":"FAIL","Title":"FAIL","new_results_function":"FAIL","some_other_param":"some_value"}
                utils = BlipTVUtils()
                
                result = utils.buildItemUrl(input)
                
                assert(result.find("FAIL") < 0)
                
        def test_buildItemUrl_should_build_url_from_params_collection(self):
                input = {"some_other_param":"some_value", "some_param":"some_other_value"}
                utils = BlipTVUtils()
                
                result = utils.buildItemUrl(input)
                
                assert(result == "some_param=some_other_value&some_other_param=some_value&")

        def test_buildItemUrl_should_append_to_existing_url(self):
                input = {"some_other_param":"some_value", "some_param":"some_other_value"}
                utils = BlipTVUtils()
                
                result = utils.buildItemUrl(input, "myfirst_url?")
                
                assert(result == "myfirst_url?some_param=some_other_value&some_other_param=some_value&")
                
        def test_addNextFolder_should_ignore_item_Title_thumbnail_page_and_new_results_funtion(self):
                sys.modules["__main__"].language.return_value = "Next"
                input = {"some_other_param":"some_value", "some_param":"some_other_value","page":"1","Title":"My annoying Title", "thumbnail":"someThumbnail","new_results_function":"functionPointer"}
                utils = BlipTVUtils()
                result = []
                
                utils.addNextFolder(result, input)
                
                assert(result[0]["Title"] == "Next")
                assert(result[0]["some_other_param"] == "some_value")
                assert(result[0]["some_param"] == "some_other_value")
                assert(result[0]["page"] == "2")
                assert(result[0]["thumbnail"] == "next")
                assert(result[0]["next"] == "true")
                
        def test_addNextFolder_should_increment_current_page(self):
                sys.modules["__main__"].language.return_value = "Next"
                input = {"some_other_param":"some_value", "some_param":"some_other_value","page":"45"}
                utils = BlipTVUtils()
                result = []
                
                utils.addNextFolder(result, input)
                
                assert(result[0]["page"] == "46")

if __name__ == '__main__':
        nose.runmodule()
