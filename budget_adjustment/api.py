import frappe
from frappe import _ 
import erpnext


@frappe.whitelist()
def get_budget_child_accounts(budget): 

    try:
         doc = frappe.get_doc('Budget', budget)
       
    except Exception as e: 
        doc = None
        frappe.throw(_('Budget Does not exist'))

    return doc

