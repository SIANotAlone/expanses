from datetime import timedelta
from PyQt5 import uic
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QApplication
from datetime import datetime
import sqlite3
from PyQt5.QtWidgets import QLineEdit, QLabel, QPushButton
from PyQt5 import QtWidgets
from qt_material import apply_stylesheet
import matplotlib.pyplot as plt

Form, Window = uic.loadUiType("mainwindow.ui")

app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
window.show()

apply_stylesheet(app, theme='dark_purple.xml')
#екран добавления расходов
lab_exp = QLabel()
le = QLineEdit()
le.setFixedHeight(40)
lab_comment=QLabel()
le_comment = QLineEdit()
le_comment.setFixedHeight(40)
onlyInt = QIntValidator()
le.setValidator(onlyInt)
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

#екран добавления прибыли
ai_edit = QLineEdit()
ai_edit.setValidator(onlyInt)
ai_edit.setFixedHeight(40)
in_cat=QLabel()
in_cat.setFixedHeight(40)
form.sel_cat.setFixedHeight(40)
in_cat.setStyleSheet("""
margin-top:10px;
""")
send_income = QPushButton()
form.label_2.setFixedHeight(40)
form.label_3.setFixedHeight(40)
send_income.setText("Добавить")
send_income.setStyleSheet("""
background-color:"#269926";
font-size:14px;
margin-bottom:10px;
margin-top:10px;
""")
comment_lab = QLabel()
comment_lab.setText("Комментарий (Не обязательно)")
comment_lab.setFixedHeight(40)
comment_lab.setStyleSheet("""
margin-top:15px;
margin-bottom:15px;
""")
comment_income = QLineEdit()
comment_income.setFixedHeight(40)
inc_status = QLabel()

form.verticalLayout_3.addWidget(ai_edit)
form.verticalLayout_3.addWidget(comment_lab)
form.verticalLayout_3.addWidget(comment_income)
form.verticalLayout_3.addWidget(send_income)
spacerItem = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
form.verticalLayout_3.addItem(spacerItem)
form.verticalLayout_3.addWidget(inc_status)




def get_categories_from_db():
    form.selected_cat.clear()
    conn = sqlite3.connect("base.db")
    cur = conn.cursor();

    #Загрузка категорий расходов
    cur.execute("SELECT (category) FROM categories")
    rows = cur.fetchall()

    for row in rows:
        form.selected_cat.addItem(str(row[0]))
        #print(row[0])
    #Загрузка категорий прибыли
    cur.execute("SELECT (category) FROM income_categories")
    rows = cur.fetchall()
    for row in rows:
        form.sel_cat.addItem(str(row[0]))

    conn.close()
#form.get_expanse.setText("15")

form.tabwidget1.setCurrentIndex(0)
#Записываем данные по расходам в базу
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
#Записываем данные по прибыли в базу
def save_income(income, curdate, curtime, category, comment):
    db = sqlite3.connect('base.db')
    sql = db.cursor()
    sql.execute(f"INSERT INTO incomes (income, date, time, category, comment) VALUES (?,?,?,?,?)",
                (income, curdate, curtime, category, comment))
    db.commit()
    sql.close()
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


def add_income():
    try:
        income = int(ai_edit.text())
        f_today = str(datetime.today().strftime('%Y-%m-%d'))
        f_time = str(datetime.now().strftime('%H:%M:%S'))
        category = form.sel_cat.currentText()
        comment = comment_income.text()
        save_income(income, f_today, f_time, category, comment)

        inc_status.setStyleSheet("""
                background-color:"#269926";
                font-size:14px; 
                
                """)
        inc_status.setText("Запись успешно добавлена")
    except:
        inc_status.setStyleSheet("""
                        background-color:"red";
                        font-size:14px; 
                        
                        """)
        inc_status.setText("Возникла ошибка =(")


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
def get_all_income():
    conn = sqlite3.connect("base.db")
    cur = conn.cursor();
    cur.execute("SELECT (income) FROM incomes")
    rows = cur.fetchall()
    all_inc = 0
    for row in rows:
        all_inc += row[0]

    conn.close()
    return all_inc


def statistics_tab():
    form.tabwidget1.setCurrentIndex(3)
def all_stat():

    #form.selected_cat.clear()
    #form.sel_cat.clear()
    income = get_all_income()
    expanses = get_all_exp()

    labels = 'Прибыль: ' + str(income), 'Расходы: ' + str(expanses)

    sizes = [income, expanses]
    explode = (0, 0.1)

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels,
            shadow=True, startangle=90)
    ax1.axis('equal')

    plt.show()



