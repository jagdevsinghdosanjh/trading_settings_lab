import streamlit as st
from logic.settings_manager import apply_preset

def main():
    st.title("Learning Lab")
    st.write("Explore settings in three categories.")

    preset = st.selectbox(
        "Apply a preset configuration",
        ["None", "Conservative", "Moderate", "Aggressive"],
    )
    if preset != "None":
        apply_preset(preset)
        st.success(f"Applied {preset} preset.")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Trading Settings")
        st.write("- Show Executions\n- Beep on Execution\n- Quick Trade Mode")
    with col2:
        st.subheader("Broker Settings")
        st.write("- Default Size\n- Trigger Spread\n- Stop-Loss Spread")
    with col3:
        st.subheader("Market Profile")
        st.write("- Profile Info\n- Privacy Preferences")

if __name__ == "__main__":
    main()
