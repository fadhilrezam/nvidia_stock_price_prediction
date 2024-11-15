from utils.logger import logging
from utils.exception import CustomException
import sys
import os
import joblib

from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from datetime import datetime

import warnings
warnings.filterwarnings("ignore")

app = Flask(__name__)
CORS(app)

def load_model_and_exog():
    model_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'models', 'arima_model.pkl'))
    df_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'data','df_cleaned.csv'))

    # Debug logs
    logging.info(f"Model path: {model_path}")
    logging.info(f"Dataframe path: {df_path}")
    # print(model_path)
    print(f"Model path exists: {os.path.exists(model_path)}")
    print(f"Dataframe path exists: {os.path.exists(df_path)}")
  

    try:
        logging.info('Load Model and Base Future Exogenous Variables')
        if os.path.exists(model_path) and os.path.exists(df_path):
            model_arima = joblib.load(model_path)
            df = pd.read_csv(df_path, index_col = 0)
            logging.info('Model and Dataframe Successfully Loaded')
            return model_arima, df
        else:
            logging.error('Model Path or Dataframe Path not found')
    except Exception as e:
        logging.error(CustomException(e,sys))
        raise CustomException(e, sys)


def predict_future(start_date, end_date, model_arima, df):
    try:
        logging.info('Prepare exogenous dataframe for future predictions')
        # #Prepare exog dataframe based on date range
        all_dates = pd.date_range(start = start_date, end = end_date, freq = 'B')
        features = df.drop(['close','close_log','close_log_diff'], axis = 1).columns.tolist()
        exog_future = df[features].tail(len(all_dates))
        exog_future.index = all_dates
        exog_future['year'] = all_dates.year
        exog_future['month'] = all_dates.month
        exog_future['day'] = all_dates.day

        logging.info('Prediction Initialization')
        y_pred = model_arima.get_forecast(steps = len(all_dates), exog = exog_future).predicted_mean.values

        df_pred = pd.DataFrame({
            'close_pred': y_pred}, index = all_dates)

        df_pred['close_pred_original_scale'] = np.exp(df_pred['close_pred'].cumsum() + df['close_log'].iloc[-1])
        logging.info('Prediction Completed')

        return df_pred[['close_pred_original_scale']]
    
    except Exception as e:
        logging.error(CustomException(e,sys))
        raise CustomException(e,sys)

@app.route('/health', methods=['GET'])
def health_check():
    return 'OK', 200

@app.route('/', methods = ['GET'])
def prediction():
    try:
        model_arima, df_exog = load_model_and_exog()
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        if not start_date_str:
            start_date_str = '2024-10-05'
        if not end_date_str:
            end_date_str = '2024-10-13'

        #Validate condition
        #1. start_date_str must be greater than 2024-10-04 
        #2. end_date_str must be greater than start_date_str

        if start_date_str <= '2024-10-04':
            return jsonify({'error': 'Start Date must be greater than 2024-10-04'})
        if end_date_str <= start_date_str:
            return jsonify({'error': 'End Date must be greater than Start Date'})
        
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

        df_pred = predict_future(start_date,end_date, model_arima, df_exog)
        df_pred = df_pred[['close_pred_original_scale']]
        df_pred.index = df_pred.index.astype('str')

        print(df_pred)

        return jsonify(df_pred.to_dict(orient='index'))

    except Exception as e:
        return jsonify({'error': str(e)}), 500 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)


