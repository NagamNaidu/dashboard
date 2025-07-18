import streamlit as st
import pandas as pd
import os
import yagmail
from datetime import datetime

def load_data(excel_path):
    try:
        if os.path.exists(excel_path):
            df = pd.read_excel(excel_path, engine='openpyxl')
        else:
            df = pd.DataFrame(columns=[
                'Employee Name', "Employee ID", 'Username', 'Password', 'Email', 'Phone',
                'Designation', 'Department', 'Blood Group', 'Joining Date',
                'Attendance', 'LastAttendanceUpdate', 'LeaveStatus', 'LeaveStart',
                'LeaveEnd', 'SalaryCredited', 'LastSalaryUpdate', 'Role',
                'AttendanceUpdatedBy', 'SalaryUpdatedBy', 'UpdateComments',
                'AdminComments', 'Timeline'
            ])
       
        required_columns = {
            'Employee Name': '', "Employee ID": '', 'Username': '', 'Password': '',
            'Email': '', 'Phone': '', 'Designation': '', 'Department': '',
            'Blood Group': '', 'Joining Date': '',
            'Attendance': 'Absent', 'LastAttendanceUpdate': '',
            'LeaveStatus': '', 'LeaveStart': '', 'LeaveEnd': '', 'SalaryCredited': 'No',
            'LastSalaryUpdate': '', 'Role': 'user', 'AttendanceUpdatedBy': '',
            'SalaryUpdatedBy': '', 'UpdateComments': '', 'AdminComments': '', 'Timeline': ''
        }
       
        for col, default in required_columns.items():
            if col not in df.columns:
                df[col] = default
       
        if df['Username'].isnull().all():
            df['Username'] = df['Employee Name'].str.split().str[0].str.lower() + df['Employee ID'].astype(str)
       
        return df
   
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame()

def save_data(df, excel_path):
    try:
        df.to_excel(excel_path, index=False, engine='openpyxl')
        st.session_state.employee_data = df  # Update session state
        return True
    except Exception as e:
        st.error(f"Error saving data: {str(e)}")
        return False

def send_email(to_email, subject, body, sender_email, app_password):
    try:
        if not sender_email or not app_password:
            st.warning("Email credentials not configured - skipping email send")
            return True
           
        yag = yagmail.SMTP(sender_email, app_password)
        yag.send(to=to_email, subject=subject, contents=body)
        return True
    except Exception as e:
        st.error(f"Failed to send email: {str(e)}")
        return False

def apply_leave(emp_id, start, end, reason, excel_path, sender_email, app_password):
    try:
        df = st.session_state.employee_data
        idx = df.index[df["Employee ID"] == emp_id].tolist()
        if idx:
            df.loc[idx[0], ["LeaveStatus", "LeaveStart", "LeaveEnd", "Attendance"]] = [reason, start, end, "On Leave"]
            email = df.loc[idx[0], 'Email']
            name = df.loc[idx[0], 'Employee Name']
           
            send_email(email, "Leave Approved",
                      f"Hi {name},\n\nYour leave has been approved from {start} to {end}.\nReason: {reason}\n\nRegards,\nLyros Admin", sender_email, app_password)
           
            timeline_entry = f"\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Leave approved from {start} to {end} | Reason: {reason}"
            df.loc[idx[0], "Timeline"] = str(df.loc[idx[0], "Timeline"]) + timeline_entry
            return save_data(df, excel_path)
        return False
    except Exception as e:
        st.error(f"Error applying leave: {str(e)}")
        return False