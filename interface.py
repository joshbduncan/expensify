from __future__ import print_function, unicode_literals
from PyInquirer import style_from_dict, Token, prompt, Separator
from PyInquirer import Validator, ValidationError


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


class NumberValidator(Validator):
    def validate(self, document):
        try:
            float(document.text)
        except ValueError:
            raise ValidationError(
                message="Please enter a dollar amount without the '$'.",
                cursor_position=len(document.text))  # Move cursor to end


# def intro():
#     questions = [
#         {
#             'type': 'list',
#             'name': 'action',
#             'message': 'What do you want to do?',
#             'choices': [
#                 'Add a new expense',
#                 'View expenses by card',
#                 Separator(),
#                 'Edit a current expense',
#                 'Delete a current expense',
#                 Separator(),
#                 'View unsubmitted expenses',
#                 'View submitted expenses',
#                 'View expenses by vendor',
#                 'View all expenses',
#                 Separator(),
#                 'Mark expenses(s) as submitted',
#                 'Mark expenses(s) as unsubmitted',
#                 Separator(),
#                 'Exit',
#                 # Separator(),
#                 # 'Test 1',
#             ]
#         }
#     ]


def intro():
    questions = [
        {
            'type': 'list',
            'name': 'action',
            'message': 'What do you want to do?',
            'choices': [
                'Add a New Expense',
                'Edit a Current Expense',
                Separator(),
                'View Expenses',
                'Delete Expense(s)',
                Separator(),
                'Insert Test Data',  # TODO move to admin interface
                Separator(),
                'Exit',
            ]
        },
        {
            'type': 'list',
            'name': 'view_type',
            'message': 'What expenses would you like to view?',
            'choices': [
                'Current Expenses',
                'Submitted Expenses',
                'All Expenses',
                Separator(),
                'By Card',
                'By Vendor',
            ],
            'when': lambda answers: answers['action'] == 'View Expenses',
        },
    ]

    answers = prompt(questions)

    return answers


def new_expense(cards, vendors):
    questions = [
        {'type': 'input', 'name': 'date', 'message': 'Expense date?'},
        {'type': 'input', 'name': 'description',
            'message': 'Expense description?'},
        {
            'type': 'list',
            'name': 'card',
            'message': 'Which expense card was used?',
            'choices': cards
        },
        {
            'type': 'input',
            'name': 'new_card',
            'message': 'New card name?',
            'when': lambda answers: answers['card'] == 'New Card',
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
            'when': lambda answers: answers['vendor'] == 'New Vendor',
        },
        {
            'type': 'input',
            'name': 'amount',
            'message': 'Amount? (excluding $)',
            'validate': NumberValidator,
        },
    ]

    answers = prompt(questions)

    if answers['vendor'] == 'New Vendor':
        answers['vendor'] = answers['new_vendor']
        del answers['new_vendor']

    return answers


def select_from_list(l, message):
    questions = [
        {
            'type': 'list',
            'name': 'selection',
            'message': message,
            'choices': l,
        },
    ]

    answers = prompt(questions)

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


def card_expenses(cards):
    questions = [
        {
            'type': 'list',
            'name': 'card',
            'message': 'Card?',
            'choices': cards
        },
    ]


def edit_expense(expenses, cards, vendors):

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
            'type': 'input',
            'name': 'new_card',
            'message': 'New card name?',
            'when': lambda answers: answers['update_card'] == True and answers['card'] == 'New Card',
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
            'name': 'new_vendor',
            'message': 'New vendor name?',
            'when': lambda answers: answers['update_vendor'] == True and answers['vendor'] == 'New Vendor',
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


# def delete_expense(expenses):

#     questions = [
#         {
#             'type': 'list',
#             'name': 'expense',
#             'message': 'What expense would you like to delete?',
#             'choices': expenses
#         },
#         {
#             'type': 'confirm',
#             'message': "Are you sure you want to delete this expense? THIS ACTION CAN'T BE UNDONE!",
#             'name': 'delete',
#             'default': False,
#         },
#     ]

#     answers = prompt(questions)

#     return answers


def delete_expenses(expenses):

    choices = []

    for expense in expenses:
        choices.append({'name': expense})

    questions = [
        {
            'type': 'checkbox',
            'message': 'What expense(s) would you like deleted?',
            'name': 'expenses',
            'choices': choices,
        },
        {
            'type': 'confirm',
            'message': "Are you sure you want to delete the selected expense(s)? THIS ACTION CAN'T BE UNDONE!",
            'name': 'delete',
            'default': False,
        },
    ]

    answers = prompt(questions)

    return answers


def mark_expense_submitted(expenses):

    choices = []

    for expense in expenses:
        choices.append({'name': expense})

    questions = [
        {
            'type': 'checkbox',
            'message': 'What expense(s) would you like mark as submitted?',
            'name': 'expenses',
            'choices': choices,
        },
        # {
        #     'type': 'confirm',
        #     'message': "Are you sure you want to mark expense(s) as submitted?",
        #     'name': 'mark',
        #     'default': False,
        # }
    ]

    answers = prompt(questions)

    if len(answers['expenses']) < 1:
        return False
    else:
        return answers


def mark_expense_unsubmitted(expenses):

    choices = []

    for expense in expenses:
        choices.append({'name': expense})

    questions = [
        {
            'type': 'checkbox',
            'message': 'What expense(s) would you like mark as unsubmitted?',
            'name': 'expenses',
            'choices': choices,
        },
        # {
        #     'type': 'confirm',
        #     'message': "Are you sure you want to mark expense(s) as unsubmitted?",
        #     'name': 'mark',
        #     'default': False,
        # }
    ]

    answers = prompt(questions)

    if len(answers['expenses']) < 1:
        return False
    else:
        return answers


def cont_program():
    questions = [
        {
            'type': 'confirm',
            'message': "Would you like to continue using the program?",
            'name': 'cont',
            'default': True,
        },
    ]

    answers = prompt(questions)

    if answers['cont']:
        return True

    return False
