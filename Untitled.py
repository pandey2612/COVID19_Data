from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import *
from PyQt5.uic import loadUiType
import os
import sys
import matplotlib.pylab as pylab
import pandas
import numpy
import seaborn
import matplotlib
import json
import COVID19Py
import subprocess
import urllib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from PIL import Image

ui, _ = loadUiType('radar.ui')


class MainApp(QMainWindow, ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setFixedSize(1528, 779)
        self.setupUi(self)
        self.center()
        self.worldDataLoad()
        self.visualData = 1
        self.timer1 = QTimer()
        self.timer2 = QTimer()
        self.HandleUI_Changes()
        if os.getcwd()+'/Total.json':
            print("yes")
            with open("Total.json", 'r') as file:
                output_Total_Temp = json.load(file)
            Total_DataFrame_Temp = pandas.DataFrame([list(
                output_Total_Temp.values())], columns=list(output_Total_Temp.keys()))
            A = str(list(Total_DataFrame_Temp['cases'])[0])
            A = f'{int(A): ,}'.strip()
            self.world_cases_Lb.setText(A)

            A = str(list(Total_DataFrame_Temp['deaths'])[0])
            A = f'{int(A): ,}'.strip()
            self.world_deaths_Lb.setText(A)

            A = str(list(Total_DataFrame_Temp['recovered'])[0])
            A = f'{int(A): ,}'.strip()
            self.world_recovered_Lb.setText(A)

            A = str(list(Total_DataFrame_Temp['todayDeaths'])[0])
            A = f'{int(A): ,}'.strip()
            self.world_today_deaths_Lb.setText(A)

            A = str(list(Total_DataFrame_Temp['todayCases'])[0])
            A = f'{int(A): ,}'.strip()
            self.world_today_cases_Lb.setText(A)
            print(list(Total_DataFrame_Temp['active'])[0])
            A = str(list(Total_DataFrame_Temp['critical'])[0])
            A = f'{int(A): ,}'.strip()
            self.world_critical_Lb.setText(A)

            A = str(list(Total_DataFrame_Temp['casesPerOneMillion'])[0])
            A = f'{int(A): ,}'.strip()
            self.world_cases_mill_Lb.setText(A)

            A = str(list(Total_DataFrame_Temp['deathsPerOneMillion'])[0])
            A = f'{int(A): ,}'.strip()
            self.world_deaths_mill_Lb.setText(A)

            A = str(list(Total_DataFrame_Temp['tests'])[0])
            A = f'{int(A): ,}'.strip()
            self.world_tests_Lb.setText(A)

            A = str(list(Total_DataFrame_Temp['testsPerOneMillion'])[0])
            A = f'{float(A): ,}'.strip()
            self.world_tests_mill_Lb.setText(A)

            A = str(list(Total_DataFrame_Temp['affectedCountries'])[0])
            A = f'{int(A): ,}'.strip()
            self.world_affected_Countries_Lb.setText(A)

            #pixmap = QtGui.QPixmap('world_pie.png')
            #pixmap_resized = pixmap.scaled(530, 320, QtCore.Qt.KeepAspectRatio)
            #pixmap_resized.save('world_pie.png')
            self.data_visual_Lb.setPixmap(QtGui.QPixmap('world_pie.png'))

    def HandleUI_Changes(self):
        self.CountryDataFrame = pandas.read_csv('Countries_DataFrame.csv')
        self.worldData()
        self.casesLinePlot()
        self.deathsLinePlot()
        #print(self.scrollArea.value())
        self.count=1
        self.worldDataVisualise()
        for i in range(len(self.CountryDataFrame['flag'])):
        	self.countryName  = str(self.CountryDataFrame['country'][i])
        	self.cases  = str(self.CountryDataFrame['cases'][i])
        	self.deaths  = str(self.CountryDataFrame['deaths'][i])
        	self.recovered  = str(self.CountryDataFrame['recovered'][i])
        	self.tests  = str(self.CountryDataFrame['tests'][i])
        	self.casesPM  = str(self.CountryDataFrame['casesPerOneMillion'][i])
        	self.deathsPM  = str(self.CountryDataFrame['deathsPerOneMillion'][i])
        	self.flag =str(self.CountryDataFrame['flag'][i])
        	self.createLayout()
        	self.count+=1
        """
        self.CountryDataFrame = pandas.read_csv('Countries_DataFrame.csv')
        print(self.CountryDataFrame['flag'][0])

        url = str(self.CountryDataFrame['flag'][0])
        data = urllib.request.urlopen(url).read()
        print(data)
        pixmap = QPixmap()
        pixmap.loadFromData(data)
        self.label_2.setPixmap(pixmap)
        self.label_2.setScaledContents(True)
        #self.label_2.setPixmap(QtGui.QPixmap(str(self.CountryDataFrame['flag'][0])))
                """
    def worldData(self):
        self.timer1.timeout.connect(self.worldDataLoad)
        self.timer1.start(60000)

    def worldDataLoad(self):
        print('data loading')
        Total = open("Total.json", 'w')
        subprocess.call("curl --location --request GET 'https://corona.lmao.ninja/all'", shell=True, stdout=Total)
        with open("Total.json", 'r') as file:
            output_Total = json.load(file)
        self.Total_DataFrame = pandas.DataFrame(
            [list(output_Total.values())], columns=list(output_Total.keys()))
        A = str(list(self.Total_DataFrame['cases'])[0])
        A = f'{int(A): ,}'.strip()
        self.world_cases_Lb.setText(A)

        A = str(list(self.Total_DataFrame['deaths'])[0])
        A = f'{int(A): ,}'.strip()
        self.world_deaths_Lb.setText(A)

        A = str(list(self.Total_DataFrame['recovered'])[0])
        A = f'{int(A): ,}'.strip()
        self.world_recovered_Lb.setText(A)

        A = str(list(self.Total_DataFrame['todayDeaths'])[0])
        A = f'{int(A): ,}'.strip()
        self.world_today_deaths_Lb.setText(A)

        A = str(list(self.Total_DataFrame['todayCases'])[0])
        A = f'{int(A): ,}'.strip()
        self.world_today_cases_Lb.setText(A)
        print(list(self.Total_DataFrame['active'])[0])

        A = str(list(self.Total_DataFrame['critical'])[0])
        A = f'{int(A): ,}'.strip()
        self.world_critical_Lb.setText(A)

        A = str(list(self.Total_DataFrame['casesPerOneMillion'])[0])
        A = f'{int(A): ,}'.strip()
        self.world_cases_mill_Lb.setText(A)

        A = str(list(self.Total_DataFrame['deathsPerOneMillion'])[0])
        A = f'{int(A): ,}'.strip()
        self.world_deaths_mill_Lb.setText(A)

        A = str(list(self.Total_DataFrame['tests'])[0])
        A = f'{int(A): ,}'.strip()
        self.world_tests_Lb.setText(A)

        A = str(list(self.Total_DataFrame['testsPerOneMillion'])[0])
        A = f'{float(A): ,}'.strip()
        self.world_tests_mill_Lb.setText(A)

        A = str(list(self.Total_DataFrame['affectedCountries'])[0])
        A = f'{int(A): ,}'.strip()
        self.world_affected_Countries_Lb.setText(A)
        self.overAllPiePLot()

        print('Done')
        #pixmap = QtGui.QPixmap('world_pie.png')
        #pixmap_resized = pixmap.scaled(530, 320, QtCore.Qt.KeepAspectRatio)
        #pixmap_resized.save('world_pie.png')
        #self.data_visual_Lb.setPixmap(QtGui.QPixmap('world_pie.png'))

    def worldDataVisualise(self):
        self.timer2.timeout.connect(self.worldDataVisualiseLoad)
        self.timer2.start(15000)

    def worldDataVisualiseLoad(self):
        if self.visualData == 1:
            self.visualData = 2
            self.data_visual_Lb.setPixmap(QtGui.QPixmap('world_pie.png'))
            self.data_visual_Lb.setScaledContents(False)
            self.data_visual_title_Lb.setText('Worldwide Data')
        elif self.visualData == 2:
            self.visualData = 3
            self.data_visual_Lb.setPixmap(QtGui.QPixmap('CasesLine.png'))
            self.data_visual_Lb.setScaledContents(True)
            self.data_visual_title_Lb.setText('Worldwide Cases TimeLine')
        elif self.visualData == 3:
            self.visualData = 1
            self.data_visual_Lb.setPixmap(QtGui.QPixmap('DeathsLine.png'))
            self.data_visual_Lb.setScaledContents(True)
            self.data_visual_title_Lb.setText('Worldwide Deaths TimeLine')

    def overAllPiePLot(self):
        D = []
        D.append(list(self.Total_DataFrame['cases'])[0])
        D.append(list(self.Total_DataFrame['deaths'])[0])
        D.append(list(self.Total_DataFrame['recovered'])[0])
        Labels = ['Cases'+' : '+str(f'{D[0]:,}'), 'Deaths'+' : '+str(
            f'{D[1]:,}'), 'Recovered'+' : '+str(f'{D[2]:,}')]
        colors = ['#66b3ff', '#ff6666', '#99ff99']
        explode = (0.09, 0, 0.08)
        fig1 = plt.figure(dpi=80)
        #fig1, ax1 = plt.subplots()
        fig1.set_facecolor('#222831')
        patches, texts, autotexts = plt.pie(D, explode=explode, pctdistance=0.8, labeldistance=1.08, colors=colors, autopct='%1.1f%%', shadow=True, labels=Labels, startangle=90)

        for text in texts:
            text.set_color('white')
            text.set_fontsize(13)
        for autotext in autotexts:
            autotext.set_color('black')
            autotext.set_fontsize(12)

        #ax1.axis('equal')
        fig1.savefig('world_pie.png', facecolor='#222831')
        print('overAllPiePLot')

    def casesLinePlot(self):
        self.Total_Cases_Timeline = pandas.read_csv('CountryTotal.csv')
        self.Total_Cases_List = list(self.Total_Cases_Timeline['Cases'])
        self.Total_Cases_Week = [self.Total_Cases_List[
                item] for item in range(0, len(self.Total_Cases_List), 7)]
        if len(self.Total_Cases_List)%7 != 0:
            self.Total_Cases_Week.append(self.Total_Cases_List[-1])
            self.WeekID = ['W'+str(item) for item in range(0,
                                                           len(self.Total_Cases_Week))]

        params = {
            'legend.fontsize': 15,
            'figure.figsize': (10, 5),
            'xtick.labelsize': 12,
            'ytick.labelsize': 12}
        pylab.rcParams.update(params)
        fig = plt.figure(dpi=62)
        fig.set_facecolor('#222831')
        ax = fig.add_subplot(111)
        ax.set_facecolor('#222831')
        ax.plot(self.WeekID, self.Total_Cases_Week, marker='o', markersize=13,
                markerfacecolor='#3282b8', color='skyblue', linewidth=3)
        #ax.spines['bottom'].set_color('#222831')
        ax.set_xlabel('No. of Weeks', labelpad=8, fontsize=15)
        ax.set_ylabel('No. of Cases', labelpad=10, fontsize=15)
        ax.xaxis.label.set_color('#f1f1b0')
        ax.yaxis.label.set_color('#f1f1b0')
        #ax.legend.color('white')

        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        plt.grid(visible=False)
        plt.legend(['Cases'])
        plt.savefig('CasesLine.png', facecolor='#222831')

    def deathsLinePlot(self):
        self.Total_Deaths_Timeline = pandas.read_csv('CountryTotal.csv')
        self.Total_Deaths_List = list(self.Total_Deaths_Timeline['Deaths'])
        self.Total_Deaths_Week = [self.Total_Deaths_List[
                item] for item in range(0, len(self.Total_Deaths_List), 7)]
        if len(self.Total_Deaths_List)%7 != 0:
            self.Total_Deaths_Week.append(self.Total_Deaths_List[-1])
            self.WeekID = ['W'+str(item) for item in range(0,
                                                           len(self.Total_Deaths_Week))]

        params = {
            'legend.fontsize': 15,
            'figure.figsize': (10, 5),
            'xtick.labelsize': 12,
            'ytick.labelsize': 12}
        pylab.rcParams.update(params)
        fig = plt.figure(dpi=62)
        fig.set_facecolor('#222831')
        ax = fig.add_subplot(111)
        ax.set_facecolor('#222831')
        ax.plot(self.WeekID, self.Total_Deaths_Week, marker='o', markersize=13,
                markerfacecolor='#e32249', color='#ff6464', linewidth=3)
        #ax.spines['bottom'].set_color('#222831')
        ax.set_xlabel('No. of Weeks', labelpad=8, fontsize=15)
        ax.set_ylabel('No. of Deaths', labelpad=10, fontsize=15)
        ax.xaxis.label.set_color('#f1f1b0')
        ax.yaxis.label.set_color('#f1f1b0')
        #ax.legend.color('white')

        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        plt.grid(visible=False)
        plt.legend(['Deaths'])
        plt.savefig('DeathsLine.png', facecolor='#222831')

    def createLayout(self):
        
        self.frame_8 = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_8.sizePolicy().hasHeightForWidth())
        self.frame_8.setSizePolicy(sizePolicy)
        self.frame_8.setMinimumSize(QtCore.QSize(280, 140))
        self.frame_8.setMaximumSize(QtCore.QSize(280, 140))
        self.frame_8.setStyleSheet("background-color:#222831;")
        self.frame_8.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_8.setObjectName("frame_8")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.frame_8)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setSpacing(10)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.verticalLayout_17 = QtWidgets.QVBoxLayout()
        self.verticalLayout_17.setSpacing(5)
        self.verticalLayout_17.setObjectName("verticalLayout_17")
        self.label_10 = QtWidgets.QLabel(self.frame_8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("arial")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setStyleSheet("font-family:arial;\n"
"color: #acdbdf;")
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.verticalLayout_17.addWidget(self.label_10)
        self.label_2 = QtWidgets.QLabel(self.frame_8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QtCore.QSize(150, 70))
        self.label_2.setMaximumSize(QtCore.QSize(150, 70))
        self.label_2.setText("")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_17.addWidget(self.label_2)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setContentsMargins(15, -1, -1, -1)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_16 = QtWidgets.QLabel(self.frame_8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_16.sizePolicy().hasHeightForWidth())
        self.label_16.setSizePolicy(sizePolicy)
        self.label_16.setMinimumSize(QtCore.QSize(0, 22))
        self.label_16.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("arial")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_16.setFont(font)
        self.label_16.setStyleSheet("font-family:arial;\n"
"color: #acdbdf;")
        self.label_16.setObjectName("label_16")
        self.label_16.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.horizontalLayout_10.addWidget(self.label_16)
        self.verticalLayout_17.addLayout(self.horizontalLayout_10)
        self.horizontalLayout_9.addLayout(self.verticalLayout_17)
        self.verticalLayout_14 = QtWidgets.QVBoxLayout()
        self.verticalLayout_14.setContentsMargins(15, -1, -1, -1)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.label_6 = QtWidgets.QLabel(self.frame_8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("arial")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("font-family:arial;\n"
"color: #d9d872;")
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_12.addWidget(self.label_6)
        self.verticalLayout_14.addLayout(self.horizontalLayout_12)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.label_8 = QtWidgets.QLabel(self.frame_8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("arial")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setStyleSheet("font-family:arial;\n"
"color: #ee4540;")
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_11.addWidget(self.label_8)
        self.verticalLayout_14.addLayout(self.horizontalLayout_11)
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.label_17 = QtWidgets.QLabel(self.frame_8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_17.sizePolicy().hasHeightForWidth())
        self.label_17.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("arial")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_17.setFont(font)
        self.label_17.setStyleSheet("font-family:arial;\n"
"color: #58b368;")
        self.label_17.setObjectName("label_17")
        self.horizontalLayout_13.addWidget(self.label_17)
        self.verticalLayout_14.addLayout(self.horizontalLayout_13)
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.label_18 = QtWidgets.QLabel(self.frame_8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_18.sizePolicy().hasHeightForWidth())
        self.label_18.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("arial")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_18.setFont(font)
        self.label_18.setStyleSheet("font-family:arial;\n"
"color: #acdbdf;")
        self.label_18.setObjectName("label_18")
        self.horizontalLayout_14.addWidget(self.label_18)
        self.verticalLayout_14.addLayout(self.horizontalLayout_14)
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.label_4 = QtWidgets.QLabel(self.frame_8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("arial")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("font-family:arial;\n"
"color: #acdbdf;")
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_15.addWidget(self.label_4)
        self.verticalLayout_14.addLayout(self.horizontalLayout_15)
        self.horizontalLayout_9.addLayout(self.verticalLayout_14)
        self.gridLayout_4.addLayout(self.horizontalLayout_9, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.frame_8, 0, 0, 1, 1)
        #mainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi1()
        print(self.frame_8.size())
        print(self.count)
        if self.count>5 and self.count<=10:
        	self.verticalLayout.addWidget(self.frame_8)
        elif self.count<=5:
        	self.verticalLayout_2.addWidget(self.frame_8)
        else:
        	self.scroll_Vir_Layout.addWidget(self.frame_8)
    def retranslateUi1(self):
        self.label_10.setText( str(self.countryName))
        self.label_16.setText( str(self.casesPM)+" CPM")
        self.label_6.setText( str(self.cases)+" C")
        self.label_8.setText( str(self.deaths)+" D")
        self.label_17.setText(str(self.recovered)+" R")
        self.label_18.setText( str(self.tests) + " T")
        self.label_4.setText( str(self.deathsPM) + " DPM")
        print(self.flag[56:])
        #url = self.flag
        #data = urllib.request.urlopen(url).read()
        #print(data)
        pixmap = QPixmap(self.flag[56:])
        
        self.label_2.setPixmap(pixmap)
        self.label_2.setScaledContents(True)


        

    def center(self):
        # geometry of the main windowy
        qr = self.frameGeometry()

        # center point of screen
        cp = QDesktopWidget().availableGeometry().center()

        # move rectangle's center point to screen's center point
        qr.moveCenter(cp)

        # top left of rectangle becomes top left of window centering it
        self.move(qr.topLeft())

app = QApplication(sys.argv)
window = MainApp()
window.show()
app.exec_()
