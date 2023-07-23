import json
import os
from os.path import expanduser
import subprocess

DIR_UMN = os.getcwd()
if DIR_UMN[-7:] == "setting":
    os.chdir('..')
    DIR_UMN = os.getcwd()

DIR_CONFIG =   os.path.expanduser("~") + '/.uumail_notification/settings'
PATH_CONFIG = DIR_CONFIG + '/config.json'
PATH_ICON = "icon/uumail.ico"

default_config = {'sync_interval': '60','DontNotify_NoMail' : 'True'}

os.makedirs(DIR_CONFIG, exist_ok=True)


def write_config(config):
    with open(PATH_CONFIG, 'w') as f:
        json.dump(config, f, indent=4)

def read_config():
    try:
        with open(PATH_CONFIG) as f:
            config = json.load(f)
        # キーが存在しなければ、エラーを吐いて、except文へ（設定ファイル作り直し）
        config['sync_interval']
        config['DontNotify_NoMail']
    except:
            config = default_config
            write_config(config)
    return config
