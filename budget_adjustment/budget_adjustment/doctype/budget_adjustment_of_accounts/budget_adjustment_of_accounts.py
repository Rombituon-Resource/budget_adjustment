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