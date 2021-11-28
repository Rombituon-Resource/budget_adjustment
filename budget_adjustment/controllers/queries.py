import frappe


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_accounts_child(doctype, txt, searchfield, start, page_len, filters):
    return frappe.db.sql("""select tabAccount.name from `tabAccount`
		    where (tabAccount.report_type = "Profit and Loss"
				or tabAccount.account_type in ("Income Account","Expense Account", "Fixed Asset", "Temporary", "Asset Received But Not Billed", "Capital Work in Progress"))
			    and tabAccount.is_group=0
			    and tabAccount.docstatus!=2
			    and tabAccount.parent_account=%(account)s
			    and tabAccount.company = %(company)s
			    order by idx desc, name""", {'company': filters.get("company"), 'account': filters.get("account")})


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_cash_received_accounts(doctype, txt, searchfield, start, page_len, filters):
    acc = frappe.db.sql(
        """select distinct a3.name from `tabAccount` a1
            INNER JOIN `tabAccount` a2 
                ON a1.name = a2.parent_account
            INNER JOIN `tabAccount` a3 
                ON (a1.name = a3.parent_account
                and a3.is_group = 0)     
		    where (a1.report_type = "Profit and Loss"
				or a1.account_type in ("Income Account","Expense Account", "Fixed Asset", "Temporary", "Asset Received But Not Billed", "Capital Work in Progress"))
			    and a1.docstatus!=2
			    and a1.parent_account=%(account)s
			    or a1.parent_account=%(account)s
			    and a1.company = %(company)s
			    """, {'company': filters.get("company"), 'account': filters.get("account")})
    return acc


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_account_to_adjust(doctype, txt, searchfield, start, page_len, filters):
    accounts = frappe.db.sql("""
                                select 
                                     tabAccount.name
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
				            """, {'company': filters.get("company"), 'account_grp': filters.get("account_grp")})

    return accounts


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_used_amount(doctype, txt, searchfield, start, page_len, filters):
    return frappe.db.sql(
        ''' 
                            select  COALESCE(sum(debit),0) - COALESCE(sum(credit),0) As balance from `tabGL Entry` where account=%s 

                        ''', {'account': filters.get("account")})
    return bal


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_budget_name(doctype, txt, searchfield, start, page_len, filters):
    budget_name = frappe.db.sql(
        """
            select 
                budget_name
            from `tabBudget` 
            where 
                docstatus=1 
                and company=%(company)s 
                and cost_center=%(cost_center)s
        """, {'company': filters.get("company"), 'cost_center': filters.get("cost_center")})
    #frappe.throw("{0}".format(budget_name))
    return budget_name
