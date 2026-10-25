# Project Report: Occupational Health and Safety (OHS) Compliance Analysis in Textile Manufacturing Using Python

**Project Title:** TextileSafe - Industrial Occupational Health & Safety Compliance Analysis Platform  
**Target Domain:** Textile Manufacturing Engineering & Mill Operations  
**Principal Investigator / Safety Analyst:** Talha Nawaz (Safety Manager)  
**Frameworks & Stack:** Python 3.11+, Streamlit, SQLite3, Pandas, NumPy, Plotly, OpenPyXL, ReportLab  
**Date:** October 2025  

---

## 1. Executive Summary

In integrated textile manufacturing facilities, personnel face an array of physical, chemical, acoustic, ergonomic, and thermal hazards. This project details the design, architecture, implementation, and analytical evaluation of **TextileSafe**, an industrial-grade Occupational Health and Safety (OHS) analytics platform. 

The system digitizes safety operations across seven core manufacturing divisions:
1. Spinning
2. Weaving
3. Knitting
4. Dyeing & Finishing
5. Cutting & Stitching
6. Boiler & Utilities
7. Raw Material & Finished Goods Warehouse

Through normalized relational data modeling in SQLite and interactive analytical visualizations in Streamlit, TextileSafe empowers plant management to track statutory compliance, monitor lead and lag safety indicators, assess department-level hazard matrices, and coordinate corrective remediations.

---

## 2. Research & Analytical Methodology

### 2.1 Exposure Model and Frequency Rate Formulations
The analytical framework operates on standard international labor exposure metrics (OSHA 1904 and ILO Code of Practice). In a baseline textile complex employing $1,200$ production workers over three shifts ($8$ hours per shift, $300$ annual operating days):

$$\text{Total Annual Exposure Hours} = 1,200 \text{ employees} \times 8 \text{ hours/day} \times 300 \text{ days} = 2,880,000 \text{ man-hours}$$

The system dynamically computes:
1. **Lost Time Injury Frequency Rate (LTIFR):**
   $$\text{LTIFR} = \frac{\text{Lost Time Injuries (LTI)} \times 1,000,000}{\text{Total Exposure Hours}} = \frac{19 \times 1,000,000}{2,880,000} = 6.60$$

2. **Total Recordable Incident Rate (TRIR - OSHA Standard):**
   $$\text{TRIR} = \frac{\text{Total Recordable Injuries} \times 200,000}{\text{Total Exposure Hours}} = \frac{42 \times 200,000}{2,880,000} = 2.92$$

3. **Severity Rate (SR):**
   $$\text{SR} = \frac{\text{Total Lost Workdays} \times 1,000,000}{\text{Total Exposure Hours}}$$

4. **Near-Miss Proactive Index:**
   $$\text{Proactive Reporting Ratio} = \frac{\text{Near Misses Reported}}{\text{Recorded Accidents}} = \frac{28}{42} = 0.67$$

### 2.2 Standardized 5×5 Risk Assessment Matrix
Risks are quantified using the formula:
$$\text{Risk Score} = \text{Likelihood} (1\text{--}5) \times \text{Severity} (1\text{--}5)$$

Threshold boundaries are documented and configured as:
- **Low Risk (1 – 4):** Standard operating procedures and basic supervision sufficient.
- **Medium Risk (5 – 9):** Engineering controls and administrative monitoring required.
- **High Risk (10 – 16):** Immediate intervention and priority corrective action needed.
- **Critical Risk (17 – 25):** Severe danger; requires immediate lockout/tagout (LOTO) or process halt until rectified.

---

## 3. Key Findings from Mill Analytics

1. **Department Risk Stratification:**
   - **Dyeing & Finishing** exhibits the highest aggregate risk profile (Score: 20/25, Critical) due to chemical burns (caustic soda, hydrogen peroxide, reactive dyes) and thermal radiation from stenter drying ranges (>45°C).
   - **Spinning & Weaving** represent high machine-guarding and noise risk profiles (Scores: 15/25 and 12/25) driven by high-speed rotating spindles, rapier loom sley swords, and acoustic spikes (>90 dBA).
   - **Warehouse** displays the lowest baseline hazard profile (Score: 4/25, Low), primarily governed by forklift aisle traffic.

2. **PPE Compliance Trends:**
   - Overall mill PPE compliance stands at **93%**, surpassing the statutory 90% benchmark.
   - Category breakdown: Helmets (95%), Safety Shoes (92%), Cut/Chemical Gloves (90%), Eye Protection (94%), Respiratory Masks (96%).
   - Hearing protection (earplugs/earmuffs) achieved the lowest compliance at **88%**, concentrated in Weaving and Spinning where high heat causes operator discomfort.

3. **Fire Safety & Emergency Preparedness:**
   - 96% pass rate across inspected extinguishers, smoke detectors, and emergency push-bar exit doors.
   - Identified deficiencies primarily involve pressure drops in dry chemical powder (DCP) units in utility rooms and intermittent aisle obstructions in finishing storage corridors.

4. **Corrective Action (CAPA) Performance:**
   - Out of 60 total tracked safety actions, 32 are verified Closed (53.3%), 16 are In Progress (26.7%), and 12 remain Open (20.0%), meeting the operational threshold of $\le 15$ open remediations.

---

## 4. Evidence-Based Industrial Recommendations

1. **Engineering Controls for High-Speed Machinery:**
   - Retrofit dual-channel optical light curtains and interlocking limit switches on carding cylinders and roving frames to eliminate nip point entanglements.
2. **Automated Chemical Dosing in Dye Kitchens:**
   - Transition from manual chemical bucket pouring to closed-loop automated pipeline dosing skids for caustic soda and concentrated liquid dyes.
3. **Acoustic Abatement & Ergonomic Hearing PPE:**
   - Install sound-absorbing baffle ceiling panels in weaving sheds and upgrade standard foam earplugs to customized filtered musician-grade acoustic plugs that permit verbal communication while attenuating harmful industrial decibels.
4. **Respirable Dust Monitoring:**
   - Install continuous real-time optical particle counters in opening and blowroom sections to ensure cotton fly remains below the OSHA Permissible Exposure Limit (PEL) of $200\,\mu\text{g/m}^3$.

---

## 5. System Limitations & Future Scope

- **Limitation:** Relies on manual audit and incident entry rather than IoT sensor feeds (e.g., smart wearable PPE, connected gas monitors).
- **Future Scope:** Integration with mill ERP systems (SAP/Oracle), computer-vision AI cameras for automated PPE detection at line entrances, and mobile QR code tagging for fire extinguishers.

---

## 6. Conclusion

The TextileSafe platform proves that modern Python data science and web technologies can be effectively tailored to industrial textile health and safety management. By unifying incident reporting, PPE compliance, fire asset inspections, and ISO-aligned risk matrix evaluations into a cohesive, aesthetically polished executive cockpit, the system significantly enhances safety culture, audit readiness, and worker protection.
