
# Weather Alert Bot

This Python script is an AWS Lambda function that checks weather alerts from the Central Weather Administration (CWA) and sends notifications via Slack, Telegram, Line Notify, and Discord.

這個 Python 腳本是一個 AWS Lambda 函數，用於從中央氣象局（CWA）檢查天氣警報，並通過 Slack、Telegram、Line Notify 和 Discord 發送通知。

## Features | 功能

- **Fetches weather alerts** for a specified location from the CWA API.
- **Sends notifications** to multiple platforms:
  - Slack
  - Telegram
  - Line Notify
  - Discord
- **Uses AWS Systems Manager Parameter Store** to store the last alert information to avoid duplicate notifications.

- **從中央氣象局 API 獲取指定地點的天氣警報**。
- **向多個平台發送通知**：
  - Slack
  - Telegram
  - Line Notify
  - Discord
- **使用 AWS Systems Manager Parameter Store** 存儲上次的警報信息，以避免重複通知。

## Setup | 設置

### 1. Clone the Repository | 克隆倉庫

```bash
git clone https://github.com/tbdavid2019/weather-alert-bot_Lambda.git
cd multi-platform-weather-alert-AWS_Lambda
```

### 2. Install Dependencies | 安裝依賴

You need to install the required dependencies. You can use `pip` to install the packages listed in `requirements.txt`.

你需要安裝所需的依賴項。可以使用 `pip` 安裝 `requirements.txt` 中列出的套件。

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables | 配置環境變量

Replace the placeholders in the script with your actual API keys, tokens, and channel IDs. Alternatively, you can set up environment variables or use AWS Secrets Manager/Parameter Store for storing sensitive information.

將腳本中的佔位符替換為你的實際 API 密鑰、令牌和頻道 ID。或者，你可以設置環境變量或使用 AWS Secrets Manager/Parameter Store 來存儲敏感信息。

### 4. Deploy to AWS Lambda | 部署到 AWS Lambda

You can deploy this script to AWS Lambda. Ensure that the Lambda function has the appropriate permissions to access the AWS Systems Manager Parameter Store and to make network requests.

你可以將這個腳本部署到 AWS Lambda。確保 Lambda 函數具有訪問 AWS Systems Manager Parameter Store 和進行網絡請求的適當權限。

### 5. Set Up a Trigger | 設置觸發器

Set up an AWS CloudWatch Events rule or another trigger to periodically invoke the Lambda function.

設置 AWS CloudWatch Events 規則或其他觸發器，定期調用 Lambda 函數。

## Packaging and Deployment | 打包和部署

To package and deploy the project to AWS Lambda:

要將項目打包並部署到 AWS Lambda：

1. **Install dependencies locally** into the project directory:

    **本地安裝依賴項** 到項目目錄：

    ```bash
    pip install -r requirements.txt -t .
    ```

2. **Package the project** into a ZIP file:

    **將項目打包** 成 ZIP 文件：

    ```bash
    zip -r WeatherAlertBot.zip .
    ```

3. **Upload the ZIP file** to AWS Lambda through the AWS Console:

    **將 ZIP 文件上傳** 到 AWS Lambda，通過 AWS 控制台進行操作。

## Environment Variables | 環境變量

- `SLACK_TOKEN`: Your Slack bot token. 你的 Slack 機器人令牌。
- `CHANNEL_NAME`: The Slack channel where alerts should be sent. 要發送警報的 Slack 頻道。
- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token. 你的 Telegram 機器人令牌。
- `TELEGRAM_CHAT_ID`: The chat ID where Telegram alerts should be sent. 要發送 Telegram 警報的聊天 ID。
- `LINE_NOTIFY_TOKEN`: Your Line Notify token. 你的 Line Notify 令牌。
- `DISCORD_WEBHOOK_URL`: Your Discord webhook URL. 你的 Discord Webhook URL。
- `CWA_API_KEY`: Your Central Weather Administration API key. 你的中央氣象局 API 密鑰。

## Contributing | 貢獻

Feel free to submit issues or pull requests if you find any bugs or have suggestions for improvements.

如果你發現任何錯誤或有改進建議，歡迎提交問題或拉取請求。

## License | 授權

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


