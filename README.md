# TextileSafe - Occupational Health and Safety (OHS) Compliance Analysis System

[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.66%2B-FF4B4B.svg)](https://streamlit.io/)
[![SQLite3](https://img.shields.io/badge/Database-SQLite3-003B57.svg)](https://www.sqlite.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **"Safer People | Safer Processes | A Stronger Textile Industry"**  
> An industrial-grade Occupational Health & Safety (OHS) Compliance & Risk Analytics Platform designed specifically for textile manufacturing mills (Spinning, Weaving, Knitting, Dyeing & Finishing, Cutting & Stitching, Boiler & Utilities, Warehouse).

---

## 1. Project Overview & Features

**TextileSafe** is a complete, fully functional, multi-module safety management information system built with Python, Streamlit, and SQLite. It provides industrial safety managers with real-time KPI visibility, incident investigation workflows, PPE audit tracking, statutory fire-equipment inspections, a 5×5 textile risk matrix, corrective & preventive action (CAPA) lifecycle management, and automated regulatory reporting (PDF & multi-tab Excel).

### Core Functional Modules
1. **Executive Safety Dashboard:**
   - Visual interface replicating modern enterprise safety software.
   - 5 KPI summary cards: Total Incidents (42), Near Misses (28), PPE Compliance (93%), Fire-Safety Compliance (96%), and Open Actions (12) with percentage comparison indicators.
   - Monthly Incident Trend (Plotly combo Bar & Line chart).
   - Incidents by Severity (Plotly Donut chart with centered total).
   - Department Risk Heatmap matrix with direct detail navigation.
   - PPE Compliance by Type horizontal progress indicators.
   - Real-time safety activity feed.

2. **Accident & Near-Miss Analysis:**
   - Formal incident registry with root-cause analysis, shift distribution, and department breakdown.
   - Industry-standard OSHA/ILO metrics:
     - **LTIFR** (Lost Time Injury Frequency Rate per 1,000,000 man-hours): $\frac{\text{LTI} \times 1,000,000}{\text{Exposure Hours}}$
     - **TRIR** (Total Recordable Incident Rate per 200,000 man-hours): $\frac{\text{Recordable Injuries} \times 200,000}{\text{Exposure Hours}}$
     - **Severity Rate** & **Near-Miss Proactive Ratio** ($28 : 42 = 0.67$).

3. **PPE Compliance Tracking:**
   - Department-wise compliance monitoring across 6 mandatory items: Helmets, Steel-Toe Safety Shoes, Chemical/Cut Gloves, Eye Goggles, Hearing Protection (Earmuffs/Earplugs), and Respiratory Lint Masks.
   - Item-level compliance progress bars and interactive floor audit logger.

4. **Fire-Safety & Emergency Systems:**
   - Asset tracking for CO2, DCP, and Water extinguishers, smoke alarms, emergency exits, and evacuation routes.
   - Automated 30-day inspection cycle tracking with visual overdue and deficiency alerts.

5. **5×5 Textile Hazard & Risk Assessment:**
   - Configurable $5 \times 5$ Risk Matrix: $\text{Risk Score} = \text{Likelihood} (1\text{--}5) \times \text{Severity} (1\text{--}5)$.
   - Dynamic threshold classification: Low (1–4), Medium (5–9), High (10–16), Critical (17–25).
   - Sector-specific hazard profiles covering 7 textile departments.

6. **Corrective & Preventive Action (CAPA) Tracker:**
   - Complete remediation lifecycle: `Open` $\rightarrow$ `In Progress` $\rightarrow$ `Closed`.
   - Assigned engineers, priority tags (High, Medium, Low), target deadlines, and one-click status transitions.

7. **Reports & Data Management:**
   - **Downloadable PDF Executive Report** generated via ReportLab.
   - **Multi-Tab Styled Excel Workbook** generated via OpenPyXL.
   - CSV and Excel file batch uploader with data schema validation.
   - Comprehensive OHS Data Dictionary.

8. **Settings & System Administration:**
   - **One-Click Benchmark Sample Data Loader:** Populates ~650 realistic records calibrated to the 2025 dashboard figures.
   - **Wipe All Operational Data:** Safeguarded factory reset.
   - **User Management & Password Reset:** In-place password reset and new user onboarding.

---

## 2. Directory Structure

```
d:/Talha Documents/EST-Project/
├── app.py                      # Main Streamlit application and navigation router
├── config.py                   # System constants, colors, departments, risk thresholds
├── requirements.txt            # Python dependencies
├── README.md                   # Complete installation, architecture, and user guide
├── database/
│   ├── __init__.py
│   ├── db.py                   # SQLite3 connection, queries, schema definition, wiping
│   └── seed_data.py            # ~650 calibrated realistic synthetic textile records (12 months)
├── modules/
│   ├── __init__.py
│   ├── auth.py                 # Split-screen enterprise login & role management
│   ├── dashboard.py            # Executive dashboard matching UI mockup
│   ├── incidents.py            # Accident & Near-Miss analytics and OSHA rate calculations
│   ├── ppe.py                  # PPE compliance analytics and audit logger
│   ├── fire_safety.py          # Fire safety asset inspection and overdue tracking
│   ├── risk_assessment.py      # 5x5 risk matrix and textile department hazard profiling
│   ├── corrective_actions.py   # CAPA lifecycle management and priority tracking
│   ├── reports.py              # PDF/Excel export, data import, and data dictionary
│   └── settings.py             # Sample data reload, data wipe, and user password reset
├── utils/
│   ├── __init__.py
│   ├── styles.py               # Custom CSS design system, KPI cards, top bar
│   ├── export_excel.py         # OpenPyXL multi-tab styled workbook generator
│   └── export_pdf.py           # ReportLab PDF executive audit report generator
└── tests/
    ├── __init__.py
    └── test_safety_metrics.py  # Automated unit test suite (5 passing test cases)
```

---

## 3. Installation and Launch Guide

### Prerequisites
- Python 3.11 or higher
- Git (optional)

### Setup Instructions

1. **Clone or navigate to the project directory:**
   ```bash
   cd "d:/Talha Documents/EST-Project"
   ```

2. **Install required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the automated unit tests:**
   ```bash
   python -m unittest tests/test_safety_metrics.py
   ```
   *Expected output: `Ran 5 tests ... OK`*

4. **Launch the Streamlit web application:**
   ```bash
   streamlit run app.py
   ```

5. **Open in your web browser:**
   ```
   http://localhost:8501
   ```

### Default Credentials
- **Role:** Safety Manager
- **Email:** `talha.nawaz@textilesafe.com`
- **Password:** `admin` *(or use the 1-click Demo Sign-in button)*

---

## 4. Academic & Engineering Methodology

### Exposure Hours & Frequency Rate Formulae
Assuming a typical integrated textile complex with $1,200$ shift workers working $8$ hours/day across $300$ operating days:
$$\text{Total Annual Man-Hours} = 1,200 \times 8 \times 300 = 2,880,000 \text{ hours}$$

- **Lost Time Injury Frequency Rate (LTIFR):**
  $$\text{LTIFR} = \frac{\text{Lost Time Injuries} \times 1,000,000}{\text{Exposure Hours}} = \frac{19 \times 1,000,000}{2,880,000} \approx 6.60$$

- **Total Recordable Incident Rate (OSHA TRIR):**
  $$\text{TRIR} = \frac{\text{Total Recordable Injuries} \times 200,000}{\text{Exposure Hours}} = \frac{42 \times 200,000}{2,880,000} \approx 2.92$$

### Textile Industry Hazard Taxonomy
- **Spinning:** Rotating roller nip points on carding/drawframes, high-velocity spindle noise, respirable raw cotton dust (byssinosis risk).
- **Weaving:** High-speed sley swords, rapier/air-jet loom acoustic spike (>92 dBA), yarn sizing mist.
- **Knitting:** Needle cylinder pinch zones, cam track vibration, needle lubrication mist.
- **Dyeing & Finishing:** Corrosive chemicals (caustic soda, hydrogen peroxide, acetic acid), thermal oil stenter exhausts (>45°C), slippery wet dye troughs.
- **Cutting & Stitching:** High-speed band knives, sewing machine needle punctures, fabric fluff.
- **Boiler & Utilities:** High-pressure steam lines (10 bar, 180°C), boiler feed pumps, chemical water softening agents.
- **Warehouse:** Forklift collision, cotton bale stack stability, battery charging hydrogen venting.

---

## 5. Disclaimer
*This application is developed as an academic and industrial analytics demonstration for textile engineering safety compliance. It provides safety decision-support analytics and does not replace statutory physical inspections, certified structural engineering evaluations, or legal third-party boiler and fire audits.*
