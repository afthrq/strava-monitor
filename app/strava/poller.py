import time
from app.utils.storage import (
    load_tokens,
    save_tokens,
    load_last_sync,
    save_last_sync
)
from app.config import TOKENS_FILE, LAST_SYNC_FILE
from app.strava.client import refresh_token, get_activities
from app.db.influx import write_activity


async def run_polling_cycle():
    tokens = load_tokens(TOKENS_FILE)
    last_sync = load_last_sync(LAST_SYNC_FILE)

    now = int(time.time())
    users = tokens.get(users, [])

    for user in users:
        name = user.get("name")
        athlete_id = str(user.get("athlete_id"))

        try:
            expires_at = int(user.get("expires_at", 0))
            if expires_at < now:
                await refresh_token(user)
            
            after_ts = last_sync.get(athlete_id, 0)
            if after_ts == 0:
                print(f"[POLLER] - No last sync, pulling latest activities")

            activities = await get_activities(
                access_token=user["access_token"],
                after_ts=after_ts
            )
            
            newest_ts = after_ts

            for act in activities:
                write_activity(user, act)

                start_date = act.get("start_date")
                if start_date:
                    from dateutil import parser
                    dt = parser.isoparse(start_date)
                    ts = int(dt.timestamp())
                    newest_ts = max(newest_ts, ts)
                
                last_sync[athlete_id] = newest_ts
        except Exception as e:
            print(f"[POLLER] ERROR for {name}: {e}")
            
    save_tokens(TOKENS_FILE, tokens)
    save_last_sync(LAST_SYNC_FILE, last_sync)


