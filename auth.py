import streamlit as st

def authenticate(username, password, admin_username, admin_password):
    try:
        if username == admin_username and password == admin_password:
            return "admin"
       
        df = st.session_state.employee_data
        if not df.empty:
            user_data = df[df["Username"].str.lower() == username.lower()]
            if not user_data.empty and user_data.iloc[0]["Password"] == password:
                return "user"
        return None
    except Exception as e:
        st.error(f"Authentication error: {str(e)}")
        return None