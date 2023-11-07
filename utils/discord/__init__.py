from urllib.parse import urlencode

from httpx import post, get
from utils import config


HEADERS = {"Content-Type": "application/x-www-form-urlencoded"}
SCOPES = "identify"


def exchange_code(code: str) -> dict:
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": config.REDIRECT_URI,
    }
    r = post(
        "%s/oauth2/token" % config.DISCORD_API_ENDPOINT,
        data=data,
        headers=HEADERS,
        auth=(config.CLIENT_ID, config.CLIENT_SECRET),
    )
    r.raise_for_status()
    return r.json()


def refresh_token(token: str) -> dict:
    data = {"grant_type": "refresh_token", "refresh_token": token}

    r = post(
        "%s/oauth2/token" % config.DISCORD_API_ENDPOINT,
        data=data,
        headers=HEADERS,
        auth=(config.CLIENT_ID, config.CLIENT_SECRET),
    )
    r.raise_for_status()
    return r.json()


def revoke_access_token(access_token: str):
    data = {"token": access_token, "token_type_hint": "access_token"}
    post(
        "%s/oauth2/token/revoke" % config.DISCORD_API_ENDPOINT,
        data=data,
        headers=HEADERS,
        auth=(config.CLIENT_ID, config.CLIENT_SECRET),
    )


def get_token() -> dict:
    data = {"grant_type": "client_credentials", "scope": SCOPES}
    r = post(
        "%s/oauth2/token" % config.DISCORD_API_ENDPOINT,
        data=data,
        headers=HEADERS,
        auth=(config.CLIENT_ID, config.CLIENT_SECRET),
    )
    r.raise_for_status()
    return r.json()


def get_auth_url() -> str:
    data = {
        "client_id": config.CLIENT_ID,
        "response_type": "code",
        "scope": SCOPES,
        "redirect_uri": config.REDIRECT_URI,
    }

    return f"https://discord.com/api/oauth2/authorize?{urlencode(data)}"
