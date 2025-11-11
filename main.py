import asyncio
import json
import boto3
import random
import datetime

class Sensor:
    def __init__(self, name, lat, lon, interval_ms):
        self.name = name
        self.lat = lat
        self.lon = lon
        self.interval = interval_ms / 1000.0  

    def generate_data(self):
        value = round(random.uniform(10, 100), 2)
        return {
            "sensor_type": self.name,
            "value": value,
            "latitude": self.lat,
            "longitude": self.lon,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }

async def send_data(sensor, queue_url, sqs_client):
    while True:
        data = sensor.generate_data()
        sqs_client.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(data)
        )
        print(f"Sent from {sensor.name}: {data}")
        await asyncio.sleep(sensor.interval)

async def main():
    with open("config.json") as f:
        config = json.load(f)

    sqs = boto3.client("sqs", region_name=config["aws_region"])
    lat, lon = config["location"]["latitude"], config["location"]["longitude"]

    sensors = [
        Sensor(config['sensors']['temperature'], lat, lon, config["sensors"]["temperature"]["interval_ms"]),
        Sensor(config['sensors']['humidity'], lat, lon, config["sensors"]["humidity"]["interval_ms"]),
        Sensor(config['sensors']['light'], lat, lon, config["sensors"]["light"]["interval_ms"])
    ]

    tasks = [asyncio.create_task(send_data(s, config["queue_url"], sqs)) for s in sensors]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
