from robocorp import browser
from _config import WEBSITE, TULOS_FILE
from bs4 import BeautifulSoup
from data_storage_classes import RelevantPageData
import requests

def open_website():
    """Open the challenge website."""
    browser.goto(WEBSITE)

def start():
    """Presses start button."""
    page = browser.page()
    page.click("id=start")

def submit():
    """Submits the CSV file."""
    page = browser.page()
    page.locator(selector="input[type='file']").set_input_files(TULOS_FILE)

def next_page():
    """Clicks the next table page button, if available."""
    page = browser.page()
    element = page.query_selector(f"[class='paginate_button next']")
    if element:
        element.click()
        return True
    return False

def html_parser_to_dict(html_page):
    """Using BeautifulSoup to parse the page content."""
    many_tables = []
    soup = BeautifulSoup(html_page, "html.parser")
    table = soup.find_all("tr", class_=["odd", "even"])
    for rows in table:
        cells = rows.find_all("td")
        many_cells = RelevantPageData(
            page_id=cells[0].text.strip(),
            invoice_id=cells[1].text.strip(),
            due_date=cells[2].text.strip(),
            invoice=cells[3].find("a")["href"],
            length=len(cells)
        )
        many_tables.append(many_cells)
    return many_tables

def get_page():
    page = browser.page()
    html_page = page.content()
    return html_page

def download_invoice(href, invoice_number_value):
    """Downloads the invoice document."""
    url = f"{WEBSITE}{href}"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    directory = "output/screenshots"
    picture = f"{directory}/{invoice_number_value}.png"
    with open(picture, "wb") as file:
        file.write(response.content)
    return picture

def main():
    """Main function."""
    pass

if __name__ == "__main__":
    main()