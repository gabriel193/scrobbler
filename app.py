# app.py

import sys
import os
import pylast
from PyQt5 import QtWidgets, QtGui, QtCore
from ui.scrobbler_ui import Ui_MainWindow
from PyQt5.QtGui import QPixmap, QPainter, QPainterPath
import urllib.request

from utils import (
    autenticar,
    verificar_artista_musica,
    save_credentials,
    load_credentials,
    remove_credentials,
    SCROBBLE_LIMIT
)
from threads import ScrobbleThread, ScrobbleThreadAlbum

class ScrobblerApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Obter o caminho base
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")
        icon_path = os.path.join(base_path, "resources", "app.ico")
        self.setWindowIcon(QtGui.QIcon(icon_path))
        self.setFixedSize(300, 320)
        self.network = None
        self.is_authenticated = False

        # Inicializa campos e botões
        self.artistInput.setEnabled(False)
        self.songInput.setEnabled(False)
        self.quantityInput.setEnabled(False)
        self.scrobbleButton.setEnabled(False)
        self.modeToggle.setEnabled(False)

        self.loginButton.clicked.connect(self.autenticar_usuario)
        self.scrobbleButton.clicked.connect(self.iniciar_scrobble)
        self.pauseButton.clicked.connect(self.pausar_ou_resumir_scrobble)
        self.cancelButton.clicked.connect(self.cancelar_scrobble)

        # Modo padrão (False para scrobble por faixa)
        self.scrobble_by_album = False
        self.modeToggle.clicked.connect(self.toggle_scrobble_mode)

        # Carrega credenciais salvas
        self.load_credentials()

        # Atualiza a interface
        self.update_interface()

    def load_credentials(self):
        username, password_hash = load_credentials()
        if username and password_hash:
            self.usernameInput.setText(username)
            self.passwordInput.setText('')
            self.network = autenticar(username, password_hash)
            if self.network:
                self.is_authenticated = True
                self.statusLabel.setText(f"<b>Vai scrobblar hoje, chefe?</b>")
                self.loginButton.setEnabled(False)
                self.load_user_image()
                self.update_interface()
            else:
                self.statusLabel.setText("<b>Falha na autenticação automática. Por favor, faça login novamente.</b>")
                self.is_authenticated = False
                remove_credentials()
        else:
            self.statusLabel.setText("Por favor, faça login.")

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

                self.userImageLabel.setPixmap(circular_pixmap)
                self.userImageLabel.setVisible(True)
            except Exception as e:
                print(f"Erro ao carregar a imagem do usuário: {e}")
        else:
            self.userImageLabel.setVisible(False)

    def toggle_scrobble_mode(self):
        self.scrobble_by_album = self.modeToggle.isChecked()
        if self.scrobble_by_album:
            self.modeToggle.setText("Scrobble por Faixa")
        else:
            self.modeToggle.setText("Scrobble por Álbum")
        self.update_interface()

    def update_interface(self):
        if self.is_authenticated:
            self.setFixedSize(300, 230)
            self.usernameLabel.setVisible(False)
            self.usernameInput.setVisible(False)
            self.passwordLabel.setVisible(False)
            self.passwordInput.setVisible(False)
            self.loginButton.setVisible(False)
            self.modeToggle.setEnabled(True)
            self.userImageLabel.setVisible(True)
        else:
            self.setFixedSize(300, 320)
            self.usernameLabel.setVisible(True)
            self.usernameInput.setVisible(True)
            self.passwordLabel.setVisible(True)
            self.passwordInput.setVisible(True)
            self.loginButton.setVisible(True)
            self.modeToggle.setEnabled(False)
            self.userImageLabel.setVisible(False)

        if self.scrobble_by_album:
            self.songLabel.setVisible(False)
            self.songInput.setVisible(False)
            self.artistLabel.setText("Artista")
            self.songInput.setText("")
            self.songInput.setEnabled(False)

            if not hasattr(self, 'albumLabel'):
                self.albumLabel = QtWidgets.QLabel("Álbum")
                self.albumInput = QtWidgets.QLineEdit()
                self.albumInput.setPlaceholderText("Coloque aqui o nome do album")  # Texto de exemplo

                album_layout = QtWidgets.QHBoxLayout()
                album_layout.setSpacing(5)
                album_layout.addWidget(self.albumLabel)
                album_layout.addWidget(self.albumInput)
                self.main_layout.insertLayout(5, album_layout)
            else:
                self.albumLabel.setVisible(True)
                self.albumInput.setVisible(True)

            self.artistInput.setEnabled(self.is_authenticated)
            self.albumInput.setEnabled(self.is_authenticated)
            self.quantityInput.setEnabled(self.is_authenticated)
            self.scrobbleButton.setEnabled(self.is_authenticated)
        else:
            self.songLabel.setVisible(True)
            self.songInput.setVisible(True)
            self.artistLabel.setText("Artista")
            self.songInput.setEnabled(self.is_authenticated)

            if hasattr(self, 'albumLabel'):
                self.albumLabel.setVisible(False)
                self.albumInput.setVisible(False)

            self.artistInput.setEnabled(self.is_authenticated)
            self.songInput.setEnabled(self.is_authenticated)
            self.quantityInput.setEnabled(self.is_authenticated)
            self.scrobbleButton.setEnabled(self.is_authenticated)

    def autenticar_usuario(self):
        username = self.usernameInput.text()
        password = self.passwordInput.text()

        if not username or not password:
            self.statusLabel.setText("Por favor, preencha os campos de usuário e senha.")
            return

        password_hash = pylast.md5(password)
        self.network = autenticar(username, password_hash)

        if self.network:
            self.is_authenticated = True
            self.statusLabel.setText("<b>Autenticado com sucesso!</b>")
            self.loginButton.setEnabled(False)
            save_credentials(username, password_hash)
            self.load_user_image()
            self.update_interface()
        else:
            self.statusLabel.setText("<b>Falha na autenticação. Verifique suas credenciais.</b>")
            self.is_authenticated = False

    def iniciar_scrobble(self):
        if not self.network:
            self.statusLabel.setText("Autentique-se primeiro.")
            return

        artista = self.artistInput.text().strip()

        try:
            quantidade = int(self.quantityInput.text())
        except ValueError:
            self.statusLabel.setText("A quantidade precisa ser um número.")
            return

        if quantidade <= 0:
            self.statusLabel.setText("A quantidade precisa ser maior que zero.")
            return

        if quantidade > SCROBBLE_LIMIT:
            self.statusLabel.setText(f"A quantidade não pode exceder {SCROBBLE_LIMIT} scrobbles por dia.")
            return

        if self.scrobble_by_album:
            album = self.albumInput.text().strip()
            if not artista or not album:
                self.statusLabel.setText("Por favor, preencha os campos de artista e álbum.")
                return

            try:
                album_obj = self.network.get_album(artista, album)
                tracks = album_obj.get_tracks()
                if not tracks:
                    self.statusLabel.setText("Álbum não encontrado ou sem faixas disponíveis.")
                    return
            except pylast.WSError as e:
                self.statusLabel.setText(f"Erro ao obter o álbum: {e}")
                return

            self.scrobbleButton.setEnabled(False)
            self.pauseButton.setVisible(True)
            self.cancelButton.setVisible(True)

            self.thread = ScrobbleThreadAlbum(self.network, artista, album, quantidade)
        else:
            musica = self.songInput.text().strip()
            if not artista or not musica:
                self.statusLabel.setText("Por favor, preencha os campos de artista e música.")
                return

            if not verificar_artista_musica(self.network, artista, musica):
                self.statusLabel.setText("Artista ou música não encontrados. Verifique as entradas.")
                return

            self.scrobbleButton.setEnabled(False)
            self.pauseButton.setVisible(True)
            self.cancelButton.setVisible(True)

            self.thread = ScrobbleThread(self.network, artista, musica, quantidade)

        self.thread.progress.connect(self.atualizar_progresso)
        self.thread.finished.connect(self.finalizar_scrobble)
        self.thread.start()

    def pausar_ou_resumir_scrobble(self):
        if self.thread.paused:
            self.thread.resume()
            self.pauseButton.setText("Pausar")
        else:
            self.thread.pause()
            self.pauseButton.setText("Retomar")

    def cancelar_scrobble(self):
        self.thread.stop()
        self.resetar_campos()

    def atualizar_progresso(self, progresso, mensagem):
        self.progressBar.setValue(progresso)
        self.statusLabel.setText(f"<b>{mensagem}</b>")

    def finalizar_scrobble(self, mensagem):
        self.scrobbleButton.setEnabled(True)
        self.pauseButton.setVisible(False)
        self.cancelButton.setVisible(False)
        self.statusLabel.setText(mensagem)
        self.progressBar.setValue(100)

    def resetar_campos(self):
        self.artistInput.setText("")
        self.songInput.setText("")
        if hasattr(self, 'albumInput'):
            self.albumInput.setText("")
        self.quantityInput.setText("")
        self.statusLabel.setText("Vai scrobblar hoje, chefe?")
        self.pauseButton.setVisible(False)
        self.cancelButton.setVisible(False)
        self.scrobbleButton.setEnabled(True)
        self.progressBar.setValue(0)
