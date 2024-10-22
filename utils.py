# utils.py

import os
import sys
import subprocess
import requests

GITHUB_REPO = "gabriel193/scrobbler"

def check_for_updates():
    current_version = get_current_version()
    latest_version = get_latest_version()
    if latest_version and latest_version != current_version:
        return True, latest_version
    return False, None

def get_current_version():
    return "v1.0.0"

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
    if os.path.exists(".git"):
        subprocess.run(["git", "pull"])
    else:
        subprocess.run(["git", "clone", f"https://github.com/{GITHUB_REPO}.git", "."])
