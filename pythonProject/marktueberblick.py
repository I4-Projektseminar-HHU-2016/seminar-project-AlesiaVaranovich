import tkinter as tk
import re
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg

LARGE_FONT = ("Verdana", 12)

class Main (tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self.geometry("800x750"))
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

def additionalInformation(data, varFirstTrade, varCurrency, varLowPrice, varHighPrice):
    reLowPrice = re.search("low:(.+?),", data)
    if reLowPrice:
        varLowPrice.set('Lowest price:'+reLowPrice.group(1))
    reHighPrice = re.search("previous_close_price:(.*)", data)
    if reHighPrice:
        varHighPrice.set('Previous close price:'+reHighPrice.group(1))
    reCurrency = re.search("currency:(.*)", data)
    if reCurrency:
        varCurrency.set('Currency:'+reCurrency.group(1))
    FirstTrade = re.search("first-trade:(.*)", data)
    if FirstTrade:
        varFirstTrade.set('First-Trade:'+FirstTrade.group(1))

class GraphPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        varCompanyName  = tk.StringVar()
        companyName = tk.Label(self,textvariable=varCompanyName)
        varCompanyName.set('Company Name:')
        varLowPrice = tk.StringVar()
        lowPrice = tk.Label(self,textvariable=varLowPrice)
        varLowPrice.set('Lowest price:')
        varHighPrice = tk.StringVar()
        highPrice = tk.Label(self,textvariable=varHighPrice)
        varHighPrice.set('Previous close price:')
        varCurrency = tk.StringVar()
        currency = tk.Label(self,textvariable=varCurrency)
        varCurrency.set('Currency:')
        varFirstTrade = tk.StringVar()
        firstTrade = tk.Label(self,textvariable=varFirstTrade)
        varFirstTrade.set('First Trade:')
        optionVariable = tk.StringVar(self)
        optionVariable.set('1m')
        optionMenu = tk.OptionMenu(self, optionVariable, '1m','3m','6m','1y','2y','5y','10y')
        label = tk.Label(self, text='Market Graph Builder', font=LARGE_FONT)
        search = tk.Button(self, text='Search')
        search.pack()
        search.place(x=445,y=30)
        label.pack(pady=10,padx=10)
        fig = Figure (figsize=(8,6), dpi=100)
        graph = fig.add_subplot(111)
        canvas = FigureCanvasTkAgg(fig,self)
        toolbar= NavigationToolbar2TkAgg(canvas,self)
        label2 = tk.Label(self, text="Market Index:")
        label3 = tk.Label(self, text="Time period:")
        IndexEntry=tk.Entry(self)
        label2.place(x=2,y=65)
        label3.place(x=210,y=65)
        IndexEntry.place(x=80,y=65)
        optionMenu.place(x=285,y=60)
        companyName.place(x=4,y=96)
        lowPrice.place(x=150,y=96)
        highPrice.place(x=320,y=96)
        currency.place(x=450,y=96)
        firstTrade.place(x=520,y=96)
app = Main()
app.mainloop()