import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from prophet import Prophet
from io import BytesIO
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# 1. Configuración avanzada
st.set_page_config(
    layout="wide",
    page_title="🌍 CO₂ Analytics Pro+",
    page_icon="✅",
    initial_sidebar_state="expanded"
)

# 2. Carga eficiente de datos
@st.cache_data(ttl=3600)  # Cache por 1 hora
def load_data():
    url = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"
    df = pd.read_csv(url, parse_dates=['year'])
    
    # Datos sectoriales realistas (ejemplo)
    sectors = {
        'energy': 'Energía',
        'transport': 'Transporte',
        'industry': 'Industria',
        'building': 'Construcción'
    }
    
    for sector in sectors.keys():
        df[f'co2_{sector}'] = df['co2'] * (0.4 + 0.02 * (df['year'].dt.year - 1990)/(2022-1990))
    
    return df, sectors

df, sectors = load_data()

# 3. Barra lateral mejorada
with st.sidebar:
    st.image("https://png.pngtree.com/png-vector/20220526/ourmid/pngtree-co2-carbon-dioxide-logo-vector-design-png-image_4724118.png", width=200)
    
    with st.expander("⚙️ CONFIGURACIÓN", expanded=True):
        # theme = st.selectbox("Tema visual", ["Claro", "Oscuro", "Personalizado"])

        # if theme == "Personalizado":
        #     main_color = st.color_picker("Elige color principal", "#00f5d4")
        #     plotly_template = "plotly"
        # elif theme == "Oscuro":
        #     main_color = "#636EFA"
        #     plotly_template = "plotly_dark"
        # else:
        #     main_color = "#636EFA"
        #     plotly_template = "plotly_white"


        # if theme == "Personalizado":
        #     main_color = st.color_picker("Elige color principal", "#00f5d4")
        # else:
        #     main_color = "#636EFA"  # color por defecto de Plotly

        # Verificamos que los países por defecto existan
        available_countries = df[~df['iso_code'].isna()]['country'].unique()
        default_countries = [c for c in ["Mexico", "United States", "China", "European Union"] if c in available_countries]

        countries = st.multiselect(
            "Seleccionar países",
            options=available_countries,
            default=default_countries,
            max_selections=5
        )
        year_range = st.slider(
            "Rango histórico",
            min_value=1750,
            max_value=2022,
            value=(2000, 2022)
        )
    
    with st.expander("🔮 PREDICCIÓN", expanded=True):
        forecast_settings = {
            'years': st.slider("Años a predecir", 1, 15, 5),
            'seasonality': st.checkbox("Incluir estacionalidad", True),
            'uncertainty': st.checkbox("Mostrar intervalo", True)
        }
    
    st.markdown("---")
    st.caption("🔍 Datos actualizados al 2023")
    st.caption("📊 v2.1 | CO₂ Analytics Pro+")

# 4. Visualizaciones optimizadas
tab1, tab2, tab3, tab4 = st.tabs(["🌎 Global", "📊 Comparar", "🔍 Detalles", "📥 Datos"])

