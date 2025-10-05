import streamlit as st
import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from sqlalchemy import text

sys.path.append(os.path.abspath("D:/D26_Files/Phonepe_Analytics/Pulse_Case_Studies/"))

from db_connection import get_phonepe_engine

engine = get_phonepe_engine()


st.set_page_config(page_title="Transaction Dynamics", layout="wide")


st.title("Transaction Dynamics on PhonePe Analysis")

st.header("PhonePe Transaction Growth Over Time")

from data_queries import get_transaction_growth
transaction_growth_df = get_transaction_growth(engine)

yearly_df = transaction_growth_df.groupby('Year').agg({
    'Total_value': 'sum',
    'Total_volume': 'sum'
}).reset_index()

fig_value = px.line(yearly_df, x='Year', y='Total_value', 
                    title='Total Transaction Value Growth (₹)', 
                    labels={'Total_value': 'Total Transaction Value'},
                    line_shape='linear')
fig_value.update_traces(line=dict(color='blue'))

fig_volume = px.line(yearly_df, x='Year', y='Total_volume', 
                     title='Total Transaction Volume Growth',
                     labels={'Total_volume': 'Total Transaction Volume'},
                     line_shape='linear')
fig_volume.update_traces(line=dict(color='green'))

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig_value, use_container_width=True)
with col2:
    st.plotly_chart(fig_volume, use_container_width=True)
    
 
st.header("Payment Category Growth Over Time")
    
from data_queries import get_payment_category_growth
payment_category_growth_df = get_payment_category_growth(engine)

fig_vol = px.bar(payment_category_growth_df,
                 x="Year",
                 y="Total_Volume",
                 color="Transaction_type",
                 color_discrete_sequence=px.colors.qualitative.Pastel1,
                 title="Transaction Volume by Category Over Years",
                 labels={"Total_Volume": "Total Transaction Volume"},
                 barmode='stack')

fig_val = px.bar(payment_category_growth_df,
                 x="Year",
                 y="Total_Value",
                 color="Transaction_type",
                 color_discrete_sequence=px.colors.qualitative.Pastel1,
                 title="Transaction Value by Category Over Years",
                 labels={"Total_Value": "Total Transaction Value (₹)"},
                 barmode='stack')

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig_val, use_container_width=True)
with col2:
    st.plotly_chart(fig_vol, use_container_width=True)
    
    
st.header("Seasonal Trends and Festive Spikes in Transaction Activity")  

from data_queries import get_seasonal_transaction_spikes
seasonal_spikes_df = get_seasonal_transaction_spikes(engine)

fig_heatmap = px.density_heatmap(seasonal_spikes_df, 
                                 x='Quarter', 
                                 y='Year', 
                                 z='Total_volume',
                                 histfunc='sum',
                                 text_auto=True,
                                 title='Heatmap: Total Transaction Volume by Quarter and Year',
                                 color_continuous_scale='Inferno',
                                 labels={'Total_volume': 'Transaction Volume'})

st.plotly_chart(fig_heatmap, use_container_width=True)


st.header("Top 10 States Driving Transaction Growth")

from data_queries import get_top_contributing_states
top_state_df = get_top_contributing_states(engine) 

fig_Value = px.bar(
    top_state_df,
    x="Total_value",
    y="State",
    orientation='h',
    title="Top 10 States by Total Transaction Value",
    labels={"Total_value": "Total Transaction Value (₹)"},
    color="Total_value",
    color_continuous_scale="Greens")

fig_Volume = px.bar(
    top_state_df,
    x="Total_value",
    y="State",
    orientation='h',
    title="Top 10 States by Total Transaction Volume",
    labels={"Total_volume": "Total Transaction Volume"},
    color="Total_volume",
    color_continuous_scale="Blues")

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig_Value, use_container_width=True)
with col2:
    st.plotly_chart(fig_Volume, use_container_width=True)


st.header("States with Declining or Stagnant Transaction Trends")  

from data_queries import get_state_transaction_trends
state_trends_df = get_state_transaction_trends(engine)

fig = px.bar(
    state_trends_df,
    x="Total_Volume",
    y="State",
    orientation='h',
    title="States with Lowest Total Transaction Volume",
    labels={"Total_Volume": "Total Transaction Volume", "State": "State"},
    color="Total_Volume",
    color_continuous_scale="Reds")

st.plotly_chart(fig, use_container_width=True)



   
    
    