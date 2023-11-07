from json import JSONDecodeError

from fastapi import HTTPException
from httpx import get, HTTPStatusError

from utils.config import DISCORD_API_ENDPOINT


def get_user(token_type: str, access_token: str, user_id: str | int = "@me") -> dict:
    try:
        response = get(
            f"{DISCORD_API_ENDPOINT}/users/{user_id}",
            headers={"Authorization": f"{token_type} {access_token}"},
        )

        response.raise_for_status()

        return response.json()

    except (JSONDecodeError, UnicodeDecodeError):
        raise HTTPException(status_code=502, detail="Discord response decoding error.")

    except HTTPStatusError as err:
        resp_json: dict | str
        # Fix it later.
        try:
            resp_json = err.response.json()
        except JSONDecodeError:
            resp_json = err.response.text

        raise HTTPException(err.response.status_code, detail=resp_json)
