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


st.set_page_config(page_title="PhonePe Analytics Dashboard", layout="wide")


st.markdown("""
    <style>
    .hover-box {
        background-color: #262730;
        border-radius: 10px;
        box-shadow: 0 1px 5px 0 #dde0e6;
        padding: 16px;
        margin-bottom: 12px;
        transition: box-shadow 0.2s, background 0.2s;
    }
    .hover-box:hover {
        box-shadow: 0 6px 24px 0 #262730;
        background-color: #262730;
    }
    </style>
""", unsafe_allow_html=True)

st.sidebar.image("D:\D26_Files\Phonepe_Analytics\Pulse_Case_Studies\PhonePe-Logo.wine.png", width=500)

Home_title = """
<p style='font-family:Roboto, Segoe UI, Arial, sans-serif; color:#6739B7; font-size:50px; font-weight:bold'>
Phonepe Pulse Analytics
</p>
"""
st.markdown(Home_title, unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
<p style='font-family:Roboto, Segoe UI, Arial, sans-serif; color:#6739B7; font-size:30px; font-weight:bold'>
Unlock Insights, Ignite Success!
</p>
""", unsafe_allow_html=True)
    
with col2:
    st.markdown(
    """
    <div class='hover-box'>
        <b> Welcome to Phonepe Pulse Analytics! Dive into data-driven insights and trends shaping the future of digital payments.Explore real-time analytics and actionable reports tailored for your needs.
            Stay ahead with our comprehensive tools and visualizations.
             Join us to transform data into powerful decision-making opportunities! </b><br>
        <pre>
    </div>
    """,
    unsafe_allow_html=True)
    
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
    title="PhonePe Transaction Value by State")

fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(width=1080, height=720)

st.plotly_chart(fig, use_container_width=True)





