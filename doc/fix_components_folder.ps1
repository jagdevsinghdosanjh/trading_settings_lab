# Rebuilds the components folder for Trading Settings Learning Lab

$root = "components"

# Ensure folder exists
if (!(Test-Path $root)) {
    New-Item -ItemType Directory -Path $root | Out-Null
}

# Create __init__.py
Set-Content "$root/__init__.py" "" -Encoding UTF8

# profile_card.py
Set-Content "$root/profile_card.py" @'
import streamlit as st

def render_profile_card():
    st.markdown("#### Student Profile")
    st.write("Name: Demo Student")
    st.write("Level: Beginner")
    st.write("Style: Explorer")
'@ -Encoding UTF8

# setting_explain.py
Set-Content "$root/setting_explain.py" @'
import streamlit as st

def render_setting_explain(name, desc, metaphor, why):
    st.subheader(name)
    st.write(desc)
    st.info(f"Metaphor: {metaphor}")
    st.write(f"Why it matters: {why}")
'@ -Encoding UTF8

# setting_adjust.py
Set-Content "$root/setting_adjust.py" @'
import streamlit as st

def render_setting_adjust(name, key, current_value, is_numeric=False):
    st.subheader(f"Adjust: {name}")
    if is_numeric:
        return st.number_input(name, value=float(current_value))
    return st.checkbox(name, value=bool(current_value))

def render_profile_adjust(name, key, settings):
    st.subheader(f"Adjust: {name}")
    st.write("Profile settings placeholder.")
'@ -Encoding UTF8

# setting_learn.py
Set-Content "$root/setting_learn.py" @'
import streamlit as st

def render_setting_learn(name):
    st.subheader(f"Learn: {name}")
    st.write("Reflection question:")
    st.text_area("Your thoughts", key=f"learn_{name}")
'@ -Encoding UTF8

# setting_examples.py
Set-Content "$root/setting_examples.py" @'
import streamlit as st

def render_setting_examples(name):
    st.subheader(f"Examples: {name}")
    st.write("Add before/after images or explanations here.")
'@ -Encoding UTF8

# chart_preview.py
Set-Content "$root/chart_preview.py" @'
import streamlit as st
import pandas as pd

def render_chart_preview():
    st.subheader("Chart Preview")

    if "market_data" not in st.session_state or "current_bar" not in st.session_state:
        st.warning("Market not initialized yet.")
        return

    df = st.session_state.market_data.copy()
    idx = st.session_state.current_bar

    df_visible = df.iloc[: idx + 1].copy()

    df_visible["execution"] = 0.0
    if "trades" in st.session_state:
        for t in st.session_state.trades:
            bar = t["bar"]
            if bar <= idx and bar in df_visible.index:
                if t["type"] in ("OPEN", "ADD"):
                    df_visible.loc[bar, "execution"] = 1.0
                elif t["type"] == "CLOSE":
                    df_visible.loc[bar, "execution"] = -1.0

    st.line_chart(df_visible[["price", "execution"]])
    st.caption(f"Showing bars 0 → {idx} of {len(df)-1}")
'@ -Encoding UTF8

# trade_log.py
Set-Content "$root/trade_log.py" @'
import streamlit as st
import pandas as pd

def render_trade_log():
    if "trades" not in st.session_state or not st.session_state.trades:
        st.write("No trades yet.")
        return

    df = pd.DataFrame(st.session_state.trades)
    st.dataframe(df, width='stretch')
'@ -Encoding UTF8

# spread_meter.py
Set-Content "$root/spread_meter.py" @'
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
'@ -Encoding UTF8

# emotional_meter.py
Set-Content "$root/emotional_meter.py" @'
import streamlit as st

def render_emotional_meter():
    st.subheader("Emotional Load")
    level = st.slider("How tense do you feel?", 1, 5, 2)

    if "emotional_log" not in st.session_state:
        st.session_state.emotional_log = []

    if st.button("Record Emotional State"):
        st.session_state.emotional_log.append(
            {"bar": st.session_state.current_bar, "level": level}
        )
        st.success("Recorded.")
'@ -Encoding UTF8

# badge_display.py
Set-Content "$root/badge_display.py" @'
import streamlit as st

def render_badge_grid(badges):
    st.subheader("Your Badges")
    if not badges:
        st.write("No badges yet.")
        return

    cols = st.columns(3)
    for i, badge in enumerate(badges):
        col = cols[i % 3]
        with col:
            st.markdown(f"### {badge.get('icon','🏅')} {badge['name']}")
            st.write(badge.get("description",""))
            st.caption(badge.get("earned_reason",""))
'@ -Encoding UTF8

Write-Host "Components folder rebuilt successfully." -ForegroundColor Green
