import sys
import os
import interface  # all termainl interface elements
import db  # all sqlite database functions
from tabulate import tabulate


# TODO: generate expense report
# TODO: setup file storage/linking with database path
# TODO: make sure "new vendor" is already a vendor
# TODO: remove '$' from any entered amount

def add_expense():  # add a new expense to the database
    vendors = get_vendors() + ['New Vendor']
    insert_data = interface.new_expense(vendors)

    # add info not aksed in interface
    insert_data['receipt'] = '/path'
    insert_data['status'] = 0
    insert_data['id'] = None

    command = "INSERT INTO expenses VALUES (:id, :date, :description, :card, :vendor, :amount, :receipt, :status)"
    status = db.execute(command, insert_data)

    if status:
        print(color.BOLD + '* New expenses added!' + color.END)
    else:
        print(color.BOLD + '* ERROR! New expense not added.' + color.END)


def edit_expense():  # edit an existing "unsubmitted" expense
    expenses = sort_expenses(get_expenses(0))
    editable_expenses = interface_list(expenses)

    vendors = get_vendors() + ['New Vendor']
    expense_to_edit = interface.edit_expense(
        editable_expenses, vendors)

    if len(expense_to_edit) > 1:

        # format the returned text to get expense record id
        expense_to_edit_id = expense_to_edit['expense'].split(
            ' | ')[-1].split(': ')[-1]

        # setup correct formatting for sql command
        edits = []
        command_text = []
        attributes = ['date', 'description', 'card', 'vendor', 'amount']

        for attribute in attributes:
            if attribute in expense_to_edit:
                edits.append(expense_to_edit[attribute])
                command_text.append(attribute + ' = ?')

        command = f"UPDATE expenses SET {', '.join(command_text)} WHERE id={expense_to_edit_id}"
        status = db.execute(command, edits)

        if status:
            print(color.BOLD + '* Expenses updates!' + color.END)
        else:
            print(color.BOLD + '* ERROR! Expense was not updated.' + color.END)
    else:  # if nothing was actually change about the expense in the interface
        print('No changes were made!')


def delete_expense():  # delete an existing "unsubmitted" expense
    expenses = sort_expenses(get_expenses(0))
    editable_expenses = interface_list(expenses)

    expense_to_delete = interface.delete_expense(editable_expenses)

    if expense_to_delete['delete'] == True:
        # format the returned text to get expense record id
        expense_to_delete_id = expense_to_delete['expense'].split(
            ' | ')[-1].split(': ')[-1]

        command = f"DELETE from expenses WHERE id={expense_to_delete_id}"
        status = db.execute(command)

        if status:
            print(color.BOLD + '* Expenses deleted!' + color.END)
        else:
            print(color.BOLD + '* ERROR! Expense was not deleted.' + color.END)
    else:
        print('Expense deletion cancelled!')


def mark_expense_submitted():  # mark existing unsubmitted expense(s) as submitted
    expenses = sort_expenses(get_expenses(0))
    editable_expenses = interface_list(expenses)

    expense_to_mark = interface.mark_expense_submitted(
        editable_expenses)

    if expense_to_mark != False:
        # loop through selected expense(s)
        for expense in expense_to_mark['expenses']:
            # format the returned text to get expense record id
            expense_to_mark_id = expense.split(' | ')[-1].split(': ')[-1]
            command = f"UPDATE expenses SET status=1 WHERE id={expense_to_mark_id}"
            status = db.execute(command)

            if status == False:
                print(color.BOLD + '* ERROR! Expense(s) not updated.' + color.END)
                break

        if status:
            print(color.BOLD + '* Expense(s) marked as submitted!' + color.END)

    else:
        print('No expenses selected! Update cancelled!')


