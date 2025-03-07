import unittest
from company import AeneanLLC, SitAmetCorp, find_keywords

class TestCompany(unittest.TestCase):

    def test_aenean_llc_create_from_text(self):
        text = "Invoice #1234\n2020-01-01\nTotal 100.00"
        company = AeneanLLC.create_from_text(text)
        self.assertEqual(company.get_number(), '1234')
        self.assertEqual(company.get_date(), '01-01-2020')
        self.assertEqual(company.get_total_due(), '100.00')

    def test_sit_amet_corp_create_from_text(self):
        text = "# 5678\nDate: January 01, 2020\nTotal $200.00"
        company = SitAmetCorp.create_from_text(text)
        self.assertEqual(company.get_number(), '5678')
        self.assertEqual(company.get_date(), '01-01-2020')
        self.assertEqual(company.get_total_due(), '200.00')

    def test_find_keywords(self):
        text = "testingfileforthisfunction\nAenean LLC\nInvoice #1234\n2020-01-01\nTotal 100.00"
        result = find_keywords(text)
        self.assertIsNotNone(result)
        self.assertEqual(result[0], '1234')
        self.assertEqual(result[1], '01-01-2020')
        self.assertEqual(result[2], 'Aenean LLC')
        self.assertEqual(result[3], '100.00')

if __name__ == '__main__':
    unittest.main()