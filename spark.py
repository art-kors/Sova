import sys
import os
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog
from PyQt5.QtWidgets import QLabel, QLineEdit, QMainWindow
from PyQt5 import uic
from PyQt5.QtCore import *
# Import the gTTS module for text
# to speech conversion 
from gtts import gTTS
from playsound import playsound

russian_morze = {'а': '.-',
                 '': '',
                 'б': '-...',
                 'в': '.--',
                 'г': '--.',
                 'д': '-..',
                 'е': '.',
                 'ж': '...-',
                 'з': '--..',
                 'и': '..',
                 'й': '.---',
                 'к': '-.-',
                 'л': '.-..',
                 'м': '--',
                 'н': '-.',
                 'о': '---',
                 'п': '.--.',
                 'р': '.-.',
                 'с': '...',
                 'т': '-',
                 'у': '..-',
                 'ф': '..-.',
                 'х': '....',
                 'ц': '-.-.',
                 'ч': '---.',
                 'ш': '----',
                 'щ': '--.-',
                 'ы': '-.--',
                 'э': '..-..',
                 'ю': '..--',
                 'я': '.-.-',
                 '1': '.----',
                 '2': '..---',
                 '3': '...--',
                 '4': '....-',
                 '5': '.....',
                 '6': '-....',
                 '7': '--...',
                 '8': '---..',
                 '9': '----.',
                 '0': '-----',
                 ',': '.-.-.-',
                 '.': '......',
                 '?': '..--..',
                 '/': '-..-.',
                 '-': '-....-',
                 '(': '-.--.',
                 ')': '-.--.-',
                 '!': '--..--',
                 '\n': '\n',
                 'ъ': '.--.-.',
                 'ь': '-..-',
                 '': '',
                 '"': '.-..-.'
                 }
russian_demorze = {'-': 'т',
                   '--': 'м',
                   '---': 'о',
                   '----': 'ш',
                   '---.': 'ч',
                   '--.': 'г',
                   '--.-': 'щ',
                   '--..': 'з',
                   '-.': 'н',
                   '-.-': 'к',
                   '-.--': 'ы',
                   '-.-.': 'ц',
                   '-..': 'д',
                   '-...': 'б',
                   '.': 'е',
                   '.-': 'а',
                   '.--': 'в',
                   '.---': 'й',
                   '.--.': 'п',
                   '.-.': 'р',
                   '.-.-': 'я',
                   '.-..': 'л',
                   '..': 'и',
                   '..-': 'у',
                   '..--': 'ю',
                   '..-.': 'ф',
                   '..-..': 'э',
                   '...': 'с',
                   '...-': 'ж',
                   '....': 'х',
                   '-----': '0',
                   '----.': '9',
                   '---..': '8',
                   '--..--': '!',
                   '--...': '7',
                   '-.--.': '(',
                   '-.--.-': ')',
                   '-..-.': '/',
                   '-....': '6',
                   '-....-': '-',
                   '.----': '1',
                   '.-.-.-': '.',
                   '..---': '2',
                   '..--..': '?',
                   '...--': '3',
                   '....-': '4',
                   '.....': '5',
                   '\n': '\n',
                   '.--.-.': 'ъ',
                   '.-.-.-': ',',
                   '......': '.',
                   '.-..-.': '"',
                   }
morze = {'a': '.-',
         'b': '-...',
         'c': '-.-.',
         '\n': '\n',
         'd': '-..',
         'e': '.',
         'f': '..-.',
         'g': '--.',
         'h': '....',
         'i': '..',
         'j': '.---',
         'k': '-.-',
         'l': '.-..',
         'm': '--',
         'n': '-.',
         'o': '---',
         'p': '.--.',
         'q': '--.-',
         'r': '.-.',
         's': '...',
         't': '-',
         'u': '..-',
         'v': '...-',
         'w': '.--',
         'x': '-..-',
         'y': '-.--',
         'z': '--..',
         '1': '.----',
         '2': '..---',
         '3': '...--',
         '4': '....-',
         '5': '.....',
         '6': '-....',
         '7': '--...',
         '8': '---..',
         '9': '----.',
         '0': '-----',
         ',': '.-.-.-',
         '.': '......',
         '?': '..--..',
         '/': '-..-.',
         '-': '-....-',
         '(': '-.--.',
         ')': '-.--.-',
         '!': '--..--',
         '\n': '\n',
         '': '',
         '"': '.-..-.'
         }
demorze = {'-': 't',
         '--': 'm',
         '---': 'o',
         '-----': '0',
         '\n': '\n',
         '': '',
         '----.': '9',
         '---..': '8',
         '--.': 'g',
         '--.-': 'q',
         '--..': 'z',
         '--..--': '!',
         '--...': '7',
         '-.': 'n',
         '-.-': 'k',
         '-.--': 'y',
         '-.--.': '(',
         '-.--.-': ')',
         '-.-.': 'c',
         '-..': 'd',
         '-..-': 'x',
         '-..-.': '/',
         '-...': 'b',
         '-....': '6',
         '-....-': '-',
         '.': 'e',
         '.-': 'a',
         '.--': 'w',
         '.---': 'j',
         '.----': '1',
         '.--.': 'p',
         '.-.': 'r',
         '.-.-.-': '.',
         '.-..': 'l',
         '..': 'i',
         '..-': 'u',
         '..---': '2',
         '..--..': '?',
         '..-.': 'f',
         '...': 's',
         '...-': 'v',
         '...--': '3',
         '....': 'h',
         '....-': '4',
         '.....': '5',
         '\n': '\n',
         '.-.-.-': ',',
         '......': '.',
         '.-..-.': '"'
           }
