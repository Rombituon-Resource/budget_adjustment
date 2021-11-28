# Copyright (c) 2013, Chris and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

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

from six import itervalues
from erpnext.accounts.doctype.accounting_dimension.accounting_dimension import get_accounting_dimensions, \
    get_dimension_with_children


def get_accounts(company):
    return frappe.db.sql("""
    		 				select ta.name,tb.account,tb.budget_amount, ta.account_number, ta.parent_account, ta.lft, ta.rgt, ta.root_type, ta.report_type, ta.account_name, ta.include_in_gross, ta.account_type, ta.is_group, ta.lft, ta.rgt from `tabAccount` ta, `tabBudget Account` tb where ta.name = tb.account  and ta.company=%s  and ta.root_type='Expense' order by lft
						""", (company), as_dict=True)


def get_expenses(account, year_start_date, year_end_date):
    accounts = frappe.db.sql(
        ''' 
                            select  COALESCE(sum(debit),0) - COALESCE(sum(credit),0) As balance from `tabGL Entry`
                             where account=%s and posting_date >= %s and posting_date <= %s and is_cancelled = 0

                        ''', (account, year_start_date, year_end_date), as_dict=1)

    if accounts:
        return accounts[0].balance
    else:
        return []


def filter_accounts(accounts, depth=20):
    parent_children_map = {}
    accounts_by_name = {}
    for d in accounts:
        accounts_by_name[d.name] = d
        parent_children_map.setdefault(d.parent_account or None, []).append(d)

    filtered_accounts = []

    def add_to_list(parent, level):
        if level < depth:
            children = parent_children_map.get(parent) or []
            sort_accounts(children, is_root=True if parent == None else False)

            for child in children:
                child.indent = level
                filtered_accounts.append(child)
                add_to_list(child.name, level + 1)

    add_to_list(None, 0)

    return filtered_accounts, accounts_by_name, parent_children_map


def sort_accounts(accounts, is_root=False, key="name"):
    """Sort root types as Asset, Liability, Equity, Income, Expense"""

    def compare_accounts(a, b):
        if re.split('\W+', a[key])[0].isdigit():
            # if chart of accounts is numbered, then sort by number
            return cmp(a[key], b[key])
        elif is_root:
            if a.report_type != b.report_type and a.report_type == "Balance Sheet":
                return -1
            if a.root_type != b.root_type and a.root_type == "Asset":
                return -1
            if a.root_type == "Liability" and b.root_type == "Equity":
                return -1
            if a.root_type == "Income" and b.root_type == "Expense":
                return -1
        else:
            # sort by key (number) or name
            return cmp(a[key], b[key])
        return 1

    accounts.sort(key=functools.cmp_to_key(compare_accounts))


def prepare_data(accounts, filters, year_start_date, year_end_date, fiscal_year):
    data = []

    parents = get_accounts_parents(filters.get('company'))
    for parent in parents:
        has_value = False
        total = 0
        acc = parent.parent_account
        expenses = get_expenses_parents(filters.get('company'), acc, year_start_date, year_end_date)
        budget = get_budget_parents(filters.get('company'), acc, fiscal_year.name)

        row = frappe._dict({
            "account": _(parent.parent_account),
            "account_name": _(parent.parent_account),
            "indent": 0,
            "allocated_amount": _(budget),
            "expenses": _(expenses),
            "available_amount": _(budget - expenses),
            "has_value": True
        })

        data.append(row)

        children = get_accounts_children(filters.get('company'), parent.parent_account)
        for child in children:
            has_value = False
            total = 0
            row = frappe._dict({
                "account": _(child.name),
                "indent": 1,
                "allocated_amount": child.budget_amount,
                "account_name": _(child.account_name),
                "expenses": _(get_expenses(child.name, year_start_date, year_end_date)),
                "available_amount": _(child.budget_amount - get_expenses(child.name, year_start_date, year_end_date)),
                "has_value": True,
                "remarks": _(get_remarks(child.name))
            })

            data.append(row)

    return data


