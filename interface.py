from __future__ import print_function, unicode_literals
from PyInquirer import style_from_dict, Token, prompt, Separator

cards = ['CA (Spark VISA 1086)', 'BP (Spark VISA 1086)',
         'RX (VISA 3715)', 'Company Account']


def intro():
    questions = [
        {
            'type': 'list',
            'name': 'action',
            'message': 'What do you want to do?',
            'choices': [
                'Add a new expense',
                'Edit a current expense',
                'Delete a current expense',
                Separator(),
                'View unsubmitted expenses',
                'View expenses by vendor',
                'View all expenses',
                Separator(),
                'Test 1',
                'List Vendors',
                'Exit',
            ]
        }
    ]
    answers = prompt(questions)
    return answers


def new_expense(vendors):
    questions = [
        {'type': 'input', 'name': 'date', 'message': 'Expense date?'},
        {'type': 'input', 'name': 'description',
            'message': 'Expense description?'},
        {
            'type': 'list',
            'name': 'card',
            'message': 'Which company card was used?',
            'choices': cards
        },
        {
            'type': 'list',
            'name': 'vendor',
            'message': 'Vendor?',
            'choices': vendors
        },
        {
            'type': 'input',
            'name': 'new_vendor',
            'message': 'New vendor name?',
            'when': lambda answers: answers['vendor'] == 'New Vendor'
        },
        {'type': 'input', 'name': 'amount',
         'message': 'Amount? (excluding $)'},
    ]
    answers = prompt(questions)

    if answers['vendor'] == 'New Vendor':
        answers['vendor'] = answers['new_vendor']
        del answers['new_vendor']

    return answers


def vendor_expenses(vendors):
    questions = [
        {
            'type': 'list',
            'name': 'vendor',
            'message': 'Expense vendor?',
            'choices': vendors
        },
    ]
    answers = prompt(questions)

    return answers


def edit_expense(expenses, vendors):

    questions = [
        {
            'type': 'list',
            'name': 'expense',
            'message': 'What expense would you like to edit?',
            'choices': expenses
        },
        {
            'type': 'confirm',
            'message': 'Do you need to update the expense date?',
            'name': 'update_date',
            'default': False,
        },
        {
            'type': 'input',
            'name': 'date',
            'message': 'What is the udpated date?',
            'when': lambda answers: answers['update_date'] == True
        },
        {
            'type': 'confirm',
            'message': 'Do you need to update the expense description?',
            'name': 'update_description',
            'default': False,
        },
        {
            'type': 'input',
            'name': 'description',
            'message': 'What is the udpated description?',
            'when': lambda answers: answers['update_description'] == True
        },
        {
            'type': 'confirm',
            'message': 'Do you need to update the expense card?',
            'name': 'update_card',
            'default': False,
        },
        {
            'type': 'list',
            'name': 'card',
            'message': 'Which is the updated card?',
            'choices': cards,
            'when': lambda answers: answers['update_card'] == True
        },
        {
            'type': 'confirm',
            'message': 'Do you need to update the expense vendor?',
            'name': 'update_vendor',
            'default': False,
        },
        {
            'type': 'list',
            'name': 'vendor',
            'message': 'What is the udpated vendor?',
            'choices': vendors,
            'when': lambda answers: answers['update_vendor'] == True
        },
        {
            'type': 'input',
            'name': 'vendor',
            'message': 'New vendor name?',
            'when': lambda answers: answers['update_vendor'] == True and answers['vendor'] == 'New Vendor'
        },
        {
            'type': 'confirm',
            'message': 'Do you need to update the expense amount?',
            'name': 'update_amount',
            'default': False,
        },
        {
            'type': 'input',
            'name': 'amount',
            'message': 'What is the udpated amount (excluding $)?',
            'when': lambda answers: answers['update_amount'] == True
        },
    ]

    answers = prompt(questions)

    del answers['update_date']
    del answers['update_description']
    del answers['update_card']
    del answers['update_vendor']
    del answers['update_amount']

    return answers


def delete_expense(expenses):

    questions = [
        {
            'type': 'list',
            'name': 'expense',
            'message': 'What expense would you like to delete?',
            'choices': expenses
        },
        {
            'type': 'confirm',
            'message': "Are you sure you want to delete this expense? THIS ACTION CAN'T BE UNDONE!",
            'name': 'delete',
            'default': False,
        },
    ]

    answers = prompt(questions)

    return answers
