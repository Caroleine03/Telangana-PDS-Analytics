import os
import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium

# Load data
@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, '..', 'outputs', 'shop_profiles_clustered.csv')
    return pd.read_csv(file_path)

shop_profiles = load_data()

features = ['utilization_ratio', 'portability_rate', 
            'rice_per_card', 'trans_volatility']

# Title
st.title("Telangana PDS Analytics Dashboard")
st.write("Shop Performance Clustering and Anomaly Detection")

# Sidebar
st.sidebar.title("Filters")
districts = ['All'] + sorted(shop_profiles['distname'].unique().tolist())
selected_district = st.sidebar.selectbox("Select District", districts)
selected_cluster = st.sidebar.selectbox("Select Cluster", ['All', 0, 1, 2, 3, 4])

# Filter data
if selected_district == 'All':
    filtered_df = shop_profiles
else:
    filtered_df = shop_profiles[shop_profiles['distname'] == selected_district]

if selected_cluster != 'All':
    filtered_df = filtered_df[filtered_df['cluster'] == selected_cluster]

# Metrics
st.subheader("Overview")
col1, col2, col3 = st.columns(3)
col1.metric("Total Shops", len(filtered_df))
col2.metric("Avg Utilization", f"{filtered_df['utilization_ratio'].mean():.2%}")
col3.metric("Avg Portability", f"{filtered_df['portability_rate'].mean():.2%}")

# Map — limit to 500 shops for performance!
st.subheader("🗺️ Shop Location Map")
st.info(f"Showing {min(500, len(filtered_df))} shops on map")

map_df = filtered_df.head(500)  # ← LIMIT FOR PERFORMANCE!
m = folium.Map(location=[17.5, 79.0], zoom_start=7)

colors = {0: 'red', 1: 'blue', 2: 'green', 
          3: 'purple', 4: 'orange'}

for _, row in map_df.iterrows():
    folium.CircleMarker(
    location=[row['latitude'], row['longitude']],
    radius=3,
    color=colors[int(row['cluster'])],
    fill=True,
    popup=f"Shop: {row['shopno']}<br>Cluster: {row['cluster']}",
    tooltip=f"Shop: {row['shopno']} | Cluster: {row['cluster']}"
).add_to(m)

st_folium(m, width=800, height=500)

# Shop Search
st.subheader("🔍 Shop Search Tool")
shop_no = st.number_input("Enter Shop Number", min_value=0, step=1)

if shop_no > 0:
    shop_data = shop_profiles[shop_profiles['shopno'] == shop_no]
    
    if len(shop_data) > 0:
        cluster_id = shop_data['cluster'].values[0]
        cluster_avg = shop_profiles[shop_profiles['cluster'] == cluster_id][features].mean()
        
        st.write(f"### Shop {shop_no} — Cluster {cluster_id}")
        
        comparison = pd.DataFrame({
            'Shop Value': shop_data[features].values[0],
            'Cluster Average': cluster_avg.values
        }, index=features)
        
        st.dataframe(comparison)
    else:
        st.warning(f"Shop {shop_no} not found!")