def get_expenses_parents(company, parent, year_start_date, year_end_date):
    totals = 0
    children = get_accounts_children(company, parent)
    for child in children:
        accounts = frappe.db.sql(
            ''' 
                            select  COALESCE(sum(debit),0) - COALESCE(sum(credit),0) As balance from `tabGL Entry`
                             where account=%s and posting_date >= %s and posting_date <= %s and is_cancelled = 0

                        ''', (child.name, year_start_date, year_end_date), as_dict=1)
        if accounts:
            totals += accounts[0].balance
        else:
            totals += 0

    return totals


def get_accounts_parents(company):
    return frappe.db.sql("""
        		 			  select ta.parent_account from `tabAccount` ta, `tabBudget Account` tb where ta.name = tb.account and ta.company=%s and ta.root_type="Expense" group by ta.parent_account
                         """, (company), as_dict=True)


def get_accounts_children(company, parent):
    return frappe.db.sql("""
    		 				select ta.name,tb.account,tb.budget_amount, ta.account_number, ta.parent_account, ta.lft, ta.rgt, ta.root_type, ta.report_type, ta.account_name, ta.include_in_gross, ta.account_type, ta.is_group, ta.lft, ta.rgt from `tabAccount` ta, `tabBudget Account` tb where ta.name = tb.account  and ta.company=%s  and ta.root_type='Expense' and ta.parent_account=%s order by lft
						""", (company, parent), as_dict=True)


def get_budget_parents(company, parent, fiscal_year):
    totals = 0
    children = get_accounts_children(company, parent)
    for child in children:
        accounts = frappe.db.sql(
            '''

                select ba.budget_amount,b.fiscal_year from `tabBudget Account` ba, `tabBudget` b 
                    where ba.parent = b.name and b.fiscal_year=%s and ba.account=%s;
            ''', (fiscal_year, child.name), as_dict=1)
        if accounts:
            totals += accounts[0].budget_amount
        else:
            totals += 0

    return totals


def get_remarks(account):
    remarks = frappe.db.sql("""

                            select tb.reason_for_adjustment from `tabBudget Adjustment Account Items` tb 
                                where tb.account =%s  order by creation desc limit 1;


                         """, account, as_dict=True)
    if remarks:
        return remarks[0].reason_for_adjustment
    else:
        return ""


def get_budget_accounts(budget):
    budget_accounts = frappe.db.sql("""
                                     select account,budget_amount 
                                        from `tabBudget Account` 
                                            where 
                                            parent=%s;
    
                                    """, budget, as_dict=True)

    return budget_accounts


def prepare_budget_data(filters, year_start_date, year_end_date):
    data = []

    budget_accounts = get_budget_accounts(filters.get('budget'))
    for budget_account in budget_accounts:
        row = frappe._dict({
            "account": _(budget_account.account),
            "indent": 1,
            "allocated_amount": budget_account.budget_amount,
            "account_name": _(budget_account.account),
            "expenses": _(get_expenses(budget_account.account, year_start_date, year_end_date)),
            "available_amount": _(
                budget_account.budget_amount - get_expenses(budget_account.account, year_start_date, year_end_date)),
            "has_value": True,
            "remarks": _(get_remarks(budget_account.account))
        })

        data.append(row)

    return data


def get_account_budget(accounts, filters, year_start_date, year_end_date, fiscal_year):
    data = []
    parents = get_accounts_parents(filters.get('company'))
    for parent in parents:
        acc = parent.parent_account

        children = get_accounts_children(filters.get('company'), parent.parent_account)
        for child in children:
            has_value = False
            total = 0
            row = frappe._dict({
                "account": _(child.name),
                "indent": 1,
                "allocated_amount": child.budget_amount,
                "account_name": _(child.account_name),
                "expenses": _(get_expenses(child.name, year_start_date, year_end_date)),
                "available_amount": _(child.budget_amount - get_expenses(child.name, year_start_date, year_end_date)),
                "has_value": True,
                "remarks": _(get_remarks(child.name))
            })

            data.append(row)

    return data
