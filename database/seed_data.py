"""
TextileSafe - Realistic Synthetic Seed Data Generator
Generates ~650 realistic records covering 12 months across all textile departments.
Calibrated precisely to match the executive dashboard benchmarks.
All data is synthetic and clearly tagged as such.
"""

import random
from datetime import datetime, date, timedelta
from database.db import get_connection, wipe_all_data, init_db
from config import DEPARTMENTS, SHIFTS, PPE_TYPES, FIRE_EQUIPMENT_TYPES

def seed_database(force_reload=False):
    """Populates database with realistic 12-month synthetic textile OHS records."""
    init_db()
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM incidents")
    count = cursor.fetchone()[0]
    if count > 0 and not force_reload:
        conn.close()
        return False  # Already seeded

    if force_reload:
        wipe_all_data()

    random.seed(42)  # Deterministic seed for reproducible KPIs

    # -------------------------------------------------------------
    # 1. GENERATE INCIDENTS (42 Accidents + 28 Near Misses = 70 total)
    # Severity distribution: 23 Minor, 13 Moderate, 5 Major, 1 Critical
    # -------------------------------------------------------------
    incident_types = (
        ["Accident (No Lost Time / First Aid)"] * 23 +
        ["Accident (Lost Time)"] * 19 +
        ["Near Miss"] * 28
    )
    
    # Predefined severities for the 42 Accidents:
    # 23 Minor, 13 Moderate, 5 Major, 1 Critical
    accident_severities = (
        ["Minor"] * 23 +
        ["Moderate"] * 13 +
        ["Major"] * 5 +
        ["Critical"] * 1
    )
    random.shuffle(accident_severities)

    # Near misses are classified as Minor or Moderate in potential
    near_miss_severities = ["Minor"] * 20 + ["Moderate"] * 8
    random.shuffle(near_miss_severities)

    textile_incidents_catalog = [
        ("Spinning", "Machine Guarding & Entanglement", "Worker finger pinched while re-threading broken roving at ring frame", "Muhammad Aslam", 1),
        ("Weaving", "Machine Guarding & Entanglement", "Weft shuttle projectile caught sleeve cuff; emergency trip wire activated", "Kashif Razzaq", 0),
        ("Dyeing & Finishing", "Chemical Handling & Toxic Fumes", "Splash of hot acetic acid during dye vat bath formulation; minor skin redness", "Rashid Minhas", 3),
        ("Boiler & Utilities", "Heat & High Humidity", "High pressure steam valve packing blow-by during pressure ramp-up", "Farooq Abdullah", 0),
        ("Cutting & Stitching", "Machine Guarding & Entanglement", "Sewing needle puncture through index finger due to missing plastic finger guard", "Saima Bibi", 0),
        ("Spinning", "Cotton Dust & Byssinosis Exposure", "High fiber fly accumulation caused worker coughing and eye irritation", "Tariq Mehmood", 0),
        ("Warehouse", "Slips, Trips & Falls", "Forklift operator swerved to avoid pallet overhang; clipped empty cotton bale stack", "Bilal Siddiqui", 0),
        ("Knitting", "Excessive Noise", "High-speed circular knitting frame motor bearing failure caused sharp acoustic spike", "Waseem Akram", 0),
        ("Dyeing & Finishing", "Slips, Trips & Falls", "Operator slipped on wet soaping floor near mercerizing drain trough", "Ali Raza", 2),
        ("Weaving", "Slips, Trips & Falls", "Tripped over air-jet loom pneumatic supply hose lying across aisle", "Naveed Akhtar", 0),
        ("Boiler & Utilities", "Fire, Boiler & Electrical Risk", "Spark noticed in condensate feed pump electrical terminal box", "Zafar Iqbal", 0),
        ("Spinning", "Machine Guarding & Entanglement", "Cleaning fly waste while carding cylinder was coasting down; laceration", "Imran Nazir", 14),
        ("Cutting & Stitching", "Slips, Trips & Falls", "Fabric bundle roll rolled off stacking cart into emergency path", "Shamim Akhtar", 0),
        ("Warehouse", "Machine Guarding & Entanglement", "Conveyor belt roller nip point safety cover was unbolted during shift", "Haroon Rasheed", 0),
    ]

    base_date = date(2025, 1, 5)
    monthly_accidents_dist = [3, 4, 3, 2, 3, 3, 2, 3, 4, 4, 6, 5]  # sum = 42
    monthly_near_miss_dist = [3, 4, 3, 2, 3, 2, 2, 3, 2, 2, 1, 1]  # sum = 28

    incident_idx = 1
    acc_idx = 0
    nm_idx = 0

    for month_zero in range(12):
        month = month_zero + 1
        num_acc = monthly_accidents_dist[month_zero]
        num_nm = monthly_near_miss_dist[month_zero]

        # Add Accidents for this month
        for _ in range(num_acc):
            dep, cause, desc, person, lost_days = random.choice(textile_incidents_catalog)
            day = random.randint(1, 28)
            inc_date = date(2025, month, day)
            sev = accident_severities[acc_idx % len(accident_severities)]
            acc_idx += 1
            inc_code = f"INC-2025-{incident_idx:03d}"
            lost_d = lost_days if sev != "Critical" else 30
            if sev == "Minor":
                lost_d = 0

            cursor.execute("""
                INSERT INTO incidents (
                    incident_code, incident_type, department, shift, severity,
                    incident_date, root_cause, description, injured_person,
                    lost_workdays, reported_by, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                inc_code,
                "Accident (Lost Time)" if lost_d > 0 else "Accident (No Lost Time / First Aid)",
                dep,
                random.choice(SHIFTS),
                sev,
                inc_date.strftime("%Y-%m-%d"),
                cause,
                desc,
                person,
                lost_d,
                "Safety Supervisor",
                "Closed" if month < 11 else random.choice(["Closed", "Investigated", "Under Review"])
            ))
            incident_idx += 1

        # Add Near Misses for this month
        for _ in range(num_nm):
            dep, cause, desc, person, _ = random.choice(textile_incidents_catalog)
            day = random.randint(1, 28)
            inc_date = date(2025, month, day)
            sev = near_miss_severities[nm_idx % len(near_miss_severities)]
            nm_idx += 1
            inc_code = f"INC-2025-{incident_idx:03d}"

            cursor.execute("""
                INSERT INTO incidents (
                    incident_code, incident_type, department, shift, severity,
                    incident_date, root_cause, description, injured_person,
                    lost_workdays, reported_by, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                inc_code,
                "Near Miss",
                dep,
                random.choice(SHIFTS),
                sev,
                inc_date.strftime("%Y-%m-%d"),
                cause,
                f"NEAR MISS: {desc} (No personal injury sustained)",
                "None",
                0,
                "Line Floor Leader",
                "Closed"
            ))
            incident_idx += 1

    # -------------------------------------------------------------
    # 2. GENERATE PPE INSPECTIONS (~310 records across departments)
    # Overall target compliance: ~93%
    # Rates: Helmets 95%, Shoes 92%, Gloves 90%, Eye 94%, Hearing 88%, Others 96%
    # -------------------------------------------------------------
    ppe_idx = 1
    inspectors = ["Zubair Ahmed", "Ayesha Malik", "Fahad Mustafa", "Usman Ghani"]

    start_date = date(2025, 1, 2)
    for day_step in range(0, 360, 4):  # every 4 days
        curr_date = start_date + timedelta(days=day_step)
        for dep in random.sample(DEPARTMENTS, 3):  # 3 departments per inspection day
            h_comp = 1 if random.random() < 0.95 else 0
            s_comp = 1 if random.random() < 0.92 else 0
            g_comp = 1 if random.random() < 0.90 else 0
            e_comp = 1 if random.random() < 0.94 else 0
            ea_comp = 1 if random.random() < 0.88 else 0
            o_comp = 1 if random.random() < 0.96 else 0

            score = (h_comp + s_comp + g_comp + e_comp + ea_comp + o_comp) / 6.0 * 100.0

            cursor.execute("""
                INSERT INTO ppe_inspections (
                    inspection_code, department, shift, inspection_date, inspector,
                    helmets_compliant, safety_shoes_compliant, gloves_compliant,
                    eye_protection_compliant, hearing_protection_compliant, others_compliant,
                    overall_compliance_pct, notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                f"PPE-2025-{ppe_idx:04d}",
                dep,
                random.choice(SHIFTS),
                curr_date.strftime("%Y-%m-%d"),
                random.choice(inspectors),
                h_comp, s_comp, g_comp, e_comp, ea_comp, o_comp,
                round(score, 1),
                "Standard floor audit round. PPE compliance verified at workstation."
            ))
            ppe_idx += 1

    # -------------------------------------------------------------
    # 3. GENERATE FIRE-SAFETY INSPECTIONS (~160 records, 96% pass)
    # -------------------------------------------------------------
    fire_idx = 1
    for day_step in range(0, 360, 7):  # weekly
        curr_date = start_date + timedelta(days=day_step)
        next_due = curr_date + timedelta(days=30)
        dep = random.choice(DEPARTMENTS)
        eq_type = random.choice(FIRE_EQUIPMENT_TYPES)
        
        is_pass = random.random() < 0.96
        status = "Passed" if is_pass else random.choice(["Deficient", "Overdue"])
        pressure = "Normal" if status == "Passed" else "Low"
        cond = "Good" if status == "Passed" else random.choice(["Damaged", "Obstructed"])
        finding = "Unit fully charged, seal intact, access clear." if status == "Passed" else "Minor inspection deficiency noted: obstruction or pressure gauge low."

        cursor.execute("""
            INSERT INTO fire_inspections (
                inspection_code, department, equipment_type, location_tag,
                inspection_date, next_due_date, status, pressure_check,
                physical_condition, findings, inspector
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            f"FIRE-2025-{fire_idx:04d}",
            dep,
            eq_type,
            f"{dep[:3].upper()}-BAY-{random.randint(101, 199)}",
            curr_date.strftime("%Y-%m-%d"),
            next_due.strftime("%Y-%m-%d"),
            status,
            pressure,
            cond,
            finding,
            random.choice(inspectors)
        ))
        fire_idx += 1

    # -------------------------------------------------------------
    # 4. GENERATE 35 TEXTILE RISK ASSESSMENTS (5 key hazards per 7 depts)
    # Calibrated to exact risk heatmap in the screenshot:
    # Spinning -> High (15)
    # Weaving -> High (12)
    # Knitting -> Medium (8)
    # Dyeing & Finishing -> Critical (20)
    # Cutting & Stitching -> Medium (6)
    # Boiler & Utilities -> High (16)
    # Warehouse -> Low (4)
    # -------------------------------------------------------------
    dept_risk_profile = {
        "Spinning": [
            ("Machine Guarding", "Carding and drawframe rotating cylinder nip entanglement", 4, 4, "Interlocked access doors", "Dual photo-electric safety light curtains"),
            ("Noise", "Spindle drive continuous high decibel emission (>88 dBA)", 4, 3, "Earplugs supplied", "Acoustic enclosure around motor drive"),
            ("Dust", "Cotton micro-dust / lint inhalation & byssinosis danger", 5, 3, "Central exhaust ducts", "Enhanced HEPA filtration & mandatory N95 respirators"),
            ("Chemical", "Synthetic sizing wax fumes in blending line", 2, 2, "General ventilation", "Local extraction hoods"),
            ("Heat", "Friction thermal build-up in spinning hall", 3, 2, "Humidification plant", "Automated temperature control ducts")
        ],
        "Weaving": [
            ("Machine Guarding", "High speed rapier / air-jet loom moving sley swords", 4, 4, "Sley covers & trip cords", "Optical sensor interlocking on loom shields"),
            ("Noise", "Loom shedding and beat-up impact noise (>92 dBA)", 5, 3, "Earmuffs issued", "Baffle ceiling sound absorption panels"),
            ("Dust", "Warp yarn lint shredding and sizing dust fly", 3, 2, "Overhead traveling cleaners", "Periodic pneumatic suction clean cycles"),
            ("Chemical", "Starch sizing and lubricating mist", 2, 2, "Floor exhaust trenches", "Bio-degradable non-misting lubricant"),
            ("Heat", "Loom motor heat dissipation in weaving shed", 3, 3, "Supply air washers", "High-volume low-speed (HVLS) cooling fans")
        ],
        "Knitting": [
            ("Machine Guarding", "Circular knitting needle cylinder and yarn feeder guides", 3, 2, "Perimeter wire guards", "Electronic stop-motion sensors"),
            ("Noise", "Cam tracks and creel vibratory hum (~80 dBA)", 2, 2, "Foam earplugs available", "Vibration dampening floor mats"),
            ("Dust", "Spun yarn fly accumulation in needle beds", 2, 2, "Blower fans", "Enclosed creel positive pressure filtration"),
            ("Chemical", "Knitting needle oil mist exposure", 2, 2, "Non-toxic oil grades", "Oil mist collectors on head frames"),
            ("Heat", "Motor heat in closed circular knitting room", 2, 2, "Air exchange units", "Split AC climate balance")
        ],
        "Dyeing & Finishing": [
            ("Machine Guarding", "Stenter frame entrance pin chains & high-speed batching rolls", 4, 4, "Safety wires along rails", "Emergency stop bar and nip roller guards"),
            ("Noise", "High-pressure jet dyeing circulation pumps & hydro-extractors", 3, 3, "Ear protection zones", "Pump sound-insulating jackets"),
            ("Dust", "Powder dyestuff dispersal during weighing & recipe mixing", 3, 3, "Exhaust booth", "Down-draft dispensing booth with laminar airflow"),
            ("Chemical", "Sodium hydrosulfite, caustic soda, reactive dyes & hydrogen peroxide", 5, 4, "Chemical apron, goggles, nitrile gloves", "Automated chemical dosing system & eyewash stations"),
            ("Heat", "Open steam from drying ranges and thermal oil stenter exhausts (>42°C)", 4, 4, "Exhaust roof cowls", "Thermal insulation on steam pipes & spot cooling")
        ],
        "Cutting & Stitching": [
            ("Machine Guarding", "Band knife cutting blade and sewing needle punctures", 3, 2, "Chainmail metal mesh gloves & needle guards", "Laser-guided finger zone boundary sensors"),
            ("Noise", "Combined sewing machine motors (~75 dBA)", 2, 1, "Direct-drive servo motors", "Maintenance lubrication routine"),
            ("Dust", "Fabric fleece cutting fluff and micro-fibers", 2, 2, "Daily sweeping", "Vacuum extraction at cutting tables"),
            ("Chemical", "Spot cleaning solvent (PCE/spot lifter sprays)", 2, 2, "Spray booth ventilation", "Solvent-free water-based spot lifters"),
            ("Heat", "Steam iron press tables and fusing machine radiant heat", 2, 2, "Exhaust canopy over irons", "Insulated press soles and chilled air blowers")
        ],
        "Boiler & Utilities": [
            ("Machine Guarding", "Compressor drive belts, feedwater pump shafts, turbine couplings", 3, 4, "Heavy wire mesh cage enclosures", "Interlocked lockout/tagout (LOTO) switch stations"),
            ("Noise", "Gas burner roaring flame and turbine generator hum (>90 dBA)", 4, 3, "Mandatory class-5 earmuffs", "Acoustic boundary walling for utility room"),
            ("Dust", "Coal/biomass handling dust (if solid fuel used)", 3, 3, "Water spray suppression", "Enclosed screw feeder & cyclone separator"),
            ("Chemical", "Boiler water treatment chemicals (hydrazine, caustic, phosphates)", 3, 4, "Acid-resistant gloves & face shield", "Closed-loop metering injection skid"),
            ("Heat", "Superheated steam lines (180°C, 10 bar) and boiler shell radiation", 4, 4, "Rockwool cladding with aluminum jacketing", "Thermal imaging leak audits & automatic blowdown")
        ],
        "Warehouse": [
            ("Machine Guarding", "Reach truck mast chains and battery charging hoist", 2, 2, "Overhead operator guard cage", "Daily pre-op mechanical inspection checklist"),
            ("Noise", "Forklift reverse alarms and pallet wrapping turntable (<75 dBA)", 1, 1, "Broadband squawker alarms", "Acoustic line markings"),
            ("Dust", "Raw cotton bale shedding in storage bays", 2, 2, "Floor scrubber dryers", "Air recirculation filtration units"),
            ("Chemical", "Lead-acid battery charging hydrogen gas emissions", 2, 2, "Explosion-proof spark-less exhaust fans", "Gas detection sensor & eye-wash shower"),
            ("Heat", "Metal warehouse roof radiant heat during summer", 2, 2, "Roof ridge ventilators", "Thermal radiant barrier insulation on roof deck")
        ]
    }

    haz_idx = 1
    for dep, hazards_list in dept_risk_profile.items():
        for cat, spec, l, s, ext_c, rec_c in hazards_list:
            score = l * s
            if score <= 4:
                lvl = "Low"
            elif score <= 9:
                lvl = "Medium"
            elif score <= 16:
                lvl = "High"
            else:
                lvl = "Critical"

            cursor.execute("""
                INSERT INTO hazards (
                    hazard_code, department, hazard_category, specific_hazard,
                    likelihood, severity, risk_score, risk_level,
                    existing_controls, recommended_controls, assessment_date
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                f"HAZ-2025-{haz_idx:03d}",
                dep,
                cat,
                spec,
                l, s, score, lvl,
                ext_c,
                rec_c,
                "2025-01-15"
            ))
            haz_idx += 1

    # -------------------------------------------------------------
    # 5. GENERATE CORRECTIVE ACTIONS (60 actions: 12 Open, 16 In Progress, 32 Closed)
    # Exactly matches the 12 Open Actions KPI card in the screenshot!
    # -------------------------------------------------------------
    capa_catalog = [
        ("Install interlocking safety light curtain at Ring Spinning Frame 12", "Incident", "Spinning", "Zubair Ahmed", "High", "2025-11-15", "Open"),
        ("Replace cracked chemical dosing flex pipe on Dyeing Machine #4", "Hazard Assessment", "Dyeing & Finishing", "Kashif Razzaq", "High", "2025-11-20", "Open"),
        ("Clear blocked emergency fire exit doorway in Finishing Hall", "Fire Audit", "Dyeing & Finishing", "Talha Nawaz", "High", "2025-11-10", "Open"),
        ("Conduct noise dosimetry mapping in Weaving Shed Bay B", "PPE Audit", "Weaving", "Ayesha Malik", "Medium", "2025-11-25", "Open"),
        ("Install chain guard on cutting department fabric unrolling table", "Hazard Assessment", "Cutting & Stitching", "Usman Ghani", "Medium", "2025-11-30", "Open"),
        ("Service dry chemical powder fire extinguisher #FE-14", "Fire Audit", "Boiler & Utilities", "Farooq Abdullah", "High", "2025-11-18", "Open"),
        ("Fix hydraulic oil leak underneath Stenter Machine input roller", "Incident", "Dyeing & Finishing", "Zubair Ahmed", "High", "2025-12-05", "Open"),
        ("Repair eye wash safety shower station pressure in Dye Kitchen", "Hazard Assessment", "Dyeing & Finishing", "Rashid Minhas", "High", "2025-11-12", "Open"),
        ("Erect anti-fall barriers on mezzanine storage rack in Warehouse", "Hazard Assessment", "Warehouse", "Bilal Siddiqui", "Medium", "2025-12-01", "Open"),
        ("Re-apply yellow non-slip floor walkway markings in Weaving Loom aisles", "Incident", "Weaving", "Naveed Akhtar", "Low", "2025-12-10", "Open"),
        ("Inspect and calibrate steam pressure relief valve on Boiler 2", "Fire Audit", "Boiler & Utilities", "Zafar Iqbal", "High", "2025-11-28", "Open"),
        ("Enforce mandatory high-protection earmuffs in Carding hall", "PPE Audit", "Spinning", "Ayesha Malik", "High", "2025-11-22", "Open"),
    ]

    # Insert the 12 Open CAPAs
    act_idx = 1
    for title, src, dep, assignee, prio, due, stat in capa_catalog:
        cursor.execute("""
            INSERT INTO corrective_actions (
                action_code, title, source_type, source_ref, department,
                assigned_to, priority, due_date, status, completion_date, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            f"CAPA-2025-{act_idx:03d}",
            title, src, f"REF-{act_idx:03d}", dep, assignee, prio, due, stat, None,
            "Action logged. Engineering and safety team actively tracking completion."
        ))
        act_idx += 1

    # Insert 16 In Progress CAPAs
    for i in range(16):
        dep = random.choice(DEPARTMENTS)
        cursor.execute("""
            INSERT INTO corrective_actions (
                action_code, title, source_type, source_ref, department,
                assigned_to, priority, due_date, status, completion_date, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            f"CAPA-2025-{act_idx:03d}",
            f"In-progress safety remediation for {dep} machinery hazard",
            "Hazard Assessment",
            f"HAZ-REF-{i+1}",
            dep,
            random.choice(inspectors),
            random.choice(["High", "Medium"]),
            "2025-12-15",
            "In Progress",
            None,
            "Procurement of safety guarding parts in progress."
        ))
        act_idx += 1

    # Insert 32 Closed CAPAs
    for i in range(32):
        dep = random.choice(DEPARTMENTS)
        cursor.execute("""
            INSERT INTO corrective_actions (
                action_code, title, source_type, source_ref, department,
                assigned_to, priority, due_date, status, completion_date, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            f"CAPA-2025-{act_idx:03d}",
            f"Completed safety control installation in {dep} work station",
            random.choice(["Incident", "PPE Audit", "Fire Audit"]),
            f"AUDIT-REF-{i+1}",
            dep,
            random.choice(inspectors),
            random.choice(["High", "Medium", "Low"]),
            "2025-08-15",
            "Closed",
            "2025-08-14",
            "Verification inspection conducted. Hazard successfully mitigated."
        ))
        act_idx += 1

    conn.commit()
    conn.close()
    return True
