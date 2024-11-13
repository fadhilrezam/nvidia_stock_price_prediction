# from utils.logger import logging
# from utils.exception import CustomException
# import sys

import streamlit as st
import datetime
from dateutil.relativedelta import relativedelta
import requests
import urllib.parse
import pandas as pd
import plotly.express as px

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
                df.index = pd.to_datetime(df.index)
                df.index = df.index.strftime('%d %B, %Y')
                col1, col2 = st.columns([0.2, 0.8])
                with col1:
                    st.dataframe(df)
                with col2:
                    min_date = df.index.min()
                    max_date = df.index.max()
                    fig = px.line(df, x = df.index, y = df['Predicted Close Price'], markers = True)
                    fig.update_layout(
                        xaxis_title="Date",
                        title_text=f'Predicted Close Price ({min_date} to {max_date})', title_font=dict(color="green", size = 20))
                    fig.update_traces(hovertemplate=None)
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.write("No data available for the selected date range.")

        except Exception as e:
            st.error(f'Error: {e}')

except Exception as e:
    # logging.error(CustomException(e, sys))
    st.error(f"Error: {e}")




