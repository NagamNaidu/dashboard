import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from ui_components import create_card, metric_card
from attendance import attendance_management
from salary import salary_management
from new_employee import add_new_employee_form
from reports import show_reports

def show_admin():
    try:
        st.title("👑 Admin Dashboard")
       
        # Welcome header with user info
        st.markdown(f"""
        <div class="main-container animate-fade">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem;">
                <div>
                    <h1 style="color: var(--primary); margin-bottom: 0.5rem;">Welcome back, {st.session_state.current_user}!</h1>
                    <p style="color: var(--dark); opacity: 0.8;">{datetime.now().strftime('%A, %B %d, %Y')}</p>
                </div>
                <div style="background: var(--accent); padding: 0.5rem 1rem; border-radius: 20px; color: white; font-weight: 600;">
                    ADMINISTRATOR
                </div>
            </div>
        """, unsafe_allow_html=True)
       
        if st.session_state.employee_data.empty:
            st.warning("No employee data found")
            return

        # Metrics Row
        df = st.session_state.employee_data
        present_count = len(df[df['Attendance'] == 'Present'])
        absent_count = len(df[df['Attendance'] == 'Absent'])
        on_leave = len(df[df['Attendance'] == 'On Leave'])
        paid_count = len(df[df['SalaryCredited'] == 'Yes'])
        total_employees = len(df)
       
        # Calculate percentages
        present_percent = int((present_count / total_employees) * 100) if total_employees > 0 else 0
        absent_percent = int((absent_count / total_employees) * 100) if total_employees > 0 else 0
       
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(metric_card("Present Today",
                                  present_count,
                                  present_percent,
                                  "normal"),
                      unsafe_allow_html=True)
        with col2:
            st.markdown(metric_card("Absent Today",
                                  absent_count,
                                  absent_count,
                                  "inverse"),
                      unsafe_allow_html=True)
        with col3:
            st.markdown(metric_card("On Leave", on_leave), unsafe_allow_html=True)
        with col4:
            st.markdown(metric_card("Salaries Paid", paid_count), unsafe_allow_html=True)
       
        st.markdown("</div>", unsafe_allow_html=True)  # Close main container

        # Main Content Tabs
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Analytics", "👥 Employee Management", "➕ Add Employee", "📤 Reports"])

        with tab1:
            col1, col2 = st.columns([3, 2])
            with col1:
                # Attendance Trends
                df = st.session_state.employee_data.copy()
                df["Date"] = pd.to_datetime(df["LastAttendanceUpdate"].str.split().str[0], errors='coerce')
                chart_df = df.groupby(["Date", "Attendance"]).size().reset_index(name='Count')
                fig = px.bar(chart_df, x="Date", y="Count", color="Attendance",
                             title="Attendance History", barmode='group')
                st.plotly_chart(fig, use_container_width=True)
           
            with col2:
                # Status Distribution
                status_df = df['Attendance'].value_counts().reset_index()
                fig = px.pie(status_df, values='count', names='Attendance',
                             title="Current Attendance Distribution")
                st.plotly_chart(fig, use_container_width=True)

        with tab2:
            # Employee Management Cards
            attendance_management()
            salary_management()

        with tab3:
            add_new_employee_form()

        with tab4:
            show_reports()
    except Exception as e:
        st.error(f"Error in admin dashboard: {str(e)}")
