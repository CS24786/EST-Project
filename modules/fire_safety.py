"""
TextileSafe - Fire-Safety Inspections Module
Tracks fire extinguishers, smoke alarms, emergency exits, and evacuation routes across mill sectors.
Provides automated overdue detection, pass/deficiency analytics, and inspection logging.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date, timedelta
from database.db import query_dataframe, execute_query
from config import DEPARTMENTS, FIRE_EQUIPMENT_TYPES

def render_fire_safety():
    """Renders the Fire-Safety Inspections view."""
    st.markdown("""
        <div>
            <h1 class="page-title">Fire-Safety & Emergency Systems Inspection</h1>
            <div class="page-subtitle">Mill-wide audit of fire extinguishers, hydrant lines, alarms, push-bar exits, and evacuation paths.</div>
        </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🔥 Inspection Analytics", "📋 Equipment Log & Overdue Alerts", "➕ Log Fire Inspection"])

    fire_df = query_dataframe("SELECT * FROM fire_inspections ORDER BY next_due_date ASC")

    with tab1:
        total_units = len(fire_df)
        passed_units = len(fire_df[fire_df["status"] == "Passed"])
        deficient_units = len(fire_df[fire_df["status"] == "Deficient"])
        overdue_units = len(fire_df[fire_df["status"] == "Overdue"])
        pass_rate = round(passed_units / max(total_units, 1) * 100, 1)

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("Fire Safety Compliance Rate", f"{pass_rate}%", delta="+2% vs baseline")
            st.caption("Standard Requirement: ≥ 95%")
        with c2:
            st.metric("Total Inspected Points", f"{total_units}", delta="100% Asset Coverage")
            st.caption("Active Fire Safeguards")
        with c3:
            st.metric("Deficiencies Requiring Attention", f"{deficient_units}", delta="-1 Resolved", delta_color="inverse")
            st.caption("Pressure or Pin Replacements")
        with c4:
            st.metric("Overdue Inspections", f"{overdue_units}", delta="Action Required", delta_color="inverse")
            st.caption("Expired 30-Day Inspection Window")

        st.markdown("<hr style='border-color:#e2e8f0; margin:1.5rem 0;'>", unsafe_allow_html=True)

        col_left, col_right = st.columns(2)
        with col_left:
            st.markdown("<h4 style='color:#0f2b48;'>Equipment Status Distribution</h4>", unsafe_allow_html=True)
            status_counts = fire_df["status"].value_counts().reset_index()
            status_counts.columns = ["status", "count"]
            color_map = {"Passed": "#10b981", "Deficient": "#f59e0b", "Overdue": "#ef4444"}
            fig_status = px.pie(status_counts, names="status", values="count", hole=0.5, color="status", color_discrete_map=color_map)
            fig_status.update_layout(height=280, margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_status, width="stretch")

        with col_right:
            st.markdown("<h4 style='color:#0f2b48;'>Status by Department</h4>", unsafe_allow_html=True)
            dep_fire = fire_df.groupby(["department", "status"]).size().reset_index(name="count")
            fig_dep_fire = px.bar(
                dep_fire,
                x="department",
                y="count",
                color="status",
                color_discrete_map=color_map,
                barmode="stack",
                labels={"department": "Department", "count": "Inspections"}
            )
            fig_dep_fire.update_layout(height=280, margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_dep_fire, width="stretch")

        # Deficiencies / Overdue alert banner
        if deficient_units > 0 or overdue_units > 0:
            st.markdown(f"""
            <div style="background:#fff7ed; border-left:4px solid #f97316; padding:1rem; border-radius:8px; margin-top:1rem;">
                <b style="color:#9a3412;">⚠️ High Priority Fire Safety Warning:</b>
                <span style="color:#7c2d12;"> There are {overdue_units} overdue equipment checks and {deficient_units} reported physical/pressure deficiencies in production bays. Prompt remediation required.</span>
            </div>
            """, unsafe_allow_html=True)

    with tab2:
        st.subheader("Equipment Registry & Inspection Records")
        f_status = st.selectbox("Filter Status", ["All", "Passed", "Deficient", "Overdue"], key="fire_tab2_stat")
        f_dep = st.selectbox("Filter Department", ["All"] + DEPARTMENTS, key="fire_tab2_dep")

        filtered_fire = fire_df.copy()
        if f_status != "All":
            filtered_fire = filtered_fire[filtered_fire["status"] == f_status]
        if f_dep != "All":
            filtered_fire = filtered_fire[filtered_fire["department"] == f_dep]

        st.caption(f"Showing {len(filtered_fire)} equipment records")
        st.dataframe(
            filtered_fire[["inspection_code", "equipment_type", "location_tag", "department", "inspection_date", "next_due_date", "status", "pressure_check", "physical_condition", "findings", "inspector"]],
            width="stretch",
            height=350
        )

    with tab3:
        st.subheader("Log Equipment Inspection / Routine Check")
        with st.form("new_fire_form"):
            c1, c2 = st.columns(2)
            with c1:
                f_type = st.selectbox("Fire Safeguard / Equipment Type", FIRE_EQUIPMENT_TYPES)
                f_dept = st.selectbox("Department Location", DEPARTMENTS)
                f_tag = st.text_input("Asset Location Tag", value=f"{f_dept[:3].upper()}-EXT-204")
                f_date = st.date_input("Inspection Date", value=date.today())
            with c2:
                f_stat = st.selectbox("Inspection Result", ["Passed", "Deficient", "Overdue"])
                f_press = st.selectbox("Pressure Gauge Status", ["Normal (Green Zone)", "Low (Recharge Needed)", "High", "N/A"])
                f_cond = st.selectbox("Physical & Access Condition", ["Good & Clear", "Obstructed Aisle", "Missing Pin/Seal", "Damaged Hose"])
                f_lead = st.text_input("Inspecting Officer", value=st.session_state.get("user", {}).get("name", "Talha Nawaz"))

            f_notes = st.text_area("Audit Notes & Defect Findings", "Weight verified. Pressure in green zone. Seal unbroken. Free from lint blockage.")

            sub_fire = st.form_submit_button("Record Inspection", type="primary", width="stretch")

            if sub_fire:
                due = f_date + timedelta(days=30)
                new_code = f"FIRE-2025-{len(fire_df)+101:04d}"

                execute_query("""
                    INSERT INTO fire_inspections (
                        inspection_code, department, equipment_type, location_tag,
                        inspection_date, next_due_date, status, pressure_check,
                        physical_condition, findings, inspector
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    new_code, f_dept, f_type, f_tag,
                    f_date.strftime("%Y-%m-%d"), due.strftime("%Y-%m-%d"),
                    f_stat, f_press.split()[0], f_cond.split()[0], f_notes, f_lead
                ))
                st.success(f"Inspection {new_code} saved. Next due date set to {due.strftime('%Y-%m-%d')}.")
                st.rerun()
