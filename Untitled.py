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
import COVID19Py
from PIL import Image
import COVID19Py

ui, _ = loadUiType('main.ui')


class MainApp(QMainWindow, ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setFixedSize(1460, 779)
        self.setupUi(self)
        self.center()

        self.visualData = 1
        self.count = 1
        self.newsCount = 0
        self.timer1 = QTimer()
        self.timer2 = QTimer()
        self.timer3 = QTimer()
        self.timer4 = QTimer()
        self.Frames = {}
        self.countriesData()
        self.worldDataLoad()
        self.newsHeadlines()
        self.news()
        self.CountryDataFrame = pandas.read_csv('Countries_DataFrame.csv')
        self.deathPercentageLolly()
        self.countryCasesComparisonLinePlot()
        self.countryDeathsComparisonLinePlot()
        self.monthCasesDeathsCount()
        
        self.HandleUI_Changes()
        self.overAll()

    def HandleUI_Changes(self):

        self.worldData()
        self.casesLinePlot()
        self.deathsLinePlot()
        self.lineEdit.textChanged.connect(self.update_display)
        #print(self.scrollArea.value())

        self.worldDataVisualise()
        for i in range(len(self.CountryDataFrame['flag'])):
            self.countryName = str(self.CountryDataFrame['country'][i])
            self.cases = str(self.CountryDataFrame['cases'][i])
            self.deaths = str(self.CountryDataFrame['deaths'][i])
            self.recovered = str(self.CountryDataFrame['recovered'][i])
            self.tests = str(self.CountryDataFrame['tests'][i])
            self.casesPM = str(self.CountryDataFrame['casesPerOneMillion'][i])
            self.deathsPM = str(
                self.CountryDataFrame['deathsPerOneMillion'][i])
            self.flag = str(self.CountryDataFrame['flag'][i])
            self.createLayout(str(self.CountryDataFrame['country'][i]))
            self.count += 1
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
        print(self.Frames)
        #self.Frames[0].hide()
    def worldData(self):
        self.timer1.timeout.connect(self.worldDataLoad)
        self.timer1.start(60000)
    def overAll(self):
        self.timer4.timeout.connect(self.overAllTimeline)
        self.timer4.start(600000)

    def worldDataLoad(self):
        try:
            
            print('data loading')
            Total = open("temp.json", 'w')
            A = subprocess.call("curl --location --request GET 'https://corona.lmao.ninja/v2/all'", shell=True, stdout=Total)
            if A==0:
                with open("temp.json", "r") as froms, open("Total.json", "w") as to:
                    to.write(froms.read())
                print("yes")

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
        except Exception as e:
            print(e)
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
            self.visualData = 4
            self.data_visual_Lb.setPixmap(QtGui.QPixmap('DeathsLine.png'))
            self.data_visual_Lb.setScaledContents(True)
            self.data_visual_title_Lb.setText('Worldwide Deaths TimeLine')
        elif self.visualData == 4:
            self.visualData = 5
            self.data_visual_Lb.setPixmap(QtGui.QPixmap('DeathPercentage.png'))
            self.data_visual_Lb.setScaledContents(True)
            self.data_visual_title_Lb.setText('Death Rate of countries(Top 10) more than 1K Cases')
        elif self.visualData == 5:
            self.visualData = 6
            self.data_visual_Lb.setPixmap(QtGui.QPixmap('CountryCasesComparison.png'))
            self.data_visual_Lb.setScaledContents(True)
            self.data_visual_title_Lb.setText('Cases TimeLine Comparison (Countries)')
        elif self.visualData == 6:
            self.visualData = 7
            self.data_visual_Lb.setPixmap(QtGui.QPixmap('CountryDeathsComparison.png'))
            self.data_visual_Lb.setScaledContents(True)
            self.data_visual_title_Lb.setText('Deaths TimeLine Comparison (Countries)')
        elif self.visualData == 7:
            self.visualData = 8
            self.data_visual_Lb.setPixmap(QtGui.QPixmap('MonthCasesCount.png'))
            self.data_visual_Lb.setScaledContents(True)
            self.data_visual_title_Lb.setText('Cases Count of 1 Month')
        elif self.visualData == 8:
            self.visualData = 1
            self.data_visual_Lb.setPixmap(QtGui.QPixmap('MonthDeathsCount.png'))
            self.data_visual_Lb.setScaledContents(True)
            self.data_visual_title_Lb.setText('Deaths Count of 1 Month')

    def news(self):
        self.timer3.timeout.connect(self.newsStart)
        self.timer3.start(8000)

    def newsStart(self):
        try:
            self.textEdit.setText(self.News_List[self.newsCount])
            self.newsCount += 1
            if len(self.News_List) == self.newsCount:
                self.newsCount = 0
        except Exception as e:
            print(e)

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

    def newsHeadlines(self):
        try:
            
           
            Total_News = open("temp.json", 'w')
            A = subprocess.call("curl --location --request GET 'https://newsapi.org/v2/everything?q=COVID&from=2020-03-17&sortBy=publishedAt&apiKey=fa20528865324b62b303c6d7918e4674&pageSize=100&page=1'"  , shell=True , stdout = Total_News)
            if A==0:
                with open("temp.json", "r") as froms, open("Total_News.json", "w") as to:
                    to.write(froms.read())
                print("yes")
            with open("Total_News.json", 'r') as file:
                output_Total_News = json.load(file)
            self.News_List = []
            for i in range(len(output_Total_News['articles'])):
                self.News_List.append(output_Total_News['articles'][i]['title'])
            print(self.News_List)
        except Exception as e:
            print(e)
            with open("Total_News.json", 'r') as file:
                output_Total_News = json.load(file)
            self.News_List = []
            for i in range(len(output_Total_News['articles'])):
                self.News_List.append(output_Total_News['articles'][i]['title'])
            print(self.News_List)

    def monthCasesDeathsCount(self):
        TotalTimeLine = pandas.read_csv('CountryTotal.csv')
        CaseTimeline = []
        for index in range(len(TotalTimeLine)-31 , len(TotalTimeLine)):
            CaseTimeline.append([TotalTimeLine.iloc[index][0] , TotalTimeLine.iloc[index][1],TotalTimeLine.iloc[index][2]]) 
        monthCases = []
        monthDeaths = []
        for i in range(len(CaseTimeline)-1):
            monthCases.append(int(CaseTimeline[i+1][1] - CaseTimeline[i][1]))
        for i in range(len(CaseTimeline)-1):
            monthDeaths.append(int(CaseTimeline[i+1][2] - CaseTimeline[i][2]))
            date =[]
        for i in range(1,len(CaseTimeline)):
            date.append(CaseTimeline[i][0][6:10])  
        params = {
         'legend.fontsize': 15,
    
         'xtick.labelsize':12,
         'ytick.labelsize':12}

        pylab.rcParams.update(params)
        fig, ax = plt.subplots(figsize=(11,6), dpi= 70)
        fig.set_facecolor('#222831')

        ax.set_facecolor('#222831')
        ax.bar([i for i in range(1,31)] , monthCases , color='#f1fa3c'  )
        ax.set_xticks([i for i in range(1,31)])
        ax.set_xticklabels(date, rotation=82)
        ax.set_xlabel('Days' , labelpad=10 , fontsize = 17)
        ax.set_ylabel('No. of Cases',labelpad=10 , fontsize = 17)
        ax.xaxis.label.set_color('#f1f1b0')
        ax.yaxis.label.set_color('#f1f1b0')
        #ax.legend('Cases')

        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        fig.tight_layout()
        plt.savefig('MonthCasesCount.png' , facecolor ='#222831')

        params = {
         'legend.fontsize': 15,
    
         'xtick.labelsize':12,
         'ytick.labelsize':12}

        pylab.rcParams.update(params)
        fig, ax = plt.subplots(figsize=(11,6), dpi= 70)
        fig.set_facecolor('#222831')

        ax.set_facecolor('#222831')
        ax.bar([i for i in range(1,31)] , monthDeaths , color='#ef4b4b'  )
        ax.set_xticks([i for i in range(1,31)])
        ax.set_xticklabels(date, rotation=82)
        ax.set_xlabel('Days' , labelpad=10 , fontsize = 17)
        ax.set_ylabel('No. of Deaths',labelpad=10 , fontsize = 17)
        ax.xaxis.label.set_color('#f1f1b0')
        ax.yaxis.label.set_color('#f1f1b0')
        #ax.legend('Cases')

        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')

        fig.tight_layout()
        plt.savefig('MonthDeathsCount.png' , facecolor ='#222831')
    def overAllTimeline(self):
        try:
            covid = COVID19Py.COVID19()
            data = covid.getAll(timelines=True)
            Confirmed_Cases = list(data['locations'][1]['timelines']['confirmed']['timeline'].values())
            Deaths = list(data['locations'][1]['timelines']['deaths']['timeline'].values())
            TimeLines = list(data['locations'][1]['timelines']['deaths']['timeline'].keys())
            Df = {'TimeLine':TimeLines ,'Cases':Confirmed_Cases , 'Deaths':Deaths}
            Countrywise_test_dataframe = pandas.DataFrame(Df)
            Confirmed_Cases1 = []
            Deaths1 = []
            current_Country = {}
            TotalCountry = False

            subprocess.call("mkdir 'Countries_TimeLine_Data'" , shell=True )
            for item in data['locations']:
                Country_name = item['country_code']
                if item['province']=='':
                    #print(Country_name)
                    Confirmed_Cases = list(item['timelines']['confirmed']['timeline'].values())
                    Deaths = list(item['timelines']['deaths']['timeline'].values())
                    TimeLines = list(item['timelines']['deaths']['timeline'].keys())
                    
                    Df = {'TimeLine':TimeLines ,'Cases':Confirmed_Cases , 'Deaths':Deaths}
                    Countrywise_test_dataframe = pandas.DataFrame(Df)
                    if TotalCountry ==False:
                        TotalCountryDataFrame = pandas.DataFrame(Df)
                        TotalCountry =True
                        Confirmed_Cases2 = Confirmed_Cases
                        Deaths2 = Deaths
                        Countrywise_test_dataframe.to_csv('CountryTotal.csv',index=False)
                        
                    else:
                        Confirmed_Cases2 = [Confirmed_Cases[j]+Confirmed_Cases2[j] for j in range(len(Confirmed_Cases))]
                        Deaths2 = [Deaths[j]+Deaths2[j] for j in range(len(Deaths))]
                        Df = {'TimeLine':TimeLines ,'Cases':Confirmed_Cases2 , 'Deaths':Deaths2}
                        Countrywise_test_dataframe1 = pandas.DataFrame(Df)
                        Countrywise_test_dataframe1.to_csv('CountryTotal.csv',index=False)
                        
                    
                    Countrywise_test_dataframe.to_csv('Countries_TimeLine_Data/'+str(Country_name)+'.csv',index=False)
                    
                else:
                    #print(Country_name , item['province'])
                    #if current_Country != Country_name:
                        #current_Country = Country_name
                        
                        
                    if Country_name in list(current_Country.keys()):
                        
                        Confirmed_Cases = list(item['timelines']['confirmed']['timeline'].values())
                        Deaths = list(item['timelines']['deaths']['timeline'].values())
                        TimeLines = list(item['timelines']['deaths']['timeline'].keys())
                        if TotalCountry ==False:
                            TotalCountryDataFrame = pandas.DataFrame(Df)
                            TotalCountry =True
                            Confirmed_Cases2 = Confirmed_Cases
                            Deaths2 = Deaths
                            Countrywise_test_dataframe.to_csv('CountryTotal.csv',index=False)
                            Df = {'TimeLine':TimeLines ,'Cases':Confirmed_Cases , 'Deaths':Deaths}
                            Countrywise_test_dataframe = pandas.DataFrame(Df)

                        else:
                            Confirmed_Cases2 = [Confirmed_Cases[j]+Confirmed_Cases2[j] for j in range(len(Confirmed_Cases))]
                            Deaths2 = [Deaths[j]+Deaths2[j] for j in range(len(Deaths))]
                            Df = {'TimeLine':TimeLines ,'Cases':Confirmed_Cases2 , 'Deaths':Deaths2}
                            Countrywise_test_dataframe1 = pandas.DataFrame(Df)
                            Countrywise_test_dataframe1.to_csv('CountryTotal.csv',index=False)
                        
                        
                        Confirmed_Cases1 = current_Country[Country_name][0]
                        Deaths1 = current_Country[Country_name][1]
                        Confirmed_Cases = [Confirmed_Cases[j]+Confirmed_Cases1[j] for j in range(len(Confirmed_Cases))]
                        Deaths = [Deaths[j]+Deaths1[j] for j in range(len(Deaths))]
                        
                        Confirmed_Cases1 = Confirmed_Cases
                        Deaths1 = Deaths
                        
                        current_Country[Country_name] = [Confirmed_Cases1 , Deaths1]
                        
                        
                        Df = {'TimeLine':TimeLines ,'Cases':Confirmed_Cases , 'Deaths':Deaths}
                        Countrywise_test_dataframe = pandas.DataFrame(Df)
                        
                        Countrywise_test_dataframe.to_csv('Countries_TimeLine_Data/'+str(Country_name)+'.csv',index=False)
                    else:
                        Confirmed_Cases = list(item['timelines']['confirmed']['timeline'].values())
                        Deaths = list(item['timelines']['deaths']['timeline'].values())
                        TimeLines = list(item['timelines']['deaths']['timeline'].keys())
                        if TotalCountry ==False:
                            TotalCountryDataFrame = pandas.DataFrame(Df)
                            TotalCountry =True
                            Confirmed_Cases2 = Confirmed_Cases
                            Deaths2 = Deaths
                            Countrywise_test_dataframe.to_csv('CountryTotal.csv',index=False)
                            Df = {'TimeLine':TimeLines ,'Cases':Confirmed_Cases , 'Deaths':Deaths}
                            Countrywise_test_dataframe = pandas.DataFrame(Df)

                        else:
                            Confirmed_Cases2 = [Confirmed_Cases[j]+Confirmed_Cases2[j] for j in range(len(Confirmed_Cases))]
                            Deaths2 = [Deaths[j]+Deaths2[j] for j in range(len(Deaths))]
                            Df = {'TimeLine':TimeLines ,'Cases':Confirmed_Cases2 , 'Deaths':Deaths2}
                            Countrywise_test_dataframe1 = pandas.DataFrame(Df)
                            Countrywise_test_dataframe1.to_csv('CountryTotal.csv',index=False)
                            
                        Confirmed_Cases1 = Confirmed_Cases
                        Deaths1 = Deaths
                        current_Country[Country_name] = [Confirmed_Cases1 , Deaths1]
                        
                        Df = {'TimeLine':TimeLines ,'Cases':Confirmed_Cases , 'Deaths':Deaths}
                        Countrywise_test_dataframe = pandas.DataFrame(Df)
                        Countrywise_test_dataframe.to_csv('Countries_TimeLine_Data/'+str(Country_name)+'.csv',index=False)
            print(list(current_Country.keys()))
        except Exception as e:
            print(e)
    def countriesData(self):
        try:
            
            Countries = open("temp.json", 'w')
            A = subprocess.call("curl --location --request GET 'https://corona.lmao.ninja/countries?sort=country'", shell=True, stdout=Countries)
            if A==0:
                with open("temp.json", "r") as froms, open("Countries.json", "w") as to:
                    to.write(froms.read())
                print("yes")
            with open("Countries.json", 'r') as file:
                output_Countries = json.load(file)
            Countries_DataFrame1 = pandas.DataFrame([list(output_Countries[i].values()) for i in range(len(output_Countries))], columns=list(output_Countries[0].keys()))
            Countries_DataFrame1 = Countries_DataFrame1.drop(
                'countryInfo', axis=1)
            Countries_DataFrame2 = pandas.DataFrame([list(output_Countries[i]['countryInfo'].values()) for i in range(len(output_Countries))], columns=list(output_Countries[0]['countryInfo'].keys()))
            A = list(Countries_DataFrame2['flag'])
            B = list(Countries_DataFrame2['long'])
            C = list(Countries_DataFrame2['lat'])
            D = list(Countries_DataFrame2['iso3'])
            E = list(Countries_DataFrame2['iso2'])
            F = list(Countries_DataFrame2['_id'])

            Countries_DataFrame1['flag'] = A
            Countries_DataFrame1['long'] = B
            Countries_DataFrame1['lat'] = C
            Countries_DataFrame1['iso3'] = D
            Countries_DataFrame1['iso2'] = E
            Countries_DataFrame1['_id'] = F

            Countries_DataFrame = Countries_DataFrame1.sort_values(
                'cases', ascending=False)
            Countries_DataFrame.to_csv('Countries_DataFrame.csv', index=False)
        except Exception as e:
            print(e)

    def casesLinePlot(self):
        self.Total_Cases_Timeline = pandas.read_csv('CountryTotal.csv')
        self.Total_Cases_List = list(self.Total_Cases_Timeline['Cases'])
        self.Total_Cases_Week = [self.Total_Cases_List[
                item] for item in range(0, len(self.Total_Cases_List), 7)]
        if len(self.Total_Cases_List)%7 != 0:
            self.Total_Cases_Week.append(self.Total_Cases_List[-1])
        elif len(self.Total_Cases_List)%7==0:
            self.Total_Cases_Week[-1] = self.Total_Cases_List[-1]
        self.WeekID = ['W'+str(item) for item in range(0,len(self.Total_Cases_Week))]

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

    def deathPercentageLolly(self):
        hist_cases = []
        hist_deaths = []
        Countries_DataFrame = self.CountryDataFrame
        for item in range(len(Countries_DataFrame['country'])):
            hist_cases.append(Countries_DataFrame.iloc[item][2])
            hist_deaths.append(Countries_DataFrame.iloc[item][4])

        A = [(100*hist_deaths[i])/hist_cases[i] for i in range(len(hist_cases))]
        Countries_DataFrame['Deaths(%)'] = A
        Countries_DataFrame = Countries_DataFrame.sort_index()
        del_List = []

        for i in range(len(Countries_DataFrame['cases'])):
            b = Countries_DataFrame.iloc[i][2]
            if b < 1000:
                del_List.append(i)
                print(Countries_DataFrame.iloc[i][2])
        Countries_DataFrame.drop(
            index=del_List, axis=1, inplace=True)
        Countries_DataFrame.sort_values(
            'Deaths(%)', ascending=False, inplace=True)
        lolly_country = []
        lolly_deathsPercentage = []
        for item in range(10):
            lolly_country.append(Countries_DataFrame.iloc[item][1])
            lolly_deathsPercentage.append(
                round(Countries_DataFrame.iloc[item][19], 2))

        params = {
            'legend.fontsize': 15,

            'xtick.labelsize': 12,
            'ytick.labelsize': 12}
        pylab.rcParams.update(params)
        fig, ax = plt.subplots(figsize=(11, 6), dpi=70)
        fig.set_facecolor('#222831')

        ax.set_facecolor('#222831')
        ax.vlines(x=lolly_country, ymin=0, ymax=lolly_deathsPercentage, linestyles='solid', color=['#b80d57'], alpha=1, linewidth=3)
        ax.scatter(x=lolly_country, y=lolly_deathsPercentage,
                   s=140, color='#b80d57', alpha=1)
        ax.set_xlabel('Countries', labelpad=10, fontsize=17)
        ax.set_ylabel('Death Percentage', labelpad=10, fontsize=17)
        ax.set_xticks(lolly_country)
        ax.set_ylim(0, 20)
        ax.xaxis.label.set_color('#f1f1b0')
        ax.yaxis.label.set_color('#f1f1b0')
        #ax.legend.color('white')

        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        for row in range(len(lolly_deathsPercentage)):
            ax.text(lolly_country[row], lolly_deathsPercentage[row]+1.2, s=str(round(lolly_deathsPercentage[row], 2))+'%', horizontalalignment='center', verticalalignment='bottom', color='#f8e1f4', fontsize=14)
        plt.savefig('DeathPercentage.png', facecolor='#222831')
    
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

    def countryCasesComparisonLinePlot(self):
        Contry_Info_dataframe = pandas.read_csv('Countries_DataFrame.csv')
        CountryCode = list(Contry_Info_dataframe['iso2'])
        CountryName= list(Contry_Info_dataframe['country']) 
        timeline={}
        for i in range(10):
            if "Countries_TimeLine_Data/"+str(CountryCode[i])+str('.csv'):
                timeline[CountryName[i]] = pandas.read_csv('Countries_TimeLine_Data/'+str(CountryCode[i])+str('.csv'))
        del timeline['France']
        del timeline['UK']
        del timeline['Iran']
        del timeline['Turkey']
        del timeline['Belgium']
        params = {
         'legend.fontsize': 15,
        'figure.figsize': (10, 5),
         'xtick.labelsize':12,
         'ytick.labelsize':12}
        pylab.rcParams.update(params)
        fig = plt.figure(dpi=62)
        fig.set_facecolor('#222831')
        ax = fig.add_subplot(111)
        ax.set_facecolor('#222831')
        M_color = ['#e32249','#cf7500','#00bcd4','#2b580c','#ffc8bd']
        L_color =['#ff6464','#f0a500','#b2ebf2','#639a67','#ffebd9']
        index=0
        print(list(timeline.keys()))
        for item in list(timeline.keys()):
            A = list(timeline[item]['Cases'])

            B = [A[item] for item in range(0,len(A) ,7)]
            
            if len(A)%7 != 0:
                B.append(A[-1])
            elif len(A)%7==0:
                B[-1] = A[-1]
            print(B)
            W = ['W'+str(item) for item in range(0 , len(B))]
            
            ax.plot(W , B , marker='o' ,markersize=13,markerfacecolor=M_color[index], color=L_color[index] , linewidth = 3)
            index+=1
        #ax.plot(W , D , marker='o' ,markersize=13,markerfacecolor='#e32249', color='#ff6464' , linewidth = 3)
        #ax.spines['bottom'].set_color('#222831')
        #ax.set_ylim(0, 450000)
        ax.set_xlabel('No. of Weeks' , labelpad=7 , fontsize = 17)
        ax.set_ylabel('No. of Cases',labelpad=7, fontsize = 17)
        ax.xaxis.label.set_color('#f1f1b0')
        ax.yaxis.label.set_color('#f1f1b0')
        #ax.legend.color('white')

        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        plt.grid(visible = False)
        plt.legend(list(timeline.keys()))
        plt.savefig('CountryCasesComparison.png' , facecolor ='#222831')

    def update_display(self, text):

        for widget in self.Frames.keys():
            if text.lower() in widget.lower():
                self.Frames[widget].show()
            else:
                self.Frames[widget].hide()
    def countryDeathsComparisonLinePlot(self):
        Contry_Info_dataframe = pandas.read_csv('Countries_DataFrame.csv')
        CountryCode = list(Contry_Info_dataframe['iso2'])
        CountryName= list(Contry_Info_dataframe['country']) 
        timeline={}
        for i in range(10):
            if "Countries_TimeLine_Data/"+str(CountryCode[i])+str('.csv'):
                timeline[CountryName[i]] = pandas.read_csv('Countries_TimeLine_Data/'+str(CountryCode[i])+str('.csv'))
        del timeline['France']
        del timeline['UK']
        del timeline['Iran']
        del timeline['Turkey']
        del timeline['Belgium']
        params = {
         'legend.fontsize': 15,
        'figure.figsize': (10, 5),
         'xtick.labelsize':12,
         'ytick.labelsize':12}
        pylab.rcParams.update(params)
        fig = plt.figure(dpi=62)
        fig.set_facecolor('#222831')
        ax = fig.add_subplot(111)
        ax.set_facecolor('#222831')
        M_color = ['#e32249','#cf7500','#00bcd4','#2b580c','#ffc8bd']
        L_color =['#ff6464','#f0a500','#b2ebf2','#639a67','#ffebd9']
        index=0
        print(list(timeline.keys()))
        for item in list(timeline.keys()):
            A = list(timeline[item]['Deaths'])

            B = [A[item] for item in range(0,len(A) ,7)]
            
            if len(A)%7 != 0:
                B.append(A[-1])
            elif len(A)%7==0:
                B[-1] = A[-1]
            print(B)
            W = ['W'+str(item) for item in range(0 , len(B))]
            
            ax.plot(W , B , marker='o' ,markersize=13,markerfacecolor=M_color[index], color=L_color[index] , linewidth = 3)
            index+=1
        #ax.plot(W , D , marker='o' ,markersize=13,markerfacecolor='#e32249', color='#ff6464' , linewidth = 3)
        #ax.spines['bottom'].set_color('#222831')
        #ax.set_ylim(0, 450000)
        ax.set_xlabel('No. of Weeks' , labelpad=7 , fontsize = 17)
        ax.set_ylabel('No. of Deaths',labelpad=7 , fontsize = 17)
        ax.xaxis.label.set_color('#f1f1b0')
        ax.yaxis.label.set_color('#f1f1b0')
        #ax.legend.color('white')

        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        plt.grid(visible = False)
        plt.legend(list(timeline.keys()))
        plt.savefig('CountryDeathsComparison.png' , facecolor ='#222831')

    def createLayout(self , name):
        self.name = name
        self.frame_8 = QtWidgets.QFrame()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_8.sizePolicy().hasHeightForWidth())
        self.frame_8.setSizePolicy(sizePolicy)
        self.frame_8.setMinimumSize(QtCore.QSize(0, 0))
        self.frame_8.setMaximumSize(QtCore.QSize(257, 155))
        self.frame_8.setStyleSheet("background-color:#222831;")
        self.frame_8.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_8.setObjectName(self.name)
        self.gridLayout_4 = QtWidgets.QGridLayout(self.frame_8)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setSpacing(7)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.verticalLayout_17 = QtWidgets.QVBoxLayout()
        self.verticalLayout_17.setSpacing(2)
        self.verticalLayout_17.setObjectName("verticalLayout_17")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
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
        self.horizontalLayout.addWidget(self.label_10)
        self.verticalLayout_17.addLayout(self.horizontalLayout)
        self.label_2 = QtWidgets.QLabel(self.frame_8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QtCore.QSize(120, 60))
        self.label_2.setMaximumSize(QtCore.QSize(120, 60))
        self.label_2.setText("")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_17.addWidget(self.label_2)
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.label_4 = QtWidgets.QLabel(self.frame_8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
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
        self.verticalLayout_17.addLayout(self.horizontalLayout_15)
        self.horizontalLayout_9.addLayout(self.verticalLayout_17)
        self.verticalLayout_14 = QtWidgets.QVBoxLayout()
        self.verticalLayout_14.setContentsMargins(0, -1, -1, -1)
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
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setContentsMargins(0, -1, -1, -1)
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
        self.horizontalLayout_10.addWidget(self.label_16)
        self.verticalLayout_14.addLayout(self.horizontalLayout_10)
        self.horizontalLayout_9.addLayout(self.verticalLayout_14)
        self.gridLayout_4.addLayout(self.horizontalLayout_9, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.frame_8, 0, 0, 1, 1)
        #mainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi1()
        print(self.frame_8.size())
        print(self.count)
        if self.count > 5 and self.count <= 10:
            self.verticalLayout.addWidget(self.frame_8)
        elif self.count <= 5:
            self.verticalLayout_2.addWidget(self.frame_8)
        else:
            self.scroll_Vir_Layout.addWidget(self.frame_8)
            self.Frames[self.name] = self.frame_8

    def retranslateUi1(self):
        self.label_10.setText(str(self.countryName))
        self.label_16.setText(str(self.casesPM)+" CPM")
        self.label_6.setText(str(self.cases)+" C")
        self.label_8.setText(str(self.deaths)+" D")
        self.label_17.setText(str(self.recovered)+" R")
        self.label_18.setText(str(self.tests) + " T")
        self.label_4.setText(str(self.deathsPM) + " DPM")
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
