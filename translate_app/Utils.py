import json

class Utils(object):
    def is_json(self, data) -> bool:
        try:
            json.loads(data)
        except ValueError as err:
            return False
        return True