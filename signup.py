import streamlit as st
from new_employee import add_new_employee
from utils import send_email

def show_signup():
    st.markdown("""
    <div style="display: flex; justify-content: center; align-items: center; height: 100vh;">
        <div class="card" style="width: 500px; padding: 2rem; text-align: center;">
            <h1 style="color: var(--primary); margin-bottom: 1.5rem;">Employee Sign Up</h1>
            <p style="color: var(--dark); margin-bottom: 2rem;">Fill in your details to create an account</p>
    """, unsafe_allow_html=True)
   
    excel_path = st.session_state.get('excel_path')
    sender_email = st.session_state.get('sender_email')
    app_password = st.session_state.get('app_password')

    with st.form("signup_form"):
        col1, col2 = st.columns(2)
        with col1:
            emp_name = st.text_input("Full Name", key="signup_name")
            emp_id = st.text_input("Employee ID", key="signup_id")
            email = st.text_input("Email", key="signup_email")
        with col2:
            phone = st.text_input("Phone Number", key="signup_phone")
            password = st.text_input("Password", type="password", key="signup_password")
            confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm_password")
       
        designation = st.text_input("Designation", key="signup_designation")
        department = st.text_input("Department", key="signup_department")
        blood_group = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"], key="signup_blood_group")
        joining_date = st.date_input("Joining Date", key="signup_joining_date")
       
        if st.form_submit_button("Sign Up"):
            if not all([emp_name, emp_id, email, phone, password, confirm_password]):
                st.error("Please fill all required fields!")
            elif password != confirm_password:
                st.error("Passwords don't match!")
            else:
                # Check if employee ID already exists
                df = st.session_state.employee_data
                if emp_id in df["Employee ID"].values:
                    st.error("Employee ID already exists!")
                else:
                    # Create new employee
                    employee_data = {
                        "Employee Name": emp_name,
                        "Employee ID": emp_id,
                        "Username": email.split('@')[0],  # Use email prefix as username
                        "Password": password,
                        "Email": email,
                        "Phone": phone,
                        "Designation": designation,
                        "Department": department,
                        "Blood Group": blood_group,
                        "Joining Date": joining_date.strftime("%Y-%m-%d")
                    }
                   
                    if add_new_employee(employee_data, excel_path, sender_email, app_password):
                        st.success("Account created successfully! Please login.")
                        st.session_state.show_signup = False
                        st.rerun()
                    else:
                        st.error("Failed to create account")
   
    st.markdown("""
        <div class="auth-switch" onclick="window.streamlit.setComponentValue('login')">
            Already have an account? Login here
        </div>
    """, unsafe_allow_html=True)
   
    st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)