import streamlit as st

def render_setting_adjust(name, key, current_value, is_numeric=False):
    st.subheader(f"Adjust: {name}")
    if is_numeric:
        return st.number_input(name, value=float(current_value))
    return st.checkbox(name, value=bool(current_value))

def render_profile_adjust(name, key, settings):
    st.subheader(f"Adjust: {name}")
    st.write("Profile settings placeholder.")
