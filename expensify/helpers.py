import sys
import os
import sqlite3
from sqlite3 import Error
from random import randrange
from random import choice
from tabulate import tabulate  # better printing of db table info
import datetime
import db  # sqlite database functions
import interface  # termainl interface elements


###########################
#### GENERAL FUNCTIONS ####
###########################


# TODO do i still need this?
def build_dict(records, table):
    d = []

    for record in records:
        info = {
            'id': record[0],
            'date': record[1],
            'description': record[2],
            'card': record[3],
            'vendor': record[4],
            'amount': record[5],
            'path': record[6],
            'status': record[7],
        }

        d.append(info)

    return l


# cleaup and print expenses in terminal
def print_expenses(expenses):
    expenses = sort_expenses(expenses)

    if not expenses:
        print(interface.color.BOLD +
              '\n* No expenses to print!' + interface.color.END)
        return False
    else:
        for i, expense in enumerate(expenses):
            del expenses[i]['id']
            del expenses[i]['receipt']
            if expenses[i]['status'] == 0:
                expenses[i]['status'] = 'N'
            else:
                expenses[i]['status'] = 'Y'

    print('')
    print(tabulate(expenses, headers="keys",
                   tablefmt='simple', showindex=False, floatfmt='.2f'))


#############################
#### INTERFACE FUNCTIONS ####
#############################


# present intro interface menu
def intro_interface():
    try:
        action = interface.intro()
        if action == {}:
            raise Exception
        else:
            return action
    except:
        os.system('clear')
        intro_interface()


###############################
#### WORKING WITH EXPENSES ####
###############################


# add a new expense to the database
def add_expense():

    cards = get_cards() + ['New Card']
    vendors = get_vendors() + ['New Vendor']

    # present the new expense interface to capture data
    insert_data = interface.new_expense(cards, vendors)

    # if expense card is new swap values
    if insert_data['card'] == 'New Card':
        insert_data['card'] = insert_data['new_card']

    # if vendor is new is new swap values
    if insert_data['vendor'] == 'New Vendor':
        insert_data['vendor'] = insert_data['new_vendor']

    # TODO figure out path and file storage
    # add in missing parameters
    insert_data['receipt'] = '/path'
    insert_data['status'] = 0
    insert_data['id'] = None

    # TODO reconfigure check_for_dupe
    # if check_for_dupe(insert_data):
    #     print(interface.color.BOLD + '\n* Expense already exists!' + interface.color.END)
    # else:
    command = "INSERT INTO expenses VALUES (:id, :date, :description, :card, :vendor, :amount, :receipt, :status)"

    status = db.execute(command, insert_data)
    if status:
        print(interface.color.BOLD +
              '\n* New expenses added!' + interface.color.END)
    else:
        print(interface.color.BOLD +
              '\n* ERROR! New expense not added.' + interface.color.END)


# get all cards currently in database
def get_cards():
    command = "SELECT card FROM expenses"
    cards = db.fetchall(command)

    if cards == []:
        return False
    else:
        # break vendor out of tuples
        cards = [card['card'] for card in cards]
        # sort cards list and remove duplicates
        return sorted(list(set(cards)))


# get all vendors currently in database
def get_vendors():
    command = "SELECT vendor FROM expenses"
    vendors = db.fetchall(command)

    if vendors == []:
        return False
    else:
        # break vendor out of tuples
        vendors = [vendor['vendor'] for vendor in vendors]
        # sort vendors list and remove duplicates
        return sorted(list(set(vendors)))


# check to make sure new/edited expense isn't a duplication
def check_for_dupe(expense):
    # get all database expenses
    expenses = get_expenses('ALL')

    # turn expense into tuple for checking against all expenses
    check_for_dupe = tuple(v for v in expense.values())

    if check_for_dupe[:4] in [expense[1:5] for expense in expenses]:
        return True
    else:
        return False


