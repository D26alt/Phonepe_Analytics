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


st.set_page_config(page_title="Device Dominance", layout="wide")


st.title("Device Dominance and User Engagement Analysis")

st.header("Device Brand Dominance Among PhonePe Users")

from data_queries import get_device_brand_dominance
device_brand_df = get_device_brand_dominance(engine)

threshold = 0.02 * device_brand_df["Total_users"].sum()
major_brands = device_brand_df[device_brand_df["Total_users"] >= threshold]
minor_brands = device_brand_df[device_brand_df["Total_users"] < threshold]

others_sum = minor_brands["Total_users"].sum()
others_row = pd.DataFrame({"Brand": ["Others"], "Total_users": [others_sum]})

brand_df = pd.concat([major_brands, others_row], ignore_index=True)

fig1 = px.pie(
    brand_df,
    names="Brand",
    values="Total_users",
    title="Registered Users by Device Brand",
    hole=0.5 )

fig1.update_layout(width=500, height=500)

st.plotly_chart(fig1, use_container_width=True)


st.header("Top 10 Districts by User Engagement")

from data_queries import get_top_district_user_engagement
district_engagement_df = get_top_district_user_engagement(engine)

district_engagement_df = district_engagement_df.rename(columns={"Total_users": "Total users"})
district_engagement_df = district_engagement_df.rename(columns={"Total_opens": "Total opens"})
district_engagement_df = district_engagement_df.rename(columns={"Engagement_score": "Engagement score"})

st.dataframe(district_engagement_df, hide_index=True)

district_engagement_df = district_engagement_df.sort_values("Engagement score", ascending=True)

fig2 = px.bar(
    district_engagement_df,
    x="Engagement score",
    y="District",
    color="Engagement score",
    orientation="h",
    labels={"Engagement score": "Engagement Score (App Opens Per User)", "District": "District"},
    color_continuous_scale="YlOrRd",
    text="State" )

st.plotly_chart(fig2, use_container_width=True)


st.header("Regional Preferences: Premium vs Budget Brands")

from data_queries import get_region_brand_preference
region_brand_df = get_region_brand_preference(engine)

fig_grouped = px.bar(
    region_brand_df,
    x="Total_users",
    y="State",
    color="Brand_category",  
    orientation="h",
    barmode="group",         
    labels={"Total_users": "User Count", "State": "State", "Brand_category": "Brand Category"},
    title="Premium vs Budget Brand Preferences by State")

fig_grouped.update_layout(width=2560, height=1440)

st.plotly_chart(fig_grouped, use_container_width=True)


st.header("Underperforming Brands: High Users, Low Market Penetration")

from data_queries import get_underperforming_brands
underperforming_brands_df = get_underperforming_brands(engine)

fig_scatter = px.scatter(
    underperforming_brands_df,
    x="Total_brand_users",
    y="Avg_market_share",
    size="States_present",
    color="Brand",
    hover_name="Brand",
    labels={
        "Total_brand_users": "Total Users",
        "Avg_market_share": "Average Market Share (%)",
        "States_present": "States Present"},
    title="Brand User Counts vs Market Penetration",
    size_max=5)

fig_scatter.update_layout(width=1080, height=720)

st.plotly_chart(fig_scatter, use_container_width=True)


st.header("User Engagement: Metro vs Non-Metro Districts")

from data_queries import get_engagement_metro_vs_nonmetro
engagement_metro_nonmetro_df = get_engagement_metro_vs_nonmetro(engine)

metro_df = engagement_metro_nonmetro_df[engagement_metro_nonmetro_df["Area_type"] == "Metro"]
nonmetro_df = engagement_metro_nonmetro_df[engagement_metro_nonmetro_df["Area_type"] == "Non-Metro"]


fig_metro = px.box(
    metro_df,
    y="Engagement_score",
    points="outliers",  
    labels={"Engagement_score": "User Engagement Score"},
    title="Metro Districts")
    
fig_metro.update_layout(width=1000, height=700)   
    


fig_nonmetro = px.box(
    nonmetro_df,
    y="Engagement_score",
    points="outliers",  
    labels={"Engagement_score": "User Engagement Score"},
    title="Non-Metro Districts")
fig_nonmetro.update_layout(width=1000, height=700)
    

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig_metro, use_container_width=False)

with col2:
    st.plotly_chart(fig_nonmetro, use_container_width=False)