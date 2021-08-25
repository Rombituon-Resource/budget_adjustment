let budget_name,bal_account,adjust_amount,all_bal,account_for_link;
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

                                   ds.forEach(function(d) {
                                    console.log(d)

                                       frm.add_child('budget_adjustment', {
                                                   account: d.name,
                                                   opening_budget: d.budget_amount,
                                                   // adjustable_amount: adjust_amount,
                                                   // adjusted_amount: adjusted_amount,
                                                   // closing_balance: (b_account.budget_amount - (adjust_amount + adjusted_amount))
                                               });
                                       });

                                    }


                    });
 frm.refresh_field('budget_adjustment');

        }
       },

    budget:function (frm) {
        budget_name = frm.doc.budget;


        if (frm.doc.budget) {
             frm.clear_table("budget_adjustment");
             frm.refresh_field('budget_adjustment');

            frappe.call({
                type: "GET",
                method: "budget_adjustment.api.get_budget_child_accounts",
                args: {"budget": budget_name},
                callback: function (r) {
                    if (r.message.docstatus != 1) {
                        frappe.throw("The Budget Is Cancelled Budget cannot be Re-allocated");
                        frm.clear_table("budget_adjustment");
                        frm.refresh_field('budget_adjustment');
                        frm.refresh_field('budget');
                    }
                    else {

                    let b_accounts = r.message.accounts;
                    console.log(b_accounts);
                    b_accounts.forEach(b_account => {
                        frappe.call({
                            type: "GET",
                            method: "budget_adjustment.budget_bal.get_actual_b",
                            args:{"account": b_account.account },
                            async:false,
                               callback: function(r) {
                                   adjust_amount = r.message;
                                   var adjusted_amount = 0

                                    frm.add_child('budget_adjustment', {
                                        account: b_account.account,
                                        opening_budget: b_account.budget_amount,
                                        adjustable_amount: adjust_amount,
                                        adjusted_amount: adjusted_amount,
                                        closing_balance: (b_account.budget_amount - (adjust_amount + adjusted_amount))
                                    });

                                 }
                    });

                    })

                    frm.refresh_field('budget_adjustment');
                }
                }
            });


        } else {
            frm.clear_table("budget_adjustment");
            frm.refresh_field('budget_adjustment');

        }


        },


    });
frappe.ui.form.on('Budget Adjustment Account Items', {
    adjusted_amount: function (frm,cdt,cdn){
        var items = locals[cdt][cdn]
        var closing_balance = items.opening_budget - items.adjusted_amount;
        frappe.model.set_value(items.doctype,items.name,"closing_balance",closing_balance);

    },
})



