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
from _config import TULOS_FILE, WEBSITE, TESSERACT_CMD

pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD
@task
def challenge():
    """Invoice extraction challenge."""
    clear_csv_file()
    open_website()
    start()
    sleep(0.05)
    page_data = gather_page_data()
    information_handler(page_data)
    submit()
    sleep(5)

def clear_csv_file():
    """Clear the contents of the CSV file."""
    with open(TULOS_FILE, 'w', newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["ID", "DueDate", "InvoiceNo", "InvoiceDate", "CompanyName", "TotalDue"])

def open_website():
    """Open the challenge website."""
    browser.goto(WEBSITE)

def start():
    """Presses start button."""
    page = browser.page()
    page.click("id=start")

def get_page_information():
    """Using BeautifulSoup to parse the page content."""
    page = browser.page()
    html_page = page.content()   
    soup = BeautifulSoup(html_page, "html.parser")
    return soup

def next_page():
    """Clicks the next table page button, if available."""
    page = browser.page()
    element = page.query_selector(f"[class='paginate_button next']")
    if element:
        element.click()
        return True
    return False

def get_table_data(soup):
    """Extracts the table data from the page."""
    return soup.find_all("tr", class_=["odd", "even"])

def gather_page_data():
    """Gathers all the data from the pages into one list."""
    page_data = []
    data = get_page_information()
    page_data.append(get_table_data(data))
    while next_page():
        data = get_page_information()
        page_data.append(get_table_data(data))
    return page_data

def information_handler(page_data):  
    """Acts as a umbrella function for the data extraction and writing to CSV."""
    good_data = drop_unwanted_rows(page_data)
    if good_data is None:
        return
    extracted_data = extract_data(good_data)
    write_to_csv_file(extracted_data)

def drop_unwanted_rows(page_data):
    """Drops rows that are not needed to process."""
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

def extract_data(data):
    """Extracts relevant data from the tables."""
    relevant_data = []
    for row in data:
        cells = row.find_all("td")
        picture = download_invoice(cells[3].find("a")["href"], cells[0].text.strip())
        if picture is None:
            continue
        text = extract_data_from_picture(picture)
        if text is None:
            continue
        invoice_number, invoice_date, company_name, total_due = find_keywords(text)
        relevant_data.append ((cells[1].text.strip(), cells[2].text.strip(), invoice_number, invoice_date, company_name, total_due))
    return relevant_data

def download_invoice(href, invoice_number_value):
    """Downloads the invoice document."""
    url = f"{WEBSITE}{href}"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    picture = f"output/screenshots/{invoice_number_value}.png"
    with open(picture, "wb") as file:
        file.write(response.content)
    return picture

def extract_data_from_picture(picture):
    """Extracts the text from the invoice document."""
    img = cv2.imread(picture)
    if not img:
        return None
    text = pytesseract.image_to_string(img)
    return text
    
def write_to_csv_file(invoice_id, due_date_str, invoice_number, invoice_date, company_name, total_due):
    """Writes the extracted data to the CSV file."""
    with open(TULOS_FILE, "a", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([invoice_id, due_date_str, invoice_number, invoice_date, company_name, total_due])

def submit():
    """Submits the CSV file."""
    page = browser.page()
    page.locator(selector="input[type='file']").set_input_files(TULOS_FILE)