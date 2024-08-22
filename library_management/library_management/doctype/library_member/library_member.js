// Copyright (c) 2024, ateeq and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Library Member", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on('Library Member', {
    refresh: function(frm) {
        // Adding a custom button for creating a membership
        frm.add_custom_button('Create Membership', function() {
            frappe.new_doc('Library Membership', {
                library_member: frm.doc.name
            });
        });
        // Adding a custom button for creating a transaction
        frm.add_custom_button('Create Transaction', function() {
            frappe.new_doc('Library Transaction', {
                library_member: frm.doc.name
            });
        });
    }
});
