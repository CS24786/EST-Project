"""
TextileSafe - System Settings & Administration Module
Provides:
- One-click Sample Data Loading (~650 realistic records calibrated to benchmark)
- Factory Reset / Wipe All Data with safeguards
- User Management & Password Reset (supports short usernames and roles)
- System Information and Database Diagnostics
"""

import os
import streamlit as st
import pandas as pd
from database.db import get_db_stats, wipe_all_data, get_connection, execute_query, DB_PATH
from database.seed_data import seed_database
from config import ROLES

def render_settings():
    """Renders the settings and system administration console."""
    st.markdown("""
        <div>
            <h1 class="page-title">Settings & System Administration</h1>
            <div class="page-subtitle">Manage sample synthetic data, system database state, user accounts, and credentials.</div>
        </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["💾 Sample Data & Database Controls", "👥 User Management & Password Reset", "⚙️ System Info & Health"])

    with tab1:
        st.subheader("Database State & Operational Data Management")
        
        # Display current record counts
        stats = get_db_stats()
        c1, c2, c3, c4, c5, c6 = st.columns(6)
        c1.metric("Incidents", stats.get("incidents", 0))
        c2.metric("PPE Audits", stats.get("ppe_inspections", 0))
        c3.metric("Fire Audits", stats.get("fire_inspections", 0))
        c4.metric("Hazards", stats.get("hazards", 0))
        c5.metric("CAPA Actions", stats.get("corrective_actions", 0))
        c6.metric("Users", stats.get("users", 0))

        st.markdown("<hr style='border-color:#e2e8f0; margin:1.5rem 0;'>", unsafe_allow_html=True)

        col_seed, col_wipe = st.columns(2)

        with col_seed:
            st.markdown("""
            <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:12px; padding:1.25rem;">
                <div style="font-size:1.1rem; font-weight:700; color:#0c2340;">🌱 Load Sample Synthetic Data</div>
                <div style="font-size:0.85rem; color:#64748b; margin-top:0.35rem; margin-bottom:1rem;">
                    Populates the database with <b>~650 realistic textile manufacturing safety records</b> covering 12 months (2025).
                    Calibrated to match the executive dashboard benchmarks: <b>42 Incidents, 28 Near Misses, 93% PPE, 96% Fire Safety, 12 Open Actions</b>.
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("🚀 Load / Reset to Benchmark Sample Data", type="primary", width="stretch"):
                with st.spinner("Seeding database with 12-month synthetic records..."):
                    seed_database(force_reload=True)
                st.success("Successfully seeded ~650 realistic textile safety records! Dashboard is fully updated.")
                st.rerun()

        with col_wipe:
            st.markdown("""
            <div style="background:#ffffff; border:1px solid #fee2e2; border-radius:12px; padding:1.25rem;">
                <div style="font-size:1.1rem; font-weight:700; color:#ef4444;">⚠️ Wipe All Operational Data</div>
                <div style="font-size:0.85rem; color:#64748b; margin-top:0.35rem; margin-bottom:1rem;">
                    Purges all records from <b>incidents, PPE inspections, fire audits, hazards, and CAPAs</b>.
                    Table schemas and user credentials are preserved. Resets all modules to zero data.
                </div>
            </div>
            """, unsafe_allow_html=True)

            wipe_confirm = st.checkbox("I understand this will permanently delete all operational records (reset to zero)", key="wipe_chk")
            if st.button("🗑️ Wipe All Data", type="secondary", width="stretch"):
                if wipe_confirm:
                    wipe_all_data()
                    st.warning("All operational records have been wiped clean. Database is at zero records.")
                    st.rerun()
                else:
                    st.error("Please tick the confirmation checkbox above before wiping data.")

    with tab2:
        st.subheader("User Accounts & Password Management")

        # Load users
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, name, email, role, created_at FROM users")
        users = [dict(r) for r in cursor.fetchall()]
        conn.close()

        df_users = pd.DataFrame(users)
        st.write("Registered System Accounts:")
        st.dataframe(df_users[["id", "username", "name", "email", "role", "created_at"]], width="stretch")

        st.markdown("<hr style='border-color:#e2e8f0; margin:1.5rem 0;'>", unsafe_allow_html=True)

        col_pw, col_add_u = st.columns(2)

        with col_pw:
            st.markdown("<h4 style='color:#0c2340;'>🔑 Reset User Password</h4>", unsafe_allow_html=True)
            user_options = [f"{u.get('username', 'user')} ({u['name']} - {u['role']})" for u in users]
            target_user_str = st.selectbox("Select User Account to Reset", user_options, key="settings_reset_user")
            new_pass = st.text_input("Enter New Password", type="password", key="settings_new_pw", autocomplete="new-password")
            confirm_new_pass = st.text_input("Confirm New Password", type="password", key="settings_conf_pw", autocomplete="new-password")

            if st.button("Update User Password", type="primary"):
                if not new_pass or new_pass != confirm_new_pass:
                    st.error("Passwords must match and cannot be empty.")
                else:
                    sel_username = target_user_str.split()[0]
                    execute_query("UPDATE users SET password = ? WHERE LOWER(username) = LOWER(?)", (new_pass.strip(), sel_username))
                    st.success(f"Password for user '{sel_username}' successfully updated!")

        with col_add_u:
            st.markdown("<h4 style='color:#0c2340;'>➕ Create New User Account</h4>", unsafe_allow_html=True)
            with st.form("new_user_form"):
                u_uname = st.text_input("System Username", "lead", autocomplete="username")
                u_name = st.text_input("Full Name", "Engr. Farhan Saeed")
                u_email = st.text_input("Corporate Email", "farhan.saeed@textilesafe.com")
                u_role = st.selectbox("Assigned System Role", ROLES)
                u_pass = st.text_input("Initial Password", "lead123", type="password", autocomplete="new-password")

                create_u_btn = st.form_submit_button("Register User", type="secondary")

                if create_u_btn:
                    try:
                        execute_query(
                            "INSERT INTO users (username, name, email, role, password) VALUES (?, ?, ?, ?, ?)",
                            (u_uname.strip(), u_name.strip(), u_email.strip(), u_role, u_pass.strip())
                        )
                        st.success(f"User '{u_uname}' ({u_name}) registered successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error registering user: {str(e)}")

    with tab3:
        st.subheader("System Information & Environment Diagnostics")
        
        db_size_kb = round(os.path.getsize(DB_PATH) / 1024, 2) if os.path.exists(DB_PATH) else 0

        info_data = [
            ("Application Name", "TextileSafe - Occupational Health & Safety Compliance Analysis"),
            ("Version", "2.5.0 Enterprise"),
            ("Database Engine", f"SQLite 3 ({DB_PATH})"),
            ("Database Size", f"{db_size_kb} KB"),
            ("Active User", st.session_state.get("user", {}).get("name", "Talha Nawaz")),
            ("Active Role", st.session_state.get("user", {}).get("role", "Safety Manager")),
            ("Web Framework", "Streamlit 1.66+"),
            ("Visual Engine", "Plotly 7.1.0"),
            ("Reporting Modules", "ReportLab 5.1 (PDF) + OpenPyXL 3.1.5 (Excel)")
        ]

        df_info = pd.DataFrame(info_data, columns=["System Parameter", "Configuration Value"])
        st.dataframe(df_info, width="stretch")
