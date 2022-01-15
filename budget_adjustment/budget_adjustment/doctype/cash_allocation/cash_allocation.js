// Copyright (c) 2021, Chris and contributors
// For license information, please see license.txt
var received_amt,rec_amt,rem_amt;
frappe.ui.form.on('Cash Allocation', {
	refresh: function(frm) {
		if(frm.doc.docstatus == 1){

			frm.add_custom_button(__('Budget'), function(){
        	}, __("Create"));

			cur_frm.page.set_inner_btn_group_as_primary(__('Create'));
		}



	},
    	onload: function(frm) {

            frm.set_query("account_group", function() {
			    return {
				    filters: {
					    company: frm.doc.company,
					    report_type: "Profit and Loss",
					    is_group: 1
				    }
			    };
		    });

            frm.set_query("cost_center", function() {
			    return {
				    filters: {
					    company: frm.doc.company,
						 is_group: 0
				    }
			    };
		    });

            frm.set_query("budget", function() {
			    return {
				    filters: {
					    company: frm.doc.company,
						cost_center: frm.doc.cost_center,
						docstatus:1
				    }
			    };
		    });

			frm.set_query("received_account", "cash_allocation", function() {
				return {
                    query: "budget_adjustment.controllers.queries.get_cash_received_accounts",
                    filters: {
                        "company": frm.doc.company,
                        "account": frm.doc.account_group
                    }
                }
			});
        },
		budget:function(frm){

					frm.refresh_field('cash_allocation');
					frm.clear_table("cash_allocation");

			if(frm.doc.budget) {
				frappe.call({
					type: "GET",
					method: "budget_adjustment.api.get_budget_child_accounts",
					args: {"budget": frm.doc.budget},
					callback: function (r) {
						if (r.message.docstatus != 1) {
							frappe.throw("The Budget Is Cancelled Budget cannot be loaded");
							frm.clear_table("cash_allocation");
							frm.refresh_field('cash_allocation');
							frm.refresh_field('budget');
						} else {

							let b_accounts = r.message.accounts;
							b_accounts.forEach(b_account => {
								frm.add_child('cash_allocation', {
									received_account: b_account.account,
									previous_budget_amount: b_account.budget_amount

								});
							});
							frm.refresh_field('cash_allocation');


						}
					}
				});
			}else{
					frm.clear_table("cash_allocation");
					frm.refresh_field('cash_allocation');
			}

		},
	before_save: function(frm){
		var total = 0;
		$.each(frm.doc.cash_allocation || [], function(i, d) {
			total += flt(d.amount_received);
		});
		frm.set_value("total", total);

		if(frm.doc.total !== frm.doc.received_amount){
			frappe.throw("The Received Amount and the total allocated amount should be equal");
		}
	},
	received_amount(frm){
		received_amt = frm.doc.received_amount;
	},

	cash_allocation_add(doc, cdt, cdn) {
		doc.total = doc.received_amount;
		var row = frappe.get_doc(cdt, cdn);
		$.each(doc.cash_allocation, function(i, d) {
			if(d.received_account && d.previous_budget_amount) {
				row.received_account = d.received_account;
				row.previous_budget_amount = d.previous_budget_amount;

			}
		});
		// set difference
		if(doc.total) {
			if(doc.total > 0) {
				row.amount_received = doc.total;

			} else {
				row.amount_received = -doc.total;
			}
		}
		// cur_frm.cscript.update_totals(doc);

		erpnext.accounts.dimensions.copy_dimension_from_first_row(this.frm, cdt, cdn, 'cash_allocation');
	},

// 	cur_frm.cscript.update_totals = function(doc) {
// 		var td=0.0;
// 		var accounts = doc.cash_allocation || [];
// 		for(var i in accounts) {
// 			td += flt(accounts[i].amount_received, precision("amount_received", accounts[i]));
// 		}
// 		var doc = locals[doc.doctype][doc.name];
// 		doc.total = td;
// 		refresh_many(['amount_received','total']);
// }

});
frappe.ui.form.on('Cash Allocation Item', {
	// cash_allocation_add(frm,cdt,cdn){
	// 	console.log(received_amt);
	//
	// }

	// amount_received: function (frm,cdt,cdn){
	//
    //     var items = locals[cdt][cdn];
    //     items.amount_received = received_amt;
	//
	//
	//
	//
	// }

})