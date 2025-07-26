import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import folium_static
import plotly.express as px
import ast

from funciones import show_map, load_shelters

st.set_page_config(page_title="Shelter Location Simulator", layout="wide")
st.title("🏠 Shelter Location Simulator")

# --- Página principal con selección
#st.markdown("### Select an optimization algorithm to explore the selected shelters:")
#col1, col2, col3 = st.columns(3)

# Variables de control
#if "page" not in st.session_state:
    #st.session_state.page = None

#with col1:
    #if st.button("🔷 NSGA-II"):
        #st.session_state.page = "NSGA"

#with col2:
    #if st.button("🔶 SPEA-II"):
        #st.session_state.page = "SPEA"

#with col3:
    #if st.button("⚖️ Agreement"):
        #st.session_state.page = "Comparative"


# --- Función para renderizar una vista
def mostrar_resultado(albergues_df, pareto_df, metodo):
    #st.markdown(f"### 📊 Pareto Front - {metodo}")
    st.markdown(f"### 📊 Lima Emergency Shelter Planning Tool")

    # --- Dividir espacio inferior en 3 columnas
    col1, col2 = st.columns([1, 2.2])  # Col3 un poco más ancha

    with col1:
        st.subheader("3D Scatter Plot")

        selected_id = st.selectbox("Select a solution:", pareto_df['Indice'], index=0)
        # Añadir color
        pareto_df['Color'] = pareto_df['Indice'].apply(lambda x: 'Selected' if x == selected_id else 'Not selected')
        
        translated_df = pareto_df.rename(columns={
            'Distancia entre albergues': 'Distance between shelters',
            'Vulnerabilidad y riesgo sísmico': 'Seismic vulnerability and risk',
            'Población demandada': 'Demanded population'
        })
        
        # Gráfico 3D con nombres en inglés
        fig = px.scatter_3d(
        translated_df,
            x='Distance between shelters',
            y='Seismic vulnerability and risk',
            z='Demanded population',
            color='Color',
            color_discrete_map={'Selected': 'red', 'Not selected': 'blue'},
            custom_data=['Indice'],
            height=500,
            labels={
                'Distance between shelters': 'Objective 1',
                'Seismic vulnerability and risk': 'Objective 2',
                'Demanded population': 'Objective 3'
            }
        )
        
        # Refuerza los títulos por si no los toma bien
        fig.update_layout(
            scene=dict(
                xaxis_title='Objective 1',
                yaxis_title='Objective 2',
                zaxis_title='Objective 3'
            ),
            showlegend=False
        )
        
        # Tooltip personalizado con los nombres reales
        fig.update_traces(
            hovertemplate="<br>".join([
                "Solution: %{customdata[0]}",
                "Distance between shelters: %{x}",
                "Seismic vulnerability and risk: %{y}",
                "Demanded population: %{z}"
            ])
        )
        
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("""
        **Objective 1**: Distance between shelters  
        **Objective 2**: Seismic vulnerability and risk  
        **Objective 3**: Demanded population
        """)

    with col2:
        st.subheader("🗺️ Map of Shelters")
        # Filtrar datos seleccionados
        selected_solution = pareto_df[pareto_df['Indice'] == selected_id]
        shelter_data = albergues_df[albergues_df['Indice'] == selected_id]
    
        # Filtro por distrito
        districts = ["All districts"] + sorted(albergues_df['DISTRITO'].unique())
        selected_district = st.selectbox("Seleccione un distrito", districts)
    
        if selected_district != "All districts":
            shelter_data = shelter_data[shelter_data['DISTRITO'] == selected_district]

        st.write(f"Number of shelters: {shelter_data.shape[0]}")

        # --- Estadísticas en ancho completo
        #st.subheader("📌 Shelter Statistics")
        avg_water = shelter_data['DIST_AGUA'].mean()
        avg_hospital = shelter_data['DIST_HOSP'].mean()
        total_pop = shelter_data['POB_DEMAN'].sum()
        total_dist = shelter_data['DISTRITO'].nunique()
    
        stats_df = pd.DataFrame({
            "Statistic": [
                "Average distance to hospitals (km)",
                "Average distance to water (km)",
                "Vulnerable population",
                "Number of districts with shelters (out of 43)"
            ],
            "Value": [
                f"{avg_hospital:.2f} km" if avg_hospital >= 0 else "-",
                f"{avg_water:.2f} km" if avg_water >= 0 else "-",
                f"{total_pop:,} people" if total_pop >= 0 else "-",
                f"{total_dist}" if total_dist >= 0 else "-"
            ]
        })
        st.dataframe(stats_df, hide_index=True)
        st.markdown("""
        - 🔵 **Blue points**: Shelters selected by the algorithm.
        - 🟢 **Green points**: Shelters selected by both the algorithm and the Municipality of Lima.
        """)        
        show_map(shelter_data)


# --- Mostrar contenido basado en botón seleccionado

pareto_df = pd.read_excel("frontera_pareto.xlsx")
albergues_df = load_shelters()
mostrar_resultado(albergues_df,pareto_df, "NSGA-II")



#if st.session_state.page == "NSGA":
    #pareto_df = pd.read_excel("frontera_pareto.xlsx")
    #albergues_df = load_shelters()
    #mostrar_resultado(albergues_df,pareto_df, "NSGA-II")

#elif st.session_state.page == "SPEA":
    #pareto_df = pd.read_excel("frontera_pareto.xlsx")
    #albergues_df = pd.read_excel("albergues_select_nsga.xlsx")
    #mostrar_resultado(albergues_df, pareto_df, "SPEA-II")

#elif st.session_state.page == "Comparative":
    #st.subheader("⚖️ Comparative analysis between NSGA-II and SPEA-II")
    #st.info("This section will show a comparative analysis of both algorithm results (to be implemented).")

