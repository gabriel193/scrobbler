# utils.py

import json
import os
import shutil
import sys
import subprocess
import requests
from PyQt5 import QtCore

CREDENTIALS_FILE = "credentials.json"
SCROBBLE_LIMIT = 3000
GITHUB_REPO = "gabriel193/scrobbler"

def check_for_updates():
    current_version = get_current_version()
    latest_version = get_latest_version()
    if latest_version and latest_version != current_version:
        return True, latest_version
    return False, None

def get_current_version():
    return "v1.4.0"

def get_latest_version():
    url = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            latest_release = response.json()
            return latest_release["tag_name"]
    except Exception as e:
        print(f"Erro ao verificar atualizações: {e}")
    return None

def update_application():
    latest_release = get_latest_release_info()

    if not latest_release:
        print("Erro ao obter informações da última release.")
        return False

    # Pegue o link do executável da última release
    exe_url = None
    for asset in latest_release.get("assets", []):
        if asset["name"] == "Scrobbler.exe":  # Nome do executável
            exe_url = asset["browser_download_url"]
            break

    if exe_url is None:
        print("Não foi possível encontrar o executável na última release.")
        return False

    # Baixar o novo executável
    print("Baixando o novo executável...")

    new_exe_path = "Scrobbler_new.exe"
    try:
        with requests.get(exe_url, stream=True) as r:
            r.raise_for_status()  # Levantar um erro em caso de falha na requisição
            with open(new_exe_path, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
        print("Download concluído. Preparando para atualizar...")
    except requests.RequestException as e:
        print(f"Erro durante o download: {e}")
        return False
    except Exception as e:
        print(f"Ocorreu um erro ao salvar o arquivo: {e}")
        return False

    # Criar script temporário para substituir o executável após o fechamento
    temp_script = "update_temp.bat"
    old_exe_path = sys.argv[0]

    with open(temp_script, 'w') as script:
        script.write(f'''
        @echo off
        echo Aguardando o fechamento do aplicativo...
        timeout /t 3 /nobreak
        del "{old_exe_path}"
        move "Scrobbler_new.exe" "{old_exe_path}"
        start "" "{old_exe_path}"
        del "%~f0"  # Exclui o script temporário
        ''')

    # Fechar o aplicativo atual e executar o script de atualização
    subprocess.Popen([temp_script], shell=True)
    QtCore.QCoreApplication.quit()

    return True

def get_latest_release_info():
    url = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Erro ao verificar atualizações: {e}")
    return None

def save_credentials(username, password_hash, api_key, api_secret):
    credentials = {
        "username": username,
        "password_hash": password_hash,
        "api_key": api_key,
        "api_secret": api_secret
    }
    with open(CREDENTIALS_FILE, 'w') as f:
        json.dump(credentials, f)

def load_credentials():
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, 'r') as f:
            credentials = json.load(f)
            return credentials
    return None

def remove_credentials():
    if os.path.exists(CREDENTIALS_FILE):
        os.remove(CREDENTIALS_FILE)
