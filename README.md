## Monitoring and Reporting System for Stock Broker

#### Assumed Data

The assumption made is that we have the Transaction History of all the clients in Table format stored in a database.
Also we have all Clients' Personal Information to be sent in the Report Format
Note : Email IDs and all the Personal Data considered for test run is not real.

MySQL Database : ethans1
Tables : Client_Info, Exe_Info, scrape_data

Client_Info : Personal information about all the clients and their Client IDs.
Exe_Info : Execution information (Transaction History Table)
scrape_data : Table created after running scraper.py at end of the day.

Connection : Connection with database is made via Python and SQLalchemy Libraries.


#### File Functionality Explained


trailconda.py : contains the function get_price('Symbol') which scrapes the data such as current price, open, high, low, close and 52 week range for NSE and BSE Stock Symbols from Yahoo Finance Website and stores it in the dataframe df_current.

Note : This project is made considering only NSE and BSE markets but the Project can be extended to global level if required.

scraper.py  : In Scraper.py, trialconda.get_price() is used to scrape all the data of all the unique symbols in Transaction list. All the scraped data is stored in df_current.
cron schedule : 31 15 * * 1-5 python scraper.py    --- for daily eod scraped data to be stored in scrape_data Table in ethans1 database.

mailing.py : Functionality for sending email


monitoring.py : Monitoring of all the clients can be done by scheduling this program by any task scheduler.
cron schedule :  0,30 9-16 * * 1-5 python monitoring.py    ---for monitoring every half an hour in weekdays when stock market is open

get_report.py  : This program prints all the dataframes required for Project Report and creates an Excel File for the Report saved as "Client_{Client_ID}_Report.xlsx" in the current directory. Path can be modified.
Can be scheduled to get weekly reports
cron schedule : 31 15 * * 5 python get_report.py


#### Report Format

Sheet 1 : Client's Personal Information
Sheet 2 : Inormation about client's stocks such as whether they are active or not and their current data scraped from yahoo finance.
Sheet 3 : Profit Loss Margin (Only if client has any history of sold stocks) 
Sheet 4 : Transaction history of customer sorted by date
