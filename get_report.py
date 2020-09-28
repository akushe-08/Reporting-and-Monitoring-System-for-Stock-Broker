#!/home/akushe_08/anaconda3/envs/my_env/bin/python
from IPython.display import display
import sys
import pandas as pd
import numpy as np
import sqlalchemy as sq
import matplotlib.pyplot as plt
import scraper
import datetime
from trialconda import df_current
import trialconda
import mailing

"""
cron schedule for weekly report --> 31 15 * * 5 python get_report.py
This program creates the Customer report (Weekly if scheduled or on demand base) in 'xlsx' format and automatically sends the customer as an attachment


"""


# Scraped values in df_current contains commas which are replaced by "" and converted to float

df_current.set_index('Stock_symbol', inplace=True)
df_current = df_current.applymap(lambda x: x.replace(",", ""))
df_current = df_current.applymap(lambda x: float(x))

engine = sq.create_engine(
    "mysql+pymysql://root:password@localhost:3306/ethans1")
# connect to ethans1 database in mysql

# Client_Info Table stores the customer's personal info which is converted to pandas dataframe
#  set global if it is required to create reports of all clients and send them by email

client_df = pd.read_sql(
    "SELECT * FROM Client_Info",
    con=engine)


def get_rep(client_id, *args):

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

    gp_trn = gp_cl.get_group(int(client_id)).groupby('Transaction')

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
# comment print statements if displaying is not required
        print('Current information regarding the stocks--------------\n')
        print(rep_df)

# Note : Profit Loss margin is only calculated if customer has sold any stock which in this if case does not hold true

# DataFrame for transaction History sorted by transaction date
        transaction_history = gp_cl.get_group(int(client_id)).sort_values(by='Transaction_Date')
        transaction_history = transaction_history.reset_index()

        # dropping extra column created by reset_index()

        transaction_history.drop('index', axis=1, inplace=True)
        print('Transaction History of the customer--------------\n')
        print(transaction_history)
        # display(df_current)

# DataFrame for Client Information from first SQL Table
        client_info = client_df.loc[client_df['Client_ID'] == int(client_id)].transpose()
        client_info.columns = ['']

# Writes all the dataframes to seperate sheets
# Report file name is kept variable and will change as per client ID

        with pd.ExcelWriter('Client_{}_Report.xlsx'.format(int(client_id)), engine='xlsxwriter') as writer:
            client_info.to_excel(writer, sheet_name='Customer Info')
            rep_df.to_excel(writer, sheet_name='Current Stock Info', index=False)
            transaction_history.to_excel(writer, sheet_name='Transaction History', index=False)


# Email Content to be defined here
# Comment out the following logic if sending email is required
# Note that the path of excel file to be sent by mail should be same as when created

# Note : Emails in the Client_Info table in database are not real for this data

        # subject = "Weekly Report"
        #
        # content = """ Report for this week """
        #
        # # print("Current Price of {0} is higher than Stock Price. Contact the client {1}".format(
        # #     rep_df.loc[i, 'Symbol'], client_id))
        # email = client_df.loc[(client_df['Client_ID'] ==
        #                        int(client_id)), 'Email'].astype('str')
        # #email = 'noclues008@gmail.com'
        #
        # path = 'Client_{}_Report.xlsx'.format(int(client_id))
        #
        # mailing.send_mail(email, subject, content, path)


# If 'Sell' Group exists some calculations remain same but few are changed
# Then the following logic is implemented

    else:
        buy_gp = gp_trn.get_group('Buy').reset_index()  # Buy Group

        sell_gp = gp_trn.get_group('Sell').reset_index()  # Sell Group

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
                    buy_gp['Transaction_Date'] == buy_max_date)), 'Hit_Price'].values[0])
                # if not sold then the Hit price mentioned in the youngest transction in 'Buy' is the current Hit Price
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
        print('Current information regarding the stocks--------------\n')
        print(rep_df)

# Logic for Profit Loss margin
# Profit or Loss are split and then added to calculate Profit Loss Margin for each stock if stock is bought or sold multiple times
# Note : Profit Loss Margin is calculated only if customer has sold any number of stocks

        buy_sort = buy_gp.sort_values(by='Transaction_Date')
        sell_sort = sell_gp.sort_values(by='Transaction_Date')

        profit_df = sell_sort.copy()
        profit_df.drop('index', axis=1, inplace=True)
        profit_df['Profit/Loss'] = np.nan  # Initialized to np.nan

        profit = []
        for i in range(len(sell_sort)):
            pr = 0
            for j in range(len(buy_sort)):
                if (sell_sort.loc[i, 'Scrape_Sym'] == buy_sort.loc[j, 'Scrape_Sym']) & (sell_sort.loc[i, 'Transaction_Date'] > buy_sort.loc[j, 'Transaction_Date']):
                    pr += (sell_sort.loc[i, 'Sell_Price'] * sell_sort.loc[i, 'Quantity']  # profit split and added to calculate total amount
                           ) - (buy_sort.loc[j, 'Buy_Price'] * sell_sort.loc[i, 'Quantity'])
            profit.append(pr)

        profit_df['Profit/Loss'] = profit
        print('Profit / Loss Margin of the stocks sold--------------\n')
        print(profit_df)

# Transaction History for customer

        transaction_history = gp_cl.get_group(int(client_id)).sort_values(by='Transaction_Date')
        transaction_history = transaction_history.reset_index()
        transaction_history.drop('index', axis=1, inplace=True)
        print('Transaction History of the customer--------------\n')
        print(transaction_history)
        # display(df_current)

# Client Info

        client_info = client_df.loc[client_df['Client_ID'] == int(client_id)].transpose()
        client_info.columns = ['']

# Writing all the dataframes to seperate sheets in Excel file
# Report file name is kept variable on purpose

        with pd.ExcelWriter('Client_{}_Report.xlsx'.format(int(client_id)), engine='xlsxwriter') as writer:
            client_info.to_excel(writer, sheet_name='Customer Info', index=True)
            rep_df.to_excel(writer, sheet_name='Current Stock Info', index=False)
            profit_df.to_excel(writer, sheet_name='Profit-Loss margin', index=False)
            transaction_history.to_excel(writer, sheet_name='Transaction History', index=False)

# If email functionality is required comment out the following Logic

        # subject = "Weekly Report"
        #
        # content = """ Report for this week """
        #
        # # print("Current Price of {0} is higher than Stock Price. Contact the client {1}".format(
        # #     rep_df.loc[i, 'Symbol'], client_id))
        # email = client_df.loc[(client_df['Client_ID'] ==
        #                        int(client_id)), 'Email'].astype('str')
        # #email = 'noclues008@gmail.com'
        #
        # path = 'Client_{}_Report.xlsx'.format(int(client_id))
        #
        # mailing.send_mail(email, subject, content, path)


# Note : This Program should be run via command line. If run from editor then adjust the arguments of the function call

get_rep(*sys.argv[1:])

# If required to create the reports of all the clients

# For all the clients -->

# Client_List = list(client_df['Client_ID'].values)
# for i in Client_List:
#     get_rep(i)
