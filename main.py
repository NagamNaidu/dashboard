import streamlit as st
from ui_components import inject_css

from utils import load_data
from login import show_login
from signup import show_signup
from admin_dashboard import show_admin
from user_dashboard import show_user_dashboard

def main():
    # Inject CSS
    inject_css()
   
    # Initialize session state
    from config import load_config
    load_config()
    if 'employee_data' not in st.session_state:
        EXCEL_PATH = st.session_state.get('excel_path')
        st.session_state.employee_data = load_data(EXCEL_PATH)
   
    # Check if we should show signup instead of login
    if 'show_signup' not in st.session_state:
        st.session_state.show_signup = False
   
    # Handle switching between login and signup
    if st.session_state.get('show_signup'):
        show_signup()
    else:
        # Authentication flow
        if 'current_user' not in st.session_state:
            show_login()
        else:
            if st.session_state.user_role == "admin":
                show_admin()
            else:
               show_user_dashboard()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
        st.stop()

# Handle switching between login/signup
if "streamlit" in globals():
    streamlit.setComponentValue = handle_auth_switch