"""
data_queries.py

This module contains functions to fetch PhonePe transaction analytics from the database.
All functions expect an SQLAlchemy engine object for the database connection.
"""
import sys
import os
import pandas as pd
from sqlalchemy import text

sys.path.append(os.path.abspath("D:/D26_Files/Phonepe_Analytics/Pulse_Case_Studies/"))

from db_connection import get_phonepe_engine

engine = get_phonepe_engine()

#1. Decoding Transaction Dynamics on PhonePe


def get_transaction_growth(engine):
    """
    Fetch total transaction volume and value growth over time (Year, Quarter) across India.
    
    Returns:
    pandas.DataFrame with columns [Year, Quarter, Total_volume, Total_value]
    """
    query = """
        SELECT 
            Year,
            Quarter,
            SUM(Transaction_count) AS Total_volume,
            SUM(Transaction_amount) AS Total_value
        FROM agg_transaction
        GROUP BY Year, Quarter
        ORDER BY Year, Quarter;
    """
    return pd.read_sql(query, engine)


def get_payment_category_growth(engine):
    """
    Fetch the total transaction volume and value growth by payment categories (like recharge, bills, merchant payments, P2P, etc.) over the years.
    
    Returns:
    pandas.DataFrame containing columns:
        - Year
        - Transaction_type
        - Total_Volume (sum of transaction counts)
        - Total_Value (sum of transaction amounts)
    """
    query = """
    SELECT 
        Year,
        Transaction_type,
        SUM(Transaction_count) as Total_Volume, 
        SUM(Transaction_amount) as Total_Value 
    FROM agg_transaction 
    GROUP BY Transaction_type, Year 
    ORDER BY Transaction_type, Year;
    """
    return pd.read_sql(query, engine)


def get_seasonal_transaction_spikes(engine):
    """
    Fetch transaction volume and value aggregated by Year and Quarter
    to analyze seasonal spikes such as festive quarters.
    """
    query = """
        SELECT
            Year, 
            Quarter,
            SUM(Transaction_count) AS Total_volume,
            SUM(Transaction_amount) AS Total_value
        FROM agg_transaction
        GROUP BY Year, Quarter
        ORDER BY Quarter, Year;
    """
    return pd.read_sql(query, engine)


def get_top_contributing_states(engine):
    """
    Fetch top 10 states contributing the most to overall transaction value and volume.
    """
    query = """
        SELECT
            State,
            SUM(Transaction_count) AS Total_volume,
            SUM(Transaction_amount) AS Total_value
        FROM agg_transaction
        GROUP BY State
        ORDER BY Total_value DESC
        LIMIT 10;
    """
    return pd.read_sql(query, engine)


def get_state_transaction_trends(engine):
    """
    Fetch yearly transaction volume by state to analyze states showing decline or stagnation despite national growth.
    """
    query = """
        SELECT 
            State,
            SUM(Transaction_count) AS Total_Volume
        FROM agg_transaction
        GROUP BY State
        ORDER BY Total_Volume ASC
        LIMIT 10;
    """
    return pd.read_sql(query, engine)


#2. Device Dominance and User Engagement Analysis


def get_device_brand_dominance(engine):
    """
    Fetch total registered users by device brand at the national level.
    """
    query = """
        SELECT 
            Brand, 
            SUM(Brand_count) AS Total_users
        FROM agg_user
        WHERE Year = (SELECT MAX(Year) FROM agg_user)
        GROUP BY Brand
        ORDER BY Total_users DESC;
    """
    return pd.read_sql(query, engine)


def get_top_district_user_engagement(engine):
    """
    Fetch top 10 districts by user engagement score (app opens per registered user), including total users and app opens.
    """
    query = """
        SELECT 
            State,
            District,
            SUM(Registered_users) AS Total_users,
            SUM(App_opens) AS Total_opens,
            ROUND(SUM(App_opens) * 1.0 / SUM(Registered_users), 2) AS Engagement_score
        FROM map_user
        WHERE Registered_users > 0 AND Year = (SELECT MAX(Year) FROM map_user)
        GROUP BY State, District
        ORDER BY Engagement_score DESC
        LIMIT 10;
    """
    return pd.read_sql(query, engine)


