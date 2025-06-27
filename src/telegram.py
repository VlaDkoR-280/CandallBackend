import hashlib
import hmac
import urllib.parse as urparse
from init_data_py import InitData
from init_data_py.types import User

async def validate_telegram_data(initData: str, bot_token: str) -> InitData | None:
    try:
        init_data = InitData.parse(initData)
    except:
        return None
    return init_data if init_data.validate(bot_token) else None
    
    # parsed = {k: v[0] for k, v in urparse.parse_qs(initData, strict_parsing=True).items()}
    # hash_from_telegram = parsed.pop('hash', None)

    # if not hash_from_telegram:
    #     return False
    
    # data_check_string = "\n".join(
    #     [f"{k}={v}" for k, v in sorted(parsed.items())]
    # )
    # secret_key = hashlib.sha256(bot_token.encode()).digest()
    # hmac_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
    
    # return hmac_hash == hash_from_telegram




async def parseInitData(initData: str) -> InitData:
    return []