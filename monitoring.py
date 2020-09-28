import sys
import pandas as pd
import numpy as np
import sqlalchemy as sq
import scraper
import datetime
from trialconda import df_current
import trialconda
import mailing

"""
cron schedule for monitoring --> 0,30 9-16 * * 1-5 python monitoring.py
Monitors data every half an hour from 9am to 4pm Mon - Fri
If Hit Price decided by customer becomes more than the current price of stock it sends an email prompt to customer (if Hit Price remains high for the rest of day, it sends a prompt every half an hour)
Note : Before running this program, replace email with real email as the emails in current databse are not real
Replace in both if and else part
"""

# Scraped values in df_current contains commas which are replaced by "" and converted to float

df_current.set_index('Stock_symbol', inplace=True)
df_current = df_current.applymap(lambda x: x.replace(",", ""))
df_current = df_current.applymap(lambda x: float(x))

engine = sq.create_engine(
    "mysql+pymysql://root:password@localhost:3306/ethans1")  # connect to ethans1 database in mysql

# Client_Info Table stores the customer's personal info which is converted to pandas dataframe
#  set global for monitoring data of all the clients
client_df = pd.read_sql(
    "SELECT * FROM Client_Info",
    con=engine)


def monitor(client_id):

    # Exe_Info Table contains the Execution Info of customer's stocks converted into dtaframe exe_df

    engine = sq.create_engine(
        "mysql+pymysql://root:password@localhost:3306/ethans1")
    exe_df = pd.read_sql(
        "SELECT * FROM Exe_Info",
        con=engine)
# client_df defined again for local use

    client_df = pd.read_sql(
        "SELECT * FROM Client_Info",
        con=engine)
# Scrape_Sym is a column combined from Stock_Symbol and Market
# Eg. Stock_Symbol = 'INFY', Market = 'NS', Scrape_Sym = 'INFY.NS'
    for i in range(len(exe_df)):
        if (exe_df.loc[i, 'Stock_Symbol'] == np.nan) | (exe_df.loc[i, 'Market'] == np.nan):
            exe_df.loc[i, 'Scrape_Sym'] = np.nan
        else:
            exe_df.loc[i, 'Scrape_Sym'] = str(
                exe_df.loc[i]['Stock_Symbol']) + '.' + str(exe_df.loc[i]['Market'])

# gp_cl contains the groups sorted by Client_ID

    gp_cl = exe_df.groupby('Client_ID')

# gp_trn does a groupby on gp_cl by transaction 'Buy' or 'Sell' for each clients

    gp_trn = gp_cl.get_group(client_id).groupby('Transaction')

# If Customer hasn't sold any stock there won't be any 'Sell' group
# then this logic is implemented
    if gp_trn.ngroups == 1:

        buy_gp = gp_trn.get_group('Buy').reset_index()  # 'Buy' group of a client
        unique_sym_buy = buy_gp['Scrape_Sym'].unique()  # unique stock symbols in 'Buy' Group
        buy_quan_dic = dict()  # dictionary for quantity of stock

        # if stock is bought multiple times then total quantity is sum of all the quantity of bought stocks

        for i in unique_sym_buy:
            for j in range(len(buy_gp)):

                qnt = buy_gp.loc[(buy_gp['Scrape_Sym'] == i), 'Quantity'].agg(sum)
            buy_quan_dic[i] = qnt

        df_dic = dict()  # dictionary to create rep_df

        col = ['Stock', 'Market', 'Symbol', 'Active', 'Quantity', 'Hit Price',
               'Current price', 'Open', 'Close', '52 Week High', '52 Week Low']  # columns of rep_df

        for i in col:
            df_dic[i] = [np.nan]  # Initializing dictionary to np.nan

        symbol_list = unique_sym_buy.tolist()  # list of all the unique stock symbols in 'Buy' Group

        stock_list = list()
        market_list = list()

        # Stock List

        for i in symbol_list:
            for j in range(len(buy_gp)):
                if i in buy_gp.loc[j, ['Scrape_Sym', 'Stock']].values:
                    stock_list.append(buy_gp.loc[j, ['Scrape_Sym', 'Stock']].values[1])
                    break

        # Market List

        market_list = [i[-2:] for i in symbol_list]

        # Active List
        # Checks if stock is active
        # If no 'Sell' Group stock is always active

        active_list = []
        for i in symbol_list:
            active_list.append('Yes')

        # Quantity List

        quantity_list = []
        for i in symbol_list:
            quantity_list.append(buy_quan_dic[i])

        # Hitprice List

        hitprice_list = []
        for i in symbol_list:
            hitprice_list.append(buy_gp.loc[(buy_gp['Scrape_Sym'] == i), 'Hit_Price'].values[0])

        global df_current

        current_price_list = []
        open_list = []
        close_list = []
        week52_high_list = []
        week52_low_list = []
        for i in symbol_list:
            current_price_list.append(df_current.loc[i, 'Current price'])
            open_list.append(df_current.loc[i, 'Open'])
            close_list.append(df_current.loc[i, 'Close'])
            week52_high_list.append(df_current.loc[i, '52 Week High'])
            week52_low_list.append(df_current.loc[i, '52 Week Low'])

        df_dic['Stock'] = stock_list
        df_dic['Market'] = market_list
        df_dic['Symbol'] = symbol_list
        df_dic['Active'] = active_list
        df_dic['Quantity'] = quantity_list
        df_dic['Hit Price'] = hitprice_list
        df_dic['Current price'] = current_price_list
        df_dic['Open'] = open_list
        df_dic['Close'] = close_list
        df_dic['52 Week High'] = week52_high_list
        df_dic['52 Week Low'] = week52_low_list

        rep_df = pd.DataFrame(df_dic, columns=col)


