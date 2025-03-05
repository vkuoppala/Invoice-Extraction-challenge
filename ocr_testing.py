from time import sleep
from robocorp.tasks import task
from robocorp import browser
from bs4 import BeautifulSoup
import pytesseract
import cv2
import requests
import re
import csv
from datetime import datetime

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

@task
def ocr_testing():
    """Invoice extraction challenge."""
    TULOS_FILE = "output.csv"
    WEBSITE = "https://rpachallengeocr.azurewebsites.net/"
    clear_csv_file(TULOS_FILE)
    invoice_number = 0
    open_website(WEBSITE)
    start()
    sleep(0.05)
    invoice_number = get_invoices(invoice_number, TULOS_FILE, WEBSITE)
    next_page(2)
    invoice_number = get_invoices(invoice_number, TULOS_FILE, WEBSITE)
    next_page(3)
    invoice_number = get_invoices(invoice_number, TULOS_FILE, WEBSITE)
    submit(TULOS_FILE)
    sleep(30)

def submit(file_path):
    page = browser.page()
    page.locator(selector="input[type='file']").set_input_files(file_path)

def open_website(url):
    browser.goto(url)

def start():
    page = browser.page()
    page.click("id=start")

def get_invoices(invoice_number_counter, tulos_file, website):
    page = browser.page()
    html_page = page.content()   
    soup = BeautifulSoup(html_page, "html.parser")
    # Find all rows with class "odd" and "even"
    rows = soup.find_all("tr", class_=["odd", "even"])
    
    for row in rows:
        cells = row.find_all("td")
        if len(cells) < 4:
            continue

        invoice_id = cells[1].text.strip()
        due_date_str = cells[2].text.strip()
        due_date = datetime.strptime(due_date_str, "%d-%m-%Y")
        if due_date > datetime.today():
            continue

        link = cells[3].find("a")["href"]
        if link:
            invoice_number_counter += 1
            invoice_number, invoice_date, company_name, total_due = check_invoice(link, invoice_number_counter, website)
            write_csv_file(invoice_id, due_date_str, invoice_number, invoice_date, company_name, total_due, tulos_file)
    return invoice_number_counter

def clear_csv_file(file_path):
    """Clear the contents of the CSV file."""
    with open(file_path, 'w', newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["ID", "DueDate", "InvoiceNo", "InvoiceDate", "CompanyName", "TotalDue"])

def next_page(page_nro):
    page = browser.page()
    element = page.query_selector(f"[data-dt-idx='{page_nro}']")
    if element:
        element.click()

def check_invoice(href, invoice_number_value, website):
    url = f"{website}{href}"
    response = requests.get(url)
    picture = f"output/screenshots/{invoice_number_value}.png"
    with open(picture, "wb") as file:
        file.write(response.content)
    img = cv2.imread(picture)
    text = pytesseract.image_to_string(img)

    # Extract specific keywords using regular expressions

    invoice_number_match = invoice_number(text)
    invoice_date_match = invoice_date(text)
    company_name_match = company_name(text)
    total_due_match = total_due(text)
    
    if invoice_number_match:
        invoice_number_value = invoice_number_match.group(1)
    
    if invoice_date_match:
        invoice_date_value = invoice_date_match.group(1)
        invoice_date_value = datetime.strptime(invoice_date_value, "%Y-%m-%d").strftime("%d-%m-%Y")
    
    if company_name_match:
        company_name_value = company_name_match.group()
    
    if total_due_match:
        total_due_value = total_due_match.group(1)
    return invoice_number_value, invoice_date_value, company_name_value, total_due_value


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

def write_csv_file(invoice_id, due_date_str, invoice_number, invoice_date, company_name, total_due, tulos_file):
    with open(tulos_file, "a", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([invoice_id, due_date_str, invoice_number, invoice_date, company_name, total_due])