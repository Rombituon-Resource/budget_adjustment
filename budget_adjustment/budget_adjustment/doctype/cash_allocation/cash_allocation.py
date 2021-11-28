# Copyright (c) 2021, Chris and contributors
# For license information, please see license.txt

import frappe
import json
from frappe.model.document import Document


class CashAllocation(Document):
	def before_save(self):
		budget = self.budget
		for cr in self.cash_allocation:

			account = cr.received_account
			amount_received = cr.amount_received

			if frappe.db.exists({'doctype': 'Budget Account', 'account': cr.received_account}):
				adjust_acc = frappe.db.sql(
					"""
                                select 
                                    name,
                                    number_of_changes,
                                    budget_amount
                                from
                                    `tabBudget Account` 
                                where 
                                    account = %(account)s
                                    and docstatus != 2
                            """, {"account": account}, as_dict=1)

				num_changes = adjust_acc[0].number_of_changes
				acc_name = adjust_acc[0].name
				budget_amt = adjust_acc[0].budget_amount
				new_bgt = budget_amt + amount_received

				frappe.db.set_value('Budget Account', acc_name, {
					"number_of_changes": (num_changes + 1),
					"budget_amount": new_bgt
				}, update_modified=False)

				frappe.publish_realtime("number_of_changes", {"doctype": "Budget Account"})
			else:
				ba = frappe.get_last_doc('Budget Account', filters={"parent": budget}, order_by="idx desc")
				budget_acc = frappe.new_doc("Budget Account")
				budget_acc.parent = budget
				budget_acc.idx = ba.idx + 1
				budget_acc.account = cr.received_account
				budget_acc.budget_amount = cr.amount_received
				budget_acc.number_of_changes = 0
				budget_acc.used_amount = 0
				budget_acc.free_balance = cr.amount_received
				budget_acc.parentfield = "accounts"
				budget_acc.parenttype = "Budget"
				budget_acc.save()
