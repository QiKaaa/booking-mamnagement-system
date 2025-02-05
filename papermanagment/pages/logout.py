import streamlit as st
from menu import menu_with_redirect

# Redirect to app.py if not logged in, otherwise show the navigation menu
menu_with_redirect()

st.session_state['user_name'] = 'Guest'
st.session_state["role"] = None
st.cache_data.clear()
st.switch_page('./app.py')
