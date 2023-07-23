
# © 2023 Ikkei Yamada All Rights Reserved.
# Email   : ikeprg@gmail.com

#   Released under the GPLv3 license.

import sys
import time
from PySide6 import QtCore, QtWidgets, QtGui
import webbrowser

from setting import setting
from setting import umn_config
from setting import passcrypt
import get

class about_window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.icon = QtGui.QIcon(umn_config.PATH_ICON)
        self.setWindowIcon(self.icon)
        self.setWindowTitle("uumail notification について")
        self.setFixedSize(600,370)
        self.setWindowFlags(QtCore.Qt.Dialog|QtCore.Qt.WindowStaysOnTopHint)
        self.label = QtWidgets.QLabel(self)
        self.label_style = """QLabel {
            font-size: 43px;               /* 文字サイズ */
            padding: 0px 40px;
        }"""
        self.font = QtGui.QFont()
        self.font.setPointSize(13)
        self.label.setStyleSheet(self.label_style)
        self.label.setText("uumail notification")
        self.label.setGeometry(QtCore.QRect(120,0,480,120))
        self.umnlogo_image = QtGui.QImage('icon\\uumail.png')
        self.umnlogo_pixmap = QtGui.QPixmap.fromImage(self.umnlogo_image.scaledToHeight(120))
        self.umnlogo_label = QtWidgets.QLabel(self)
        self.umnlogo_label.setPixmap(self.umnlogo_pixmap)
        self.umnlogo_label.setGeometry(QtCore.QRect(0,0,120,120))
        self.varsion_txt = QtWidgets.QLabel(self)
        self.varsion_txt.setText("Version  :  2.0")
        self.varsion_txt.setFont(self.font)
        self.varsion_txt.setGeometry(QtCore.QRect(40,150,500,30))
        self.github_txt = QtWidgets.QLabel(self)
        self.github_txt.setText("Github : https://github.com/ikepggthb/uumail_notification")
        self.github_txt.setFont(self.font)
        self.github_txt.setGeometry(QtCore.QRect(40,190,500,30))
        self.licence_txt = QtWidgets.QLabel(self)
        self.licence_txt.setText("オープンソースソフトウェア(OSS)であり、GPLv3の条件で許諾されます。\nこのソフトウェアを使用、複製、配布、ソースコードを修正することができます。")
        self.licence_txt.setFont(self.font)
        self.licence_txt.setGeometry(QtCore.QRect(40,230,500,45))
        self.cpn_txt = QtWidgets.QLabel(self)
        self.cpn_txt.setText( "© 2020 ikkei Yamada All Rights Reserved.\n	, Email : ikeprg@gmail.com")
        self.cpn_txt.setFont(self.font)
        self.cpn_txt.setGeometry(QtCore.QRect(40,290,500,45))
    # closeEventをオーバーライド ウィンドウを閉じたとき、アプリが終了しないようにするため
    def closeEvent(self, event):
        self.hide()
        event.ignore()

class umn_systray(QtWidgets.QSystemTrayIcon):
    def __init__(self):
        super().__init__()
        self.icon = QtGui.QIcon(umn_config.PATH_ICON)
        self.setIcon(self.icon)
        self.init_menu()
        self.show()
        
    def init_menu(self):
        # メニューの作成
        self.menu = QtWidgets.QMenu()
        # 項目 : 最新の状態を取得
        self.get_mail_action = QtGui.QAction('最新の状態を取得', self.menu)
        self.get_mail_action.setObjectName('get_mail')
        self.get_mail_action.triggered.connect(self.get_mail)
        self.menu.addAction(self.get_mail_action)
        # 項目 : 最新の状態を取得
        self.open_uumail_action = QtGui.QAction('uumailを開く', self.menu)
        self.open_uumail_action.setObjectName('open_uumail')
        self.open_uumail_action.triggered.connect(self.open_uumail)
        self.menu.addAction(self.open_uumail_action)
        # 項目 : 設定
        self.show_setting_action = QtGui.QAction('設定', self.menu)
        self.show_setting_action.setObjectName('setting')
        self.show_setting_action.triggered.connect(self.show_setting)
        self.menu.addAction(self.show_setting_action)
        self.setting_wg = setting.setting_window()
        # 項目 : バージョン情報
        self.show_about_action = QtGui.QAction('uumail notificationについて', self.menu)
        self.show_about_action.setObjectName('about')
        self.show_about_action.triggered.connect(self.show_about)
        self.menu.addAction(self.show_about_action)
        self.about_wg = about_window()
        # 項目 : Quit
        self.exit_action = QtGui.QAction('Quit', self.menu)
        self.exit_action.setObjectName('exit')
        self.exit_action.triggered.connect(self.quit_)
        self.menu.addAction(self.exit_action)
        # システムトレイアイコンに反映
        self.setContextMenu(self.menu)

    def get_info(self):
        try:
            ACCOUNT_DATA = passcrypt.read_data()
        except:
            self.showMessage("uumail","アカウント情報を読み込めません",QtWidgets.QSystemTrayIcon.Critical)
            return False
        authid = ACCOUNT_DATA[0]
        password = ACCOUNT_DATA[1]
        uumail_info = get.Get_mail_recent(authid=authid,password=password)
        uumail_info.run()
        self.showMessage("uumail", uumail_info.info_mail_recent,QtWidgets.QSystemTrayIcon.Information)
    def get_mail(self):
        self.get_info()
    def open_uumail(self):
        webbrowser.open("https://uumail.cc.utsunomiya-u.ac.jp/")
    def show_setting(self):
        self.setting_wg.show()
    def show_about(self):
        self.about_wg.show()
    def quit_(self):
        sys.exit()
