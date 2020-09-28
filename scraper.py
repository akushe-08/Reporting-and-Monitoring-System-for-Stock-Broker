import pandas as pd
import numpy as np
import sqlalchemy as sq
from datetime import date
import trialconda

# cron schedule for scraper --> 31 15 * * 1-5 python scraper.py

# connect with mysql database ethans1
engine = sq.create_engine("mysql+pymysql://root:password@localhost:3306/ethans1")

# read table Exe_Info which contains the execution info of the customer's stock
exe_df = pd.read_sql(
    "SELECT * FROM Exe_Info",
    con=engine)
# Scrape_Sym is a column combined from Stock_Symbol and Market
# Eg. Stock_Symbol = 'INFY', Market = 'NS', Scrape_Sym = 'INFY.NS'
for i in range(len(exe_df)):
    if (exe_df.loc[i, 'Stock_Symbol'] == np.nan) | (exe_df.loc[i, 'Market'] == np.nan):
        exe_df.loc[i, 'Scrape_Sym'] = np.nan
    else:
        exe_df.loc[i, 'Scrape_Sym'] = str(
            exe_df.loc[i]['Stock_Symbol']) + '.' + str(exe_df.loc[i]['Market'])

# scrape_list is a list of all the unique symbols whose values are required to be scraped
scrape_list = list(exe_df['Scrape_Sym'].unique())
for i in range(len(scrape_list)):
    # get_price() stores all the scraped values to df_current which is set as global in trialconda
    trialconda.get_price(str(scrape_list[i]))
"""
If Scraper is executed, all the scraped data is stored to a table 'scrape_data' in ethans1 database
Scraper should be executed at the end of the day to store all the scraped data in sql table

If imported only scrapes the data and stores in df_current
"""

if __name__ == '__main__':
    data = trialconda.df_current.copy()
    today = date.today()
    list_today = [today for i in range(len(data))]
    data.insert(loc=0, column='Date', value=list_today)
    dbConnection = engine.connect()
    data.to_sql('scrape_data', dbConnection, if_exists='append')
    dbConnection.close()
