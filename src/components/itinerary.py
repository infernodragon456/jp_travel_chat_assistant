import streamlit as st
from icalendar import Calendar, Event
from datetime import datetime
from src.components.utils import log_message

def build_itinerary(activities):
    """Builds and exports itinerary."""
    log_message(f"Building itinerary: {activities}")
    if 'itinerary' not in st.session_state:
        st.session_state.itinerary = []
    
    for act in activities:
        if st.checkbox(f"Add {act['name']} to itinerary"):
            st.session_state.itinerary.append(act)
    
    if st.button("Export Itinerary"):
        cal = Calendar()
        for act in st.session_state.itinerary:
            event = Event()
            event.add('summary', act['name'])
            event.add('dtstart', datetime.now())
            cal.add_component(event)
        with open('itinerary.ics', 'wb') as f:
            f.write(cal.to_ical())
        st.download_button("Download ICS", 'itinerary.ics')
