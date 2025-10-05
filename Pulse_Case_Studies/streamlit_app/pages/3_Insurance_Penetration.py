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


st.set_page_config(page_title="Insurance Penetration", layout="wide")


st.title("Insurance Penetration and Growth Potential Analysis")

st.header("State-wise Insurance Adoption Rate")

from data_queries import get_insurance_adoption_by_state
insurance_adoption_df = get_insurance_adoption_by_state(engine)

fig_bar = px.bar(
    insurance_adoption_df,
    x="Insurance_Adoption_Rate_Percentage",
    y="State",
    orientation="h",
    color="Insurance_Adoption_Rate_Percentage",
    color_continuous_scale="sunset",
    labels={
        "Insurance_Adoption_Rate_Percentage": "Insurance Adoption Rate (%)",
        "State": "State"},
    title="Insurance Adoption Rate by State")

fig_bar.update_layout(width=1000, height=800)

st.plotly_chart(fig_bar, use_container_width=False)


st.header("States Lagging in Insurance Penetration Despite High Users")

from data_queries import get_lagging_insurance_penetration_states
lagging_penetration_df = get_lagging_insurance_penetration_states(engine)

fig_group = px.bar(
    lagging_penetration_df,
    x="Insurance_Adoption_Rate_Percentage",
    y="State",
    orientation="h",
    color="Total_Registered_Users",
    color_continuous_scale="sunsetdark",  
    barmode="group",         
    labels={"Total_Registered_Users": "User Count", "State": "State", "Insurance_Adoption_Rate_Percentage": "Adoption Percentage"},
    title="States Lagging in Insurance Penetration")

fig_group.update_layout(width=1000, height=800)

st.plotly_chart(fig_group, use_container_width=True)


st.header("Quarterly Growth of Insurance Transactions")

from data_queries import get_insurance_quarterly_growth
insurance_quarterly_df = get_insurance_quarterly_growth(engine)

insurance_quarterly_df['Year-Quarter'] = insurance_quarterly_df['Year'].astype(str) + " Q" + insurance_quarterly_df['Quarter'].astype(str)

fig_value = px.area(
    insurance_quarterly_df,
    x='Year-Quarter',
    y= 'Transaction_Value',
    labels={'Transaction_Value': 'Total Transaction Value', 'Year-Quarter': "Quarter"},
    line_shape='spline',
    title='Quarterly Growth (Area): Value (₹)')
fig_value.update_traces(line=dict(color='green'))

fig_volume = px.area(
    insurance_quarterly_df,
    x='Year-Quarter',
    y='Transaction_Volume', 
    labels={'Total_volume': 'Total Transaction Volume', 'Year-Quarter': "Quarter"},
    line_shape='spline',
    title='Quarterly Growth (Area): Volume')
fig_volume.update_traces(line=dict(color='blue'))


col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig_value, use_container_width=True)
with col2:
    st.plotly_chart(fig_volume, use_container_width=True)
    

st.header("Insurance Adoption: Top vs Bottom 10 States")

from data_queries import get_top_10_insurance_adoption_states
top_10_df = get_top_10_insurance_adoption_states(engine)

from data_queries import get_bottom_10_insurance_adoption_states
bottom_10_df = get_bottom_10_insurance_adoption_states(engine)
    
fig_top_10_df = px.box(
    top_10_df,
    y="Insurance_Adoption_Rate_Percentage",
    points="outliers",  
    labels={"Insurance_Adoption_Rate_Percentage": "Adoption Rate Percentage"},
    color_discrete_sequence=["green"],
    title="Top 10 States")
    
fig_top_10_df.update_layout(width=500, height=700)   
    
fig_bottom_10_df = px.box(
    bottom_10_df,
    y="Insurance_Adoption_Rate_Percentage",
    points="outliers",  
    labels={"Insurance_Adoption_Rate_Percentage": "Adoption Rate Percentage"},
    color_discrete_sequence=["red"],
    title="Bottom 10 States")
fig_bottom_10_df.update_layout(width=500, height=700)
    

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig_top_10_df, use_container_width=False)

with col2:
    st.plotly_chart(fig_bottom_10_df, use_container_width=False)
    
    
st.header("Untapped Insurance Opportunity by State")

from data_queries import get_insurance_untapped_opportunities
untapped_df = get_insurance_untapped_opportunities(engine)

fig = px.scatter(
    untapped_df,
    x='Untapped_Users',
    y='Insurance_Adoption_Rate_Percentage',
    size='Total_Registered_Users',
    color='App_Engagement',
    hover_name='State',
    labels={
        'Untapped_Users': 'Untapped Users',
        'Insurance_Adoption_Rate_Percentage': 'Insurance Adoption Rate (%)',
        'Total_Registered_Users': 'Registered Users',
        'App_Engagement': 'App Engagement'},
    title="Bubble Chart: Untapped Insurance Opportunity by State",
    size_max=60,
    text="State",
    color_continuous_scale=px.colors.sequential.YlOrBr_r
)

st.plotly_chart(fig, use_container_width=True)