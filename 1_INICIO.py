import streamlit as st
import pandas as pd

#import streamlit as st
import pandas as pd

# Título y descripción del Centro
st.title("Centro Eco-pedagógico AUCCA")
st.subheader("Potenciando el intercambio de saberes para la autogestión comunitaria en armonía con el medio ambiente")

# Función para cargar el logo
def load_logo():
    logo_path = "images/logo_aucca.png"
    st.image(logo_path, use_column_width=True)

# Cargar y mostrar el logo
load_logo()

# Función para cargar la lista de plantas
@st.cache_data
def load_listado_plantas_aucca():
    return pd.read_csv("lista_plantas_aucca.csv", sep=';', encoding='latin1')




# Cargar el listado de plantas
plantas_list = load_listado_plantas_aucca()

# Conversión de los valores de "Familia" a string y manejo de NaN
plantas_list['Familia'] = plantas_list['Familia'].fillna("Sin información").astype(str)


# Conversión de los valores de "Disponible Nov 2024" a string y manejo de NaN
plantas_list['Disponible Nov 2024'] = plantas_list['Disponible Nov 2024'].fillna("No especificado").astype(str)
disponible_opciones = sorted(plantas_list['Disponible Nov 2024'].unique())

# Selección de filtros
familia_opciones = sorted(plantas_list['Familia'].unique())
disponible_opciones = sorted(plantas_list['Disponible Nov 2024'].unique())

familia_seleccionada = st.selectbox("Selecciona la Familia de plantas", ["Todas"] + familia_opciones)
disponible_seleccionado = st.selectbox("Disponible en Noviembre 2024", ["Todas"] + disponible_opciones)

# Filtrar las plantas según los filtros seleccionados
plantas_filtradas = plantas_list.copy()

if familia_seleccionada != "Todas":
    plantas_filtradas = plantas_filtradas[plantas_filtradas['Familia'] == familia_seleccionada]

if disponible_seleccionado != "Todas":
    plantas_filtradas = plantas_filtradas[plantas_filtradas['Disponible Nov 2024'] == disponible_seleccionado]

# Mostrar la lista filtrada de plantas
st.write("### Listado de Plantas")
st.dataframe(plantas_filtradas)