# prompt only when stock is active and current price is higher than Hit price

        for i in range(len(rep_df)):
            if rep_df.loc[i, 'Active'] == 'Yes':
                if rep_df.loc[i, 'Current price'] > rep_df.loc[i, 'Hit Price']:

                    subject = "Prompt about your Stock"

# Email Content to be defined here

                    content = """Current Price of {0} is higher than Hit Price.
                        Hit Price : {1}\n
                        Current price : {2}\n
                        """.format(
                        rep_df.loc[i, 'Symbol'], rep_df.loc[i, 'Hit Price'], rep_df.loc[i, 'Current price'])

# Note : Emails in the Client_Info table in database are not real for this data

                    email = client_df.loc[(client_df['Client_ID'] ==
                                           int(client_id)), 'Email'].astype('str')
                    #email = 'noclues008@gmail.com'

                    mailing.send_mail(email, subject, content, 0)  # No attachment for monitoring

# If 'Sell' Group exists some calculations remain same but few are changed
# Then the following logic is implemented

    else:
        buy_gp = gp_trn.get_group('Buy').reset_index()  # 'Buy' Group

        sell_gp = gp_trn.get_group('Sell').reset_index()  # 'Sell' Group

        unique_sym_buy = buy_gp['Scrape_Sym'].unique()  # unique stock symbols in 'Buy' Group

        unique_sym_sell = sell_gp['Scrape_Sym'].unique()  # unique stock symbols in 'Sell' Group

        buy_quan_dic = dict()
        for i in unique_sym_buy:
            for j in range(len(buy_gp)):
                qnt = buy_gp.loc[(buy_gp['Scrape_Sym'] == i), 'Quantity'].agg(sum)
            buy_quan_dic[i] = qnt  # holds total quantity for 'Buy' Group

        sell_quan_dic = dict()
        for i in unique_sym_sell:
            for j in range(len(sell_gp)):
                qnt1 = sell_gp.loc[(sell_gp['Scrape_Sym'] == i), 'Quantity'].agg(sum)
            sell_quan_dic[i] = qnt1  # holds total quantity for 'Sell' Group

        current_quantity = dict()

# if particular stock not sold then current quantity remains same

        for i in buy_quan_dic:
            if i not in sell_quan_dic:
                current_quantity[i] = buy_quan_dic[i]

# if particular stock is sold then current quantity reduces

        for i in sell_quan_dic:
            current_quantity[i] = buy_quan_dic[i] - sell_quan_dic[i]

        df_dic = dict()  # dictionary for creating rep_df

        col = ['Stock', 'Market', 'Symbol', 'Active', 'Quantity', 'Hit Price',
               'Current price', 'Open', 'Close', '52 Week High', '52 Week Low']

        for i in col:
            df_dic[i] = [np.nan]  # Initializing dictionary to np.nan

        symbol_list = unique_sym_buy.tolist()  # if symbol exists in sell group it will surely exist in 'Buy' Group

