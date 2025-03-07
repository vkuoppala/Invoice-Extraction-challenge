import unittest
from unittest.mock import patch, MagicMock
from challenge import (
    clear_csv_file, open_website, start, get_page_information, next_page,
    gather_page_data, drop_unwanted_rows, information_handler, extract_data,
    download_invoice, extract_data_from_picture, write_to_csv_file, submit
)
from _config import TULOS_FILE, WEBSITE

class TestChallenge(unittest.TestCase):

    @patch('challenge.csv.writer')
    @patch('challenge.open')
    def test_clear_csv_file(self, mock_open, mock_csv_writer):
        clear_csv_file()
        mock_open.assert_called_once_with(TULOS_FILE, 'w', newline="")
        mock_csv_writer().writerow.assert_called_once()

    @patch('challenge.browser.goto')
    def test_open_website(self, mock_goto):
        open_website()
        mock_goto.assert_called_once_with(WEBSITE)

    @patch('challenge.browser.page')
    def test_start(self, mock_page):
        mock_page().click = MagicMock()
        start()
        mock_page().click.assert_called_once_with("id=start")

    @patch('challenge.browser.page')
    @patch('challenge.BeautifulSoup')
    def test_get_page_information(self, mock_soup, mock_page):
        mock_page.content = "<html></html>"
        mock_soup.return_value.find_all.return_value = []
        result = get_page_information()
        self.assertEqual(result, [])

    @patch('challenge.browser.page')
    def test_next_page(self, mock_page):
        mock_page().query_selector.return_value = MagicMock()
        result = next_page()
        self.assertTrue(result)

    @patch('challenge.get_page_information')
    @patch('challenge.next_page')
    @patch('challenge.drop_unwanted_rows')
    def test_gather_page_data(self, mock_drop_unwanted_rows, mock_next_page, mock_get_page_information):
        mock_get_page_information.return_value = [{'id': '1', 'invoice_number': '123', 'due_date': '01-01-2020', 'invoice': 'link'}]
        mock_next_page.side_effect = [True, False]
        mock_drop_unwanted_rows.return_value = [{'id': '1', 'invoice_number': '123', 'due_date': '01-01-2020', 'invoice': 'link'}]
        result = gather_page_data()
        self.assertIsNotNone(result)

    def test_drop_unwanted_rows(self):
        page_data = [{'id': '1', 'invoice_number': '123', 'due_date': '01-01-2020', 'invoice': 'link'}]
        result = drop_unwanted_rows(page_data)
        self.assertEqual(len(result), 1)

    @patch('challenge.extract_data')
    @patch('challenge.write_to_csv_file')
    def test_information_handler(self, mock_write_to_csv_file, mock_extract_data):
        mock_extract_data.return_value = []
        information_handler([])
        mock_write_to_csv_file.assert_called_once()

    """ @patch('challenge.requests.get')
    @patch('challenge.os.makedirs')
    @patch('challenge.os.path.exists')
    def test_download_invoice(self, mock_exists, mock_makedirs, mock_get): # Ei toimi
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = b'content'
        mock_exists.side_effect = lambda path: path != 'output/screenshots'
        mock_makedirs.return_value = None
        result = download_invoice('/link', '12')
        self.assertIsNotNone(result)
        mock_makedirs.assert_called_once_with('output/screenshots', exist_ok=True)"""

    @patch('challenge.cv2.imread')
    @patch('challenge.pytesseract.image_to_string')
    def test_extract_data_from_picture(self, mock_image_to_string, mock_imread):
        mock_imread.return_value = 'image'
        mock_image_to_string.return_value = 'text'
        result = extract_data_from_picture('picture.png')
        self.assertEqual(result, 'text')

    @patch('challenge.csv.writer')
    @patch('challenge.open')
    def test_write_to_csv_file(self, mock_open, mock_csv_writer):
        write_to_csv_file([('123', '01-01-2020', '123', '01-01-2020', 'Company', '100.00')])
        mock_open.assert_called_once_with(TULOS_FILE, 'a', newline="")
        mock_csv_writer().writerow.assert_called_once()

    @patch('challenge.browser.page')
    def test_submit(self, mock_page):
        mock_page().locator().set_input_files = MagicMock()
        submit()
        mock_page().locator().set_input_files.assert_called_once_with(TULOS_FILE)

if __name__ == '__main__':
    unittest.main()