def get_region_brand_preference(engine):
    """
    Fetch user counts by state for premium and budget brand categories (Apple, OnePlus vs Xiaomi, Vivo, Samsung).
    """
    query = """
        SELECT 
            State,
            Brand,
            SUM(Brand_count) AS Total_users,
            CASE 
                WHEN Brand IN ('Apple', 'OnePlus') THEN 'Premium'
                WHEN Brand IN ('Xiaomi', 'Vivo', 'Samsung') THEN 'Budget'
            END AS Brand_category     
        FROM agg_user 
        WHERE Brand IN ('Apple', 'OnePlus', 'Xiaomi', 'Vivo', 'Samsung') AND Year = (SELECT MAX(Year) FROM agg_user)
        GROUP BY State, Brand, Brand_category
        ORDER BY State, Total_users DESC;
    """
    return pd.read_sql(query, engine)


def get_underperforming_brands(engine):
    """
    Fetch brands with total users, average market share, and number of states present to identify underperforming brands.
    """
    query = """
        SELECT 
            Brand,
            SUM(Brand_count) AS Total_brand_users,
            AVG(Brand_percentage) AS Avg_market_share,
            COUNT(DISTINCT State) AS States_present
        FROM agg_user
        WHERE Year = (SELECT MAX(Year) FROM agg_user)
        GROUP BY Brand
        ORDER BY Avg_market_share DESC;
    """
    return pd.read_sql(query, engine)


def get_engagement_metro_vs_nonmetro(engine):
    """
    Fetch average registered users and engagement scores comparing major metropolitan and smaller districts.
    """
    query = """
        SELECT 
            State,
            District,
            ROUND(AVG(Registered_users), 0) AS Avg_users,
            ROUND(AVG(App_opens * 1.0 / Registered_users), 2) AS Engagement_score,
            CASE 
                WHEN District IN ('Ahmedabad District', 'Bengaluru Urban District', 'Chennai District', 'Hyderabad District', 'Kolkata District', 'Mumbai District', 'Mumbai Suburban District', 'Pune District', 'Thane District', 'Gautam Buddha Nagar District', 'Ghaziabad District', 'Gurugram District', 'Faridabad District', 'Kamrup Metropolitan District', 'New Delhi District', 'South East Delhi District', 'North East District', 'South West District', 'North West District', 'Sas Nagar District', 'Chandigarh District', 'Rangareddy District', 'Medchal Malkajgiri District', 'Sangareddy District', 'North Twenty Four Parganas District', 'South Twenty Four Parganas District', 'Howrah District', 'Hooghly District') 
                THEN 'Metro'
                ELSE 'Non-Metro'
            END AS Area_type
        FROM map_user
        WHERE Registered_users > 0 AND Year = (SELECT MAX(Year) FROM map_user)
        GROUP BY State, District, Area_type
        ORDER BY Engagement_score DESC;
    """
    return pd.read_sql(query, engine)


#3. Insurance Penetration and Growth Potential Analysis


def get_insurance_adoption_by_state(engine):
    """
    Retrieve states with their insurance transaction counts, total registered PhonePe users,
    and calculate insurance adoption rate percentage (insurance txns per 100 users).
    """
    query = """
    SELECT 
        i.State,
        SUM(i.Insurance_txn_count) AS Total_Insurance_Transactions,
        MAX(u.Registered_users) AS Total_Registered_Users,
        ROUND((SUM(i.Insurance_txn_count) * 100.0 / MAX(u.Registered_users)), 4) AS Insurance_Adoption_Rate_Percentage
    FROM insurance_transaction i
    JOIN agg_user u 
        ON i.State = u.State 
        AND i.Year = u.Year 
        AND i.Quarter = u.Quarter
    GROUP BY i.State
    HAVING MAX(u.Registered_users) > 0
    ORDER BY Insurance_Adoption_Rate_Percentage DESC;
    """
    return pd.read_sql(query, engine)


def get_lagging_insurance_penetration_states(engine):
    """
    Get states with high registered users (over 1 million) but low insurance adoption rate.
    """
    query = """
        SELECT 
            i.State,
            MAX(u.Registered_users) AS Total_Registered_Users,
            SUM(i.Insurance_txn_count) AS Total_Insurance_Transactions,
            ROUND((SUM(i.Insurance_txn_count) * 100.0 / MAX(u.Registered_users)), 4) AS Insurance_Adoption_Rate_Percentage
        FROM insurance_transaction i
        JOIN agg_user u 
            ON i.State = u.State 
            AND i.Year = u.Year 
            AND i.Quarter = u.Quarter
        GROUP BY i.State
        HAVING MAX(u.Registered_users) > 10000000
        ORDER BY Total_Registered_Users DESC, Insurance_Adoption_Rate_Percentage ASC;
    """
    return pd.read_sql(query, engine)