with tab1:
    st.header("Tendencias Globales de Emisiones")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        metric = st.radio(
            "Métrica clave",
            ["co2", "co2_per_capita", "co2_per_gdp"],
            format_func=lambda x: {
                "co2": "Emisiones Totales (Mt)",
                "co2_per_capita": "Per Cápita (t)",
                "co2_per_gdp": "Por PIB (kg/$)"
            }[x],
            horizontal=True
        )
    
    with col2:
        if st.button("🔄 Actualizar gráficos"):
            st.cache_data.clear()
    
    fig = px.line(
        df[(df['country'].isin(countries)) & 
           (df['year'].dt.year.between(year_range[0], year_range[1]))],
        x='year',
        y=metric,
        color='country',
        line_shape="spline",
        render_mode="svg",
        hover_data={
            'population': True,
            'gdp': ':.2f',
            'year': '%Y'
        }
    )
    
    # Modelado predictivo con Prophet
    if countries:
        for country in countries:
            country_data = df[df['country'] == country][['year', metric]].rename(
                columns={'year': 'ds', metric: 'y'}).dropna()
            
            if len(country_data) > 10:
                model = Prophet(
                    yearly_seasonality=forecast_settings['seasonality'],
                    uncertainty_samples=100 if forecast_settings['uncertainty'] else 0
                )
                model.fit(country_data)
                
                future = model.make_future_dataframe(
                    periods=forecast_settings['years'] * 365,
                    freq='D'
                )
                forecast = model.predict(future)
                
                fig.add_trace(go.Scatter(
                    x=forecast['ds'],
                    y=forecast['yhat'],
                    mode='lines',
                    line=dict(dash='dot', width=2),
                    name=f'{country} (Predicción)',
                    showlegend=True
                ))
                
                if forecast_settings['uncertainty']:
                    fig.add_trace(go.Scatter(
                        x=forecast['ds'].tolist() + forecast['ds'].tolist()[::-1],
                        y=forecast['yhat_upper'].tolist() + forecast['yhat_lower'].tolist()[::-1],
                        fill='toself',
                        fillcolor='rgba(100,100,100,0.2)',
                        line=dict(color='rgba(255,255,255,0)'),
                        hoverinfo="skip",
                        name=f'Intervalo {country}'
                    ))
    
    st.plotly_chart(fig, use_container_width=True, theme="streamlit")

    st.header("Tendencias Globales de Emisiones")
    
    # Sección de documentación con pestañas
    doc_tabs = st.tabs(["📌 Guía Rápida", "🛠️ Tutorial", "⚠️ Limitaciones", "ℹ️ Acerca de"])
    
    with doc_tabs[0]:  # Guía Rápida
        st.markdown("""
        ### Bienvenido a CO₂ Analytics Pro+
        Herramienta interactiva para analizar emisiones globales de CO₂ (1750-2022)
        
        **Funcionalidades principales:**
        🌍 | Visualización de tendencias históricas  
        📊 | Comparación entre países  
        🔮 | Predicciones con modelo Prophet  
        🏭 | Análisis sectorial de emisiones  
        💾 | Exportación de datos en múltiples formatos
        
        **Cómo comenzar:**
        1. Selecciona países en la barra lateral (máx. 5)
        2. Ajusta el rango de años según tu interés
        3. Explora las diferentes métricas disponibles
        """)
        
        # Glosario técnico en columnas
        col_glos1, col_glos2 = st.columns(2)
        with col_glos1:
            st.markdown("""
            **Glosario técnico:**
            - Mt: Millones de toneladas
            - t: Toneladas métricas
            - kg/$: kg por dólar PIB
            """)
        
        with col_glos2:
            st.markdown("""
            **Símbolos gráficos:**
            - ▬ Datos históricos
            - - - - Predicciones
            - █ Margen de error
            """)
    
    with doc_tabs[1]:  # Tutorial
        st.markdown("""
        ### Tutorial Práctico
        
        **Ejemplo 1: Comparación UE vs USA**
        ```python
        1. Seleccionar:
           - European Union
           - United States
        2. Ajustar rango: 2000-2022
        3. Métrica: co2_per_capita
        4. Activar predicción (5 años)
        ```
        
        **Ejemplo 2: Análisis sectorial**
        ```python
        1. Seleccionar solo "China"
        2. Ir a pestaña 🔍 Detalles
        3. Explorar mix energético 2020
        ```
        
        **Interpretación gráfica:**
        ```diff
        + Colores más cálidos = Mayores emisiones
        + Eje Y = Países
        + Eje X = Años
        ```
        """)
    
    with doc_tabs[2]:  # Limitaciones
        st.warning("""
        **Limitaciones importantes:**
        - Datos sectoriales son estimaciones aproximadas
        - Predicciones no consideran eventos disruptivos
        - Rendimiento puede disminuir con >5 países
        - Actualización automática cada 1 hora
        """)
        
        st.info("""
        **Solución a problemas comunes:**
        - Si faltan países: Verificar rango de años
        - Si los gráficos no se actualizan: Usar botón 🔄
        - Si la app es lenta: Reducir número de países
        """)
    
    with doc_tabs[3]:  # Acerca de
        st.markdown("""
        ### Información técnica
        **Versión:** 2.1 (Mayo 2024)  
        **Dataset:** Our World in Data (2023)  
        **Modelo predictivo:** Facebook Prophet  
        **Tecnologías:** Python, Streamlit, Plotly  
        
        **Soporte técnico:**
        📧 soporte@co2analytics.edu  
        🕘 L-V 9:00-18:00 (GMT-5)
        """)
        
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/8/8d/Global_Carbon_Project_logo.svg/1200px-Global_Carbon_Project_logo.svg.png", 
                width=200)
    
    # Separador visual
    st.divider()
    
    # Contenido principal original (gráficos)
    col1, col2 = st.columns([3, 1])
    with col1:
        metric = st.radio(
            "seleccion_metrica",  # ID único modificado
            ["co2", "co2_per_capita", "co2_per_gdp"],
            format_func=lambda x: {
                "co2": "Emisiones Totales (Mt)",
                "co2_per_capita": "Per Cápita (t)",
                "co2_per_gdp": "Por PIB (kg/$)"
            }[x],
            horizontal=True
        )
    
    with col2:
        if st.button("🔄 Actualizar gráficos"):
            st.cache_data.clear()
    
    # ... (resto del código original del gráfico)