japan_name_letters = {
    'А': 'ка',
    'И': 'ки',
    'Р': 'ши',
    'Ш': 'ли',
    'Б': 'зу',
    'Й': 'фу',
    'С': 'ари',
    'Щ': 'ни',
    'В': 'ру',
    'К': 'ме',
    'Т': 'чи',
    'Ъ': 'д',
    'Г': 'джи',
    'Л': 'та',
    'У': 'мей',
    'Ы': 'хе',
    'Д': 'те',
    'М': 'рин',
    'Ф': 'лу',
    'Ь': 'ксе',
    'Е': 'ку',
    'Ё': 'ку',
    'Н': 'то',
    'Х': 'ри',
    'Э': 'га',
    'Ж': 'зу',
    'О': 'мо',
    'Ц': 'ми',
    'Ю': 'до',
    'З': 'з',
    'П': 'но',
    'Ч': 'зи',
    'Я': 'ма',
    '': '',
    ' ': ' '}


def japan_name(name):
    res = ''
    for i in name.upper():
        res += japan_name_letters[i]
    res = res.capitalize()
    return res


def encode_to_morse(message):
    # декодер
    cipher = ''
    message = message.lower()
    for letter in message:
        if letter != ' ':
            try:
                cipher += morze[letter] + ' '
            except KeyError:
                cipher += 'Неопределенный символ'
        else:
            cipher += ' '
    return cipher
    


def decode_to_morse(message):
    message += ' '
 
    decipher = ''
    citext = ''
    i = 0
    for letter in message:
 
        # checks for space
        if (letter != ' '):
 
            # counter to keep track of space
            i = 0
 
            # storing morse code of a single character
            citext += letter
 
        # in case of space
        else:
            # if i = 1 that indicates a new character
            i += 1
 
            # if i = 2 that indicates a new word
            if i == 2 :
 
                 # adding space to separate words
                decipher += ' '
            else:
 
                # accessing the keys using their values (reverse of encryption)
                try:
                    decipher += list(morze.keys()
                                     )[list(morze.values()).index(citext)]
                    citext = ''
                except Exception:
                    pass

 
    return decipher


def rus_to_morze(message):
    cipher = ''
    message = message.lower()
    for letter in message:
        if letter != ' ':
            try:
                cipher += russian_morze[letter] + ' '
            except KeyError:
                cipher += 'Неопределенный символ'
        else:
            cipher += ' '
    return cipher    


