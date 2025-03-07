from dataclasses import dataclass

@dataclass
class RelevantPageData:
	page_id: str
	invoice_id: str
	due_date: str
	invoice: str
	length: int
	
@dataclass
class InvoiceData:
	invoice_id: str
	due_date: str
	invoice_number: str
	invoice_date: str
	company_name: str
	total_due: str
	
@dataclass
class CompanyData:
	company_name: str
	invoice_number: str
	invoice_date: str
	total_due: str