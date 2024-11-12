from utils.logger import logging
from utils.exception import CustomException
import sys
import os

import pandas as pd
import numpy as np



    
def load_dataset():
    logging.info('Dataframe initialization')
    try:
        folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__),"..","data","raw"))
        file_name = 'nvda_stock_prices.csv'
        file_path = os.path.join(folder_path,file_name)
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)[['Date','Close']]
            logging.info('Dataframe successfully loaded')
            return df
    except Exception as e:
        logging.error(CustomException(e,sys))

def preprocess_dataset(df):
    try:
        # Lower column name, replace whitespace and extract year, month and day from date column as new columns or features
        df.columns = df.columns.str.lower().str.replace(' ','_')
        df['date'] = pd.to_datetime(df['date'])
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
        df['day'] = df['date'].dt.day

        #Transform dataframe with transformation log and differencing to stabilze the data range and remove any trends
        df['close_log'] = np.log(df['close'])
        df['close_log_diff'] = df['close_log'].diff()
        df.dropna(inplace = True)

        for lag in range(1, 4):
            df[f'lag_{lag}'] = df['close_log_diff'].shift(lag)
            df.dropna(inplace = True)
        df['rolling_mean'] = df['close_log_diff'].rolling(window = 5).mean()
        df.dropna(inplace = True)

        # Split dataframe and to train test split with 80/20 distribution
        # Store other features as exogenous variables
        df.set_index('date', inplace = True)
        df.index = pd.to_datetime(df.index)
        # n_rows = int(len(df)*0.8)
        # df_train = df.iloc[:n_rows]
        # df_test = df.iloc[n_rows:]
        # exog_train = df_train[['lag_1', 'lag_2', 'lag_3', 'rolling_mean', 'year', 'month', 'day']]
        # exog_test = df_test[['lag_1', 'lag_2', 'lag_3', 'rolling_mean', 'year', 'month', 'day']]
        n_rows = int(len(df)*0.85)
        df_train = df.iloc[:n_rows]
        df_test = df.iloc[n_rows:]

        features = df.drop(['close','close_log','close_log_diff'], axis = 1).columns.tolist()
        exog_train = df_train[features]
        exog_test = df_test[features]
        return df, df_train, df_test, exog_train, exog_test
    
    except CustomException as e:
        logging.error(CustomException(e,sys))

def store_dataframe(df, df_train, df_test, exog_train, exog_test):
    logging.info('Preparing to store train,test and exogenous dataframe')
    try:
        folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__),"..","data","processed"))
        folder_path_backend = os.path.abspath(os.path.join(os.path.dirname(__file__),"..","backend","data"))
        if os.path.exists(folder_path):
            df.to_csv(os.path.join(folder_path, 'df_cleaned.csv'), index = True)
            df.to_csv(os.path.join(folder_path_backend, 'df_cleaned.csv'), index = True)
            df_train.to_csv(os.path.join(folder_path, 'df_train.csv'), index = True)
            df_test.to_csv(os.path.join(folder_path, 'df_test.csv'), index = True)
            exog_train.to_csv(os.path.join(folder_path, 'exog_train.csv'), index = True)
            exog_test.to_csv(os.path.join(folder_path, 'exog_test.csv'), index = True)
            logging.info(f'Preprocessed Dataframe Successfully stored in {folder_path} and {folder_path_backend} for df_cleaned')
    except Exception as e:
        logging.error(CustomException(e,sys))
    
if __name__ == '__main__':
    df = load_dataset()
    df_cleaned, df_train, df_test, exog_train, exog_test = preprocess_dataset(df)
    store_dataframe(df_cleaned, df_train, df_test, exog_train, exog_test)



