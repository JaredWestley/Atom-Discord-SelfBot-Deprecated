import json
import os

_config = None

def load_config(config_path: str = "config.json") -> dict:
    global _config
    if _config is None:
        with open(config_path) as f:
            _config = json.load(f)
    return _config

def get_config() -> dict:
    if _config is None:
        return load_config()
    return _config

def get_token() -> str:
    return get_config().get('token')

def get_password() -> str:
    return get_config().get('password')

def get_prefix() -> str:
    return get_config().get('prefix')

def get_giveaway_sniper() -> bool:
    return get_config().get('giveaway_sniper') == 'true' or get_config().get('giveaway_sniper') == True

def get_nitro_sniper() -> bool:
    return get_config().get('nitro_sniper') == 'true' or get_config().get('nitro_sniper') == True

def get_slotbot_sniper() -> bool:
    return get_config().get('slotbot_sniper') == 'true' or get_config().get('nitro_sniper') == True

def get_privnote_sniper() -> bool:
    return get_config().get('privnote_sniper') == 'true' or get_config().get('privnote_sniper') == True

def get_silent_mode() -> bool:
    mode = get_config().get('silent_mode')
    return mode == 'true' or mode == 'True' or mode == True

def get_stream_url() -> str:
    return get_config().get('stream')

def get_auto_delete_timeout() -> int:
    return get_config().get('auto_delete_timeout')

def get_auto_giveaway_delay() -> int:
    return get_config().get('auto_giveaway_delay')
