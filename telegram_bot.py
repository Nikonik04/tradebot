import requests

def send_telegram_message(msg, cfg):
    token = cfg['telegram']['bot_token']
    chat_id = cfg['telegram']['chat_id']
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        requests.post(url, json={"chat_id": chat_id, "text": msg})
    except:
        pass
