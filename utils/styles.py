"""
TextileSafe - Custom CSS and Design System
Provides modern, enterprise industrial styling matching the UI mockup:
- Navy blue primary palette
- Clean white card layout
- Responsive sidebar navigation with high-contrast visible dropdown & logout button
- Top deploy button and default toolbars completely hidden
- Strict Light Theme enforcement across all browsers & OS dark modes
"""

def get_custom_css():
    return """
    <style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

    /* STRICT LIGHT THEME ENFORCEMENT */
    :root {
        color-scheme: light !important;
        --navy-dark: #0a192f;
        --navy-primary: #0c2340;
        --navy-sidebar: #0b1f35;
        --navy-hover: #16385e;
        --blue-accent: #2563eb;
        --blue-active: #1d4ed8;
        --blue-light: #3b82f6;
        --bg-main: #f4f6f9;
        --card-bg: #ffffff;
        --border-color: #e2e8f0;
        --text-primary: #0f172a;
        --text-secondary: #64748b;
        --text-light: #94a3b8;
        --success: #10b981;
        --warning: #f59e0b;
        --high-risk: #f97316;
        --critical: #ef4444;
        --purple: #8b5cf6;
    }

    /* Completely Hide Deploy Button, Header Toolbar, and Streamlit Status */
    .stAppDeployButton,
    .stDeployButton,
    header[data-testid="stHeader"],
    [data-testid="stToolbar"],
    [data-testid="stDecoration"],
    [data-testid="stStatusWidget"],
    #MainMenu,
    footer {
        display: none !important;
        visibility: hidden !important;
        height: 0px !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    /* Force Light Background on Main App */
    html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stMainBlockContainer"], .main {
        background-color: #f4f6f9 !important;
        color: #0f172a !important;
        font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    /* Container Spacing */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 2.5rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 100% !important;
    }

    /* Login Form - Remember Me & Right-Aligned Forgot Password */
    form[data-testid="stForm"] div[data-testid="column"]:nth-child(2),
    div[data-testid="stForm"] div[data-testid="stColumn"]:nth-child(2),
    div[data-testid="stForm"] div[data-testid="column"]:nth-child(2) {
        display: flex !important;
        justify-content: flex-end !important;
        align-items: center !important;
        text-align: right !important;
    }
    form[data-testid="stForm"] div[data-testid="column"]:nth-child(2) div[data-testid="stFormSubmitButton"],
    div[data-testid="stForm"] div[data-testid="stColumn"]:nth-child(2) div[data-testid="stFormSubmitButton"],
    div[data-testid="stForm"] div[data-testid="column"]:nth-child(2) div[data-testid="stFormSubmitButton"] {
        display: flex !important;
        justify-content: flex-end !important;
        margin-left: auto !important;
        width: 100% !important;
    }
    form[data-testid="stForm"] div[data-testid="column"]:nth-child(2) button,
    div[data-testid="stForm"] div[data-testid="stColumn"]:nth-child(2) button,
    div[data-testid="stForm"] div[data-testid="column"]:nth-child(2) button {
        background: transparent !important;
        border: none !important;
        color: #2563eb !important;
        font-weight: 600 !important;
        font-size: 0.86rem !important;
        padding: 0.2rem 0 !important;
        box-shadow: none !important;
        float: right !important;
        margin-left: auto !important;
        text-decoration: none !important;
        cursor: pointer !important;
    }
    form[data-testid="stForm"] div[data-testid="column"]:nth-child(2) button:hover,
    div[data-testid="stForm"] div[data-testid="stColumn"]:nth-child(2) button:hover,
    div[data-testid="stForm"] div[data-testid="column"]:nth-child(2) button:hover {
        color: #1d4ed8 !important;
        text-decoration: underline !important;
        background: transparent !important;
    }

    /* User Profile Pill */
    .user-pill {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        background: #ffffff;
        border: 1px solid var(--border-color);
        padding: 0.35rem 0.85rem;
        border-radius: 30px;
        font-size: 0.85rem;
        font-weight: 600;
        color: var(--text-primary);
        box-shadow: 0 1px 3px rgba(0,0,0,0.03);
    }
    .user-avatar {
        width: 32px;
        height: 32px;
        background: #0c2340;
        color: #ffffff;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    .notif-bell {
        position: relative;
        cursor: pointer;
        font-size: 1.2rem;
        color: var(--text-secondary);
        display: flex;
        align-items: center;
    }
    .notif-badge {
        position: absolute;
        top: -5px;
        right: -8px;
        background: var(--critical);
        color: white;
        font-size: 0.65rem;
        font-weight: 700;
        padding: 1px 5px;
        border-radius: 10px;
    }

    /* Page Header */
    .page-title {
        font-size: 1.75rem;
        font-weight: 800;
        color: #0c2340;
        margin: 0;
        padding: 0;
        letter-spacing: -0.02em;
    }
    .page-subtitle {
        font-size: 0.92rem;
        color: var(--text-secondary);
        margin-top: 0.2rem;
        margin-bottom: 1.25rem;
    }

    /* KPI Cards Styling */
    .kpi-card {
        background: #ffffff;
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 1.15rem 1.25rem;
        box-shadow: 0 1px 4px rgba(12, 35, 64, 0.04);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        height: 100%;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 14px rgba(12, 35, 64, 0.08);
    }
    .kpi-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.65rem;
    }
    .kpi-title {
        font-size: 0.85rem;
        font-weight: 600;
        color: #475569;
        letter-spacing: 0.01em;
    }
    .kpi-icon-wrap {
        width: 38px;
        height: 38px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.15rem;
    }
    .kpi-value {
        font-size: 2.2rem;
        font-weight: 800;
        color: #0c2340;
        line-height: 1.1;
        letter-spacing: -0.02em;
    }
    .kpi-footer {
        display: flex;
        align-items: center;
        gap: 0.4rem;
        margin-top: 0.65rem;
        font-size: 0.8rem;
    }
    .kpi-badge-green {
        color: #059669;
        font-weight: 700;
        background: #ecfdf5;
        padding: 0.15rem 0.45rem;
        border-radius: 6px;
    }
    .kpi-badge-red {
        color: #dc2626;
        font-weight: 700;
        background: #fef2f2;
        padding: 0.15rem 0.45rem;
        border-radius: 6px;
    }
    .kpi-subtext {
        color: var(--text-light);
        font-size: 0.78rem;
    }

    /* Content Cards */
    .content-card {
        background: #ffffff;
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        box-shadow: 0 1px 4px rgba(12, 35, 64, 0.04);
        margin-bottom: 1.25rem;
        height: 100%;
        overflow: hidden;
    }
    .content-card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #f1f5f9;
        padding-bottom: 0.75rem;
        margin-bottom: 0.85rem;
    }
    .content-card-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #0c2340;
        margin: 0;
    }
    .content-card-link {
        font-size: 0.85rem;
        color: var(--blue-accent);
        font-weight: 600;
        text-decoration: none;
    }

    /* Risk Heatmap Table */
    .heatmap-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.76rem;
        table-layout: fixed;
    }
    .heatmap-table th {
        color: #64748b;
        font-weight: 600;
        padding: 5px 2px;
        text-align: center;
        border-bottom: 1px solid #e2e8f0;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .heatmap-table td {
        padding: 5px 2px;
        text-align: center;
        border-bottom: 1px solid #f8fafc;
    }
    .heatmap-cell {
        border-radius: 4px;
        display: block;
        width: 100%;
        height: 18px;
    }

    /* Risk Badges */
    .risk-badge {
        display: inline-block;
        padding: 0.15rem 0.5rem;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.74rem;
        text-align: center;
        min-width: 58px;
    }
    .risk-low {
        background-color: #d1fae5;
        color: #065f46;
        border: 1px solid #a7f3d0;
    }
    .risk-medium {
        background-color: #fef3c7;
        color: #92400e;
        border: 1px solid #fde68a;
    }
    .risk-high {
        background-color: #ffedd5;
        color: #9a3412;
        border: 1px solid #fed7aa;
    }
    .risk-critical {
        background-color: #fee2e2;
        color: #991b1b;
        border: 1px solid #fecaca;
    }

    /* PPE Progress Bar */
    .ppe-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 0.85rem;
        gap: 0.75rem;
    }
    .ppe-label {
        font-size: 0.86rem;
        font-weight: 600;
        color: #1e293b;
        min-width: 130px;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .ppe-bar-bg {
        flex-grow: 1;
        height: 10px;
        background: #e2e8f0;
        border-radius: 5px;
        overflow: hidden;
    }
    .ppe-bar-fill {
        height: 100%;
        background: #2563eb;
        border-radius: 5px;
    }
    .ppe-pct {
        font-size: 0.86rem;
        font-weight: 700;
        color: #0c2340;
        min-width: 38px;
        text-align: right;
    }

    /* Activity Feed Items */
    .activity-item {
        display: flex;
        align-items: flex-start;
        gap: 0.75rem;
        padding: 0.6rem 0;
        border-bottom: 1px solid #f1f5f9;
    }
    .activity-item:last-child {
        border-bottom: none;
    }
    .activity-icon {
        width: 30px;
        height: 30px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.95rem;
        flex-shrink: 0;
    }
    .activity-body {
        flex-grow: 1;
    }
    .activity-title {
        font-size: 0.85rem;
        font-weight: 700;
        color: #0c2340;
    }
    .activity-desc {
        font-size: 0.78rem;
        color: #64748b;
        margin-top: 1px;
    }
    .activity-time {
        font-size: 0.72rem;
        color: #94a3b8;
        white-space: nowrap;
    }

    /* SIDEBAR CUSTOMIZATION - PROMINENT & HIGH CONTRAST */
    section[data-testid="stSidebar"] {
        background-color: var(--navy-sidebar) !important;
        border-right: 1px solid #16385e !important;
    }
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown span,
    section[data-testid="stSidebar"] .stRadio label {
        color: #e2e8f0 !important;
    }
    section[data-testid="stSidebar"] hr {
        border-color: #1e3a5f !important;
    }

    /* Navigation Radio Items in Sidebar */
    section[data-testid="stSidebar"] .stRadio > div {
        gap: 4px;
    }
    section[data-testid="stSidebar"] .stRadio label {
        padding: 0.65rem 1rem !important;
        border-radius: 8px !important;
        transition: all 0.15s ease;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        cursor: pointer !important;
    }
    section[data-testid="stSidebar"] .stRadio label:hover {
        background-color: #16385e !important;
        color: #ffffff !important;
    }

    /* PROMINENT HIGH-CONTRAST GLOBAL SECTOR SELECTBOX (FIX PHOTO 3) */
    section[data-testid="stSidebar"] [data-testid="stSelectbox"] {
        background-color: transparent !important;
    }
    section[data-testid="stSidebar"] [data-testid="stSelectbox"] div[data-baseweb="select"],
    section[data-testid="stSidebar"] div[data-baseweb="select"] {
        background-color: #0f2744 !important;
        border: 2px solid #38bdf8 !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3) !important;
    }
    section[data-testid="stSidebar"] div[data-baseweb="select"] > div,
    section[data-testid="stSidebar"] div[data-baseweb="select"] > div > div {
        background-color: #0f2744 !important;
        color: #ffffff !important;
        border: none !important;
    }
    section[data-testid="stSidebar"] div[data-baseweb="select"] span,
    section[data-testid="stSidebar"] div[data-baseweb="select"] div,
    section[data-testid="stSidebar"] div[data-baseweb="select"] input {
        color: #ffffff !important;
        background-color: transparent !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
    }
    section[data-testid="stSidebar"] div[data-baseweb="select"] svg {
        fill: #38bdf8 !important;
        color: #38bdf8 !important;
    }
    
    /* Dropdown Popover & Options List */
    div[data-baseweb="popover"],
    div[data-baseweb="popover"] > div,
    div[data-baseweb="menu"],
    ul[role="listbox"],
    li[role="option"] {
        background-color: #0b1f35 !important;
        color: #ffffff !important;
    }
    li[role="option"] * {
        color: #ffffff !important;
        background-color: transparent !important;
    }
    li[role="option"]:hover,
    li[role="option"][aria-selected="true"] {
        background-color: #1d4ed8 !important;
        color: #ffffff !important;
    }
    li[role="option"]:hover * {
        color: #ffffff !important;
    }

    /* PROMINENT LOGOUT BUTTON IN SIDEBAR */
    section[data-testid="stSidebar"] .stButton > button {
        background-color: #16385e !important;
        color: #ffffff !important;
        border: 1.5px solid #ef4444 !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
        width: 100% !important;
        padding: 0.6rem 1rem !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2) !important;
    }
    section[data-testid="stSidebar"] .stButton > button:hover {
        background-color: #dc2626 !important;
        color: #ffffff !important;
        border-color: #dc2626 !important;
        box-shadow: 0 4px 14px rgba(220, 38, 38, 0.4) !important;
    }

    /* General Form & Input Styling in Content Workspace */
    .main input, .main textarea, .main select {
        background-color: #ffffff !important;
        color: #0f172a !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 8px !important;
    }

    /* Primary and Secondary Buttons */
    .stButton>button {
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 0.5rem 1.25rem !important;
        transition: all 0.15s ease !important;
    }
    button[kind="primary"] {
        background-color: #0c2340 !important;
        color: #ffffff !important;
        border: none !important;
    }
    button[kind="primary"]:hover {
        background-color: #16385e !important;
        box-shadow: 0 4px 12px rgba(12, 35, 64, 0.25) !important;
    }

    /* App Footer */
    .app-footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-top: 1px solid var(--border-color);
        padding-top: 1.25rem;
        margin-top: 2rem;
        font-size: 0.82rem;
        color: var(--text-secondary);
    }
    .app-footer-secure {
        display: flex;
        align-items: center;
        gap: 0.4rem;
        color: var(--text-secondary);
    }
    </style>
    """

