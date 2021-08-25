# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

import frappe
from frappe import _
from frappe.utils import flt, formatdate
import frappe
import erpnext
import json
from frappe.desk.reportview import get_match_cond, get_filters_cond
from frappe.utils import nowdate, getdate
from collections import defaultdict


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def populate_budget(account, doctype, name):
    # free_balance,budget_amount = 0
    return frappe.db.get_value(doctype, name, "budget_amount")

    # frappe.db.set_value(doctype, name, {
    #     used_amount: bal,
    #     free_balance:
    # }).then(r= > {
    #     let
    # doc = r.message;
    # console.log(doc);
    # })
    #
    #
    # frappe.db.set_value(doctype, name, "used_amount");
    # frappe.db.set_value(doctype, name, "free_balance");

    # return (budget_amount)
