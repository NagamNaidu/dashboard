import streamlit as st
from utils import apply_leave

def leave_request_form():
    st.markdown("""
        <div class="card animate-fade">
            <div class="card-header">Leave Request</div>
            <div style="margin-top: 1rem;">
                <p>Submit a leave request below:</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    user_data = st.session_state.get('user_data')
    excel_path = st.session_state.get('excel_path')
    sender_email = st.session_state.get('sender_email')
    app_password = st.session_state.get('app_password')

    with st.form("leave_form"):
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date")
        with col2:
            end_date = st.date_input("End Date")

        reason = st.text_area("Reason for Leave")

        if st.form_submit_button("Submit Leave Request"):
            if apply_leave(user_data["Employee ID"], start_date, end_date, reason, excel_path, sender_email, app_password):
                st.success("Leave request submitted!")
                st.rerun()
            else:
                st.error("Failed to submit leave request")