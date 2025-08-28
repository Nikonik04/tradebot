import yaml, time, requests
from db import init_db
from filters import is_blacklisted, detect_fake_volume
from rugcheck import check_rugcheck
from bonkbot import trade_with_bonkbot
from telegram_bot import send_telegram_message

def load_config():
    with open("config.yaml") as f:
        return yaml.safe_load(f)

def fetch_tokens():
    # пример получения токенов с dexscreener
    url = "https://api.dexscreener.com/latest/dex/tokens"
    try:
        r = requests.get(url, timeout=10)
        return r.json().get("pairs", [])
    except:
        return []

def main():
    cfg = load_config()
    conn = init_db()
    cur = conn.cursor()

    while True:
        tokens = fetch_tokens()
        for t in tokens:
            contract = t.get("pairAddress")
            name = t.get("baseToken", {}).get("name")
            symbol = t.get("baseToken", {}).get("symbol")
            volume = float(t.get("volume", {}).get("h24", 0))
            liquidity = float(t.get("liquidity", {}).get("usd", 0))
            traders = int(t.get("txns", {}).get("h24", 0))

            # rugcheck
            rc = check_rugcheck(contract, cfg)
            if rc["status"].lower() != "good":
                continue
            if rc["bundle_related"]:
                cfg['filters']['blacklist_tokens'].append(contract)
                if rc["dev"]:
                    cfg['filters']['blacklist_developers'].append(rc["dev"])
                continue

            # фильтры
            if is_blacklisted(contract, rc["dev"], cfg):
                continue
            if detect_fake_volume(volume, liquidity, traders, cfg):
                continue

            # запись
            try:
                cur.execute("INSERT INTO tokens (contract,name,symbol,status,volume,liquidity,dev) VALUES (?,?,?,?,?,?,?)",
                            (contract, name, symbol, rc["status"], volume, liquidity, rc["dev"]))
                conn.commit()
            except:
                pass

            # уведомление
            msg = f"🔥 Новый токен: {name} ({symbol})\nContract: {contract}\nLiquidity: ${liquidity}\nVolume24h: ${volume}"
            send_telegram_message(msg, cfg)

            # торговля BonkBot
            trade_res = trade_with_bonkbot("buy", contract, 10, cfg)  # пример — покупка на $10
            send_telegram_message(f"BonkBot trade: {trade_res}", cfg)

        time.sleep(60)

if __name__ == "__main__":
    main()
