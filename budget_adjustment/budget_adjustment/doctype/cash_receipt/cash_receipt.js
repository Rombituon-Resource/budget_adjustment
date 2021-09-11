// Copyright (c) 2021, Chris and contributors
// For license information, please see license.txt
let totals = 0;
frappe.ui.form.on('Cash Receipt', {
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


			frm.set_query("received_account", "cash_receipts", function() {
				return {
                    query: "budget_adjustment.controllers.queries.get_accounts_child",
                    filters: {
                        "company": frm.doc.company,
                        "account": frm.doc.account_group
                    }
                }
			});
        },



});
frappe.ui.form.on('Cash Receipt Item', {

	amount_received: function(frm,cdt,cdn){
		var items = locals[cdt][cdn];
		totals += items.amount_received;
		frm.set_value("total", totals);


	}
});