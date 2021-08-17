let budget_name;
frappe.ui.form.on('Budget Adjustment Voucher', {

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
                    let budget_against = r.message.budget_against;
                    // frappe.call({
                    //       type: "GET",
                    //     // method: "erpnext.accounts.report.budget_variance_report.get_actual_details",
                    //        method: "budget_adjustment.api.get_actual_det",
                    //         args:{
                    //             "name":budget_name,
                    //              "budget_against":budget_against
                    //          },
                    //            callback: function(r) {
                    //                console.log(r.message);
                    //
                    //
                    //              }
                    // })

                    b_accounts.forEach(b_account => {
                        frm.add_child('budget_adjustment', {
                            account: b_account.account,
                            opening_budget: b_account.budget_amount
                        })
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

    // refresh: function(frm){
    //    frm.clear_table("budget_adjustment");
    //    frm.refresh_field('budget_adjustment');
    // }



    });
    




