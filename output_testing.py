from time import sleep
from robocorp.tasks import task
from csv_operations import create_csv_file
from web_operations import open_website, start, submit
from process_information import gather_page_data, extract_data

@task
def challenge():
    """Invoice extraction challenge."""
    open_website()
    start()
    sleep(0.5)
    relevant_page_data = gather_page_data()
    extracted_data = extract_data(relevant_page_data)
    create_csv_file(extracted_data)
    submit()
    sleep(5)
