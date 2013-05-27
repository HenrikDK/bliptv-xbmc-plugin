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
import sys, time, json

class BlipTVLogin():
    def __init__(self):
        self.settings = sys.modules["__main__"].settings
        self.language = sys.modules["__main__"].language
        self.common = sys.modules["__main__"].common
        self.utils = sys.modules["__main__"].utils

        self.oauth_url = "https://www.facebook.com/dialog/oauth?display=popup&domain=blip.tv&scope=email&e2e=%7B%7D&app_id=136482209767138&locale=en_US&sdk=joey&client_id=136482209767138&redirect_uri=http%3A%2F%2Fstatic.ak.facebook.com%2Fconnect%2Fxd_arbiter.php%3Fversion%3D24%23cb%3Df1ec7ef034f6e36%26origin%3Dhttp%253A%252F%252Fblip.tv%252Ff19fa655d24faaa%26domain%3Dblip.tv%26relation%3Dopener%26frame%3Df4a8273bce9c22&origin=1&response_type=token%2Csigned_request"
        self.callback_url = "http://blip.tv/facebook/verify_viewer_user"

    def extractForm(self, html):
        self.common.log("")
        post_data = {}
        post_url = self.common.parseDOM(html, "form", ret="action")

        if post_url[0].find("http") == 0:
            post_url = post_url[0]
        else:
            post_url = "https://www.facebook.com/" + post_url[0]

        for inp in self.common.parseDOM(html, "input", ret="name"):
            for val in self.common.parseDOM(html, "input", attrs={"name": inp.replace("[", "\[").replace("]", "\]")}, ret="value"):
                post_data[inp] = val

        for inp in self.common.parseDOM(html, "button", ret="name"):
            for val in self.common.parseDOM(html, "button", attrs={"name": inp.replace("[", "\[").replace("]", "\]")}, ret="value"):
                post_data[inp] = val

        self.common.log("Done: " + repr(post_url) + " - " + repr(post_data))
        return post_url, post_data

    def allowAccess(self, result):
        self.common.log("")
        post_url, post_data = self.extractForm(result["content"])
        del post_data["__CANCEL__"]
        post_data["redirect_uri"] = post_data["redirect_uri"].replace("&amp;", "&")
        self.common.log("Posting: " + repr(post_data))
        result = self.common.fetchPage({"link": post_url, "post_data": post_data, "refering": result["new_url"]})
        self.common.log("Done")
        return result

    def securityCode(self, result): # Untested after refactor
        self.common.log("Need 2-factor authentication")
        post_url2, post_data2 = self.extractForm(result["content"])

        userpin = self.common.getUserInputNumbers(self.language(30627))
        if len(userpin) > 0:
            post_data2["approvals_code"] = userpin
            result = self.common.fetchPage({"link": post_url2, "post_data": post_data2, "refering": result["new_url"]})

        self.common.log("Done")
        return result

    def rememberBrowser(self, result): # Unverified after refactor
        self.common.log("")
        post_url2, post_data2 = self.extractForm(result["content"])

        post_url2 = post_url2.replace("%26amp%3B", "%26")
        post_data2["name_action_selected"] = "save_device"
        result = self.common.fetchPage({"link": post_url2, "post_data": post_data2, "refering": result["new_url"]})

        self.common.log("Done")
        return result

    def reviewRecentLogins(self, result): # Unverified after refactor
        self.common.log("Must review recent logins")
        post_url2, post_data2 = self.extractForm(result["content"]) # This should deny all other logins. currently just fails(does both)

        post_url2 = post_url2 # Press continue

        result = self.common.fetchPage({"link": post_url2, "post_data": post_data2, "refering": result["new_url"]})
        post_data2 = {}
        post_url2 = self.common.parseDOM(result["content"], "form", ret="action")
        for inp in self.common.parseDOM(result["content"], "input", ret="name"):
            for val in self.common.parseDOM(result["content"], "input", attrs={"name": inp.replace("[", "\[").replace("]", "\]")}, ret="value"):
                self.common.log("Setting input: %s = %s" % (inp, val))
                if val.find("I don&#039;t recognise") > -1:
                    continue
                post_data2[inp] = val

        result = self.common.fetchPage({"link": post_url2, "post_data": post_data2, "refering": result["new_url"]}) # Press "this is okay"

        post_url2, post_data2 = self.extractForm(result["content"])

        post_data2["name_action_selected"] = "save_device"
        result = self.common.fetchPage({"link": post_url2, "post_data": post_data2, "refering": result["new_url"]}) # Press continue

        self.common.log("Done")
        return result

    def getSessionCookies(self, result, callback_url=False):
        if not callback_url:
            callback_url = self.callback_url
        fb_reply = self.common.extractJS(result["content"], variable="message")
        self.common.log("FB_REPLY: " + repr(fb_reply))
        if len(fb_reply) == 0:
            self.common.log("Result1: " + repr(result), 0)
            return result

        fb_reply = self.common.getParameters(fb_reply[0])
        self.common.log("FB_REPLY: " + repr(fb_reply))

        user_id = 0

        tcookies = self.common.getCookieInfoAsHTML()
        for inp in self.common.parseDOM(tcookies, "cookie", ret="name"):
            for val in self.common.parseDOM(tcookies, "cookie", attrs={"name": inp.replace("[", "\[").replace("]", "\]")}, ret="value"):
                if inp.find("c_user") > -1:
                    user_id = val
                    self.common.log("Found cookie: " + repr(inp) + " = " + repr(val))

        settings.setSetting("login_expires_at", str(time.time() + float(fb_reply["expires_in"]) ))
        post_data = {"authResponse": json.dumps({"accessToken": fb_reply["access_token"],
                                                 "userID": user_id,
                                                 "expiresIn": fb_reply["expires_in"],
                                                 "signedRequest": fb_reply["signed_request"]}),
                     "skin": "json",
                     "no-cache": 1,
                     "no-wrap": 1}
        cookies = "fbm_136482209767138=base_domain=.blip.tv; v_session=LOGGEDOUT; "
        cookies += "fbsr_136482209767138=" + fb_reply["signed_request"] + "; "

        result = self.common.fetchPage({"link": callback_url, "refering": result["new_url"], "cookie": cookies, "post_data": post_data})
        self.common.log("Done: " + repr(result), 0)
        return cookies

    def replaceSessionCookie(self, cookies):
        self.common.log("")

        tcookies = self.common.getCookieInfoAsHTML()
        for inp in self.common.parseDOM(tcookies, "cookie", ret="name"):
            for val in self.common.parseDOM(tcookies, "cookie", attrs={"name": inp.replace("[", "\[").replace("]", "\]")}, ret="value"):
                if inp.find("v_session") > -1:
                    self.common.log("Found cookie: " + repr(inp) + " = " + repr(val))
                    cookies.replace("v_session=LOGGEDOUT", "%s=%s; " % (inp, val))

        self.common.log("Done")

        return cookies

    def login(self, params = {}):
        if not self.settings.getSetting("login_expires_at") or float(self.settings.getSetting("login_expires_at")) < time.time():
            self._login(params)

    def _login(self, params = {}):
        self.common.log("")

        email = self.settings.getSetting("username")
        if email == "":
            self.common.log("No facebook email address provided")
            return False

        pword = self.settings.getSetting("user_password")
        if pword == "":
            pword = self.common.getUserInput(self.language(30628), hidden=True)

        if pword == "":
            self.common.log("No facebook password provided")
            return False

        result = self.common.fetchPage({"link": self.oauth_url})

        self.utils.showMessage(self.language(30027), self.language(30027))
        if result["content"].find("login_form") > -1:
            post_url, post_data = self.extractForm(result["content"])

            post_data["email"] = email
            post_data["pass"] = pword

            del post_data["cancel"]

            result = self.common.fetchPage({"link": post_url, "post_data": post_data, "refering": result["new_url"]}) # Hits: "The parameter app_id is required". still works.

            if result["content"].find("Enter Security Code to Continue") > -1:
                result = self.securityCode(result)

            if result["content"].find("Remember Browser") > -1:
                result = self.rememberBrowser(result)

            if result["content"].find("Review Recent Login") > -1:
                result = self.reviewRecentLogin(result)

            errors = self.common.parseDOM(result["content"], "div", attrs={"id": "enter_code_error"},)
            if len(errors) > 0:
                self.common.log("Got error from facebook: " + repr(errors))
                self.utils.showMessage(self.language(30609), errors[0])

        self.common.log("Result2: " + repr(result), 3)

        result = self.common.fetchPage({"link": self.oauth_url, "refering": result["new_url"]})
        self.common.log("Result3: " + repr(result), 3)
        if result["content"].find("platformDialogForm") > -1:
            result = self.allowAccess(result)

        if result["content"].find("signed_request") > -1:
            cookies = self.getSessionCookies(result, self.callback_url)
            cookies = self.replaceSessionCookie(cookies)

            self.settings.setSetting("login_cookie", json.dumps(cookies))
            self.common.log("Done: " + repr(cookies))
            self.utils.showMessage(self.language(30027), self.language(30031))
        else:
            self.common.log("Failed to login")
            self.utils.showMessage(self.language(30600), self.language(30609))
