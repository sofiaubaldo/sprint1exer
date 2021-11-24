# 10: Plotting maps using st.map (page 4)

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium
from streamlit_folium import folium_static
import geopandas as gpd
import warnings
warnings.filterwarnings('ignore')


df = pd.read_csv("data/2016-2019-voter-data.csv")
my_page = st.sidebar.radio('Page Navigation', ['page 1', 'page 2', 'page 3', 'page 4'])

if my_page == 'page 1':
    st.title("Data")
    st.header("2016-2019 Philippine Voter Dataset")
    if st.checkbox('Show data', value = True):
        st.subheader('Data')
        data_load_state = st.text('Loading data...')
        st.write(df.head(20))
        data_load_state.markdown('Loading data...**done!**')
    
elif my_page == 'page 2':
    option = st.sidebar.selectbox('Which region do you want to see?', df['Region'].unique())

    'You selected: ', option

    # Filter the entry in the plot
    province_level = df[df['Region'] == option].groupby("Province")["2019-Registered_Voters"].sum()

    st.header(f"Barchart of {option}")

    # store figure in fig variable
    fig = plt.figure(figsize=(8,6)) 

    plt.bar(province_level.index, province_level.values) 

    plt.title("Registered Voters by Province", fontsize=16)
    plt.ylabel("Number of Registered Voters", fontsize=12)
    plt.xlabel("Province", fontsize=12)
    plt.xticks(rotation=45)

    # display graph
    st.pyplot(fig)
    
elif my_page == 'page 3':
    st.title("Geospatial Analysis: Folium")
    shapefile = gpd.read_file('data/Provinces/Provinces.shp')
    shapefile["x"] = shapefile.geometry.centroid.x
    shapefile["y"] = shapefile.geometry.centroid.y
    map_center = [14.583197, 121.051538]

    # Styling the map
    mymap = folium.Map(location=map_center, height=700, width=1000, tiles="OpenStreetMap", zoom_start=14)
    option_reg = st.sidebar.selectbox(
        'Which region',
        shapefile["REGION"].unique())
    
    'You selected: ', option_reg
    
    reg = option_reg
    df_reg = shapefile[shapefile["REGION"]==reg]

    for i in np.arange(len(df_reg)):
        lat = df_reg["y"].values[i]
        lon = df_reg["x"].values[i]
        name = df_reg["PROVINCE"].values[i]
        folium.Marker([lat, lon], popup=name).add_to(mymap)
    folium_static(mymap)
    
elif my_page == 'page 4':
    st.title("Geospatial Analysis: st.map()")
    shapefile = gpd.read_file('data/Provinces/Provinces.shp')
    shapefile["lat"] = shapefile.geometry.centroid.x
    shapefile["lon"] = shapefile.geometry.centroid.y
    st.map(shapefile)