import requests
import boto3
import json
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# 配置 Slack, Telegram, Line Notify, Discord
slack_token = 'your_slack_token_here'
channel_name = 'your_channel_name_here'
telegram_bot_token = 'your_telegram_bot_token_here'
telegram_chat_id = 'your_telegram_chat_id_here'
line_notify_token = 'your_line_notify_token_here'
discord_webhook_url = 'your_discord_webhook_url_here'

# 啟用/停用機器人選項
enable_slack_bot = True
enable_telegram_bot = True
enable_line_notify = True
enable_discord_notify = True

# CWA API URL
cwa_api_url = 'https://opendata.cwa.gov.tw/api/v1/rest/datastore/W-C0033-001'
params = {
    'Authorization': 'your_cwa_api_key_here',
    'format': 'JSON',
    'locationName': '高雄市',
    'phenomena': '大雨,豪雨,大豪雨,超大豪雨,海上陸上颱風'
}

# 定义 Parameter Store 参数的名称
parameter_name = '/weather_alert/last_hazard_info'

# 初始化 boto3 客户端
ssm = boto3.client('ssm')

def load_last_hazard_info():
    try:
        response = ssm.get_parameter(Name=parameter_name, WithDecryption=True)
        return response['Parameter']['Value']
    except ssm.exceptions.ParameterNotFound:
        return None

def save_last_hazard_info(hazard_info):
    ssm.put_parameter(Name=parameter_name, Value=hazard_info, Type='String', Overwrite=True)

def send_notifications(weather_info):
    # 發送到 Slack
    if enable_slack_bot:
        client = WebClient(token=slack_token)
        try:
            response = client.chat_postMessage(
                channel=channel_name,
                text=weather_info
            )
        except SlackApiError as e:
            print(f"Error sending message to Slack: {e.response['error']}")

    # 發送到 Telegram
    if enable_telegram_bot:
        telegram_url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
        telegram_params = {
            'chat_id': telegram_chat_id,
            'text': weather_info
        }
        response = requests.get(telegram_url, params=telegram_params)
        if response.status_code != 200:
            print(f"Error sending message to Telegram: {response.status_code}, {response.text}")

    # 發送到 Line Notify
    if enable_line_notify:
        line_notify_url = 'https://notify-api.line.me/api/notify'
        line_notify_headers = {
            'Authorization': f'Bearer {line_notify_token}'
        }
        line_notify_data = {
            'message': weather_info
        }
        response = requests.post(line_notify_url, headers=line_notify_headers, data=line_notify_data)
        if response.status_code != 200:
            print(f"Error sending message to Line Notify: {response.status_code}, {response.text}")

    # 發送到 Discord
    if enable_discord_notify:
        discord_data = {
            'content': weather_info
        }
        response = requests.post(discord_webhook_url, json=discord_data)
        if response.status_code != 204:
            print(f"Error sending message to Discord: {response.status_code}, {response.text}")

def lambda_handler(event, context):
    # 發送 API 請求
    response = requests.get(cwa_api_url, params=params)
    data = response.json()

    # 檢查 hazards 是否有內容並格式化訊息
    try:
        hazards = data['records']['location'][0]['hazardConditions']['hazards']
        if hazards:
            hazard_info = hazards[0]
            language = hazard_info['info']['language']
            phenomena = hazard_info['info']['phenomena']
            significance = hazard_info['info']['significance']
            start_time = hazard_info['validTime']['startTime']
            end_time = hazard_info['validTime']['endTime']
            
            weather_info = (f"高雄市的天氣狀況\n"
                            f"現象：{phenomena}\n"
                            f"意義：{significance}\n"
                            f"開始時間：{start_time}\n"
                            f"結束時間：{end_time}")

            # 从 Parameter Store 加载上次的警报信息
            last_hazard_info = load_last_hazard_info()

            # 如果当前信息与上次不同，或者上次无警报，则发送通知并保存当前信息
            if weather_info != last_hazard_info:
                send_notifications(weather_info)
                save_last_hazard_info(weather_info)

        # 如果当前无警报，并且上次有警报，清空 Parameter Store 中的记录
        elif last_hazard_info:
            save_last_hazard_info("")

    except KeyError as e:
        print(f"無法取得天氣資訊，出現 KeyError: {e}")