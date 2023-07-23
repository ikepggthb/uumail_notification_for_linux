# © 2023 Ikkei Yamada All Rights Reserved.
# Email  : ikeprg@gmail.com

import sys
from PySide6 import QtCore, QtWidgets, QtGui

import notification_daemon
from setting import setting
from setting import passcrypt
import umn_systray


def main():

    # todo: 多重起動防止 
    app = QtWidgets.QApplication([])

    systray = umn_systray.umn_systray()

    try :
        passcrypt.read_data()
    except:
        QtWidgets.QMessageBox.warning(None, \
                                                "uumail notification - エラー", \
                                                "アカウント情報を読み込めません。\nアカウント情報を設定してください", \
                                                QtWidgets.QMessageBox.Ok)
        systray.show_setting()
    
    reg_notify = notification_daemon.Regularly_notify(systray)
    reg_notify.start()

    app.exec()


if __name__ == "__main__":
    main()

