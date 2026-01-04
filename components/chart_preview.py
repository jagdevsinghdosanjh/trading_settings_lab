import streamlit as st
import pandas as pd

def render_chart_preview():
    st.subheader("Chart Preview")

    if "market_data" not in st.session_state or "current_bar" not in st.session_state:
        st.warning("Market not initialized yet.")
        return

    df = st.session_state.market_data.copy()
    idx = st.session_state.current_bar

    df_visible = df.iloc[: idx + 1].copy()

    df_visible["execution"] = 0.0
    if "trades" in st.session_state:
        for t in st.session_state.trades:
            bar = t["bar"]
            if bar <= idx and bar in df_visible.index:
                if t["type"] in ("OPEN", "ADD"):
                    df_visible.loc[bar, "execution"] = 1.0
                elif t["type"] == "CLOSE":
                    df_visible.loc[bar, "execution"] = -1.0

    st.line_chart(df_visible[["price", "execution"]])
    st.caption(f"Showing bars 0 â†’ {idx} of {len(df)-1}")
