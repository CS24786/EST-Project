"""
Database manager for TextileSafe OHS analytics.
Provides SQLite initialization, queries, and data management.
"""

import sqlite3
import os
import pandas as pd
from config import DEFAULT_USERS

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "textilesafe.db")

def get_connection():
    """Create and return an optimized SQLite database connection with row factory enabled."""
    conn = sqlite3.connect(DB_PATH, timeout=10.0, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    return conn

def init_db():
    """Initializes tables if they do not exist."""
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Users table (with username and role)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            role TEXT NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Check if username column exists; if not, add it
    cursor.execute("PRAGMA table_info(users)")
    cols = [r["name"] for r in cursor.fetchall()]
    if "username" not in cols:
        cursor.execute("ALTER TABLE users ADD COLUMN username TEXT")

    # 2. Incidents & Near Misses table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            incident_code TEXT UNIQUE NOT NULL,
            incident_type TEXT NOT NULL,
            department TEXT NOT NULL,
            shift TEXT NOT NULL,
            severity TEXT NOT NULL,
            incident_date DATE NOT NULL,
            root_cause TEXT NOT NULL,
            description TEXT,
            injured_person TEXT,
            lost_workdays INTEGER DEFAULT 0,
            reported_by TEXT,
            status TEXT DEFAULT 'Closed'
        )
    """)

    # 3. PPE Inspections table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ppe_inspections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            inspection_code TEXT UNIQUE NOT NULL,
            department TEXT NOT NULL,
            shift TEXT NOT NULL,
            inspection_date DATE NOT NULL,
            inspector TEXT NOT NULL,
            helmets_compliant INTEGER DEFAULT 1,
            safety_shoes_compliant INTEGER DEFAULT 1,
            gloves_compliant INTEGER DEFAULT 1,
            eye_protection_compliant INTEGER DEFAULT 1,
            hearing_protection_compliant INTEGER DEFAULT 1,
            others_compliant INTEGER DEFAULT 1,
            overall_compliance_pct REAL NOT NULL,
            notes TEXT
        )
    """)

    # 4. Fire-Safety Inspections table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fire_inspections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            inspection_code TEXT UNIQUE NOT NULL,
            department TEXT NOT NULL,
            equipment_type TEXT NOT NULL,
            location_tag TEXT NOT NULL,
            inspection_date DATE NOT NULL,
            next_due_date DATE NOT NULL,
            status TEXT NOT NULL,
            pressure_check TEXT DEFAULT 'Normal',
            physical_condition TEXT DEFAULT 'Good',
            findings TEXT,
            inspector TEXT NOT NULL
        )
    """)

    # 5. Textile Risk & Hazard Assessment table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS hazards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hazard_code TEXT UNIQUE NOT NULL,
            department TEXT NOT NULL,
            hazard_category TEXT NOT NULL,
            specific_hazard TEXT NOT NULL,
            likelihood INTEGER NOT NULL,
            severity INTEGER NOT NULL,
            risk_score INTEGER NOT NULL,
            risk_level TEXT NOT NULL,
            existing_controls TEXT,
            recommended_controls TEXT,
            assessment_date DATE NOT NULL
        )
    """)

    # 6. Corrective & Preventive Action (CAPA) Tracker table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS corrective_actions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action_code TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            source_type TEXT NOT NULL,
            source_ref TEXT,
            department TEXT NOT NULL,
            assigned_to TEXT NOT NULL,
            priority TEXT NOT NULL,
            due_date DATE NOT NULL,
            status TEXT NOT NULL,
            completion_date DATE,
            notes TEXT
        )
    """)

    conn.commit()

    # Seed or synchronize default users (admin, super, officer, auditor, head)
    for u in DEFAULT_USERS:
        cursor.execute("SELECT id FROM users WHERE LOWER(email) = LOWER(?) OR LOWER(username) = LOWER(?)", (u["email"], u["username"]))
        existing = cursor.fetchone()
        if not existing:
            cursor.execute(
                "INSERT INTO users (username, name, email, role, password) VALUES (?, ?, ?, ?, ?)",
                (u["username"], u["name"], u["email"], u["role"], u["password"])
            )
        else:
            # Update credentials to match the requested standard
            cursor.execute(
                "UPDATE users SET username = ?, password = ?, role = ? WHERE id = ?",
                (u["username"], u["password"], u["role"], existing["id"])
            )
    conn.commit()
    conn.close()

def execute_query(query: str, params: tuple = ()):
    """Execute write query (INSERT, UPDATE, DELETE)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()

def query_dataframe(query: str, params: tuple = ()) -> pd.DataFrame:
    """Execute select query and return results as a Pandas DataFrame."""
    conn = get_connection()
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

def wipe_all_data():
    """Wipes all operational data while preserving table structures and default users."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM incidents")
    cursor.execute("DELETE FROM ppe_inspections")
    cursor.execute("DELETE FROM fire_inspections")
    cursor.execute("DELETE FROM hazards")
    cursor.execute("DELETE FROM corrective_actions")
    # Reset sqlite auto-increment sequence
    cursor.execute("DELETE FROM sqlite_sequence WHERE name NOT IN ('users')")
    conn.commit()
    conn.close()

def get_db_stats() -> dict:
    """Returns total record counts for all entities."""
    conn = get_connection()
    cursor = conn.cursor()
    stats = {}
    for table in ["incidents", "ppe_inspections", "fire_inspections", "hazards", "corrective_actions", "users"]:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        stats[table] = cursor.fetchone()[0]
    conn.close()
    return stats
