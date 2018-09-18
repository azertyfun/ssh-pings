import time
from json import JSONEncoder

import geotool

class PingEncoder(JSONEncoder):
    def default(self, p):
        origin_location = p.origin_location()
        if origin_location is None:
            origin_location = "unknown"

        return {
            'timestamp': p.timestamp,
            'origin': origin_location
        }

class Ping():
    def __init__(self, timestamp=time.time(), origin=""):
        timestamp = int(timestamp)

        if timestamp / 1e15 < 1: # If timestamp not in µs
            self.timestamp = timestamp * 1e6
        else:
            self.timestamp = timestamp
    
        self.origin = origin

    def origin_location(self):
        if self.origin != "":
            return geotool.get_country(self.origin)
        else:
            return None

    def timestamp_seconds(self):
        return int(self.timestamp / 1e6)
    
