let used_budget,free_balance,b_amount;
frappe.ui.form.on('Budget', {

    onload(frm){

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
                                    if(r.message === undefined){
                                       used_budget = 0;
                                    }else{
                                        used_budget = r.message;
                                    }
                                   free_balance = b_amount - used_budget;
                                   frappe.model.set_value(d.doctype, d.name, "used_amount", used_budget);
                                   frappe.model.set_value(d.doctype, d.name, "free_balance", free_balance);

                                 }
                    });

              });
            frm.dirty();
            frm.save();


        }
    },

}) //end frappe.ui.form.on

