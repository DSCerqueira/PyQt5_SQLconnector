from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from Connect_dtb_MySQL import Ui_MainWindow
from chart_mysql import Ui_plot_ch
from CreateTbt import Ui_creatingTbl
import sys
import mysql.connector as msq
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import numpy as np



class mywindow(QtWidgets.QMainWindow):

    def __init__(self):

        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        #######################click buttons#########################
        self.ui.connect_bt.clicked.connect(self.connectar)
        self.ui.comboBox_dtb.currentIndexChanged.connect(self.tablelist)
        self.ui.decb_tb_bt.clicked.connect(self.desc)
        self.ui.query_bt.clicked.connect(self.rquery)
        self.ui.disconnect_bt.clicked.connect(self.discon)
        self.ui.expt_csv_bt.clicked.connect(self.exportcsv)
        self.ui.import_tb_bt.clicked.connect(self.importcsv)
        self.ui.crt_tbt_bt.clicked.connect(self.create_dtb)
        self.ui.chart_bt.clicked.connect(self.chart)
        self.ui.exit_bt.clicked.connect(self.closewindow)

    ################body functions##############################

    def connectar(self):
        self.user = self.ui.lineEdit_user.text()
        self.hostn = self.ui.lineEdit_host.text()
        self.passd = self.ui.lineEdit_pass.text()

        try:
            global cnx
            cnx = msq.connect(user=self.user, host=self.hostn, password=self.passd, auth_plugin='mysql_native_password')
            self.ui.connect_St.setText('Conexão Ok!')
            self.cursor = cnx.cursor()
            self.cursor.execute('show databases;')
            self.dtbs = self.cursor.fetchall()
            self.ui.lineEdit_user.enable = 'False'

            for i in self.dtbs:
                for n in i:
                    self.ui.comboBox_dtb.addItem(n)

        except msq.Error as err:
            erroname='Connection failed.\n'+str(err)
            self.mesg=QMessageBox.information(self,'Connection Failed',erroname)

        else:
            cursor = cnx.cursor()

    def tablelist(self):
        try:
            self.cursor = cnx.cursor()
            self.cursor.execute('use ' + self.ui.comboBox_dtb.currentText() + ';')
            self.cursor.execute('show tables;')
            self.tbdtb = self.cursor.fetchall()
            self.ui.table_tbt.setColumnCount(1)  # add collumns
            self.ui.table_tbt.setRowCount(len(self.tbdtb))
            self.ui.table_tbt.setHorizontalHeaderLabels(('Existing Tables',))  # set header text

            row = 0
            for i in self.tbdtb:
                col = 0
                for n in i:
                    cellinfo = QtWidgets.QTableWidgetItem(n)
                    self.ui.table_tbt.setItem(row, col, cellinfo)
                    col = col + 1
                row += 1

        except:
            pass

    def desc(self):
        try:
            self.cursor = cnx.cursor()
            self.row = self.ui.table_tbt.currentRow()
            self.col = self.ui.table_tbt.currentColumn()
            self.tbl = self.ui.table_tbt.item(self.row, self.col).text()
            self.cursor.execute('desc ' + self.tbl + ';')
            self.tbdtb = self.cursor.fetchall()
            self.ui.out_tbt.setRowCount(len(self.tbdtb))
            self.ui.out_tbt.setColumnCount(len(self.tbdtb[0]))

            row = 0
            for i in self.tbdtb:
                col = 0
                for n in i:
                    cellinfo = QtWidgets.QTableWidgetItem(n)
                    self.ui.out_tbt.setItem(row, col, cellinfo)
                    col = col + 1
                row += 1
            ncol = self.cursor.column_names
            self.ui.out_tbt.setHorizontalHeaderLabels(ncol)
        except:
            pass

    def rquery(self):
        try:
            self.cursor = cnx.cursor()
            self.sql = self.ui.query_edt.toPlainText()
            self.cursor.execute(self.sql)
            self.tbdtb = self.cursor.fetchall()
            self.ui.out_tbt.setRowCount(len(self.tbdtb))
            self.ui.out_tbt.setColumnCount(len(self.tbdtb[0]))

            row = 0
            for i in self.tbdtb:
                col = 0
                for n in i:
                    cellinfo = QtWidgets.QTableWidgetItem(str(n))
                    self.ui.out_tbt.setItem(row, col, cellinfo)
                    col = col + 1
                row += 1
            ncol = self.cursor.column_names
            self.ui.out_tbt.setHorizontalHeaderLabels(ncol)

        except:
            pass

    def discon(self):
        try:
            cnx.close()
            self.ui.label_7.setText('Disconnected!')
            self.ui.comboBox_dtb.clear()
            self.ui.table_tbt.clear()
            self.ui.out_tbt.clear()
            self.ui.query_edt.clear()
        except:
            self.ui.comboBox_dtb.clear()
            self.ui.table_tbt.clear()
            self.ui.out_tbt.clear()
            self.ui.query_edt.clear()

    def exportcsv(self):

        try:
            x = self.ui.out_tbt.rowCount()
            y = self.ui.out_tbt.columnCount()

            self.row = 0
            self.data = []
            for i in range(x):
                self.col = 0
                self.rowdata = []
                for n in range(y):
                    self.rowdata.append(self.ui.out_tbt.item(i, n).text())
                    self.col += 1
                self.data.append(self.rowdata)
                self.row += 1

            self.cols = []
            for n in range(y):
                self.cols.append(self.ui.out_tbt.horizontalHeaderItem(n).text())

            self.data = pd.DataFrame(self.data, columns=list(self.cols))
            pathl = sys.path
            print(pathl)
            self.name = QInputDialog.getText(self,'ExportFile','Enter filename:')
            self.name=self.name[0]
            self.pathfile = pathl[0] + '\\' + self.name + '.csv'
            self.data.to_csv(self.pathfile, index=False)
        except:
            pass

    def importcsv(self):

        try:
            fname= QFileDialog()
            fname.setFileMode(QFileDialog.AnyFile)
            fname.setNameFilter('CSV files (*.csv)')
            if fname.exec_():
                self.fname=fname.selectedFiles()
                self.dataframe=pd.read_csv(self.fname[0])
                self.dataframe=pd.DataFrame(self.dataframe)

            dima=np.shape(self.dataframe)
            self.ui.out_tbt.setRowCount(dima[0])
            self.ui.out_tbt.setColumnCount(dima[1])
            self.ui.out_tbt.setHorizontalHeaderLabels(self.dataframe.columns)

            row = 0
            for i in range(dima[0]):
                col = 0
                for n in list(self.dataframe.loc[i]):
                    cellinfo = QtWidgets.QTableWidgetItem(str(n))
                    self.ui.out_tbt.setItem(row, col, cellinfo)
                    col = col + 1
                row += 1

        except:
            pass

    def create_dtb(self):
        #try:
            x = self.ui.out_tbt.rowCount()
            y = self.ui.out_tbt.columnCount()

            self.row = 0
            self.data = []
            for i in range(x):
                self.col = 0
                self.rowdata = []
                for n in range(y):
                    self.rowdata.append(self.ui.out_tbt.item(i, n).text())
                    self.col += 1
                self.data.append(self.rowdata)
                self.row += 1

            self.cols = []
            for n in range(y):
                self.cols.append(self.ui.out_tbt.horizontalHeaderItem(n).text())

            self.data = pd.DataFrame(self.data, columns=list(self.cols))

            self.tablemysql=create_tbl(self.data,self.ui.out_tbt)
            self.tablemysql.show()

    def chart(self):
        x = self.ui.out_tbt.rowCount()
        y = self.ui.out_tbt.columnCount()

        self.row = 0
        self.data = []
        for i in range(x):
            self.col = 0
            self.rowdata = []
            for n in range(y):
                self.rowdata.append(self.ui.out_tbt.item(i, n).text())
                self.col += 1
            self.data.append(self.rowdata)
            self.row += 1

        self.cols = []
        for n in range(y):
            self.cols.append(self.ui.out_tbt.horizontalHeaderItem(n).text())

        self.data = pd.DataFrame(self.data, columns=list(self.cols))

        self.callchart=mychart(self.data,self.ui.out_tbt)

    def closewindow(self):
        sys.exit()

