import streamlit as st
def _get_current_price_and_spread():
    df = st.session_state.market_data
    idx = st.session_state.current_bar
    return float(df["price"].iloc[idx]), float(df["spread"].iloc[idx])

def get_risk_summary():
    trades = st.session_state.get("trades",[])
    realized = sum(t["pnl"] for t in trades if t["type"]=="CLOSE")
    pos = st.session_state.get("open_position",{})
    open_pos = 1 if pos and pos.get("size",0)>0 else 0
    return {"open_positions":open_pos,"realized_pnl":realized,"max_drawdown":0.0}

def check_stop_loss_hit():
    pos = st.session_state.get("open_position",{})
    if not pos or pos["side"] is None:
        return
    price,_ = _get_current_price_and_spread()
    bar = st.session_state.current_bar
    sl = pos["stop_loss"]
    hit = (pos["side"]=="Buy" and price<=sl) or (pos["side"]=="Sell" and price>=sl)
    if not hit:
        return
    pnl = (sl - pos["entry_price"])*pos["size"] if pos["side"]=="Buy" else (pos["entry_price"] - sl)*pos["size"]
    st.session_state.trades.append({
        "type":"CLOSE","bar":bar,"side":pos["side"],"size":pos["size"],
        "price":sl,"pnl":pnl,"reason":"Stop-loss hit"
    })
    from logic.badge_engine import evaluate_badges_after_event
    register_trade_for_session()
    st.session_state.last_execution_message = f"Stop-loss hit PnL {pnl:.2f}"
    st.session_state.open_position = {"side":None,"size":0,"entry_price":None,"entry_bar":None,"stop_loss":None}
    evaluate_badges_after_event("sl_hit")

def init_session_state():
    if "current_session_id" not in st.session_state:
        st.session_state.current_session_id = 1
    if "sessions" not in st.session_state:
        st.session_state.sessions = {}
    sid = st.session_state.current_session_id
    if sid not in st.session_state.sessions:
        st.session_state.sessions[sid] = {"trades_indices":[], "reflections_indices":[]}

def register_trade_for_session():
    sid = st.session_state.current_session_id
    idx = len(st.session_state.get("trades",[])) - 1
    st.session_state.sessions[sid]["trades_indices"].append(idx)

def register_reflection_for_session():
    sid = st.session_state.current_session_id
    idx = len(st.session_state.get("reflections",[])) - 1
    st.session_state.sessions[sid]["reflections_indices"].append(idx)
