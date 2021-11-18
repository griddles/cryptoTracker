import tkinter as tk
from tkinter import ttk
from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import crypto

# set up the tkinter window
root = Tk()
root.title("Crypto Tracker")

# get the values for the 5 different cryptocurrencies, and a total value
btc = crypto.getTradeRate("btcusd")
eth = crypto.getTradeRate("ethusd")
sol = crypto.getTradeRate("soleur") * 1.13104 # iexCloud doesnt let you get solana and chainlink in USD so i get them
ltc = crypto.getTradeRate("ltcusd")
link = crypto.getTradeRate("linkeur") * 1.13104 # in euros and then convert to USD (roughly)
total = btc + eth + sol + ltc + link

# create the strings that will be displayed
btcText = "Bitcoin to USD is currently ${0:,.2f}.".format(btc)
ethText = "Ethereum to USD is currently ${0:,.2f}.".format(eth)
solText = "Solana to USD is currently ${0:,.2f}.".format(sol)
ltcText = "Litecoin to USD is currently ${0:,.2f}.".format(ltc)
linkText = "Chainlink to USD is currently ${0:,.2f}.".format(link)
totalText = "Total value is currently ${0:,.2f}.".format(total)

# the start date all the graphs use
graphDate = "2021-11-11"

# set up the main window and pad the edges a little bit
mainframe = ttk.Frame(root, padding="30 3 30 3")
# set up the grid to align all the elements in the window
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# set up each graph (i dont think you can use a loop for this so its really repetitive)
btcGraph = crypto.getPriceGraph("BTC", "USD", graphDate)
figure1 = plt.Figure(figsize=(5,4), dpi=69)
ax1 = figure1.add_subplot(111)
line1 = FigureCanvasTkAgg(figure1, root)
line1.get_tk_widget().grid(column=0, row=0, sticky=N)
df1 = btcGraph[['date','close']].groupby('date').sum()
df1.plot(kind='line', legend=False, ax=ax1)
ax1.set_title('Bitcoin values | 1 week')

ethGraph = crypto.getPriceGraph("ETH", "USD", graphDate)
figure2 = plt.Figure(figsize=(5,4), dpi=69)
ax2 = figure2.add_subplot(111)
line2 = FigureCanvasTkAgg(figure2, root)
line2.get_tk_widget().grid(column=1, row=0, sticky=N)
df2 = ethGraph[['date','close']].groupby('date').sum()
df2.plot(kind='line', legend=False, ax=ax2)
ax2.set_title('Ethereum values | 1 week')

solGraph = crypto.getPriceGraph("SOL", "USD", graphDate)
figure3 = plt.Figure(figsize=(5,4), dpi=69)
ax3 = figure3.add_subplot(111)
line3 = FigureCanvasTkAgg(figure3, root)
line3.get_tk_widget().grid(column=2, row=0, sticky=N)
df3 = solGraph[['date','close']].groupby('date').sum()
df3.plot(kind='line', legend=False, ax=ax3)
ax3.set_title('Solana values | 1 week')

ltcGraph = crypto.getPriceGraph("LTC", "USD", graphDate)
figure4 = plt.Figure(figsize=(5,4), dpi=69)
ax4 = figure4.add_subplot(111)
line4 = FigureCanvasTkAgg(figure4, root)
line4.get_tk_widget().grid(column=0, row=3, sticky=N)
df4 = ltcGraph[['date','close']].groupby('date').sum()
df4.plot(kind='line', legend=False, ax=ax4)
ax4.set_title('Litecoin values | 1 week')

linkGraph = crypto.getPriceGraph("LINK", "USD", graphDate)
figure5 = plt.Figure(figsize=(5,4), dpi=69)
ax5 = figure5.add_subplot(111)
line5 = FigureCanvasTkAgg(figure5, root)
line5.get_tk_widget().grid(column=1, row=3, sticky=N)
df5 = linkGraph[['date','close']].groupby('date').sum()
df5.plot(kind='line', legend=False, ax=ax5)
ax5.set_title('Chainlink values | 1 week')

totalGraph = crypto.combineGraphs([btcGraph, ethGraph, solGraph, ltcGraph, linkGraph])
figure6 = plt.Figure(figsize=(5,4), dpi=69)
ax6 = figure6.add_subplot(111)
line6 = FigureCanvasTkAgg(figure6, root)
line6.get_tk_widget().grid(column=2, row=3, sticky=N)
df6 = totalGraph[['date','close']].groupby('date').sum()
df6.plot(kind='line', legend=False, ax=ax6)
ax6.set_title('Total values | 1 week')

# add the labels for the current crypto values under each graph
ttk.Label(root, text=btcText).grid(column=0, row=1, sticky=N)
ttk.Label(root, text=ethText).grid(column=1, row=1, sticky=N)
ttk.Label(root, text=solText).grid(column=2, row=1, sticky=N)
ttk.Label(root, text=ltcText).grid(column=0, row=4, sticky=N)
ttk.Label(root, text=linkText).grid(column=1, row=4, sticky=N)
ttk.Label(root, text=totalText).grid(column=2, row=4, sticky=N)

# show the window
root.mainloop()
