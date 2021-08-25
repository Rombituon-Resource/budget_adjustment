let budget_names,bal_accounts,adjust_amounts,all_bals;
frappe.ui.form.on('Budget Adjustment Voucher', {

    budget:function (frm) {
        budget_names = frm.doc.budget;


        if (frm.doc.budget) {
             frm.clear_table("budget_adjustment");
             frm.refresh_field('budget_adjustment');

            frappe.call({
                type: "GET",
                method: "budget_adjustment.api.get_budget_child_accounts",
                args: {"budget": budget_names},
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
                                   adjust_amounts = r.message;
                                   var adjusted_amounts = 0

                                    frm.add_child('budget_adjustment', {
                                        account: b_account.account,
                                        opening_budget: b_account.budget_amount,
                                        adjustable_amount: adjust_amounts,
                                        adjusted_amount: adjusted_amounts,
                                        closing_balance: (b_account.budget_amount - (adjust_amounts + adjusted_amounts))
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
    



