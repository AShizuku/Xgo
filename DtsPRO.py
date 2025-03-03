import requests
import json
import os
import time
import hmac
import hashlib
import base64
import urllib.parse
import Xgo.GET as GET


def get_img_token():
    response = requests.get(url='https://oapi.dingtalk.com/gettoken', params={"appkey":'dingz1ujtgxumtnz3kga',"appsecret":'EqyheUFmozDY2YFzNey_c8mIy8_fEuS29jy5BjVSISQ_yfx0LaQU9AagNDD5QXYa'})
    response.close()
    access_token = response.json().get("access_token") # 获取token
    return(access_token)
def get_img(image_path):
    if not os.path.exists(image_path):
        print("文件不存在，请检查路径是否正确！❌")
        return None
    access_token = get_img_token()
    upload_url = f"https://oapi.dingtalk.com/media/upload?access_token={access_token}&type=image"
    with open(image_path, 'rb') as image_file:
        files = {
            'media': (os.path.basename(image_path), image_file, 'image/jpeg')
        }
        ddts_img = requests.post(upload_url, files=files)
        ddts_img.close()
    result = ddts_img.json()
    if result.get("errcode") == 0:
        return(result.get("media_id"))
    else:
        print(f"上传失败！❌，错误码{result.get("errmsg")}")
        return('@lADPDfJ6fgjpzFDNAfTNAfQ')
    
def get_url_img(img_url):
    response = GET.get_url(img_url)
    # 检查请求是否成功
    if response.status_code == 200:
        # 保存图片到本地
        with open("downloaded_image.jpg", "wb") as file:
            file.write(response.content)
        # print("图片下载成功！")
        return get_img("downloaded_image.jpg")
    else:
        print(f"下载失败，状态码：{response.status_code}")

def send_dingtalk_message(md_pic_url,kaid,ttitle,message,xyurl):
    # 获取时间戳
    timestamp = str(round(time.time() * 1000))
    secret = 'SECb0d54eb0ec94ae23c48b518ddfb08100f539e942efdf3f6c0ce5d8f15038ca1c'
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code).decode('utf-8'))

    # 钉钉机器人的Webhook URL
    token = 'ce5173b27a28b3c2060a6a2a8baa82b2aa5c60df1c097af23dbb4cafc494444e'
    webhook = f"https://oapi.dingtalk.com/robot/send?access_token={token}&timestamp={timestamp}&sign={sign}"

    # 请求头
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    
    md_pic_url = get_url_img(md_pic_url)

    # 消息内容
    data = {
        "msgtype": "actionCard",
        "actionCard": {
            "title": "到祸啦",
            "text": f"![screenshot]({md_pic_url}) \n\n #### {ttitle} \n\n{message}",
            "btnOrientation": "0",
            "btns": [
                {
                    "title": "咸鱼链接",
                    "actionURL": xyurl
                },
                {
                    "title": "酷安链接",
                    "actionURL": f"https://www.coolapk.com/feed/{kaid}"
                }
            ]
        },
        "at": {
            "isAtAll": 'True'
        }
    }

    # 发送POST请求
    response = requests.post(url=webhook, headers=headers, data=json.dumps(data))
    print("已推送")

    # 返回响应状态码和响应内容
    return response.status_code, response.text





# md_pic_url = "http://image.coolapk.com/feed/2025/0301/19/5002069_3453f3cf_9558_7908_590-uhdr@2160x3840.jpeg"
# kaid = "6666666"
# ttitle = "标题"
# message = "内容"
# xyurl = '#'

# send_dingtalk_message(md_pic_url, kaid, ttitle, message, xyurl)