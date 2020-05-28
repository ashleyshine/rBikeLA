import json


CLIENT_PATH = '../config/client'

def get_client_credentials():
    with open(CLIENT_PATH, 'r') as f:
        return json.loads(f.read())