def mark_expense_unsubmitted():  # mark existing submitted expense(s) as unsubmitted
    expenses = sort_expenses(get_expenses(1))
    editable_expenses = interface_list(expenses)

    expense_to_mark = interface.mark_expense_unsubmitted(
        editable_expenses)

    if expense_to_mark != False:
        # loop through selected expense(s)
        for expense in expense_to_mark['expenses']:
            # format the returned text to get expense record id
            expense_to_mark_id = expense.split(' | ')[-1].split(': ')[-1]
            command = f"UPDATE expenses SET status=0 WHERE id={expense_to_mark_id}"
            status = db.execute(command)

            if status == False:
                print(color.BOLD + '* ERROR! Expense(s) not updated.' + color.END)
                break

        if status:
            print(color.BOLD + '* Expense(s) marked as unsubmitted!' + color.END)

    else:
        print('No expenses selected! Update cancelled!')


def get_vendors():  # get all vendors currently in database
    command = "SELECT Vendor FROM expenses"
    vendors = db.fetchall(command)

    # break vendor out of tuples
    vendors = [item for sublist in vendors for item in sublist]

    # sort vendors list and remove duplicates
    return sorted(list(set(vendors)))


def get_all_expenses():  # get every expense from the database
    command = "SELECT * FROM expenses"
    expenses = db.fetchall(command)
    return expenses


def get_expenses(status):  # get all expenses of status (0 == unsubmitted, 1 == submitted)
    command = f"SELECT * FROM expenses WHERE status={status}"
    expenses = db.fetchall(command)
    return expenses


def get_vendor_expenses(selected_vendor):  # get all expenses from vendor
    command = "SELECT * FROM expenses WHERE vendor=:vendor"
    expenses = db.fetchall(command, selected_vendor)
    return expenses


def sort_expenses(expenses):  # accept list of expenses, return sorted list of dicts
    sorted_expenses = []
    for expense in expenses:
        d = {'id': expense[0],
             'date': expense[1],
             'description': expense[2],
             'card': expense[3],
             'vendor': expense[4],
             'amount': expense[5],
             'receipt': expense[6],
             'status': expense[7],
             }
        sorted_expenses.append(d)
    sorted_expenses.sort(key=lambda x: (x['date'], x['vendor']))
    return sorted_expenses


def interface_list(expenses):  # generate list of expenses for interface
    interface_list = []
    for expense in expenses:
        title = f"{expense['date']} | ${expense['amount']:.2f} | {expense['description']} | {expense['vendor']} | ID: {expense['id']}"
        interface_list.append(title)
    return interface_list


def print_expenses(expenses, hide_vendor=False):  # cleaup and print expenses in terminal
    expenses = sort_expenses(expenses)
    for n, expense in enumerate(expenses):
        del expenses[n]['id']
        del expenses[n]['receipt']
        if expenses[n]['status'] == 0:
            expenses[n]['status'] = 'N'
        else:
            expenses[n]['status'] = 'Y'

    print('')
    print(tabulate(expenses, headers="keys",
                   tablefmt='simple', showindex=False, floatfmt='.2f'))


class color:  # terminal coloring and bolding
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def main():

    # run intro menu interface and get user action
    action = interface.intro()

    # act upon the user selected action
    if action['action'] == 'Add a new expense':
        add_expense()

    if action['action'] == 'Edit a current expense':
        edit_expense()

    if action['action'] == 'Delete a current expense':
        delete_expense()

    if action['action'] == 'Mark expenses(s) as submitted':
        mark_expense_submitted()

    if action['action'] == 'Mark expenses(s) as unsubmitted':
        mark_expense_unsubmitted()

    if action['action'] == 'View unsubmitted expenses':
        expenses = get_expenses(0)
        print_expenses(expenses)

    if action['action'] == 'View expenses by vendor':
        vendors = sorted(list(set(get_vendors())))
        selected_vendor = interface.vendor_expenses(vendors)
        expenses = get_vendor_expenses(selected_vendor)
        print_expenses(expenses, True)

    if action['action'] == 'View all expenses':
        expenses = get_all_expenses()
        print_expenses(expenses)

    # exit the program
    if action['action'] == 'Exit':
        return False

    # testing menu items for easy access
    if action['action'] == 'Test 1':
        interface.pizza()

    # check to see if users wants to continue using program
    print('')
    cont = interface.cont_program()

    if cont:
        os.system('clear')
        return True
    else:
        return False


if __name__ == '__main__':
    status = True
    while status:
        status = main()
