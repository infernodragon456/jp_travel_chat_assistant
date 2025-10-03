import streamlit as st
from src.components.utils import log_message

def render_activity_card(activity):
    """Renders a rich card for a suggested activity."""
    log_message(f"Rendering activity card: {activity}")
    st.markdown(f"### {activity['name']}")
    if 'image' in activity:
        st.image(activity['image'], width=300)
    st.write(f"**Rating:** {activity.get('rating', 'N/A')}")
    st.write(activity['description'])
    if 'link' in activity:
        st.markdown(f"[More Info]({activity['link']})")
