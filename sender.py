from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget,
                             QCheckBox, QFormLayout, QLineEdit, QHBoxLayout, QWidget, QTextBrowser, QGridLayout,
                             QTextEdit)
import sys
from PyQt5.uic.properties import QtGui
import lamport
import maths
from random import randint
from recipient import RecipientWindow
import goldwasser

class SenderWindow(QMainWindow):
    secretkey_sign: list
    openkey_sign: list
    sign: list
    openkey_sender: tuple
    mess_encrypted: list
    mess_encrypted_sign: str
    recipient: RecipientWindow; button_gen: QPushButton; button_sign: QPushButton; button_send: QPushButton
    a1: QLabel; label_openkey_sign: QLabel; a3: QLabel; label_openkey_text: QLabel; openkeybrowser_label: QLabel
    can_sign: bool
    val_Changed = pyqtSignal(name='valChanged')
    openkey_texter: QTextBrowser
    def __init__(self):
        super().__init__()
        self.openkey_sender = ()
        self.setWindowTitle("Отправитель")
        self.setGeometry(200, 0, 900, 350)
        self.configure_labels()
        self.configure_buttons()
        self.textfield = QTextEdit()
        self.textfield.textChanged.connect(self.on_text_changed)
        self.val_Changed.connect(self.on_text_changed)
        self.openkey_texter = QTextBrowser()
        self.openkey_texter.setMaximumHeight(100)
        self.configure_layouts()

    @pyqtSlot()
    def on_gen(self):
        secretkey_sign = lamport.generate_secret_key()
        self.openkey_sign = lamport.generate_open_key(secretkey_sign)
        open_key = ['(' + ','.join(keypair) + ')' for keypair in self.openkey_sign]
        open_key[len(open_key) // 2 - 1] += '\n'
        self.label_openkey_sign.setText(' '.join(open_key))
        self.openkey_texter.setText(' '.join(open_key))
        self.secretkey_sign = secretkey_sign
        self.can_sign = True
        self.val_Changed.emit()
        return secretkey_sign

    @pyqtSlot()
    def on_cypher_sign(self):
        int_encoded = goldwasser.int_encode_str(self.textfield.toPlainText())
        print(int_encoded)
        self.mess_encrypted, self.mess_encrypted_sign, text_for_field = goldwasser.encrypt(int_encoded,
                                                                                           self.openkey_sender)
        self.textfield.setText(text_for_field)
        self.sign = lamport.sign(message=self.mess_encrypted_sign, secretkey=self.secretkey_sign)
        self.button_send.setEnabled(True)

    @pyqtSlot()
    def on_send(self):
        self.recipient.mess_encrypted = self.mess_encrypted
        self.recipient.mess_encrypted_sign = self.mess_encrypted_sign
        self.recipient.sign = self.sign
        self.recipient.openkey_sign = self.openkey_sign
        self.recipient.textfield.setPlainText(self.textfield.toPlainText())
        self.recipient.button_checksign.setEnabled(True)

    @pyqtSlot()
    def on_text_changed(self):
        self.button_sign.setEnabled(bool(self.textfield.toPlainText())
                                    and self.can_sign
                                    and (len(self.openkey_sender) > 0))

    def pass_window(self, recipient):
        self.recipient = recipient

    def configure_buttons(self):
        self.button_gen = QPushButton('Сгенерировать ключи', self)
        self.button_gen.clicked.connect(self.on_gen)
        self.button_sign = QPushButton('Зашифровать и подписать', self)
        self.button_sign.clicked.connect(self.on_cypher_sign)
        self.button_sign.setEnabled(False)
        self.can_sign = False
        self.button_send = QPushButton('Отправить', self)
        self.button_send.clicked.connect(self.on_send)
        self.button_send.setEnabled(False)

    def configure_layouts(self):
        main = QVBoxLayout()
        qhbox = QHBoxLayout()
        keys = QVBoxLayout()
        actions = QVBoxLayout()
        grid = QGridLayout()
        # openkeyer = QVBoxLayout()
        # openkeyer.addWidget(self.openkeybrowser_label)
        # openkeyer.addWidget(self.openkey_texter)
        keys.addWidget(self.a1)
        keys.addWidget(self.openkey_texter)
        keys.addStretch(1)
        keys.addWidget(self.a3)
        keys.addWidget(self.label_openkey_text)
        keys.addStretch(1)
        actions.addWidget(self.button_gen)
        actions.addWidget(self.button_sign)
        actions.addWidget(self.button_send)
        actions.addStretch(1)
        qhbox.addLayout(keys)
        qhbox.addLayout(actions)
        widget = QWidget()
        main.addLayout(qhbox)
        main.addWidget(self.textfield)
        # grid.addLayout(main, 0, 0)
        # grid.addLayout(openkeyer, 0, 1)
        widget.setLayout(main)
        self.setCentralWidget(widget)

    def configure_labels(self):
        self.a1 = QLabel('Открытый ключ для подписи')
        self.label_openkey_sign = QLabel('')
        self.label_openkey_sign.setMinimumWidth(550)
        self.a3 = QLabel('Открытый ключ для текста')
        self.openkeybrowser_label = QLabel('Открытый ключ для подписи')
        self.label_openkey_text = QLabel('')

