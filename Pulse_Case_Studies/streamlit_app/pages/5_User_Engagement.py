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


st.set_page_config(page_title="User Engagement", layout="wide")


st.title("User Engagement and Growth Strategy Analysis")

st.header("Top 10 States/Districts of Registered Users")

from data_queries import get_top_states_by_registered_users
top_states_df = get_top_states_by_registered_users(engine)

from data_queries import get_top_districts_by_registered_users
top_districts_df = get_top_districts_by_registered_users(engine)

from data_queries import indian_number_format

top_states_df = top_states_df.rename(columns={"Total_Users": "Total Users"})
top_states_df['Total Users'] = top_states_df['Total Users'].apply(indian_number_format)

top_districts_df = top_districts_df.rename(columns={"Total_Users": "Total Users"})
top_districts_df['Total Users'] = top_districts_df['Total Users'].apply(indian_number_format)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Top 10 States by Registered Users")
    st.dataframe(top_states_df, hide_index=True)
    
with col2:
    st.subheader("Top 10 Districts by Registered Users")
    st.dataframe(top_districts_df, hide_index=True)
    
    
st.header("User Engagement Ratio: Top 10 States & Districts")

from data_queries import get_state_engagement_ratio
top_states_engagement_df = get_state_engagement_ratio(engine)

from data_queries import get_district_engagement_ratio
top_districts_engagement_df = get_district_engagement_ratio(engine)

fig_states = px.pie(
    top_states_engagement_df,
    names='State',
    values='Engagement_Ratio_Percent',
    hole=0.5,
    title="User Engagement Ratio (Top 10 States)")

fig_districts = px.pie(
    top_districts_engagement_df,
    names='District',
    values='Engagement_Ratio_Percent',
    hole=0.5,
    title="User Engagement Ratio (Top 10 Districts)")

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig_states, use_container_width=True)
with col2:
    st.plotly_chart(fig_districts, use_container_width=True)
    
    
st.header("Top 10 Dormant Regions: High Registration, Low Engagement")

from data_queries import get_dormant_user_regions
dormant_regions_df = get_dormant_user_regions(engine)

fig_scatter = px.scatter(
    dormant_regions_df,
    x="Total_Registered",
    y="Engagement_Ratio_Percent",
    text="State",  
    size_max= 5,  
    color="State",  
    labels={
        "Total_Registered": "Total Registered Users",
        "Engagement_Ratio_Percent": "Engagement Ratio (%)"},
    title="Scatter Plot: High Registration vs. Low Engagement",
    hover_data=["Total_Registered", "Engagement_Ratio_Percent"])

fig_scatter.update_traces(textposition='top center')
fig_scatter.update_layout(width=1080, height=720)

st.plotly_chart(fig_scatter, use_container_width=True)


st.header("Growth of User Engagement Across States Over Time")

from data_queries import get_growth_states_by_engagement
yearly_growth_df = get_growth_states_by_engagement(engine)

fig_heatmap = px.density_heatmap(yearly_growth_df, 
                                 x='Year', 
                                 y='State', 
                                 z='Yearly_Engagement_Percent',
                                 histfunc='sum',
                                 text_auto=True,
                                 title='Heatmap: Yearly User Engagement Percentage by State',
                                 color_continuous_scale='Inferno',
                                 labels={"Year": "Year",
                                         "Yearly_Engagement_Percent": "Engagement Rate (%)",
                                         "State": "State"})
fig_heatmap.update_layout(width=2180, height=1080)

st.plotly_chart(fig_heatmap, use_container_width=True)


st.header("Target Districts to Boost User Stickiness")

from data_queries import get_target_districts_low_engagement
target_districts_df = get_target_districts_low_engagement(engine)

fig_bar = px.bar(
    target_districts_df,
    x="Engagement_Ratio_Percent",
    y="District",
    color="Engagement_Ratio_Percent",
    orientation="h",
    labels={"Engagement_Ratio_Percent": "Engagement Ratio (%)", "District": "District"},
    color_continuous_scale="YlOrRd",
    text="State" )
fig_bar.update_layout(width=1080, height=720)

st.plotly_chart(fig_bar, use_container_width=True)