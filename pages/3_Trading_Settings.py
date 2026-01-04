import streamlit as st

from components.setting_explain import render_setting_explain
from components.setting_adjust import render_setting_adjust
from components.setting_learn import render_setting_learn
from components.setting_examples import render_setting_examples
from logic.settings_manager import get_current_settings, update_setting

def main():
    st.title("Trading Settings")

    setting_choice = st.selectbox(
        "Choose a setting",
        ["Show Executions", "Beep on Execution", "Quick Trade Mode"],
    )

    settings = get_current_settings()

    if setting_choice == "Show Executions":
        setting_key = "show_executions"
        metaphor = "Footprints on the path"
        description = "Show markers where trades were executed."
    elif setting_choice == "Beep on Execution":
        setting_key = "beep_on_execution"
        metaphor = "A bell during important moments"
        description = "Play a sound when an order fills."
    else:
        setting_key = "quick_trade_mode"
        metaphor = "Permanent marker instead of pencil"
        description = "Enable one-click trading."

    st.markdown("---")

    tab1, tab2, tab3, tab4 = st.tabs(["Explain", "Adjust", "Learn", "Examples"])

    with tab1:
        render_setting_explain(setting_choice, description, metaphor, "Helps shape your trading behavior.")

    with tab2:
        new_value = render_setting_adjust(setting_choice, setting_key, settings.get(setting_key))
        if new_value != settings.get(setting_key):
            update_setting(setting_key, new_value)
            st.success("Updated.")

    with tab3:
        render_setting_learn(setting_choice)

    with tab4:
        render_setting_examples(setting_choice)

if __name__ == "__main__":
    main()