# edit an existing expense
def edit_expense(status='ALL'):

    # get a list of all expenses in the database
    if status == 'ALL':
        command = "SELECT * FROM expenses"
    else:
        command = f"SELECT * FROM expenses WHERE status={status}"

    fetch = sort_expenses(db.fetchall(command,))

    # TODO limit by vendor or card (default to all)
    # TODO check for any available expenses

    if fetch == []:
        print(interface.color.BOLD +
              '\n* No expenses available to edit!' + interface.color.END)
    else:
        # iterate through returned expenses and make pretty for interface
        expenses = []
        for expense in fetch:
            title = f"{expense['date']} {expense['description']} from {expense['vendor']} for ${expense['amount']:.2f} (ID: {expense['id']})"
            expenses.append(title)

        cards = get_cards() + ['New Card']
        vendors = get_vendors() + ['New Vendor']

        # present edit expense interface and return data
        update_data = interface.edit_expense(expenses, cards, vendors)

        if len(update_data) > 1:
            # if expense card is new swap values
            if 'card' in update_data.keys():
                if update_data['card'] == 'New Card':
                    update_data['card'] = update_data['new_card']

            # if vendor is new is new swap values
            if 'vendor' in update_data.keys():
                if update_data['vendor'] == 'New Vendor':
                    update_data['vendor'] = update_data['new_vendor']

            # format the returned text to get expense record id
            update_data_id = update_data['expense'].split(
                ' (')[-1].split(': ')[-1][:-1]

            # setup correct formatting for sql command
            edits = []
            command_text = []
            attributes = ['date', 'description', 'card', 'vendor', 'amount']

            for attribute in attributes:
                if attribute in update_data:
                    edits.append(update_data[attribute])
                    command_text.append(attribute + ' = ?')

            command = f"UPDATE expenses SET {', '.join(command_text)} WHERE id={update_data_id}"

            # submit update command to database
            status = db.execute(command, edits)

            if status:
                print(interface.color.BOLD +
                      '\n* Expense updated!' + interface.color.END)
            else:
                print(interface.color.BOLD +
                      '\n* ERROR! Expense was not updated.' + interface.color.END)
        else:  # if nothing was actually changed about the expense in the interface
            print(interface.color.BOLD +
                  '\n* No changes were made!' + interface.color.END)


# grab expenses that match view selected in interface
def view_expenses(view_type):
    if view_type == 'Current Expenses':
        command = "SELECT * FROM expenses WHERE status=0"
    elif view_type == 'Submitted Expenses':
        command = "SELECT * FROM expenses WHERE status=1"
    elif view_type == 'All Expenses':
        command = "SELECT * FROM expenses"
    elif view_type == 'By Card':
        # TODO display the card and digits
        cards = get_cards()
        result = interface.select_from_list(
            cards, 'Which card?')
        command = f"SELECT * FROM expenses WHERE card='{result['selection']}'"
    elif view_type == 'By Vendor':
        vendors = get_vendors()
        result = interface.select_from_list(
            vendors, 'Which vendor?')
        command = f"SELECT * FROM expenses WHERE vendor='{result['selection']}'"

    expenses = db.fetchall(command,)
    print_expenses(expenses)


# accept list of expenses (dicts), return sorted list
def sort_expenses(expenses):
    try:
        sorted_expenses = sorted(
            expenses, key=lambda x: (x['date'], x['vendor']))
    except:
        return False
    return sorted_expenses


#########################
#### ADMIN FUNCTIONS ####
#########################


def insert_test_data(records):
    cards = ['Expense Card 3625', 'Expense Card 7485',
             'Expense Card 4859', 'Expense Card 2145']
    vendors = ['Apple', 'Google', 'Bestbuy', 'Amazon',
               'TDW', 'Basecamp', 'Airtable', 'Ford', 'Tesla']

    for i in range(records):
        month = str(randrange(1, 12, 1))
        day = str(randrange(1, 28, 1))
        amount = str(randrange(100, 25000, 1))

        insert_data = {'id': None,
                       'date': f'2019-{month}-{day}',
                       'description': f'Test Expense {i + 1}',
                       'card': choice(cards),
                       'vendor': choice(vendors),
                       'amount': f'{amount[:-2]}.{amount[-2:]}',
                       'receipt': '/path',
                       'status': choice([0, 1]),
                       }

        command = "INSERT INTO expenses VALUES (:id, :date, :description, :card, :vendor, :amount, :receipt, :status)"
        db.execute(command, insert_data)

    print(interface.color.BOLD + '\n* Text Expenses Added!' + interface.color.END)
