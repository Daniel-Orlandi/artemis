import jxmlease
import json


def xml_response(response: str):
    try:
        return jxmlease.parse(response)

    except Exception:
        raise ValueError("Could not read as xml")


def json_response(response: str):
    try:
        return json.loads(response)

    except Exception:
        raise ValueError("Could not read as json")
