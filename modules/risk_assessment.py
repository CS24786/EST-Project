"""
TextileSafe - Textile Risk Assessment Module
Configurable 5x5 Risk Matrix: Risk Score = Likelihood x Severity.
Sector-specific hazards across Spinning, Weaving, Knitting, Dyeing, Cutting, Boiler, Warehouse.
Interactive Heatmap, ISO 45001 / ILO guidelines, and hierarchy of hazard controls.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from database.db import query_dataframe, execute_query
from config import DEPARTMENTS, HAZARD_TYPES, LIKELIHOOD_LEVELS, SEVERITY_LEVELS, get_risk_level

def render_risk_assessment():
    """Renders the 5x5 Risk Matrix and Textile Hazard Assessment module."""
    st.markdown("""
        <div>
            <h1 class="page-title">Textile Hazard & Risk Assessment (5×5 Matrix)</h1>
            <div class="page-subtitle">Standardized occupational risk profiling aligned with ISO 45001 & ILO textiles guidelines.</div>
        </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["🗺️ Risk Matrix & Heatmap", "🏭 Department Risk Profiles", "📋 Hazard Register", "➕ Conduct Hazard Assessment"])

    haz_df = query_dataframe("SELECT * FROM hazards ORDER BY risk_score DESC")

    with tab1:
        st.markdown("""
        <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:12px; padding:1.25rem; margin-bottom:1.5rem;">
            <div style="font-size:1.1rem; font-weight:700; color:#0f2b48; margin-bottom:0.25rem;">Standard 5×5 Risk Assessment Matrix</div>
            <div style="font-size:0.85rem; color:#64748b; margin-bottom:1rem;">
                <b>Risk Score = Likelihood (1–5) × Severity (1–5)</b> &bull; Thresholds:
                <span class="risk-badge risk-low" style="margin-left:0.5rem;">Low (1-4)</span>
                <span class="risk-badge risk-medium">Medium (5-9)</span>
                <span class="risk-badge risk-high">High (10-16)</span>
                <span class="risk-badge risk-critical">Critical (17-25)</span>
            </div>
        """, unsafe_allow_html=True)

        # Build 5x5 grid visualization
        matrix_data = []
        for l in range(5, 0, -1):  # Likelihood on Y-axis (5 down to 1)
            row = []
            for s in range(1, 6):   # Severity on X-axis (1 to 5)
                score = l * s
                count = len(haz_df[(haz_df["likelihood"] == l) & (haz_df["severity"] == s)])
                row.append(f"Score: {score}<br>({count} Hazards)")
            matrix_data.append(row)

        fig_matrix = go.Figure(data=go.Heatmap(
            z=[[l*s for s in range(1, 6)] for l in range(5, 0, -1)],
            x=["1: Insignificant", "2: Minor", "3: Moderate", "4: Major", "5: Catastrophic"],
            y=["5: Almost Certain", "4: Likely", "3: Possible", "2: Unlikely", "1: Rare"],
            colorscale=[
                [0.0, "#d1fae5"],
                [0.16, "#a7f3d0"],
                [0.36, "#fef3c7"],
                [0.64, "#ffedd5"],
                [1.0, "#fee2e2"]
            ],
            showscale=False,
            text=matrix_data,
            texttemplate="%{text}",
            textfont={"size": 11, "family": "Plus Jakarta Sans"}
        ))

        fig_matrix.update_layout(
            height=340,
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis_title="Severity (Consequence)",
            yaxis_title="Likelihood (Probability)",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_matrix, width="stretch")
        st.markdown("</div>", unsafe_allow_html=True)

    with tab2:
        st.subheader("Department-Wise Textile Hazard Comparison")
        if not haz_df.empty:
            dept_scores = haz_df.groupby("department")["risk_score"].mean().round(1).reset_index()
            dept_scores = dept_scores.sort_values(by="risk_score", ascending=False)

            fig_bar_risk = px.bar(
                dept_scores,
                x="department",
                y="risk_score",
                color="risk_score",
                color_continuous_scale=["#10b981", "#f59e0b", "#f97316", "#ef4444"],
                labels={"risk_score": "Average Risk Score", "department": "Textile Sector"}
            )
            fig_bar_risk.add_hline(y=16, line_dash="dot", line_color="#ef4444", annotation_text="Critical Threshold (17+)")
            fig_bar_risk.add_hline(y=9, line_dash="dash", line_color="#f97316", annotation_text="High Risk Threshold (10+)")
            fig_bar_risk.update_layout(height=320, margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", coloraxis_showscale=False)
            st.plotly_chart(fig_bar_risk, width="stretch")

            # High Risk Hotspots Table
            st.markdown("<h4 style='color:#0f2b48; margin-top:1.5rem;'>Top Priority Textile Mill Hazards (Score ≥ 12)</h4>", unsafe_allow_html=True)
            high_hazards = haz_df[haz_df["risk_score"] >= 12]
            st.dataframe(
                high_hazards[["hazard_code", "department", "hazard_category", "specific_hazard", "risk_score", "risk_level", "recommended_controls"]],
                width="stretch",
                height=260
            )

    with tab3:
        st.subheader("Textile Mill Hazard Register")
        f_dep = st.selectbox("Select Department", ["All"] + DEPARTMENTS, key="haz_tab3_dep")
        f_lvl = st.selectbox("Select Risk Level", ["All", "Critical", "High", "Medium", "Low"], key="haz_tab3_lvl")

        filtered_haz = haz_df.copy()
        if f_dep != "All":
            filtered_haz = filtered_haz[filtered_haz["department"] == f_dep]
        if f_lvl != "All":
            filtered_haz = filtered_haz[filtered_haz["risk_level"] == f_lvl]

        st.caption(f"Showing {len(filtered_haz)} hazard entries")
        st.dataframe(
            filtered_haz[["hazard_code", "department", "hazard_category", "specific_hazard", "likelihood", "severity", "risk_score", "risk_level", "existing_controls", "recommended_controls"]],
            width="stretch",
            height=380
        )

    with tab4:
        st.subheader("Log a New Hazard Assessment")
        with st.form("new_hazard_form"):
            c1, c2 = st.columns(2)
            with c1:
                h_dept = st.selectbox("Textile Sector", DEPARTMENTS, key="new_h_dept")
                h_cat = st.selectbox("Hazard Category", HAZARD_TYPES, key="new_h_cat")
                h_spec = st.text_input("Specific Hazard Description", "Unguarded draw frame nip roller nip point")
            with c2:
                h_like = st.slider("Likelihood (1: Rare -> 5: Almost Certain)", 1, 5, 3)
                h_sev = st.slider("Severity (1: Insignificant -> 5: Catastrophic)", 1, 5, 4)
                score_preview = h_like * h_sev
                lvl_preview = get_risk_level(score_preview)["label"]
                st.info(f"Calculated Score: **{score_preview}** | Classification: **{lvl_preview}**")

            c_ctrl1, c_ctrl2 = st.columns(2)
            with c_ctrl1:
                ext_ctrl = st.text_input("Existing Safeguards / Engineering Controls", "Operator visual warning sign posted.")
            with c_ctrl2:
                rec_ctrl = st.text_input("Recommended Hierarchy Controls", "Install interlocked mechanical barrier with emergency brake stop.")

            sub_haz = st.form_submit_button("Record Hazard Assessment", type="primary", width="stretch")

            if sub_haz:
                score = h_like * h_sev
                lvl = get_risk_level(score)["label"]
                new_code = f"HAZ-2025-{len(haz_df)+101:03d}"

                execute_query("""
                    INSERT INTO hazards (
                        hazard_code, department, hazard_category, specific_hazard,
                        likelihood, severity, risk_score, risk_level,
                        existing_controls, recommended_controls, assessment_date
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    new_code, h_dept, h_cat, h_spec,
                    h_like, h_sev, score, lvl,
                    ext_ctrl, rec_ctrl, "2025-10-25"
                ))
                st.success(f"Hazard {new_code} saved with {lvl} priority ({score}).")
                st.rerun()
