import streamlit as st

from components.setting_explain import render_setting_explain
from components.setting_adjust import render_profile_adjust
from components.setting_learn import render_setting_learn
from components.setting_examples import render_setting_examples
from logic.settings_manager import get_current_settings

def main():
    st.title("Market Profile")

    setting_choice = st.selectbox(
        "Choose a setting",
        ["Profile Information", "Privacy Preferences"],
    )

    settings = get_current_settings()

    if setting_choice == "Profile Information":
        setting_key = "profile_info"
        description = "Your trading identity."
        metaphor = "Telling the platform who you are"
    else:
        setting_key = "privacy_preferences"
        description = "What you choose to share."
        metaphor = "Your privacy boundary"

    st.markdown("---")

    tab1, tab2, tab3, tab4 = st.tabs(["Explain", "Adjust", "Learn", "Examples"])

    with tab1:
        render_setting_explain(setting_choice, description, metaphor, "Influences platform behavior.")

    with tab2:
        render_profile_adjust(setting_choice, setting_key, settings)

    with tab3:
        render_setting_learn(setting_choice)

    with tab4:
        render_setting_examples(setting_choice)

if __name__ == "__main__":
    main()