def render_clean_html(html_str: str):
    """
    Renders pure HTML without any leading indentation on any line,
    completely preventing markdown or DOMPurify from interpreting lines as code blocks.
    """
    import streamlit as st
    compact = "".join(line.strip() for line in html_str.splitlines() if line.strip())
    st.html(compact)

def render_kpi_card(title: str, value: str, change_pct: str, is_positive: bool, icon: str, icon_bg: str, icon_color: str, comparison_text="vs. previous period"):
    """Renders an executive KPI card with comparison indicator."""
    badge_class = "kpi-badge-green" if is_positive else "kpi-badge-red"
    arrow = "↑" if ("+" in change_pct or is_positive and "-" not in change_pct) else "↓"
    if "↓" in change_pct or "↑" in change_pct:
        arrow = ""

    card_html = f"""<div class="kpi-card">
<div class="kpi-header">
<div class="kpi-title">{title}</div>
<div class="kpi-icon-wrap" style="background:{icon_bg}; color:{icon_color};">
{icon}
</div>
</div>
<div class="kpi-value">{value}</div>
<div class="kpi-footer">
<span class="{badge_class}">{arrow} {change_pct}</span>
<span class="kpi-subtext">{comparison_text}</span>
</div>
</div>"""
    return card_html

def render_footer():
    """Renders the standard footer matching the design mockup."""
    footer_html = """<div class="app-footer">
<div>© 2025 TextileSafe. All rights reserved.</div>
<div class="app-footer-secure">
🛡️ Your safety data is protected. Access is restricted to authorized users.
</div>
</div>"""
    return footer_html
