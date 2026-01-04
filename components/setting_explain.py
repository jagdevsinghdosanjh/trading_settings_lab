import streamlit as st

def render_setting_explain(name, desc, metaphor, why):
    st.subheader(name)
    st.write(desc)
    st.info(f"Metaphor: {metaphor}")
    st.write(f"Why it matters: {why}")
