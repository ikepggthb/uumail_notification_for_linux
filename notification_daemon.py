# © 2023 Ikkei Yamada All Rights Reserved.
# Email  : ikeprg@gmail.com

import time
import threading

from PySide6 import QtWidgets

import get

# 設定、アカウント情報読み込み 
from setting import passcrypt
from setting import umn_config

class Regularly_notify(threading.Thread):
    def __init__(self,systray = None):
        super(Regularly_notify, self).__init__()
        self.systray = systray
        self.setDaemon(True)
    def read_config(self):
        try:
            ACCOUNT_DATA = passcrypt.read_data()
            CONFIG = umn_config.read_config()
            self.id = ACCOUNT_DATA[0]
            self.passwd = ACCOUNT_DATA[1]
            self.interval = 60 * int(CONFIG['sync_interval']) # 秒
            self.DontNotify_NoMail = bool(CONFIG['DontNotify_NoMail'])
            return True
        except:
            return False

    def notification(self,msg,title="uumail",info_type=QtWidgets.QSystemTrayIcon.Information):
        if self.systray is None:
            print(msg)
        else:
            self.systray.showMessage(title, msg,info_type)

    def run(self):
        # init
        uumail_info_getter = get.Get_mail_recent()
        time_start = time.time()
        self.interval = 0
        count = 0
        while True:
            timer = time.time()
            if timer >= time_start + self.interval * count:
                already_notified_cannot_reed = False
                while not self.read_config():
                    if not already_notified_cannot_reed:
                        self.notification("アカウント情報を読み込めません\nアカウント情報を設定してください","uumail",QtWidgets.QSystemTrayIcon.Critical)
                    already_notified_cannot_reed = True
                    time.sleep(10)
                uumail_info_getter.authid = self.id
                uumail_info_getter.password = self.passwd
                uumail_info_getter.run()
                if not ( ( self.DontNotify_NoMail and uumail_info_getter.is_nomail() ) or uumail_info_getter.is_same_before() ) :
                    self.notification(uumail_info_getter.info_mail_recent)
                count += 1
            time.sleep(10)

