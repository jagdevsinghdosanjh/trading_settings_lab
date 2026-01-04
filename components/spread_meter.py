import streamlit as st

def render_spread_meter():
    st.subheader("Spread Meter")

    if "market_data" not in st.session_state or "current_bar" not in st.session_state:
        st.write("Spread not available yet.")
        return

    df = st.session_state.market_data
    idx = st.session_state.current_bar
    spread = float(df["spread"].iloc[idx])

    st.write(f"Current spread: {spread:.3f}")

    if spread < 0.15:
        st.success("Spread is low.")
    elif spread < 0.25:
        st.warning("Spread is moderate.")
    else:
        st.error("Spread is high.")
