# utils.py

import pylast
import configparser
import os

API_KEY = ""
API_SECRET = ""
SCROBBLE_LIMIT = 3000

def autenticar(username: str, password_hash: str):
    try:
        network = pylast.LastFMNetwork(
            api_key=API_KEY,
            api_secret=API_SECRET,
            username=username,
            password_hash=password_hash
        )
        network.get_authenticated_user()
        return network
    except pylast.WSError as e:
        print(f"Erro de autenticação: {e}")
        return None

def verificar_artista_musica(network, artista: str, musica: str) -> bool:
    try:
        track = network.get_track(artista, musica)
        return track is not None
    except pylast.WSError as e:
        print(f"Erro ao verificar artista ou música: {e}")
        return False

def save_credentials(username, password_hash):
    config = configparser.ConfigParser()
    config['Credentials'] = {
        'username': username,
        'password_hash': password_hash
    }
    with open('credentials.ini', 'w') as configfile:
        config.write(configfile)

def load_credentials():
    config = configparser.ConfigParser()
    if os.path.exists('credentials.ini'):
        config.read('credentials.ini')
        if 'Credentials' in config:
            username = config['Credentials'].get('username')
            password_hash = config['Credentials'].get('password_hash')
            return username, password_hash
    return None, None

def remove_credentials():
    if os.path.exists('credentials.ini'):
        os.remove('credentials.ini')
