# 🌍 CO₂ Analytics Pro+

**Aplicación Web Interactiva para el Análisis, Visualización y Predicción de Emisiones Globales de CO₂**

> Proyecto Final - Programación para Ciencia de Datos  
> CDAT-D02A-H-2708-202510  
> Universidad Tecnológica de Bolívar  
> Fecha de entrega: 30 de mayo de 2025

---

## 🧠 Descripción del Proyecto

**CO₂ Analytics Pro+** es una aplicación web interactiva desarrollada con **Streamlit**, que permite a los usuarios explorar, comparar y predecir las emisiones de dióxido de carbono a nivel global. La plataforma se apoya en inteligencia artificial para automatizar visualizaciones y modelos de predicción, ofreciendo una herramienta potente para la comprensión del cambio climático desde un enfoque visual, exploratorio y analítico.

El proyecto tiene como objetivo facilitar la **reflexión crítica**, promover la **alfabetización de datos ambientales** y generar **insumos estratégicos** para políticas públicas o acciones ciudadanas frente a la crisis climática.

---

## 🗂️ Contenido

- [🔍 Fuente y Estructura del Dataset](#-fuente-y-estructura-del-dataset)
- [🧰 Funcionalidades Clave](#-funcionalidades-clave)
- [📊 Tipos de Análisis Realizados](#-tipos-de-análisis-realizados)
- [🔮 Modelo Predictivo Integrado](#-modelo-predictivo-integrado)
- [🤖 Uso de Inteligencia Artificial en el Desarrollo](#-uso-de-inteligencia-artificial-en-el-desarrollo)
- [🧾 Instrucciones de Uso](#-instrucciones-de-uso)
- [🎯 Reflexión Crítica y Relevancia Práctica](#-reflexión-crítica-y-relevancia-práctica)
- [📦 Archivos Entregables](#-archivos-entregables)
- [👥 Autores](#-autores)
- [📝 Créditos y Fuentes](#-créditos-y-fuentes)

---

## 🔍 Fuente y Estructura del Dataset

- **Fuente oficial:** [Our World in Data - CO₂ Dataset](https://github.com/owid/co2-data)
- **Formato:** CSV
- **Cobertura temporal:** 1750 a 2022
- **Cobertura geográfica:** Más de 200 países y regiones
- **Variables clave:**
  - `country`: Nombre del país
  - `iso_code`: Código ISO del país
  - `year`: Año (convertido a datetime)
  - `co2`: Emisiones totales en megatoneladas
  - `co2_per_capita`: Emisiones por persona
  - `co2_per_gdp`: Emisiones por dólar del PIB
  - `population`: Población del país
  - `gdp`: Producto Interno Bruto en USD

Además, se generan variables adicionales simuladas sectoriales (`co2_energy`, `co2_transport`, `co2_industry`, `co2_building`) para representar la participación de sectores clave en las emisiones totales.

---

## 🧰 Funcionalidades Clave

### 🧭 Interfaz Inteligente y Adaptativa

- Diseño responsivo con selección de tema claro/oscuro/personalizado
- Barra lateral configurable: países, rangos históricos, predicción
- Controles accesibles e intuitivos para una navegación fluida

### 📈 Visualización Interactiva

- **Series Temporales** con líneas suavizadas (Plotly)
- **Comparación entre países** con filtros dinámicos
- **Mapas de calor temporales** que muestran intensidad anual por país
- **Gráficos circulares y de barras** para análisis sectorial
- **Exportación directa** de datos y gráficos en CSV y HTML

---

## 📊 Tipos de Análisis Realizados

1. **Exploración Histórica**  
   Se analiza la evolución de emisiones desde 1750 hasta 2022 en métricas absolutas y relativas:
   - Emisiones totales (Mt)
   - Emisiones per cápita (t)
   - Emisiones por PIB (kg/$)

2. **Análisis Comparativo Global**
   - Comparación visual entre regiones seleccionadas
   - Análisis sectorial de las fuentes de emisión para un año objetivo
   - Mapa de calor que muestra cambios en intensidad por país a lo largo del tiempo

3. **Estadísticas Descriptivas por País**
   - Indicadores sociales y económicos (población, PIB)
   - Visualización de la proporción sectorial en las emisiones nacionales

---

## 🔮 Modelo Predictivo Integrado

La app incorpora **modelos de series temporales con Prophet** (Meta/Facebook) para proyectar tendencias futuras en las emisiones por país.  

**Características del modelo:**
- Predicción ajustable de hasta 15 años
- Inclusión opcional de estacionalidad
- Visualización de bandas de incertidumbre
- Generación dinámica por país y métrica

Esto permite simular escenarios futuros y anticipar riesgos o mejoras según políticas implementadas.

---

## 🤖 Uso de Inteligencia Artificial en el Desarrollo

El código fue asistido mediante **prompts iterativos en plataformas IA como ChatGPT**. Los prompts fueron diseñados para:
- Automatizar la lectura, limpieza y transformación de datos
- Construir visualizaciones interactivas y responsivas
- Integrar un modelo Prophet funcional dentro de Streamlit
- Simular distribución sectorial con fórmulas realistas
- Mejorar el rendimiento con `@st.cache_data`

**Prompt base utilizado:**  
> “Crea una app en Streamlit que lea datos de emisiones de CO₂, permita filtrar países, mostrar líneas temporales y gráficos por sector, y realice predicciones usando Prophet. Quiero filtros dinámicos y una interfaz intuitiva con barra lateral.”

El resultado fue un diseño modular, funcional y replicable, demostrando dominio sobre la generación asistida por IA en proyectos de análisis de datos.

---

## 🧾 Instrucciones de Uso

1. Abre la aplicación web en tu navegador:  
   🌐 [https://tu-enlace-deploy.streamlit.app](https://tu-enlace-deploy.streamlit.app)

2. Usa la **barra lateral** para:
   - Seleccionar países de interés
   - Elegir el periodo de análisis
   - Configurar parámetros del modelo predictivo

3. Explora las **4 pestañas**:
   - 🌎 Global: evolución histórica y proyección
   - 📊 Comparar: mapa de calor y análisis sectorial
   - 🔍 Detalles: información desglosada por país
   - 📥 Datos: descarga del dataset y gráfico principal

4. Exporta resultados para compartir o seguir analizando localmente.

---

## 🎯 Reflexión Crítica y Relevancia Práctica

El cambio climático es uno de los mayores desafíos de nuestro tiempo. Esta aplicación permite que:
- **Ciudadanos** accedan a datos relevantes de forma clara.
- **Investigadores** encuentren correlaciones y tendencias.
- **Gobiernos** fundamenten decisiones con base en proyecciones confiables.

Al integrar visualización, análisis predictivo y personalización en una sola plataforma, **CO₂ Analytics Pro+** representa una herramienta útil tanto en el aula como en entornos reales de toma de decisiones ambientales.

---

## 📦 Archivos Entregables

- `proyecto.py`: Código principal de la aplicación
- `README.md`: Documentación del proyecto (este archivo)
- `captura_de_pantalla.png`: Imagen de la interfaz con filtros y gráficos activos
- `prompt.txt`: Texto del prompt utilizado en el desarrollo
- Enlace web: [https://tu-enlace-deploy.streamlit.app](https://tu-enlace-deploy.streamlit.app) *(actualizar tras desplegar)*

---

## 👥 Autor:
- 👤 Nombre completo del estudiante 2 *(Keren Hapuc Subiroz Galvan - T00065933)*


---

## 📝 Créditos y Fuentes

- **Datos:** Our World in Data ([owid.co2-data](https://github.com/owid/co2-data))
- **Visualización:** Plotly Express y Graph Objects
- **Modelo Predictivo:** [Prophet](https://facebook.github.io/prophet/)
- **Framework Web:** [Streamlit](https://streamlit.io)
- **Logo Global Carbon Project:** Wikimedia Commons
-

---

**© 2025 - Proyecto académico sin fines comerciales**

