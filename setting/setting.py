from PySide6 import QtCore, QtWidgets, QtGui
import re

from setting import umn_config, passcrypt

DIR_UMN = umn_config.DIR_UMN

class account_setting_window(QtWidgets.QDialog):
    def __init__(self,setting_window):
        super().__init__()
        self.icon = QtGui.QIcon(umn_config.PATH_ICON)
        self.setWindowIcon(self.icon)
        self.setting_window = setting_window
        # root
        self.setFixedSize(330,100)
        self.setWindowTitle("uumail notification - アカウントを設定する")
        self.setWindowFlags(QtCore.Qt.Dialog|QtCore.Qt.WindowStaysOnTopHint)

        # widget
        self.label_id = QtWidgets.QLabel(self)
        self.label_id.setText("ID")
        self.input_id = QtWidgets.QLineEdit(self)
        self.label_pass = QtWidgets.QLabel(self)
        self.label_pass.setText("パスワード")
        self.input_pass = QtWidgets.QLineEdit(self)
        self.input_pass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.button_cancel = QtWidgets.QPushButton(self)
        self.button_cancel.clicked.connect(self.close_window)
        self.button_cancel.setText("キャンセル")
        self.button_save = QtWidgets.QPushButton(self)
        self.button_save.clicked.connect(self.save_setting)
        self.button_save.setText("OK")

        # layout
        self.win_layout = QtWidgets.QGridLayout(self)
        self.button_layout = QtWidgets.QHBoxLayout(self)
        self.button_layout.setContentsMargins(100,0,0,0)
        self.win_layout.addWidget(self.label_id,0,0)
        self.win_layout.addWidget(self.input_id,0,1)
        self.win_layout.addWidget(self.label_pass,1,0)
        self.win_layout.addWidget(self.input_pass,1,1)
        self.win_layout.addLayout(self.button_layout,2,1)
        self.button_layout.addWidget(self.button_cancel)
        self.button_layout.addWidget(self.button_save)

    def is_collect_login_data(self,ID, PASSWD):
        passwd_in_twoalpha = bool(re.search(r'[a-zA-Z_].*[a-zA-Z_]', PASSWD))
        passwd_in_notalpha = bool(re.search(r'[^a-zA-Z]+', PASSWD))
        # エラーを避けるため、文字数の確認を先に行っている。
        is_collect = \
            len(ID) == 7 and \
            ID[0] == 't' and \
            str.isdecimal(ID[1:7]) and \
            len(PASSWD) >= 6 and \
            passwd_in_twoalpha and \
            passwd_in_notalpha
        return is_collect

    def close_window(self):
        self.hide()
        self.input_id.clear()
        self.input_pass.clear()
    def save_setting(self):
        if self.is_collect_login_data(self.input_id.text(), self.input_pass.text()):
            passcrypt.write_data(self.input_id.text(), self.input_pass.text())
            self.setting_window.login_status_label.setText("状態 : " + self.setting_window.confirm_login_status())
            self.close_window()
        else:
            self.hide()
            self.setWindowFlags(QtCore.Qt.Dialog)
            self.show()
            ret = QtWidgets.QMessageBox.warning(None, \
                                                "uumail notification", \
                                                "正しいIDとパスワードを入力してください", \
                                                QtWidgets.QMessageBox.Ok)
            self.hide()
            self.setWindowFlags(QtCore.Qt.Dialog|QtCore.Qt.WindowStaysOnTopHint)
            self.show()

    def closeEvent(self, event):
        self.close_window()
        event.ignore()

