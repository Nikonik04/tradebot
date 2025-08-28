import requests

def trade_with_bonkbot(action, contract, amount, cfg):
    """
    action: "buy" или "sell"
    """
    if not cfg['bonkbot']['enabled']:
        return {"status": "disabled"}

    url = cfg['bonkbot']['api_url']
    payload = {
        "action": action,
        "contract": contract,
        "amount": amount
    }
    headers = {"Authorization": f"Bearer {cfg['bonkbot']['api_key']}"}
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=10)
        return r.json()
    except Exception as e:
        return {"status": f"error: {e}"}
