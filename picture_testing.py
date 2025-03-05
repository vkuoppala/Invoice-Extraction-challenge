from time import sleep
from robocorp.tasks import task
import pytesseract
import cv2
import re

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

picture = "output/screenshots/2.png"
@task
def picture_testing():
    img = cv2.imread(picture)
    text = pytesseract.image_to_string(img)

    # Extract specific keywords using regular expressions
    
    invoice_number_match = invoice_number(text)
    invoice_date_match = invoice_date(text)
    company_name_match = company_name(text)
    total_due_match = total_due(text)
    
    if invoice_number_match:
        invoice_number_value = invoice_number_match.group(1)
        print(f"Invoice Number: {invoice_number_value}")
    
    if invoice_date_match:
        invoice_date_value = invoice_date_match.group(1)
        print(f"Invoice Date: {invoice_date_value}")
    
    if company_name_match:
        company_name_value = company_name_match.group()
        print(f"Company Name: {company_name_value}")
    
    if total_due_match:
        total_due_value = total_due_match.group(1)
        print(f"Total Due: {total_due_value}")


def invoice_number(text):
    if re.search(r'Invoice #(\d+)', text):
        return re.search(r'Invoice #(\d+)', text)
    if re.search(r'# (\d+)', text):
        return re.search(r'# (\d+)', text)
    return None
    
def invoice_date(text):
    if re.search(r'(\d{4}-\d{2}-\d{2})', text):
        return re.search(r'(\d{4}-\d{2}-\d{2})', text)
    if re.search(r'Date: (\w+ \d{2}, \d{4})', text):
        return re.search(r'Date: (\w+ \d{2}, \d{4})', text)
    return None

def company_name(text):
    match = re.search("Aenean LLC", text)
    if match:
        return match
    match = re.search("Sit Amet Corp", text)
    if match:
        return match
    return None

def total_due(text):
    if re.search(r'Total (\d+\.\d{2})', text):
        return re.search(r'Total (\d+\.\d{2})', text)
    if re.search(r'Total \$([\d,]+\.\d{2})', text):
        return re.search(r'Total \$([\d,]+\.\d{2})', text)
    return None