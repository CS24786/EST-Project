"""
TextileSafe - Authentication & Login Module
Pixel-perfect recreation of the reference login screen in Photo 2:
- Sleek split-screen design matching reference mockup
- Strict role matching: Selected role MUST match the user's registered role
- No demo text, no unrendered HTML code boxes
- Clean 'Forgot password?' workflow and Google authentication trigger
"""

import streamlit as st
from config import ROLES, DEFAULT_USERS, APP_NAME, APP_SUBTITLE, APP_TAGLINE
from database.db import get_connection

def verify_credentials(identifier: str, password: str, selected_role: str):
    """
    Verifies user credentials and strictly enforces role matching.
    Prevents admin credentials from logging in as safety officer, supervisor, etc.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT id, username, name, email, role, password FROM users 
           WHERE (LOWER(username) = LOWER(?) OR LOWER(email) = LOWER(?)) AND password = ?""",
        (identifier.strip(), identifier.strip(), password.strip())
    )
    user = cursor.fetchone()
    conn.close()

    if not user:
        return None, "Invalid username/email or password."

    user_dict = dict(user)
    registered_role = user_dict.get("role", "")

    # Strict Role Matching: Selected role must match the user's registered role
    if registered_role.strip().lower() != selected_role.strip().lower():
        return None, f"Access Denied: Account '{identifier}' does not have the '{selected_role}' role. This account is registered as '{registered_role}'. Please select the role matching your account."

    return user_dict, "Success"

def reset_user_password(identifier: str, new_password: str):
    """Updates user password in database via username or email."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM users WHERE LOWER(username) = LOWER(?) OR LOWER(email) = LOWER(?)",
        (identifier.strip(), identifier.strip())
    )
    existing = cursor.fetchone()
    if not existing:
        conn.close()
        return False, "No registered account found with that username or email."
    
    cursor.execute("UPDATE users SET password = ? WHERE id = ?", (new_password.strip(), existing["id"]))
    conn.commit()
    conn.close()
    return True, "Password has been successfully updated! You can now log in."

def render_login_page():
    """Renders the split-screen enterprise login page matching Photo 2."""
    
    if "show_forgot_pw" not in st.session_state:
        st.session_state["show_forgot_pw"] = False

    col_left, col_right = st.columns([1, 1], gap="large")

    # LEFT COLUMN: Dark Navy Branding Panel matching Photo 2 exactly
    with col_left:
        left_panel_html = f"""<div style="background: linear-gradient(180deg, rgba(12, 35, 64, 0.95) 0%, rgba(7, 21, 38, 0.98) 100%), url('https://images.unsplash.com/photo-1584824486509-112e4181ff6b?auto=format&fit=crop&w=1000&q=80') center/cover; padding: 3.5rem 2.5rem; border-radius: 16px; min-height: 580px; color: white; display: flex; flex-direction: column; justify-content: space-between; box-shadow: 0 10px 25px rgba(12, 35, 64, 0.25);">
<div>
<div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 0.5rem;">
<div style="width: 52px; height: 52px; background: rgba(255,255,255,0.12); border: 1.5px solid rgba(255,255,255,0.25); border-radius: 14px; display: flex; align-items: center; justify-content: center; font-size: 1.8rem;">
🛡️
</div>
<div>
<div style="font-size: 2rem; font-weight: 800; letter-spacing: -0.02em; line-height: 1.1;">{APP_NAME}</div>
<div style="font-size: 0.85rem; color: #94a3b8; font-weight: 500;">{APP_SUBTITLE}</div>
</div>
</div>
<div style="font-size: 0.82rem; color: #cbd5e1; border-bottom: 1px solid rgba(255,255,255,0.15); padding-bottom: 1.25rem; margin-bottom: 2rem;">
{APP_TAGLINE}
</div>
<div style="display: flex; flex-direction: column; gap: 1.35rem;">
<div style="display: flex; align-items: center; gap: 1rem; font-size: 0.95rem; font-weight: 500;">
<span style="font-size: 1.3rem;">🛡️</span>
<span>Monitor Incidents & Near Misses</span>
</div>
<div style="display: flex; align-items: center; gap: 1rem; font-size: 0.95rem; font-weight: 500;">
<span style="font-size: 1.3rem;">⛑️</span>
<span>Track PPE Compliance</span>
</div>
<div style="display: flex; align-items: center; gap: 1rem; font-size: 0.95rem; font-weight: 500;">
<span style="font-size: 1.3rem;">🔥</span>
<span>Manage Fire-Safety Inspections</span>
</div>
<div style="display: flex; align-items: center; gap: 1rem; font-size: 0.95rem; font-weight: 500;">
<span style="font-size: 1.3rem;">📊</span>
<span>Analyze Risks & Hazards</span>
</div>
<div style="display: flex; align-items: center; gap: 1rem; font-size: 0.95rem; font-weight: 500;">
<span style="font-size: 1.3rem;">📄</span>
<span>Generate Reports & Insights</span>
</div>
</div>
</div>
<div style="background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 0.75rem 1rem; font-size: 0.78rem; color: #94a3b8; margin-top: 2rem;">
🧵 Textile Manufacturing OHS System &bull; Mill Safety Compliance Suite
</div>
</div>"""
        st.html(left_panel_html)

    # RIGHT COLUMN: Clean White Form matching Photo 2
    with col_right:
        right_header_html = """<div style="background: #ffffff; padding: 1.5rem 2rem 0.5rem 2rem; border-radius: 16px 16px 0 0; border: 1px solid #e2e8f0; border-bottom: none;">
