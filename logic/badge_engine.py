import streamlit as st

def _ensure_badge_state():
    """Make sure earned_badges exists in session_state."""
    if "earned_badges" not in st.session_state:
        st.session_state.earned_badges = []

def get_all_badges_for_user(user_id):
    _ensure_badge_state()
    return st.session_state.earned_badges

def _award(name, icon, desc, reason):
    _ensure_badge_state()

    # Prevent duplicates
    for b in st.session_state.earned_badges:
        if b["name"] == name:
            return

    st.session_state.earned_badges.append({
        "name": name,
        "icon": icon,
        "description": desc,
        "earned_reason": reason,
    })

def evaluate_badges_after_event(event):
    _ensure_badge_state()

    settings = st.session_state.get("settings_snapshot_for_badges", {})
    trades = st.session_state.get("trades", [])

    if event == "spread_block":
        _award(
            "Spread Whisperer",
            "🌬️",
            "Recognized that high spread can block trades.",
            "Your order was blocked due to high spread."
        )

    if any(t["type"] in ("OPEN", "ADD", "CLOSE") for t in trades):
        _award(
            "Footprint Finder",
            "👣",
            "Left footprints on the chart.",
            "You placed trades in the simulation."
        )

    if settings.get("quick_trade_mode") is False:
        _award(
            "Pencil First",
            "✏️",
            "Chose to learn slowly before using quick trading.",
            "Quick Trade Mode was OFF while trading."
        )

# import streamlit as st

# def get_all_badges_for_user(user_id):
#     if "earned_badges" not in st.session_state:
#         st.session_state.earned_badges = []
#     return st.session_state.earned_badges

# def _award(name, icon, desc, reason):
#     for b in st.session_state.get("earned_badges",[]):
#         if b["name"]==name:
#             return
#     st.session_state.earned_badges.append({
#         "name":name,"icon":icon,"description":desc,"earned_reason":reason
#     })

# def evaluate_badges_after_event(event):
#     settings = st.session_state.get("settings_snapshot_for_badges",{})
#     trades = st.session_state.get("trades",[])

#     if event=="spread_block":
#         _award("Spread Whisperer","ðŸŒ¬ï¸","Understood spread impact","Spread blocked a trade")

#     if any(t["type"] in ("OPEN","ADD","CLOSE") for t in trades):
#         _award("Footprint Finder","ðŸ‘£","Left footprints on chart","Placed trades")

#     if settings.get("quick_trade_mode") is False:
#         _award("Pencil First","âœï¸","Learned slowly first","Quick trade mode off")
