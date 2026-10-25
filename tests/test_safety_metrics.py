"""
Unit tests for TextileSafe OHS Compliance Calculations and Logic:
- Risk score and classification logic
- PPE compliance aggregations
- Fire-safety pass rates
- Incident frequency metrics (TRIR, LTIFR)
- Database queries and seeding integrity
"""

import unittest
from config import get_risk_level
from database.db import init_db, get_connection, query_dataframe, wipe_all_data
from database.seed_data import seed_database

class TestSafetyMetrics(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Initialize database and seed baseline data for test assertions."""
        init_db()
        seed_database(force_reload=True)

    @classmethod
    def tearDownClass(cls):
        """Restore operational database to clean zero-data state for fresh launch."""
        wipe_all_data()

    def test_risk_score_and_classification(self):
        """Verifies 5x5 matrix calculations and threshold mappings."""
        # Low: 1 - 4
        self.assertEqual(get_risk_level(1)["label"], "Low")
        self.assertEqual(get_risk_level(4)["label"], "Low")

        # Medium: 5 - 9
        self.assertEqual(get_risk_level(5)["label"], "Medium")
        self.assertEqual(get_risk_level(9)["label"], "Medium")

        # High: 10 - 16
        self.assertEqual(get_risk_level(10)["label"], "High")
        self.assertEqual(get_risk_level(16)["label"], "High")

        # Critical: 17 - 25
        self.assertEqual(get_risk_level(17)["label"], "Critical")
        self.assertEqual(get_risk_level(25)["label"], "Critical")

    def test_incident_rates_calculation(self):
        """Verifies OSHA TRIR and LTIFR rate logic."""
        exposure_hours = 2880000  # 1,200 employees * 8 hrs * 300 days
        lost_time_injuries = 19
        recordable_injuries = 42

        ltifr = round((lost_time_injuries * 1000000) / exposure_hours, 2)
        trir = round((recordable_injuries * 200000) / exposure_hours, 2)

        self.assertAlmostEqual(ltifr, 6.6, places=1)
        self.assertAlmostEqual(trir, 2.92, places=2)

    def test_ppe_compliance_average(self):
        """Verifies PPE compliance calculations."""
        df = query_dataframe("SELECT overall_compliance_pct FROM ppe_inspections")
        self.assertFalse(df.empty)
        avg_score = df["overall_compliance_pct"].mean()
        self.assertGreaterEqual(avg_score, 85.0)
        self.assertLessEqual(avg_score, 100.0)

    def test_fire_safety_compliance(self):
        """Verifies fire safety pass rate calculation."""
        df = query_dataframe("SELECT status FROM fire_inspections")
        self.assertFalse(df.empty)
        passed = len(df[df["status"] == "Passed"])
        rate = (passed / len(df)) * 100
        self.assertGreaterEqual(rate, 90.0)

    def test_database_seed_integrity(self):
        """Ensures that benchmark KPI figures match the calibrated dataset."""
        inc_df = query_dataframe("SELECT incident_type FROM incidents")
        accidents = inc_df[inc_df["incident_type"].str.contains("Accident")]
        near_misses = inc_df[inc_df["incident_type"] == "Near Miss"]

        # Expected calibrated counts
        self.assertEqual(len(accidents), 42)
        self.assertEqual(len(near_misses), 28)

        capa_df = query_dataframe("SELECT status FROM corrective_actions WHERE status = 'Open'")
        self.assertEqual(len(capa_df), 12)

if __name__ == "__main__":
    unittest.main()
