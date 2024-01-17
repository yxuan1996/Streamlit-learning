import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import ast
import time
from statistics import median
import pydeck as pdk

import folium
from streamlit_folium import st_folium

st.set_page_config(
    page_title="F1 Race Tracks",
    page_icon="🏎️",
    layout="wide"
)

def initialize_session_state():
    if "Point_Marker" not in st.session_state:
        st.session_state['Point_Marker'] = 0
    if "option" not in st.session_state:
        st.session_state['option'] = 0
    if 'Lat_Length' not in st.session_state:
        st.session_state['Lat_Length'] = 1

initialize_session_state()

def reset_session_state():
    st.session_state['Point_Marker'] = 0

@st.cache_data
def load_data():
    df = pd.read_csv("2018_F1_race_tracks.csv")
    return df

race_tracks = load_data()

def get_race_track(selected):
    selected_race_track = race_tracks[race_tracks['name'] == selected]

    Park_Coords = list(selected_race_track['coordinates_list'])[0]
    Lat = []
    Long = []
    Points = []

    # Convert String back to list
    Park_Coords = ast.literal_eval(Park_Coords)

    for i in Park_Coords:
        j = i.split(",")
        Lat.append(float(j[1]))
        Long.append(float(j[0]))
        Points.append([float(j[1]), float(j[0])])

    return Lat, Long, Points

def create_map(Lat, Long, Points):

    df_points = pd.DataFrame({'Coordinates': [Points], 'color': [(255,0,0)]})

    # Create a PyDeck layer for the polyline
    layer = pdk.Layer(
        "PathLayer",
        data=df_points,
        get_path="Coordinates",
        get_width=5,
        # get_color=[255, 0, 0],  # Red color
        width_scale=20,
        width_min_pixels=5,
        get_color='color',
    )

    # Set the initial view state
    view_state = pdk.ViewState(
        latitude=median(Lat),
        longitude=median(Long),
        zoom=14
    )

    # Create a PyDeck deck
    deck = pdk.Deck(layers=[layer], initial_view_state=view_state)

    return deck, df_points


st.title('F1 Race Tracks')

option = st.selectbox(
    'Please select a race track',
    (race_tracks['name']))

my_bar = st.progress(float(st.session_state['Point_Marker']/(st.session_state['Lat_Length'] )), text='Race Progress')

on = st.toggle('Update Map in Realtime', value=True)

if ((option != None) or (st.session_state['option'] != None)):
    st.session_state['option'] = option

    LatR, LongR, PointsR = get_race_track(st.session_state['option'])

    deck, df_points = create_map(LatR, LongR, PointsR)
    st.write(df_points)

    st.pydeck_chart(deck)

    # while (st.session_state['Point_Marker'] <= len(LatR)):
    #     time.sleep(7)

    #     my_bar.progress(float(st.session_state['Point_Marker']/(len(LatR))), text='Race Progress')
    #     st.session_state['Lat_Length'] = len(LatR)

    #     print(st.session_state['Point_Marker'])
    #     folium.CircleMarker(location=(PointsR[st.session_state['Point_Marker']][0], PointsR[st.session_state['Point_Marker']][1]), radius=3, color='Green').add_to(m)

    #     fg = folium.FeatureGroup(name='Competitors')

    #     fg.add_child(
    #         folium.CircleMarker(location=(PointsR[st.session_state['Point_Marker']][0], PointsR[st.session_state['Point_Marker']][1]), radius=3, color='Fuchsia')
    #     )

    #     st_data = st_folium(m,
    #         feature_group_to_add=fg,
    #         height=400,
    #         width=700,
    #     )

    #     st.session_state['Point_Marker'] = st.session_state['Point_Marker'] + 1

        # if on:
        #     st.rerun()

