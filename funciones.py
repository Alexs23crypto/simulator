import pandas as pd
import numpy as np
import folium
from streamlit_folium import folium_static

def load_shelters():
    return pd.read_excel("albergues_select_nsga.xlsx")


def show_map(selected_shelters):
    m = folium.Map(location=[-12.0464, -77.0428], zoom_start=10)
    municipality = folium.FeatureGroup(name='Municipality of Lima')
    nsga = folium.FeatureGroup(name='Algorithm Selection')

    for _, albergue in selected_shelters.iterrows():
        if albergue['Estado'] == 'N':
            # Marcadores de Municipalidad
            folium.Marker(
                [albergue['LATITUD'], albergue['LONGITUD']],
                popup=f"District: {albergue['DISTRITO']} - Place: {albergue['ALBERGUE']}",
                icon=folium.Icon(color='green', icon='home', prefix='fa')
            ).add_to(municipality)
        else:
            # Marcadores de NSGA-II
            folium.Marker(
                [albergue['LATITUD'], albergue['LONGITUD']],
                popup=f"District: {albergue['DISTRITO']} - Place: {albergue['ALBERGUE']}",
                icon=folium.Icon(color='blue', icon='home', prefix='fa')
            ).add_to(nsga)


    municipality.add_to(m)
    nsga.add_to(m)
    folium.LayerControl(position='topright').add_to(m)
    folium_static(m)