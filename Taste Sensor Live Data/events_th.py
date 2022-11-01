from PyQt5 import QtCore, QtGui, QtWidgets
from datetime import datetime
import csv
from threading import Thread
from time import strftime
import matplotlib.pyplot as plt
from fetch_th import SerialData
import time


class Ui_Form(QtCore.QObject):
    
    dataChanged = QtCore.pyqtSignal(list,list,list,list,list,list,list)
    def __init__(self, parent=None):
        
        super(self.__class__, self).__init__(parent)
        self.inputList = []
        self.serialobj=SerialData()
        self.flag = 1
        self.s = 0
        self.m = 0
        self.h = 0
        self.serialobj=SerialData()
        
        #get the changed data from fetch_th.py and call function graph whenever 
        self.serialobj.dataChanged.connect(self.graph)#the data changes
        datim = (str(datetime.now())[:-10]).replace(':','_') #set current dat and time for filename
        self.filename = datim #setting filename
        
    def generateMeta(self): #generate metadata to be stored in the file
        self.metaDateTemp = self.dateEdit.date()# like date, time, Name, Conc,
        self.metaDate = self.metaDateTemp.toPyDate()#Solution etc, which are given by the 
        self.metaSolution = self.comboBox.currentText()#use in the gui [Check GUI]
        self.metaTimeTemp = self.timeEdit.time()
        self.metaTime = self.metaTimeTemp.toPyTime()
        self.metaName = self.lineEdit.text()
        self.metaConcentration = self.lineEdit_2.text()    
    
    def writeMeta(self): #write the collected metadata into the file
        with open(self.filename + str(".csv"),'a+',newline='') as f:
            writer=csv.writer(f)
            writer.writerow([])#write the metadata 
            writer.writerow(['Date','Solution','Time','Name','Concentration'])
            writer.writerow([self.metaDate,self.metaSolution,self.metaTime,self.metaName
                             ,self.metaConcentration])
            writer.writerow([])  
            writer.writerow(['S0','S1','S2','S3','S4','S5','S6'])#give headers for the sensors
            
    
    def writeSensorMeta(self):   #wrapper fucnction to generate and write metadata 
        self.generateMeta()
        self.writeMeta()
    
    #Graph function writes the latest sensor data to the file
    #and plots the sensor data on the graph in real time
    #graph function runs on a seperate python thread and
    #gets data from the fetch function in fetch_th.py
    def graph(self, sensor0, sensor1, sensor2, sensor3, sensor4, sensor5, sensor6):

        with open(self.filename + str(".csv"),'a+',newline='') as f:
               writer=csv.writer(f)
               writer.writerow([sensor0[-1],sensor1[-1],sensor2[-1],sensor3[-1],sensor4[-1],sensor5[-1],sensor6[-1],strftime("%Y-%m-%d"),strftime("%H:%M:%S")])
        
        plt.pause(0.00001)
        plt.title('Live Streaming Sensor Data')
        plt.grid(True)
        plt.ylabel('Sensor Data')
        if(self.serialobj.counter < 3):
            plt.legend(loc='upper left')
            
        if (self.serialobj.counter > 50): #check the maximum data plotted
            plt.clf()
            time.sleep(0.5)
            plt.grid(True)
            plt.title('Live Streaming Sensor Data')
            plt.grid(True)
            plt.ylabel('Sensor Data')    
            
        plt.plot(sensor0, label='Sensor 0')#plot the sensor data
        plt.plot(sensor1, label='Sensor 1')
        plt.plot(sensor2, label='Sensor 2')
        plt.plot(sensor3, label='Sensor 3')
        plt.plot(sensor4, label='Sensor 4')
        plt.plot(sensor5, label='Sensor 5')
        plt.plot(sensor6, label='Sensor 6')
        
            
    def Time(self): #functin to display the timer on the gui
                    #timer counts in revers from 60 and increass 1 minute
        if self.s < 59:#sililarly for every 60 minutes, 1 hour is added
            self.s += 1
        else:
            if self.m < 59:
                self.s = 0
                self.m += 1
            elif self.m == 59 and self.h < 24:
                self.h += 1
                self.m = 0
                self.s = 0
            else:
                self.timer.stop()

        self.timeString = "{0}:{1}:{2}".format(self.h,self.m,self.s)
        self.lcdNumber.setDigitCount(len(self.timeString))
        self.lcdNumber.display(self.timeString)#display timer on LCD gui 
    
    def Reset(self): #reset button for gui
     
        self.h = 0
        self.m = 0
        self.s = 0
        
        self.serialobj.clear()
        
        self.timer.stop() #stop timer
        self.lineEdit.setText("")#clear gui
        self.lineEdit_2.setText("")#clear gui
        self.timeEdit.setTime(QtCore.QTime.currentTime())#set timer to current time
        self.dateEdit.setDate(QtCore.QDate.currentDate())
        self.timeString = "{0}:{1}:{2}".format(self.h,self.m,self.s)

        self.lcdNumber.setDigitCount(len(self.timeString))
        self.lcdNumber.display(self.timeString)
        
        datim = (str(datetime.now())[:-10]).replace(':','_')
        self.filename = datim #Changes the file name to current date and time

    
    def timerStart(self): #Start timer when start button is pushed
        self.timer.start(1000)
           
    def stopGraph(self): #set flag when stop button is pushed 
        self.serialobj.stop()#to stop the graph and fetch operation
        time.sleep(2)#add delay
        self.serialobj.portObj.close()#close port to the arduino
        self.serialobj.clear()#clear flag
        self.resetButton.setEnabled(True)#enable reset button
           
    def setupUi(self, Form): #define the gui for the script
        Form.setObjectName("Form")
        Form.resize(409, 366)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(130, 20, 151, 21))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(120, 50, 161, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(70, 70, 291, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(20, 120, 47, 13))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.dateEdit = QtWidgets.QDateEdit(Form)
        self.dateEdit.setGeometry(QtCore.QRect(140, 120, 110, 22))
        self.dateEdit.setObjectName("dateEdit")
        self.comboBox = QtWidgets.QComboBox(Form)
        self.comboBox.setGeometry(QtCore.QRect(140, 160, 111, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("Analyte")
        self.comboBox.addItem("Conditioning Solution")
        self.comboBox.addItem("Reference")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(20, 160, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.timeEdit = QtWidgets.QTimeEdit(Form)
        self.timeEdit.setGeometry(QtCore.QRect(140, 200, 118, 22))
        self.timeEdit.setObjectName("timeEdit")
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setGeometry(QtCore.QRect(20, 200, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(140, 240, 121, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.label_7 = QtWidgets.QLabel(Form)
        self.label_7.setGeometry(QtCore.QRect(20, 240, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(Form)
        self.label_8.setGeometry(QtCore.QRect(20, 280, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.lineEdit_2 = QtWidgets.QLineEdit(Form)
        self.lineEdit_2.setGeometry(QtCore.QRect(140, 280, 121, 20))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(140, 310, 121, 41))
        self.pushButton.setObjectName("pushButton")
        self.lcdNumber = QtWidgets.QLCDNumber(Form)
        self.lcdNumber.setGeometry(QtCore.QRect(310, 250, 81, 41))
        self.lcdNumber.setObjectName("lcdNumber")
        self.stopButton = QtWidgets.QPushButton(Form)
        self.stopButton.setGeometry(QtCore.QRect(275, 310, 121, 41))
        self.stopButton.setObjectName("stopButton")
        self.resetButton = QtWidgets.QPushButton(Form)
        self.resetButton.setGeometry(QtCore.QRect(30, 310, 81, 41))
        self.resetButton.setObjectName("resetButton")
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.Time)
        self.timeEdit.setTime(QtCore.QTime.currentTime())
        self.dateEdit.setDate(QtCore.QDate.currentDate())
       
        self.pushButton.clicked.connect(lambda: Thread(target = self.serialobj.fetch).start())
        self.pushButton.clicked.connect(lambda: self.writeSensorMeta())
        self.pushButton.clicked.connect(lambda: self.timerStart())
        self.stopButton.clicked.connect(lambda: self.stopGraph())
        self.stopButton.clicked.connect(lambda: self.timer.stop())
        self.resetButton.clicked.connect(self.Reset)
        self.resetButton.setEnabled(False)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Taste Sensor"))
        self.label_2.setText(_translate("Form", "Designed and developed by"))
        self.label_3.setText(_translate("Form", "CSIR - Central Scientific Instruments Organization"))
        self.label_4.setText(_translate("Form", "Date"))
        self.label_5.setText(_translate("Form", "Select Solution"))
        self.label_6.setText(_translate("Form", "Time"))
        self.label_7.setText(_translate("Form", "Name"))
        self.label_8.setText(_translate("Form", "Concentration"))
        self.pushButton.setText(_translate("Form", "START"))
        self.stopButton.setText(_translate("Form", "STOP"))
        self.resetButton.setText(_translate("Form", "RESET"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    
    Form.show()
    Form.setFixedSize(400,370)
    sys.exit(app.exec_())

