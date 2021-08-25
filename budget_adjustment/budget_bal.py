# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

import frappe
from frappe import _
from frappe.utils import flt, formatdate
import json


# Get actual details from gl entry
@frappe.whitelist()
def get_actual_b(account):
    gl_balance = frappe.db.sql(
        ''' 
         select  sum(debit) - sum(credit) As balance from `tabGL Entry` where account=%s

        ''', account)

    if gl_balance:
        bal = gl_balance[0][0]

    else:
        bal = 0

    return bal


@frappe.whitelist()
def get_accounts_based_on_group(company, account):
    accounts = frappe.db.sql("""select tabAccount.name as name from `tabAccount`
			    where (tabAccount.report_type = "Profit and Loss"
					or tabAccount.account_type in ("Income Account","Expense Account", "Fixed Asset", "Temporary", "Asset Received But Not Billed", "Capital Work in Progress"))
				    and tabAccount.is_group=0
				    and tabAccount.docstatus!=2
				    and tabAccount.parent_account=%(account)s
				    and tabAccount.company = %(company)s
				    order by idx desc, name""", {'company': company, 'account': account}, as_dict=1)

    return accounts


@frappe.whitelist()
def get_budget_accounts_amount(company, account):
    accounts = frappe.db.sql(
        """
        select 
        tabAccount.name as name,
        ba.budget_amount 
         from
          `tabAccount`,
          `tabBudget Account` ba,
		  `tabBudget` b
		 where
			 (tabAccount.report_type = "Profit and Loss"
				or tabAccount.account_type in ("Income Account","Expense Account", "Fixed Asset", "Temporary", "Asset Received But Not Billed", "Capital Work in Progress"))
			and tabAccount.is_group=0
			and tabAccount.docstatus!=2
			and tabAccount.parent_account=%(account)s
			and tabAccount.company = %(company)s
			and ba.account=%(account)s
			order by name
		""", {'company': company, 'account': account}, as_dict=1)
    return accounts


@frappe.whitelist()
def get_budget_account_group_amount(company, account, account_grp):
    accounts = frappe.db.sql(
        """
            select 
                    tabAccount.name,
                    ba.budget_amount,
                    sum(gl.debit) as debit,
                    sum(gl.credit) as credit
                from 
                    `tabAccount`,
                    `tabBudget Account` ba, 
                    `tabBudget` b,
                    `tabGL Entry` gl 
                where 
                    (tabAccount.report_type = "Profit and Loss" 
                    or tabAccount.account_type in ("Income Account","Expense Account", "Fixed Asset", "Temporary", "Asset Received But Not Billed", "Capital Work in Progress")) 
                    and tabAccount.is_group=0 
                    and tabAccount.docstatus!=2 
                    and tabAccount.parent_account=%(account_grp)s 
                    and tabAccount.name=%(account)s
                    and tabAccount.company = %(company)s
                    and ba.account=%(account)s
                    and gl.account=%(account)s
                    and b.name = ba.parent 
                    and b.docstatus = 1
                    
		""", {'company': company, 'account': account, 'account_grp': account_grp}, as_dict=1)
    return accounts


@frappe.whitelist()
def get_budget_account_to(company, account_grp):
    accounts = frappe.db.sql("""
                                select distinct
                                     tabAccount.name,
                                     ba.budget_amount
                                from 
                                    `tabAccount`,
                                    `tabBudget` b, 
                                    `tabBudget Account` ba
                                where
                                 ba.account = tabAccount.name
                                 and b.name = ba.parent 
                                 and b.docstatus=1 
                                 and b.company=%(company)s
                                 and tabAccount.parent_account=%(account_grp)s 
                                 and tabAccount.company = %(company)s 
				            """, {'company': company, 'account_grp': account_grp}, as_dict=1)

    return accounts