class create_tbl(QtWidgets.QMainWindow):

    def __init__(self,data,tbwidget,parent=None):
        super(create_tbl,self).__init__(parent)
        self.uimtable = Ui_creatingTbl()
        self.uimtable.setupUi(self)
        self.data=data
        self.tableout=tbwidget
        self.tableout.setEnabled(False)
        ###################click buttons#############
        self.uimtable.CertaTbt_bt.clicked.connect(self.crtable_mysql)
        self.uimtable.Canceltbt_bt.clicked.connect(self.closewind)
        self.variables=list(self.data.columns)
        self.colunalengh=len(self.variables)
        self.uimtable.TableVr.setRowCount(self.colunalengh)
        self.uimtable.TableVr.setColumnCount(3)
        self.uimtable.TableVr.setHorizontalHeaderLabels(('Columns','Variable Type','Add Y/N?'))
        self.variablesql = ['CHAR( )', 'VARCHAR( )', 'TINYTEXT', 'TEXT', 'BLOB', 'MEDIUMTEXT', 'MEDIUMBLOB', 'LONGTEXT',
                            'LONGBLOB', 'TINYINT ( )', 'SMALLINT( )', 'MEDIUMINT( )', 'INT( )', 'BIGINT( )', 'FLOAT',
                            'DOUBLE( , )', 'DECIMAL( , )', 'DATE', 'DATETIME', 'TIMESTAMP', 'TIME', 'YEAR']

        row = 0
        for i in self.variables:
            cellinfo = QtWidgets.QTableWidgetItem(str(i))
            self.uimtable.TableVr.setItem(row, 0, cellinfo)
            combo = QComboBox()
            combo.setEditable(True)

            comboyesno=QComboBox()
            comboyesno.addItem('Yes')
            comboyesno.addItem('No')

            for n in self.variablesql:
                combo.addItem(n)
            self.uimtable.TableVr.setCellWidget(row,1,combo)
            self.uimtable.TableVr.setCellWidget(row, 2, comboyesno)
            row += 1

    def crtable_mysql(self):
        try:
            self.colvariable=[]
            self.listcol=[]
            self.listvariable=[]

            for i in range(self.colunalengh):
                if self.uimtable.TableVr.cellWidget(i,2).currentText()=='Yes':
                    self.listcol.append(i)
                    self.listvariable.append(self.uimtable.TableVr.cellWidget(i,1).currentText())
                    self.colvariable.append(self.uimtable.TableVr.item(i,0).text())

            self.tablename=QInputDialog.getText(self,'Table name','Enter name Table:')
            self.strquery='('
            for i in range(len(self.listcol)-1):
                self.strquery=self.strquery+self.colvariable[i]+' '+self.listvariable[i]+','
            self.strquery=self.strquery+self.colvariable[len(self.listcol)-1]+' '+self.listvariable[len(self.listcol)-1]+');'
            self.query='CREATE TABLE '+self.tablename[0]+' '+self.strquery
            print(self.query)
            self.cursor = cnx.cursor()
            print('bola')
            try:
                print('zaul')
                self.cursor.execute(self.query)
                self.mesg=QMessageBox.information(self,'Creating Table','Table '+self.tablename[0]+' created.')
            except msq.Error as err:
                erroname = 'Table creation failed.\n' + str(err)
                self.mesg = QMessageBox.information(self, 'Erro', erroname)

            self.strquery='('
            for i in range(len(self.listcol)-1):
                self.strquery=self.strquery+self.colvariable[i]+','
            self.strquery=self.strquery+self.colvariable[len(self.listcol)-1]+') VALUES '
            print('casa2')
            print(self.strquery)


            self.strvalues='('
            laco=np.shape(self.data)
            jump=laco[0]+1
            print(jump)

            lm=0
            for i in range(jump):
                lm=lm+1
                print(lm)
                linedata=self.data.loc[i]
                colcolect='('
                for n in range(len(self.listcol)-1):
                    colset=self.listcol[n]
                    colcolect=colcolect + '"' + str(linedata[colset]) + '"' + ','
                colcolect=colcolect+'"'+str(linedata[self.listcol[len(self.listcol)-1]])+'")'
                strqueryq = 'INSERT INTO ' + self.tablename[0] + ' ' + self.strquery +colcolect+';'
                print(strqueryq)
                try:
                    self.cursor = cnx.cursor()
                    self.cursor.execute(strqueryq)
                    #self.mesg = QMessageBox.information(self, 'Creating table','Values load into table ' + self.tablename[0])

                except msq.Error as err:
                    erroname = 'Table creation failed.\n' + str(err)
                    self.mesg = QMessageBox.information(self, 'Erro', 'Data insertion failed. \n' + erroname)

        except:
            pass
    def closewind(self):
        self.close()
    def closeEvent(self, event):
        self.tableout.setEnabled(True)

