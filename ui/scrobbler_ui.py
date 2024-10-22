# scrobbler_ui.py

from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(300, 500)  # Ajuste no tamanho para acomodar os novos campos
        MainWindow.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
            }
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #388e3c;
            }
            QPushButton:disabled {
                background-color: #999;
            }
            QLabel {
                font-size: 14px;
                color: #333;
            }
            QProgressBar {
                border: 1px solid #999;
                border-radius: 5px;
                text-align: center;
            }
        """)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Layout principal vertical
        self.main_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(5)

        # Layout do usuário
        username_layout = QtWidgets.QHBoxLayout()
        username_layout.setSpacing(5)
        self.usernameLabel = QtWidgets.QLabel("Usuário")
        self.usernameInput = QtWidgets.QLineEdit()
        self.usernameInput.setPlaceholderText("Coloque aqui seu usuário")
        username_layout.addWidget(self.usernameLabel)
        username_layout.addWidget(self.usernameInput)
        self.main_layout.addLayout(username_layout)

        # Layout da senha
        password_layout = QtWidgets.QHBoxLayout()
        password_layout.setSpacing(5)
        self.passwordLabel = QtWidgets.QLabel("Senha")
        self.passwordInput = QtWidgets.QLineEdit()
        self.passwordInput.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordInput.setPlaceholderText("Coloque aqui sua senha")
        password_layout.addWidget(self.passwordLabel)
        password_layout.addWidget(self.passwordInput)
        self.main_layout.addLayout(password_layout)

        # Campos para API Key e API Secret
        api_key_layout = QtWidgets.QHBoxLayout()
        api_key_layout.setSpacing(5)
        self.apiKeyLabel = QtWidgets.QLabel("API Key")
        self.apiKeyInput = QtWidgets.QLineEdit()
        self.apiKeyInput.setPlaceholderText("Coloque sua API Key")
        api_key_layout.addWidget(self.apiKeyLabel)
        api_key_layout.addWidget(self.apiKeyInput)
        self.main_layout.addLayout(api_key_layout)

        api_secret_layout = QtWidgets.QHBoxLayout()
        api_secret_layout.setSpacing(5)
        self.apiSecretLabel = QtWidgets.QLabel("API Secret")
        self.apiSecretInput = QtWidgets.QLineEdit()
        self.apiSecretInput.setPlaceholderText("Coloque seu API Secret")
        api_secret_layout.addWidget(self.apiSecretLabel)
        api_secret_layout.addWidget(self.apiSecretInput)
        self.main_layout.addLayout(api_secret_layout)

        # Link para gerar as credenciais
        self.apiLinkLabel = QtWidgets.QLabel()
        self.apiLinkLabel.setText('<a href="https://www.last.fm/api/account/create">Clique aqui para gerar suas credenciais de API</a>')
        self.apiLinkLabel.setOpenExternalLinks(True)
        self.main_layout.addWidget(self.apiLinkLabel)

        # Botão de login
        self.loginButton = QtWidgets.QPushButton("Login")
        self.loginButton.setFixedHeight(30)
        self.main_layout.addWidget(self.loginButton, alignment=QtCore.Qt.AlignCenter)

        # Linha separadora
        separator = QtWidgets.QFrame()
        separator.setFrameShape(QtWidgets.QFrame.HLine)
        separator.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.main_layout.addWidget(separator)

        # Layout do artista
        artist_layout = QtWidgets.QHBoxLayout()
        artist_layout.setSpacing(5)
        self.artistLabel = QtWidgets.QLabel("Artista")
        self.artistInput = QtWidgets.QLineEdit()
        self.artistInput.setPlaceholderText("Coloque aqui o nome do artista")
        artist_layout.addWidget(self.artistLabel)
        artist_layout.addWidget(self.artistInput)
        self.main_layout.addLayout(artist_layout)

        # Layout da música
        song_layout = QtWidgets.QHBoxLayout()
        song_layout.setSpacing(5)
        self.songLabel = QtWidgets.QLabel("Música")
        self.songInput = QtWidgets.QLineEdit()
        self.songInput.setPlaceholderText("Coloque aqui o nome da música")
        song_layout.addWidget(self.songLabel)
        song_layout.addWidget(self.songInput)
        self.main_layout.addLayout(song_layout)

        # Layout da quantidade
        quantity_layout = QtWidgets.QHBoxLayout()
        quantity_layout.setSpacing(5)
        self.quantityLabel = QtWidgets.QLabel("Quantidade")
        self.quantityInput = QtWidgets.QLineEdit()
        self.quantityInput.setPlaceholderText("Coloque aqui a quantidade de scrobbles")
        int_validator = QtGui.QIntValidator(1, 9999)
        self.quantityInput.setValidator(int_validator)
        quantity_layout.addWidget(self.quantityLabel)
        quantity_layout.addWidget(self.quantityInput)
        self.main_layout.addLayout(quantity_layout)

        # Layout horizontal para os botões Scrobblar e Modo
        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_layout.setSpacing(5)
        self.scrobbleButton = QtWidgets.QPushButton("Scrobblar")
        self.scrobbleButton.setFixedHeight(30)
        self.modeToggle = QtWidgets.QPushButton("Scrobble por Álbum")
        self.modeToggle.setCheckable(True)
        self.modeToggle.setFixedHeight(30)
        buttons_layout.addWidget(self.scrobbleButton)
        buttons_layout.addWidget(self.modeToggle)
        self.main_layout.addLayout(buttons_layout)

        # Barra de progresso
        self.progressBar = QtWidgets.QProgressBar()
        self.progressBar.setMaximum(100)
        self.progressBar.setValue(0)
        self.main_layout.addWidget(self.progressBar)

        # Botões de Pausar e Cancelar
        control_buttons_layout = QtWidgets.QHBoxLayout()
        control_buttons_layout.setSpacing(5)
        self.pauseButton = QtWidgets.QPushButton("Pausar")
        self.pauseButton.setFixedHeight(30)
        self.pauseButton.setVisible(False)
        self.cancelButton = QtWidgets.QPushButton("Cancelar")
        self.cancelButton.setFixedHeight(30)
        self.cancelButton.setVisible(False)
        control_buttons_layout.addWidget(self.pauseButton)
        control_buttons_layout.addWidget(self.cancelButton)
        self.main_layout.addLayout(control_buttons_layout)

        # Status label
        self.statusLabel = QtWidgets.QLabel("Vai scrobblar hoje, chefe?")
        self.statusLabel.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.statusLabel.setWordWrap(True)
        self.statusLabel.setStyleSheet("font-weight: bold; color: #333333;font-size: 10px;")
        self.main_layout.addWidget(self.statusLabel)

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle("Fazendo coisas erradas")
