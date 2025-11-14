from influxdb_client import InfluxDBClient, Point, WriteOptions
from app.config import INFLUX_URL, INFLUX_TOKEN, INFLUX_ORG, INFLUX_BUCKET

client = InfluxDBClient(
    url=INFLUX_URL,
    token=INFLUX_TOKEN,
    org=INFLUX_ORG
)

write_api = client.write_api(write_options=WriteOptions(batch_size=1))

def write_activity(user, act):
    p = (
        Point("activity")
        .tag("athlete_id", str(user["athlete_id"]))
        .tag("type", act.get("type"))
        .tag("name", act.get("name"))
        .field("distance", act.get("distance", 0.0))
        .field("moving_time", act.get("moving_time", 0))
        .field("elapsed_time", act.get("elapsed_time", 0))
        .field("avg_hr", act.get("average_heartrate", 0.0))
        .field("max_hr", act.get("max_heartrate", 0.0))
        .field("elev_gain", act.get("total_elevation_gain", 0.0))
        .time(act.get("start_date"))
    )

    write_api.write(bucket=INFLUX_BUCKET, record=p)
