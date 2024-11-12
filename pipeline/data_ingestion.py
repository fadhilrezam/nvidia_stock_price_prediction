from utils.logger import logging
from utils.exception import CustomException
import sys
import yfinance as yf
from datetime import datetime
from dateutil.relativedelta import relativedelta
import os


#Function get_stock_data to store in csv format in local folder
def get_stock_data(ticker_code, start_date, end_date):
    try:
        folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__),"..",'data','raw'))
        if os.path.exists(folder_path):
            df = yf.download(ticker_code, start = start_date, end = end_date)
            file_name = f'{ticker_code.lower().replace("^","")}_stock_prices.csv'
            file_path = os.path.join(folder_path, file_name)
            df.to_csv(file_path)
            logging.info(f'{ticker_code} stock data successfully saved in {file_path}')
            logging.info('Data Ingestion Completed')
            return df.head()
    except Exception as e:
        logging.error(CustomException(e,sys))


if __name__ == '__main__':
    logging.info('Initializing Ticker Code and Date Range')
    ticker_code = input('Input the stock name (ex. TSLA, NVDA, ^GSPC, etc): ').strip().upper()
    start_date = input('Input start date (YYYY-MM-DD):')
    end_date = input('Input end date (YYYY-MM-DD):')
    if not ticker_code:
        ticker_code = 'NVDA'
    if not start_date:
        start_date = datetime(2019,10,5)
    if not end_date: 
        end_date = start_date + relativedelta(years = 5)
    df = get_stock_data(ticker_code, start_date, end_date)
