import tkinter as tk
import re
from tkinter import messagebox
import urllib
from urllib.error import HTTPError
import numpy
import matplotlib.dates as mDates
import matplotlib.pyplot as mPyplot
import matplotlib.ticker as mTicker


LARGE_FONT = ("Verdana", 12)

class Main (tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self.geometry("800x150"))
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (GraphPage , TBD):#TBD
          frame = F(container, self)
          self.frames[F] = frame
          frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(GraphPage)
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class TBD(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

def additionalInformation(data):
    reCompanyName = re.search("Company-Name:(.*)", data)
    #print (data)
    #print (reCompanyName)
    if reCompanyName:
        additionalData = "Company-Name:" + reCompanyName.group(1)+"\n"

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
        additionalData = additionalData + "Currency:" + reCurrency.group(1) +"\n"

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
        optionVariable = tk.StringVar(self)
        optionVariable.set('1m')
        optionMenu = tk.OptionMenu(self, optionVariable, '1m','3m','6m','1y','2y','5y','10y')
        label = tk.Label(self, text='Market Graph Builder', font=LARGE_FONT)
        searchButton = tk.Button(self, text="Search",command=lambda: marketGraph(IndexEntry.get(),optionVariable.get()))
        searchButton.pack()
        searchButton.place(x=445,y=30)
        label.pack(pady=10,padx=10)
        label2 = tk.Label(self, text="Market Index:")
        label3 = tk.Label(self, text="Time period:")
        IndexEntry=tk.Entry(self)
        label2.place(x=2,y=65)
        label3.place(x=210,y=65)
        IndexEntry.place(x=80,y=65)
        optionMenu.place(x=285,y=60)

#percent of price change during the day(open and close price)
def procentOfDayChangePrice(openp, closep):
    return (closep*100/openp)-100

def datestr2num(fmt, encoding='utf-8'):
    strConverter = mDates.strpdate2num(fmt)
    def bytesConverter(b):
        s = b.decode(encoding)
        return strConverter(s)
    return bytesConverter

def marketGraph(MarketIndex,optionMenu):
    stockPriceURL = 'http://chartapi.finance.yahoo.com/instrument/1.0/'+"GOOG"+'/chartdata;type=quote;range='+optionMenu+'/csv'
    try:
        data = urllib.request.urlopen(stockPriceURL).read().decode()
    except HTTPError as e:
        print('Error code: ', e.code)
        messagebox.showinfo('Error', 'Index not found. you can type z. B.: BAC or AAPL...etc.')
    else:
        if 'message:No symbol found - symbol' not in data:

            fig = mPyplot.figure(figsize=(8.0, 8.0),facecolor='#f0f0f0')
            graph1 = mPyplot.subplot2grid((6,1), (0,0), rowspan=1, colspan=1)
            mPyplot.title(MarketIndex+" Charts" + "(" + optionMenu +")", color='#115252')
            mPyplot.ylabel('%')
            graph2 = mPyplot.subplot2grid((6,1), (1,0), rowspan=4, colspan=1, sharex=graph1)
            mPyplot.ylabel('Price')
            graph3 = mPyplot.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=graph1)
            mPyplot.ylabel('Volume')

            marketData = []
            splitSource = data.split('\n')
            for line in splitSource:
                split_line = line.split(',')
                # more than 6 elements in row and exclude row with "labels" and "values" from result
                if len(split_line) == 6:
                    if 'labels' not in line and 'values' not in line:
                        marketData.append(line)

            date, closep, highp, lowp, openp, volume = numpy.loadtxt(marketData, delimiter=',', unpack=True, converters={0: datestr2num('%Y%m%d')})

            # percent of price change during the day
            priceChangesDuringTheDay = list(map(procentOfDayChangePrice, closep, openp))
            graph1.plot(date,priceChangesDuringTheDay,'-', label='percent of price change during the day')
            graph1.yaxis.set_major_locator(mTicker.MaxNLocator(nbins=4, prune='lower'))

            graph2.plot(date, highp, linewidth=1, label='high')
            graph2.plot(date, lowp, linewidth=1, label='low')
            graph2.yaxis.set_major_locator(mTicker.MaxNLocator(nbins=4, prune='upper'))

            graph3.plot(date,volume,'-', label='volume')
            graph3.yaxis.set_major_locator(mTicker.MaxNLocator(nbins=4, prune='lower'))

            graph3.xaxis.set_major_formatter(mDates.DateFormatter('%Y-%m-%d'))
            graph3.xaxis.set_major_locator(mTicker.MaxNLocator(10))
            graph3.yaxis.set_major_locator(mTicker.MaxNLocator(nbins=4, prune='upper'))

            for label in graph3.xaxis.get_ticklabels():
                label.set_rotation(15)

            mPyplot.setp(graph1.get_xticklabels(), visible=False)
            mPyplot.setp(graph2.get_xticklabels(), visible=False)
            mPyplot.subplots_adjust(left=0.11, bottom=0.24, right=0.90, top=0.90, wspace=0.2, hspace=0)

            graph1.legend()
            leg = graph1.legend(loc=9, ncol=2,prop={'size':10})
            leg.get_frame().set_alpha(0.4)

            graph2.legend()
            leg = graph2.legend(loc=9, ncol=2,prop={'size':10})
            leg.get_frame().set_alpha(0.4)

            graph3.legend()
            leg = graph3.legend(loc=9, ncol=2,prop={'size':10})
            leg.get_frame().set_alpha(0.4)

            mPyplot.figtext(.1, .0, "\n \n \n \n \n"+ additionalInformation(data))

            mPyplot.show()
            fig.savefig(MarketIndex +'.png', facecolor=fig.get_facecolor())
        else:
                messagebox.showinfo('Error', 'Index not found. you can type z. B.: BAC or AAPL...etc.')
app = Main()
app.mainloop()