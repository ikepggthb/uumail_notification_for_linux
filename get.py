# uumail notification 
# version : 2.1
# get.py
#
# © 2020 Ikkei Yamada All Rights Reserved.
# Twitter: @idkaeti
# Email  : ikeprg@gmail.com

#   Released under the GPLv3 license.

import requests
import time
import re

class Get_mail_recent():
    """
    get()             : def メール情報の取得をする,
    run([回数])       : def メール情報の取得を複数回繰り返す,
    info_mail_recent  : str 取得したメール情報,
    """
    def __init__(self,authid="",password=""):
        super().__init__()
        self.url = "https://uumail.cc.utsunomiya-u.ac.jp/am_bin/amlogin"
        self.url_login = "https://uumail.cc.utsunomiya-u.ac.jp/am_bin/amlogin/login_auth"
        self.url_logout = "https://uumail.cc.utsunomiya-u.ac.jp/am_bin/amlogin/logout"
        self.fail_message = {
            "FAIL_ACSESS"   : "アクセスに失敗しました",
            "WRONG_DATA"    : "IDやパスワードが違う可能性があります",
            "FAIL_GET_INFO" : "情報の取得に失敗しました"
        }
        self.authid = authid
        self.password = password
        self.info_mail_recent = "メール情報の取得をしていません"
        self.info_mail_prev = ""
    def gen_login_deta(self):
        login_data = {
            'login_page_lang': 'ja',
            'charset': 'UTF-8',
            'am_authid': self.authid,
            'am_authpasswd': self.password,
            'language': 'auto',
            'ajax': 'on'
        }
        return login_data
    def get(self):
        """
        メール情報の取得をする,
        返り値:bool,
        変数info_mail_recentへ保存
        """
        # セッションの作成
        print("get ...")
        session = requests.session()
        try:
            login_data = self.gen_login_deta()
            login = session.post(self.url_login, data=login_data, timeout=(3.0, 8))

            # 取得したコードのJavascript内にある"self.location.href="のあとのURLを取得
            search_redirect_url = re.search("(?<=self.location.href=\").+(?=\")", login.text)

            if search_redirect_url :
                redirect_url =search_redirect_url.group()
            else :
                self.info_mail_recent = self.fail_message["FAIL_ACSESS"]
                return False
            # time.sleep(0.5)

            # リダイレクト
            session.get(redirect_url, timeout=(3.0, 8))
        except :
            self.info_mail_recent = self.fail_message["FAIL_ACSESS"]
            return False


        # urlからセッションIDを取得
        search_session_id = re.search("(?<=id=)[0-9]+_[0-9]+", redirect_url)
        if search_session_id :
            session_id = search_session_id.group()
        else :
            self.info_mail_recent = self.fail_message["WRONG_DATA"]
            return False

        try:
            # homeへアクセス
            # time.sleep(0.5)
            uumail_home = session.get(redirect_url.replace("top", "home"))

        except:
            self.info_mail_recent = self.fail_message["FAIL_GET_INFO"] 
            return False
        
        # 新着メール情報
        search_mail_recent_class = re.search("<div class=\"mail_recent shadow\">(\s|.)*?</div>", uumail_home.text)
        if search_mail_recent_class :
            search_info_mail_recent = re.search("(?<=<li>).*?(?=</li>)", search_mail_recent_class.group().replace("\n", "").replace(" ", ""))
            if search_info_mail_recent :
                self.info_mail_recent = search_info_mail_recent.group()
            else :
                self.info_mail_recent = self.fail_message["FAIL_GET_INFO"] 
                return False
        else :
            self.info_mail_recent = self.fail_message["FAIL_GET_INFO"] 
            return False

        try:
            # logout処理
            logout_url = self.url_logout + "?id=" + session_id
            # time.sleep(0.5)
            logout = session.get(logout_url, timeout=(3.0, 8))
        except:
            print("fail logout")

        return True

    def run(self,redo_count = 5):
        """
        メール情報の取得が成功するまで複数回繰り返す,
        返り値:bool,
        変数"info_mail_recent"へ保存
        """
        self.info_mail_prev = self.info_mail_recent
        count = 0
        while count < redo_count:
            if self.get():
                return True
            count += 1
            time.sleep(5)
        return False

    def is_same_before(self):
        return  self.info_mail_prev == self.info_mail_recent
    def is_nomail(self):
        return self.info_mail_recent == "新着メールはありません"