def inc_stat():
    conn = sqlite3.connect("base.db")
    cur = conn.cursor();

    # Загрузка категорий прибыли
    cur.execute("SELECT (category) FROM income_categories")
    rows = cur.fetchall()
    categories = []
    for row in rows:
        categories.append(str(row[0]))
    conn.close()
    # print(categories)
    labels = categories
    conn = sqlite3.connect("base.db")
    cur = conn.cursor();
    categories_exp = []
    sum = []
    cat_len = len(categories)
    # print(str(i))
    i = 0
    while i != cat_len:

        sum_cat = 0
        cur.execute("SELECT (income) FROM incomes WHERE category='" + categories[i] + "'")
        rows = cur.fetchall()
        for row in rows:
            sum_cat += row[0]

        categories[i] += ": " + str(sum_cat)
        i += 1
        sum.append(sum_cat)
        # print(str(sum_cat))
    print(sum)
    conn.close()
    labels = categories

    sizes = sum
    # explode = (0, 0.1)

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels,
            shadow=False, startangle=90)
    ax1.axis('equal')

    plt.show()


def exp_stat():
    conn = sqlite3.connect("base.db")
    cur = conn.cursor();

    # Загрузка категорий расходов
    cur.execute("SELECT (category) FROM categories")
    rows = cur.fetchall()
    categories = []
    for row in rows:
        categories.append(str(row[0]))
    conn.close()
    #print(categories)
    labels = categories
    conn = sqlite3.connect("base.db")
    cur = conn.cursor();
    categories_exp = []
    sum = []
    cat_len = len(categories)
    #print(str(i))
    i=0
    while i!=cat_len:

        sum_cat=0
        cur.execute("SELECT (expanse) FROM expanses WHERE category='"+categories[i]+"'")
        rows = cur.fetchall()
        for row in rows:
            sum_cat += row[0]

        categories[i] += ": " + str(sum_cat)
        i += 1
        sum.append(sum_cat)
        #print(str(sum_cat))
    print(sum)
    conn.close()
    labels = categories

    sizes = sum
    #explode = (0, 0.1)

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes,  labels=labels,
            shadow=False, startangle=90)
    ax1.axis('equal')

    plt.show()

def get_exp_by_week():
    f_today = str(datetime.today().strftime('%Y-%m-%d'))

    #day = str(datetime.today().strftime('%d'))

    day = f_today.split("-")
    print(day)

    conn = sqlite3.connect("base.db")
    cur = conn.cursor();
    exp = []
    cur.execute("SELECT (category) FROM categories")
    rows = cur.fetchall()
    categories = []
    for row in rows:
        categories.append(str(row[0]))
    sum=0
    n=0
    bycategories = []
    for n in range(len(categories)):
        #print(categories[n])
        #print("Итерация цикла: " + str(n))
        i = 0
        while i != 7:
            get_date = datetime.strptime(f_today, '%Y-%m-%d')
            delta = get_date - timedelta(days=i)
            day = str(delta).split(" ")
            # print(day[0])
            query = "SELECT (expanse) FROM expanses WHERE date='" + day[0] + "' AND category='"+categories[n]+"'"
            #print(query)
            cur.execute(query)
            rows = cur.fetchall()
            all_exp = 0
            for row in rows:
                all_exp += row[0]
            exp.append(all_exp)
            sum += exp[i]
            i += 1
        #print(str(exp))
        #print(str(sum))
        bycategories.append(sum)
    conn.close()
    print(str(bycategories))

    for m in range(len(categories)):
        categories [m]+= ": " + str(bycategories[m])

    labels = categories

    sizes = bycategories
    # explode = (0, 0.1)

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels,
            shadow=False, startangle=90)
    ax1.axis('equal')

    plt.show()
        #i+=1
    # conn = sqlite3.connect("base.db")
    # cur = conn.cursor();
    # cur.execute("SELECT (expanse) FROM expanses WHERE date='"+f_today+"'")
    # rows = cur.fetchall()
    # all_exp = 0
    # for row in rows:
    #     # form.selected_cat.addItem(str(row[0]))
    #     # print(row[0])
    #     all_exp += row[0]
    #
    # conn.close()
    # return all_exp

form.add_expanse.clicked.connect(on_click_expance)
form.add_income.clicked.connect(on_click_income)
form.back_expanse.clicked.connect(click_back)
form.back_income.clicked.connect(click_back)
form.btn_exit.clicked.connect(exit)
send_exp.clicked.connect(save_expanse)
send_income.clicked.connect(add_income)
form.statistics.clicked.connect(statistics_tab)
form.stat_back.clicked.connect(click_back)
form.all_stat.clicked.connect(all_stat)
form.inc_stat.clicked.connect(inc_stat)
form.exp_stat.clicked.connect(exp_stat)
form.sort_by_week.clicked.connect(get_exp_by_week)

print('Общее кол-во трат: ' + str(get_all_exp()))
print('Общее кол-во прибыли: ' + str(get_all_income()))
get_categories_from_db()


app.exec()
