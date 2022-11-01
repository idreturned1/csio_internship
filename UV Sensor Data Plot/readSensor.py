import csv
import matplotlib.pyplot as plt
from scipy.integrate import simps

class fileplot(object):
    
    def __init__(self):
        self.fig1, self.ax1 = plt.subplots()
        self.fig2, self.ax2 = plt.subplots()
        self.fig3, self.ax3 = plt.subplots()

    #plot the raw, normalized and ratio data
    def plot(self, file_name):
        label_name = self.generateLabel(file_name)
        self.readFile(file_name)
        self.plotRaw(label_name)
        self.plotNormalized(label_name)
        self.plotRatio(label_name)
        
    #generate the graph labels from the filenames    
    def generateLabel(self,file_name):
        temp = file_name.split('.')
        return temp[0]
        
    #read input files
    def readFile(self, file_name):
        self.flag = 0
        self.data_y = []
        self.data_x = []
        self.normalized_data_y = []
        self.ratio_data_y = []
        with open(file_name,"r") as file_obj:
            reader = csv.reader(file_obj)
            for row in reader:
                if(row == ['#DATA']): #start reading data from below #data in file 
                    self.flag = 1
                    continue
                    
                if(self.flag == 1):
                    temp = row[0].split('\t')
                    self.data_x.append(float(temp[0]))
                    self.data_y.append(float(temp[1]))
        
        self.ymin = min(self.data_y)
        self.ymax = max(self.data_y)
                    
    #Create normalized data for the raw data    
    def generateNormalized(self):
        
        for i in self.data_y:
            temp_y = (i - self.ymin)/(self.ymax-self.ymin)
            self.normalized_data_y.append(temp_y)
    
    #create Ratio of data
    def generateRatio(self):
        
        for i in self.data_y:
            temp_y = i/self.ymax
            self.ratio_data_y.append(temp_y)
        
    #plotting fuctions
    def plotRaw(self,file_name):
        self.ax1.set_title('Raw Sensor Data')
        self.ax1.grid(True)
        self.ax1.set_ylabel('Y Data')
        self.ax1.set_xlabel('X Data')
        
        self.ax1.plot(self.data_x,self.data_y, label=file_name)
        self.ax1.legend(loc='upper right')
        self.area(self.data_y,"Area for Raw plot " + file_name + " = ")
        #self.fig1.show()
        
    def plotNormalized(self,file_name):
        self.generateNormalized()

        self.ax2.set_title('Normalized Sensor Data')
        self.ax2.grid(True)
        self.ax2.set_ylabel('Y Data')
        self.ax2.set_xlabel('X Data')
        
        self.ax2.plot(self.data_x,self.normalized_data_y, label=file_name)
        self.ax2.legend(loc='upper right')
        self.area(self.normalized_data_y,"Area for Normalized plot " + file_name + " = ")
        #self.fig2.show()
        
    def plotRatio(self,file_name):
        self.generateRatio()

        self.ax3.set_title('Ratio Sensor Data')
        self.ax3.grid(True)
        self.ax3.set_ylabel('Y Data')
        self.ax3.set_xlabel('X Data')
        
        self.ax3.plot(self.data_x,self.ratio_data_y, label=file_name)
        self.ax3.legend(loc='upper right')
        self.area(self.ratio_data_y,"Area for Ratio plot " + file_name + " = ")
        #self.fig3.show()
        
    #get areas of plots    
    def area(self,values,data_string):
        area = simps(values,dx=1)
        print(data_string, area)
        
    #show plots on terminal
    def showPlot(self):
        plt.show()
        
            
                    
testobj = fileplot()
testobj.plot("10 ppm Ni oep heptanal.asc")
testobj.plot("10 ppm Ni oep hexanal.asc")
testobj.plot("10 ppm Ni oep propenal.asc")
testobj.plot("Ni oep.asc")
testobj.showPlot()            
        

