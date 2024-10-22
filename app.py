# app.py

import sys
import os
import threading
import pylast
from PyQt5 import QtWidgets, QtGui, QtCore
from ui.scrobbler_ui import Ui_MainWindow
from PyQt5.QtGui import QPixmap, QPainter, QPainterPath
import urllib.request

from utils import (
    save_credentials,
    load_credentials,
    remove_credentials,
    SCROBBLE_LIMIT,
    check_for_updates,
    update_application,
)

from threads import ScrobbleThread, ScrobbleThreadAlbum

class ScrobblerApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Obter o caminho base
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")
        icon_path = os.path.join(base_path, "resources", "app.ico")
        self.setWindowIcon(QtGui.QIcon(icon_path))
        self.setFixedSize(300, 500)  # Ajuste no tamanho para acomodar os novos campos
        self.network = None
        self.is_authenticated = False

        # Inicializa campos e botões
        self.ui.artistInput.setEnabled(False)
        self.ui.songInput.setEnabled(False)
        self.ui.quantityInput.setEnabled(False)
        self.ui.scrobbleButton.setEnabled(False)
        self.ui.modeToggle.setEnabled(False)

        self.ui.loginButton.clicked.connect(self.autenticar_usuario)
        self.ui.scrobbleButton.clicked.connect(self.iniciar_scrobble)
        self.ui.pauseButton.clicked.connect(self.pausar_ou_resumir_scrobble)
        self.ui.cancelButton.clicked.connect(self.cancelar_scrobble)

        # Modo padrão (False para scrobble por faixa)
        self.scrobble_by_album = False
        self.ui.modeToggle.clicked.connect(self.toggle_scrobble_mode)

        # Carrega credenciais salvas
        self.load_credentials()

        # Atualiza a interface
        self.update_interface()

        # Verificar atualizações em segundo plano
        threading.Thread(target=self.check_for_updates, daemon=True).start()

    def load_credentials(self):
        credentials = load_credentials()
        if credentials:
            username = credentials.get('username')
            password_hash = credentials.get('password_hash')
            api_key = credentials.get('api_key')
            api_secret = credentials.get('api_secret')

            self.ui.usernameInput.setText(username)
            self.ui.passwordInput.setText('')
            self.ui.apiKeyInput.setText(api_key)
            self.ui.apiSecretInput.setText(api_secret)

            self.network = self.autenticar(username, password_hash, api_key, api_secret)
            if self.network:
                self.is_authenticated = True
                self.ui.statusLabel.setText(f"<b>Vai scrobblar hoje, chefe?</b>")
                self.ui.loginButton.setEnabled(False)
                self.load_user_image()
                self.update_interface()
            else:
                self.ui.statusLabel.setText("<b>Falha na autenticação automática. Por favor, faça login novamente.</b>")
                self.is_authenticated = False
                remove_credentials()
        else:
            self.ui.statusLabel.setText("Por favor, faça login.")

    def autenticar(self, username, password_hash, api_key, api_secret):
        try:
            network = pylast.LastFMNetwork(
                api_key=api_key,
                api_secret=api_secret,
                username=username,
                password_hash=password_hash
            )
            # Verificar se o login foi bem-sucedido
            user = network.get_authenticated_user()
            return network
        except pylast.WSError as e:
            self.ui.statusLabel.setText(f"Erro de autenticação: {e}")
            return None
        except Exception as e:
            self.ui.statusLabel.setText(f"Ocorreu um erro: {e}")
            return None

    def load_user_image(self):
        user = self.network.get_authenticated_user()
        image_url = user.get_image()
        if image_url:
            try:
                data = urllib.request.urlopen(image_url).read()
                pixmap = QPixmap()
                pixmap.loadFromData(data)

                size = 32
                pixmap = pixmap.scaled(size, size, QtCore.Qt.KeepAspectRatioByExpanding, QtCore.Qt.SmoothTransformation)

                circular_pixmap = QtGui.QPixmap(size, size)
                circular_pixmap.fill(QtCore.Qt.transparent)

                painter = QPainter(circular_pixmap)
                painter.setRenderHint(QPainter.Antialiasing)
                path = QPainterPath()
                path.addEllipse(0, 0, size, size)
                painter.setClipPath(path)
                painter.drawPixmap(0, 0, pixmap)
                painter.end()

                self.ui.userImageLabel.setPixmap(circular_pixmap)
                self.ui.userImageLabel.setVisible(True)
            except Exception as e:
                print(f"Erro ao carregar a imagem do usuário: {e}")
        else:
            self.ui.userImageLabel.setVisible(False)

    def toggle_scrobble_mode(self):
        self.scrobble_by_album = self.ui.modeToggle.isChecked()
        if self.scrobble_by_album:
            self.ui.modeToggle.setText("Scrobble por Faixa")
            self.ui.songLabel.setText("Álbum")
        else:
            self.ui.modeToggle.setText("Scrobble por Álbum")
            self.ui.songLabel.setText("Música")
        self.update_interface()

    def update_interface(self):
        if self.is_authenticated:
            self.setFixedSize(300, 230)  # Ajuste o tamanho conforme necessário
            self.ui.usernameLabel.setVisible(False)
            self.ui.usernameInput.setVisible(False)
            self.ui.passwordLabel.setVisible(False)
            self.ui.passwordInput.setVisible(False)
            self.ui.apiKeyLabel.setVisible(False)
            self.ui.apiKeyInput.setVisible(False)
            self.ui.apiSecretLabel.setVisible(False)
            self.ui.apiSecretInput.setVisible(False)
            self.ui.apiLinkLabel.setVisible(False)
            self.ui.loginButton.setVisible(False)
            self.ui.modeToggle.setEnabled(True)
            self.ui.userImageLabel.setVisible(True)

            self.ui.artistInput.setEnabled(True)
            self.ui.songInput.setEnabled(True)
            self.ui.quantityInput.setEnabled(True)
            self.ui.scrobbleButton.setEnabled(True)
        else:
            self.setFixedSize(300, 380)  # Ajuste no tamanho para acomodar os campos de login
            self.ui.usernameLabel.setVisible(True)
            self.ui.usernameInput.setVisible(True)
            self.ui.passwordLabel.setVisible(True)
            self.ui.passwordInput.setVisible(True)
            self.ui.apiKeyLabel.setVisible(True)
            self.ui.apiKeyInput.setVisible(True)
            self.ui.apiSecretLabel.setVisible(True)
            self.ui.apiSecretInput.setVisible(True)
            self.ui.apiLinkLabel.setVisible(True)
            self.ui.loginButton.setVisible(True)
            self.ui.modeToggle.setEnabled(False)
            self.ui.userImageLabel.setVisible(False)

            self.ui.artistInput.setEnabled(False)
            self.ui.songInput.setEnabled(False)
            self.ui.quantityInput.setEnabled(False)
            self.ui.scrobbleButton.setEnabled(False)

    def autenticar_usuario(self):
        username = self.ui.usernameInput.text()
        password = self.ui.passwordInput.text()
        api_key = self.ui.apiKeyInput.text()
        api_secret = self.ui.apiSecretInput.text()

        if not username or not password or not api_key or not api_secret:
            self.ui.statusLabel.setText("Por favor, preencha todos os campos de login e API.")
            return

        password_hash = pylast.md5(password)
        self.network = self.autenticar(username, password_hash, api_key, api_secret)

        if self.network:
            self.is_authenticated = True
            self.ui.statusLabel.setText("<b>Autenticado com sucesso!</b>")
            self.ui.loginButton.setEnabled(False)
            save_credentials(username, password_hash, api_key, api_secret)
            self.load_user_image()
            self.update_interface()
        else:
            self.ui.statusLabel.setText("<b>Falha na autenticação. Verifique suas credenciais.</b>")
            self.is_authenticated = False

    def iniciar_scrobble(self):
        if not self.network:
            self.ui.statusLabel.setText("Autentique-se primeiro.")
            return

        artista = self.ui.artistInput.text().strip()
        musica_album = self.ui.songInput.text().strip()

        try:
            quantidade = int(self.ui.quantityInput.text())
        except ValueError:
            self.ui.statusLabel.setText("A quantidade precisa ser um número.")
            return

        if quantidade <= 0:
            self.ui.statusLabel.setText("A quantidade precisa ser maior que zero.")
            return

        if quantidade > SCROBBLE_LIMIT:
            self.ui.statusLabel.setText(f"A quantidade não pode exceder {SCROBBLE_LIMIT} scrobbles por dia.")
            return

        if self.scrobble_by_album:
            album = musica_album
            if not artista or not album:
                self.ui.statusLabel.setText("Por favor, preencha os campos de artista e álbum.")
                return

            self.ui.scrobbleButton.setEnabled(False)
            self.ui.pauseButton.setVisible(True)
            self.ui.cancelButton.setVisible(True)

            self.thread = ScrobbleThreadAlbum(self.network, artista, album, quantidade)
        else:
            musica = musica_album
            if not artista or not musica:
                self.ui.statusLabel.setText("Por favor, preencha os campos de artista e música.")
                return

            self.ui.scrobbleButton.setEnabled(False)
            self.ui.pauseButton.setVisible(True)
            self.ui.cancelButton.setVisible(True)

            self.thread = ScrobbleThread(self.network, artista, musica, quantidade)

        self.thread.progress.connect(self.atualizar_progresso)
        self.thread.finished.connect(self.finalizar_scrobble)
        self.thread.start()

    def pausar_ou_resumir_scrobble(self):
        if self.thread.paused:
            self.thread.resume()
            self.ui.pauseButton.setText("Pausar")
        else:
            self.thread.pause()
            self.ui.pauseButton.setText("Retomar")

    def cancelar_scrobble(self):
        self.thread.stop()
        self.resetar_campos()

    def atualizar_progresso(self, progresso, mensagem):
        self.ui.progressBar.setValue(progresso)
        self.ui.statusLabel.setText(f"<b>{mensagem}</b>")

    def finalizar_scrobble(self, mensagem):
        self.ui.scrobbleButton.setEnabled(True)
        self.ui.pauseButton.setVisible(False)
        self.ui.cancelButton.setVisible(False)
        self.ui.statusLabel.setText(mensagem)
        self.ui.progressBar.setValue(0)

    def resetar_campos(self):
        self.ui.artistInput.setText("")
        self.ui.songInput.setText("")
        self.ui.quantityInput.setText("")
        self.ui.statusLabel.setText("Vai scrobblar hoje, chefe?")
        self.ui.pauseButton.setVisible(False)
        self.ui.cancelButton.setVisible(False)
        self.ui.scrobbleButton.setEnabled(True)
        self.ui.progressBar.setValue(0)

    def check_for_updates(self):
        has_update, latest_version = check_for_updates()
        if has_update:
            reply = QtWidgets.QMessageBox.question(
                self,
                "Atualização Disponível",
                f"Uma nova versão ({latest_version}) está disponível. Deseja atualizar agora?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
            )
            if reply == QtWidgets.QMessageBox.Yes:
                update_application()
                QtWidgets.QMessageBox.information(
                    self,
                    "Atualização Concluída",
                    "O aplicativo será reiniciado para concluir a atualização."
                )
                QtCore.QCoreApplication.quit()
                QtCore.QProcess.startDetached(sys.executable, sys.argv)
