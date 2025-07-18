import pandas as pd
import streamlit as st
from datetime import datetime
from utils import save_data, send_email

def add_new_employee(employee_data, excel_path, sender_email, app_password):
    try:
        df = st.session_state.employee_data
       
        # Check if employee ID already exists
        if employee_data["Employee ID"] in df["Employee ID"].values:
            st.error("Employee ID already exists!")
            return False
           
        # Create new row as dictionary
        new_row = {
            'Employee Name': employee_data["Employee Name"],
            'Employee ID': employee_data["Employee ID"],
            'Username': employee_data["Username"],
            'Password': employee_data["Password"],
            'Email': employee_data["Email"],
            'Phone': employee_data["Phone"],
            'Designation': employee_data["Designation"],
            'Department': employee_data["Department"],
            'Blood Group': employee_data["Blood Group"],
            'Joining Date': employee_data["Joining Date"],
            'Attendance': 'Absent',
            'LastAttendanceUpdate': '',
            'LeaveStatus': '',
            'LeaveStart': '',
            'LeaveEnd': '',
            'SalaryCredited': 'No',
            'LastSalaryUpdate': '',
            'Role': 'user',
            'AttendanceUpdatedBy': '',
            'SalaryUpdatedBy': '',
            'UpdateComments': '',
            'AdminComments': '',
            'Timeline': f"\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: New employee added by {st.session_state.current_user}"
        }
       
        # Append new row to dataframe
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
       
        # Save data
        if save_data(df, excel_path):
            # Send welcome email
            send_email(
                employee_data["Email"],
                "Welcome to Lyros Office",
                f"Hi {employee_data['Employee Name']},\n\n"
                f"Your account has been created successfully!\n"
                f"Username: {employee_data['Username']}\n"
                f"Password: {employee_data['Password']}\n\n"
                f"Regards,\nLyros Admin Team", sender_email, app_password
            )
            return True
        return False
    except Exception as e:
        st.error(f"Error adding new employee: {str(e)}")
        return False

def add_new_employee_form():
    st.markdown("""
        <div class="card animate-fade">
            <div class="card-header">Add New Employee</div>
            <div style="margin-top: 1rem;">
                <p>Fill in the details below to add a new employee:</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
   
    excel_path = st.session_state.get('excel_path')
    sender_email = st.session_state.get('sender_email')
    app_password = st.session_state.get('app_password')

    with st.form("add_employee_form"):
        col1, col2 = st.columns(2)
        with col1:
            emp_name = st.text_input("Full Name", key="new_emp_name")
            emp_id = st.text_input("Employee ID", key="new_emp_id")
            username = st.text_input("Username", key="new_username")
            password = st.text_input("Password", type="password", key="new_password")
            email = st.text_input("Email", key="new_email")
        with col2:
            phone = st.text_input("Phone Number", key="new_phone")
            designation = st.text_input("Designation", key="new_designation")
            department = st.text_input("Department", key="new_department")
            blood_group = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"], key="new_blood_group")
            joining_date = st.date_input("Joining Date", key="new_joining_date")
       
        if st.form_submit_button("Add Employee"):
            if not all([emp_name, emp_id, username, password, email, phone]):
                st.error("Please fill all required fields!")
            else:
                employee_data = {
                    "Employee Name": emp_name,
                    "Employee ID": emp_id,
                    "Username": username,
                    "Password": password,
                    "Email": email,
                    "Phone": phone,
                    "Designation": designation,
                    "Department": department,
                    "Blood Group": blood_group,
                    "Joining Date": joining_date.strftime("%Y-%m-%d")
                }
               
                if add_new_employee(employee_data, excel_path, sender_email, app_password):
                    st.success("Employee added successfully!")
                    st.rerun()
                else:
                    st.error("Failed to add employee")