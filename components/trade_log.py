import streamlit as st
import pandas as pd

def render_trade_log():
    if "trades" not in st.session_state or not st.session_state.trades:
        st.write("No trades yet.")
        return

    df = pd.DataFrame(st.session_state.trades)
    st.dataframe(df, use_container_width=True)
