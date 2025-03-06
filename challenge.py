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
from company import find_keywords

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

@task
def challenge():
    """Invoice extraction challenge."""
    TULOS_FILE = "output/output.csv"
    WEBSITE = "https://rpachallengeocr.azurewebsites.net/"
    clear_csv_file(TULOS_FILE)
    open_website(WEBSITE)
    start()
    sleep(0.05)
    page_data = gather_page_data()
    information_handler(page_data, TULOS_FILE, WEBSITE)
    submit(TULOS_FILE)
    sleep(5)

def clear_csv_file(file_path):
    """Clear the contents of the CSV file."""
    with open(file_path, 'w', newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["ID", "DueDate", "InvoiceNo", "InvoiceDate", "CompanyName", "TotalDue"])

def open_website(url):
    browser.goto(url)

def start():
    page = browser.page()
    page.click("id=start")

def get_page_information():
    page = browser.page()
    html_page = page.content()   
    soup = BeautifulSoup(html_page, "html.parser")
    return soup

def next_page():
    page = browser.page()
    element = page.query_selector(f"[class='paginate_button next']")
    if element:
        element.click()
        return True
    return False

def get_table_data(soup):
    return soup.find_all("tr", class_=["odd", "even"])

def gather_page_data():
    page_data = []
    data = get_page_information()
    page_data.append(get_table_data(data))
    while next_page():
        data = get_page_information()
        page_data.append(get_table_data(data))
    return page_data

def information_handler(page_data, tulos_file, website):  
    good_data = drop_unwanted_rows(page_data)
    if good_data is None:
        return
    for row in good_data:
        cells = row.find_all("td")
        picture = download_invoice(cells[3].find("a")["href"], cells[0].text.strip(), website)
        text = extract_data_from_picture(picture)
        invoice_number, invoice_date, company_name, total_due = find_keywords(text)
        write_to_csv_file(cells[1].text.strip(), cells[2].text.strip(), invoice_number, invoice_date, company_name, total_due, tulos_file)

def drop_unwanted_rows(page_data):
    good_files = []
    for table in page_data:
        for row in table:
            cells = row.find_all("td")
            if len(cells) < 4:
                continue
            due_date_str = cells[2].text.strip()
            due_date = datetime.strptime(due_date_str, "%d-%m-%Y")
            if due_date > datetime.today():
                continue
            good_files.append(row)
    return good_files

def download_invoice(href, invoice_number_value, website):
    url = f"{website}{href}"
    response = requests.get(url)
    picture = f"output/screenshots/{invoice_number_value}.png"
    with open(picture, "wb") as file:
        file.write(response.content)
    return picture

def extract_data_from_picture(picture):
    img = cv2.imread(picture)
    text = pytesseract.image_to_string(img)
    return text
    
def write_to_csv_file(invoice_id, due_date_str, invoice_number, invoice_date, company_name, total_due, tulos_file):
    with open(tulos_file, "a", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([invoice_id, due_date_str, invoice_number, invoice_date, company_name, total_due])

def submit(file_path):
    page = browser.page()
    page.locator(selector="input[type='file']").set_input_files(file_path)