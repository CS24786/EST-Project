"""
TextileSafe - Accident & Near-Miss Analysis Module
Comprehensive incident logging, OSHA/ILO safety rate metrics (TRIR, LTIFR),
cause analysis, shift/department trends, and interactive management.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date
from database.db import query_dataframe, execute_query
from config import DEPARTMENTS, SHIFTS, SEVERITIES, INCIDENT_TYPES, HAZARD_TYPES, SEVERITY_COLORS

def render_incidents():
    """Renders the Accident & Near-Miss Analysis view."""
    st.markdown("""
        <div>
            <h1 class="page-title">Accidents & Near-Miss Analysis</h1>
            <div class="page-subtitle">Record, analyze, and investigate safety occurrences, root causes, and shift patterns.</div>
        </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📊 Analytics & Safety Metrics", "📋 Incident Registry & Records", "➕ Report New Occurrence"])

    # Load data
    df = query_dataframe("SELECT * FROM incidents ORDER BY incident_date DESC")

    with tab1:
        # Industry Metric Calculations
        # Standard Textile Mill Assumption: 1,200 workers × 8 hrs × 300 days = 2,880,000 annual exposure hours
        ANNUAL_MAN_HOURS = 2880000
        
        accidents = df[df["incident_type"].str.contains("Accident", case=False, na=False)]
        lost_time_accidents = df[df["incident_type"] == "Accident (Lost Time)"]
        near_misses = df[df["incident_type"] == "Near Miss"]
        total_lost_days = df["lost_workdays"].sum()

        # LTIFR = (Lost Time Injuries * 1,000,000) / Exposure Hours
        ltifr = round((len(lost_time_accidents) * 1000000) / ANNUAL_MAN_HOURS, 2) if ANNUAL_MAN_HOURS > 0 else 0
        # TRIR (OSHA) = (Total Recordable Injuries * 200,000) / Exposure Hours
        trir = round((len(accidents) * 200000) / ANNUAL_MAN_HOURS, 2) if ANNUAL_MAN_HOURS > 0 else 0
        # Severity Rate = (Lost Days * 1,000,000) / Exposure Hours
        sev_rate = round((total_lost_days * 1000000) / ANNUAL_MAN_HOURS, 1)

        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
        with m_col1:
            st.metric("LTIFR (Per 1M Hours)", f"{ltifr}", delta="-14% YoY", delta_color="inverse")
            st.caption("Lost Time Injury Frequency Rate")
        with m_col2:
            st.metric("TRIR (OSHA Standard)", f"{trir}", delta="-8% YoY", delta_color="inverse")
            st.caption("Total Recordable Incident Rate")
        with m_col3:
            st.metric("Total Lost Workdays", f"{total_lost_days} Days", delta="-22 Days", delta_color="inverse")
            st.caption("Accumulated Lost Workdays")
        with m_col4:
            st.metric("Near-Miss Ratio", f"{round(len(near_misses)/max(len(accidents),1), 2)} : 1", delta="+0.15 Proactive", delta_color="normal")
            st.caption("Near-Misses per Recorded Accident")

        st.markdown("<hr style='border-color:#e2e8f0; margin:1.5rem 0;'>", unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("<h4 style='color:#0f2b48;'>Incidents by Department & Severity</h4>", unsafe_allow_html=True)
            if not df.empty:
                dep_sev = df.groupby(["department", "severity"]).size().reset_index(name="count")
                fig_dep = px.bar(
                    dep_sev,
                    x="department",
                    y="count",
                    color="severity",
                    color_discrete_map=SEVERITY_COLORS,
                    barmode="stack",
                    labels={"count": "Number of Incidents", "department": "Department", "severity": "Severity"}
                )
                fig_dep.update_layout(height=320, margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig_dep, width="stretch")

        with c2:
            st.markdown("<h4 style='color:#0f2b48;'>Root Causes (Pareto Analysis)</h4>", unsafe_allow_html=True)
            if not df.empty:
                causes = df["root_cause"].value_counts().reset_index()
                causes.columns = ["cause", "count"]
                causes["cumulative_pct"] = (causes["count"].cumsum() / causes["count"].sum() * 100).round(1)

                fig_pareto = go.Figure()
                fig_pareto.add_trace(go.Bar(
                    x=causes["cause"],
                    y=causes["count"],
                    name="Frequency",
                    marker_color="#2563eb"
                ))
                fig_pareto.add_trace(go.Scatter(
                    x=causes["cause"],
                    y=causes["cumulative_pct"],
                    name="Cumulative %",
                    yaxis="y2",
                    mode="lines+markers",
                    line=dict(color="#f97316", width=2)
                ))
                fig_pareto.update_layout(
                    height=320,
                    margin=dict(l=10, r=10, t=10, b=10),
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    yaxis=dict(title="Count"),
                    yaxis2=dict(title="Cumulative %", overlaying="y", side="right", range=[0, 105]),
                    showlegend=False
                )
                st.plotly_chart(fig_pareto, width="stretch")

        # Shift Distribution
        st.markdown("<h4 style='color:#0f2b48; margin-top:1rem;'>Incident Distribution by Work Shift</h4>", unsafe_allow_html=True)
        shift_counts = df["shift"].value_counts().reset_index()
        shift_counts.columns = ["shift", "count"]
        fig_shift = px.pie(shift_counts, names="shift", values="count", hole=0.45, color_discrete_sequence=["#3b82f6", "#f59e0b", "#6366f1"])
        fig_shift.update_layout(height=260, margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_shift, width="stretch")

    with tab2:
        st.subheader("Filter and Manage Incident Records")
        
        # Filter controls
        f_col1, f_col2, f_col3 = st.columns(3)
        with f_col1:
            sel_dep = st.selectbox("Filter Department", ["All"] + DEPARTMENTS, key="inc_f_dep")
        with f_col2:
            sel_sev = st.selectbox("Filter Severity", ["All"] + SEVERITIES, key="inc_f_sev")
        with f_col3:
            sel_type = st.selectbox("Filter Type", ["All"] + INCIDENT_TYPES, key="inc_f_type")

        filtered = df.copy()
        if sel_dep != "All":
            filtered = filtered[filtered["department"] == sel_dep]
        if sel_sev != "All":
            filtered = filtered[filtered["severity"] == sel_sev]
        if sel_type != "All":
            filtered = filtered[filtered["incident_type"] == sel_type]

        st.caption(f"Showing {len(filtered)} records matching filter criteria")
        st.dataframe(
            filtered[["incident_code", "incident_date", "incident_type", "department", "shift", "severity", "root_cause", "lost_workdays", "status", "description"]],
            width="stretch",
            height=380
        )

        # Record Actions: Delete record safeguard
        with st.expander("🗑️ Delete an Incident Record (Admin)"):
            del_code = st.selectbox("Select Record Code to Remove", [""] + list(df["incident_code"].values))
            if del_code:
                confirm = st.checkbox(f"Confirm deletion of {del_code}")
                if st.button("Delete Record", type="primary") and confirm:
                    execute_query("DELETE FROM incidents WHERE incident_code = ?", (del_code,))
                    st.success(f"Record {del_code} successfully removed.")
                    st.rerun()

    with tab3:
        st.subheader("Log a New Incident or Near-Miss")
        with st.form("new_incident_form"):
            c1, c2 = st.columns(2)
            with c1:
                in_type = st.selectbox("Occurrence Classification", INCIDENT_TYPES)
                in_dep = st.selectbox("Factory Department", DEPARTMENTS)
                in_shift = st.selectbox("Operating Shift", SHIFTS)
                in_date = st.date_input("Incident Date", value=date.today())
                in_sev = st.selectbox("Severity Classification", SEVERITIES)
            with c2:
                in_cause = st.selectbox("Primary Hazard / Root Cause", HAZARD_TYPES)
                in_person = st.text_input("Injured Person / Involved Worker", value="Muhammad Asif")
                in_lost_days = st.number_input("Lost Workdays (LWD)", min_value=0, max_value=365, value=0)
                in_reporter = st.text_input("Reported By", value=st.session_state.get("user", {}).get("name", "Talha Nawaz"))
                in_status = st.selectbox("Initial Status", ["Under Review", "Investigated", "Closed"])

            in_desc = st.text_area("Detailed Event Description & Immediate Corrective Steps", "Worker noticed safety trip wire on spinning frame disengaged; maintenance halted machine immediately.")

            submit_inc = st.form_submit_button("Submit Incident Record", type="primary", width="stretch")

            if submit_inc:
                new_code = f"INC-2025-{len(df)+101:03d}"
                execute_query("""
                    INSERT INTO incidents (
                        incident_code, incident_type, department, shift, severity,
                        incident_date, root_cause, description, injured_person,
                        lost_workdays, reported_by, status
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    new_code, in_type, in_dep, in_shift, in_sev,
                    in_date.strftime("%Y-%m-%d"), in_cause, in_desc, in_person,
                    in_lost_days, in_reporter, in_status
                ))
                st.success(f"Incident {new_code} logged successfully into persistent database.")
                st.rerun()
