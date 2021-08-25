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
			    order by idx desc, name""",{ 'company': filters.get("company"), 'account': filters.get("account")})



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
				            """, { 'company': filters.get("company"), 'account_grp': filters.get("account_grp")})

    return accounts


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_used_amount(doctype, txt, searchfield, start, page_len, filters):
    return frappe.db.sql(
                         ''' 
                            select  COALESCE(sum(debit),0) - COALESCE(sum(credit),0) As balance from `tabGL Entry` where account=%s 

                        ''', {'account': filters.get("account")})
    return bal