from utils.logger import logging
from utils.exception import CustomException
import sys
import os

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import root_mean_squared_error
import mlflow
from mlflow.models.signature import infer_signature, ModelSignature
from mlflow.types.schema import Schema, ColSpec, TensorSpec

import warnings
warnings.filterwarnings("ignore")


def load_preprocessed_dataset():
    logging.info('Train, Test and Exog Dataframe Initialization')
    try:
        folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__),"..","data","processed"))
        if os.path.exists(folder_path):
            df_train = pd.read_csv(os.path.join(folder_path, 'df_train.csv'), index_col=0)
            df_train.index = pd.to_datetime(df_train.index)
            df_test = pd.read_csv(os.path.join(folder_path, 'df_test.csv'), index_col=0)
            df_test.index = pd.to_datetime(df_test.index)
            exog_train = pd.read_csv(os.path.join(folder_path, 'exog_train.csv'), index_col=0)
            exog_train.index = pd.to_datetime(exog_train.index)
            exog_test =pd.read_csv(os.path.join(folder_path, 'exog_test.csv'), index_col=0)
            exog_test.index = pd.to_datetime(exog_test.index)
            logging.info('Train, Test and Exog Dataframe Loaded Successfully')
            print(df_train.shape, df_test.shape, exog_train.shape, exog_test.shape)
        return df_train, df_test, exog_train, exog_test
    except Exception as e:
        logging.error(CustomException(e,sys))
        raise CustomException(e,sys)

def train_model(df_train, df_test, exog_train, exog_test):
    logging.info('Training Model Initialization')
    mlflow.statsmodels.autolog()
    try:
        mlflow.set_experiment("MLflow Stock Forecast with ARIMA")

        # Start an MLflow run
        with mlflow.start_run():
            logging.info("Start Training Model")
            try:
                order = (1,0,1)
                model_arima = ARIMA(df_train['close_log_diff'], order = order, exog = exog_train).fit() 
                y_pred_arima = model_arima.get_forecast(steps = len(df_test), exog = exog_test).predicted_mean.values

                df_pred_arima = pd.DataFrame({
                    'close_pred': y_pred_arima}, index = df_test.index)

                close_pred_original = np.exp(df_pred_arima['close_pred'].cumsum() + df_train['close_log'].iloc[-1])
                df_pred_arima['close_pred_original_scale']= close_pred_original
                rmse_arima = root_mean_squared_error(df_test['close_log_diff'], df_pred_arima['close_pred'])
                rmse_arima_original_scale = root_mean_squared_error(df_test['close'], df_pred_arima['close_pred_original_scale'])
                
                # Log ARIMA order and loss metric
                mlflow.log_param("ARIMA_order", order)
                mlflow.log_metric("RMSE Score Scaled", rmse_arima)
                mlflow.log_metric("RMSE Score Original Scale", rmse_arima_original_scale)

                # Log Model with it's signature
                input_example = pd.concat([df_train[['close_log_diff']],exog_train], axis = 1).iloc[[0]]
                output_example = pd.DataFrame({'predicted_mean': [y_pred_arima[0]]})
                signature = infer_signature(input_example, output_example)
                mlflow.statsmodels.log_model(model_arima, artifact_path="model_arima", signature=signature, input_example = input_example)
                logging.info('Model and Parameters Successufuly Stored in MLflow')

            except Exception as e:
                logging.info(CustomException(e,sys))
        
            try:
                #Plotting
                logging.info('Line Plot Comparison : Train vs Test vs Prediction Close Price')
                plt.figure(figsize=(18, 6))
                plt.title('ARIMA Model: Comparison of Training, Testing, and Predicted Close Price')
                sns.lineplot(x=df_train.index, y=df_train['close'], label='Training Data (Close Price)')
                sns.lineplot(x=df_test.index, y=df_test['close'], label='Test Data (Close Price)')
                sns.lineplot(x=df_pred_arima.index, y=df_pred_arima['close_pred_original_scale'], label='Predicted Close Price')
                plt.legend()

                folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__),"..","data","visualizations"))
                image_name = 'arima_model_comparison.png'
                if os.path.exists(folder_path):
                    image_path = os.path.join(folder_path,image_name)
                    plt.savefig(image_path) #Store lineplot to local folder
                    mlflow.log_artifact(image_path) #Store lineplot to mlflow directory
                    logging.info('Plot Successfully Saved to Local and MLflow Experiments')
                else:
                    logging.info(f'Creating {folder_path}')
                    os.makedirs(folder_path)
                    image_path = os.path.join(folder_path,image_name)
                    plt.savefig(image_path) #Store lineplot to local folder
                    mlflow.log_artifact(image_path) #Store lineplot to mlflow directory
                    mlflow.log_figure()
                    logging.info('Plot Successfully Saved to Local and MLflow Experiments')
            except Exception as e:
                logging.info(CustomException(e,sys))
        
            # Set a tag that we can use to remind ourselves what this run was for
            mlflow.set_tag("Training Info", "ARIMA Model For NVIDIA stock price")
            logging.info("Training pipeline completed successfully")

        return model_arima, rmse_arima, rmse_arima_original_scale
            
    except Exception as e:
        logging.error(CustomException(e,sys))
  

def save_model(model_arima):
    try:
        logging.info('ARIMA Model Saving Initialization ')
        folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__),"..","data","models"))
        model_name = 'arima_model.pkl'
        if os.path.exists(folder_path):
            model_path = os.path.join(folder_path,model_name)
            model_arima.save(model_path)
            logging.info(f"Saved ARIMA Model to {model_path}")
        else:
            logging.error('Model Folder Path Not Found')
    except Exception as e:
        logging.error(CustomException(e,sys))


if __name__ == '__main__':
    df_train, df_test, exog_train, exog_test = load_preprocessed_dataset()
    model_arima, rmse_arima, rmse_arima_original_scale = train_model(df_train, df_test, exog_train, exog_test)
    print('RMSE Original Scale: ', rmse_arima_original_scale)
    save_model(model_arima)

 
    