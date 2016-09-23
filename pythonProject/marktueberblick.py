import tkinter as tk
import re
from tkinter import messagebox
import urllib
from urllib.error import HTTPError
import numpy
import matplotlib.dates as mDates
import matplotlib.pyplot as mPyplot
import matplotlib.ticker as mTicker

import datetime

from matplotlib.finance import volume_overlay
from matplotlib.finance import candlestick_ohlc


LARGE_FONT = ("Verdana", 12)

class Main (tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self.geometry("600x150"))
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}

        # tuple of all Frames in application
        for F in (HomePage,GraphPage,HelpPage):
          frame = F(container, self)
          self.frames[F] = frame
          frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(HomePage)
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Home Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button3 = tk.Button(self, text="Market graph",
                            command=lambda: controller.show_frame(GraphPage))
        button3.pack()

        button = tk.Button(self, text="Help",
                            command=lambda: controller.show_frame(HelpPage))
        button.pack()


class HelpPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Info.", font=LARGE_FONT)
        label.pack(pady=4,padx=10)
        objText=tk.Text(self, height=6, width=67)
        objText.pack()
        objText.insert('end', "Yahoo Finance provide some possibility to do search by Index on the\n"
                              "differents Stock Exchange."
                              " For that's enough add dot and market suffix to index. "
                              "\nFor example BMW.MI to do serch on milan Stock/BMW.F farnkfurt Stock"
                              "\nLiast of all Yahoo suffix : http://www.jarloo.com/yahoo_finance/"
                              "\nGoogle finance doesn't work with such of suffix! ")
        button = tk.Button(self, text="Home Page", command=lambda: controller.show_frame(HomePage))
        button.pack()

def additionalInformationCompanyName(data):
    if "Company-Name:" in data:
        reCompanyName = re.search("Company-Name:(.*)", data)
        reCompanyName = reCompanyName.group(1)+"/"
    else:
        reCompanyName = ""
    return reCompanyName


def additionalInformation(data):
    additionalData =""
    reExchangeName = re.search("Exchange-Name:(.*)", data)
    if reExchangeName:
        additionalData = additionalData + "Exchange-Name:" + reExchangeName.group(1) +"\n"

    reFirstTrade = re.search("first-trade:(.*)", data)
    if reFirstTrade:
        additionalData = additionalData + "First-trade:" + reFirstTrade.group(1) +"\n"

    reLastTrade = re.search("last-trade:(.*)", data)
    if reLastTrade:
        additionalData = additionalData + "Last-trade:" + reLastTrade.group(1) +"\n"

    reCurrency = re.search("currency:(.*)", data)
    if reCurrency:
        additionalData = additionalData + "Currency:" + reCurrency.group(1) +"   "

    rePrClosePrice = re.search("previous_close_price:(.*)", data)
    if rePrClosePrice:
        additionalData =  additionalData + "Previous close price:" + rePrClosePrice.group(1) +" "+ reCurrency.group(1)+"\n"

    #reLowPrice = re.search("low:(.+?),", data)
    #if reLowPrice:
    #    additionalData = reLowPrice
    #print ("-----------------------------")

    #print (additionalData)
    return additionalData

class GraphPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def autoFillIndexEntry(event):
            selected = optionIntervalCompanie.get()
            if selected == "Google(Alphabet Inc.)":
                IndexEntry.delete(0, 'end')
                IndexEntry.insert(0,"GOOG")
            elif selected == "Apple Inc.":
                IndexEntry.delete(0, 'end')
                IndexEntry.insert(0,"AAPL")
            elif selected == "Deutsche Bank AG":
                IndexEntry.delete(0, 'end')
                IndexEntry.insert(0,"DB")
            elif selected == "Barclays":
                IndexEntry.delete(0, 'end')
                IndexEntry.insert(0,"BCS")
            elif selected == "Nintendo Co., Ltd.":
                IndexEntry.delete(0, 'end')
                IndexEntry.insert(0,"7974")
            elif selected == "Volkswagen Group":
                IndexEntry.delete(0, 'end')
                IndexEntry.insert(0,"VLKAY")

        optionIntervalVariable = tk.StringVar(self)
        optionIntervalVariable.set('1m')

        optionIntervalCompanie = tk.StringVar(self)
        optionIntervalCompanie.set('')

        #Objects
        optionIntervalMenu  = tk.OptionMenu(self,  optionIntervalVariable, '1m','3m','6m','1y','2y','5y','10y')
        optionCompaniesMenu = tk.OptionMenu(self,  optionIntervalCompanie, "Google(Alphabet Inc.)", "Apple Inc." ,
                                            "Deutsche Bank AG","Barclays", "Nintendo Co., Ltd.","Volkswagen Group",
                                            command=autoFillIndexEntry)

        searchYahooFinance = tk.Button(self, text="Yahoo Finance ",
                                       command=lambda: marketGraph(IndexEntry.get(),optionIntervalVariable.get(),"Yahoo"))
        searchGoogleFinance = tk.Button(self, text="Google Finance",
                                        command=lambda: marketGraph(IndexEntry.get(),optionIntervalVariable.get(),"Google"))

        labeTitel = tk.Label(self, text='Market Graph Builder', font=LARGE_FONT)
        labelMarketIndex = tk.Label(self, text="Market Index:")
        labelTimeperiod = tk.Label(self, text="Time period:")
        labelCompany = tk.Label(self, text="Company name:")

        IndexEntry=tk.Entry(self)

        #American Stock Exchange	N/A
        #BATS Exchange	N/A
        #Dow Jones Indexes	N/A
        #NASDAQ Stock Exchange	N/A
        #New York Stock Exchange	N/A
        #S & P Indices	N/A
        #Nikkei Indices	N/A

        searchYahooFinance.pack()
        searchGoogleFinance.pack()

        #Entry position (x,y)
        IndexEntry.place(x=80,y=65)

        #labels position (x,y)
        labeTitel.pack(pady=10,padx=10)
        labelMarketIndex.place(x=2,y=65)

        labelCompany.place(x=210,y=50)
        labelTimeperiod.place(x=210,y=80)

        #OptionMenu position (x,y)
        optionIntervalMenu.place(x=310,y=80)
        optionCompaniesMenu.place(x=310,y=50)

        #Buttons position (x,y)
        searchYahooFinance.place(x=475,y=50)
        searchGoogleFinance.place(x=475,y=80)

#percent of price change during the day(open and close price)
def procentOfDayChangePrice(openp, closep):
    return (closep*100/openp)-100

#def getData(MarketIndex,optionMenu,source):

def datestr2num(fmt):
    def converter(b):
        return mDates.strpdate2num(fmt)(b.decode('utf-8'))
    return converter

def prepareURL(MarketIndex,optionMenu,source):
    if len(source) == 5:
        stockPriceURL = 'http://chartapi.finance.yahoo.com/instrument/1.0/' + MarketIndex+ \
                        '/chartdata;type=quote;range='+optionMenu+'/csv'
    else:
        if "y" in optionMenu:
            graphInterval= optionMenu.replace("y", "Y")
            print(graphInterval)
        else:
            graphInterval= str(int(optionMenu.replace("m", "")) * 30) + "d"
            print(graphInterval)
        stockPriceURL = 'https://www.google.com/finance/getprices?q=' + MarketIndex + \
                        '&i=86401&p=' + graphInterval + '&f=d,o,h,l,c,v'
    return stockPriceURL