def get_insurance_quarterly_growth(engine):
    """
    Fetch total insurance transaction counts and transaction values aggregated quarterly by year.
    """
    query = """
    SELECT 
        Year,
        Quarter,
        SUM(Insurance_txn_count) as Transaction_Volume,
        SUM(Insurance_txn_amount) as Transaction_Value
    FROM insurance_transaction
    GROUP BY Year, Quarter
    ORDER BY Year, Quarter;
    """
    return pd.read_sql(query, engine)


def get_top_10_insurance_adoption_states(engine):
    """
    Fetch top 10 states with highest insurance adoption rate compared to PhonePe user base.
    """
    query = """
        SELECT 
            i.State,
            MAX(u.Registered_users) as Total_Registered_Users,
            SUM(i.Insurance_txn_count) as Total_Insurance_Transactions,
            ROUND((SUM(i.Insurance_txn_count) * 100.0 / MAX(u.Registered_users)), 2) as Insurance_Adoption_Rate_Percentage
        FROM insurance_transaction i
        JOIN agg_user u 
            ON i.State = u.State 
            AND i.Year = u.Year 
            AND i.Quarter = u.Quarter
        GROUP BY i.State
        ORDER BY Insurance_Adoption_Rate_Percentage DESC
        LIMIT 10;
    """
    return pd.read_sql(query, engine)

def get_bottom_10_insurance_adoption_states(engine):
    """
    Fetch bottom 10 states with lowest insurance adoption rate compared to PhonePe user base.
    """
    query = """
        SELECT 
            i.State,
            MAX(u.Registered_users) as Total_Registered_Users,
            SUM(i.Insurance_txn_count) as Total_Insurance_Transactions,
            ROUND((SUM(i.Insurance_txn_count) * 100.0 / MAX(u.Registered_users)), 2) as Insurance_Adoption_Rate_Percentage
        FROM insurance_transaction i
        JOIN agg_user u 
            ON i.State = u.State 
            AND i.Year = u.Year 
            AND i.Quarter = u.Quarter
        GROUP BY i.State
        ORDER BY Insurance_Adoption_Rate_Percentage ASC
        LIMIT 10;
    """
    return pd.read_sql(query, engine)


def get_insurance_untapped_opportunities(engine):
    """
    Fetch states with large user bases but low insurance adoption rates, highlighting untapped users and app engagement.
    """
    query = """
        SELECT 
            i.State,
            MAX(u.Registered_users) as Total_Registered_Users,
            SUM(u.App_opens) as App_Engagement,
            SUM(i.Insurance_txn_count) as Total_Insurance_Transactions,
            ROUND((SUM(i.Insurance_txn_count) * 100.0 / MAX(u.Registered_users)), 2) as Insurance_Adoption_Rate_Percentage,
            MAX(u.Registered_users) - SUM(i.Insurance_txn_count) as Untapped_Users
        FROM insurance_transaction i
        JOIN agg_user u 
            ON i.State = u.State 
            AND i.Year = u.Year 
            AND i.Quarter = u.Quarter
        GROUP BY i.State
        HAVING Total_Registered_Users > 1000000 AND Insurance_Adoption_Rate_Percentage < 10
        ORDER BY Untapped_Users DESC, App_Engagement DESC;
    """
    return pd.read_sql(query, engine)


#4. Transaction Analysis for Market Expansion


def get_states_contribution(engine):
    """
    Fetches state-level aggregated transaction statistics from the database.
    """
    query = """
        SELECT 
            State,
            SUM(Transaction_count) AS Total_Transaction_Volume,
            SUM(Transaction_amount) AS Total_Transaction_Value,
            ROUND(AVG(Transaction_amount/Transaction_count), 2) AS Avg_Transaction_Value
        FROM agg_transaction
        GROUP BY State
        ORDER BY Total_Transaction_Value DESC, Total_Transaction_Volume DESC;
    """
    return pd.read_sql(query, engine)


