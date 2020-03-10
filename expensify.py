import sys
import os
from tabulate import tabulate  # better printing of db table info

# import internal modules
import settings  # import project setting
import interface  # all termainl interface elements
import db  # all sqlite database functions


# check for database, create if not there
def check_for_database():
    # get the path of the python program
    program_path = os.path.dirname(os.path.realpath(__file__))
    # set the correct path for the database
    db_path = str(program_path + '/' + settings.db)

    if os.path.exists(db_path):
        return True
    else:
        return False


# add a new expense to the database
def add_expense():

    vendors = get_vendors()
    if vendors:
        vendors.append('New Vendor')
    else:
        vendors = ['New Vendor']

    # TODO: setup new card entry system (like vendors)
    # TODO: new expense no cards present

    insert_data = interface.new_expense(vendors)

    insert_data['receipt'] = '/path'
    insert_data['status'] = 0
    insert_data['id'] = None

    command = "INSERT INTO expenses VALUES (:id, :date, :description, :card, :vendor, :amount, :receipt, :status)"

    status = db.execute(command, insert_data)
    if status:
        print(color.BOLD + '\n* New expenses added!' + color.END)
    else:
        print(color.BOLD + '\n* ERROR! New expense not added.' + color.END)


# edit an existing "unsubmitted" expense
def edit_expense():

    # get the "unsubmitted" (status=0) expenses in the database
    expenses = sort_expenses(get_expenses(0))

    if expenses == []:
        print('\nNo expenses available to edit!')
    else:
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
                print(color.BOLD + '\n* Expenses updates!' + color.END)
            else:
                print(color.BOLD + '\n* ERROR! Expense was not updated.' + color.END)
        else:  # if nothing was actually change about the expense in the interface
            print('No changes were made!')


# delete an existing "unsubmitted" expense
def delete_expense():
    expenses = sort_expenses(get_expenses(0))
    if expenses == []:
        print('\nNo expenses available to delete!')
    else:
        editable_expenses = interface_list(expenses)

        expense_to_delete = interface.delete_expense(editable_expenses)

        if expense_to_delete['delete'] == True:
            # format the returned text to get expense record id
            expense_to_delete_id = expense_to_delete['expense'].split(
                ' | ')[-1].split(': ')[-1]

            command = f"DELETE from expenses WHERE id={expense_to_delete_id}"
            status = db.execute(command)

            if status:
                print(color.BOLD + '\n* Expenses deleted!' + color.END)
            else:
                print(color.BOLD + '\n* ERROR! Expense was not deleted.' + color.END)
        else:
            print('Expense deletion cancelled!')


# mark existing unsubmitted expense(s) as submitted
def mark_expense_submitted():
    expenses = sort_expenses(get_expenses(0))
    if expenses == []:
        print('\nNo matching expenses!')
    else:
        # generate interface list of available expenses
        editable_expenses = interface_list(expenses)

        # present available expenses for selection by user
        expense_to_mark = interface.mark_expense_submitted(
            editable_expenses)

        if expense_to_mark:
            # loop through selected expense(s)
            for expense in expense_to_mark['expenses']:
                # format the returned text to get expense record id
                expense_to_mark_id = expense.split(' | ')[-1].split(': ')[-1]

                # mark expense as submitted in database
                command = f"UPDATE expenses SET status=1 WHERE id={expense_to_mark_id}"

                # check database write status and report to user
                status = db.execute(command)
                if not status:
                    print(color.BOLD +
                          '\n* ERROR! Expense(s) not updated.' + color.END)
                    break

            # if every expense was submitted correctly, let user know
            if status:
                print(color.BOLD + '\n* Expense(s) marked as submitted!' + color.END)

        else:
            print('No expenses selected! Update cancelled!')


# mark existing submitted expense(s) as unsubmitted
def mark_expense_unsubmitted():
    expenses = sort_expenses(get_expenses(1))
    if expenses == []:
        print('\nNo matching expenses!')
    else:
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
                    print(color.BOLD +
                          '\n* ERROR! Expense(s) not updated.' + color.END)
                    break

            if status:
                print(color.BOLD + '\n* Expense(s) marked as unsubmitted!' + color.END)

        else:
            print('No expenses selected! Update cancelled!')


# get all vendors currently in database
def get_vendors():
    command = "SELECT Vendor FROM expenses"
    vendors = db.fetchall(command)

    if vendors == []:
        return False
    else:
        # break vendor out of tuples
        vendors = [item for sublist in vendors for item in sublist]
        # sort vendors list and remove duplicates
        return sorted(list(set(vendors)))


# get expenses of status (0 == unsubmitted, 1 == submitted, 'ALL' == All)
def get_expenses(status):
    if status == 'ALL':
        command = "SELECT * FROM expenses"
    else:
        command = f"SELECT * FROM expenses WHERE status={status}"
    expenses = db.fetchall(command)

    return expenses


# get all expenses from vendor
def get_vendor_expenses(selected_vendor):
    command = "SELECT * FROM expenses WHERE vendor=:vendor"
    expenses = db.fetchall(command, selected_vendor)
    return expenses


# accept list of expenses, return sorted list of dicts
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


# generate list of expenses for interface
def interface_list(expenses):
    interface_list = []
    for expense in expenses:
        title = f"{expense['date']} | ${expense['amount']:.2f} | {expense['description']} | {expense['vendor']} | ID: {expense['id']}"
        interface_list.append(title)
    return interface_list


# cleaup and print expenses in terminal
def print_expenses(expenses, hide_vendor=False):
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

    # check to see if expenses.db database is created
    # TODO: check on sqlite db error catching
    # https://www.sqlitetutorial.net/sqlite-python/create-tables/
    valid_db = check_for_database()
    if not valid_db:
        print('\nExepense database not found! Creating a new one...\n')
        status = db.create_db()

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
        if expenses == []:
            print('\nNo matching expenses!')
        else:
            print_expenses(expenses)

    if action['action'] == 'View submitted expenses':
        expenses = get_expenses(1)
        if expenses == []:
            print('\nNo matching expenses!')
        else:
            print_expenses(expenses)

    if action['action'] == 'View expenses by vendor':
        vendors = get_vendors()

        if vendors:
            vendors = sorted(list(set(vendors)))
            selected_vendor = interface.vendor_expenses(vendors)
            expenses = get_vendor_expenses(selected_vendor)
            print_expenses(expenses)
        else:
            print('\nNo current vendors!')

    if action['action'] == 'View all expenses':
        expenses = get_expenses('ALL')
        if expenses == []:
            print('\nNo matching expenses!')
        else:
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

    return True


if __name__ == '__main__':

    status = True
    while status:
        status = main()
