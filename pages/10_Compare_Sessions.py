import streamlit as st
from logic.reflection_engine import generate_session_narrative

def main():
    st.title("Compare Sessions")

    sessions = st.session_state.get("sessions", {})
    if len(sessions) < 2:
        st.write("Need at least two sessions.")
        return

    ids = sorted(sessions.keys())
    col1, col2 = st.columns(2)
    with col1:
        s1 = st.selectbox("Session A", ids)
    with col2:
        s2 = st.selectbox("Session B", ids)

    if s1 == s2:
        st.warning("Choose two different sessions.")
        return

    st.subheader("Session A Narrative")
    st.write(generate_session_narrative(s1))

    st.subheader("Session B Narrative")
    st.write(generate_session_narrative(s2))

if __name__ == "__main__":
    main()
