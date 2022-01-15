// Copyright (c) 2016, Chris and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Budget  Report"] = {
	"filters": [
		{
			"fieldname":"from_fiscal_year",
			"label": __("Fiscal Year"),
			"fieldtype": "Link",
			"options": "Fiscal Year",
			"reqd": 1,
			"default": frappe.sys_defaults.fiscal_year
		},
		{
			"fieldname": "company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"reqd":1,
			"default":frappe.defaults.get_user_default("Company")
		},
		{
			"fieldname": "budget",
			"label": __("Budget"),
			"fieldtype": "Link",
			"options": "Budget"
			//  get_data: function(txt) {
			// 	return frappe.db.get_list('Budget', txt, {
			// 		company: frappe.query_report.get_filter_value("company")
			// 	});
			// }
			// "get_query" : function(){
			// 	var company = frappe.query_report_filters_by_name.company.get_value();
			// 	return{
			// 		"doctype": "Budget",
			// 		"filters":{
			// 			"company":company,
			// 		}
			// 	}
			// }

		},

	],
	"formatter": function(value, row, column, data, default_formatter) {
		if (data && column.fieldname=="account") {
			value = data.account_name || value;
			column.is_tree = true;
		}

		value = default_formatter(value, row, column, data);

		if (data && !data.parent_account) {
			value = $(`<span>${value}</span>`);

			var $value = $(value).css("font-weight", "bold");
			if (data.warn_if_negative && data[column.fieldname] < 0) {
				$value.addClass("text-danger");
			}

			value = $value.wrap("<p></p>").parent().html();
		}

		return value;
	},
    "tree": true,
    "name_field": "account",
    "parent_field": "parent_account",
    "initial_depth": 2

};
