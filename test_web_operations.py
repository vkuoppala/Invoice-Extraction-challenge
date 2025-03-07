import unittest
from unittest.mock import patch, MagicMock
from web_operations import open_website, start, submit, next_page, html_parser_to_dict, store_page_data_to_storage, get_page, download_invoice_data
from _config import WEBSITE, TULOS_FILE

class TestWebOperations(unittest.TestCase):

    @patch('web_operations.browser.goto')
    def test_open_website(self, mock_goto):
        open_website()
        mock_goto.assert_called_once_with(WEBSITE)

    @patch('web_operations.browser.page')
    def test_start(self, mock_page):
        mock_page().click = MagicMock()
        start()
        mock_page().click.assert_called_once_with("id=start")

    @patch('web_operations.browser.page')
    def test_submit(self, mock_page):
        mock_page().locator().set_input_files = MagicMock()
        submit()
        mock_page().locator().set_input_files.assert_called_once_with(TULOS_FILE)

    @patch('web_operations.browser.page')
    def test_next_page(self, mock_page):
        mock_page().query_selector.return_value = MagicMock()
        result = next_page()
        self.assertTrue(result)

    @patch('web_operations.BeautifulSoup')
    def test_html_parser_to_dict(self, mock_soup):
        mock_soup.return_value.find_all.return_value = []
        result = html_parser_to_dict('<html></html>')
        self.assertIsInstance(result, list)

    def test_store_page_data_to_storage(self):
        data = MagicMock()
        data.find_all.return_value = [MagicMock(text='1'), MagicMock(text='2'), MagicMock(text='3'), MagicMock(text='4')]
        result = store_page_data_to_storage(data)
        self.assertIsNotNone(result)

    @patch('web_operations.browser.page')
    def test_get_page(self, mock_page):
        mock_page().content.return_value = '<html></html>'
        result = get_page()
        self.assertEqual(result, '<html></html>')

    @patch('web_operations.requests.get')
    def test_download_invoice_data(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = b'content'
        result = download_invoice_data('/link')
        self.assertEqual(result, b'content')

if __name__ == '__main__':
    unittest.main()