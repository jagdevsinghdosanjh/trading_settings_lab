# Rebuilds the logic folder for Trading Settings Learning Lab

$root = "logic"

# Ensure folder exists
if (!(Test-Path $root)) {
    New-Item -ItemType Directory -Path $root | Out-Null
}

# Create __init__.py
Set-Content "$root/__init__.py" "" -Encoding UTF8

# settings_manager.py
Set-Content "$root/settings_manager.py" @'
import streamlit as st

_settings = {
    "show_executions": True,
    "beep_on_execution": False,
    "quick_trade_mode": False,
    "default_size": 1.0,
    "trigger_spread": 0.2,
    "stop_loss_spread": 0.4,
    "profile_info": {"level": "Beginner", "style": "Explorer"},
    "privacy_preferences": {"share_usage_data": False},
}

def get_current_settings():
    return dict(_settings)

def update_setting(key, value):
    _settings[key] = value
    st.session_state.settings_snapshot_for_badges = dict(_settings)

def apply_preset(name):
    import json, os
    path = os.path.join("data", "presets.json")
    if not os.path.exists(path):
        return
    with open(path) as f:
        presets = json.load(f)
    preset = presets.get(name)
    if not preset:
        return
    for k, v in preset.items():
        _settings[k] = v
    st.session_state.settings_snapshot_for_badges = dict(_settings)
'@ -Encoding UTF8

# market_engine.py
Set-Content "$root/market_engine.py" @'
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
'@ -Encoding UTF8

# order_engine.py
Set-Content "$root/order_engine.py" @'
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
'@ -Encoding UTF8

# risk_engine.py
Set-Content "$root/risk_engine.py" @'
import streamlit as st
from logic.order_engine import get_current_price_and_spread

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
    price,_ = get_current_price_and_spread()
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
'@ -Encoding UTF8

# badge_engine.py
Set-Content "$root/badge_engine.py" @'
import streamlit as st

def get_all_badges_for_user(user_id):
    if "earned_badges" not in st.session_state:
        st.session_state.earned_badges = []
    return st.session_state.earned_badges

def _award(name, icon, desc, reason):
    for b in st.session_state.get("earned_badges",[]):
        if b["name"]==name:
            return
    st.session_state.earned_badges.append({
        "name":name,"icon":icon,"description":desc,"earned_reason":reason
    })

def evaluate_badges_after_event(event):
    settings = st.session_state.get("settings_snapshot_for_badges",{})
    trades = st.session_state.get("trades",[])

    if event=="spread_block":
        _award("Spread Whisperer","🌬️","Understood spread impact","Spread blocked a trade")

    if any(t["type"] in ("OPEN","ADD","CLOSE") for t in trades):
        _award("Footprint Finder","👣","Left footprints on chart","Placed trades")

    if settings.get("quick_trade_mode") is False:
        _award("Pencil First","✏️","Learned slowly first","Quick trade mode off")
'@ -Encoding UTF8

# reflection_engine.py
Set-Content "$root/reflection_engine.py" @'
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
'@ -Encoding UTF8

Write-Host "Logic folder rebuilt successfully." -ForegroundColor Green
