# Expensify CLI Expense Tracking App 

expensify.py - Main Application  
interface.py - PyInquirer CLI Interface Elements  
db.py - SQLite Databse Funcation

## Requirements:

[pyfpdf: FPDF for Python](https://github.com/reingart/pyfpdf)  
[PyPDF2](https://github.com/mstamy2/PyPDF2)  
[PythonInquirer](https://github.com/CITGuru/PyInquirer)  
[python-tabulate](https://github.com/astanin/python-tabulate)  
[sqlite3](https://docs.python.org/3/library/sqlite3.html)  

## Database Setup: expensify.db

### expenses Table Schema:

- id (INTEGER): expense id *(primary key)*
- date (TEXT): date *(ex. 2000-01-01)*
- description(TEXT): description of expense
- card (TEXT): company card used
- vendor (TEXT): expense vendor
- amount (TEXT): dollar amount of expense
- receipt (TEXT): path to locally stored PDF receipt
- status (INTEGER): 0 = not submitted, 1 = subitted

### cards Table Schema:

- id (INTEGER): expense card id *(primary key)*
- date (TEXT): date added *(CURRENT_TIMESTAMP)*
- name (TEXT): card name/nickname
- type (TEXT): type/brand of card *(ex. visa, amex, other)*
- digits (TEXT): last four digits of the card number
- status (INTEGER): 0 = inactive, 1 = active

### vendors Table Schema:

- id (INTEGER): vendor id *(primary key)*
- date (TEXT): date added *(CURRENT_TIMESTAMP)*
- name (TEXT): vendor name
- status (INTEGER): 0 = inactive, 1 = active

## TO-DO's

*general*
- [ ] delete multiple expenses
- [ ] move color to interface.py
- [ ] check if exact record already exists
- [ ] sanitize input data
- [ ] add proper spacing in code
- [ ] add comments to code
- [ ] make sure all messages are BOLD

*database*

- [x] check to see if expenses.db database is created
- [ ] check on sqlite db error catching
- [ ] import csv of external expenses
- [ ] new expense no cards present

*vendors*

- [ ] new vendor can't be int
- [ ] make sure "new vendor" isn't already a vendor


*expense report*

- [ ] generate expense report
- [ ] view old reports

*file storage*

- [ ] setup file storage/linking with database path