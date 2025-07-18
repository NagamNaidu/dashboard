import streamlit as st

EXCEL_PATH = r"C:\Users\chait\lyros project office management\Book1.xlsx"  # Updated path
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"
SENDER_EMAIL = "your_email@gmail.com"
APP_PASSWORD = "your_app_password"

def load_config():
    st.session_state['excel_path'] = EXCEL_PATH
    st.session_state['admin_username'] = ADMIN_USERNAME
    st.session_state['admin_password'] = ADMIN_PASSWORD
    st.session_state['sender_email'] = SENDER_EMAIL
    st.session_state['app_password'] = APP_PASSWORD