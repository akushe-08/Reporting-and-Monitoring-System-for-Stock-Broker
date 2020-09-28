import pandas as pd
import numpy as np
from requests import get
from bs4 import BeautifulSoup
pd.set_option('display.max_columns', None)

# df_current is assigned as none initially. In get_price, we store the scraped data in dataframe df_current.

df_current = None


def get_price(stock_sym):

    # variable url allows to scrape even when stock symbol changes
    url = f'https://in.finance.yahoo.com/quote/{stock_sym}?p={stock_sym}&.tsrc=fin-srch'
    response = get(url)

    html_soup = BeautifulSoup(response.text, 'html.parser')

    table_container = html_soup.find_all(
        'td', class_='Ta(end) Fw(600) Lh(14px)')  # values mentioned in names
    close = html_soup.find('span', class_='Mb(-4px)')  # current price of stock
    # checks if stock is closed or not
    close_state = html_soup.find('div', id='quote-market-notice')

    if 'close' in close_state.text:  # close_val stores the close price of stock when stock closes
        close_val = close.text  # when stock is not closed close_val stores 0

    else:
        close_val = '0'  # when stock is not closed

    current_val = close.text

# list for values to be scraped
    names = ['Previous close', 'Open', 'Bid', 'Ask',
             'Day\'s range', '52-week range', 'Volume', 'Avg. volume']

    values = dict()  # dictionary to create df_current
    for i in range(len(names)):
        values[names[i]] = table_container[i].text
# splitting the High low range and 52 week range in seperate prices
    low = values["Day's range"].split("-")[0]
    high = values["Day's range"].split("-")[1]

    week_52_low = values["52-week range"].split("-")[0]
    week_52_high = values["52-week range"].split("-")[1]

# names contained ranges which changed to seperate prices in names_updated
    names_updated = ['Stock_symbol', 'Current price', 'Previous close', 'Open',
                     'Close', 'Low', 'High', '52 Week Low', '52 Week High', 'Volume', 'Avg. volume']

    values_updated = [stock_sym, current_val, values[names[0]], values[names[1]],
                      close_val, low, high, week_52_low, week_52_high, values[names[6]], values[names[7]]]

# create df_current if doesn't exists otherwise append to it
    global df_current
    if df_current is None:
        df_current = pd.DataFrame(columns=names_updated)
        df_current.loc[len(df_current)] = values_updated
    else:
        df_current.loc[len(df_current)] = values_updated
    # print(values)


# get_price('INFY.NS')