def morze_to_rus(message):
    # extra space added at the end to access the
        # last morse code
        message += ' '
     
        decipher = ''
        citext = ''
        i = 0
        for letter in message:
     
            # checks for space
            if (letter != ' '):
     
                # counter to keep track of space
                i = 0
     
                # storing morse code of a single character
                citext += letter
     
            # in case of space
            else:
                # if i = 1 that indicates a new character
                i += 1
     
                # if i = 2 that indicates a new word
                if i == 2 :
     
                     # adding space to separate words
                    decipher += ' '
                else:
     
                    # accessing the keys using their values (reverse of encryption)
                    try:
                        decipher += list(russian_morze.keys()
                                         )[list(russian_morze.values()).index(citext)]
                        citext = ''
                    except Exception:
                        pass
        return decipher


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Текстовый редактор.ui.xml', self)
        self.setWindowTitle('Project "Ы"')
        self.doc.setReadOnly(True)
        self.create.clicked.connect(self.creator)
        self.save.clicked.connect(self.saver)
        self.opn.clicked.connect(self.opener)
        self.translit.clicked.connect(self.trans)
        self.doc.setPlainText('')
        self.engToMorze.clicked.connect(self.morze)
        self.morzeToEng.clicked.connect(self.morze)
        self.rusToMorze.clicked.connect(self.morze)
        self.morzeToRus.clicked.connect(self.morze)
        self.speak.clicked.connect(self.speaker)
        self.eng_speak.clicked.connect(self.speaker2)
        self.tr = {
            'А': 'A',
            'Б': 'B',
            'В': 'V',
            'Г': 'G',
            'Д': 'D',
            'Е': 'E',
            'Ё': 'E',
            'Ж': 'Zh',
            'З': 'Z',
            'И': 'I',
            'Й': 'I',
            'К': 'K',
            'Л': 'L',
            'М': 'M',
            'Н': 'N',
            'О': 'O',
            'П': 'P',
            'Р': 'R',
            'С': 'S',
            'Т': 'T',
            'У': 'U',
            'Ф': 'F',
            'Х': 'Kh',
            'Ц': 'Tc',
            'Ч': 'Ch',
            'Ш': 'Sh',
            'Щ': 'Shch',
            'Ы': 'Y',
            'Э': 'E',
            'Ю': 'Iu',
            'Я': 'Ia',
            'а': 'a',
            'б': 'b',
            'в': 'v',
            'г': 'g',
            'д': 'd',
            'е': 'e',
            'ё': 'e',
            'ж': 'zh',
            'з': 'z',
            'и': 'i',
            'й': 'i',
            'к': 'k',
            'л': 'l',
            'м': 'm',
            'н': 'n',
            'о': 'o',
            'п': 'p',
            'р': 'r',
            'с': 's',
            'т': 't',
            'у': 'u',
            'ф': 'f',
            'х': 'kh',
            'ц': 'tc',
            'ч': 'ch',
            'ш': 'sh',
            'щ': 'shch',
            'ы': 'y',
            'э': 'e',
            'ю': 'iu',
            'я': 'ia'
        }

    def opener(self):
        self.doc.setReadOnly(False)
        txt = ''
        fname = QFileDialog.getOpenFileName(
            self, 'Выбрать документ', '',
            'Документ (*.txt);;Документ (*.txt);;Все файлы (*)')[0]
        if fname == '':
            pass
        else:

            with open(fname, 'r', encoding='utf-8') as f:
                txt = f.read()
            self.doc.setPlainText(txt)
            self.setWindowTitle('Project "Ы" - ' + fname)

    def trans(self):
        forbid = ['ь', 'Ъ', 'ъ', 'Ь']
        sp = []
        for i in self.doc.toPlainText():
            if i in forbid:
                el = ''
            elif i.isalpha() and i not in forbid:
                el = self.tr.get(i, i)          
            elif i == ' ':
                el = ' '
            else:
                el = i
            sp.append(el)
        self.doc.setPlainText(''.join(sp))
        
    def saver(self):
        self.doc.setReadOnly(False)
        filename, ok = QFileDialog.getSaveFileName(self,
                                     "Сохранить файл",
                                     "",
                                     "Документ(*.txt)")
        if ''.join(filename.split()) == '':
            pass
        else:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(self.doc.toPlainText())


    def creator(self):
        self.doc.setReadOnly(False)
        self.setWindowTitle('Project "Ы" - новый документ')

    def morze(self):
        signal = self.sender().text()
        res = ''
        print(signal)
        if signal == 'в морзе(eng)':
            res = encode_to_morse(self.doc.toPlainText().lower())
        elif signal == 'из морзе(eng)':
            res = decode_to_morse(self.doc.toPlainText().lower())
        elif signal == 'в морзе(рус.)':
            res = rus_to_morze(self.doc.toPlainText().lower())
        elif signal == 'из морзе(рус.)':
            res = morze_to_rus(self.doc.toPlainText().lower())
        else:
            res = 'Мне кажется, или идет что-то не так?'
        self.doc.setPlainText(str(res))

    def speaker(self):
        language = 'ru'
        # Passing the text and language to the engine,
        # here we have assign slow=False. Which denotes
        # the module that the transformed audio should
        # have a high speed
        txt = self.doc.toPlainText()
        try:
            obj = gTTS(text=txt, lang=language, slow=False)
        except Exception:
            self.doc.setText('Не удается озвучить текст')
        else:
            obj.save("test.mp3")
            # Play the exam.mp3 file
            playsound("test.mp3")
            os.remove('test.mp3')

    def speaker2(self):
        language = 'en'
         
        # Passing the text and language to the engine, 
        # here we have assign slow=False. Which denotes 
        # the module that the transformed audio should 
        # have a high speed
        txt = self.doc.toPlainText()
        try:
            obj = gTTS(text=txt, lang=language, slow=False)
        except Exception:
            self.doc.setText('Не удается озвучить текст')
        else:
            # Here we are saving the transformed audio in a mp3 file named
            # exam.mp3 
            obj.save("test1.mp3")
            # Play the exam.mp3 file
            playsound("test1.mp3")
            os.remove('test1.mp3')

    def keyPressEvent(self, event):
        if int(event.modifiers()) == Qt.ControlModifier:
            if event.key() == Qt.Key_S:
                self.saver()
            elif event.key() == Qt.Key_N:
                self.creator()
            elif event.key() == Qt.Key_O:
                self.opener()
            elif event.key() == Qt.Key_T:
                self.trans()
            elif event.key() == Qt.Key_R:
                self.speaker()
            elif event.key() == Qt.Key_E:
                self.speaker2()
            elif event.key() == Qt.Key_1:
                self.doc.setPlainText(
                    str(encode_to_morse(self.doc.toPlainText())))
            elif event.key() == Qt.Key_2:
                self.doc.setPlainText(
                    str(decode_to_morse(self.doc.toPlainText())))
            elif event.key() == Qt.Key_3:
                self.doc.setPlainText(
                    str(rus_to_morze(self.doc.toPlainText())))
            elif event.key() == Qt.Key_4:
                self.doc.setPlainText(
                    str(morze_to_rus(self.doc.toPlainText())))

if __name__ == '__main__':
    app=QApplication(sys.argv)
    ex=Example()
    ex.show()
    sys.exit(app.exec())
