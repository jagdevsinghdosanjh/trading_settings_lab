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
            st.markdown(f"### {badge.get('icon','ðŸ…')} {badge['name']}")
            st.write(badge.get("description",""))
            st.caption(badge.get("earned_reason",""))
