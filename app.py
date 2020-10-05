from flask import Flask, render_template,request
from functions import *
import seaborn as sns

from os import listdir, chdir

import json

import matplotlib.pyplot as plt
import sqlite3
import pandas as pd
import numpy as np

from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_pacf
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.arima_model import ARMA

app = Flask(__name__)

# @app.route("/")
# def home():
# 	return "hi"

#dropdown menu for selecting ETF, testing with colors
# @app.route("/", methods=['GET'])
# def dropdown():
#     colours = ['Red', 'Blue', 'Black', 'Orange']
#     return render_template("home.html", colours=colours)

# if __name__ == '__main__':
#     app.run()


@app.route("/", methods = ['POST','GET'])
def home():
	# need to format the tickers so they are actual chars
	# if request.method == 'POST':
	# 	selection = 
	# elif request.method == 'GET':
	with open('tickers.txt') as file:
		tickers = json.load(file)

	return render_template('home.html',ETFs = tickers)	

@app.route("/run", methods = ['POST','GET'])
def run():
    conn = sqlite3.connect('ETF.db')
    c = conn.cursor()

    #erros dict for 
    results = {}
    fail_batch = []
    #look through the database and run a prophet model to find lowest error
    for t in listdir('./data')[:5]:
        ticker, ext = t.split('.')

        if ext != 'csv':
            continue
        try:
            fetch = retrieve(c,ticker)
            if len(fetch) < 50:
                fail_batch.append(ticker)
                continue
            error, forecast, summary = prophetize(fetch,4)
            results[ticker] = error

        except TypeError:
            fail_batch.append(ticker)
            continue

        print('-next iter-')

    #find the min error and the resulting key value pair
    min_error = min(results.values())
    min_error_rounded =format(min(results.values()),'.4f')
    out = [key for key in results if results[key] == min_error]

    return render_template('model.html', out=out, min_error = min_error_rounded)
#see the tickers associated with the lowest RMSE
    # print('Tickers of interest: ', out)
    # print('With the lowest error of: ', min_error)
    # print('Failed batches at :', fail_batch)

@app.route("/{ETF}")
def visualize(ETF):
	conn = sqlite3.connect('ETF.db')
	c = conn.cursor()

	data = retrieve(c,etf)
	graph = sns.lineplot(data['Date'],data['Open'])

	return render_template('visualizations.html',data = data, graph = graph)

@app.route("/about")
def about():
	return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True)