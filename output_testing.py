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
def output_testing():
    """Invoice extraction challenge."""
    invoice_number = 0
    open_website("https://rpachallengeocr.azurewebsites.net/")
    start()
    sleep(1)
    invoice_number = get_invoices(invoice_number)
    next_page(2)
    invoice_number = get_invoices(invoice_number)
    next_page(3)
    invoice_number = get_invoices(invoice_number)

def open_website(url):
    browser.goto(url)

def start():
    page = browser.page()
    page.click("id=start")


def get_invoices(invoice_number_counter):
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
        print(invoice_id, due_date_str)
        link = cells[3].find("a")["href"]
        if link:
            invoice_number_counter += 1
            # invoice_number, invoice_date, company_name, total_due = check_invoice(link, invoice_number_counter)
            # write_csv_file(invoice_number, invoice_date, company_name, total_due)
    return invoice_number_counter

def next_page(page_nro):
    open_website("https://rpachallengeocr.azurewebsites.net/")
    sleep(1)
    page = browser.page()
    element = page.query_selector(f"[data-dt-idx='{page_nro}']")
    if element:
        element.click()
