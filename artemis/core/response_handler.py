import jxmlease
import json


def xml_response(response: str):
    return jxmlease.parse(response)


def json_response(response: str):
    return json.loads(response)    
    
