let used_budget,free_balance,b_amount;
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

    setup(frm){

	    if (frm.doc.docstatus == 1){
	        console.log(frm.doc);

	        var ds =  frm.doc;

            ds.accounts.forEach(function(d) {
                b_amount = d.budget_amount;
                        frappe.call({
                            type: "GET",
                            method: "budget_adjustment.budget_bal.get_actual_b",
                            args:{"account": d.account },
                            async:false,
                               callback: function(r) {

                                   used_budget = r.message;
                                   free_balance = b_amount - used_budget;
                                   console.log(free_balance)
                                   let free_b = d.budget_amount - used_budget;
                                   console.log(free_b)
                                   frappe.db.set_value(d.doctype, d.name, "used_amount", used_budget);
                                     frappe.db.set_value(d.doctype, d.name, "free_balance", free_b);
                                     // frappe.db.set_value(d.doctype, d.name, "number_of_changes", 2);
                                     // frappe.db.set_value(d.doctype, d.name, "free_balance", free_balance);

                                 }
                    });

              });


        }
    },

}) //end frappe.ui.form.on

