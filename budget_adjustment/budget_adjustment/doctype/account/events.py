import frappe
import json
from frappe import _
import erpnext 

def before_submit(self,method):
        add_account_num(self)


def validate(self, method):
    add_account_num(self)

def on_update(self, method):
    add_account_num(self)
    self.reload()




def add_account_num(self):
    if (self.n1 and self.n2 and self.n3):
        account_num = self.n1 + ""+self.n2+""+self.n3
        frappe.db.set_value(self.doctype, self.name, "account_number", account_num, update_modified=False)
        frappe.publish_realtime("account_number", {"doctype": "Account"})

        



