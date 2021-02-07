# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CreateTbt.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_creatingTbl(object):
    def setupUi(self, creatingTbl):
        creatingTbl.setObjectName("creatingTbl")
        creatingTbl.resize(413, 569)
        creatingTbl.setMinimumSize(QtCore.QSize(105, 125))
        creatingTbl.setMaximumSize(QtCore.QSize(413, 569))
        self.centralwidget = QtWidgets.QWidget(creatingTbl)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.TableVr = QtWidgets.QTableWidget(self.centralwidget)
        self.TableVr.setObjectName("TableVr")
        self.TableVr.setColumnCount(0)
        self.TableVr.setRowCount(0)
        self.verticalLayout.addWidget(self.TableVr)
        self.CertaTbt_bt = QtWidgets.QPushButton(self.centralwidget)
        self.CertaTbt_bt.setObjectName("CertaTbt_bt")
        self.verticalLayout.addWidget(self.CertaTbt_bt)
        self.Canceltbt_bt = QtWidgets.QPushButton(self.centralwidget)
        self.Canceltbt_bt.setObjectName("Canceltbt_bt")
        self.verticalLayout.addWidget(self.Canceltbt_bt)
        creatingTbl.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(creatingTbl)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 413, 21))
        self.menubar.setObjectName("menubar")
        creatingTbl.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(creatingTbl)
        self.statusbar.setObjectName("statusbar")
        creatingTbl.setStatusBar(self.statusbar)

        self.retranslateUi(creatingTbl)
        QtCore.QMetaObject.connectSlotsByName(creatingTbl)

    def retranslateUi(self, creatingTbl):
        _translate = QtCore.QCoreApplication.translate
        creatingTbl.setWindowTitle(_translate("creatingTbl", "Creating Table MySQL"))
        self.CertaTbt_bt.setText(_translate("creatingTbl", "Create Table"))
        self.Canceltbt_bt.setText(_translate("creatingTbl", "Cancel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    creatingTbl = QtWidgets.QMainWindow()
    ui = Ui_creatingTbl()
    ui.setupUi(creatingTbl)
    creatingTbl.show()
    sys.exit(app.exec_())
