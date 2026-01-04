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
