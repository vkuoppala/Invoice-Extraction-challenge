from time import sleep
from robocorp.tasks import task
from robocorp import browser
from bs4 import BeautifulSoup
import pytesseract
import cv2
import requests
import csv
import os
from datetime import datetime
from company import find_keywords
from _config import TULOS_FILE, WEBSITE, TESSERACT_CMD, HEADER

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
        csvwriter.writerow(HEADER)

def open_website():
    """Open the challenge website."""
    browser.goto(WEBSITE)

def start():
    """Presses start button."""
    page = browser.page()
    page.click("id=start")

def get_page_information():
    """Using BeautifulSoup to parse the page content."""
    many_tables = []
    page = browser.page()
    html_page = page.content()   
    soup = BeautifulSoup(html_page, "html.parser")
    table = soup.find_all("tr", class_=["odd", "even"])
    for rows in table:
        cells = rows.find_all("td")
        many_cells = {}
        many_cells["id"] = cells[0].text.strip()
        many_cells["invoice_number"] = cells[1].text.strip()
        many_cells["due_date"] = cells[2].text.strip()
        many_cells["invoice"] = cells[3].find("a")["href"]
        many_tables.append(many_cells)
    return many_tables

def next_page():
    """Clicks the next table page button, if available."""
    page = browser.page()
    element = page.query_selector(f"[class='paginate_button next']")
    if element:
        element.click()
        return True
    return False

def gather_page_data():
    """Gathers all the data from the pages into one list."""
    page_data = []
    for dict in get_page_information():
        page_data.append(dict)
    while next_page():
        for dict in get_page_information():
            page_data.append(dict)
    good_data = drop_unwanted_rows(page_data)
    if good_data is None:
        return
    return good_data

def drop_unwanted_rows(page_data):
    """Drops rows that are not needed to process."""
    good_files = []
    for cells in page_data:
        if len(cells) < 4:
            continue
        due_date_str = cells["due_date"]
        due_date = datetime.strptime(due_date_str, "%d-%m-%Y")
        if due_date > datetime.today():
            continue
        good_files.append(cells)
    return good_files

def information_handler(good_data):  
    """Acts as a umbrella function for the data extraction and writing to CSV."""
    extracted_data = extract_data(good_data)
    write_to_csv_file(extracted_data)

def extract_data(data):
    """Extracts relevant data from the tables."""
    relevant_data = []
    for cells in data:
        picture = download_invoice(cells["invoice"], cells["id"])
        if picture is None:
            continue
        text = extract_data_from_picture(picture)
        if text is None:
            continue
        invoice_number, invoice_date, company_name, total_due = find_keywords(text)
        relevant_data.append ((cells["invoice_number"], cells["due_date"], invoice_number, invoice_date, company_name, total_due))
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
    if img is None:
        return None
    text = pytesseract.image_to_string(img)
    return text
    
def write_to_csv_file(extracted_data):
    """Writes the extracted data to the CSV file."""
    with open(TULOS_FILE, "a", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        for row in extracted_data:
            csvwriter.writerow(row)

def submit():
    """Submits the CSV file."""
    page = browser.page()
    page.locator(selector="input[type='file']").set_input_files(TULOS_FILE)