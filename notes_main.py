from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication,QWidget,QPushButton,QHBoxLayout,QVBoxLayout,QLabel,QMessageBox,QRadioButton,QGroupBox,QButtonGroup,QTextEdit,QListWidget,QLineEdit,QInputDialog
import json

notes = {}

with open("notes_data.json","r",encoding="UTF-8") as file:
    notes = json.load(file)

with open("notes_data.json","w",encoding="UTF-8") as file:
    json.dump(notes,file,sort_keys=True)

app = QApplication([])
alert = QWidget()
alert.setWindowTitle('Умные заметки')

glav_lay = QHBoxLayout()
lay_1 = QVBoxLayout()
lay_2 = QVBoxLayout()
lay_3 = QHBoxLayout()
lay_4 = QHBoxLayout()

glav_window = QTextEdit()
wind_blit_1 = QListWidget()
wind_blit_2 = QListWidget()
py_input = QLineEdit("Введите тег:")
text_1 = QLabel("Список заметок")
text_2 = QLabel("Список тегов")
zam_create = QPushButton("Создать заметку")
zam_delete = QPushButton("Удалить заметку")
zam_save = QPushButton("Сохранить заметку")
zam_add = QPushButton("Добавить к заметке")
zam_cut = QPushButton("Открепить от заметки")
zam_search = QPushButton("Искать заметки по тегу")

lay_1.addWidget(glav_window)
lay_2.addWidget(text_1,alignment = Qt.AlignLeft)
lay_2.addWidget(wind_blit_1,alignment = Qt.AlignCenter)
lay_3.addWidget(zam_create,alignment = Qt.AlignCenter)
lay_3.addWidget(zam_delete,alignment = Qt.AlignCenter)
lay_2.addLayout(lay_3)
lay_2.addWidget(zam_save,alignment = Qt.AlignCenter)
lay_2.addWidget(text_2,alignment = Qt.AlignLeft)
lay_2.addWidget(wind_blit_2,alignment = Qt.AlignCenter)
lay_2.addWidget(py_input,alignment = Qt.AlignCenter)
lay_4.addWidget(zam_add,alignment = Qt.AlignCenter)
lay_4.addWidget(zam_cut,alignment = Qt.AlignCenter)
lay_2.addLayout(lay_4)
lay_2.addWidget(zam_search,alignment = Qt.AlignCenter)

def create_note():
    name_note, ok = QInputDialog.getText(alert,"Добавить заметку","Название заметки:")
    if (ok != False) and name_note != "":
        notes[name_note] = {'текст':'','теги':[]}
        wind_blit_1.addItem(name_note)
        wind_blit_2.addItems(notes[name_note]['теги'])

def save_note():
    if wind_blit_1.selectedItems():
        text = glav_window.toPlainText()
        key = wind_blit_1.selectedItems()[0].text()
        notes[key]['текст'] = text
        with open("notes_data.json","w",encoding="UTF-8") as file:
            json.dump(notes,file)
    else:
        danger = QMessageBox()
        danger.setText("Заметка не выбрана!")
        danger.exec_()

def delete_note():
    if wind_blit_1.selectedItems():
        key = wind_blit_1.selectedItems()[0].text()
        del notes[key]
        glav_window.clear()
        wind_blit_1.clear()
        wind_blit_2.clear()
        wind_blit_1.addItems(notes)
        with open("notes_data.json","w",encoding="UTF-8") as file:
            json.dump(notes,file)
    else:
        danger = QMessageBox()
        danger.setText("Заметка не выбрана!")
        danger.exec_()  

zam_delete.clicked.connect(delete_note)
zam_create.clicked.connect(create_note)
zam_save.clicked.connect(save_note)

def add_tag():
    if wind_blit_1.selectedItems():
        tag_text = py_input.text()
        key = wind_blit_1.selectedItems()[0].text()
        if tag_text not in notes[key]['теги'] and tag_text != "":
            notes[key]['теги'].append(tag_text)
            wind_blit_2.addItem(tag_text)
            with open("notes_data.json","w",encoding="UTF-8") as file:
                json.dump(notes,file,sort_keys=True)
zam_add.clicked.connect(add_tag)

def del_tag():
    if wind_blit_1.selectedItems() and wind_blit_2.selectedItems():
        key = wind_blit_2.selectedItems()[0].text()
        note = wind_blit_1.selectedItems()[0].text()
        wind_blit_2.clear()
        notes[note]['теги'].remove(key)
        wind_blit_2.addItems(notes[note]['теги'])
        with open("notes_data.json","w",encoding="UTF-8") as file:
                json.dump(notes,file,sort_keys=True)
zam_cut.clicked.connect(del_tag)

def search_teg():
    if zam_search.text() == "Искать заметки по тегу":
        tag_text = py_input.text()
        if tag_text != "":
            notes_filltered = {}
            for element in notes:
                if tag_text in notes[element]['теги']:
                    notes_filltered[element] = notes[element]
            wind_blit_1.clear()
            wind_blit_2.clear()
            py_input.setText("Введите тег:")
            wind_blit_1.addItems(notes_filltered)
            zam_search.setText("Сбросить поиск")    
    elif zam_search.text() == "Сбросить поиск":
        wind_blit_1.clear()
        wind_blit_2.clear()
        wind_blit_1.addItems(notes)
        zam_search.setText("Искать заметки по тегу")
zam_search.clicked.connect(search_teg)

def show_note():
    name = wind_blit_1.selectedItems()[0].text()
    glav_window.setText(notes[name]["текст"])
    wind_blit_2.clear()
    wind_blit_2.addItems(notes[name]["теги"])
    

wind_blit_1.itemClicked.connect(show_note)

glav_lay.addLayout(lay_1)
glav_lay.addLayout(lay_2)
alert.setLayout(glav_lay)

alert.show()

wind_blit_1.addItems(notes)
app.exec_()


