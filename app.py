import streamlit as st
import requests
from PIL import Image
from io import BytesIO


def obtener_datos_especie_o_genero(nombre):
    url = f"https://api.gbif.org/v1/species/match?name={nombre}&strict=false&verbose=true"
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        return respuesta.json()
    else:
        st.error("Error al realizar la búsqueda")
        return None


def obtener_imagen_wikipedia(nombre):
    url = f"https://en.wikipedia.org/w/api.php?action=query&titles={nombre}&prop=pageimages&format=json&pithumbsize=500"
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        resultados = respuesta.json()
        pages = resultados.get('query', {}).get('pages', {})
        if pages:
            page = next(iter(pages.values()))
            return page.get('thumbnail', {}).get('source')
    return None


def run_app():
    st.sidebar.header("Buscar taxon")
    nombre = st.sidebar.text_input("busqueda:")

    if nombre:
        datos = obtener_datos_especie_o_genero(nombre)
        if datos:
            col1, col2 = st.columns([1, 2])

            imagen_url = obtener_imagen_wikipedia(nombre)
            if imagen_url:
                with col1:
                    st.image(imagen_url, caption=f"Imagen de {nombre}")

            with col2:
                st.write(datos)
        else:
            st.error("No se encontraron resultados para este nombre.")


if __name__ == "__main__":
    run_app()





