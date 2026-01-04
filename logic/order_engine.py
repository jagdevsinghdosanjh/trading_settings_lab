import streamlit as st
from logic.market_engine import load_sample_data
from logic.badge_engine import evaluate_badges_after_event
from logic.risk_engine import register_trade_for_session

def _init_trade_state():
    if "trades" not in st.session_state:
        st.session_state.trades = []
    if "open_position" not in st.session_state:
        st.session_state.open_position = {
            "side":None,"size":0.0,"entry_price":None,"entry_bar":None,"stop_loss":None
        }

def get_current_price_and_spread():
    if "market_data" not in st.session_state:
        data = load_sample_data()
        return float(data["price"].iloc[0]), float(data["spread"].iloc[0])
    df = st.session_state.market_data
    idx = st.session_state.current_bar
    return float(df["price"].iloc[idx]), float(df["spread"].iloc[idx])

def place_order(side, size, settings):
    _init_trade_state()
    price, spread = get_current_price_and_spread()
    bar = st.session_state.current_bar

    trigger = float(settings.get("trigger_spread",0.5))
    if spread > trigger:
        st.session_state.last_execution_message = (
            f"Order blocked: spread {spread:.3f} > trigger {trigger:.3f}"
        )
        evaluate_badges_after_event("spread_block")
        return

    slippage = 0.3 * spread
    fill = price + slippage if side=="Buy" else price - slippage

    pos = st.session_state.open_position

    def compute_sl(entry, side):
        sl_spread = float(settings.get("stop_loss_spread",0.5))
        return entry - sl_spread if side=="Buy" else entry + sl_spread

    # Open new
    if pos["side"] is None or pos["size"]==0:
        sl = compute_sl(fill, side)
        st.session_state.open_position = {
            "side":side,"size":size,"entry_price":fill,"entry_bar":bar,"stop_loss":sl
        }
        st.session_state.trades.append({
            "type":"OPEN","bar":bar,"side":side,"size":size,"price":fill,
            "pnl":0.0,"reason":"Manual entry"
        })
        register_trade_for_session()
        st.session_state.last_execution_message = f"Opened {side} at {fill:.2f}"
        evaluate_badges_after_event("order_event")
        return

    # Add
    if pos["side"] == side:
        new_size = pos["size"] + size
        new_entry = (pos["entry_price"]*pos["size"] + fill*size)/new_size
        sl = compute_sl(new_entry, side)
        st.session_state.open_position.update({
            "size":new_size,"entry_price":new_entry,"stop_loss":sl
        })
        st.session_state.trades.append({
            "type":"ADD","bar":bar,"side":side,"size":size,"price":fill,
            "pnl":0.0,"reason":"Add"
        })
        register_trade_for_session()
        st.session_state.last_execution_message = f"Added to {side}"
        evaluate_badges_after_event("order_event")
        return

    # Close
    pnl = (fill - pos["entry_price"])*pos["size"] if pos["side"]=="Buy" else (pos["entry_price"] - fill)*pos["size"]
    st.session_state.trades.append({
        "type":"CLOSE","bar":bar,"side":side,"size":pos["size"],"price":fill,
        "pnl":pnl,"reason":"Manual exit"
    })
    register_trade_for_session()
    st.session_state.last_execution_message = f"Closed {pos['side']} PnL {pnl:.2f}"
    st.session_state.open_position = {"side":None,"size":0,"entry_price":None,"entry_bar":None,"stop_loss":None}
    evaluate_badges_after_event("order_event")
