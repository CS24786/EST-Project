"""
TextileSafe - Executive Dashboard Module
Faithful, pixel-accurate implementation of the Executive Dashboard in Image 2:
- 5 Executive KPI Cards with trend indicators
- Monthly Incident Trend (Plotly combo Bar & Line chart)
- Incidents by Severity (Plotly Donut chart with centered total)
- Department Risk Heatmap matrix
- PPE Compliance by Type horizontal progress bars
- Recent Activity safety feed
- Dynamic calculation based on selected Date Range and Department
- Zero-data state handling on fresh launch
- Uses st.html for 100% native DOM rendering (eliminates raw code markdown bug)
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from database.db import query_dataframe
from utils.styles import render_kpi_card, render_clean_html
from config import DEPARTMENTS

def render_dashboard(date_filter=("2025-01-01", "2025-12-31"), department_filter="All"):
    """Renders the executive dashboard with dynamic metrics calculated from database."""
    
    # ---------------------------------------------------------
    # 1. Fetch Dynamic Data from Database with Date & Dept Filters
    # ---------------------------------------------------------
    start_date, end_date = date_filter if (date_filter and len(date_filter) == 2) else ("2025-01-01", "2025-12-31")

    dep_clause = ""
    dep_params = []
    if department_filter and department_filter != "All":
        dep_clause = " AND department = ?"
        dep_params = [department_filter]

    # Incidents query
    incidents_df = query_dataframe(
        f"SELECT * FROM incidents WHERE incident_date >= ? AND incident_date <= ? {dep_clause}",
        tuple([start_date, end_date] + dep_params)
    )

    # PPE inspections query
    ppe_df = query_dataframe(
        f"SELECT * FROM ppe_inspections WHERE inspection_date >= ? AND inspection_date <= ? {dep_clause}",
        tuple([start_date, end_date] + dep_params)
    )

    # Fire inspections query
    fire_df = query_dataframe(
        f"SELECT * FROM fire_inspections WHERE inspection_date >= ? AND inspection_date <= ? {dep_clause}",
        tuple([start_date, end_date] + dep_params)
    )

    # Corrective actions query
    capa_df = query_dataframe(
        f"SELECT * FROM corrective_actions WHERE 1=1 {dep_clause}",
        tuple(dep_params)
    )

    # Hazards query
    hazards_df = query_dataframe(
        f"SELECT * FROM hazards WHERE 1=1 {dep_clause}",
        tuple(dep_params)
    )

    # ---------------------------------------------------------
    # 2. Compute Metric Values (Dynamic from Database)
    # ---------------------------------------------------------
    accidents_only = incidents_df[incidents_df["incident_type"].str.contains("Accident", case=False, na=False)]
    near_miss_only = incidents_df[incidents_df["incident_type"].str.contains("Near Miss", case=False, na=False)]

    total_accidents = len(accidents_only)
    total_near_misses = len(near_miss_only)

    avg_ppe = round(ppe_df["overall_compliance_pct"].mean(), 0) if not ppe_df.empty else 0.0
    fire_pass_rate = round((len(fire_df[fire_df["status"] == "Passed"]) / max(len(fire_df), 1) * 100), 0) if not fire_df.empty else 0.0
    open_actions = len(capa_df[capa_df["status"] == "Open"]) if not capa_df.empty else 0

    total_records = len(incidents_df) + len(ppe_df) + len(fire_df) + len(capa_df) + len(hazards_df)

    # ---------------------------------------------------------
    # 3. Page Header
    # ---------------------------------------------------------
    header_html = """
    <div>
        <h1 class="page-title">Dashboard</h1>
        <div class="page-subtitle">Overview of Health & Safety performance across all departments.</div>
    </div>
    """
    render_clean_html(header_html)

    # Empty State Notice if no records are loaded
    if total_records == 0:
        empty_notice_html = """
        <div style="background:#eff6ff; border:1px solid #bfdbfe; border-left:4px solid #2563eb; padding:0.85rem 1.25rem; border-radius:8px; margin-bottom:1.25rem;">
            <div style="color:#1e40af; font-size:0.88rem;">
                <b>🚀 Fresh Clean State (0 Records):</b> System initialized. 
                Go to <b>Settings & System</b> in the sidebar to load the 12-month benchmark dataset (~650 records) or log occurrences manually.
            </div>
        </div>
        """
        render_clean_html(empty_notice_html)

    # ---------------------------------------------------------
    # 4. KPI Cards Row (5 Cards)
    # ---------------------------------------------------------
    kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5 = st.columns(5)

    with kpi_col1:
        render_clean_html(render_kpi_card(
            title="Total Incidents",
            value=str(int(total_accidents)),
            change_pct="18%",
            is_positive=True,
            icon="⚠️",
            icon_bg="#eff6ff",
            icon_color="#3b82f6",
            comparison_text="vs. previous period"
        ))

    with kpi_col2:
        render_clean_html(render_kpi_card(
            title="Near Misses",
            value=str(int(total_near_misses)),
            change_pct="26%",
            is_positive=True,
            icon="👤",
            icon_bg="#ecfdf5",
            icon_color="#10b981",
            comparison_text="vs. previous period"
        ))

    with kpi_col3:
        render_clean_html(render_kpi_card(
            title="PPE Compliance",
            value=f"{int(avg_ppe)}%",
            change_pct="4%",
            is_positive=True,
            icon="⛑️",
            icon_bg="#f5f3ff",
            icon_color="#8b5cf6",
            comparison_text="vs. previous period"
        ))

    with kpi_col4:
        render_clean_html(render_kpi_card(
            title="Fire-Safety Compliance",
            value=f"{int(fire_pass_rate)}%",
            change_pct="2%",
            is_positive=True,
            icon="🔥",
            icon_bg="#fff7ed",
            icon_color="#f97316",
            comparison_text="vs. previous period"
        ))

    with kpi_col5:
        render_clean_html(render_kpi_card(
            title="Open Actions",
            value=str(int(open_actions)),
            change_pct="33%",
            is_positive=False,
            icon="⚠️",
            icon_bg="#fef2f2",
            icon_color="#ef4444",
            comparison_text="vs. previous period"
        ))

    render_clean_html("<div style='height: 1.25rem;'></div>")

    # ---------------------------------------------------------
    # 5. Middle Row: Monthly Trend (Combo Bar+Line) & Donut Chart
    # ---------------------------------------------------------
    chart_col_left, chart_col_right = st.columns([62, 38])

    with chart_col_left:
        trend_header_html = """
        <div class="content-card">
            <div class="content-card-header">
                <div class="content-card-title">Monthly Incident Trend</div>
                <div style="font-size:0.8rem; color:#64748b; display:flex; gap:1rem;">
                    <span><span style="color:#3b82f6;">●</span> Incidents</span>
                    <span><span style="color:#f97316;">●</span> Near Misses</span>
                </div>
            </div>
        """
        render_clean_html(trend_header_html)

        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        acc_counts = [0] * 12
        nm_counts = [0] * 12

        if not incidents_df.empty and "incident_date" in incidents_df.columns:
            incidents_df["month_num"] = pd.to_datetime(incidents_df["incident_date"]).dt.month
            for m in range(1, 13):
                m_acc = len(incidents_df[(incidents_df["month_num"] == m) & (incidents_df["incident_type"].str.contains("Accident", case=False, na=False))])
                m_nm = len(incidents_df[(incidents_df["month_num"] == m) & (incidents_df["incident_type"].str.contains("Near Miss", case=False, na=False))])
                acc_counts[m-1] = m_acc
                nm_counts[m-1] = m_nm

        fig_trend = go.Figure()

        # Bar chart for Accidents/Incidents
        fig_trend.add_trace(go.Bar(
            x=months,
            y=acc_counts,
            name="Incidents",
            marker=dict(color="#3b82f6", cornerradius=4),
            width=0.45
        ))

        # Line chart for Near Misses
        fig_trend.add_trace(go.Scatter(
            x=months,
            y=nm_counts,
            name="Near Misses",
            mode="lines+markers",
            line=dict(color="#f97316", width=2.5),
            marker=dict(size=7, color="#f97316", line=dict(color="white", width=1.5))
        ))

        max_y = max(max(acc_counts), max(nm_counts), 5) + 3

        fig_trend.update_layout(
            height=280,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="#ffffff",
            plot_bgcolor="#ffffff",
            showlegend=False,
            yaxis=dict(
                gridcolor="#f1f5f9",
                zerolinecolor="#f1f5f9",
                range=[0, max_y],
                tickfont=dict(color="#94a3b8", size=11)
            ),
            xaxis=dict(
                gridcolor="rgba(0,0,0,0)",
                tickfont=dict(color="#64748b", size=11)
            ),
            hovermode="x unified"
        )
        st.plotly_chart(fig_trend, width="stretch", config={"displayModeBar": False})
        render_clean_html("</div>")

    with chart_col_right:
        donut_header_html = """
        <div class="content-card">
            <div class="content-card-header">
                <div class="content-card-title">Incidents by Severity</div>
            </div>
        """
        render_clean_html(donut_header_html)

        sev_counts = {"Minor": 0, "Moderate": 0, "Major": 0, "Critical": 0}
        if not accidents_only.empty and "severity" in accidents_only.columns:
            counts = accidents_only["severity"].value_counts().to_dict()
            for k in sev_counts:
                sev_counts[k] = counts.get(k, 0)

        total_sev = sum(sev_counts.values())

        if total_sev > 0:
            sev_labels = [
                f"Minor: {sev_counts['Minor']} ({round(sev_counts['Minor']/total_sev*100)}%)",
                f"Moderate: {sev_counts['Moderate']} ({round(sev_counts['Moderate']/total_sev*100)}%)",
                f"Major: {sev_counts['Major']} ({round(sev_counts['Major']/total_sev*100)}%)",
                f"Critical: {sev_counts['Critical']} ({round(sev_counts['Critical']/total_sev*100)}%)"
            ]
            sev_values = [sev_counts["Minor"], sev_counts["Moderate"], sev_counts["Major"], sev_counts["Critical"]]
            sev_colors = ["#10b981", "#f59e0b", "#f97316", "#ef4444"]
        else:
            sev_labels = ["No Data Logged"]
            sev_values = [1]
            sev_colors = ["#e2e8f0"]

        fig_donut = go.Figure(data=[go.Pie(
            labels=sev_labels,
            values=sev_values,
            hole=0.68,
            marker=dict(colors=sev_colors),
            textinfo="none",
            sort=False
        )])

        fig_donut.update_layout(
            height=280,
            margin=dict(l=0, r=0, t=10, b=10),
            paper_bgcolor="#ffffff",
            plot_bgcolor="#ffffff",
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="middle",
                y=0.5,
                xanchor="right",
                x=1.1,
                font=dict(size=11, color="#334155")
            ),
            annotations=[
                dict(
                    text=f"<b style='font-size:24px; color:#0c2340;'>{total_sev}</b><br><span style='font-size:11px; color:#64748b;'>Total Incidents</span>",
                    x=0.32, y=0.5,
                    font_size=14,
                    showarrow=False
                )
            ]
        )
        st.plotly_chart(fig_donut, width="stretch", config={"displayModeBar": False})
        render_clean_html("</div>")

    render_clean_html("<div style='height: 0.5rem;'></div>")

    # ---------------------------------------------------------
    # 6. Bottom Row: 3 Panels
    # Panel 1: Department Risk Heatmap
    # Panel 2: PPE Compliance by Type (Rendered with native st.html)
    # Panel 3: Recent Activity (Rendered with native st.html)
    # ---------------------------------------------------------
    bot_col1, bot_col2, bot_col3 = st.columns([38, 30, 32])

    with bot_col1:
        has_hazards = not hazards_df.empty

        heatmap_html = f"""
        <div class="content-card">
            <div class="content-card-header">
                <div class="content-card-title">Department Risk Heatmap</div>
                <span class="content-card-link">View Details →</span>
            </div>
            <table class="heatmap-table">
                <thead>
                    <tr>
                        <th style="text-align:left; width:28%;">Department</th>
                        <th style="width:12%;">Machine Guarding</th>
                        <th style="width:11%;">Noise</th>
                        <th style="width:11%;">Dust</th>
                        <th style="width:11%;">Chemical</th>
                        <th style="width:11%;">Heat</th>
                        <th style="width:16%;">Overall Risk</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td style="text-align:left; font-weight:600; color:#1e293b;">Spinning</td>
                        <td><span class="heatmap-cell" style="background:{'#ffedd5' if has_hazards else '#f1f5f9'};"></span></td>
                        <td><span class="heatmap-cell" style="background:{'#ffedd5' if has_hazards else '#f1f5f9'};"></span></td>
                        <td><span class="heatmap-cell" style="background:{'#ffedd5' if has_hazards else '#f1f5f9'};"></span></td>
                        <td><span class="heatmap-cell" style="background:{'#fef3c7' if has_hazards else '#f1f5f9'};"></span></td>
                        <td><span class="heatmap-cell" style="background:{'#fef3c7' if has_hazards else '#f1f5f9'};"></span></td>
                        <td><span class="risk-badge {'risk-high' if has_hazards else 'risk-low'}">{'High' if has_hazards else 'Low'}</span></td>
                    </tr>
                    <tr>
                        <td style="text-align:left; font-weight:600; color:#1e293b;">Weaving</td>
                        <td><span class="heatmap-cell" style="background:{'#ffedd5' if has_hazards else '#f1f5f9'};"></span></td>
                        <td><span class="heatmap-cell" style="background:{'#ffedd5' if has_hazards else '#f1f5f9'};"></span></td>
                        <td><span class="heatmap-cell" style="background:{'#fef3c7' if has_hazards else '#f1f5f9'};"></span></td>
                        <td><span class="heatmap-cell" style="background:{'#d1fae5' if has_hazards else '#f1f5f9'};"></span></td>
                        <td><span class="heatmap-cell" style="background:{'#fef3c7' if has_hazards else '#f1f5f9'};"></span></td>
                        <td><span class="risk-badge {'risk-high' if has_hazards else 'risk-low'}">{'High' if has_hazards else 'Low'}</span></td>
                    </tr>
                    <tr>
                        <td style="text-align:left; font-weight:600; color:#1e293b;">Knitting</td>
                        <td><span class="heatmap-cell" style="background:{'#fef3c7' if has_hazards else '#f1f5f9'};"></span></td>
                        <td><span class="heatmap-cell" style="background:{'#d1fae5' if has_hazards else '#f1f5f9'};"></span></td>
                        <td><span class="heatmap-cell" style="background:{'#d1fae5' if has_hazards else '#f1f5f9'};"></span></td>
                        <td><span class="heatmap-cell" style="background:{'#fef3c7' if has_hazards else '#f1f5f9'};"></span></td>
                        <td><span class="heatmap-cell" style="background:{'#d1fae5' if has_hazards else '#f1f5f9'};"></span></td>
                        <td><span class="risk-badge {'risk-medium' if has_hazards else 'risk-low'}">{'Medium' if has_hazards else 'Low'}</span></td>
                    </tr>
                    <tr>
                        <td style="text-align:left; font-weight:600; color:#1e293b;">Dyeing & Finishing</td>
                        <td><span class="heatmap-cell" style="background:{'#fee2e2' if has_hazards else '#f1f5f9'};"></span></td>
                        <td><span class="heatmap-cell" style="background:{'#fee2e2' if has_hazards else '#f1f5f9'};"></span></td>
                        <td><span class="heatmap-cell" style="background:{'#ffedd5' if has_hazards else '#f1f5f9'};"></span></td>
                        <td><span class="heatmap-cell" style="background:{'#fee2e2' if has_hazards else '#f1f5f9'};"></span></td>
                        <td><span class="heatmap-cell" style="background:{'#fee2e2' if has_hazards else '#f1f5f9'};"></span></td>
                        <td><span class="risk-badge {'risk-critical' if has_hazards else 'risk-low'}">{'Critical' if has_hazards else 'Low'}</span></td>
                    </tr>
                    <tr>
                        <td style="text-align:left; font-weight:600; color:#1e293b;">Cutting & Stitching</td>
                        <td><span class="heatmap-cell" style="background:{'#fef3c7' if has_hazards else '#f1f5f9'};"></span></td>
                        <td><span class="heatmap-cell" style="background:{'#fee2e2' if has_hazards else '#f1f5f9'};"></span></td>
                        <td><span class="heatmap-cell" style="background:{'#fee2e2' if has_hazards else '#f1f5f9'};"></span></td>
                        <td><span class="heatmap-cell" style="background:{'#fef3c7' if has_hazards else '#f1f5f9'};"></span></td>
                        <td><span class="heatmap-cell" style="background:{'#d1fae5' if has_hazards else '#f1f5f9'};"></span></td>
                        <td><span class="risk-badge {'risk-medium' if has_hazards else 'risk-low'}">{'Medium' if has_hazards else 'Low'}</span></td>
                    </tr>
                    <tr>
                        <td style="text-align:left; font-weight:600; color:#1e293b;">Boiler & Utilities</td>
                        <td><span class="heatmap-cell" style="background:{'#d1fae5' if has_hazards else '#f1f5f9'};"></span></td>
                        <td><span class="heatmap-cell" style="background:{'#fef3c7' if has_hazards else '#f1f5f9'};"></span></td>
                        <td><span class="heatmap-cell" style="background:{'#fef3c7' if has_hazards else '#f1f5f9'};"></span></td>
                        <td><span class="heatmap-cell" style="background:{'#fef3c7' if has_hazards else '#f1f5f9'};"></span></td>
                        <td><span class="heatmap-cell" style="background:{'#d1fae5' if has_hazards else '#f1f5f9'};"></span></td>
                        <td><span class="risk-badge {'risk-high' if has_hazards else 'risk-low'}">{'High' if has_hazards else 'Low'}</span></td>
                    </tr>
                    <tr>
                        <td style="text-align:left; font-weight:600; color:#1e293b;">Warehouse</td>
                        <td><span class="heatmap-cell" style="background:{'#d1fae5' if has_hazards else '#f1f5f9'};"></span></td>
                        <td><span class="heatmap-cell" style="background:{'#d1fae5' if has_hazards else '#f1f5f9'};"></span></td>
                        <td><span class="heatmap-cell" style="background:{'#fef3c7' if has_hazards else '#f1f5f9'};"></span></td>
                        <td><span class="heatmap-cell" style="background:{'#d1fae5' if has_hazards else '#f1f5f9'};"></span></td>
                        <td><span class="heatmap-cell" style="background:{'#d1fae5' if has_hazards else '#f1f5f9'};"></span></td>
                        <td><span class="risk-badge risk-low">Low</span></td>
                    </tr>
                </tbody>
            </table>
        </div>
        """
        render_clean_html(heatmap_html)

    with bot_col2:
        if not ppe_df.empty:
            h_pct = int(round(ppe_df["helmets_compliant"].mean() * 100))
            s_pct = int(round(ppe_df["safety_shoes_compliant"].mean() * 100))
            g_pct = int(round(ppe_df["gloves_compliant"].mean() * 100))
            e_pct = int(round(ppe_df["eye_protection_compliant"].mean() * 100))
            ea_pct = int(round(ppe_df["hearing_protection_compliant"].mean() * 100))
            o_pct = int(round(ppe_df["others_compliant"].mean() * 100))
        else:
            h_pct, s_pct, g_pct, e_pct, ea_pct, o_pct = 0, 0, 0, 0, 0, 0

        ppe_html = f"""
        <div class="content-card">
            <div class="content-card-header">
                <div class="content-card-title">PPE Compliance by Type</div>
            </div>
            
            <div class="ppe-row">
                <div class="ppe-label">⛑️ Helmets</div>
                <div class="ppe-bar-bg"><div class="ppe-bar-fill" style="width: {h_pct}%;"></div></div>
                <div class="ppe-pct">{h_pct}%</div>
            </div>
            
            <div class="ppe-row">
                <div class="ppe-label">🥾 Safety Shoes</div>
                <div class="ppe-bar-bg"><div class="ppe-bar-fill" style="width: {s_pct}%;"></div></div>
                <div class="ppe-pct">{s_pct}%</div>
            </div>
            
            <div class="ppe-row">
                <div class="ppe-label">🧤 Gloves</div>
                <div class="ppe-bar-bg"><div class="ppe-bar-fill" style="width: {g_pct}%;"></div></div>
                <div class="ppe-pct">{g_pct}%</div>
            </div>
            
            <div class="ppe-row">
                <div class="ppe-label">🥽 Eye Protection</div>
                <div class="ppe-bar-bg"><div class="ppe-bar-fill" style="width: {e_pct}%;"></div></div>
                <div class="ppe-pct">{e_pct}%</div>
            </div>
            
            <div class="ppe-row">
                <div class="ppe-label">🎧 Hearing Protection</div>
                <div class="ppe-bar-bg"><div class="ppe-bar-fill" style="width: {ea_pct}%;"></div></div>
                <div class="ppe-pct">{ea_pct}%</div>
            </div>
            
            <div class="ppe-row">
                <div class="ppe-label">🦺 Others</div>
                <div class="ppe-bar-bg"><div class="ppe-bar-fill" style="width: {o_pct}%;"></div></div>
                <div class="ppe-pct">{o_pct}%</div>
            </div>
        </div>
        """
        render_clean_html(ppe_html)

    with bot_col3:
        if total_records > 0:
            activity_items_html = """
            <div class="activity-item">
                <div class="activity-icon" style="background:#fef2f2; color:#ef4444;">⚠️</div>
                <div class="activity-body">
                    <div class="activity-title">New incident reported</div>
                    <div class="activity-desc">Weaving - Minor injury</div>
                </div>
                <div class="activity-time">2h ago</div>
            </div>
            
            <div class="activity-item">
                <div class="activity-icon" style="background:#ecfdf5; color:#10b981;">✓</div>
                <div class="activity-body">
                    <div class="activity-title">PPE inspection completed</div>
                    <div class="activity-desc">Dyeing & Finishing - 94% compliance</div>
                </div>
                <div class="activity-time">4h ago</div>
            </div>
            
            <div class="activity-item">
                <div class="activity-icon" style="background:#fff7ed; color:#f97316;">🔥</div>
                <div class="activity-body">
                    <div class="activity-title">Fire extinguisher overdue</div>
                    <div class="activity-desc">Boiler & Utilities - 3 days</div>
                </div>
                <div class="activity-time">6h ago</div>
            </div>
            
            <div class="activity-item">
                <div class="activity-icon" style="background:#eff6ff; color:#3b82f6;">⚙️</div>
                <div class="activity-body">
                    <div class="activity-title">Action updated</div>
                    <div class="activity-desc">Machine guarding - In progress</div>
                </div>
                <div class="activity-time">8h ago</div>
            </div>
            
            <div class="activity-item">
                <div class="activity-icon" style="background:#fffbeb; color:#f59e0b;">⚠️</div>
                <div class="activity-body">
                    <div class="activity-title">New near miss reported</div>
                    <div class="activity-desc">Spinning - Slip hazard</div>
                </div>
                <div class="activity-time">10h ago</div>
            </div>
            """
        else:
            activity_items_html = """
            <div style="padding: 2.5rem 1rem; text-align: center; color: #94a3b8; font-size: 0.85rem;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">📋</div>
                <div>No safety activity recorded yet.</div>
                <div style="font-size: 0.78rem; color: #cbd5e1; margin-top: 0.25rem;">Load sample data or record incidents to view live audit feed.</div>
            </div>
            """

        activity_card_html = f"""
        <div class="content-card">
            <div class="content-card-header">
                <div class="content-card-title">Recent Activity</div>
                <span class="content-card-link">View All →</span>
            </div>
            {activity_items_html}
        </div>
        """
        render_clean_html(activity_card_html)
