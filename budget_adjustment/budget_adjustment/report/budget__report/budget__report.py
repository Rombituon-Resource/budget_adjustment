# Copyright (c) 2013, Chris and contributors
# For license information, please see license.txt

import frappe
import re
from past.builtins import cmp
import functools
import math
from datetime import datetime
import frappe, erpnext
from erpnext.accounts.report.utils import get_currency, convert_to_presentation_currency
from erpnext.accounts.utils import get_fiscal_year
from frappe import _
from frappe.utils import (flt, getdate, get_first_day, add_months, add_days, formatdate, cstr, cint)

from budget_adjustment.budget_adjustment.report.utils import (filter_accounts, prepare_data, get_accounts,
                                                              prepare_budget_data)


def execute(filters=None):
    return get_columns(), get_data(filters)


def get_data(filters):
    fiscal_year = get_fiscal_year(filters.get('fiscal_year'))
    year_start_date = fiscal_year.get('year_start_date').strftime("%Y-%m-%d")
    year_end_date = fiscal_year.get('year_end_date').strftime("%Y-%m-%d")

    if not filters.get('budget'):
        accounts = get_accounts(filters.get('company'))
        filtered_accounts, accounts_by_name, parent_children_map = filter_accounts(accounts)

        if not accounts:
            return None
        data = prepare_data(accounts, filters, year_start_date, year_end_date, fiscal_year)

        return data
    else:

        data = prepare_budget_data(filters, year_start_date, year_end_date)

        return data


def get_columns():
    columns = [
        {
            'label': _('Account'),
            'fieldname': 'account',
            'fieldtype': 'Link',
            'options': 'Account',
            'width': 300
        },
        {
            'label': _('Allocated Amount'),
            'fieldname': 'allocated_amount',
            'fieldtype': 'Currency',
            'options': 'currency',
            'width': 200
        },
        {
            'label': _('Expenses'),
            'fieldname': 'expenses',
            'fieldtype': 'Currency',
            'options': 'currency',
            'width': 200
        },
        {
            'label': _('Available Amount'),
            'fieldname': 'available_amount',
            'fieldtype': 'Currency',
            'options': 'currency',
            'width': 200
        },
        {
            'label': _('Remarks'),
            'fieldname': 'remarks',
            'fieldtype': 'Text Editor',
            'width': 200
        }
    ]

    return columns
