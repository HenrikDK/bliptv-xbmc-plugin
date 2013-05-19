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
import json
settings = sys.modules["__main__"].settings
language = sys.modules["__main__"].language
common = sys.modules["__main__"].common
utils = sys.modules["__main__"].utils

def extractForm(html):
    common.log("")
    post_data = {}
    post_url = common.parseDOM(html, "form", ret="action")
    
    if post_url[0].find("http") == 0:
        post_url = post_url[0]
    else:
        post_url = "https://www.facebook.com/" + post_url[0]

    for inp in common.parseDOM(html, "input", ret="name"):
        for val in common.parseDOM(html, "input", attrs={"name": inp.replace("[", "\[").replace("]", "\]")}, ret="value"):
            post_data[inp] = val

    for inp in common.parseDOM(html, "button", ret="name"):
        for val in common.parseDOM(html, "button", attrs={"name": inp.replace("[", "\[").replace("]", "\]")}, ret="value"):
            post_data[inp] = val

    common.log("Done: " + repr(post_url) + " - " + repr(post_data))
    return post_url, post_data

def fbAllowAccess(result):
    common.log("")
    post_url, post_data = extractForm(result["content"])
    del post_data["__CANCEL__"]
    post_data["redirect_uri"] = post_data["redirect_uri"].replace("&amp;", "&")
    common.log("Posting: " + repr(post_data))
    result = common.fetchPage({"link": post_url, "post_data": post_data, "refering": result["new_url"]})
    common.log("Done")
    return result

def fbSecurityCode(result): # Untested after refactor
    common.log("Need 2-factor authentication")
    post_url2, post_data2 = extractForm(result["content"])

    userpin = common.getUserInputNumbers(language(30627))
    if len(userpin) > 0:
        post_data2["approvals_code"] = userpin
        result = common.fetchPage({"link": post_url2, "post_data": post_data2, "refering": result["new_url"]})

    common.log("Done")
    return result

def fbRememberBrowser(result): # Unverified after refactor
    common.log("")
    post_url2, post_data2 = extractForm(result["content"])

    post_url2 = post_url2.replace("%26amp%3B", "%26")
    post_data2["name_action_selected"] = "save_device"
    result = common.fetchPage({"link": post_url2, "post_data": post_data2, "refering": result["new_url"]})

    common.log("Done")
    return result

def fbReviewRecentLogins(result): # Unverified after refactor
    common.log("Must review recent logins")
    post_url2, post_data2 = extractForm(result["content"]) # This should deny all other logins. currently just fails(does both)

    post_url2 = post_url2 # Press continue

    result = common.fetchPage({"link": post_url2, "post_data": post_data2, "refering": result["new_url"]})
    post_data2 = {}
    post_url2 = common.parseDOM(result["content"], "form", ret="action")
    for inp in common.parseDOM(result["content"], "input", ret="name"):
        for val in common.parseDOM(result["content"], "input", attrs={"name": inp.replace("[", "\[").replace("]", "\]")}, ret="value"):
            common.log("Setting input: %s = %s" % (inp, val))
            if val.find("I don&#039;t recognise") > -1:
                continue
            post_data2[inp] = val

    result = common.fetchPage({"link": post_url2, "post_data": post_data2, "refering": result["new_url"]}) # Press "this is okay"

    post_url2, post_data2 = extractForm(result["content"])

    post_data2["name_action_selected"] = "save_device"
    result = common.fetchPage({"link": post_url2, "post_data": post_data2, "refering": result["new_url"]}) # Press continue

    common.log("Done")
    return result

def getSessionCookies(result, callback_url):
    fb_reply = common.extractJS(result["content"], variable="message")
    common.log("FB_REPLY: " + repr(fb_reply))
    if len(fb_reply) == 0:
        common.log("Result1: " + repr(result), 0)
        return result

    fb_reply = common.getParameters(fb_reply[0])
    common.log("FB_REPLY: " + repr(fb_reply))

    user_id = 0

    tcookies = common.getCookieInfoAsHTML()
    for inp in common.parseDOM(tcookies, "cookie", ret="name"):
        for val in common.parseDOM(tcookies, "cookie", attrs={"name": inp.replace("[", "\[").replace("]", "\]")}, ret="value"):
            if inp.find("c_user") > -1:
                user_id = val
                common.log("Found cookie: " + repr(inp) + " = " + repr(val))

    post_data = {"authResponse": json.dumps({"accessToken": fb_reply["access_token"],
                                             "userID": user_id,
                                             "expiresIn": fb_reply["expires_in"],
                                             "signedRequest": fb_reply["signed_request"]}),
                 "skin": "json",
                 "no-cache": 1,
                 "no-wrap": 1}
    cookies = "fbm_136482209767138=base_domain=.blip.tv; v_session=LOGGEDOUT; "
    cookies += "fbsr_136482209767138=" + fb_reply["signed_request"] + "; "

    result = common.fetchPage({"link": callback_url, "refering": result["new_url"], "cookie": cookies, "post_data": post_data})
    common.log("Done: " + repr(result), 0)
    return return cookies

def replaceSessionCookie(cookies):
    common.log("")

    tcookies = common.getCookieInfoAsHTML()
    for inp in common.parseDOM(tcookies, "cookie", ret="name"):
        for val in common.parseDOM(tcookies, "cookie", attrs={"name": inp.replace("[", "\[").replace("]", "\]")}, ret="value"):
            if inp.find("v_session") > -1:
                common.log("Found cookie: " + repr(inp) + " = " + repr(val))
                cookies.replace("v_session=LOGGEDOUT", "%s=%s; " % (inp, val))
    common.log("Done")
    return cookies

def login(oauth_url, callback_url):
    common.log("")
    cookies = ""
    result = common.fetchPage({"link": oauth_url})

    if result["content"].find("login_form") > -1:
        post_url, post_data = extractForm(result["content"])
                
        post_data["email"] = settings.getSetting("username")
        post_data["pass"] = settings.getSetting("user_password")
        if post_data["pass"] == "":
            post_data["pass"] = common.getUserInput(language(30628), hidden=True)

        del post_data["cancel"]

        result = common.fetchPage({"link": post_url, "post_data": post_data, "refering": result["new_url"]}) # Hits: "The parameter app_id is required". still works.

        if result["content"].find("Enter Security Code to Continue") > -1:
            result = fbSecurityCode(result)

        if result["content"].find("Remember Browser") > -1:
            result = fbRememberBrowser(result)

        if result["content"].find("Review Recent Login") > -1:
            result = fbReviewRecentLogin(result)

        errors = common.parseDOM(result["content"], "div", attrs={"id": "enter_code_error"},)
        if len(errors) > 0:
            common.log("Got error from facebook: " + repr(errors))
            utils.showMessage("Error", errors[0])

    common.log("Result2: " + repr(result), 3)

    result = common.fetchPage({"link": oauth_url, "refering": result["new_url"]})
    common.log("Result3: " + repr(result), 3)
    if result["content"].find("platformDialogForm") > -1:
        result = fbAllowAccess(result)

    if result["content"].find("signed_request") > -1:
        cookies = getSessionCookies(result, callback_url)
        cookies = replaceSessionCookie(cookies)

        common.log("cookies2: " + repr(cookies))
        settings.setSetting("login_cookie", json.dumps(cookies))

    common.log("Done: " + repr(cookies))

