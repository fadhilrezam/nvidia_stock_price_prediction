# from utils.logger import logging
# from utils.exception import CustomException
import sys

import streamlit as st
import datetime
from dateutil.relativedelta import relativedelta
import requests
import urllib.parse
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")


st.markdown("<h1 style='text-align: center;'>NVIDIA Stock Close Price Prediction</h1>", unsafe_allow_html=True)

try:
    st.markdown("<h3 style='text-align: left;'>Select Date Range</h3>", unsafe_allow_html=True)
    min_value_start = datetime.date(2024,10,5)
    min_value_end = min_value_start + relativedelta(days = 1)
    start_date = st.date_input('Start Date', value = datetime.date(2024,10,5), min_value = min_value_start)
    end_date = st.date_input('End Date', value = datetime.date(2024,10,13), min_value = min_value_end)

    if st.button("Submit"):
        # Prepare data for the prediction request
        data = {
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d')
        }

        # main_url = "http://127.0.0.1:5000/?"
        main_url = "https://mutual-jolyn-fadhilrezam-e8b0b3af.koyeb.app/?"
        url = main_url + urllib.parse.urlencode(data)

        try:
            # Make the API request
            json_response = requests.get(url, json=data).json()
            if json_response:
                # Convert response to DataFrame and display it
                df = pd.DataFrame.from_dict(json_response, orient='index').rename(
                    columns={'close_pred_original_scale': 'Predicted Close Price'})
                st.dataframe(df)
                fig, ax = plt.subplots(figsize = (20,2), dpi = 500)
                
                ax.plot(df.index, df['Predicted Close Price'], marker='o') 
                ax.set_title(f'NVIDIA Predicted Close Price ({df.index.min()} to {df.index.max()})')
                ax.set_xlabel("Date")
                ax.set_ylabel("Predicted Close Price")
                st.markdown("<div style='display: flex; justify-content: center;'>", unsafe_allow_html=True)
                st.pyplot(fig, use_container_width= True)
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.write("No data available for the selected date range.")

        except Exception as e:
            st.error(f"Error: {e}")

except Exception as e:
    # logging.error(CustomException(e, sys))
    st.error(f"Error: {e}")




