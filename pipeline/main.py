from utils.logger import logging
from utils.exception import CustomException
import sys

from .data_ingestion import get_stock_data
from .data_preprocess import load_dataset, preprocess_dataset, store_dataframe
from .train_model import train_model, save_model

from datetime import datetime
from dateutil.relativedelta import relativedelta

def run_pipeline(ticker_code, start_date, end_date):
    try:
        get_stock_data(ticker_code, start_date,end_date)
        '''
        -> args (default):
            1. ticker_code = 'NVDA'
            2. start_date = 2019-10-05
            3.end_date = start_date + 5 years ahead (2024-10-05)
        -> return: None
        '''
    except Exception as e:
        logging.error(CustomException(e,sys))

    try:
        df  = load_dataset()
        '''
        -> args: None
        -> return: df (dataframe)
        '''
    except Exception as e:
        logging.error(CustomException(e,sys))

    try:
        df_cleaned, df_train, df_test, exog_train, exog_test = preprocess_dataset(df)
        
        '''
        -> args: df
        -> return: df_train, df_test, exog_train, exog_test
        '''
    except Exception as e:
        logging.error(CustomException(e,sys))

    try:
        store_dataframe(df_cleaned, df_train, df_test, exog_train, exog_test)
        '''
        -> args: df_cleaned, df_train, df_test, exog_train, exog_test
        -> return: None'''
    except Exception as e:
        logging.error(CustomException(e,sys))    
    try:
        model_arima = train_model(df_train, df_test, exog_train, exog_test)
        '''
        -> args: df_train, df_test, exog_train, exog_test
        -> return: model_arima
        '''
    except Exception as e:
        logging.error(CustomException(e,sys))

    try:
        save_model(model_arima)
        '''
        -> args: model_arima
        -> return: None
        '''
    except Exception as e:
        logging.error(CustomException(e,sys))

if __name__ == '__main__':
    try:
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
        run_pipeline(ticker_code, start_date, end_date)
    except Exception as e:
        logging.error(CustomException(e,sys))
    





