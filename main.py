# -*- coding: utf-8 -*-
# !/usr/bin/python3

import sys
import csv
import pandas as pd
import smtplib

from email.mime.text import MIMEText
from PyQt5 import uic, QtCore, QtWidgets
from PyQt5.QtCore import pyqtSignal, QEvent
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QLineEdit

main_window = None
sender_wind = None
admin_name = None
registration = None
login_error = None
passwords_error = None
total_error = None
table_window = None
add = None
delet = None
users_registration = None
id_except = None

message = 'Здравствуйте, уважаемый участник нашей програмы! Спасибо за то, что выбрали именно нас. Спешим напомнить вам,' \
          ' что срок вашего обучения подходит к концу... Желаем удачи и ждем вас снова!'

with open('dict.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file, delimiter=';')
    logins_and_passwords = list(reader)
file.close()

with open('user_info.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file, delimiter=';')
    user_info = list(reader)[1:]
file.close()


id = list()
FIO = list()
NAPR = list()
courses = list()
PROD = list()
HOUR = list()
Start = list()
end = list()
org = list()
dog = list()
phone = list()
email = list()
for i in range(len(user_info)):
    id.append(user_info[i][0])
    FIO.append(user_info[i][1])
    NAPR.append(user_info[i][2])
    courses.append(user_info[i][3])
    PROD.append(user_info[i][4])
    HOUR.append(user_info[i][5])
    Start.append(user_info[i][6])
    end.append(user_info[i][7])
    org.append(user_info[i][8])
    dog.append(user_info[i][9])
    phone.append(user_info[i][10])
    email.append(user_info[i][11])


def clikable_lineEdit(widget):
    class Filter(QLineEdit):
        clicked = pyqtSignal()

        def eventFilter(self, obj, event):
            if obj == widget and event.type() == QEvent.MouseButtonRelease and obj.rect().contains(event.pos()):
                self.clicked.emit()
                return True
            else:
                return False

    filter = Filter(widget)
    widget.installEventFilter(filter)
    filter.hide()
    return filter.clicked


class PandasModel(QtCore.QAbstractTableModel):
    def __init__(self, df=pd.DataFrame(), parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent=parent)
        self._df = df.copy()

    def toDataFrame(self):
        return self._df.copy()

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        if orientation == QtCore.Qt.Horizontal:
            try:
                return self._df.columns.tolist()[section]
            except (IndexError,):
                return QtCore.QVariant()
        elif orientation == QtCore.Qt.Vertical:
            try:
                return self._df.index.tolist()[section]
            except (IndexError,):
                return QtCore.QVariant()

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        if not index.isValid():
            return QtCore.QVariant()

        return QtCore.QVariant(str(self._df.iloc[index.row(), index.column()]))

    def setData(self, index, value, role):
        row = self._df.index[index.row()]
        col = self._df.columns[index.column()]
        if hasattr(value, 'toPyObject'):
            # PyQt4 gets a QVariant
            value = value.toPyObject()
        else:
            # PySide gets an unicode
            dtype = self._df[col].dtype
            if dtype != object:
                value = None if value == '' else dtype.type(value)
        self._df.set_value(row, col, value)
        return True

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._df.index)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self._df.columns)

    def sort(self, column, order):
        colname = self._df.columns.tolist()[column]
        self.layoutAboutToBeChanged.emit()
        self._df.sort_values(colname, ascending=order == QtCore.Qt.AscendingOrder, inplace=True)
        self._df.reset_index(inplace=True, drop=True)
        self.layoutChanged.emit()


class myWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(myWindow, self).__init__(parent)
        self.initUi()

    def initUi(self):
        self.CSS = """
       .QWidget {
            text-family: "Lato";
            background-color: black;
       }
       .QPushButton {
           background-color: #FFF;
           border: 3px solid transparent;
           border-color: #90EE90;
           border-radius: 5px;
       }
       .QPushButton::hover {
           background-color: #90EE90;
           border-color: gold;
           border-radius: 10px;
       }
       .QTableView {
            background-color: black;
            border-color: black;
            outline: none;
            gridline-color: black;
            border-color: rgb(242, 128, 133);
       }
       .QHeaderView::section {
            background-color: rgb(71, 153, 176);
            color: white;
            height: 35px;
            font: 14px;
       }
       .QTableView::item:focus{
            border: 2px solid gold;
            background-color: #90ee90;
            color: black;
       }
       .QTableView::item {
           background-color: #FFF;
       }
       .QTableView::item:selected {
            color: black;
            background-color: #90ee90;
       }
       .QScrollBar:vertical {
           background: rgb(188, 224, 235);
       }
       .QScrollBar::handle:vertical {
           background: rgb(71, 153, 176);
       }
       .QScrollBar:horizontal {
           background: rgb(188, 224, 235);
       }
       .QScrollBar::handle:horizontal {
           background: rgb(71, 153, 176);
       }
       .QLineEdit {
           background-color: #FFF;
       }
       .QComboBox {
           font: 16px Lato;
           background-color: #fff;
           border: 1px solid #90EE90;
           border-radius: 7px;
           padding-left: 1px;
       }
       .QComboBox::drop-down {
           border: 0px;
       }
       .QComboBox::down-arrow {
           image: url('imgs/arrow_down.png');
           width: 12px;
           height: 12px;
           margin-right: 12px;
       }
       .QComboBox:on{
           border: 4px solid #90EE90;
       }
       .QComboBox QAbstractItemView::SelectItems{
           font-size: 2px;
           border: 1px solid rgba(0, 0, 0, 10%);
           padding: 5px;
           background-color: #fff;
           outline: 0px;
       }
       .QComboBox QAbstractItemView:item {
           padding-left: 10px;
           background-color: #fff;
       }
       .QComboBox QAbstractItemView:item:hover {
           background-color: #90EE90;
       }
       .QLabel {
           color: #fdfdfd;
           font-weight: solid;
           font-family: "Lato";
           font-size: 20px;
       }
        """
        self.centralwidget = QtWidgets.QWidget(self)
        self.lineEdit = QtWidgets.QLineEdit(self)
        self.view = QtWidgets.QTableView(self)
        self.view.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.comboBox = QtWidgets.QComboBox(self)
        self.label = QtWidgets.QLabel(self)
        self.back_bt = QtWidgets.QPushButton(self)
        self.back_bt.setIcon(QIcon(r'imgs\back.png'))
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.addWidget(self.back_bt, 0, 3, 1, 8)
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.view, 1, 0, 1, 11)
        self.gridLayout.addWidget(self.comboBox, 0, 2, 1, 1)
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.back_bt.clicked.connect(self.back)
        self.setStyleSheet(self.CSS)
        self.back_bt.setStyleSheet(self.CSS)
        self.lineEdit.setStyleSheet(self.CSS)
        self.comboBox.setStyleSheet(self.CSS)
        self.label.setStyleSheet(self.CSS)

        self.setCentralWidget(self.centralwidget)
        self.label.setText("Regex Filter")

        self.load_sites()
        self.comboBox.addItems(["{0}".format(col) for col in self.model._df.columns])

        self.lineEdit.textChanged.connect(self.on_lineEdit_textChanged)
        self.comboBox.currentIndexChanged.connect(self.on_comboBox_currentIndexChanged)

        self.horizontalHeader = self.view.horizontalHeader()
        self.horizontalHeader.sectionClicked.connect(self.on_view_horizontalHeader_sectionClicked)

    def back(self):
        global main_window, table_window
        main_window = MainWindow()
        table_window.hide()
        main_window.show()

    def load_sites(self):
        global id, FIO, NAPR, courses, PROD, HOUR, Start, end, org, dog, phone, email

        df = pd.DataFrame({'id': id,
                           'ФИО': FIO,
                           'Направление': NAPR,
                           'Курс': courses,
                           'Продолжительность': PROD,
                           'Учебный день': HOUR,
                           'Дата начала': Start,
                           'Дата окончания': end,
                           'Организация': org,
                           '№Договор': dog,
                           'Номер телефона': phone,
                           'e-mail': email})
        self.model = PandasModel(df)
        self.proxy = QtCore.QSortFilterProxyModel(self)
        self.proxy.setSourceModel(self.model)
        self.view.setModel(self.proxy)
        self.view.resizeColumnsToContents()

    @QtCore.pyqtSlot(int)
    def on_view_horizontalHeader_sectionClicked(self, logicalIndex):

        self.logicalIndex = logicalIndex
        self.menuValues = QtWidgets.QMenu(self)
        self.signalMapper = QtCore.QSignalMapper(self)
        self.comboBox.blockSignals(True)
        self.comboBox.setCurrentIndex(self.logicalIndex)
        self.comboBox.blockSignals(True)

        valuesUnique = self.model._df.iloc[:, self.logicalIndex].unique()

        actionAll = QtWidgets.QAction("All", self)
        actionAll.triggered.connect(self.on_actionAll_triggered)
        self.menuValues.addAction(actionAll)
        self.menuValues.addSeparator()
        for actionNumber, actionName in enumerate(sorted(list(set(valuesUnique)))):
            action = QtWidgets.QAction(actionName, self)
            self.signalMapper.setMapping(action, actionNumber)
            action.triggered.connect(self.signalMapper.map)
            self.menuValues.addAction(action)
        self.signalMapper.mapped.connect(self.on_signalMapper_mapped)
        headerPos = self.view.mapToGlobal(self.horizontalHeader.pos())
        posY = headerPos.y() + self.horizontalHeader.height()
        posX = headerPos.x() + self.horizontalHeader.sectionPosition(self.logicalIndex)

        self.menuValues.exec_(QtCore.QPoint(posX, posY))

    @QtCore.pyqtSlot()
    def on_actionAll_triggered(self):
        filterColumn = self.logicalIndex
        filterString = QtCore.QRegExp("",
                                      QtCore.Qt.CaseInsensitive,
                                      QtCore.QRegExp.RegExp
                                      )

        self.proxy.setFilterRegExp(filterString)
        self.proxy.setFilterKeyColumn(filterColumn)

    @QtCore.pyqtSlot(int)
    def on_signalMapper_mapped(self, i):
        stringAction = self.signalMapper.mapping(i).text()
        filterColumn = self.logicalIndex
        filterString = QtCore.QRegExp(stringAction,
                                      QtCore.Qt.CaseSensitive,
                                      QtCore.QRegExp.FixedString
                                      )

        self.proxy.setFilterRegExp(filterString)
        self.proxy.setFilterKeyColumn(filterColumn)

    @QtCore.pyqtSlot(str)
    def on_lineEdit_textChanged(self, text):
        search = QtCore.QRegExp(text,
                                QtCore.Qt.CaseInsensitive,
                                QtCore.QRegExp.RegExp
                                )

        self.proxy.setFilterRegExp(search)

    @QtCore.pyqtSlot(int)
    def on_comboBox_currentIndexChanged(self, index):
        self.proxy.setFilterKeyColumn(index)


class EnterWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initWindow()

    def initWindow(self):
        uic.loadUi(r'forms\registrationWindow.ui', self)
        clikable_lineEdit(self.login_line).connect(self.login_change)
        clikable_lineEdit(self.password_line).connect(self.password_change)
        self.pixmap = QPixmap(r'imgs\logo.png')
        self.pixmap_photo1 = QPixmap(r'imgs\photo1.png')
        self.pixmap_photo2 = QPixmap(r'imgs\photo2.png')
        self.pixmap_photo3 = QPixmap(r'imgs\photo3.png')
        self.pixmap_photo4 = QPixmap(r'imgs\photo4.png')
        self.pixmap_photo5 = QPixmap(r'imgs\photo5.png')
        self.pixmap_photo6 = QPixmap(r'imgs\photo6.png')
        self.pixmap_photo7 = QPixmap(r'imgs\photo7.png')
        self.pixmap_photo8 = QPixmap(r'imgs\photo8.png')
        self.pixmap_photo9 = QPixmap(r'imgs\photo9.png')
        self.pixmap_photo10 = QPixmap(r'imgs\photo10.png')
        self.pixmap_photo11 = QPixmap(r'imgs\photo11.png')
        self.pixmap_photo12 = QPixmap(r'imgs\photo12.png')
        self.pixmap_photo13 = QPixmap(r'imgs\photo13.png')
        self.pixmap_photo14 = QPixmap(r'imgs\photo14.png')
        self.pixmap_photo15 = QPixmap(r'imgs\photo15.png')
        self.pixmap_photo16 = QPixmap(r'imgs\photo16.png')
        self.photo1.setPixmap(self.pixmap_photo1)
        self.photo2.setPixmap(self.pixmap_photo2)
        self.photo3.setPixmap(self.pixmap_photo3)
        self.photo4.setPixmap(self.pixmap_photo4)
        self.photo5.setPixmap(self.pixmap_photo5)
        self.photo6.setPixmap(self.pixmap_photo6)
        self.photo7.setPixmap(self.pixmap_photo7)
        self.photo8.setPixmap(self.pixmap_photo8)
        self.photo9.setPixmap(self.pixmap_photo9)
        self.photo10.setPixmap(self.pixmap_photo10)
        self.photo11.setPixmap(self.pixmap_photo11)
        self.photo12.setPixmap(self.pixmap_photo12)
        self.photo13.setPixmap(self.pixmap_photo13)
        self.photo14.setPixmap(self.pixmap_photo14)
        self.photo15.setPixmap(self.pixmap_photo15)
        self.photo16.setPixmap(self.pixmap_photo16)
        self.logo.setPixmap(self.pixmap)
        self.EnterButton.clicked.connect(self.enter)
        self.EnterButton.setAutoDefault(True)
        self.password_line.returnPressed.connect(self.EnterButton.clicked.emit)
        self.login_line.returnPressed.connect(self.EnterButton.clicked.emit)
        self.changed = """
        .QLineEdit{
            background-color: white;
            border-radius: 10px;
            border: 3px solid transparent;
            border-color: #90EE90;
            font-weight: bold;
            font: 16px Lato;
            color: black;
        }
        """
        self.CSS = """
        .QWidget{
            background-color: black;
        }
        .QPushButton{
            background-color: #FFF;
            border-radius: 15px;
            border: 3px solid transparent;
            border-color: #90EE90;
            font-weight: bold;
            font-size: 16px Lato;
        }
        .QLineEdit{
            background-color: white;
            border-radius: 10px;
            border: 3px solid transparent;
            border-color: #90EE90;
            font-weight: bold;
            font: 16px Lato;
            color: gray;
        }
         .QPushButton::hover{
            border: 3px solid transparent;
            border-color: black;
            background-color: #90EE90;
        }
        """
        self.EnterButton.setStyleSheet(self.CSS)
        self.login_line.setStyleSheet(self.CSS)
        self.password_line.setStyleSheet(self.CSS)
        self.setStyleSheet(self.CSS)

    def login_change(self):
        if not self.login_line.isEnabled():
            self.login_line.setEnabled(True)
            self.login_line.setText('')
            self.login_line.setStyleSheet(self.changed)
            self.login_flag = False
            if self.password_line.text() == '':
                self.password_line.setEnabled(False)
                self.password_line.setEchoMode(QLineEdit.Normal)
                self.password_line.setText('Пароль')
                self.password_line.setStyleSheet(self.CSS)
                self.password_flag = True
            self.login_line.setFocus()

    def password_change(self):
        if not self.password_line.isEnabled():
            self.password_line.setEnabled(True)
            self.password_line.setFocus()
            self.password_line.setText('')
            self.password_line.setStyleSheet(self.changed)
            self.password_line.setEchoMode(QLineEdit.Password)
            if self.login_line.text() == '':
                self.login_line.setEnabled(False)
                self.login_line.setText('Логин')
                self.login_line.setStyleSheet(self.CSS)
                self.login_flag = True
            self.password_flag = False

    def enter(self):
        global main_window, admin_name
        flag = True
        for i in range(len(logins_and_passwords)):
            if self.login_line.text() in logins_and_passwords[i]['login'] and self.password_line.text() == \
                    logins_and_passwords[i]['password']:
                admin_name = logins_and_passwords[i]['user_name']
                main_window = MainWindow()
                application.hide()
                main_window.show()
                main_window.setFixedSize(353, 452)
                flag = False
                break
        if flag:
            main_window = Invalid()
            main_window.show()
            self.password_line.setText('Пароль')
            self.password_line.setEnabled(False)
            self.password_flag = True
            self.password_line.setEchoMode(QLineEdit.Normal)
            main_window.setStyleSheet('background-color: black;')
            main_window.setFixedSize(332, 172)


