def is_blacklisted(token, dev, cfg):
    if token in cfg['filters']['blacklist_tokens']:
        return True
    if dev and dev in cfg['filters']['blacklist_developers']:
        return True
    return False

def detect_fake_volume(volume, liquidity, traders, cfg):
    if not cfg['filters']['fake_volume_detection']['enabled']:
        return False
    ratio = volume / (liquidity + 1)
    if ratio > cfg['filters']['fake_volume_detection']['heuristic']['vol_to_liq_ratio']:
        return True
    if traders < cfg['filters']['fake_volume_detection']['heuristic']['min_unique_traders']:
        return True
    return False
