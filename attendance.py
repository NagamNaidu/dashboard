import streamlit as st
from datetime import datetime
from utils import save_data

def mark_attendance(emp_id, status, updated_by, comment, excel_path):
    try:
        df = st.session_state.employee_data
        idx = df.index[df["Employee ID"] == emp_id].tolist()
        if idx:
            now = datetime.now()
            timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
            day = now.strftime("%A")
            df.loc[idx[0], "Attendance"] = status
            df.loc[idx[0], "LastAttendanceUpdate"] = f"{timestamp} ({day})"
            df.loc[idx[0], "AttendanceUpdatedBy"] = updated_by
            df.loc[idx[0], "UpdateComments"] = comment
           
            timeline_entry = f"\n{timestamp}: Attendance marked as {status} by {updated_by}"
            if comment:
                timeline_entry += f" | Comment: {comment}"
               
            df.loc[idx[0], "Timeline"] = str(df.loc[idx[0], "Timeline"]) + timeline_entry
            return save_data(df, excel_path)
        return False
    except Exception as e:
        st.error(f"Error marking attendance: {str(e)}")
        return False

def attendance_management():
    st.markdown("""
        <div class="card animate-fade">
            <div class="card-header">Attendance Management</div>
            <div style="margin-top: 1rem;">
                <p>Update employee attendance status below:</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
   
    excel_path = st.session_state.get('excel_path')

    for i, row in st.session_state.employee_data.iterrows():
        with st.expander(f"{row['Employee Name']} (ID: {row['Employee ID']})", expanded=False):
            cols = st.columns([2, 3, 2])
            with cols[0]:
                status = st.selectbox(
                    "Status",
                    ["Present", "Absent", "On Leave"],
                    index=0 if row['Attendance'] == "Present" else 1 if row['Attendance'] == "Absent" else 2,
                    key=f"att_select_{i}"
                )
            with cols[1]:
                comment = st.text_input("Comment", key=f"att_comment_{i}")
            with cols[2]:
                if st.button("Update", key=f"att_btn_{i}"):
                    if mark_attendance(row["Employee ID"], status,
                                     st.session_state.current_user, comment, excel_path):
                        st.success("Updated!")
                        st.rerun()