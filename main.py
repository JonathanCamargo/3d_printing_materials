import streamlit as st
import sys

sys.path.insert(0, r'C:/Users/juanp/Downloads/Caracterizacion/Parser')

from base2 import cargar_conjunto,propiedades


st.session_state.conjunto=cargar_conjunto()
st.session_state.propiedades=propiedades(st.session_state.conjunto)