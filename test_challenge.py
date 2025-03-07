import unittest
from unittest.mock import patch, MagicMock
from challenge import challenge
from csv_operations import create_csv_file
from web_operations import open_website, start, submit
from process_information import gather_page_data, extract_data

class TestChallenge(unittest.TestCase):

    @patch('challenge.create_csv_file')
    @patch('challenge.extract_data')
    @patch('challenge.gather_page_data')
    @patch('challenge.submit')
    @patch('challenge.start')
    @patch('challenge.open_website')
    @patch('challenge.sleep', return_value=None)
    def test_challenge(self, mock_sleep, mock_open_website, mock_start, mock_submit, mock_gather_page_data, mock_extract_data, mock_create_csv_file):
        # Mock the return values
        mock_gather_page_data.return_value = 'mock_page_data'
        mock_extract_data.return_value = 'mock_extracted_data'

        # Call the challenge function
        challenge()

        # Assert the calls
        mock_open_website.assert_called_once()
        mock_start.assert_called_once()
        mock_sleep.assert_any_call(0.5)
        mock_gather_page_data.assert_called_once()
        mock_extract_data.assert_called_once_with('mock_page_data')
        mock_create_csv_file.assert_called_once_with('mock_extracted_data')
        mock_submit.assert_called_once()
        mock_sleep.assert_any_call(5)

if __name__ == '__main__':
    unittest.main()