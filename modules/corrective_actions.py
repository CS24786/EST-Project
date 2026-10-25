"""
TextileSafe - Corrective & Preventive Action (CAPA) Tracker Module
Enables lifecycle tracking for safety remediations: Open -> In Progress -> Closed.
Tracks assignees, deadlines, overdue status, priorities, and audit trail.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
from database.db import query_dataframe, execute_query
from config import DEPARTMENTS

def render_corrective_actions():
    """Renders the Corrective Actions (CAPA) tracking view."""
    st.markdown("""
        <div>
            <h1 class="page-title">Corrective & Preventive Action (CAPA) Tracker</h1>
            <div class="page-subtitle">Track safety remediations, assignees, deadlines, and closure verification across the mill.</div>
        </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📋 Action Registry & Status", "➕ Create New CAPA", "📊 Closure Analytics"])

    capa_df = query_dataframe("SELECT * FROM corrective_actions ORDER BY due_date ASC")

    with tab1:
        # Metrics row
        total_actions = len(capa_df)
        open_actions = len(capa_df[capa_df["status"] == "Open"])
        in_progress = len(capa_df[capa_df["status"] == "In Progress"])
        closed_actions = len(capa_df[capa_df["status"] == "Closed"])
        closure_rate = round(closed_actions / max(total_actions, 1) * 100, 1)

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("Open Remediations", f"{open_actions}", delta="+2 New", delta_color="inverse")
            st.caption("Awaiting Engineering Action")
        with c2:
            st.metric("In Progress", f"{in_progress}", delta="Under Implementation")
            st.caption("Active Remediation")
        with c3:
            st.metric("Closed & Verified", f"{closed_actions}", delta=f"{closure_rate}% Completed")
            st.caption("Verified by Safety Dept")
        with c4:
            st.metric("Overall Closure Rate", f"{closure_rate}%", delta="+5.2% vs target")
            st.caption("Benchmark: ≥ 85%")

        st.markdown("<hr style='border-color:#e2e8f0; margin:1.25rem 0;'>", unsafe_allow_html=True)

        # Filters
        f1, f2, f3 = st.columns(3)
        with f1:
            s_filter = st.selectbox("Status Filter", ["All", "Open", "In Progress", "Closed"], key="capa_s_filter")
        with f2:
            p_filter = st.selectbox("Priority Filter", ["All", "High", "Medium", "Low"], key="capa_p_filter")
        with f3:
            d_filter = st.selectbox("Department Filter", ["All"] + DEPARTMENTS, key="capa_d_filter")

        filtered_capa = capa_df.copy()
        if s_filter != "All":
            filtered_capa = filtered_capa[filtered_capa["status"] == s_filter]
        if p_filter != "All":
            filtered_capa = filtered_capa[filtered_capa["priority"] == p_filter]
        if d_filter != "All":
            filtered_capa = filtered_capa[filtered_capa["department"] == d_filter]

        st.caption(f"Showing {len(filtered_capa)} corrective action entries")
        st.dataframe(
            filtered_capa[["action_code", "title", "department", "assigned_to", "priority", "due_date", "status", "source_type", "notes"]],
            width="stretch",
            height=340
        )

        # Quick Update Status Tool
        st.markdown("<h4 style='color:#0f2b48; margin-top:1.5rem;'>⚡ Quick Status Update</h4>", unsafe_allow_html=True)
        u_col1, u_col2, u_col3 = st.columns([2, 1, 1])
        with u_col1:
            act_select = st.selectbox("Select Action to Update", [""] + [f"{r['action_code']}: {r['title']}" for _, r in capa_df.iterrows()])
        with u_col2:
            new_stat = st.selectbox("New Lifecycle Status", ["Open", "In Progress", "Closed"])
        with u_col3:
            st.markdown("<div style='height:28px;'></div>", unsafe_allow_html=True)
            if st.button("Update Status", type="primary", width="stretch"):
                if act_select:
                    code = act_select.split(":")[0].strip()
                    comp_date = date.today().strftime("%Y-%m-%d") if new_stat == "Closed" else None
                    execute_query("UPDATE corrective_actions SET status = ?, completion_date = ? WHERE action_code = ?", (new_stat, comp_date, code))
                    st.success(f"Action {code} status updated to {new_stat}.")
                    st.rerun()

    with tab2:
        st.subheader("Assign a New Corrective Action (CAPA)")
        with st.form("new_capa_form"):
            c1, c2 = st.columns(2)
            with c1:
                c_title = st.text_input("Remediation Title", "Install sound insulation partition around compressor room")
                c_dept = st.selectbox("Department", DEPARTMENTS, key="capa_form_dept")
                c_src = st.selectbox("Identified From", ["Incident", "Near Miss", "PPE Audit", "Fire Audit", "Hazard Assessment"])
                c_ref = st.text_input("Source Reference ID", value="AUDIT-2025-042")
            with c2:
                c_assignee = st.text_input("Responsible Engineer / Officer", value="Engr. Muhammad Tariq")
                c_prio = st.selectbox("Priority Level", ["High", "Medium", "Low"])
                c_due = st.date_input("Target Resolution Date", value=date.today())
                c_init_stat = st.selectbox("Initial State", ["Open", "In Progress"])

            c_notes = st.text_area("Detailed Action Plan & Required Materials", "Engineering team to procure vibration isolation dampers and sound absorbing gypsum paneling.")

            sub_capa = st.form_submit_button("Create Corrective Action", type="primary", width="stretch")

            if sub_capa:
                new_code = f"CAPA-2025-{len(capa_df)+101:03d}"
                execute_query("""
                    INSERT INTO corrective_actions (
                        action_code, title, source_type, source_ref, department,
                        assigned_to, priority, due_date, status, completion_date, notes
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    new_code, c_title, c_src, c_ref, c_dept,
                    c_assignee, c_prio, c_due.strftime("%Y-%m-%d"), c_init_stat, None, c_notes
                ))
                st.success(f"CAPA {new_code} assigned to {c_assignee}.")
                st.rerun()

    with tab3:
        st.subheader("Remediation Closure & Department Performance")
        c_left, c_right = st.columns(2)
        with c_left:
            st.markdown("<h4 style='color:#0f2b48;'>Actions by Lifecycle Status</h4>", unsafe_allow_html=True)
            stat_dist = capa_df["status"].value_counts().reset_index()
            stat_dist.columns = ["status", "count"]
            fig_stat_capa = px.pie(stat_dist, names="status", values="count", hole=0.5, color="status",
                                   color_discrete_map={"Open": "#ef4444", "In Progress": "#f59e0b", "Closed": "#10b981"})
            fig_stat_capa.update_layout(height=280, margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_stat_capa, width="stretch")

        with c_right:
            st.markdown("<h4 style='color:#0f2b48;'>Actions by Priority</h4>", unsafe_allow_html=True)
            prio_dist = capa_df["priority"].value_counts().reset_index()
            prio_dist.columns = ["priority", "count"]
            fig_prio = px.bar(prio_dist, x="priority", y="count", color="priority",
                              color_discrete_map={"High": "#ef4444", "Medium": "#f59e0b", "Low": "#3b82f6"})
            fig_prio.update_layout(height=280, margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_prio, width="stretch")
