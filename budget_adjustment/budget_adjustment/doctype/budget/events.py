import frappe
import json
from frappe import _
import erpnext


def on_change(self, method):
    for account in self.accounts:
        frappe.db.set_value(account.doctype, account.name, "used_amount", account.used_amount,
                            update_modified=False)
        frappe.db.set_value(account.doctype, account.name, "free_balance",
                            (account.budget_amount - account.used_amount),
                            update_modified=False)
    # frappe.publish_realtime("free_balance", {"doctype": "Budget "})
    #
    # frappe.clear_cache(doctype='Budget')
    # self.reload()
    self.clear_cache()


def onload(self, method):
    self.reload()
