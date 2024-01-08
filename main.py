import sys

from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QFileDialog
from random import choice


class Gallows(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.alf = {}
        self.file = QFileDialog.getOpenFileName(self, 'Выберите файл с словами', '')[0]
        self.s_word, self.them = choice(open(self.file, 'r', encoding='utf8').read().split()).split(',')
        self.sec_word = self.s_word
        self.setWindowTitle('Gallows')
        self.resize(800, 800)
        self.color = QColor(0, 0, 0)
        self.secret_word = QLabel(self)
        self.secret_word.setFont(QFont('Times', 30))
        self.secret_word.setText("_ " * (len(self.s_word) - 1) + "_")
        self.secret_word.move(400, 100)
        self.secret_word.resize(500, 50)
        self.res = QPushButton(self, text='Заново')
        self.res.clicked.connect(self.restart)
        self.res.resize(110, 40)
        self.res.move(660, 590)
        self.result = QLabel(self)
        self.result.setFont(QFont('Times', 30))
        self.result.move(30, 570)
        self.result.resize(650, 50)
        self.result_word = QLabel(self)
        self.result_word.setFont(QFont('Times', 30))
        self.result_word.move(30, 520)
        self.result_word.resize(650, 50)
        self.mis = QLabel(self, text='Ошибки:')
        self.mis.setFont(QFont('Times', 30))
        self.mis.resize(650, 50)
        self.mis.move(30, 470)
        self.theme = QLabel(self)
        self.theme.setText(f'Тема: {self.them}')
        self.theme.resize(500, 50)
        self.theme.move(400, 50)
        self.theme.setFont(QFont('Times', 30))
        self.count = 0
        count = 0
        height = 640
        for i in range(ord('а'), ord('я') + 1):
            count += 1
            letter = QPushButton(self, text=(chr(i)))
            letter.clicked.connect(self.select_letter)
            letter.resize((800 - 30 * 12) // 11, (800 - 30 * 12) // 11)
            letter.move(30 * count + (800 - 30 * 12) // 11 * (count - 1), height)
            self.alf[chr(i)] = letter
            if chr(i) == 'е':
                count += 1
                letter = QPushButton(self, text='ё')
                letter.clicked.connect(self.select_letter)
                letter.resize((800 - 30 * 12) // 11, (800 - 30 * 12) // 11)
                letter.move(30 * count + (800 - 30 * 12) // 11 * (count - 1), height)
                self.alf['ё'] = letter
            if count == 11:
                height += 50
                count = 0

    def paintEvent(self, e):
        self.painter = QPainter()
        self.painter.begin(self)
        self.painter.setPen(self.color)
        if self.count > 0:
            self.painter.drawLine(30, 400, 230, 400)
        if self.count > 1:
            self.painter.drawLine(80, 400, 80, 100)
        if self.count > 2:
            self.painter.drawLine(50, 100, 220, 100)
        if self.count > 3:
            self.painter.drawLine(80, 130, 110, 100)
        if self.count > 4:
            self.painter.drawEllipse(195, 150, 50, 50)
        if self.count > 5:
            self.painter.drawLine(220, 200, 220, 280)
        if self.count > 6:
            self.painter.drawLine(200, 250, 220, 200)
            self.painter.drawLine(240, 250, 220, 200)
        if self.count > 7:
            self.painter.drawLine(200, 340, 220, 280)
            self.painter.drawLine(240, 340, 220, 280)
        if self.count > 8:
            self.painter.drawLine(220, 100, 220, 150)
        self.painter.end()

    def select_letter(self):
        letter = self.sender()
        text = self.secret_word.text()
        if letter.text() in self.s_word:
            while letter.text() in self.s_word:
                index = self.s_word.index(letter.text())
                self.s_word = self.s_word[:index] + '_' + self.s_word[index + 1:]
                text = text[:index * 2] + letter.text() + text[index * 2 + 1:]
            self.secret_word.setText(text)
        else:
            self.mis.setText(f'{self.mis.text()} {letter.text()}')
            self.count += 1
            self.update()
        letter.hide()
        if '_' not in self.secret_word.text():
            self.result.setText("Вы победили, нажмите 'Заново'.")
            for i in self.alf.keys():
                self.alf[i].setEnabled(False)
        elif self.count == 9:
            for i in self.alf.keys():
                self.alf[i].setEnabled(False)
            self.result.setText("Вы проиграли, нажмите 'Заново'.")
            self.result_word.setText(f"Загаданное слово - '{self.sec_word}'")

    def restart(self):
        for i in self.alf.keys():
            self.alf[i].show()
            self.alf[i].setEnabled(True)
        self.s_word, self.them = choice(open(self.file, 'r', encoding='utf8').read().split()).split(',')
        self.sec_word = self.s_word
        self.secret_word.setText("_ " * (len(self.s_word) - 1) + "_")
        self.secret_word.setFont(QFont('Times', 30))
        self.result.setText('')
        self.result_word.setText('')
        self.mis.setText('Ошибки:')
        self.theme.setText(f'Тема: {self.them}')
        self.count = 0
        self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Gallows()
    window.show()
    sys.exit(app.exec_())
