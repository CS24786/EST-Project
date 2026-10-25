"""
TextileSafe - Occupational Health & Safety Compliance Analysis
Main Application Controller and Router.
Features:
- Starts at Login screen by default
- Zero-data clean initial state (load sample data on demand in Settings)
- Role-Based Access Control (RBAC) across Admin, Supervisor, Officer, Auditor, Head
- High-contrast prominent sidebar controls (Sector Filter & Logout)
- Topbar deploy and chrome elements hidden
- Instant, zero-lag module switching
"""

import streamlit as st

# Configure page settings
st.set_page_config(
    page_title="TextileSafe - OHS Analytics & Compliance",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

from utils.styles import get_custom_css, render_footer
from database.db import init_db
from modules.auth import render_login_page
from modules.dashboard import render_dashboard
from modules.incidents import render_incidents
from modules.ppe import render_ppe
from modules.fire_safety import render_fire_safety
from modules.risk_assessment import render_risk_assessment
from modules.corrective_actions import render_corrective_actions
from modules.reports import render_reports
from modules.settings import render_settings
from config import DEPARTMENTS, APP_NAME, ROLE_PERMISSIONS

# Inject Custom Industrial CSS (forces strict Light Theme & hides Deploy button)
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Initialize Database schema once (prevents lag on sidebar navigation)
@st.cache_resource
def setup_database_once():
    init_db()
    return True

setup_database_once()

# -------------------------------------------------------------
# 1. AUTHENTICATION STATE GUARD (Login Screen First!)
# -------------------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state.get("logged_in", False):
    render_login_page()
    st.stop()

# Get currently authenticated user and role
current_user = st.session_state.get("user", {
    "username": "admin",
    "name": "Talha Nawaz",
    "role": "Safety Manager"
})
user_role = current_user.get("role", "Safety Manager")

# -------------------------------------------------------------
# 2. ROLE-BASED ACCESS CONTROL (RBAC) NAVIGATION
# -------------------------------------------------------------
allowed_modules = ROLE_PERMISSIONS.get(user_role, ROLE_PERMISSIONS["Safety Manager"])

all_nav_items = [
    ("Dashboard", "🏠  Dashboard"),
    ("Incidents & Near Misses", "⚠️  Incidents & Near Misses"),
    ("PPE Compliance", "⛑️  PPE Compliance"),
    ("Fire-Safety Inspections", "🔥  Fire-Safety Inspections"),
    ("Risk Assessment", "📊  Risk Assessment"),
    ("Corrective Actions", "☑️  Corrective Actions"),
    ("Reports & Data", "📄  Reports & Data"),
    ("Settings & System", "⚙️  Settings & System")
]

# Filter sidebar navigation items based on user's authorized role permissions
nav_options = [label for key, label in all_nav_items if key in allowed_modules]

with st.sidebar:
    # Sidebar Brand Header
    st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 0.75rem; padding: 0.5rem 0 1.25rem 0;">
        <div style="width: 40px; height: 40px; background: rgba(255,255,255,0.12); border: 1px solid rgba(255,255,255,0.25); border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 1.4rem;">
            🛡️
        </div>
        <div>
            <div style="font-size: 1.3rem; font-weight: 800; color: #ffffff; letter-spacing: -0.01em; line-height: 1.1;">{APP_NAME}</div>
            <div style="font-size: 0.75rem; color: #94a3b8; font-weight: 500;">OHS Analytics & Compliance</div>
        </div>
    </div>
    <hr style="border-color: #1e3a5f; margin: 0 0 1rem 0;">
    """, unsafe_allow_html=True)

    selected_nav = st.radio("Navigation", nav_options, index=0, label_visibility="collapsed")

    st.markdown("<hr style='border-color: #1e3a5f; margin: 1.25rem 0 0.85rem 0;'>", unsafe_allow_html=True)

    # Department Filter in sidebar - High Contrast & Prominent
    st.markdown("<div style='font-size:0.78rem; font-weight:700; color:#38bdf8; text-transform:uppercase; margin-bottom:0.35rem; letter-spacing:0.03em;'>Global Sector Filter</div>", unsafe_allow_html=True)
    selected_dept = st.selectbox(
        "Department Filter",
        ["All"] + DEPARTMENTS,
        index=0,
        label_visibility="collapsed"
    )

    st.markdown("<div style='height: 2.5rem;'></div>", unsafe_allow_html=True)

    # Bottom Branding & User Info
    st.markdown(f"""
    <div style="background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.12); border-radius: 10px; padding: 0.85rem; font-size: 0.82rem; margin-bottom: 0.85rem;">
        <div style="font-weight: 700; color: #ffffff; margin-bottom: 0.25rem;">Textile Manufacturing</div>
        <div style="color: #cbd5e1;">Active Role: <b style="color:#38bdf8; font-weight:800;">{user_role}</b></div>
        <div style="color: #94a3b8; font-size: 0.74rem; margin-top: 0.25rem;">Signed In: {current_user.get('name', 'Talha Nawaz')}</div>
    </div>
    """, unsafe_allow_html=True)

    # High Contrast Logout Button in Sidebar
    if st.button("🚪 Logout", width="stretch"):
        st.session_state["logged_in"] = False
        st.session_state.pop("user", None)
        st.rerun()

# -------------------------------------------------------------
# 3. INTERACTIVE TOP HEADER & DATE RANGE FILTER BAR
# -------------------------------------------------------------
user_display_name = current_user.get("name", "Talha Nawaz")
initials = "".join([part[0] for part in user_role.split()][:2]).upper() if user_role else "OHS"

top_col_search, top_col_date, top_col_notif, top_col_role, top_col_signout = st.columns([30, 28, 5, 23, 14])

with top_col_search:
    search_query = st.text_input("Search", placeholder="🔍 Search safety records, hazards...", label_visibility="collapsed")

with top_col_date:
    date_presets = {
        "📅 Jan 01, 2025 - Dec 31, 2025 (Full Year)": ("2025-01-01", "2025-12-31"),
        "📅 Jan 01, 2025 - Mar 31, 2025 (Q1 2025)": ("2025-01-01", "2025-03-31"),
        "📅 Apr 01, 2025 - Jun 30, 2025 (Q2 2025)": ("2025-04-01", "2025-06-30"),
        "📅 Jul 01, 2025 - Sep 30, 2025 (Q3 2025)": ("2025-07-01", "2025-09-30"),
        "📅 Oct 01, 2025 - Dec 31, 2025 (Q4 2025)": ("2025-10-01", "2025-12-31"),
        "📅 Jul 01, 2025 - Dec 31, 2025 (Last 6 Months)": ("2025-07-01", "2025-12-31"),
    }
    selected_preset_label = st.selectbox("Date Range", list(date_presets.keys()), index=0, label_visibility="collapsed")
    active_date_range = date_presets[selected_preset_label]

with top_col_notif:
    st.markdown("""
        <div style="display:flex; justify-content:center; align-items:center; height:100%; padding-top:4px;">
            <div class="notif-bell" title="3 Active Safety Alerts">
                🔔<span class="notif-badge">3</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

with top_col_role:
    st.markdown(f"""
        <div class="user-pill" title="{user_display_name} - {user_role}">
            <div class="user-avatar">{initials}</div>
            <div style="line-height:1.2; overflow:hidden;">
                <div style="font-size:0.86rem; font-weight:800; color:#0c2340; white-space:nowrap; text-overflow:ellipsis; overflow:hidden;">{user_role}</div>
                <div style="font-size:0.72rem; color:#64748b; font-weight:500; white-space:nowrap; text-overflow:ellipsis; overflow:hidden;">{user_display_name}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with top_col_signout:
    if st.button("🚪 Sign Out", key="top_header_signout_btn", width="stretch"):
        st.session_state["logged_in"] = False
        st.session_state.pop("user", None)
        st.rerun()

st.markdown("<hr style='border-color:#e2e8f0; margin:0.85rem 0 1.25rem 0;'>", unsafe_allow_html=True)

# -------------------------------------------------------------
# 4. INSTANT ROUTER
# -------------------------------------------------------------
if "Dashboard" in selected_nav:
    render_dashboard(date_filter=active_date_range, department_filter=selected_dept)
elif "Incidents" in selected_nav:
    render_incidents()
elif "PPE" in selected_nav:
    render_ppe()
elif "Fire-Safety" in selected_nav:
    render_fire_safety()
elif "Risk Assessment" in selected_nav:
    render_risk_assessment()
elif "Corrective Actions" in selected_nav:
    render_corrective_actions()
elif "Reports & Data" in selected_nav:
    render_reports()
elif "Settings" in selected_nav:
    render_settings()

# Standard Footer
st.markdown(render_footer(), unsafe_allow_html=True)
