from _config import HEADER, TULOS_FILE
import csv

def create_csv_file(extracted_data):
    """Writes the extracted data to the CSV file."""
    with open(TULOS_FILE, "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(HEADER)
        for row in extracted_data:
            data_to_write = [row.invoice_id,
                                row.due_date,
                                row.invoice_number,
                                row.invoice_date,
                                row.company_name,
                                row.total_due]
            csvwriter.writerow(data_to_write)

def main():
    """Main function."""
    pass

if __name__ == "__main__":
    main()