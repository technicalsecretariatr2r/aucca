import streamlit as st
import pandas as pd
import re
from PIL import Image

# Function to load and configure the page
def structure_and_format():
    im = Image.open("images/logo_aucca.png")
    st.set_page_config(page_title="Plantas Aucca", layout="wide", initial_sidebar_state="expanded")
    st.sidebar.image(im, use_column_width=True)
    css_path = "style.css"

    with open(css_path) as css:
        st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)
    
    # Hide Streamlit footer and menu
    hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    # Hide index column in tables
    hide_table_row_index = """
        <style>
        thead tr th:first-child {display:none}
        tbody th {display:none}
        </style>
    """
    st.markdown(hide_table_row_index, unsafe_allow_html=True)

structure_and_format()

# Function to load plant list
@st.cache_data
def load_listado_plantas_aucca():
    return pd.read_csv("lista_plantas_aucca.csv", sep=';', encoding='latin1')

# Load the plant list
plantas_list = load_listado_plantas_aucca()


st.markdown("## Lista de plantas del cuaderno Chalo")


# CLEANING
# Trim whitespace in 'Disponible Nov 2024', 'Familia', and 'Propiedades' columns
def espacios(value):
    return value.strip() if isinstance(value, str) else value
plantas_list[['Disponible Nov 2024', 'Familia', 'Propiedades']] = plantas_list[['Disponible Nov 2024', 'Familia', 'Propiedades']].applymap(espacios)
plantas_list['Disponible Nov 2024'] = plantas_list['Disponible Nov 2024'].fillna("No especificado").astype(str)
plantas_list['Familia'] = plantas_list['Familia'].fillna("Sin información").astype(str)
plantas_list['Propiedades'] = plantas_list['Propiedades'].fillna("Sin información").astype(str)

def clean_properties(value):
    if isinstance(value, str):
        # Split by multiple delimiters, strip whitespace, and convert each word to lowercase
        words = [word.strip().lower() for word in re.split(r'[,\-]', value)]
        # Join words back into a single string, separated by commas
        return ', '.join(words)
    return value
plantas_list['Familia'] = plantas_list['Familia'].apply(clean_properties)
plantas_list['Propiedades'] = plantas_list['Propiedades'].apply(clean_properties)


def get_unique_words_from_column(df, column_name):
    # Drop NaN values and convert to a list
    all_properties = df[column_name].dropna().tolist()
    # Use regex to split by commas, hyphens, spaces, tabs, and new lines
    all_words = [word.strip() for prop in all_properties for word in re.split(r'[,\-]', prop)]
    # Remove duplicates by converting to a set and back to a list
    unique_words = list(set(all_words))
    return unique_words

plantas_filtradas = plantas_list.copy()

# FILTERS
st.markdown("#### Filtros de Plantas")
st.sidebar.markdown("#### Base de datos")

# FILTER 1: Disponible Nov 2024
disponible_opciones = sorted(plantas_list['Disponible Nov 2024'].unique())
disponible_seleccionado = st.sidebar.selectbox("Disponible en Noviembre 2024", ["Todas"] + disponible_opciones)

if disponible_seleccionado != "Todas":
    plantas_filtradas = plantas_filtradas[plantas_filtradas['Disponible Nov 2024'] == disponible_seleccionado]


# FILTER 2: Familia
plantas_filtradas_2 = plantas_filtradas
familia_opciones = sorted(plantas_filtradas['Familia'].unique())
familia_seleccionada = st.selectbox("Selecciona la Familia de plantas", ["Todas"] + familia_opciones)
if familia_seleccionada != "Todas":
    plantas_filtradas_2 = plantas_filtradas[plantas_filtradas['Familia'] == familia_seleccionada]

# FILTER 3: Propiedades
unique_properties_words_propiedades = get_unique_words_from_column(plantas_filtradas_2, 'Propiedades')
propiedades_seleccion = st.multiselect("Selecciona propiedades para filtrar:", unique_properties_words_propiedades)

plantas_filtradas_3 = plantas_filtradas_2

# Filter by 'Propiedades' only if there are selected words
if propiedades_seleccion:
    plantas_filtradas_3 = plantas_filtradas_3[
        plantas_filtradas_3['Propiedades'].apply(lambda x: any(word in str(x) for word in propiedades_seleccion))
    ]

# Display the filtered DataFrame
st.write("#### Resultados")
st.dataframe(plantas_filtradas_3)


st.write("#### Detalle de Planta")
# FILTER 4: by "Nombre vulgar"
nombre_vulgar_selection_words = sorted(plantas_filtradas_3['Nombre vulgar'].unique())
nombre_vulgar_selection = st.selectbox("Planta específica para leer en detalle", ["Selecciona una planta"] + nombre_vulgar_selection_words)

# Filter by "Nombre vulgar" if a selection is made
if nombre_vulgar_selection != "Selecciona una planta":
    plantas_filtradas_4 = plantas_filtradas_3[plantas_filtradas_3['Nombre vulgar'] == nombre_vulgar_selection]

    # Check if there is data to display for the selected "Nombre vulgar"
    if not plantas_filtradas_4.empty:
        # Iterate over each row in the filtered DataFrame to display detailed information
        for idx, row in plantas_filtradas_4.iterrows():
            st.markdown(f"### Detalles de la Planta: {row['Nombre vulgar']}")
            for column_name, value in row.items():
                if column_name == 'Nombre vulgar':
                    continue  # Skip displaying the "Nombre vulgar" itself
                # Check for missing or empty values
                display_value = value if pd.notna(value) and value != "" else "Información no disponible"
                # Display each field with its column name as a label
                st.markdown(f"**{column_name}:** {display_value}")
            st.markdown("---")  # Add a separator between plants
    else:
        st.write("No hay información disponible")
else:
    st.write("")
    # st.write("Por favor selecciona una planta para explorar más")