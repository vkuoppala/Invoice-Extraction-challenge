import unittest
from company import AeneanLLC, SitAmetCorp, find_keywords
from data_storage_classes import CompanyData

class TestCompany(unittest.TestCase):

    def test_aenean_llc_create_from_text(self):
        text = "Invoice #1234\n2020-01-01\nTotal 100.00"
        company = AeneanLLC()
        company.create_from_text(text)
        self.assertEqual(company.get_number(), '1234')
        self.assertEqual(company.get_date(), '01-01-2020')
        self.assertEqual(company.get_total_due(), '100.00')

    def test_sit_amet_corp_create_from_text(self):
        text = "# 5678\nDate: January 01, 2020\nTotal $200.00"
        company = SitAmetCorp()
        company.create_from_text(text)
        self.assertEqual(company.get_number(), '5678')
        self.assertEqual(company.get_date(), '01-01-2020')
        self.assertEqual(company.get_total_due(), '200.00')

    def test_find_keywords_aenean_llc(self):
        text = "testingfileforthisfunction\nAenean LLC\nInvoice #1234\n2020-01-01\nTotal 100.00"
        result = find_keywords(text)
        self.assertIsNotNone(result)
        self.assertEqual(result.invoice_number, '1234')
        self.assertEqual(result.invoice_date, '01-01-2020')
        self.assertEqual(result.company_name, 'Aenean LLC')
        self.assertEqual(result.total_due, '100.00')

    def test_find_keywords_sit_amet_corp(self):
        text = "testingfileforthisfunction\nSit Amet Corp\n# 5678\nDate: January 01, 2020\nTotal $200.00"
        result = find_keywords(text)
        self.assertIsNotNone(result)
        self.assertEqual(result.invoice_number, '5678')
        self.assertEqual(result.invoice_date, '01-01-2020')
        self.assertEqual(result.company_name, 'Sit Amet Corp')
        self.assertEqual(result.total_due, '200.00')

if __name__ == '__main__':
    unittest.main()