import json


class JSONFile:
    def __init__(self, path):
        self.path = path

    def read(self):
        try:
            with open(self.path, "r") as f:
                try:
                    result = json.load(f)
                    return result
                except json.JSONDecodeError:
                    return None
        except FileNotFoundError:
            return None

    def write(self, data):
        if data is None:
            return False

        with open(self.path, "w") as f:
            json.dump(data, f, indent=4)
            return True
