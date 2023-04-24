from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget,
                             QCheckBox, QFormLayout, QLineEdit, QHBoxLayout, QWidget, QTextBrowser, QGridLayout,
                             QTextEdit, QMessageBox)
import sys
from PyQt5.uic.properties import QtGui
import lamport
import maths
from random import randint
# from sender import SenderWindow
import goldwasser

class RecipientWindow(QMainWindow):
    secretkey_cypher: tuple
    openkey_cypher: tuple
    openkey_sign: list
    sender: object
    mess_encrypted: list
    mess_encrypted_sign: int
    sign: list
    label_openkey: QLabel; label_openkey_text: QLabel
    button_gen: QPushButton; button_sendkey: QPushButton; button_checksign: QPushButton
    textfield: QTextBrowser
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Получатель")
        self.setGeometry(200, 580, 900, 350)
        self.configure_labels()
        self.configure_buttons()
        self.configure_layouts()

    def pass_window(self, sender):
        self.sender = sender

    @pyqtSlot()
    def on_gen(self):
        open_key = goldwasser.generate_key()
        self.label_openkey_text.setText(str(open_key['pub']))
        self.openkey_cypher = open_key['pub']
        print(f"Сгенерирован открытый ключ получателя (открытый ключ для шифрования [p, q]):\n{str(open_key['pub'])}")
        self.secretkey_cypher = open_key['priv']
        print(f"Сгенерирован закрытый ключ отправителя (закрытый ключ для шифрования [n, y]):\n{str(open_key['priv'])}")
        self.button_sendkey.setEnabled(True)
        return open_key

    @pyqtSlot()
    def on_send(self):
        self.sender.label_openkey_text.setText(str(self.openkey_cypher))
        self.sender.openkey_sender = self.openkey_cypher
        self.sender.val_Changed.emit()

    @pyqtSlot()
    def on_check_sign(self):
        if lamport.verify(self.sign, self.mess_encrypted_sign, self.openkey_sign):
            original_message = goldwasser.decode_cypher(self.mess_encrypted, self.secretkey_cypher)
            self.textfield.setPlainText(original_message)
            QMessageBox.about(self, "Проверка прошла успешно", "Подпись верна!")
        else:
            QMessageBox.about(self, "Проверка прошла успешно", "Подпись неверна")

    def configure_labels(self):
        self.label_openkey = QLabel('Открытый ключ для текста')
        self.label_openkey_text = QLabel('')
        self.textfield = QTextBrowser()

    def configure_buttons(self):
        self.button_gen = QPushButton('Сгенерировать ключи', self)
        self.button_gen.clicked.connect(self.on_gen)
        self.button_sendkey = QPushButton('Отправить открытый ключ', self)
        self.button_sendkey.clicked.connect(self.on_send)
        self.button_checksign = QPushButton('Проверить подпись и расшифровать', self)
        self.button_checksign.clicked.connect(self.on_check_sign)
        self.button_checksign.setEnabled(False)
        self.button_sendkey.setEnabled(False)

    def configure_layouts(self):
        main = QVBoxLayout()
        qhbox = QHBoxLayout()
        keys = QVBoxLayout()
        actions = QVBoxLayout()
        actions.addWidget(self.button_gen)
        actions.addWidget(self.button_sendkey)
        actions.addWidget(self.button_checksign)
        actions.addStretch(1)
        keys.addWidget(self.label_openkey)
        keys.addWidget(self.label_openkey_text)
        keys.addStretch(1)
        qhbox.addLayout(keys)
        qhbox.addLayout(actions)
        main.addLayout(qhbox)
        main.addWidget(self.textfield)
        widget = QWidget()
        widget.setLayout(main)
        self.setCentralWidget(widget)

