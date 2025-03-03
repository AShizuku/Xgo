import json
import time
import GET
import datetime
import DtsPRO

# 获取json
def resp2_feed(json_id):
    url2 = f"https://www.coolapk.com/feed/{json_id}" 
    resp2 = GET.get_url(url2)
    content(resp2)


# 获取json数据
def content(resp2):
    if resp2.json()['data']['istag'] == 1 or resp2.json()['data']['ershou_info']['product_config_data'] == '' :
        config = '无参数'
    else:
        sb_config = resp2.json()['data']['ershou_info']['product_config_data']
        data_dict = json.loads(sb_config)
        config = "||".join(str(value) for value in data_dict.values())
    data_timestamp = datetime.datetime.fromtimestamp(resp2.json()['data']['create_time']) # 时间戳获取
    data_message_title = resp2.json()['data']['message_title'] # 标题
    data_picArr = resp2.json()['data']['picArr'] # 图片
    data_link_url = resp2.json()['data']['ershou_info']['link_url']
    content=(
        f"🌸 昵称: {resp2.json()['data']['username']}\n\n" 
        f"❤️ 内容: {resp2.json()['data']['message']}\n\n"
        f"🧡 参数: {config}\n\n"
        f"💙 时间：{data_timestamp}\n\n"
    )
    ddts = DtsPRO.send_dingtalk_message(data_picArr[0],resp2.json()['data']['id'],data_message_title,content,data_link_url)
    #print(content)

# 全局变量，用于存储已处理过的ID
processed_ids = set()
def main(resp,js_data=0):
    try:
        json_data = resp.json()
        new_ids = []  # 用于存储本次获取的新ID
        for item in json_data['data']:
            item_id = item['id']
            if item_id not in processed_ids:  # 如果是新的ID
                processed_ids.add(item_id)  # 添加到已处理ID集合中
                new_ids.append(item_id)  # 将新ID添加到列表中
        # 输出本次获取的所有新ID
        for new_id in new_ids:
            js_data +=1
            print(f"🎉有新的消息了! TOP:{js_data} ID:{new_id}")
            resp2_feed(new_id)
            time.sleep(1)
            
    except Exception as e:
        print(f"发生错误: {e}❌")


if __name__ == "__main__":
    url_id = "2116"
    base_url = "https://api.coolapk.com/v6/page/dataList/page?url=/product/feedList?cacheExpires=60&type=trade&id={url_id}&listType=dateline_desc"
    url1 = base_url.format(url_id=url_id)
    max_retries = 3  # 每次请求的最大重试次数
    retry_interval = 2  # 每次重试的间隔时间（秒）

    while True:  # 无限循环，持续运行
        retry_count = 0
        while retry_count < max_retries:
            try:
                resp = GET.get_url(url1)  # 发起请求
                if resp and resp.status_code == 200:
                    print("GET 成功，开始处理数据✔️")
                    main(resp)  # 处理响应数据
                    break  # 成功处理后退出当前重试循环
                else:
                    print(f"尝试获取数据，重试次数: {retry_count + 1}/{max_retries}")
                    print("GET 失败，正在重试...")
                    retry_count += 1
                    time.sleep(retry_interval)  # 等待一段时间后重试
            except Exception as e:
                print(f"请求过程中发生错误: {e}❌")
                retry_count += 1
                time.sleep(retry_interval)  # 等待一段时间后重试
        else:
            print("达到最大重试次数，本次获取数据失败。❌")
        time.sleep(10)  # 每次循环间隔10秒，避免过于频繁请求