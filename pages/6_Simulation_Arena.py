import streamlit as st

from components.chart_preview import render_chart_preview
from components.trade_log import render_trade_log
from components.spread_meter import render_spread_meter
from components.emotional_meter import render_emotional_meter
from logic.market_engine import init_market_state, step_market
from logic.order_engine import place_order
from logic.risk_engine import get_risk_summary, check_stop_loss_hit, init_session_state
from logic.settings_manager import get_current_settings
from logic.reflection_engine import get_prompt_for_last_event, save_reflection

def main():
    st.title("Simulation Arena")

    init_market_state()
    init_session_state()

    settings = get_current_settings()
    with st.expander("Current Settings"):
        st.json(settings)

    col1, col2, col3 = st.columns([1,2,1])

    with col1:
        st.subheader("Controls")
        speed = st.selectbox("Playback speed", ["1x","2x","5x"])

        if st.button("Step Market"):
            step_market(speed)
            check_stop_loss_hit()
            st.success("Advanced.")

        st.markdown("---")
        st.subheader("Place Trade")
        side = st.radio("Side", ["Buy","Sell"])
        size = st.number_input("Size", min_value=0.1, value=float(settings.get("default_size",1.0)))
        if st.button("Submit Order"):
            place_order(side, size, settings)
            st.success("Order submitted.")

        st.markdown("---")
        st.subheader("Session Control")
        st.write(f"Current session: {st.session_state.current_session_id}")
        if st.button("End Session and Start New"):
            st.session_state.current_session_id += 1
            st.success(f"Started Session {st.session_state.current_session_id}")

        st.markdown("---")
        st.subheader("Current Bar")
        st.write(st.session_state.current_bar)

    with col2:
        render_chart_preview()

    with col3:
        render_spread_meter()
        st.markdown("---")
        render_emotional_meter()
        st.markdown("---")
        st.subheader("Risk Summary")
        st.json(get_risk_summary())

    st.markdown("---")
    st.subheader("Trade Log")
    render_trade_log()

    if "last_execution_message" in st.session_state:
        st.info(f"Event: {st.session_state.last_execution_message}")
        prompt = get_prompt_for_last_event()
        if prompt:
            st.markdown("### Reflection")
            st.write(prompt)
            txt = st.text_area("Your thoughts", key="event_reflection")
            if st.button("Save Reflection"):
                save_reflection("demo_student", st.session_state.last_execution_message, txt)
                st.success("Reflection saved.")

if __name__ == "__main__":
    main()
