import os
import db  # sqlite database functions
import interface  # termainl interface elements
import helpers  # program helper functions


def main():

    os.system('clear')

    # check to see if the expensify database is present
    if not db.check_for_database():
        print(interface.color.BOLD +
              '\n* Expensify database not found! Creating a new one...\n'
              + interface.color.END)
        db.create_db()

    while True:

        # run intro menu interface and get user action
        action = helpers.intro_interface()

        # add a new expense
        if action['action'] == 'Add a New Expense':
            helpers.add_expense()

        # edit a current expense
        if action['action'] == 'Edit a Current Expense':
            helpers.edit_expense(0)

        # viewing expenses
        if action['action'] == 'View Expenses':
            helpers.view_expenses(action['view_type'])

        # inserting test data
        # TODO remove this or move to admin interface
        # TODO remove all test data
        if action['action'] == 'Insert Test Data':
            helpers.insert_test_data(20)  # supply number so test expenses

        # exit the program
        if action['action'] == 'Exit':
            break

        # check to see if users wants to continue using program
        print('')
        cont = interface.cont_program()

        if cont:
            os.system('clear')
            pass
        else:
            break


if __name__ == '__main__':
    main()
