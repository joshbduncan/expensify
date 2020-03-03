import sys
import interface  # all termainl interface elements
import db  # all sqlite database functions
from tabulate import tabulate


# add a new expense to the database
def add_expense():
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


# edit an existing "unsubmitted" expense
def edit_expense():
    expenses = sort_expenses(get_expenses(0))
    editable_expenses = []

    # generate a sorted list of unsubmitted expenses for interface
    for expense in expenses:
        title = f"{expense['date']} | ${expense['amount']:.2f} | {expense['description']} | {expense['vendor']}) | ID: {expense['id']}"
        editable_expenses.append(title)

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
        sys.exit(0)


# delete an existing "unsubmitted" expense
def delete_expense():
    expenses = sort_expenses(get_expenses(0))
    editable_expenses = []

    # generate a sorted list of unsubmitted expenses for interface
    for expense in expenses:
        title = f"{expense['date']} | ${expense['amount']:.2f} | {expense['description']} | {expense['vendor']}) | ID: {expense['id']}"
        editable_expenses.append(title)

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
        sys.exit(0)


# mark an existing unsubmitted expense(s) as submitted
def mark_expense_submitted():
    expenses = sort_expenses(get_expenses(0))
    editable_expenses = []

    # generate a sorted list of unsubmitted expenses for interface
    for expense in expenses:
        title = f"{expense['date']} | ${expense['amount']:.2f} | {expense['description']} | {expense['vendor']}) | ID: {expense['id']}"
        editable_expenses.append(title)

    expense_to_mark = interface.mark_expense_submitted(
        editable_expenses)

    if expense_to_mark['mark'] == True:
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
        print('Expense(s) update cancelled!')
        sys.exit(0)


# mark an existing submitted expense(s) as unsubmitted
def mark_expense_unsubmitted():
    expenses = sort_expenses(get_expenses(1))
    editable_expenses = []

    # generate a sorted list of unsubmitted expenses for interface
    for expense in expenses:
        title = f"{expense['date']} | ${expense['amount']:.2f} | {expense['description']} | {expense['vendor']}) | ID: {expense['id']}"
        editable_expenses.append(title)

    expense_to_mark = interface.mark_expense_unsubmitted(
        editable_expenses)

    if expense_to_mark['mark'] == True:
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
        print('Expense(s) update cancelled!')
        sys.exit(0)


# get all vendors currently in database
def get_vendors():
    command = "SELECT Vendor FROM expenses"
    vendors = db.fetchall(command)

    # break vendor out of tuples
    vendors = [item for sublist in vendors for item in sublist]

    # sort vendors list and remove duplicates
    return sorted(list(set(vendors)))


# get every expense from the database
def get_all_expenses():
    command = "SELECT * FROM expenses"
    expenses = db.fetchall(command)
    return expenses


# get all expenses that haven't been submitted
def get_expenses(status):  # 0 == unsubmitted, 1 == submitted

    command = f"SELECT * FROM expenses WHERE status={status}"
    expenses = db.fetchall(command)
    return expenses


# get all expenses from provided vendor
def get_vendor_expenses(selected_vendor):
    command = "SELECT * FROM expenses WHERE vendor=:vendor"
    expenses = db.fetchall(command, selected_vendor)
    return expenses


# accept a list of expenses from database
# make dictionay for each expense and return all in soted list
def sort_expenses(expenses):
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


# cleaup and print out provided expenses in terminal
def print_expenses(expenses, hide_vendor=False):
    expenses = sort_expenses(expenses)
    for n, expense in enumerate(expenses):
        del expenses[n]['id']
        del expenses[n]['receipt']
        if expenses[n]['status'] == 0:
            expenses[n]['status'] = 'N'
        else:
            expenses[n]['status'] = 'Y'

    print(tabulate(expenses, headers="keys",
                   tablefmt='simple', showindex=False, floatfmt='.2f'))


# terminal coloring and bolding
class color:
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
    if action['action'] == 'Exit':
        sys.exit(0)

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

    # TO-DO: generate expense report

    # TO-DO: mark current expense as sbumitted

    # testing menu items for easy access
    if action['action'] == 'Test 1':
        expenses = get_expenses(0)
        print_expenses(expenses)

    if action['action'] == 'List Vendors':
        vendors = get_vendors()
        for vendor in vendors:
            print(vendor)


if __name__ == '__main__':
    main()
