import streamlit as st
from datetime import datetime
from utils import save_data

def update_salary(emp_id, status, updated_by, comment, excel_path):
    try:
        df = st.session_state.employee_data
        idx = df.index[df["Employee ID"] == emp_id].tolist()
        if idx:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            df.loc[idx[0], "SalaryCredited"] = status
            df.loc[idx[0], "LastSalaryUpdate"] = now
            df.loc[idx[0], "SalaryUpdatedBy"] = updated_by
            df.loc[idx[0], "UpdateComments"] = comment
           
            timeline_entry = f"\n{now}: Salary updated to {status} by {updated_by}"
            if comment:
                timeline_entry += f" | Comment: {comment}"
               
            df.loc[idx[0], "Timeline"] = str(df.loc[idx[0], "Timeline"]) + timeline_entry
            return save_data(df, excel_path)
        return False
    except Exception as e:
        st.error(f"Error updating salary: {str(e)}")
        return False

def salary_management():
    st.markdown("""
        <div class="card animate-fade">
            <div class="card-header">Salary Management</div>
            <div style="margin-top: 1rem;">
                <p>Update salary status below:</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
   
    excel_path = st.session_state.get('excel_path')

    for i, row in st.session_state.employee_data.iterrows():
        with st.expander(f"{row['Employee Name']}", expanded=False):
            cols = st.columns([2, 3, 2])
            with cols[0]:
                status = st.selectbox(
                    "Salary Status",
                    ["Yes", "No"],
                    index=0 if row['SalaryCredited'] == "Yes" else 1,
                    key=f"sal_select_{i}"
                )
            with cols[1]:
                comment = st.text_input("Comment", key=f"sal_comment_{i}")
            with cols[2]:
                if st.button("Update", key=f"sal_btn_{i}"):
                    if update_salary(row["Employee ID"], status,
                                   st.session_state.current_user, comment, excel_path):
                        st.success("Updated!")
                        st.rerun()