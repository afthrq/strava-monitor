import time
import httpx
from app.config import (
    STRAVA_CLIENT_ID,
    STRAVA_CLIENT_SECRET,
    STRAVA_TOKEN_URL,
    STRAVA_BASE
)

# -----------------------------
# Refresh Token
# -----------------------------
async def refresh_token(user: dict):
    """
    Refresh Strava tokens for a given user.
    Updates the dict in-place.
    """

    payload = {
        "client_id": STRAVA_CLIENT_ID,
        "client_secret": STRAVA_CLIENT_SECRET,
        "grant_type": "refresh_token",
        "refresh_token": user.get("refresh_token"),
    }

    async with httpx.AsyncClient() as client:
        r = await client.post(STRAVA_TOKEN_URL, data=payload, timeout=30)
        r.raise_for_status()
        data = r.json()

    user["access_token"] = data["access_token"]
    user["refresh_token"] = data["refresh_token"]
    user["expires_at"] = data.get("expires_at", int(time.time()) + 3600)

    return user


# -----------------------------
# Fetch athlete activities
# -----------------------------
async def get_activities(access_token: str, after_ts: int | None = None, per_page: int = 50):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    params = {
        "per_page": per_page
    }

    if after_ts:
        params["after"] = int(after_ts)

    url = f"{STRAVA_BASE}/athlete/activities"

    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers=headers, params=params, timeout=30)
        r.raise_for_status()
        return r.json()
