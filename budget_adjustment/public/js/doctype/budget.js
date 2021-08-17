frappe.ui.form.on('Budget', {

	refresh(frm) {
        // your code here

        if (frm.doc.docstatus == 1) {

            frm.add_custom_button(__("Budget Adjustement Voucher"), function () {
                 // When this button is clicked, do this
                //    frm.get_budget_child_accounts()
                frappe.set_route("Form", "Budget Adjustment Voucher", {"budget": frm.doc.name});

            });
        }
        
    
    }, //end refresh



}) //end frappe.ui.form.on