def marketGraph(MarketIndex,optionMenu,source):
    dateFormat = "%Y%m%d"
    try:
        data = urllib.request.urlopen(prepareURL(MarketIndex,optionMenu,source)).read().decode("utf-8")
    except HTTPError as e:
        print('Error code: ', e.code)
        messagebox.showinfo('Error', 'Index not found. you can type z. B.: BAC or AAPL...etc.')
    else:
        if 'message:No symbol found - symbol' not in data and 'EXCHANGE%3DUNKNOWN+EXCHANGE' not in data :
            fig = mPyplot.figure(figsize=(8.0, 8.0),facecolor='#f0f0f0')
            graph1 = mPyplot.subplot2grid((6,1), (0,0), rowspan=1, colspan=1)
            mPyplot.title(additionalInformationCompanyName(data)+ MarketIndex +"(" + optionMenu +")", color='#115252')
            mPyplot.ylabel('%')
            graph2 = mPyplot.subplot2grid((6,1), (1,0), rowspan=4, colspan=1, sharex=graph1)
            mPyplot.ylabel('Price')
            graph3 = mPyplot.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=graph1)
            mPyplot.ylabel('Volume')
            marketData = []
            #dateGraph = []
            #ohlc = []
            splitSource = data.split('\n')
            #print (splitSource)
            i=0
            for line in splitSource:

                split_line = line.split(',')
                # more than 6 elements in row and exclude row with "labels" and "values" from result
                if len(split_line) == 6:
                    if 'labels' not in line and 'values' not in line and len(source)==5:
                        i+=1
                        marketData.append(datetime.datetime.strptime(line[0:8],"%Y%m%d").strftime(dateFormat)+ line[8:]+",1")
                    elif "COLUMNS" not in line and "DATA_SESSIONS" not in line and len(source)==6  :
                        i+=1
                        marketData.append(datetime.datetime.fromtimestamp(int(line[1:11])).strftime(dateFormat)+ line[11:]+","+str(i))

            date, closep, highp, lowp, openp, volume, rowN = numpy.loadtxt(marketData, delimiter=',',
                                                                           unpack=True, converters={0:  datestr2num(dateFormat)})

            iterrator2 = 0
            ohlc = []
            while iterrator2 < i:
                listTmp = date[iterrator2], openp[iterrator2], highp[iterrator2], lowp[iterrator2], closep[iterrator2], volume[iterrator2]
                print(listTmp)
                ohlc.append(listTmp)
                iterrator2 +=1
                rowN=date

            priceChangesDuringTheDay = list(map(procentOfDayChangePrice, closep, openp))
            graph1.plot_date(rowN,priceChangesDuringTheDay,'-', label="percent of price change during the day")
            graph1.yaxis.set_major_locator(mTicker.MaxNLocator(nbins=4, prune="lower"))

            #quotes : sequence of (time, open, high, low, close, ...) sequences
            candlestick_ohlc(graph2, ohlc, width=0.3, colorup='#ade7ae', colordown='#E57878')
            graph2.yaxis.set_major_locator(mTicker.MaxNLocator(nbins=7, prune='upper'))
            graph2.grid(True)

            graph3.plot_date(rowN,volume,'-', label="Volume")
            graph3.yaxis.set_major_locator(mTicker.MaxNLocator(nbins=4, prune="lower"))

            graph3.fill_between(rowN,0, volume, facecolor='#4CA1BE', alpha=0.3)
            graph3.grid(False)
            graph3.set_ylim(0, 4*volume.max())

            if len(source)==5:
                graph3.xaxis.set_major_formatter(mDates.DateFormatter(dateFormat))
            else:
                graph3.xaxis.set_major_formatter(mDates.DateFormatter(dateFormat))
            graph3.xaxis.set_major_locator(mTicker.MaxNLocator(10))
            graph3.yaxis.set_major_locator(mTicker.MaxNLocator(nbins=4, prune="upper"))
            for label in graph3.xaxis.get_ticklabels():
                label.set_rotation(45)
            mPyplot.setp(graph1.get_xticklabels(), visible=False)
            mPyplot.setp(graph2.get_xticklabels(), visible=False)
            mPyplot.subplots_adjust(left=0.11, bottom=0.23, right=0.95, top=0.95, wspace=0.2, hspace=0)
            mPyplot.figtext(.1, .0, ""+ additionalInformation(data))
            mPyplot.show()
        else:
                messagebox.showinfo("Error", "Index not found. you can type z. B.: BAC or AAPL...etc.")
app = Main()
app.mainloop()