class setting_window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.icon = QtGui.QIcon(umn_config.PATH_ICON)
        self.setWindowIcon(self.icon)
        self.sync_interval_option = {'30分毎': '30', '1時間毎': '60', '2時間毎': "120", '4時間毎': '240'}
        # root, style
        self.setWindowTitle("uumail notification - 設定")
        self.root_x = 620
        self.root_y = 600
        self.header_x = 60
        self.indent_x = 30
        self.setFixedSize(self.root_x,self.root_y)
        self.setStyleSheet("QWidget{font-family: メイリオ;font-size: 14px;}")
        self.heading_style = """
        QLabel{
            font-size: 17px;
            font-weight:bold;
        }
        """

        # widget
        self.icon_settings =  QtGui.QImage(DIR_UMN + '\\setting\\settings.png')
        self.pixmap_setting = QtGui.QPixmap.fromImage(self.icon_settings.scaledToHeight(20))

        self.setting_icon_label = QtWidgets.QLabel(self)
        self.setting_icon_label.setPixmap(self.pixmap_setting)
        self.setting_icon_label.setGeometry(QtCore.QRect(30,20,20,20))
        
        self.setting_label = QtWidgets.QLabel(self)
        self.setting_label.setText("設定")
        self.setting_label.setStyleSheet("QLabel{font-size: 20px; font-weight:bold;}")
        self.setting_label.setGeometry(QtCore.QRect(60,20,100,20))

        self.label_acount = QtWidgets.QLabel(self)
        self.label_acount.setText("アカウント")
        self.label_acount.setStyleSheet(self.heading_style)
        self.label_acount.setGeometry(QtCore.QRect(self.header_x,70,500,20))

        self.login_status_label = QtWidgets.QLabel(self)
        self.login_status_label.setGeometry(QtCore.QRect(self.header_x+self.indent_x,120,500,20))

        self.button_account_setting = QtWidgets.QPushButton(self)
        self.button_account_setting.clicked.connect(self.account_setting_window_show)
        self.button_account_setting.setText("アカウントを設定する")
        self.button_account_setting.setGeometry(QtCore.QRect(130,160,170,30))

        self.button_account_delete = QtWidgets.QPushButton(self)
        self.button_account_delete.clicked.connect(self.delete_account)
        self.button_account_delete.setText("アカウント情報を削除する")
        self.button_account_delete.setGeometry(QtCore.QRect(320,160,200,30))

        self.label_sync = QtWidgets.QLabel(self)
        self.label_sync.setText("同期")
        self.label_sync.setStyleSheet(self.heading_style)
        self.label_sync.setGeometry(QtCore.QRect(self.header_x,230,500,20))

        self.label_sync_interval = QtWidgets.QLabel(self)
        self.label_sync_interval.setText("同期頻度")
        self.label_sync_interval.setGeometry(QtCore.QRect(self.header_x+self.indent_x,280,500,20))

        self.cb_sync_interval = QtWidgets.QComboBox(self)
        self.cb_sync_interval.setGeometry(QtCore.QRect(370,280,150,20))
        self.cb_sync_interval.addItems(self.sync_interval_option.keys())

        self.label_notify = QtWidgets.QLabel(self)
        self.label_notify.setText("通知")
        self.label_notify.setStyleSheet(self.heading_style)
        self.label_notify.setGeometry(QtCore.QRect(self.header_x,430,500,20))

        self.chk_DontNotify_NoMail = QtWidgets.QCheckBox(self)
        self.chk_DontNotify_NoMail.setText("メールがないときは通知しない")
        self.chk_DontNotify_NoMail.setGeometry(QtCore.QRect(self.header_x+self.indent_x,470,500,20))

        self.button_cancel = QtWidgets.QPushButton(self)
        self.button_cancel.clicked.connect(self.cancel)
        self.button_cancel.setText("キャンセル")
        self.button_cancel.setGeometry(QtCore.QRect(350,550,100,30))

        self.button_save = QtWidgets.QPushButton(self)
        self.button_save.clicked.connect(self.save)
        self.button_save.setText("OK")
        self.button_save.setGeometry(QtCore.QRect(460,550,100,30))

        self.account_setting_widget = account_setting_window(self)

        self.set_widget_state()

    def confirm_login_status(self):
        try:
            login_data = passcrypt.read_data()
            status = login_data[0] +' でログインします'
        except:
            status = 'アカウントが設定されていません'
        return status

    def set_widget_state(self):
        self.config = umn_config.read_config()
        self.login_status_label.setText("状態 : " + self.confirm_login_status())
        sync_interval_option_values = list(self.sync_interval_option.values())
        if not self.config['sync_interval'] in sync_interval_option_values:
            umn_config.write_config(umn_config.default_config)
            self.config = umn_config.read_config()
        sync_interval = sync_interval_option_values.index(self.config['sync_interval'])
        self.cb_sync_interval.setCurrentIndex(sync_interval)
        
        if bool(self.config['DontNotify_NoMail']):
            self.chk_DontNotify_NoMail.setCheckState(QtCore.Qt.Checked)
        else:
            self.chk_DontNotify_NoMail.setCheckState(QtCore.Qt.Unchecked)
    
    def is_login_id(self):
        try:
            passcrypt.read_data()
            return True
        except:
            return False
    
    def account_setting_window_show(self):
        self.account_setting_widget.open()

    def delete_account(self):
        passcrypt.del_data()
        QtWidgets.QMessageBox.information(None, \
                                        "uumail notification", \
                                        "アカウント情報を削除しました", \
                                        QtWidgets.QMessageBox.Ok)
        self.login_status_label.setText("状態 : " + self.confirm_login_status())

    def save(self):
        if not self.is_login_id():
            ret = QtWidgets.QMessageBox.warning(None, \
                                         "uumail notification - エラー", \
                                         "アカウント情報を読み込めません。\nアカウント情報を設定してください", \
                                          QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
            if ret == QtWidgets.QMessageBox.Ok :
                return
        if self.account_setting_widget.isHidden():
            self.config = {
                'sync_interval' :  str(self.sync_interval_option[self.cb_sync_interval.currentText()]),
                'DontNotify_NoMail' : self.chk_DontNotify_NoMail.isChecked()
                }
            umn_config.write_config(self.config)
            self.hide()
    def show(self) -> None:
        self.set_widget_state()
        return super().show()
    def cancel(self):
        if self.account_setting_widget.isHidden():
            self.hide()
    # closeEventをオーバーライド -> ウィンドウを閉じたとき、アプリが終了しないようにするため
    def closeEvent(self, event):
        self.cancel()
        event.ignore()
