"""
TextileSafe - Reports & Data Management Module
Provides Excel workbook export, ReportLab PDF download, CSV/Excel file import with validation,
and comprehensive OHS Data Dictionary.
"""

import streamlit as st
import pandas as pd
from utils.export_excel import create_styled_excel_report, create_sample_import_template
from utils.export_pdf import generate_pdf_report
from database.db import query_dataframe, execute_query

def render_reports():
    """Renders the Reports and Data Management center."""
    st.markdown("""
        <div>
            <h1 class="page-title">Reports & Data Management</h1>
            <div class="page-subtitle">Generate regulatory audit exports, import batch spreadsheets, and inspect data dictionaries.</div>
        </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📑 Export Reports (PDF & Excel)", "📥 Import Data & Validation", "📖 OHS Data Dictionary"])

    with tab1:
        st.subheader("Official OHS Compliance Deliverables")
        st.write("Generate and download comprehensive executive safety reports for management review, customer compliance audits (WRAP, OEKO-TEX, SEDEX), and regulatory compliance.")

        col_pdf, col_excel = st.columns(2)

        with col_pdf:
            st.markdown("""
            <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:12px; padding:1.5rem; text-align:center;">
                <div style="font-size:3rem; margin-bottom:0.5rem;">📄</div>
                <div style="font-size:1.15rem; font-weight:700; color:#0f2b48;">Executive OHS Compliance PDF</div>
                <div style="font-size:0.85rem; color:#64748b; margin-top:0.25rem; margin-bottom:1.25rem;">
                    Formal multi-page audit report with KPI benchmarks, department risk heatmaps, and evidence-based industrial controls.
                </div>
            </div>
            """, unsafe_allow_html=True)

            user = st.session_state.get("user", {})
            pdf_bytes = generate_pdf_report(
                author_name=user.get("name", "Talha Nawaz"),
                author_role=user.get("role", "Safety Manager")
            )
            st.download_button(
                label="⬇️ Download Executive PDF Report",
                data=pdf_bytes,
                file_name="TextileSafe_OHS_Executive_Report_2025.pdf",
                mime="application/pdf",
                type="primary",
                width="stretch"
            )

        with col_excel:
            st.markdown("""
            <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:12px; padding:1.5rem; text-align:center;">
                <div style="font-size:3rem; margin-bottom:0.5rem;">📊</div>
                <div style="font-size:1.15rem; font-weight:700; color:#0f2b48;">Complete Multi-Tab Excel Workbook</div>
                <div style="font-size:0.85rem; color:#64748b; margin-top:0.25rem; margin-bottom:1.25rem;">
                    Fully styled OpenPyXL workbook containing raw datasets for Incidents, PPE, Fire Safety, Hazards, and CAPA.
                </div>
            </div>
            """, unsafe_allow_html=True)

            excel_bytes = create_styled_excel_report()
            st.download_button(
                label="⬇️ Download Comprehensive Excel Workbook",
                data=excel_bytes,
                file_name="TextileSafe_Mill_Safety_Data_2025.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                type="secondary",
                width="stretch"
            )

    with tab2:
        st.subheader("Import Safety Records (CSV / Excel)")
        st.write("Upload standardized incident records to populate the system in batch mode.")

        # Download sample template
        template_bytes = create_sample_import_template()
        st.download_button(
            label="📄 Download Standard Incident Import Template (Excel)",
            data=template_bytes,
            file_name="TextileSafe_Import_Template.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])

        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith(".csv"):
                    df_upload = pd.read_csv(uploaded_file)
                else:
                    df_upload = pd.read_excel(uploaded_file)

                st.success(f"File loaded successfully: {len(df_upload)} records detected.")
                st.write("Data Preview & Validation:")
                st.dataframe(df_upload.head(5), width="stretch")

                required_cols = ["incident_code", "incident_type", "department", "severity", "incident_date"]
                missing = [c for c in required_cols if c not in df_upload.columns]

                if missing:
                    st.error(f"Validation Error: Missing required columns: {', '.join(missing)}")
                else:
                    st.info("Validation passed: All mandatory safety fields present.")
                    if st.button("Confirm and Commit to Database", type="primary"):
                        success_count = 0
                        dup_count = 0
                        for _, r in df_upload.iterrows():
                            try:
                                execute_query("""
                                    INSERT INTO incidents (
                                        incident_code, incident_type, department, shift, severity,
                                        incident_date, root_cause, description, injured_person,
                                        lost_workdays, reported_by, status
                                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                                """, (
                                    str(r.get("incident_code", "")),
                                    str(r.get("incident_type", "Near Miss")),
                                    str(r.get("department", "Spinning")),
                                    str(r.get("shift", "Morning (06:00 - 14:00)")),
                                    str(r.get("severity", "Minor")),
                                    str(r.get("incident_date", "2025-01-01")),
                                    str(r.get("root_cause", "Unspecified")),
                                    str(r.get("description", "")),
                                    str(r.get("injured_person", "None")),
                                    int(r.get("lost_workdays", 0) if pd.notnull(r.get("lost_workdays")) else 0),
                                    str(r.get("reported_by", "Batch Import")),
                                    str(r.get("status", "Closed"))
                                ))
                                success_count += 1
                            except Exception:
                                dup_count += 1

                        st.success(f"Batch import completed: {success_count} records committed. ({dup_count} duplicate codes skipped)")
            except Exception as e:
                st.error(f"Error parsing uploaded file: {str(e)}")

    with tab3:
        st.subheader("Industrial OHS Data Dictionary")
        st.write("Technical metadata schema, data types, and compliance standards utilized by the TextileSafe system.")

        dict_data = [
            ("incident_code", "TEXT", "UNIQUE NOT NULL", "Unique standardized incident identifier (e.g. INC-2025-001)"),
            ("incident_type", "TEXT", "CHECK (IN types)", "Accident (Lost Time), Accident (No Lost Time), Near Miss, Unsafe Act"),
            ("department", "TEXT", "FOREIGN KEY", "Spinning, Weaving, Knitting, Dyeing & Finishing, Cutting, Boiler, Warehouse"),
            ("shift", "TEXT", "NOT NULL", "Morning (06-14h), Evening (14-22h), Night (22-06h)"),
            ("severity", "TEXT", "NOT NULL", "Minor, Moderate, Major, Critical based on clinical intervention criteria"),
            ("lost_workdays", "INTEGER", "DEFAULT 0", "Total calendar days employee was absent from work (OSHA 1904 standard)"),
            ("risk_score", "INTEGER", "1 to 25", "Mathematical product: Likelihood (1-5) * Severity (1-5)"),
            ("risk_level", "TEXT", "NOT NULL", "Low (1-4), Medium (5-9), High (10-16), Critical (17-25)"),
            ("overall_compliance_pct", "REAL", "0.0 - 100.0%", "Aggregated arithmetic mean of 6 critical PPE categories observed in audit")
        ]

        df_dict = pd.DataFrame(dict_data, columns=["Column Name", "Data Type", "Constraints", "Operational Definition"])
        st.dataframe(df_dict, width="stretch", height=360)
