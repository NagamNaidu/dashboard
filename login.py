import streamlit as st
from auth import authenticate

def show_login():
    st.markdown("""
    <div style="display: flex; justify-content: center; align-items: center; height: 100vh;">
        <div class="card" style="width: 400px; padding: 2rem; text-align: center;">
            <h1 style="color: var(--primary); margin-bottom: 1.5rem;">Lyros Office</h1>
            <p style="color: var(--dark); margin-bottom: 2rem;">Management Dashboard</p>
    """, unsafe_allow_html=True)
   
    admin_username = st.session_state.get('admin_username')
    admin_password = st.session_state.get('admin_password')

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
       
        if st.form_submit_button("Login"):
            auth_result = authenticate(username, password, admin_username, admin_password)
            if auth_result:
                st.session_state.current_user = username
                st.session_state.user_role = auth_result
                st.rerun()
            else:
                st.error("Invalid username or password")
   
    st.markdown("""
        <div class="auth-switch" onclick="window.streamlit.setComponentValue('signup')">
            New employee? Sign up here
        </div>
    """, unsafe_allow_html=True)
   
    st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)