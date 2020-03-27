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

## Database Setup: expenses.db

**expenses Table Schema:**  
  - id (INTEGER): expense id (primary key)
  - date (TEXT): date 2000-01-01
  - description(TEXT): description of expense
  - card (TEXT): company card used
  - vendor (TEXT): expense vendor
  - amount (TEXT): dollar amount of expense
  - receipt (TEXT): path to locally stored PDF receipt
  - status (INTERGER): 0 = not submitted, 1 = subitted

## TO-DO's

- [x] check to see if expenses.db database is created
- [ ] setup new card entry system (like vendors)
- [ ] new expense no cards present
- [ ] check if exact record already exists
- [ ] new vendor can't be int
- [ ] delete multiple expenses
- [ ] check on sqlite db error catching
- [ ] generate expense report
- [ ] sanitize input data
- [ ] view old reports
- [ ] setup file storage/linking with database path
- [ ] make sure "new vendor" is already a vendor
- [ ] add proper spacing in code
- [ ] add comments to code
- [ ] import csv of external expenses
- [ ] make sure all messages are BOLD

