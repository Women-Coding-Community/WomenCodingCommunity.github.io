import unittest
from automation_mentors import get_mentorship_type, type_ad_hoc, type_long_term, TYPE_BOTH

class TestMentorAutomation(unittest.TestCase):
    AD_HOC_1 = "Ad-Hoc Format"
    AD_HOC_2 = "Ad Hoc Format"
    LONG_TERM_1 = "Long-term Format"
    LONG_TERM_2 = "Long term Format"
    BOTH = "Both"
    WRONG_FORMAT = "Wrong Format"
    EMPTY = ""

    def test_get_ad_hoc_type(self):
        self.assertEqual(type_ad_hoc[0], get_mentorship_type(self.AD_HOC_1))
        self.assertEqual(type_ad_hoc[0], get_mentorship_type(self.AD_HOC_2))

    def test_get_long_term_type(self):
        self.assertEqual(type_long_term[0], get_mentorship_type(self.LONG_TERM_1))
        self.assertEqual(type_long_term[0], get_mentorship_type(self.LONG_TERM_2))

    def test_get_both_type(self):
        self.assertEqual(TYPE_BOTH, get_mentorship_type(self.BOTH))

    def test_get_not_defined_type(self):
        self.assertEqual("NOT_FOUND", get_mentorship_type(self.WRONG_FORMAT))
        self.assertEqual("NOT_FOUND", get_mentorship_type(self.EMPTY))
