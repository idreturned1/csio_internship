import threading
import serial
from PyQt5 import QtCore 
import time

class SerialData(QtCore.QObject):
    
    #Signal when data coming from arduino changes and call graph function[check event_th.py]
    dataChanged = QtCore.pyqtSignal(list,list,list,list,list,list,list)
    
    #contructor, Specify port, baudrate and timeOut values
    def __init__(self, port = 'COM3', baudRate  = 9600, timeOut  = 5, parent=None):
        super(self.__class__, self).__init__(parent)
        
        self.port = port
        self.baudRate = baudRate
        self.timeOut = timeOut
        self.counter = 0   
        self.flag = 1
        self.sensor0 = []
        self.sensor1 = []
        self.sensor2 = []
        self.sensor3 = []
        self.sensor4 = []
        self.sensor5 = []
        self.sensor6 = []
        self._stop_event = threading.Event()
        
    #set stop flag to stop thread operation    
    def stop(self):
        self._stop_event.set()
        
    #clear flag to start fetch operation again
    def clear(self):
        self._stop_event.clear()
                 
    def fetch(self): #fetch data from arduino

        try: #open arduino port
            self.portObj = serial.Serial(port=self.port, baudrate=self.baudRate, timeout=self.timeOut)
        except Exception as e:
            print(e)            
            self.portObj.close()
        
        while(self.flag): #check flag
            if(self._stop_event.is_set()):
                return
            self.dataString = str(self.portObj.readline()) #get data from arduino in form of unformatted string
            for ch in ['b\'','r', 'n', '\\\\', '\'']: #clean the string to extract values of sensors
                if ch in self.dataString:
                    self.dataString = self.dataString.replace(ch,'')
                
            self.inputList = self.dataString.split(',') #split the string to get value of each sensor in a list
            print(self.inputList) #print sensor data
        
            if (len(self.inputList) == 7): #create lists of 7 sensors and append the data to the list 
                self.sensor0.append(int(self.inputList[0]))
                self.sensor1.append(int(self.inputList[1]))
                self.sensor2.append(int(self.inputList[2]))
                self.sensor3.append(int(self.inputList[3]))
                self.sensor4.append(int(self.inputList[4]))
                self.sensor5.append(int(self.inputList[5]))
                self.sensor6.append(int(self.inputList[6]))
                
                if (self.counter < 51): #The graph will display a maximum of 50 entries at one time
                    self.dataChanged.emit(self.sensor0,self.sensor1,self.sensor2
                                              ,self.sensor3,self.sensor4,
                                              self.sensor5,self.sensor6)
                    self.counter += 1
                else: #After 50 entries are collected, only the latest 50 entries will be sent to graph function
                    self.dataChanged.emit(self.sensor0[-50:],self.sensor1[-50:],self.sensor2[-50:]#to be plotted
                                              ,self.sensor3[-50:],self.sensor4[-50:],
                                              self.sensor5[-50:],self.sensor6[-50:])
                time.sleep(1)#delay, so that the graph function has sufficient time to plot the data
            else:
                pass
        
    
  