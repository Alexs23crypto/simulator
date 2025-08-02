import pandas as pd
import numpy as np
import folium
from streamlit_folium import folium_static

def load_shelters():
    return pd.read_excel("albergues_select_nsga.xlsx")


def show_map(selected_shelters):
    muni_df = pd.read_excel("ALBERGUES TEMPORALES MUNICIPALIDAD_v2.xlsx")
    
    m = folium.Map(location=[-12.0464, -77.0428], zoom_start=10)
    both = folium.FeatureGroup(name='Algorithm and Municipality of Lima')
    nsga = folium.FeatureGroup(name='Algorithm Selection')
    municipality = folium.FeatureGroup(name = 'Municipality of Lima')

    show_muni = st.checkbox("Show Municipality shelters")

    for _, albergue in selected_shelters.iterrows():
        marker_popup = folium.Popup(
            f"District: {albergue['DISTRITO']}<br>Place: {albergue['ALBERGUE']}", max_width=300)

        if albergue['Estado'] == 'N':
            # Marcadores de Municipalidad con CircleMarker más pequeño
            folium.CircleMarker(
                location=[albergue['LATITUD'], albergue['LONGITUD']],
                radius=4,  # tamaño del punto
                color='green',
                fill=True,
                fill_color='green',
                fill_opacity=0.7,
                popup=marker_popup
            ).add_to(both)
        else:
            # Marcadores de NSGA-II con CircleMarker más pequeño
            folium.CircleMarker(
                location=[albergue['LATITUD'], albergue['LONGITUD']],
                radius=4,  # tamaño del punto
                color='blue',
                fill=True,
                fill_color='blue',
                fill_opacity=0.7,
                popup=marker_popup
            ).add_to(nsga)

    if show_muni:
        for _, muni in muni_df.iterrows():
            marker_popup = folium.Popup(
                f"District: {muni['DISTRITO']}<br>Place: {muni['ALBERGUE']}", max_width=300)

            folium.CircleMarker(
                location=[muni['LATITUD'], muni['LONGITUD']],
                radius=4,
                color='green',
                fill=True,
                fill_color='green',
                fill_opacity=0.7,
                popup=marker_popup
            ).add_to(municipality)

        municipality.add_to(m)

    #municipality.add_to(m)
    nsga.add_to(m)
    both.add_to(m)
    
    folium.LayerControl(position='topright').add_to(m)
    folium_static(m)
