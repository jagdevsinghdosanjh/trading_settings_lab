import streamlit as st

def render_setting_learn(name):
    st.subheader(f"Learn: {name}")
    st.write("Reflection question:")
    st.text_area("Your thoughts", key=f"learn_{name}")
