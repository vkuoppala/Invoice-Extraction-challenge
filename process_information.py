from datetime import datetime
from web_operations import get_page, html_parser_to_dict, next_page, download_invoice_data
from company import find_keywords
from _config import TESSERACT_CMD
from data_storage_classes import InvoiceData
import pytesseract
import cv2

def gather_page_data():
    """Gathers all the data from the pages into one list."""
    page_data = []
    for dict in html_parser_to_dict(get_page()):
        page_data.append(dict)
    while next_page():
        for dict in html_parser_to_dict(get_page()):
            page_data.append(dict)
    good_data = filter_rows(page_data)
    if good_data is None:
        return
    return good_data

def filter_rows(page_data):
    """Drops rows that are not needed to process."""
    good_files = []
    for cells in page_data:
        if cells.length < 4:
            continue
        due_date_str = cells.due_date
        due_date = datetime.strptime(due_date_str, "%d-%m-%Y")
        if due_date > datetime.today():
            continue
        good_files.append(cells)
    return good_files

def extract_data(data):
    """Extracts relevant data from the tables."""
    relevant_data = []
    for cells in data:
        picture = create_picture(cells.invoice, cells.page_id)
        if picture is None:
            continue
        text = extract_data_from_picture(picture)
        if text is None:
            continue
        company_data = find_keywords(text)
        relevant_data.append(InvoiceData(
            invoice_id=cells.invoice_id,
            due_date=cells.due_date,
            invoice_number=company_data.invoice_number,
            invoice_date=company_data.invoice_date,
            company_name=company_data.company_name,
            total_due=company_data.total_due))
    return relevant_data

def create_picture(href, invoice_number_value):
    """Downloads the invoice document."""
    directory = "output/screenshots"
    picture = f"{directory}/{invoice_number_value}.png"
    with open(picture, "wb") as file:
        file.write(download_invoice_data(href))
    return picture


def extract_data_from_picture(picture):
    """Extracts the text from the invoice document."""
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD
    img = cv2.imread(picture)
    if img is None:
        return None
    text = pytesseract.image_to_string(img)
    return text