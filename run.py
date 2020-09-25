from os import listdir, chdir

import matplotlib.pyplot as plt
import sqlite3
import pandas as pd
import numpy as np

from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_pacf
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.arima_model import ARMA

from functions import *

# -------------------------------------------- #

#Connect to existing database, here is currently a sqlite db located in same directory
conn = sqlite3.connect('ETF.db')
c = conn.cursor()

#erros dict for 
results = {}

#look through the database and run a prophet model to find lowest error
for t in listdir('./data'):
    ticker, ext = t.split('.')

    if ext != 'csv':
        continue

    fetch = retrieve(c,ticker)

    error, forecast, summary = prophetize(fetch,4)

    results[ticker] = error
    print('-next iter-')

#find the min error and the resulting key value pair
min_error = min(results.values())
out = [key for key in results if results[key] == min_error]

#see the tickers associated with the lowest RMSE
print('Tickers of interest: ', out)
print('With the lowest error of: ', min_error)
