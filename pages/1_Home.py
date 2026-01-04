import streamlit as st
from components.profile_card import render_profile_card

def main():
    st.title("🏠 Home")
    st.write("Welcome to the Trading Settings Learning Lab.")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Start Learning")
        st.write("Explore how trading, broker, and profile settings shape your experience.")
    with col2:
        st.subheader("Jump to Simulation")
        st.write("Test your settings in a safe, simulated environment.")

    st.markdown("---")
    st.subheader("Your Profile")
    render_profile_card()

if __name__ == "__main__":
    main()
