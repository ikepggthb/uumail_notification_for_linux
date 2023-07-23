from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
import os
import shutil


# todo: キーリングを使う

# todo: パスの変数の記述場所を見直す。
PATH_ACCOUNT_DIR = os.path.expanduser("~") + '/.uumail_notification/account'
PATH_PASSWD = PATH_ACCOUNT_DIR + '/login.data'
PATH_KEY = PATH_ACCOUNT_DIR + '/login.key'
PATH_ID = PATH_ACCOUNT_DIR+"/loginid.txt"


def read_bin(path):
    with open(path, mode = "rb") as f:
        data = f.read()
    return data

def write_bin(path, data):
    with open(path, mode = "wb") as f:
	    f.write(data)

def encrypt(input_data):   # str型平文  -->  バイナリ（key,暗号化データ）
    passwd = pad(input_data.encode("utf-8"), AES.block_size)
    key  = Random.get_random_bytes(AES.block_size)
    iv   = Random.get_random_bytes(AES.block_size)
    encrypt_obj = AES.new(key, AES.MODE_CBC, iv)
    data_enc = encrypt_obj.encrypt(passwd)
    return {'key':key, 'passwd':iv + data_enc}

def decrypt(key, input_data):  # バイナリ（key,暗号化データ） -->  str型平文
    # ivと暗号化データに分ける
    iv   = input_data[0:AES.block_size]
    data_enc = input_data[AES.block_size :]
    # 復号化オブジェクトを生成
    decrypt_obj = AES.new(key, AES.MODE_CBC, iv=iv)
    # 復号化、バイナリをstrに変換
    data = unpad(decrypt_obj.decrypt(data_enc), AES.block_size).decode('utf-8')
    return data

def read_data():
    data = read_bin(PATH_PASSWD)
    key = read_bin(PATH_KEY)
    passwd = decrypt(key, data)
    with open(PATH_ID, mode='r') as f:
        loginid = f.read()
    return loginid, passwd

def write_data(loginid,passwd):
    os.makedirs(PATH_ACCOUNT_DIR, exist_ok=True)
    erc = encrypt(passwd)
    write_bin(PATH_KEY, erc['key'])
    write_bin(PATH_PASSWD, erc['passwd'])
    with open(PATH_ID, mode='w') as f:
        f.write(loginid)

def del_data():
    try:
        shutil.rmtree(PATH_ACCOUNT_DIR)
    except OSError as err:
        pass





