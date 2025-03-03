import time
import base64
import hashlib
import requests

def get_url(url):
    token = get_token()
    headers = {
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 10; MI 8 MIUI/V12.5.1.0.QEACNXM) (#Build; Xiaomi; MI 8; QKQ1.190828.002 test-keys; 10) +CoolMarket/9.6.2-1910242",
        "X-Requested-With": "XMLHttpRequest",
        "X-App-Id": "com.coolapk.market",
        "X-App-Token": token,
        "X-App-Version": "9.6.2",
        "X-App-Code": "1910242",
        "X-Api-Version": "9",
        "X-App-Device": "4ASSNByOp12bhlGWgsTat9WYphFI7ADO6kDO6QjM6ATR6cDO6QTOgsDbsVnbgsDbsVnbgsTYhdjYhFTZ5gDZllzYwITM",
    }
    resp1 = requests.get(url=url, headers=headers)
    resp1.close()
    return(resp1)

def get_token():
    device_id = "4ASSNByOp12bhlGWgsTat9WYphFI7ADO6kDO6QjM6ATR6cDO6QTOgsDbsVnbgsDbsVnbgsTYhdjYhFTZ5gDZllzYwITM"
    ctime = int(time.time())
    md5_timestamp = hashlib.new('md5', str(ctime).encode()).hexdigest()
    arg1 = "token://com.coolapk.market/c67ef5943784d09750dcfbb31020f0ab?" + md5_timestamp + "$" + device_id + "&com.coolapk.market"
    md5_str = hashlib.new('md5', base64.b64encode(arg1.encode())).hexdigest()
    token = md5_str + device_id + str(hex(ctime))
    return token