def get_top5_states_dominance(engine):
    """
    Returns aggregated transaction dominance of top 5 states vs rest of India.
    """
    query = """
    WITH state_totals AS (
        SELECT 
            State,
            SUM(Transaction_count) as Total_Volume,
            SUM(Transaction_amount) as Total_Value
        FROM agg_transaction 
        GROUP BY State
    ),
    ranked_states AS (
        SELECT 
            State,
            Total_Volume,
            Total_Value,
            ROW_NUMBER() OVER (ORDER BY Total_Value DESC) as state_rank
        FROM state_totals
    )
    SELECT 
        CASE 
            WHEN state_rank <= 5 THEN 'Top 5 States'
            ELSE 'Rest of India'
        END as Category,
        SUM(Total_Volume) as Total_Transaction_Volume,
        SUM(Total_Value) as Total_Transaction_Value,
        COUNT(*) as Number_of_States,
        ROUND(SUM(Total_Value) * 100.0 / (SELECT SUM(Total_Value) FROM state_totals), 2) as Percentage_of_Total_Value,
        ROUND(SUM(Total_Volume) * 100.0 / (SELECT SUM(Total_Volume) FROM state_totals), 2) as Percentage_of_Total_Volume
    FROM ranked_states
    GROUP BY 
        CASE 
            WHEN state_rank <= 5 THEN 'Top 5 States'
            ELSE 'Rest of India'
        END
    ORDER BY Total_Transaction_Value DESC;
    """
    return pd.read_sql(query, engine)


def get_underperforming_growth_states(engine):
    """
    Retrieves states with transaction amount growth rates comparing the most recent year 
    to the previous year, including total overall value.
    """
    query = """
    SELECT 
        State,
        SUM(CASE WHEN Year = (SELECT MAX(Year) FROM agg_transaction) 
            THEN Transaction_amount ELSE 0 END) as Recent_Year_Value,
        SUM(CASE WHEN Year = (SELECT MAX(Year) - 1 FROM agg_transaction) 
            THEN Transaction_amount ELSE 0 END) as Previous_Year_Value,
        SUM(Transaction_amount) as Total_Overall_Value,
        ROUND(
            ((SUM(CASE WHEN Year = (SELECT MAX(Year) FROM agg_transaction) THEN Transaction_amount ELSE 0 END) - 
              SUM(CASE WHEN Year = (SELECT MAX(Year) - 1 FROM agg_transaction) THEN Transaction_amount ELSE 0 END)) * 100.0 /
             SUM(CASE WHEN Year = (SELECT MAX(Year) - 1 FROM agg_transaction) THEN Transaction_amount ELSE 0 END)), 2
        ) as Growth_Rate
    FROM agg_transaction
    GROUP BY State
    HAVING Previous_Year_Value > 0
    ORDER BY Growth_Rate DESC
    LIMIT 10;
    """
    return pd.read_sql(query, engine)

def get_market_status(engine):
    """
    Retrieves market status by state including total transaction value, 
    average transaction size, and growth percentage between the most recent two years.
    """
    query = """
    SELECT 
        State,
        SUM(Transaction_amount) as Total_Value,
        ROUND(AVG(Transaction_amount/Transaction_count), 2) as Avg_Transaction_Size,
        ROUND(
            (MAX(CASE WHEN Year = (SELECT MAX(Year) FROM agg_transaction) THEN Transaction_amount END) -
             MAX(CASE WHEN Year = (SELECT MAX(Year) - 1 FROM agg_transaction) THEN Transaction_amount END))
            * 100.0 /
            MAX(CASE WHEN Year = (SELECT MAX(Year) - 1 FROM agg_transaction) THEN Transaction_amount END), 2) as Growth_Percentage
    FROM agg_transaction
    GROUP BY State
    HAVING MAX(Year) >= (SELECT MAX(Year) - 1 FROM agg_transaction)
    ORDER BY Total_Value DESC;
    """
    return pd.read_sql(query, engine)

def get_top_transaction_volume_states(engine):
    """
    Fetches top states by total transaction volume from agg_transaction table.
    """
    query = """
    SELECT 
        State,
        SUM(Transaction_count) as Total_Transaction_Volume
    FROM agg_transaction
    GROUP BY State
    ORDER BY Total_Transaction_Volume DESC
    LIMIT 10;
    """
    return pd.read_sql(query, engine)

def get_top_transaction_value_states(engine):
    """
    Fetches top states by total transaction value from agg_transaction table.
    """
    query = """
    SELECT 
         State,
         SUM(Transaction_amount) as Total_Transaction_Value
    FROM agg_transaction
    GROUP BY State
    ORDER BY Total_Transaction_Value DESC
    LIMIT 10;
    """
    return pd.read_sql(query, engine)


#5. User Engagement and Growth Strategy


