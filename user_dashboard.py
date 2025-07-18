import streamlit as st
from ui_components import create_card
from leave import leave_request_form
from datetime import datetime

def show_user_dashboard():
    try:
        df = st.session_state.employee_data
        user_data = df[df["Username"].str.lower() == st.session_state.current_user.lower()].iloc[0]
        st.session_state['user_data'] = user_data
       
        st.markdown(f"""
        <div class="main-container animate-fade">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem;">
                <div>
                    <h1 style="color: var(--primary); margin-bottom: 0.5rem;">Welcome, {user_data['Employee Name']}!</h1>
                    <p style="color: var(--dark); opacity: 0.8;">{datetime.now().strftime('%A, %B %d, %Y')}</p>
                </div>
                <div style="background: var(--accent); padding: 0.5rem 1rem; border-radius: 20px; color: white; font-weight: 600;">
                    EMPLOYEE PORTAL
                </div>
            </div>
        """, unsafe_allow_html=True)
       
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(create_card("Your Information",
        f"""<div style="margin-top: 1rem;">
            <p><strong>Employee ID:</strong> {user_data['Employee ID']}</p>
            <p><strong>Designation:</strong> {user_data['Designation']}</p>
            <p><strong>Department:</strong> {user_data['Department']}</p>
            <p><strong>Blood Group:</strong> {user_data['Blood Group']}</p>
            <p><strong>Joining Date:</strong> {user_data['Joining Date']}</p>
        </div>"""
        ), unsafe_allow_html=True)
       
        with col2:
            st.markdown(create_card("Contact Information",
        f"""<div style="margin-top: 1rem;">
            <p><strong>Email:</strong> {user_data['Email']}</p>
            <p><strong>Phone:</strong> {user_data['Phone']}</p>
            <p><strong>Username:</strong> {user_data['Username']}</p>
        </div>"""
        ), unsafe_allow_html=True)
       
        status_color = "var(--success)" if user_data['Attendance'] == "Present" else "var(--danger)" if user_data['Attendance'] == "Absent" else "var(--warning)"
        salary_color = "var(--success)" if user_data['SalaryCredited'] == "Yes" else "var(--danger)"
       
        st.markdown(create_card("Current Status",
        f"""<div style="margin-top: 1rem;">
            <p><strong>Attendance:</strong> <span style="color: {status_color}">{user_data['Attendance']}</span></p>
            <p><strong>Salary Status:</strong> <span style="color: {salary_color}">{user_data['SalaryCredited']}</span></p>
            <p><strong>Last Update:</strong> {user_data['LastAttendanceUpdate']}</p>
        </div>"""
        ), unsafe_allow_html=True)
       
        # Leave Request Card
        leave_request_form()
       
        # Timeline Card
        st.markdown(create_card("Your Activity Timeline", f"""
            <div style="margin-top: 1rem; height: 300px; overflow-y: auto;">
                <pre style="white-space: pre-wrap; font-family: inherit;">{user_data['Timeline']}</pre>
            </div>
        """, "400px"), unsafe_allow_html=True)
       
        st.markdown("</div>", unsafe_allow_html=True)  # Close main container
    except Exception as e:
        st.error(f"Error in user dashboard: {str(e)}")