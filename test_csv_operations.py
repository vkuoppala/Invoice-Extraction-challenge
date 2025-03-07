import unittest
from unittest.mock import patch, mock_open
from csv_operations import create_csv_file
from data_storage_classes import InvoiceData
from _config import HEADER, TULOS_FILE

class TestCSVOperations(unittest.TestCase):

    @patch('csv_operations.open', new_callable=mock_open)
    @patch('csv_operations.csv.writer')
    def test_create_csv_file(self, mock_csv_writer, mock_open):
        extracted_data = [
            InvoiceData(
                invoice_id='1',
                due_date='01-01-2020',
                invoice_number='1234',
                invoice_date='01-01-2020',
                company_name='Aenean LLC',
                total_due='100.00'
            )
        ]
        create_csv_file(extracted_data)
        mock_open.assert_called_once_with(TULOS_FILE, 'w', newline="")
        mock_csv_writer().writerow.assert_any_call(HEADER)
        mock_csv_writer().writerow.assert_any_call([
            '1', '01-01-2020', '1234', '01-01-2020', 'Aenean LLC', '100.00'
        ])

if __name__ == '__main__':
    unittest.main()