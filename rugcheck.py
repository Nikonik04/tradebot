import requests

def check_rugcheck(contract, cfg):
    if not cfg['rugcheck']['enabled']:
        return {"status": "Unknown", "bundle_related": False, "dev": None}

    url = f"{cfg['rugcheck']['api_url']}/{contract}"
    headers = {}
    if cfg['rugcheck']['api_key']:
        headers["Authorization"] = f"Bearer {cfg['rugcheck']['api_key']}"
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code != 200:
            return {"status": "Error", "bundle_related": False, "dev": None}
        data = r.json()
        return {
            "status": data.get("status", "Unknown"),
            "bundle_related": bool(data.get("bundle", False)),
            "dev": data.get("deployer") or data.get("owner")
        }
    except Exception:
        return {"status": "Error", "bundle_related": False, "dev": None}