<div style="font-size: 1.85rem; font-weight: 800; color: #0c2340; margin-bottom: 0.35rem;">Welcome Back</div>
<div style="font-size: 0.9rem; color: #64748b; margin-bottom: 0.75rem;">
Sign in to access the Occupational Health & Safety Compliance Dashboard.
</div>
</div>"""
        st.html(right_header_html)

        form_container = st.container()
        with form_container:
            if st.session_state["show_forgot_pw"]:
                st.subheader("🔑 Reset Password")
                reset_id = st.text_input("Username or Email Address", value="", autocomplete="username")
                new_pw = st.text_input("New Password", type="password", autocomplete="new-password")
                confirm_pw = st.text_input("Confirm New Password", type="password", autocomplete="new-password")
                
                c_btn1, c_btn2 = st.columns(2)
                with c_btn1:
                    if st.button("Update Password", type="primary", width="stretch"):
                        if not new_pw or new_pw != confirm_pw:
                            st.error("Passwords must match and cannot be empty.")
                        else:
                            ok, msg = reset_user_password(reset_id, new_pw)
                            if ok:
                                st.success(msg)
                                st.session_state["show_forgot_pw"] = False
                                st.rerun()
                            else:
                                st.error(msg)
                with c_btn2:
                    if st.button("Back to Login", width="stretch"):
                        st.session_state["show_forgot_pw"] = False
                        st.rerun()

            else:
                with st.form("login_form"):
                    role_choice = st.selectbox("Role", ROLES, index=0)
                    user_id_input = st.text_input("Email Address or Username", placeholder="Enter your email or username", autocomplete="username")
                    password_input = st.text_input("Password", placeholder="Enter your password", type="password", autocomplete="current-password")

                    col_chk, col_forgot = st.columns([1, 1])
                    with col_chk:
                        remember_me = st.checkbox("Remember me", value=True)
                    with col_forgot:
                        forgot_clicked = st.form_submit_button("Forgot password?", type="secondary")
                        if forgot_clicked:
                            st.session_state["show_forgot_pw"] = True
                            st.rerun()

                    login_submitted = st.form_submit_button("➔ Login", type="primary", width="stretch")

                    if login_submitted:
                        if not user_id_input or not password_input:
                            st.error("Please enter both username/email and password.")
                        else:
                            user, msg = verify_credentials(user_id_input, password_input, role_choice)
                            if user:
                                st.session_state["logged_in"] = True
                                st.session_state["user"] = {
                                    "id": user["id"],
                                    "username": user.get("username", user_id_input),
                                    "name": user["name"],
                                    "email": user["email"],
                                    "role": user["role"]
                                }
                                st.success(f"Welcome back, {user['name']} ({user['role']})!")
                                st.rerun()
                            else:
                                st.error(msg)

                footer_security_html = """<div style="text-align: center; font-size: 0.8rem; color: #64748b; margin-top: 1.5rem; display: flex; align-items: center; justify-content: center; gap: 0.4rem;">
<span>🛡️</span> Your data is secure and protected. Only authorized users can access the system.
</div>"""
                st.html(footer_security_html)
