import streamlit as st
import pandas as pd

def main():
    st.title("Teacher Dashboard")

    sessions = st.session_state.get("sessions", {})
    trades = st.session_state.get("trades", [])
    reflections = st.session_state.get("reflections", [])

    st.subheader("Summary")
    st.metric("Total Sessions", len(sessions))
    st.metric("Total Trades", len(trades))
    st.metric("Total Reflections", len(reflections))

    spread_blocks = sum(1 for t in trades if "spread" in t.get("reason","").lower())
    sl_hits = sum(1 for t in trades if "stop-loss" in t.get("reason","").lower())

    st.metric("Spread Blocks", spread_blocks)
    st.metric("Stop-Loss Hits", sl_hits)

    st.subheader("Reflection Themes")
    themes = {"fear":0,"confidence":0,"spread":0,"stop-loss":0,"mistake":0}
    for r in reflections:
        text = r.get("text","").lower()
        for k in themes:
            if k in text:
                themes[k]+=1

    df = pd.DataFrame.from_dict(themes, orient="index", columns=["count"])
    st.bar_chart(df)

if __name__ == "__main__":
    main()
