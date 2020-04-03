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

## TO-DO's

*general*
- [ ] delete multiple expenses
- [ ] move color to interface.py
- [ ] check if exact record already exists
- [ ] sanitize input data
- [ ] add proper spacing in code
- [ ] add comments to code
- [ ] make sure all messages are BOLD
- [ ] setup admin interface
- [ ] setup check for dupe on new expense function
- [ ] limit editable expense list by card/vendor

*database*

- [x] check to see if expenses.db database is created
- [ ] check on sqlite db error catching
- [ ] import csv of external expenses
- [x] new expense no cards present
- [x] insert test data function
- [ ] setup function to remove test data

*vendors*

- [ ] new vendor can't be int
- [ ] make sure "new vendor" isn't already a vendor


*expense report*

- [ ] generate expense report
- [ ] view old reports

*file storage*

- [ ] setup file storage/linking with database path