def get_top_states_by_registered_users(engine):
    """
    Fetch top 10 states by total registered PhonePe users.
    """
    query = """
        SELECT 
            State,
            SUM(Registered_users) as Total_Users
        FROM agg_user
        WHERE Year = (SELECT MAX(Year) FROM agg_user)  
        GROUP BY State 
        ORDER BY Total_Users DESC
        LIMIT 10;
    """
    return pd.read_sql(query, engine)

def get_top_districts_by_registered_users(engine):
    """
    Fetch top 10 districts by total registered PhonePe users.
    """
    query = """
        SELECT 
            State,
            District,
            SUM(Registered_users) as Total_Users
        FROM map_user
        WHERE Year = (SELECT MAX(Year) FROM map_user)  
        GROUP BY State, District 
        ORDER BY Total_Users DESC
        LIMIT 10;
    """
    return pd.read_sql(query, engine)


def get_state_engagement_ratio(engine):
    """
    Returns user engagement ratio by state as percentage of app opens to registered users.
    """
    query = """
    SELECT 
        State,
        SUM(Registered_users) as Total_Registered,
        SUM(App_opens) as Total_App_Opens,
        ROUND((SUM(App_opens) * 1.0 / SUM(Registered_users)) * 100, 2) as Engagement_Ratio_Percent
    FROM agg_user 
    WHERE Registered_users > 0 AND Year = (SELECT MAX(Year) FROM agg_user)
    GROUP BY State 
    ORDER BY Engagement_Ratio_Percent DESC
    LIMIT 10;
    """
    return pd.read_sql(query, engine)

def get_district_engagement_ratio(engine):
    """
    Returns top 20 districts with highest user engagement ratios.
    """
    query = """
    SELECT 
        State,
        District,
        SUM(Registered_users) as Total_Registered,
        SUM(App_opens) as Total_App_Opens,
        ROUND((SUM(App_opens) * 1.0 / SUM(Registered_users)) * 100, 2) as Engagement_Ratio_Percent
    FROM map_user 
    WHERE Registered_users > 0 AND Year = (SELECT MAX(Year) FROM map_user)
    GROUP BY State, District 
    ORDER BY Engagement_Ratio_Percent DESC
    LIMIT 10;
    """
    return pd.read_sql(query, engine)


def get_dormant_user_regions(engine):
    """
    Fetch top 10 regions with high registered users but low engagement levels, indicating dormant users.
    """
    query = """
        SELECT 
            State,
            SUM(Registered_users) as Total_Registered,
            SUM(App_opens) as Total_App_Opens,
            ROUND((SUM(App_opens) * 1.0 / SUM(Registered_users)) * 100, 2) as Engagement_Ratio_Percent,
            'Dormant Region' as Category
        FROM agg_user 
        WHERE Registered_users > 0 AND Year = (SELECT MAX(Year) FROM agg_user)
        GROUP BY State 
        ORDER BY Total_Registered DESC, Engagement_Ratio_Percent ASC
        LIMIT 10;
    """
    return pd.read_sql(query, engine)


def get_growth_states_by_engagement(engine):
    """
    Retrieve states with the yearly engagement rate (app opens per registered users).
    """
    query = """
        SELECT 
            State,
            Year,
            ROUND(
                (SUM(App_opens) * 1.0 / SUM(Registered_users)) * 100, 2
            ) as Yearly_Engagement_Percent
        FROM agg_user 
        GROUP BY State, Year 
        ORDER BY Yearly_Engagement_Percent DESC;
    """
    return pd.read_sql(query, engine)


def get_target_districts_low_engagement(engine):
    """
    Retrieve 20 districts ranked by lowest engagement ratio (app opens per registered user) for targeting user stickiness.
    """
    query = """
        SELECT
            State,
            District,
            SUM(Registered_users) AS Total_Registered,
            SUM(App_opens) AS Total_App_Opens,
            ROUND((SUM(App_opens) * 1.0 / NULLIF(SUM(Registered_users), 0)) * 100, 2) AS Engagement_Ratio_Percent
        FROM map_user
        WHERE Year = (SELECT MAX(Year) FROM map_user)
        GROUP BY State, District
        HAVING Engagement_Ratio_Percent > 0
        ORDER BY Engagement_Ratio_Percent ASC
        LIMIT 20;
    """
    return pd.read_sql(query, engine)


#Indian curreny format

def indian_number_format(n):
    if n >= 1e7:
        return f"{n/1e7:.2f} crores"
    elif n >= 1e5:
        return f"{n/1e5:.2f} lakhs"
    elif n >= 1e3:
        return f"{n/1e3:.2f} thousands"
    else:
        return f"{n:.0f}"







