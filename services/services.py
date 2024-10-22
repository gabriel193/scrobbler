# services.py

import pylast

class LastFMService:
    def __init__(self):
        self.network = None
        self.username = None
        self.password_hash = None
        self.api_key = None
        self.api_secret = None

    def authenticate(self, username, password, api_key, api_secret):
        self.username = username
        self.password_hash = pylast.md5(password)
        self.api_key = api_key
        self.api_secret = api_secret
        return self._connect()

    def authenticate_with_password_hash(self, username, password_hash, api_key, api_secret):
        self.username = username
        self.password_hash = password_hash
        self.api_key = api_key
        self.api_secret = api_secret
        return self._connect()

    def _connect(self):
        try:
            self.network = pylast.LastFMNetwork(
                api_key=self.api_key,
                api_secret=self.api_secret,
                username=self.username,
                password_hash=self.password_hash
            )
            # Verifica se a autenticação foi bem-sucedida
            self.network.get_authenticated_user()
            return True
        except pylast.WSError as e:
            print(f"Erro de autenticação: {e}")
            return False
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            return False
