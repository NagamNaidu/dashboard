import streamlit as st
import pandas as pd
from io import BytesIO
from fpdf import FPDF
from fpdf.enums import XPos, YPos

def export_report(filter_column, filter_value):
    try:
        df = st.session_state.employee_data
        filtered = df[df[filter_column] == filter_value]
        towrite = BytesIO()
        filtered.to_excel(towrite, index=False, engine='openpyxl')
        towrite.seek(0)
        return towrite
    except Exception as e:
        st.error(f"Error exporting report: {str(e)}")
        return BytesIO()

def export_pdf():
    try:
        df = st.session_state.employee_data
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("helvetica", size=12)
        pdf.cell(200, 10, text="Lyros Employee Report", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
        pdf.ln(10)
       
        for _, row in df.iterrows():
            pdf.cell(200, 10,
                    text=f'Employee: {row["Employee Name"]} | ID: {row["Employee ID"]} | Status: {row["Attendance"]} | Salary: {row["SalaryCredited"]}',
                    new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.cell(200, 10, text=f"Last Update: {row['LastAttendanceUpdate']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.ln(5)
       
        b = BytesIO()
        pdf.output(b)
        b.seek(0)
        return b
    except Exception as e:
        st.error(f"Error generating PDF: {str(e)}")
        return BytesIO()

def show_reports():
    from ui_components import create_card
    st.markdown(create_card("Generate Reports",
    """
    <div style="margin-top: 1rem;">
        <p>Select report type and download:</p>
    </div>
        """
        ), unsafe_allow_html=True)
   
    report_type = st.selectbox("Select Report Type", [
        "All Employees",
        "Attendance - Present",
        "Attendance - Absent",
        "Salary - Credited",
        "Salary - Pending"
    ])
   
    if report_type == "All Employees":
        data = st.session_state.employee_data
    elif "Present" in report_type:
        data = st.session_state.employee_data[st.session_state.employee_data['Attendance'] == 'Present']
    elif "Absent" in report_type:
        data = st.session_state.employee_data[st.session_state.employee_data['Attendance'] == 'Absent']
    elif "Credited" in report_type:
        data = st.session_state.employee_data[st.session_state.employee_data['SalaryCredited'] == 'Yes']
    else:
        data = st.session_state.employee_data[st.session_state.employee_data['SalaryCredited'] == 'No']
   
    st.dataframe(data)
   
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            "📥 Download Excel Report",
            data=export_report('Attendance', 'Present'),
            file_name=f"{report_type.replace(' ', '_')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    with col2:
        st.download_button(
            "📄 Download PDF Report",
            data=export_pdf(),
            file_name="Employee_Report.pdf",
            mime="application/pdf"
        )