# Same as previous case

        stock_list = list()
        market_list = list()
        for i in symbol_list:
            for j in range(len(buy_gp)):
                if i in buy_gp.loc[j, ['Scrape_Sym', 'Stock']].values:
                    stock_list.append(buy_gp.loc[j, ['Scrape_Sym', 'Stock']].values[1])
                    break

        market_list = [i[-2:] for i in symbol_list]

        active_list = []
        for i in symbol_list:
            if current_quantity[i] == 0:
                active_list.append('No')
            else:
                active_list.append('Yes')

        quantity_list = []
        for i in symbol_list:
            quantity_list.append(current_quantity[i])

# Logic for Hit price
# If Customers sells the stock, the new Hit Price will be recorded in Hit Price value if stock quantity is not zero

        hitprice_list = []
        for i in symbol_list:
            # youngest transaction date for 'Buy'
            buy_max_date = buy_gp.loc[(buy_gp['Scrape_Sym'] == i), 'Transaction_Date'].max()
            # youngest transaction date for 'Sell'
            sell_max_date = sell_gp.loc[(sell_gp['Scrape_Sym'] == i), 'Transaction_Date'].max()
            if i not in unique_sym_sell:
                hitprice_list.append(buy_gp.loc[((buy_gp['Scrape_Sym'] == i) & (
                    buy_gp['Transaction_Date'] == buy_max_date)), 'Hit_Price'].values[0])  # if not sold then the Hit price mentioned in the youngest transction in 'Buy' is the current Hit Price
            else:
                if buy_max_date > sell_max_date:
                    hitprice_list.append(buy_gp.loc[((buy_gp['Scrape_Sym'] == i) & (
                        buy_gp['Transaction_Date'] == buy_max_date)), 'Hit_Price'].values[0])  # if sold but youngest transaction is 'Buy'
                else:
                    hitprice_list.append(sell_gp.loc[((sell_gp['Scrape_Sym'] == i) & (
                        sell_gp['Transaction_Date'] == sell_max_date)), 'Hit_Price'].values[0])  # if 'Sell' is the youngest transaction

        current_price_list = []
        open_list = []
        close_list = []
        week52_high_list = []
        week52_low_list = []
        for i in symbol_list:
            current_price_list.append(df_current.loc[i, 'Current price'])
            open_list.append(df_current.loc[i, 'Open'])
            close_list.append(df_current.loc[i, 'Close'])
            week52_high_list.append(df_current.loc[i, '52 Week High'])
            week52_low_list.append(df_current.loc[i, '52 Week Low'])

        df_dic['Stock'] = stock_list
        df_dic['Market'] = market_list
        df_dic['Symbol'] = symbol_list
        df_dic['Active'] = active_list
        df_dic['Quantity'] = quantity_list
        df_dic['Hit Price'] = hitprice_list
        df_dic['Current price'] = current_price_list
        df_dic['Open'] = open_list
        df_dic['Close'] = close_list
        df_dic['52 Week High'] = week52_high_list
        df_dic['52 Week Low'] = week52_low_list

        rep_df = pd.DataFrame(df_dic, columns=col)

# if stock is active and current price > Hit price send the prompt

        for i in range(len(rep_df)):
            if rep_df.loc[i, 'Active'] == 'Yes':
                if rep_df.loc[i, 'Current price'] > rep_df.loc[i, 'Hit Price']:

                    subject = "Prompt about your Stock"

                    content = """Current Price of {0} is higher than Hit Price.
                        Hit Price : {1}\n
                        Current price : {2}\n
                        """.format(
                        rep_df.loc[i, 'Symbol'], rep_df.loc[i, 'Hit Price'], rep_df.loc[i, 'Current price'])

                    # print("Current Price of {0} is higher than Stock Price. Contact the client {1}".format(
                    #     rep_df.loc[i, 'Symbol'], client_id))
                    email = client_df.loc[(client_df['Client_ID'] ==
                                           int(client_id)), 'Email'].astype('str')
                    #email = 'noclues008@gmail.com'

                    mailing.send_mail(email, subject, content, 0)


# Monitoring for all the clients
Client_List = list(client_df['Client_ID'].values)

for i in Client_List:
    monitor(i)
