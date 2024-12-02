import json


class StixExtractor:
    def __init__(self) -> None:
        pass

    def extract(self, bundle_path: str) -> str:
        with open(bundle_path, "r") as file:
            bundle = json.load(file)

        malwares = []
        for obj in bundle["objects"]:
            if obj["type"] == "malware":
                malwares.append(obj["name"])
        return malwares