#!/usr/bin/env python
# coding: utf-8

# In[ ]:
import matplotlib.pyplot as plt
import sqlite3
import pandas as pd
import numpy as np

from fbprophet import Prophet



def del_table(cursor, name):
    query = """DROP TABLE {}""".format(name)
    cursor.execute(query + ";")


# In[ ]:


def create_table(cursor, name):
    query = """CREATE TABLE {} (date text, open FLOAT, high FLOAT, low FLOAT, close FLOAT, adj_close FLOAT, volume INTEGER)""".format(name)
    cursor.execute(query + ";")

def insert(cursor, name, values):
    query = """INSERT INTO {} VALUES(?, ?, ?, ?, ?, ?, ?)""".format(name) + ";"
    
    cursor.execute(query, values)

# def retrieve(c,name):
#     query = """SELECT * FROM {}""".format(name) + ";"
#     c.execute(query)
    
#     rows = c.fetchall()
    
#     for row in rows[:5]:
#         print(row)


# In[ ]:


def retrieve(c,name):
    # ------ Getting from SQL DB ----- # 
    query = """SELECT * FROM {}""".format(name) + ";"
    c.execute(query)
    
    rows = c.fetchall()
    data = []
    for row in rows:
        data.append(row)

    # ----- Cleaning output ----- #
    columns = ['Date','Open','High','Low','Close','Adj_Close','Volume']
    data = pd.DataFrame(data, columns = columns)
    
    #clean data
    data['Date'] = pd.to_datetime(data['Date'])
    data['Volume'] = [int.from_bytes(value, byteorder = 'little') for value in data['Volume']]
    
    return data


# In[ ]:


def prophetize(data,p):
    m = Prophet() #initailize
    
    #format data
    df = data.loc[:,['Date','Open']]
    df.rename(columns = {'Date': 'ds', 'Open': 'y'}, inplace = True)
    
    #fit and forecast
    model = m.fit(df) 
    future_frame = model.make_future_dataframe(periods=p, freq = 'W')
    forecast = model.predict(future_frame)
    
    #Get summary stats
    summary = pd.DataFrame()
    summary['Original'] = data['Open'].values
    summary['Forecast'] = forecast['yhat'].values[:-4]
    
    summary['Error'] = summary['Forecast'] - summary['Original']
    summary['Error^2'] = summary['Error']**2
    
    RMSE = np.sqrt(sum(summary['Error^2']/len(summary)))
    
    return (RMSE, forecast, summary)

