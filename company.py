import re
from datetime import datetime
from abc import ABC, abstractmethod
from data_storage_classes import CompanyData

class Company(ABC):

    company_list = []

    def __init__(self, company_name, invoice_number, invoice_date, total_due):
        self.number = invoice_number
        self.date = invoice_date
        self.company_name = company_name
        self.total_due = total_due

    def __str__(self):
        return f"Company(name={self.company_name}, number={self.number}, date={self.date}, total_due={self.total_due})"

    def get_number(self):
        return self.number
    
    def set_number(self, number):
        self.number = number
    
    @abstractmethod
    def get_date(self):
        pass
    
    @abstractmethod
    def set_date(self, date):
        pass
    
    def get_company_name(self):
        return self.company_name
    
    def get_total_due(self):    
        return self.total_due
    
    def set_total_due(self, total_due):
        self.total_due = total_due
    
    def get_company_list(self):
        return Company.company_list
    
    @abstractmethod
    def create_from_text(cls, text):
        pass
    
class AeneanLLC(Company):
    def __init__(self):
        self.company_name = "Aenean LLC"
        self.number = None
        self.date = None
        self.total_due = None
        Company.company_list.append(self)

    def get_date(self):
        return self.date

    def set_date(self, date):
        self.date = datetime.strptime(date, "%Y-%m-%d").strftime("%d-%m-%Y")

    def create_from_text(self, text):
        self.set_number(re.search(r'Invoice #(\d+)', text).group(1))
        self.set_date(re.search(r'(\d{4}-\d{2}-\d{2})', text).group(1))
        self.set_total_due(re.search(r'Total (\d+\.\d{2})', text).group(1))

class SitAmetCorp(Company):
    def __init__(self):
        self.company_name = "Sit Amet Corp"
        self.number = None
        self.date = None
        self.total_due = None
        Company.company_list.append(self)

    def get_date(self):
        return self.date

    def set_date(self, date):
        self.date = datetime.strptime(date, "%B %d, %Y").strftime("%d-%m-%Y")

    def create_from_text(self, text):
        self.set_number(re.search(r'# (\d+)', text).group(1))
        self.set_date(re.search(r'Date: (\w+ \d{2}, \d{4})', text).group(1))
        self.set_total_due(re.search(r'Total \$([\d,]+\.\d{2})', text).group(1))

def find_keywords(text):
    all_companies = [AeneanLLC(), SitAmetCorp()]
    for company in all_companies:
        company_name_match = re.search(company.get_company_name(), text)
        if company_name_match:
            company.create_from_text(text)
            return CompanyData(
                invoice_number=company.get_number(), 
                invoice_date=company.get_date(), 
                company_name=company.get_company_name(), 
                total_due=company.get_total_due())
    return None