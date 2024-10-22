#scrobbler_ui.py

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(300, 350)  # Ajuste no tamanho para tornar o app mais compacto
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
        self.main_layout.setContentsMargins(10, 10, 10, 10)  # Reduz as margens superior e inferior
        self.main_layout.setSpacing(5)  # Reduz o espaçamento entre os widgets

        # Layout do usuário
        username_layout = QtWidgets.QHBoxLayout()
        username_layout.setSpacing(5)
        self.usernameLabel = QtWidgets.QLabel("Usuário")
        self.usernameInput = QtWidgets.QLineEdit()
        self.usernameInput.setPlaceholderText("Coloque aqui seu usuário")  # Texto de exemplo
        username_layout.addWidget(self.usernameLabel)
        username_layout.addWidget(self.usernameInput)
        self.main_layout.addLayout(username_layout)

        # Layout da senha
        password_layout = QtWidgets.QHBoxLayout()
        password_layout.setSpacing(5)
        self.passwordLabel = QtWidgets.QLabel("Senha")
        self.passwordInput = QtWidgets.QLineEdit()
        self.passwordInput.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordInput.setPlaceholderText("Coloque aqui sua senha")  # Texto de exemplo
        password_layout.addWidget(self.passwordLabel)
        password_layout.addWidget(self.passwordInput)
        self.main_layout.addLayout(password_layout)

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
        self.artistInput.setPlaceholderText("Coloque aqui o nome do artista")  # Texto de exemplo
        artist_layout.addWidget(self.artistLabel)
        artist_layout.addWidget(self.artistInput)
        self.main_layout.addLayout(artist_layout)

        # Layout da música
        song_layout = QtWidgets.QHBoxLayout()
        song_layout.setSpacing(5)
        self.songLabel = QtWidgets.QLabel("Música")
        self.songInput = QtWidgets.QLineEdit()
        self.songInput.setPlaceholderText("Coloque aqui o nome da música")  # Texto de exemplo
        song_layout.addWidget(self.songLabel)
        song_layout.addWidget(self.songInput)
        self.main_layout.addLayout(song_layout)

        # Layout da quantidade
        quantity_layout = QtWidgets.QHBoxLayout()
        quantity_layout.setSpacing(5)
        self.quantityLabel = QtWidgets.QLabel("Quantidade")
        self.quantityInput = QtWidgets.QLineEdit()
        self.quantityInput.setPlaceholderText("Coloque aqui a quantidade de scrobbles")  # Texto de exemplo
        
        # Configura um validador que só permite números maiores que 0
        int_validator = QtGui.QIntValidator(1, 9999)  # Limita os valores de 1 a 9999, por exemplo
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

        # Barra de progresso logo abaixo dos botões
        self.progressBar = QtWidgets.QProgressBar()
        self.progressBar.setMaximum(100)
        self.progressBar.setValue(0)
        self.main_layout.addWidget(self.progressBar)

        # Layout horizontal para a imagem do usuário e o statusLabel
        status_layout = QtWidgets.QHBoxLayout()
        status_layout.setSpacing(5)

        # Criar o userImageLabel
        self.userImageLabel = QtWidgets.QLabel()
        self.userImageLabel.setFixedSize(32, 32)
        self.userImageLabel.setVisible(False)
        status_layout.addWidget(self.userImageLabel, 0)  # Stretch fator 0 para a imagem

        # Botões de Pausar e Cancelar em um layout horizontal
        control_buttons_layout = QtWidgets.QHBoxLayout()
        control_buttons_layout.setSpacing(5)
        self.pauseButton = QtWidgets.QPushButton("Pausar")
        self.pauseButton.setFixedHeight(30)
        self.pauseButton.setVisible(False)  # Inicialmente oculto
        self.cancelButton = QtWidgets.QPushButton("Cancelar")
        self.cancelButton.setFixedHeight(30)
        self.cancelButton.setVisible(False)  # Inicialmente oculto
        control_buttons_layout.addWidget(self.pauseButton)
        control_buttons_layout.addWidget(self.cancelButton)
        self.main_layout.addLayout(control_buttons_layout)

        # Status label
        self.statusLabel = QtWidgets.QLabel("Vai scrobblar hoje, chefe?")
        self.statusLabel.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.statusLabel.setWordWrap(True)
        self.statusLabel.setStyleSheet("font-weight: bold; color: #333333;font-size: 10px;")
        status_layout.addWidget(self.statusLabel, 1)  # Stretch fator 1 para o texto

        self.main_layout.addLayout(status_layout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle("Fazendo coisas erradas")
