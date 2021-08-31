# Copyright (c) 2021, Chris and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class BudgetAdjustmentOfAccounts(Document):

    @frappe.whitelist()
    def get_accounts_based_on_group(company, account):
        return frappe.db.sql("""select tabAccount.name from `tabAccount`
			    where (tabAccount.report_type = "Profit and Loss"
					or tabAccount.account_type in ("Income Account","Expense Account", "Fixed Asset", "Temporary", "Asset Received But Not Billed", "Capital Work in Progress"))
				    and tabAccount.is_group=0
				    and tabAccount.docstatus!=2
				    and tabAccount.parent_account=%(account)s
				    and tabAccount.company = %(company)s
				    order by idx desc, name""", {'company': company, 'account': account})

    def before_submit(self):
        for ba in self.budget_adjustment:
            account = ba.account
            opening_budget = ba.opening_budget
            adjustable_amount = ba.adjustable_amount
            adjusted_amount = ba.adjusted_amount
            closing_balance = ba.closing_balance
            account_to_adjust = ba.account_to_adjust

            if account_to_adjust and adjusted_amount != 0:

                new_budget_amount = opening_budget - adjusted_amount

                baccount = frappe.db.sql(
                     """
					select 
						name,
						number_of_changes
					from
						`tabBudget Account` 
					where 
						account = %(account)s
						and docstatus != 2
				""", {"account": account}, as_dict=1)
                num_of_changes = baccount[0].number_of_changes
                name = baccount[0].name

                frappe.db.set_value('Budget Account', name, {
                "number_of_changes": (num_of_changes + 1),
                "budget_amount": new_budget_amount
            }, update_modified=False)

                adjust_acc = frappe.db.sql(
                     """
                        select 
                            name,
                            number_of_changes,
                            budget_amount
                        from
                            `tabBudget Account` 
                        where 
                            account = %(account_to_adjust)s
                            and docstatus != 2
                    """, {"account_to_adjust": account_to_adjust}, as_dict=1)

                num_changes = adjust_acc[0].number_of_changes
                acc_name = adjust_acc[0].name
                budget_amt = adjust_acc[0].budget_amount
                new_bgt = budget_amt + adjusted_amount

                frappe.db.set_value('Budget Account', acc_name, {
                "number_of_changes": (num_changes + 1),
                "budget_amount": new_bgt
            }, update_modified=False)

            frappe.publish_realtime("number_of_changes", {"doctype": "Budget Account"})
