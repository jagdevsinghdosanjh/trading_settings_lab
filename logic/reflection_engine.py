import streamlit as st
from logic.risk_engine import register_reflection_for_session

def save_reflection(user, context, text):
    if "reflections" not in st.session_state:
        st.session_state.reflections = []
    st.session_state.reflections.append({"user":user,"context":context,"text":text})
    register_reflection_for_session()

def get_prompt_for_last_event():
    msg = st.session_state.get("last_execution_message")
    if not msg:
        return None
    if "spread" in msg:
        return "Spread blocked your order. What does this teach you?"
    if "Stop-loss" in msg:
        return "Your stop-loss was hit. Was it too tight or too loose?"
    if "Opened" in msg:
        return "You opened a position. How confident were you?"
    if "Closed" in msg:
        return "You closed a position. What influenced your timing?"
    return "What did you notice about this event?"

def generate_session_narrative(session_id):
    sessions = st.session_state.get("sessions",{})
    if session_id not in sessions:
        return "No session data."
    trades = st.session_state.get("trades",[])
    idxs = sessions[session_id]["trades_indices"]
    if not idxs:
        return "You observed the market without trading."
    session_trades = [trades[i] for i in idxs]
    closes = [t for t in session_trades if t["type"]=="CLOSE"]
    pnl = sum(t["pnl"] for t in closes)
    return f"You placed {len(session_trades)} trades. Realized PnL: {pnl:.2f}"

def get_learning_objectives_for_session(session_id):
    import json, os
    path = os.path.join("data","learning_objectives.json")
    if not os.path.exists(path):
        return []
    with open(path) as f:
        obj = json.load(f)
    sessions = st.session_state.get("sessions",{})
    trades = st.session_state.get("trades",[])
    idxs = sessions[session_id]["trades_indices"]
    used = set()
    for i in idxs:
        r = trades[i].get("reason","").lower()
        if "spread" in r:
            used.add("trigger_spread")
        if "stop-loss" in r:
            used.add("stop_loss_spread")
    return [obj[k] for k in used if k in obj]
