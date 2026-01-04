import streamlit as st

from components.setting_explain import render_setting_explain
from components.setting_adjust import render_setting_adjust
from components.setting_learn import render_setting_learn
from components.setting_examples import render_setting_examples
from logic.settings_manager import get_current_settings, update_setting

def main():
    st.title("Broker Settings")

    setting_choice = st.selectbox(
        "Choose a setting",
        ["Default Size", "Trigger Spread", "Stop-Loss Spread"],
    )

    settings = get_current_settings()

    if setting_choice == "Default Size":
        setting_key = "default_size"
        description = "Default trade quantity."
        metaphor = "Your default step size"
        numeric = True
    elif setting_choice == "Trigger Spread":
        setting_key = "trigger_spread"
        description = "Max spread allowed before blocking trades."
        metaphor = "How much chaos you allow"
        numeric = True
    else:
        setting_key = "stop_loss_spread"
        description = "Breathing room for your stop-loss."
        metaphor = "Your defensive buffer"
        numeric = True

    st.markdown("---")

    tab1, tab2, tab3, tab4 = st.tabs(["Explain", "Adjust", "Learn", "Examples"])

    with tab1:
        render_setting_explain(setting_choice, description, metaphor, "Affects risk and execution.")

    with tab2:
        new_value = render_setting_adjust(setting_choice, setting_key, settings.get(setting_key), is_numeric=numeric)
        if new_value != settings.get(setting_key):
            update_setting(setting_key, new_value)
            st.success("Updated.")

    with tab3:
        render_setting_learn(setting_choice)

    with tab4:
        render_setting_examples(setting_choice)

if __name__ == "__main__":
    main()