class mychart(QtWidgets.QMainWindow):
    def __init__(self,data,tbwdiget,parent=None):
        super(mychart,self).__init__(parent)
        self.uichart=Ui_plot_ch()
        self.uichart.setupUi(self)
        self.data=data
        self.tbforeing=tbwdiget
        self.uichart.charttable.setColumnCount(3)
        self.uichart.charttable.setHorizontalHeaderLabels(('X Variable','Y Variable','Chart Name'))

  #########################################################################################
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        layout = self.uichart.ChartVlay
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.matrizchart = []  ######chart array#####
        self.krow = 0 ############row table counter

        self.show()

#############click buttons#########################################################
        self.uichart.Linear_Bt.clicked.connect(self.linearchart)
        self.uichart.chart_add_bt.clicked.connect(self.addfunction)
        self.uichart.Removevar.clicked.connect(self.removevar)
        self.uichart.Bar_bt.clicked.connect(self.barchart)

###################loading table#########################################################
        self.frame = pd.DataFrame(self.data)
        ncol = list(self.frame.columns)
        for i in ncol:
            self.uichart.VarX_cb.addItem(i)
            self.uichart.VarY_cb.addItem(i)
        nl = self.frame.shape[0]
        cl = self.frame.shape[1]

##############################Funcitons ###################################################################

    def addfunction(self):
        self.uichart.charttable.setRowCount(self.krow+1)
        self.colnX = self.uichart.VarX_cb.currentText()
        self.colnY = self.uichart.VarY_cb.currentText()
        self.chartname = self.uichart.Chartname.text()
        cellinfoX = QtWidgets.QTableWidgetItem(str(self.colnX))
        self.uichart.charttable.setItem(self.krow, 0, cellinfoX)
        cellinfoY = QtWidgets.QTableWidgetItem(str(self.colnY))
        self.uichart.charttable.setItem(self.krow, 1, cellinfoY)
        cellinfoname = QtWidgets.QTableWidgetItem(str(self.chartname))
        self.uichart.charttable.setItem(self.krow, 2, cellinfoname)
        self.krow += 1

    def removevar(self):
        rowdel=self.uichart.charttable.currentRow()
        self.uichart.charttable.removeRow(rowdel)

        if self.krow>0:
            self.krow=self.krow-1


    def linearchart(self):
        self.figure.clear()
        ax=self.figure.subplots()
        self.chartname = self.uichart.Chartitle.text()
        self.axisXname = self.uichart.AxisXname.text()
        self.axisYname = self.uichart.AxisYname.text()
        maxax=0
        maxay=0
        for i in range(self.krow):
            self.colnX = self.uichart.charttable.item(i,0).text()
            self.colnY = self.uichart.charttable.item(i,1).text()
            self.namechartlist=self.uichart.charttable.item(i, 2).text()

            self.varXlist = list(self.frame[self.colnX])
            self.varXlist = [float(i) for i in  self.varXlist]
            self.varYlist = list(self.frame[self.colnY])
            self.varYlist = [float(i) for i in self.varYlist]
            self.namelist = str(self.namechartlist)
            ax.plot(self.varXlist,self.varYlist,label=str(self.namechartlist))

        ax.set_title(self.chartname)
        ax.set_xlabel(self.axisXname)
        ax.set_ylabel(self.axisYname)

        self.canvas.draw()
    def barchart(self):
        self.figure.clear()
        ax = self.figure.subplots()
        self.chartname = self.uichart.Chartitle.text()
        self.axisXname=self.uichart.AxisXname.text()
        self.axisYname = self.uichart.AxisYname.text()
        nchart=0
        kn=1

        for i in range(self.krow):

            self.colnX = self.uichart.charttable.item(i,0).text()
            self.colnY = self.uichart.charttable.item(i,1).text()
            self.namechartlist=self.uichart.charttable.item(i, 2).text()
            self.varXlist = list(self.frame[self.colnX])
            self.varYlist = list(self.frame[self.colnY])
            self.varYlist = [float(i) for i in self.varYlist]
            self.namelist = str(self.namechartlist)
            self.width=(1-0.2)/self.krow

            x = np.arange(len(self.varXlist))
            ax.bar(x-kn*nchart*self.width/2,self.varYlist,self.width,label=str(self.namechartlist))
            nchart=nchart+1
            kn=kn*(-1)
            print(self.namechartlist)

        ax.set_title(self.chartname)
        ax.set_xlabel(self.axisXname)
        ax.set_ylabel(self.axisYname)
        ax.set_xticks(x)
        ax.set_xticklabels(self.varXlist)
        self.canvas.draw()


        #self.varX=list(self.frame[self.colnX])
        #self.varY = list(self.frame[self.colnY])
        #ax = self.figure.add_subplot(111)
        #ax.plot(self.varX,self.varY)
        #ax.plot.title(self.uichart.Chartitle.text())
        #print(self.colnX)

        #self.canvas.draw()


    def closeEvent(self, event):
        self.tbforeing.setEnabled(True)

app = QtWidgets.QApplication([])

application = mywindow()

application.show()

sys.exit(app.exec())