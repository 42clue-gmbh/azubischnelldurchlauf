import json
import requests
from azubi_schnelldurchlauf import settings
from threading import Thread
import time

import influxdb_client
from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS
from urllib3 import Retry

class Temperaturmonitor:
    def _safe_data(self, point: Point) -> None:
        retries = Retry(connect=10, read=5, redirect=10)
        dbclient = influxdb_client.InfluxDBClient(
            url=settings.influx_url, org=settings.influx_org, token=settings.influx_token, retries=retries
        )

        write_api = dbclient.write_api(write_options=SYNCHRONOUS)
        try:
            write_api.write(bucket=settings.influx_bucket, record=point)
        except Exception as e:
            print(e)
        write_api.close()
        dbclient.close()

    def _run(self) -> None:
        while True:
            try:
                response = requests.get("http://127.0.0.1:5000/temperatur")
            except Exception:
                continue

            response.raise_for_status()
            p = Point("Temperatur")
            text = json.loads(response.text)
            for entry in text:
                p.field("temperatur", text[entry])
                p.tag("name", entry)
                self._safe_data(p)
                
            time.sleep(1)


    def run(self) -> None:
        thread = Thread(target=self._run)
        thread.start()
        thread.join()
