import streamlit as st
from base2 import sel_propiedades

options=st.multiselect("Seleccione los casos a considerar", st.session_state.conjunto.keys())

dfE,dfF=sel_propiedades(st.session_state.propiedades,options)

dfE

dfF