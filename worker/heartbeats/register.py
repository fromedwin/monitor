import requests
import datetime

async def register(url, secret_key):
    
    # Register function send to the server details about how to access it (url, username, password).
    # It receive back its unique identifier and store it within the .env file.
    SERVER_REGISTER_URL = f'{url}/clients/register/{secret_key}/'

    # Send registration request to SERVER_URL and receive worker's identifier (uuid)
    print(f'Register server at {SERVER_REGISTER_URL}')
    try:
        response = requests.get(SERVER_REGISTER_URL)
        response.raise_for_status()

        json = response.json()
        return json["uuid"]
    except Exception as err:
        raise Exception(f"[{datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')}]: {err}")
