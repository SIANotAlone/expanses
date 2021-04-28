from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from datetime import datetime
import sqlite3
from PyQt5.QtWidgets import QLineEdit, QLabel, QPushButton

Form, Window = uic.loadUiType("mainwindow.ui")

app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
window.show()


lab_exp = QLabel()
le = QLineEdit()
lab_comment=QLabel()
le_comment = QLineEdit()
send_exp = QPushButton()
send_exp.setText("Добавить")
send_exp.setStyleSheet("""
background-color:"#269926";
font-size:14px;
margin-bottom:10px;

""")
status = QLabel()


form.verticalLayout_2.addWidget(lab_exp)
form.verticalLayout_2.addWidget(le)
form.verticalLayout_2.addWidget(lab_comment)
form.verticalLayout_2.addWidget(le_comment)
form.verticalLayout_2.addWidget(send_exp)
form.verticalLayout_2.addWidget(status)

lab_exp.setText("Введите трату (Поле не может быть пустым)")
lab_comment.setText('Введите комментарий к трате (Поле может быть пустым)')
status.setText("")

def get_categories_from_db():
    form.selected_cat.clear()
    conn = sqlite3.connect("base.db")
    cur = conn.cursor();
    cur.execute("SELECT (category) FROM categories")
    rows = cur.fetchall()

    for row in rows:
        form.selected_cat.addItem(str(row[0]))
        #print(row[0])

    conn.close()
#form.get_expanse.setText("15")

form.tabwidget1.setCurrentIndex(0)

def savetodb(save_expanse, curdate, curtime, category, comment):
    db = sqlite3.connect('base.db')
    sql = db.cursor()
    sql.execute(f"INSERT INTO expanses (expanse, date, time, category, comment) VALUES (?,?,?,?,?)", (save_expanse, curdate, curtime, category, comment))
    db.commit()
    sql.close()

def on_click_expance(self):
    #form.label1.setText('Оно работает!11')
    form.tabwidget1.setCurrentIndex(1)







def on_click_income():
    #form.label1.setText("")
    form.tabwidget1.setCurrentIndex(2)


    

def click_back():
    form.tabwidget1.setCurrentIndex(0)
    

def exit():
    app.exit()
def save_expanse():
    try:
        save_expance = int(le.text())
        comment = le_comment.text()
        f_today = str(datetime.today().strftime('%Y-%m-%d'))
        f_time = str(datetime.now().strftime('%H:%M:%S'))
        category = form.selected_cat.currentText()
        savetodb(int(save_expance), f_today, f_time, category, comment)
        status.setStyleSheet("""
        background-color:"#269926";
        font-size:14px; 
        """)
        status.setText("Запись успешно добавлена")
    except:
        status.setStyleSheet("""
                background-color:"red";
                font-size:14px; 
                """)
        status.setText("Возникла ошибка =(")



def get_all_exp():
    conn = sqlite3.connect("base.db")
    cur = conn.cursor();
    cur.execute("SELECT (expanse) FROM expanses")
    rows = cur.fetchall()
    all_exp = 0
    for row in rows:
        #form.selected_cat.addItem(str(row[0]))
        #print(row[0])
        all_exp += row[0]

    conn.close()
    return all_exp

form.add_expanse.clicked.connect(on_click_expance)
form.add_income.clicked.connect(on_click_income)
form.back_expanse.clicked.connect(click_back)
form.back_income.clicked.connect(click_back)
form.btn_exit.clicked.connect(exit)
send_exp.clicked.connect(save_expanse)

print('Общее кол-во трат: ' + str(get_all_exp()))
get_categories_from_db()



app.exec()
