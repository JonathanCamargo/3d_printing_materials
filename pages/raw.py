import streamlit as st
from base2 import graficar_conjunto



options=st.multiselect("Seleccione los casos a graficar", st.session_state.conjunto.keys())

fig=graficar_conjunto(st.session_state.conjunto,options)

st.pyplot(fig)