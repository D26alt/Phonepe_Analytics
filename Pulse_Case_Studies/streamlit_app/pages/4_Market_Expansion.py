import streamlit as st
import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import json
from sqlalchemy import text

sys.path.append(os.path.abspath("D:/D26_Files/Phonepe_Analytics/Pulse_Case_Studies/"))

from db_connection import get_phonepe_engine

engine = get_phonepe_engine()


st.set_page_config(page_title="Market Expansion", layout="wide")


st.title("Transaction Analysis for Market Expansion")

st.header("State-wise Contribution to PhonePe Transaction Volume and Value")

from data_queries import get_states_contribution
states_contribution_df = get_states_contribution(engine)

    
fig = px.choropleth(
    states_contribution_df,
    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
    featureidkey="properties.ST_NM",  
    locations="State",
    color="Total_Transaction_Value",
    color_continuous_scale="purp",
    hover_name="State",
    hover_data=["Total_Transaction_Volume", "Avg_Transaction_Value"],
    title="Choropleth Map: State-wise Transaction Value")

fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(width=1080, height=720)

st.plotly_chart(fig, use_container_width=True)


st.header("Top 5 States Dominance in India's Transactions")

from data_queries import get_top5_states_dominance
Top5_dominance_df = get_top5_states_dominance(engine)


fig_value = px.pie(
    Top5_dominance_df,
    names='Category',
    values='Percentage_of_Total_Value',
    hole=0.5,
    title="Transaction Value Share")

fig_volume = px.pie(
    Top5_dominance_df,
    names='Category',
    values='Percentage_of_Total_Volume',
    hole=0.5,
    title="Transaction Volume Share")

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig_value, use_container_width=True)
with col2:
    st.plotly_chart(fig_volume, use_container_width=True)


st.header("Underperforming States Showing Strong Recent Growth: Future Opportunities")

from data_queries import get_underperforming_growth_states
underperforming_growth_states_df = get_underperforming_growth_states(engine)

underperforming_growth_states_df = underperforming_growth_states_df.rename(columns={"Recent_Year_Value": "Recent Year Value"})
underperforming_growth_states_df = underperforming_growth_states_df.rename(columns={"Previous_Year_Value": "Previous Year Value"})
underperforming_growth_states_df = underperforming_growth_states_df.rename(columns={"Total_Overall_Value": "Total Overall Value"})
underperforming_growth_states_df = underperforming_growth_states_df.rename(columns={"Growth_Rate": "Growth Rate"})

fig_scatter = px.scatter(
    underperforming_growth_states_df,
    x="Recent Year Value",
    y="Growth Rate",
    size_max= 5,  
    color="State",  
    labels={
        "Recent Year Value": "Recent Year Value",
        "Growth Rate": "Growth Rate (%)"},
    title="Scatter Plot: Recent Growth of Underperforming States",
    hover_data=["Recent Year Value", "Previous Year Value", "Growth Rate"])

fig_scatter.update_layout(width=1080, height=720)

st.plotly_chart(fig_scatter, use_container_width=True)


st.header("Saturated vs Emerging State Markets")

from data_queries import get_market_status
market_status_df = get_market_status(engine)

fig_bubble = px.scatter(
    market_status_df,
    x='Total_Value',
    y='Growth_Percentage',
    size='Avg_Transaction_Size',
    color='State',
    hover_name='State',
    labels={
        'Total_Value': 'Total Value',
        'Growth_Percentage': 'Growth Percentage (%)',
        'Avg_Transaction_Size': 'Avg Transaction Size'},
    title="Scatter Chart: Growth Opportunity vs. Market Saturation",
    size_max=5,
    color_continuous_scale=px.colors.sequential.YlOrBr_r)

fig_bubble.update_layout(width=1080, height=720)

st.plotly_chart(fig_bubble, use_container_width=True)


st.header("Top 10 States: High Transaction Value vs. Volume")

from data_queries import get_top_transaction_volume_states
top_transaction_volume_df = get_top_transaction_volume_states(engine)

from data_queries import get_top_transaction_value_states
top_transaction_value_df = get_top_transaction_value_states(engine)

from data_queries import indian_number_format

top_transaction_volume_df = top_transaction_volume_df.rename(columns={"Total_Transaction_Volume": "Total Transaction Volume"})
top_transaction_volume_df['Total Transaction Volume'] = top_transaction_volume_df['Total Transaction Volume'].apply(indian_number_format)

top_transaction_value_df = top_transaction_value_df.rename(columns={"Total_Transaction_Value": "Total Transaction Value"})
top_transaction_value_df['Total Transaction Value'] = top_transaction_value_df['Total Transaction Value'].apply(indian_number_format)

col1, col2 = st.columns(2)

with col1:
    st.subheader("High Transaction Volume States")
    st.dataframe(top_transaction_volume_df, hide_index=True)
    
with col2:
    st.subheader("High Transaction Value States")
    st.dataframe(top_transaction_value_df, hide_index=True)



    





