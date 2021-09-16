let budget_name,bal_account,adjust_amount,all_bal,account_for_link,used_amount;
frappe.ui.form.on('Budget Adjustment Of Accounts', {

    onload: function(frm) {
        // cur_frm.add_fetch('customer', 'local_tax_no', 'local_tax_no');

		frm.set_query("account_group", function() {
			return {
				filters: {
					company: frm.doc.company,
					report_type: "Profit and Loss",
					is_group: 1
				}
			};
		});

			frm.set_query("account_to_adjust", "budget_adjustment", function() {
				return {
                    query: "budget_adjustment.controllers.queries.get_account_to_adjust",
                    filters: {
                        "company": frm.doc.company,
                        "account_grp": frm.doc.account_group
                    }
                }
			});

    },

    account_group: function (frm){
        frm.refresh_field('budget_adjustment');
        frm.clear_table("budget_adjustment");

        if(frm.doc){
            var ac_g = frm.doc;
                  frappe.call({
                            type: "GET",
                            method: "budget_adjustment.budget_bal.get_budget_account_to",
                            args:{
					                company: frm.doc.company,
                                    account_grp: frm.doc.account_group
                            },
                            async:false,
                               callback: function(r) {
                                   var ds = r.message;
                                   console.log(ds)

                                   ds.forEach(function(d) {
                                        frappe.call({
                                            type: "GET",
                                            method: "budget_adjustment.budget_bal.get_actual_b",
                                            args:{"account": d.name },
                                            async:false,
                                            callback: function(r) {
                                                if(r.message === undefined){
                                                   used_amount = 0;
                                                }else{
                                                        used_amount = r.message;
                                                }

                                                console.log(adjust_amount);
                                                var adjusted_amount = 0
                                                    frm.add_child('budget_adjustment', {
                                                        account: d.name,
                                                        opening_budget: d.budget_amount,
                                                        adjustable_amount: used_amount,
                                                        adjusted_amount: adjusted_amount,
                                                        closing_balance: (d.budget_amount - (used_amount + adjusted_amount))
                                                    });

                                                }
                                    });

                                       });

                                    }


                    });
 frm.refresh_field('budget_adjustment');

        }
       },

    });
frappe.ui.form.on('Budget Adjustment Account Items', {
    adjusted_amount: function (frm,cdt,cdn){
        var items = locals[cdt][cdn]
        var adjustable_amt = items.opening_budget - items.adjustable_amount;
        if(items.adjusted_amount <= adjustable_amt) {
            var closing_balance = items.opening_budget - (items.adjustable_amount + items.adjusted_amount);
            frappe.model.set_value(items.doctype, items.name, "closing_balance", closing_balance);
        }else{

            frappe.msgprint({
                title: __('Error'),
                indicator: 'red',
                message: __('The amount to adjust cannot be more than the free balance available')
            });
            frappe.model.set_value(items.doctype, items.name, "adjusted_amount", 0);
        }

    },
})



