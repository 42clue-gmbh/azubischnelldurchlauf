from pathlib import Path

import yaml


class _Settings:
    def __init__(self, data):
        self.influx_token = data["influx_token"]
        self.influx_org = data["influx_org"]
        self.influx_bucket = data["influx_bucket"]
        self.influx_url = data["influx_url"]

__version__ = "2024.7.0"

root_dir = Path(__file__).parent.parent.resolve()
conf_dir = root_dir.joinpath("conf")

settings = _Settings(yaml.safe_load(conf_dir.joinpath("settings.yaml").read_text()))