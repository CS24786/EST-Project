"""
TextileSafe - Occupational Health & Safety Compliance Configuration
Constants, palettes, risk matrix definitions, user roles, and role-based access control.
"""

# App Metadata
APP_NAME = "TextileSafe"
APP_SUBTITLE = "Occupational Health & Safety Compliance Analysis"
APP_TAGLINE = "Safer People | Safer Processes | A Stronger Textile Industry"
APP_VERSION = "2.5.0"
COPYRIGHT_TEXT = "© 2025 TextileSafe. All rights reserved."

# Color Scheme (Matches Provided Enterprise UI Specifications)
COLORS = {
    "navy_dark": "#0a192f",
    "navy_primary": "#0c2340",
    "navy_sidebar": "#0b1f35",
    "navy_hover": "#16385e",
    "blue_accent": "#2563eb",
    "blue_active": "#1d4ed8",
    "blue_light": "#3b82f6",
    "blue_subtle": "#eff6ff",
    "bg_main": "#f4f6f9",
    "card_bg": "#ffffff",
    "border": "#e2e8f0",
    "text_dark": "#0f172a",
    "text_muted": "#64748b",
    
    # Severity & Risk Status Colors
    "success": "#10b981",    # Minor / Low Risk / Compliant
    "warning": "#f59e0b",    # Moderate / In Progress
    "high_risk": "#f97316",  # Major / High Risk
    "critical": "#ef4444",   # Critical / Overdue / Non-compliant
    "purple": "#8b5cf6",
}

# Textile Manufacturing Departments
DEPARTMENTS = [
    "Spinning",
    "Weaving",
    "Knitting",
    "Dyeing & Finishing",
    "Cutting & Stitching",
    "Boiler & Utilities",
    "Warehouse"
]

# Work Shifts
SHIFTS = [
    "Morning (06:00 - 14:00)",
    "Evening (14:00 - 22:00)",
    "Night (22:00 - 06:00)"
]

# Incident Classifications & Severities
INCIDENT_TYPES = [
    "Accident (Lost Time)",
    "Accident (No Lost Time / First Aid)",
    "Near Miss",
    "Unsafe Act / Unsafe Condition"
]

SEVERITIES = ["Minor", "Moderate", "Major", "Critical"]

SEVERITY_COLORS = {
    "Minor": "#10b981",
    "Moderate": "#f59e0b",
    "Major": "#f97316",
    "Critical": "#ef4444"
}

# Textile Hazard Categories
HAZARD_TYPES = [
    "Machine Guarding & Entanglement",
    "Excessive Noise",
    "Cotton Dust & Byssinosis Exposure",
    "Chemical Handling & Toxic Fumes",
    "Heat & High Humidity",
    "Ergonomic & Repetitive Strain",
    "Slips, Trips & Falls",
    "Fire, Boiler & Electrical Risk"
]

# PPE Categories
PPE_TYPES = [
    "Helmets",
    "Safety Shoes",
    "Gloves",
    "Eye Protection",
    "Hearing Protection",
    "Others"
]

# Fire Safety Equipment & Inspection Checklist
FIRE_EQUIPMENT_TYPES = [
    "CO2 Fire Extinguisher",
    "Dry Chemical Powder (DCP) Extinguisher",
    "Water / Foam Extinguisher",
    "Smoke Detector & Fire Alarm",
    "Emergency Exit & Push Bar",
    "Evacuation Route & Emergency Lights",
    "Fire Hose Reel & Hydrant"
]

# 5x5 Risk Matrix Configurations
LIKELIHOOD_LEVELS = {
    1: "Rare (1)",
    2: "Unlikely (2)",
    3: "Possible (3)",
    4: "Likely (4)",
    5: "Almost Certain (5)"
}

SEVERITY_LEVELS = {
    1: "Insignificant (1)",
    2: "Minor (2)",
    3: "Moderate (3)",
    4: "Major (4)",
    5: "Catastrophic (5)"
}

# Configurable Risk Matrix Thresholds
RISK_THRESHOLDS = {
    "Low": {"min": 1, "max": 4, "color": "#10b981", "badge_class": "risk-low", "label": "Low"},
    "Medium": {"min": 5, "max": 9, "color": "#f59e0b", "badge_class": "risk-medium", "label": "Medium"},
    "High": {"min": 10, "max": 16, "color": "#f97316", "badge_class": "risk-high", "label": "High"},
    "Critical": {"min": 17, "max": 25, "color": "#ef4444", "badge_class": "risk-critical", "label": "Critical"}
}

def get_risk_level(score: int) -> dict:
    """Returns risk level dict based on risk score (1-25)."""
    for level, conf in RISK_THRESHOLDS.items():
        if conf["min"] <= score <= conf["max"]:
            return conf
    return RISK_THRESHOLDS["Critical"]

# User Roles
ROLES = [
    "Safety Manager",
    "Safety Supervisor",
    "Safety Officer",
    "Compliance Auditor",
    "Department Head",
    "Plant General Manager"
]

# Standard Role-Based Default Users (Username & Password mapping)
DEFAULT_USERS = [
    {
        "username": "admin",
        "name": "Talha Nawaz",
        "email": "admin@textilesafe.com",
        "role": "Safety Manager",
        "password": "admin123"
    },
    {
        "username": "super",
        "name": "Muhammad Aslam",
        "email": "super@textilesafe.com",
        "role": "Safety Supervisor",
        "password": "super123"
    },
    {
        "username": "officer",
        "name": "Zubair Ahmed",
        "email": "officer@textilesafe.com",
        "role": "Safety Officer",
        "password": "officer123"
    },
    {
        "username": "auditor",
        "name": "Ayesha Malik",
        "email": "auditor@textilesafe.com",
        "role": "Compliance Auditor",
        "password": "auditor123"
    },
    {
        "username": "head",
        "name": "Kashif Razzaq",
        "email": "head@textilesafe.com",
        "role": "Department Head",
        "password": "head123"
    },
    {
        "username": "gm",
        "name": "Tariq Mehmood",
        "email": "gm@textilesafe.com",
        "role": "Plant General Manager",
        "password": "gm123"
    }
]

# Role-Based Access Control (RBAC) Permissions Matrix
ROLE_PERMISSIONS = {
    "Safety Manager": [
        "Dashboard",
        "Incidents & Near Misses",
        "PPE Compliance",
        "Fire-Safety Inspections",
        "Risk Assessment",
        "Corrective Actions",
        "Reports & Data",
        "Settings & System"
    ],
    "Plant General Manager": [
        "Dashboard",
        "Incidents & Near Misses",
        "PPE Compliance",
        "Fire-Safety Inspections",
        "Risk Assessment",
        "Corrective Actions",
        "Reports & Data",
        "Settings & System"
    ],
    "Safety Supervisor": [
        "Dashboard",
        "Incidents & Near Misses",
        "PPE Compliance",
        "Fire-Safety Inspections",
        "Corrective Actions"
    ],
    "Safety Officer": [
        "Dashboard",
        "Incidents & Near Misses",
        "PPE Compliance",
        "Fire-Safety Inspections",
        "Corrective Actions"
    ],
    "Compliance Auditor": [
        "Dashboard",
        "Incidents & Near Misses",
        "PPE Compliance",
        "Fire-Safety Inspections",
        "Risk Assessment",
        "Reports & Data"
    ],
    "Department Head": [
        "Dashboard",
        "Incidents & Near Misses",
        "Risk Assessment",
        "Corrective Actions"
    ]
}
