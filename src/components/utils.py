import streamlit as st

def log_message(message):
    """Utility function to log messages for debugging.

    Debug output is currently disabled. To re-enable, restore the st.write line below.
    """
    # if isinstance(message, (dict, list)):
    #     import json
    #     log_str = json.dumps(message, indent=2, ensure_ascii=False)
    # else:
    #     log_str = repr(message)
    # st.write(f"Debug: {log_str}")
    return
