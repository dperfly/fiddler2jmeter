# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!

import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog

from code.start import run


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 521)
        MainWindow.setWindowTitle("Fiddler or Charles Convert to jmeter Script")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.cmd_result = QtWidgets.QTextEdit(self.centralwidget)
        self.cmd_result.setGeometry(QtCore.QRect(10, 240, 781, 251))
        self.cmd_result.setObjectName("cmd_result")

        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 779, 249))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 20, 180, 16))
        self.label_3.setObjectName("label_3")
        self.select_input_textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.select_input_textEdit.setGeometry(QtCore.QRect(180, 10, 500, 31))
        self.select_input_textEdit.setObjectName("select_input_textEdit")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(10, 70, 200, 16))
        self.label_4.setObjectName("label_4")
        self.select_output_textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.select_output_textEdit.setGeometry(QtCore.QRect(180, 60, 500, 31))
        self.select_output_textEdit.setObjectName("select_output_textEdit")

        # 添加去重复选框
        self.select_distinct_path = QtWidgets.QCheckBox(self.centralwidget)
        self.select_distinct_path.setGeometry(QtCore.QRect(180, 193, 30, 35))
        self.select_distinct_path.setObjectName("select_distinct")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(200, 205, 500, 15))
        self.label_5.setObjectName("label_5")

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 170, 151, 16))
        self.label_2.setObjectName("label_2")
        self.host_name_textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.host_name_textEdit.setGeometry(QtCore.QRect(180, 120, 500, 31))
        self.host_name_textEdit.setObjectName("host_name_textEdit")
        self.filter_url_textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.filter_url_textEdit.setGeometry(QtCore.QRect(180, 160, 500, 31))
        self.filter_url_textEdit.setObjectName("filter_url_textEdit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 130, 151, 16))
        self.label.setObjectName("label")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(0, 100, 801, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(0, 220, 801, 16))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.run = QtWidgets.QPushButton(self.centralwidget)
        self.run.setGeometry(QtCore.QRect(700, 130, 75, 51))
        self.run.setObjectName("run")
        self.select_input_btn = QtWidgets.QPushButton(self.centralwidget)
        self.select_input_btn.setGeometry(QtCore.QRect(700, 10, 75, 31))
        self.select_input_btn.setObjectName("select_input_btn")

        self.select_output_btn = QtWidgets.QPushButton(self.centralwidget)
        self.select_output_btn.setGeometry(QtCore.QRect(700, 60, 75, 31))
        self.select_output_btn.setObjectName("select_output_btn")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_fiddler = QtWidgets.QAction(MainWindow)
        self.action_fiddler.setCheckable(True)
        self.action_fiddler.setObjectName("action_fiddler")
        self.action_3 = QtWidgets.QAction(MainWindow)
        self.action_3.setCheckable(True)
        self.action_3.setObjectName("action_3")
        self.action_jmeter_4_0 = QtWidgets.QAction(MainWindow)
        self.action_jmeter_4_0.setCheckable(True)
        self.action_jmeter_4_0.setObjectName("action_jmeter_4_0")
        self.menu.addAction(self.action_fiddler)
        self.menu.addAction(self.action_3)
        self.menu.addSeparator()
        self.menu.addAction(self.action_jmeter_4_0)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.select_input_btn.clicked.connect(self.select_input_file)
        self.select_output_btn.clicked.connect(self.select_output_file)
        self.filter_url_textEdit.setText(R"/(.*)\.(css|ico|jpg|png|gif|bmp|wav|js|jpe)(\?.*)?$")
        self.host_name_textEdit.setText(R"^.*$")
        self.run.clicked.connect(self.run_script)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_3.setText(_translate("MainWindow",
                                        "<html><head/><body><p><span style=\" font-size:10pt;\">* 导入Fiddler/Charles文件</span></p></body></html>"))
        self.label_4.setText(_translate("MainWindow",
                                        "<html><head/><body><p><span style=\" font-size:10pt;\">* 导出文件或覆盖jmx文件</span></p></body></html>"))
        self.label_2.setText(_translate("MainWindow",
                                        "<html><head/><body><p><span style=\" font-size:10pt;\">* 过滤请求类型正则匹配</span></p></body></html>"))
        self.label.setText(_translate("MainWindow",
                                      "<html><head/><body><p><span style=\" font-size:10pt;\">* 过滤host正则匹配</span></p></body></html>"))
        self.label_5.setText(_translate("MainWindow",
                                        "<html><head/><body><p><span style=\" font-size:10pt;\"> 是否进行去重  注：请求URL后面跟的参数不同不会被去掉</span></p></body></html>"))
        self.run.setText(_translate("MainWindow", "RUN"))
        self.select_input_btn.setText(_translate("MainWindow", "选择文件"))
        self.select_output_btn.setText(_translate("MainWindow", "选择文件"))

        # 暂时用不到，隐藏
        # self.menu.setTitle(_translate("MainWindow", "文件"))
        # self.action_fiddler.setText(_translate("MainWindow", "导入Fiddler文件"))
        # self.action_fiddler.setChecked(True)
        # self.action_3.setText(_translate("MainWindow", "导入Charles文件(暂不支持)"))
        # self.action_3.setChecked(False)
        # self.action_jmeter_4_0.setText(_translate("MainWindow", "导出jmeter 4.0脚本"))
        # self.action_jmeter_4_0.setChecked(True)

    def select_input_file(self):
        openfile_name = QFileDialog.getOpenFileName(None, '选择文件', '', '')
        # print(openfile_name)
        self.select_input_textEdit.setText(openfile_name[0])

    def select_output_file(self):
        openfile_name = QFileDialog.getOpenFileName(None, '选择文件', '', '')
        # print(openfile_name)
        self.select_output_textEdit.setText(openfile_name[0])

    def run_script(self):
        filter_url = self.filter_url_textEdit.toPlainText()
        host_name = self.host_name_textEdit.toPlainText()
        input_file = self.select_input_textEdit.toPlainText()
        output_file = self.select_output_textEdit.toPlainText()
        is_distinct = self.select_distinct_path.isChecked()
        # print(filter_url, host_name, input_file, output_file)
        result = run(file_path=input_file, filter_url=filter_url, host_name=host_name,
                     output_jmxScript=output_file, distinct=is_distinct)
        self.cmd_result.setText(result)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
