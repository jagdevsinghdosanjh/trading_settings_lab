import pandas as pd
import numpy as np
import streamlit as st

_sample_data = None

def load_sample_data():
    global _sample_data
    if _sample_data is None:
        prices = [100,101,102,101,103,104,103,105]
        times = [f"10:{i:02d}" for i in range(len(prices))]
        rng = np.random.default_rng(42)
        spreads = 0.05 + rng.random(len(prices))*0.3
        _sample_data = pd.DataFrame({"time":times,"price":prices,"spread":spreads})
    return _sample_data

def init_market_state():
    if "current_bar" not in st.session_state:
        st.session_state.current_bar = 0
    if "market_data" not in st.session_state:
        st.session_state.market_data = load_sample_data()

def step_market(speed="1x"):
    steps = {"1x":1,"2x":2,"5x":5}
    step = steps.get(speed,1)
    max_idx = len(st.session_state.market_data)-1
    st.session_state.current_bar = min(st.session_state.current_bar + step, max_idx)
