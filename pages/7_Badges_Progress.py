import streamlit as st
from components.badge_display import render_badge_grid
from logic.badge_engine import get_all_badges_for_user

def main():
    st.title("Badges & Progress")
    badges = get_all_badges_for_user("demo_student")
    render_badge_grid(badges)

if __name__ == "__main__":
    main()
