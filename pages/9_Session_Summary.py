import streamlit as st
import pandas as pd
from logic.risk_engine import init_session_state
from logic.reflection_engine import generate_session_narrative, get_learning_objectives_for_session

def main():
    st.title("Session Summary")

    init_session_state()

    sessions = st.session_state.get("sessions", {})
    if not sessions:
        st.write("No sessions yet.")
        return

    ids = sorted(sessions.keys())
    sel = st.selectbox("Select a session", ids)

    st.subheader("Narrative")
    st.write(generate_session_narrative(sel))

    st.subheader("Learning Objectives")
    for obj in get_learning_objectives_for_session(sel):
        st.write(f"- {obj}")

    st.subheader("Trades")
    trades = st.session_state.get("trades", [])
    idxs = sessions[sel]["trades_indices"]
    if idxs:
        df = pd.DataFrame([trades[i] for i in idxs])
        st.dataframe(df)
    else:
        st.write("No trades.")

    st.subheader("Reflections")
    refs = st.session_state.get("reflections", [])
    r_idxs = sessions[sel]["reflections_indices"]
    if r_idxs:
        df = pd.DataFrame([refs[i] for i in r_idxs])
        st.dataframe(df)
    else:
        st.write("No reflections.")

    if "emotional_log" in st.session_state:
        st.subheader("Emotional Load Over Time")
        df = pd.DataFrame(st.session_state.emotional_log)
        if not df.empty:
            st.line_chart(df.set_index("bar"))

if __name__ == "__main__":
    main()
