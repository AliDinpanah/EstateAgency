import yaml
import base64
from cryptography.fernet import Fernet

from fastapi import HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader
from fastapi.security.oauth2 import OAuth2AuthorizationCodeBearer

config = yaml.safe_load(open("./data/config.yaml"))

if "encryption_key" not in config:
    key = Fernet.generate_key()
    config["encryption_key"] = key
    with open("./data/config.yaml", "w") as f:
        yaml.dump(config, f)

cipher_suite = Fernet(config['encryption_key'])

token_header = APIKeyHeader(name="X-Auth-Token", auto_error=False)


async def check_token(api_key_header: str = Security(token_header)):
    if api_key_header is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API Key"
        )
    if not (await verify_phone_token(api_key_header)):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate phone cookie"
        )
    
    phone, role = api_key_header.split(":")[1].split("-")
    return {"phone": phone, "role": role}


async def generate_phone_token(phone: str) -> str:
    encrypted_phone = cipher_suite.encrypt(phone.encode())
    encoded_phone = base64.urlsafe_b64encode(encrypted_phone).decode('utf-8')
    return f"{encoded_phone}:{phone}"


async def verify_phone_token(cookie_value: str) -> str:
    encoded_phone, phone = cookie_value.split(":")
    encrypted_phone = base64.urlsafe_b64decode(encoded_phone)
    decrypted_phone = cipher_suite.decrypt(encrypted_phone).decode('utf-8')
    if decrypted_phone != phone:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate phone cookie"
        )
    return phone

