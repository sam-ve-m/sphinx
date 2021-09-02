import json
from datetime import datetime


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return int(obj.timestamp() * 1000)
        return json.JSONEncoder.default(self, obj)
