import unittest
from unittest.mock import patch, MagicMock
from process_information import gather_page_data, filter_rows, extract_data, create_picture, extract_data_from_picture
from data_storage_classes import RelevantPageData, InvoiceData, CompanyData

class TestProcessInformation(unittest.TestCase):

    @patch('process_information.html_parser_to_dict')
    @patch('process_information.get_page')
    @patch('process_information.next_page')
    def test_gather_page_data(self, mock_next_page, mock_get_page, mock_html_parser_to_dict):
        mock_get_page.return_value = 'mock_page'
        mock_html_parser_to_dict.return_value = [
            RelevantPageData(page_id='1', invoice_id='123', due_date='01-01-2020', invoice='link', length=4),
            RelevantPageData(page_id='2', invoice_id='124', due_date='01-01-2026', invoice='link', length=4)
        ]
        mock_next_page.side_effect = [True, False]
        result = gather_page_data()
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 2)

    def test_filter_rows(self):
        page_data = [
            RelevantPageData(page_id='1', invoice_id='123', due_date='01-01-2020', invoice='link', length=4),
            RelevantPageData(page_id='2', invoice_id='124', due_date='01-01-2026', invoice='link', length=4)
        ]
        result = filter_rows(page_data)
        self.assertEqual(len(result), 1)

    @patch('process_information.create_picture')
    @patch('process_information.extract_data_from_picture')
    @patch('process_information.find_keywords')
    def test_extract_data(self, mock_find_keywords, mock_extract_data_from_picture, mock_create_picture):
        mock_create_picture.return_value = 'mock_picture'
        mock_extract_data_from_picture.return_value = 'mock_text'
        mock_find_keywords.return_value = CompanyData(
            company_name='Aenean LLC', invoice_number='1234', invoice_date='01-01-2020', total_due='100.00'
        )
        data = [
            RelevantPageData(page_id='1', invoice_id='123', due_date='01-01-2020', invoice='link', length=4)
        ]
        result = extract_data(data)
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], InvoiceData)

    """@patch('process_information.download_invoice_data')
    def test_create_picture(self, mock_download_invoice_data):
        mock_download_invoice_data.return_value = b'content'
        result = create_picture('link', '12')
        self.assertIsNotNone(result)""" # Binary file, can't test

    @patch('process_information.cv2.imread')
    @patch('process_information.pytesseract.image_to_string')
    def test_extract_data_from_picture(self, mock_image_to_string, mock_imread):
        mock_imread.return_value = 'image'
        mock_image_to_string.return_value = 'text'
        result = extract_data_from_picture('picture.png')
        self.assertEqual(result, 'text')

if __name__ == '__main__':
    unittest.main()