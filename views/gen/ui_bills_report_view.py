# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'res/bills_report.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_bills_report_view(object):
    def setupUi(self, bills_report_view):
        bills_report_view.setObjectName("bills_report_view")
        bills_report_view.resize(677, 408)
        self.centralwidget = QtWidgets.QWidget(bills_report_view)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.dateEdit_begin = QtWidgets.QDateEdit(self.centralwidget)
        self.dateEdit_begin.setObjectName("dateEdit_begin")
        self.verticalLayout.addWidget(self.dateEdit_begin)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.dateEdit_end = QtWidgets.QDateEdit(self.centralwidget)
        self.dateEdit_end.setObjectName("dateEdit_end")
        self.verticalLayout.addWidget(self.dateEdit_end)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.comboBox_type = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_type.setObjectName("comboBox_type")
        self.comboBox_type.addItem("")
        self.comboBox_type.addItem("")
        self.verticalLayout.addWidget(self.comboBox_type)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.verticalLayout.addWidget(self.label_5)
        self.plainTextEdit_result = QtWidgets.QPlainTextEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plainTextEdit_result.sizePolicy().hasHeightForWidth())
        self.plainTextEdit_result.setSizePolicy(sizePolicy)
        self.plainTextEdit_result.setMaximumSize(QtCore.QSize(200, 16777215))
        self.plainTextEdit_result.setReadOnly(True)
        self.plainTextEdit_result.setObjectName("plainTextEdit_result")
        self.verticalLayout.addWidget(self.plainTextEdit_result)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.pushButton_create = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_create.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("res/imgs/contract.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_create.setIcon(icon)
        self.pushButton_create.setObjectName("pushButton_create")
        self.verticalLayout.addWidget(self.pushButton_create)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_2.addWidget(self.label_6)
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setObjectName("tableView")
        self.verticalLayout_2.addWidget(self.tableView)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        bills_report_view.setCentralWidget(self.centralwidget)

        self.retranslateUi(bills_report_view)
        QtCore.QMetaObject.connectSlotsByName(bills_report_view)

    def retranslateUi(self, bills_report_view):
        _translate = QtCore.QCoreApplication.translate
        bills_report_view.setWindowTitle(_translate("bills_report_view", "Отчет"))
        self.label.setText(_translate("bills_report_view", "Отчет"))
        self.label_2.setText(_translate("bills_report_view", "Начало периода:"))
        self.dateEdit_begin.setDisplayFormat(_translate("bills_report_view", "yyyy-MM-dd"))
        self.label_3.setText(_translate("bills_report_view", "Конец периода:"))
        self.dateEdit_end.setDisplayFormat(_translate("bills_report_view", "yyyy-MM-dd"))
        self.label_4.setText(_translate("bills_report_view", "Тип расчета:"))
        self.comboBox_type.setItemText(0, _translate("bills_report_view", "Доходы"))
        self.comboBox_type.setItemText(1, _translate("bills_report_view", "Расходы"))
        self.label_5.setText(_translate("bills_report_view", "Результат:"))
        self.pushButton_create.setText(_translate("bills_report_view", "Создать отчет"))
        self.label_6.setText(_translate("bills_report_view", "Выписка:"))
