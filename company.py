import re
from datetime import datetime

class Company:
    def __init__(self, company_name, invoice_number, invoice_date, total_due):
        self.number = invoice_number
        self.date = invoice_date
        self.company_name = company_name
        self.total_due = total_due

    def __str__(self):
        return f"Company(name={self.company_name}, number={self.number}, date={self.date}, total_due={self.total_due})"

    def get_number(self):
        return self.number
    
    def get_date(self):
        return self.date
    
    def get_company_name(self):
        return self.company_name
    
    def get_total_due(self):    
        return self.total_due
    
def create_Aenean_LLC(text):
    """Create companies."""
    Aenean_LLC = Company("Aenean LLC", re.search(r'Invoice #(\d+)', text).group(1),
                          re.search(r'(\d{4}-\d{2}-\d{2})', text).group(1), re.search(r'Total (\d+\.\d{2})', text).group(1))
    return Aenean_LLC

def create_Sit_Amet_Corp(text):
    """Create companies."""
    Sit_Amet_Corp = Company("Sit Amet Corp", re.search(r'# (\d+)', text).group(1),
                             re.search(r'Date: (\w+ \d{2}, \d{4})', text).group(1), re.search(r'Total \$([\d,]+\.\d{2})', text).group(1))
    return Sit_Amet_Corp