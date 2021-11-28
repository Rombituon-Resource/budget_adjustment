from __future__ import unicode_literals
import frappe
import erpnext
from frappe import _
from erpnext.accounts.doctype.budget.budget import Budget
from erpnext.accounts.doctype.budget.budget import *


class CustomBudget(Budget):

    def autoname(self):
        self.name = self.budget_name
