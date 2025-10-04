import streamlit as st
from icalendar import Calendar, Event
from datetime import datetime
from src.components.utils import log_message
import streamlit_shadcn_ui as ui

def build_itinerary(activities):
    """Builds and exports itinerary."""
    log_message(f"Building itinerary: {activities}")
    if 'itinerary' not in st.session_state:
        st.session_state.itinerary = []
    
    for i, act in enumerate(activities):
        if st.checkbox(f"Add {act['name']} to itinerary", key=f"itinerary_checkbox_{i}"):
            st.session_state.itinerary.append(act)
    
    # Date picker
    selected_date = st.date_input("Select date for events")

    if ui.button("Export Itinerary", key="export_ics_btn", variant="primary"):
        cal = Calendar()
        for act in st.session_state.itinerary:
            event = Event()
            event.add('summary', act['name'])
            # Use selected date at current time
            event.add('dtstart', datetime.combine(selected_date, datetime.now().time()))
            cal.add_component(event)
        import io
        buffer = io.BytesIO()
        buffer.write(cal.to_ical())
        buffer.seek(0)
        st.download_button("Download ICS", buffer, file_name="itinerary.ics", mime="text/calendar")
