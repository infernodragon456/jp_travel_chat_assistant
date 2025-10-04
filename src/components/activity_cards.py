import streamlit as st
import streamlit_shadcn_ui as ui
from src.components.utils import log_message
from src.components.parsers import sanitize_text, sanitize_url

def render_activity_card(activity):
    """Renders a rich card for a suggested activity."""
    log_message(f"Rendering activity card: {activity}")
    name = sanitize_text(activity.get('name', ''))
    desc = sanitize_text(activity.get('description', ''))
    rating = activity.get('rating', 'N/A')
    image = sanitize_url(activity.get('image'))
    link = sanitize_url(activity.get('link'))

    st.markdown(f"### {name}")
    if image:
        st.image(image, width=300)
    st.write(f"**Rating:** {rating}")
    st.write(desc)
    if link:
        st.markdown(f"[More Info]({link})")

    # Per-activity bookmark button (shadcn)
    btn_key = f"bookmark_{name}_{link or ''}"
    if ui.button("Bookmark", key=btn_key, variant="secondary"):
        if 'bookmarked_activities' not in st.session_state:
            st.session_state.bookmarked_activities = []
        st.session_state.bookmarked_activities.append({
            'name': name,
            'description': desc,
            'rating': rating,
            'image': image,
            'link': link,
        })
        ui.badge("Bookmarked", variant="success")