class Invalid(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        uic.loadUi(r'forms\Invalid.ui', self)
        self.CSS = """
        .QLabel{
            color: #FFF;
            font-family: "Lato";
            font-size: 16px;
        }
        """
        self.pixmap = QPixmap(r'imgs\error.png')
        self.error_label.setPixmap(self.pixmap)
        self.ok.setStyleSheet('.QPushButton{background-color: #90EE90; border: 3px solid transparent;'
                              'border-color: #90EE90; border-radius: 10px;'
                              'font-family: "Lato"; font-size: 16px; font-weight: bold;}')
        self.ok.clicked.connect(self.close)
        self.error.setStyleSheet(self.CSS)

    def close(self):
        global main_window
        main_window.hide()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        global admin_name
        uic.loadUi(r'forms\main.ui', self)
        self.admin_name.setText('Вы вошли как администратор: {0}'.format(admin_name))
        self.CSS = """
        .QWidget{
            background-color: black;
        }
        .QPushButton{
            background-color: #FFF;
            border-radius: 15px;
            border: 3px solid transparent;
            border-color: #90EE90;
            font-size: 16px;
        }
        .QPushButton::hover{
            border: 3px solid transparent;
            border-color: gold;
            background-color: #90EE90;
        }
        .QLabel{
            background-color: None;
            color: #FFF;
            font-family: "Lato";
            font-size: 18px;
        }
        """
        self.setStyleSheet(self.CSS)
        self.fire.setStyleSheet(self.CSS)
        self.fire.clicked.connect(self.open)
        self.guard.setStyleSheet(self.CSS)
        self.guard.clicked.connect(self.deleter)
        self.human_guard.setStyleSheet(self.CSS)
        self.human_guard.clicked.connect(self.users_open)
        self.industry.setStyleSheet(self.CSS)
        self.industry.clicked.connect(self.sender)
        self.add_admin.setStyleSheet(self.CSS)
        self.add_admin.clicked.connect(self.add_admin_pressed)
        self.label.setStyleSheet(self.CSS)
        self.label_2.setStyleSheet(self.CSS)
        self.label_3.setStyleSheet(self.CSS)
        self.admin_name.setStyleSheet("""
            background-color: None;
            color: #FFF;
            font-family: "Lato";
            font-size: 16px;
        """)

    def add_admin_pressed(self):
        global registration
        registration = AdminRegistration()
        registration.setStyleSheet('background-color: black;')
        registration.show()

    def open(self):
        global table_window
        table_window = myWindow()
        table_window.showFullScreen()
        table_window.setWindowTitle('Просмотр базы')
        main_window.hide()

    def add_people(self):
        global registration
        registration = AdminRegistration()
        registration.setStyleSheet('background-color: black;')
        registration.show()

    def sender(self):
        global sender_wind

        sender_wind = Sender()
        sender_wind.setWindowTitle('Рассылка')
        sender_wind.setStyleSheet('background-color: black;')
        sender_wind.show()
        sender = "noreply.centerobr@gmail.com"
        password = "omwbbkwdwqclebxt"
        getters = ['dpankratov06@yandex.ru', 'makc.roslov@gmail.com']
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        try:
            server.login(sender, password)
            msg = MIMEText(message)
            msg["Subject"] = "ОБУЧЕНИЕ"
            server.sendmail(sender, getters, msg.as_string())

            return "The message was sent successfully!"
        except Exception as _ex:
            return f"{_ex}\nCheck your login or password please!"

    def deleter(self):
        global delet, main_window
        delet = Del()
        delet.setStyleSheet('background-color: black;')
        delet.show()
        main_window.hide()

    def users_open(self):
        global users_registration, main_window
        users_registration = Users_registration()
        users_registration.setFixedSize(739, 453)
        users_registration.show()
        main_window.hide()


class AdminRegistration(QMainWindow):
    def __init__(self):
        super().__init__()
        self.flag1, self.flag2, self.flag3, self.flag4 = True, True, True, True
        self.initUi()

    def initUi(self):
        uic.loadUi(r'forms\AdminRegistration.ui', self)
        clikable_lineEdit(self.login).connect(self.login_edit)
        clikable_lineEdit(self.password).connect(self.password_edit)
        clikable_lineEdit(self.Name_Surname).connect(self.Name_Surname_edit)
        clikable_lineEdit(self.repiat_password).connect(self.repiat_password_edit)
        self.Registration_button.clicked.connect(self.registration)
        self.Registration_button.setAutoDefault(True)
        self.login.returnPressed.connect(self.Registration_button.clicked.emit)
        self.password.returnPressed.connect(self.Registration_button.clicked.emit)
        self.Name_Surname.returnPressed.connect(self.Registration_button.clicked.emit)
        self.repiat_password.returnPressed.connect(self.Registration_button.clicked.emit)
        self.Registration_button.setStyleSheet('background-color: #90EE90; border: 3px solid transparent;'
                                               'border-radius: 10px; font-family: "Lato"; font-size: 16px;'
                                               'border-color: #90EE90')
        line_edit_style = 'background-color: #FFF; border: 3px solid transparent; border-radius: 5px;' \
                          'border-color: #90EE90; font-family: "Lato"; font-size: 18px'
        self.Name_Surname.setStyleSheet(line_edit_style)
        self.login.setStyleSheet(line_edit_style)
        self.password.setStyleSheet(line_edit_style)
        self.repiat_password.setStyleSheet(line_edit_style)
        self.registr.setStyleSheet('color: #FFF; font-family: "Lato"; font-size: 32px;')

    def login_edit(self):
        if self.flag1:
            self.login.setEnabled(True)
            self.login.setText('')
            self.login.setFocus()
            self.flag1 = False

    def password_edit(self):
        if self.flag2:
            self.password.setEnabled(True)
            self.password.setText('')
            self.password.setEchoMode(QLineEdit.Password)
            self.password.setFocus()
            self.flag2 = False

    def Name_Surname_edit(self):
        if self.flag3:
            self.Name_Surname.setEnabled(True)
            self.Name_Surname.setText('')
            self.Name_Surname.setFocus()
            self.flag3 = False

    def repiat_password_edit(self):
        if self.flag4:
            self.repiat_password.setEnabled(True)
            self.repiat_password.setText('')
            self.repiat_password.setEchoMode(QLineEdit.Password)
            self.repiat_password.setFocus()
            self.flag4 = False

    def registration(self):
        global registration, login_error, passwords_error, total_error
        login_flag, passwords_flag = True, True
        for i in range(len(logins_and_passwords)):
            if self.login.text() in logins_and_passwords[i]['login']:
                login_flag = False
                break
        if self.password.text() != self.repiat_password.text():
            passwords_flag = False
        if login_flag and passwords_flag and (self.Name_Surname.text() != '' or self.login.text() != '' or
                                              self.password.text() != '' or self.repiat_password.text() != ''):
            with open('dict.csv', 'a', encoding='utf-8') as wfile:
                try:
                    name = f'{self.Name_Surname.text().split()[0]} {self.Name_Surname.text().split()[1][0]}.' \
                           f'{self.Name_Surname.text().split()[2][0]}.'
                    wfile.write(f'\n"{self.login.text()}";"{self.password.text()}";"{name}"')
                    wfile.close()
                    registration.hide()
                except Exception as e:
                    total_error = Total_error()
                    total_error.setStyleSheet('background-color: black;')
                    total_error.show()
        elif self.Name_Surname.text() == '' or self.login.text() == '' or \
                self.password.text() == '' or self.repiat_password.text() == '':
            total_error = Total_error()
            total_error.setStyleSheet('background-color: black;')
            total_error.show()
        elif login_flag is False:
            login_error = Error_in_login()
            login_error.setStyleSheet('background-color: black;')
            login_error.show()
        elif passwords_flag is False:
            passwords_error = Error_in_passwords()
            passwords_error.setStyleSheet('background-color: black;')
            passwords_error.show()


class Error_in_login(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        uic.loadUi(r'forms\error_in_login.ui', self)
        self.pixmap = QPixmap(r'imgs\error.png')
        self.error_label.setPixmap(self.pixmap)
        self.ok.setStyleSheet('background-color: #90EE90; border: 3px solid transparent;'
                              'border-color: #90EE90; border-radius: 10px;'
                              'font-family: "Lato"; font-size: 16px; font-weight: bold;')
        self.ok.clicked.connect(self.close)
        self.error.setStyleSheet('color: white; font-family: "Lato"; font-size: 16px;')

    def close(self):
        global login_error
        login_error.hide()


class Error_in_passwords(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        uic.loadUi(r'forms\error_in_passwords.ui', self)
        self.pixmap = QPixmap(r'imgs\error.png')
        self.error_label.setPixmap(self.pixmap)
        self.ok.setStyleSheet('background-color: #90EE90; border: 3px solid transparent;'
                              'border-color: #90EE90; border-radius: 10px;'
                              'font-family: "Lato"; font-size: 16px; font-weight: bold;')
        self.ok.clicked.connect(self.close)
        self.error.setStyleSheet('color: white; font-family: "Lato"; font-size: 16px;')

    def close(self):
        global passwords_error
        passwords_error.hide()


class ExceptId(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        uic.loadUi(r'forms\id_except.ui', self)
        self.pixmap = QPixmap(r'imgs\error.png')
        self.error_label.setPixmap(self.pixmap)
        self.ok.setStyleSheet('background-color: #90EE90; border: 3px solid transparent;'
                              'border-color: #90EE90; border-radius: 10px;'
                              'font-family: "Lato"; font-size: 16px; font-weight: bold;')
        self.ok.clicked.connect(self.close)
        self.error.setStyleSheet('color: white; font-family: "Lato"; font-size: 16px;')

    def close(self):
        global id_except
        id_except.hide()


class Total_error(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        uic.loadUi(r'forms\total_error.ui', self)
        self.pixmap = QPixmap(r'imgs\error.png')
        self.error_label.setPixmap(self.pixmap)
        self.ok.setStyleSheet('background-color: #90EE90; border: 3px solid transparent;'
                              'border-color: #90EE90; border-radius: 10px;'
                              'font-family: "Lato"; font-size: 16px; font-weight: bold;')
        self.ok.clicked.connect(self.close)
        self.error.setStyleSheet('color: white; font-family: "Lato"; font-size: 16px;')

    def close(self):
        global total_error
        total_error.hide()


class Sender(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        uic.loadUi(r'forms\sender.ui', self)
        self.ok_2.setStyleSheet('background-color: #90EE90; border: 3px solid transparent;'
                                'border-color: #90EE90; border-radius: 10px;'
                                'font-family: "Lato"; font-size: 16px; font-weight: bold;')
        self.ok_2.clicked.connect(self.close)
        self.error.setStyleSheet('color: white; font-family: "Lato"; font-size: 18px;')

    def close(self):
        global sender_wind
        sender_wind.hide()


class Add(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        uic.loadUi(r'forms\add.ui', self)
        self.ok_2.setStyleSheet('background-color: #90EE90; border: 3px solid transparent;'
                                'border-color: #90EE90; border-radius: 10px;'
                                'font-family: "Lato"; font-size: 16px; font-weight: bold;')
        self.ok_2.clicked.connect(self.close)
        self.error.setStyleSheet('color: white; font-family: "Lato"; font-size: 18px;')

    def close(self):
        global add
        add.hide()


class Del(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(r'forms\user_del.ui', self)
        self.CSS = """
        .QWidget {
            background-color: black;
            text-family: "Lato";
        }
        .QPushButton {
            background-color: #FFF;
            border: 3px solid transparent;
            border-color: #90ee90;
            border-radius: 15px;
        }
        .QPushButton::hover {
            background-color: #90ee90;
	        border-color: gold;
        }
        .QLineEdit {
            background-color: #FFF;
            border: 3px solid transparent;
            border-color: #90EE90;
            border-radius: 10px;
        }
        .QLabel {
            color: #FFF;
            font-size: 18pt;
        }
        """
        self.initUi()

    def initUi(self):
        self.setFixedSize(500, 201)
        self.setStyleSheet(self.CSS)
        self.back.setStyleSheet(self.CSS)
        self.back.setIcon(QIcon(r'imgs\back.png'))
        self.back.clicked.connect(self.close)
        self.reg_label.setStyleSheet(self.CSS)
        clikable_lineEdit(self.id_line).connect(self.availible)
        self.add_bt.setStyleSheet(self.CSS)
        self.add_bt.clicked.connect(self.delet)
        self.id_line.setStyleSheet(self.CSS)

    def availible(self):
        if not self.id_line.isEnabled():
            self.id_line.setEnabled(True)
            self.id_line.setText('')
            self.id_line.setFocus()

    def delet(self):
        global id_except, delet, id, FIO, email, phone, NAPR, Start, end, courses, HOUR, dog, org, main_window
        try:
            id_del = int(self.id_line.text())

            with open('user_info.csv', 'r', encoding='utf-8') as file:
                reader = csv.reader(file, delimiter=';')
                user_info = list(reader)[1:]

            if id_del <= len(user_info) and id_del != 0:
                cnt = 1
                for i in user_info:
                    if int(i[0]) == id_del:
                        del user_info[user_info.index(i)]
                for i in user_info:
                    i[0] = str(cnt)
                    cnt += 1
                file.close()

                with open('user_info.csv', 'w', encoding='utf-8') as file:
                    file.write(f'"id";"ФИО";"Направление";"Курс";"Продолжительность в часах";"Учебный день в часах";'
                               f'"Дата_начала";"Дата_окончания";"Организация";"№Договор";"Номер_телефона";"E-mail"\n')
                    for i in user_info:
                        if i != user_info[-1]:
                            file.write(f'"{i[0]}";"{i[1]}";"{i[2]}";"{i[3]}";"{i[4]}";"{i[5]}";"{i[6]}";"{i[7]}";"{i[8]}";'
                                       f'"{i[9]}";"{i[10]}";"{i[11]}"\n')
                        else:
                            file.write(
                                f'"{i[0]}";"{i[1]}";"{i[2]}";"{i[3]}";"{i[4]}";"{i[5]}";"{i[6]}";"{i[7]}";"{i[8]}";'
                                f'"{i[9]}";"{i[10]}";"{i[11]}"')
                    file.close()
                delet.hide()
                main_window = MainWindow()
                main_window.show()

                id.clear()
                FIO.clear()
                NAPR.clear()
                courses.clear()
                PROD.clear()
                HOUR.clear()
                Start.clear()
                end.clear()
                org.clear()
                dog.clear()
                phone.clear()
                email.clear()

                for i in range(len(user_info)):
                    id.append(user_info[i][0])
                    FIO.append(user_info[i][1])
                    NAPR.append(user_info[i][2])
                    courses.append(user_info[i][3])
                    PROD.append(user_info[i][4])
                    HOUR.append(user_info[i][5])
                    Start.append(user_info[i][6])
                    end.append(user_info[i][7])
                    org.append(user_info[i][8])
                    dog.append(user_info[i][9])
                    phone.append(user_info[i][10])
                    email.append(user_info[i][11])
            else:
                id_except = ExceptId()
                id_except.show()
                self.id_line.setText('Введите id нужного пользователя')
                self.id_line.setEnabled(False)
                id_except.setStyleSheet('background-color: #000;')
        except:
            id_except = ExceptId()
            self.id_line.setText('Введите id нужного пользователя')
            self.id_line.setEnabled(False)
            id_except.show()
            id_except.setStyleSheet('background-color: #000;')


class Users_registration(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(r'forms\usres_registration.ui', self)
        self.names = [self.name_surname, self.time_course, self.start, self.end, self.organization, self.contract,
                      self.phone, self.mail, self.time_days]
        self.CSS = """
                       .QWidget{
                           background-color: black;
                       }
                       .QLabel{
                           color: #FFF;
                       }
                       .QLineEdit{
                           background-color: #FFF;
                           border-radius: 10px;
                           border: 3px solid transparent;
                           border-color: #90EE90;
                           font-weight: bold;
                           font: 12px Lato;
                       }
                       .QLineEdit::hover {
                           background-color: lightgray;
                       }
                       .QComboBox {
                           font: 12px Lato;
                           background-color: #fff;
                           border: 3px solid transparent;
                           border-color: #90EE90;
                           padding: 5%;
                           max-height: 30px;
                           min-width: 140px;
                           color: black;
                           border-radius: 10px;                 /* закруглёные углы */
                       }
                       .QComboBox::hover {
                           background-color: #5e5e5e;
                       }
                       .QComboBox::drop-down {
                           border: 0px;
                       }
                       .QComboBox::down-arrow {
                           image: url('imgs/arrow_down.png');
                           width: 12px;
                           height: 12px;
                           margin-right: 15px;
                       }
                       .QComboBox::on {
                           border: 4px solid;
                           border-color: #c2dbfe;
                       }
                       .QComboBox::down-arrow:pressed {
                           background-color: #fff;
                       }
                       .QComboBox QListView{
                           background-color: #FFF;
                           color: black;
                       }
                       .QPushButton{
                           background-color: #FFF;
                           color: black;
                           font-family: "Lato";
                           font-size: 14px;
                           border: 3px solid transparent;
                           border-radius: 15px;
                           border-color: #90EE90;
                       }
                       .QPushButton::hover{
                           background-color: #90EE90;
                       }
                       .QStandardItem {
                           color: #5e5e5e;
                       }
                       .QStandardItemModel QStandartItem {
                           color: #1e1e1e;
                       }
                       """
        self.initUi()

    def initUi(self):
        self.add_bt.clicked.connect(self.registration)
        self.setStyleSheet(self.CSS)
        self.back.setIcon(QIcon(r'imgs\back.png'))
        self.back.clicked.connect(self.back1)
        self.back.setStyleSheet(self.CSS)
        self.add_bt.setStyleSheet(self.CSS)
        self.name_surname.setStyleSheet(self.CSS)
        self.time_course.setStyleSheet(self.CSS)
        self.start.setStyleSheet(self.CSS)
        self.end.setStyleSheet(self.CSS)
        self.organization.setStyleSheet(self.CSS)
        self.contract.setStyleSheet(self.CSS)
        self.phone.setStyleSheet(self.CSS)
        self.mail.setStyleSheet(self.CSS)
        self.time_days.setStyleSheet(self.CSS)
        self.reg_label.setStyleSheet(self.CSS)
        self.direction.setStyleSheet(self.CSS)
        self.ceep.setStyleSheet(self.CSS)
        self.fire_ceep.setStyleSheet(self.CSS)
        self.human_ceep.setStyleSheet(self.CSS)
        self.eco_ceep.setStyleSheet(self.CSS)
        self.industry_ceep.setStyleSheet(self.CSS)
        self.fire_ceep.hide()
        self.human_ceep.hide()
        self.eco_ceep.hide()
        self.eco_ceep.setEnabled(False)
        self.industry_ceep.hide()
        self.industry_ceep.setEnabled(False)
        self.ceep.show()
        self.direction.currentTextChanged.connect(self.choice)
        clikable_lineEdit(self.name_surname).connect(self.change2)
        clikable_lineEdit(self.time_course).connect(self.change1)
        clikable_lineEdit(self.start).connect(self.change3)
        clikable_lineEdit(self.end).connect(self.change4)
        clikable_lineEdit(self.organization).connect(self.change5)
        clikable_lineEdit(self.contract).connect(self.change6)
        clikable_lineEdit(self.phone).connect(self.change7)
        clikable_lineEdit(self.mail).connect(self.change8)
        clikable_lineEdit(self.time_days).connect(self.change9)

    def choice(self):
        text = self.direction.currentText()
        if text == 'Противопожарная безопасность':
            self.fire_ceep.show()
            self.human_ceep.hide()
            self.eco_ceep.hide()
            self.industry_ceep.hide()
            self.ceep.hide()
        elif text == 'Гражданская оборона и ЧС':
            self.fire_ceep.hide()
            self.human_ceep.show()
            self.eco_ceep.hide()
            self.industry_ceep.hide()
            self.ceep.hide()
        elif text == 'Промышленная безопасность':
            self.fire_ceep.hide()
            self.human_ceep.hide()
            self.eco_ceep.hide()
            self.industry_ceep.show()
            self.ceep.hide()
        elif text == 'Экологическая безопасность':
            self.fire_ceep.hide()
            self.human_ceep.hide()
            self.eco_ceep.show()
            self.industry_ceep.hide()
            self.ceep.hide()
        else:
            self.fire_ceep.hide()
            self.human_ceep.hide()
            self.eco_ceep.hide()
            self.industry_ceep.hide()
            self.ceep.show()

    def check(self):
        for name in self.names:
            if name.isEnabled() and name.text() == '':
                name.setEnabled(False)
                if name == self.names[0]:
                    name.setText('ФИО')
                elif name == self.names[1]:
                    name.setText('Продолжительность курса')
                elif name == self.names[2]:
                    name.setText('Дата начала')
                elif name == self.names[3]:
                    name.setText('Дата окончания')
                elif name == self.names[4]:
                    name.setText('Организация')
                elif name == self.names[5]:
                    name.setText('№Договора')
                elif name == self.names[6]:
                    name.setText('Номер телефона')
                elif name == self.names[7]:
                    name.setText('E-mail')
                else:
                    name.setText('Продолжительность учебный день')

    def change1(self):
        if not self.time_course.isEnabled():
            self.check()
            self.time_course.setEnabled(True)
            self.time_course.setText('')
            self.time_course.setFocus()

    def change2(self):
        if not self.name_surname.isEnabled():
            self.check()
            self.name_surname.setEnabled(True)
            self.name_surname.setText('')
            self.name_surname.setFocus()

    def change3(self):
        if not self.start.isEnabled():
            self.check()
            self.start.setEnabled(True)
            self.start.setText('')
            self.start.setFocus()

    def change4(self):
        if not self.end.isEnabled():
            self.check()
            self.end.setEnabled(True)
            self.end.setText('')
            self.end.setFocus()

    def change5(self):
        if not self.organization.isEnabled():
            self.check()
            self.organization.setEnabled(True)
            self.organization.setText('')
            self.organization.setFocus()

    def change6(self):
        if not self.contract.isEnabled():
            self.check()
            self.contract.setEnabled(True)
            self.contract.setText('')
            self.contract.setFocus()

    def change7(self):
        if not self.phone.isEnabled():
            self.check()
            self.phone.setEnabled(True)
            self.phone.setText('')
            self.phone.setFocus()

    def change8(self):
        if not self.mail.isEnabled():
            self.check()
            self.mail.setEnabled(True)
            self.mail.setText('')
            self.mail.setFocus()

    def change9(self):
        if not self.time_days.isEnabled():
            self.check()
            self.time_days.setEnabled(True)
            self.time_days.setText('')
            self.time_days.setFocus()

    def registration(self):
        global main_window, users_registration, id, FIO, email, phone, NAPR, Start, end, courses, HOUR, dog, org
        with open('user_info.csv', 'a', encoding='utf-8') as file:
            # file.write('\n')
            if self.ceep.isEnabled():
                file.write(f'\n"{int(id[-1]) + 1}";"{self.name_surname.text().split()[0]} '
                           f'{self.name_surname.text().split()[1][0].capitalize()}.'
                           f'{self.name_surname.text().split()[2][0].capitalize()}";'
                           f'"{self.direction.currentText()}";"{self.ceep.currentText()}";"{self.time_course.text()}";'
                           f'"{self.time_days.text()}";"{self.start.text()}";"{self.end.text()}";'
                           f'"{self.organization.text()}";"{self.contract.text()}";"{self.phone.text()}";'
                           f'"{self.mail.text()}"')
            elif self.fire_ceep.isEnabled():
                file.write(f'\n"{int(id[-1]) + 1}";"{self.name_surname.text().split()[0]} '
                           f'{self.name_surname.text().split()[1][0].capitalize()}.'
                           f'{self.name_surname.text().split()[2][0].capitalize()}";'
                           f'"{self.direction.currentText()}";"{self.fire_ceep.currentText()}";"{self.time_course.text()}";'
                           f'"{self.time_days.text()}";"{self.start.text()}";"{self.end.text()}";'
                           f'"{self.organization.text()}";"{self.contract.text()}";"{self.phone.text()}";'
                           f'"{self.mail.text()}"')
            elif self.human_ceep.isEnabled():
                file.write(f'\n"{int(id[-1]) + 1}";"{self.name_surname.text().split()[0]} '
                           f'{self.name_surname.text().split()[1][0].capitalize()}.'
                           f'{self.name_surname.text().split()[2][0].capitalize()}";'
                           f'"{self.direction.currentText()}";"{self.human_ceep.currentText()}";"{self.time_course.text()}";'
                           f'"{self.time_days.text()}";"{self.start.text()}";"{self.end.text()}";'
                           f'"{self.organization.text()}";"{self.contract.text()}";"{self.phone.text()}";'
                           f'"{self.mail.text()}"')
            elif self.eco_ceep.isEnabled():
                file.write(f'\n"{int(id[-1]) + 1}";"{self.name_surname.text().split()[0]} '
                           f'{self.name_surname.text().split()[1][0].capitalize()}.'
                           f'{self.name_surname.text().split()[2][0].capitalize()}";'
                           f'"{self.direction.currentText()}";"{self.eco_ceep.currentText()}";"{self.time_course.text()}";'
                           f'"{self.time_days.text()}";"{self.start.text()}";"{self.end.text()}";'
                           f'"{self.organization.text()}";"{self.contract.text()}";"{self.phone.text()}";'
                           f'"{self.mail.text()}"')
            elif self.industry_ceep.isEnabled():
                file.write(f'\n"{int(id[-1]) + 1}";"{self.name_surname.text().split()[0]} '
                           f'{self.name_surname.text().split()[1][0].capitalize()}.'
                           f'{self.name_surname.text().split()[2][0].capitalize()}";'
                           f'"{self.direction.currentText()}";"{self.course.currentText()}";"{self.time_course.text()}";'
                           f'"{self.time_days.text()}";"{self.start.text()}";"{self.end.text()}";'
                           f'"{self.organization.text()}";"{self.contract.text()}";"{self.phone.text()}";'
                           f'"{self.mail.text()}"')
            file.close()

        with open('user_info.csv', 'r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=';')
            user_info = list(reader)[1:]
        file.close()

        id.clear()
        FIO.clear()
        NAPR.clear()
        courses.clear()
        PROD.clear()
        HOUR.clear()
        Start.clear()
        end.clear()
        org.clear()
        dog.clear()
        phone.clear()
        email.clear()

        for i in range(len(user_info)):
            id.append(user_info[i][0])
            FIO.append(user_info[i][1])
            NAPR.append(user_info[i][2])
            courses.append(user_info[i][3])
            PROD.append(user_info[i][4])
            HOUR.append(user_info[i][5])
            Start.append(user_info[i][6])
            end.append(user_info[i][7])
            org.append(user_info[i][8])
            dog.append(user_info[i][9])
            phone.append(user_info[i][10])
            email.append(user_info[i][11])
        self.sender()
        main_window = MainWindow()
        users_registration.hide()
        main_window.show()

    def back1(self):
        global main_window, users_registration
        users_registration.hide()
        main_window = MainWindow()
        main_window.show()

    def sender(self):
        if self.ceep.isEnabled():
            message = f'Здравствуйте, {self.name_surname.text().split()[1].lower().capitalize()}!\n' \
                      f'Вы были успешно зарегистрированы на курс "{self.ceep.currentText().lower().capitalize()}"' \
                      f' в направлении ' \
                      f'"{self.direction.currentText()}". \n' \
                      f'Вы можете приступать к обучению {self.start.text()}.\n' \
                      f'Продолжительность курса составляет {self.time_course.text()} часа.\n' \
                      f'Время обучения в день: {self.time_days.text()} часа.\n' \
                      f'Предварительная дата окнчания обучения планируется на {self.end.text()} (при возникновении' \
                      f'уважительных причин дата может быть изменена, для этого свяжитесь с администратором).\n' \
                      f'Номер вашего договора: {self.contract.text()}.\n' \
                      f'Указаная организация: {self.organization.text()}.\n' \
                      f'Спасибо, что решили воспользоваться нашими услугами, желаем вам удачи!'
        elif self.fire_ceep.isEnabled():
            message = f'Здравствуйте, {self.name_surname.text().split()[1].lower().capitalize()}!\n' \
                      f'Вы были успешно зарегистрированы на курс "{self.fire_ceep.currentText().lower().capitalize()}"' \
                      f' в направлении ' \
                      f'"{self.direction.currentText()}". \n' \
                      f'Вы можете приступать к обучению {self.start.text()}.\n' \
                      f'Продолжительность курса составляет {self.time_course.text()} часа.\n' \
                      f'Время обучения в день: {self.time_days.text()} часа.\n' \
                      f'Предварительная дата окнчания обучения планируется на {self.end.text()} (при возникновении' \
                      f'уважительных причин дата может быть изменена, для этого свяжитесь с администратором).\n' \
                      f'Номер вашего договора: {self.contract.text()}.\n' \
                      f'Указаная организация: {self.organization.text()}.\n' \
                      f'Спасибо, что решили воспользоваться нашими услугами, желаем вам удачи!'
        elif self.human_ceep.isEnabled():
            message = f'Здравствуйте, {self.name_surname.text().split()[1].lower().capitalize()}!\n' \
                      f'Вы были успешно зарегистрированы на курс "{self.human_ceep.currentText().lower().capitalize()}"' \
                      f' в направлении ' \
                      f'"{self.direction.currentText()}". \n' \
                      f'Вы можете приступать к обучению {self.start.text()}.\n' \
                      f'Продолжительность курса составляет {self.time_course.text()} часа.\n' \
                      f'Время обучения в день: {self.time_days.text()} часа.\n' \
                      f'Предварительная дата окнчания обучения планируется на {self.end.text()} (при возникновении' \
                      f'уважительных причин дата может быть изменена, для этого свяжитесь с администратором).\n' \
                      f'Номер вашего договора: {self.contract.text()}.\n' \
                      f'Указаная организация: {self.organization.text()}.\n' \
                      f'Спасибо, что решили воспользоваться нашими услугами, желаем вам удачи!'
        elif self.eco_ceep.isEnabled():
            message = f'Здравствуйте, {self.name_surname.text().split()[1].lower().capitalize()}!\n' \
                      f'Вы были успешно зарегистрированы на курс "{self.eco_ceep.currentText().lower().capitalize()}"' \
                      f' в направлении ' \
                      f'"{self.direction.currentText()}". \n' \
                      f'Вы можете приступать к обучению {self.start.text()}.\n' \
                      f'Продолжительность курса составляет {self.time_course.text()} часа.\n' \
                      f'Время обучения в день: {self.time_days.text()} часа.\n' \
                      f'Предварительная дата окнчания обучения планируется на {self.end.text()} (при возникновении' \
                      f'уважительных причин дата может быть изменена, для этого свяжитесь с администратором).\n' \
                      f'Номер вашего договора: {self.contract.text()}.\n' \
                      f'Указаная организация: {self.organization.text()}.\n' \
                      f'Спасибо, что решили воспользоваться нашими услугами, желаем вам удачи!'
        elif self.industry_ceep.isEnabled():
            message = f'Здравствуйте, {self.name_surname.text().split()[1].lower().capitalize()}!\n' \
                      f'Вы были успешно зарегистрированы на курс "{self.industry_ceep.currentText().lower().capitalize()}"' \
                      f' в направлении ' \
                      f'"{self.direction.currentText()}". \n' \
                      f'Вы можете приступать к обучению {self.start.text()}.\n' \
                      f'Продолжительность курса составляет {self.time_course.text()} часа.\n' \
                      f'Время обучения в день: {self.time_days.text()} часа.\n' \
                      f'Предварительная дата окнчания обучения планируется на {self.end.text()} (при возникновении' \
                      f'уважительных причин дата может быть изменена, для этого свяжитесь с администратором).\n' \
                      f'Номер вашего договора: {self.contract.text()}.\n' \
                      f'Указаная организация: {self.organization.text()}.\n' \
                      f'Спасибо, что решили воспользоваться нашими услугами, желаем вам удачи!'

        sender = "noreply.centerobr@gmail.com"
        password = "omwbbkwdwqclebxt"
        getters = self.mail.text()
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        try:
            server.login(sender, password)
            msg = MIMEText(message)
            msg["Subject"] = "ОБУЧЕНИЕ"
            server.sendmail(sender, getters, msg.as_string())

            return "The message was sent successfully!"
        except Exception as _ex:
            return f"{_ex}\nCheck your login or password please!"


if __name__ == '__main__':
    app = QApplication(sys.argv)
    application = EnterWindow()
    application.setStyleSheet('background-color: black; font-family: "Lato"; font-size: 16px;')
    application.setFixedSize(575, 590)
    application.show()
    sys.exit(app.exec_())
