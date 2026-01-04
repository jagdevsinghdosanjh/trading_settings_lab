import streamlit as st

def render_emotional_meter():
    st.subheader("Emotional Load")
    level = st.slider("How tense do you feel?", 1, 5, 2)

    if "emotional_log" not in st.session_state:
        st.session_state.emotional_log = []

    if st.button("Record Emotional State"):
        st.session_state.emotional_log.append(
            {"bar": st.session_state.current_bar, "level": level}
        )
        st.success("Recorded.")
