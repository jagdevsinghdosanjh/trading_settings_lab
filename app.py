import streamlit as st
from components.profile_card import render_profile_card
from logic.settings_manager import get_current_settings

def main():
    st.set_page_config(
        page_title="Trading Settings Learning Lab",
        page_icon="ðŸ“˜",
        layout="wide",
    )

    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("Trading Settings Learning Lab")
        st.caption("Learn how your trading environment shapes your decisions.")
    with col2:
        render_profile_card()

    st.markdown("---")

    st.subheader("Welcome")
    st.write(
        "Use the left sidebar or the pages menu to navigate between the Learning Lab, "
        "Simulation Arena, Badges & Progress, Session Summary, and Teacher Dashboard."
    )

    settings = get_current_settings()
    with st.expander("Current Settings Snapshot"):
        st.json(settings)

    st.info(
        "Tip: Start with the Learning Lab pages to understand each setting "
        "before entering the Simulation Arena."
    )

if __name__ == "__main__":
    main()