with tab2:
    st.header("Análisis Comparativo")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Mapa de Calor Temporal")
        pivot_df = df[(df['country'].isin(countries))].pivot(
            index='year', columns='country', values='co2')
        fig_heatmap = px.imshow(
            pivot_df.T,
            labels=dict(x="Año", y="País", color="Emisiones"),
            aspect="auto"
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)
    
    with col2:
        st.subheader("Distribución Sectorial")
        sector = st.selectbox("Seleccionar sector", list(sectors.values()))
        sector_key = [k for k, v in sectors.items() if v == sector][0]
        
        fig_sector = px.bar(
            df[(df['country'].isin(countries)) & 
               (df['year'].dt.year == year_range[1])],
            x='country',
            y=f'co2_{sector_key}',
            color='country',
            labels={'country': '', f'co2_{sector_key}': f'Emisiones {sector} (Mt)'}
        )
        st.plotly_chart(fig_sector, use_container_width=True)

with tab3:
    st.header("Detalles por País")
    
    selected_country = st.selectbox("Elegir país", countries)
    country_data = df[df['country'] == selected_country]
    
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(px.pie(
            country_data[country_data['year'].dt.year == year_range[1]],
            values=[country_data[f'co2_{sector}'].iloc[0] for sector in sectors.keys()],
            names=list(sectors.values()),
            title=f"Mix Sectorial {selected_country} ({year_range[1]})"
        ), use_container_width=True)
    
    with col2:
        metrics = {
            "Población": "population",
            "PIB (USD)": "gdp",
            "Intensidad Carbónica": "co2_per_gdp"
        }

        data = country_data[country_data['year'].dt.year == year_range[1]][list(metrics.values())]
        data = data.rename(columns=dict(zip(metrics.values(), metrics.keys())))
        data = data.T  # Transponer
        data.columns = ["Valor"]  # Renombrar la única columna resultante

        st.dataframe(
            data,
            column_config={"Valor": st.column_config.NumberColumn(format="%.2f")}
        )


with tab4:
    st.header("Exportación de Datos")
    
    st.download_button(
        label="📥 Descargar dataset completo (CSV)",
        data=df.to_csv(index=False).encode('utf-8'),
        file_name=f"co2_data_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )
    
    st.download_button(
        label="📊 Descargar gráfico principal (HTML)",
        data=fig.to_html(),
        file_name="co2_trend.html",
        mime="text/html"
    )
    
    st.dataframe(
        df[(df['country'].isin(countries)) & 
           (df['year'].dt.year.between(year_range[0], year_range[1]))],
        hide_index=True,
        height=300
    )

# 5. Footer profesional
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 10px;">
    <p>© 2023 CO₂ Analytics Pro+ | <a href="https://www.globalcarbonproject.org/" target="_blank">Datos del Global Carbon Project</a></p>
    <small>v2.1 | Powered by Streamlit y Prophet</small>
</div>
""", unsafe_allow_html=True)
