	frappe.ready(function() {
		// Bind custom validation to the form
		$('form').on('submit', function(e) {
			e.preventDefault(); // Prevent default form submission
			validateForm();
		});
	
		function validateForm() {
			let member = $('[name="member"]').val();
			let article = $('[name="article"]').val();
			let type = $('[name="type"]').val();
			let date = $('[name="date"]').val();
			let action = $('[name="action"]').val();
			let quantity = $('[name="quantity"]').val();
	
			// Validate membership
			frappe.call({
				method: 'frappe.client.get_value',
				args: {
					doctype: 'Library Membership',
					filters: {
						member: member,
						docstatus: 1,
						from_date: ['<', date],
						to_date: ['>', date]
					},
					fieldname: 'name'
				},
				callback: function(response) {
					if (!response.message) {
						frappe.msgprint('The member does not have a valid membership');
						return;
					}
					validateIssue(article, type, action, quantity);
				}
			});
		}
	
		function validateIssue(article, type, action, quantity) {
			frappe.call({
				method: 'frappe.client.get',
				args: {
					doctype: 'Article',
					name: article
				},
				callback: function(response) {
					let articleDoc = response.message;
					if (type == "Issue") {
						if (articleDoc.status == "Issued") {
							frappe.msgprint('Article is already issued by another member');
							return;
						}
						validateMaximumLimit(article, type, action, quantity);
					} else if (type == "Return") {
						if (articleDoc.status == "Available") {
							frappe.msgprint('Article cannot be returned without being issued first');
							return;
						}
						submitForm();
					}
				}
			});
		}
	
		function validateMaximumLimit(article, type, action, quantity) {
			frappe.call({
				method: 'frappe.client.get_single_value',
				args: {
					doctype: 'Library Settings',
					field: 'max_articles'
				},
				callback: function(response) {
					let max_articles = response.message;
					frappe.call({
						method: 'frappe.client.count',
						args: {
							doctype: 'Article Issue',
							filters: {
								member: $('[name="member"]').val(),
								type: 'Issue',
								docstatus: 1
							}
						},
						callback: function(response) {
							let count = response.message;
							if (count >= max_articles) {
								frappe.msgprint('Maximum limit reached for issuing articles');
								return;
							}
							validateStock(article, action, quantity);
						}
					});
				}
			});
		}
	
		function validateStock(article, action, quantity) {
			frappe.call({
				method: 'frappe.client.get',
				args: {
					doctype: 'Article Management',
					name: article
				},
				callback: function(response) {
					let articleManagement = response.message;
					if (action == "Lend.") {
						if (articleManagement.quantity_available < quantity) {
							frappe.msgprint(`Out Of Stock. Only ${articleManagement.quantity_available} articles available in the library`);
							return;
						}
					} else if (action == "Return.") {
						if (articleManagement.quantity_available == 0) {
							frappe.msgprint("Article has been Restocked Now.");
						}
					}
					submitForm();
				}
			});
		}
	
		function submitForm() {
			// Submit the form after validation
			$('form')[0].submit();
		}
	});

	frappe.ready(function() {
		// Bind custom validation to the form
		$('form').on('submit', function(e) {
			e.preventDefault(); // Prevent default form submission
			validateForm();
		});
	
		function validateForm() {
			calculate_overdue_period();
		}
	
		function calculate_overdue_period() {
			let issue_date = new Date($('[name="issue_date"]').val());
			let due_date = new Date($('[name="due_date"]').val());
			let current_date = new Date();
			let is_returned = $('[name="is_returned"]').is(':checked');
	
			// Set time part to zero for accurate date comparison
			issue_date.setHours(0, 0, 0, 0);
			due_date.setHours(0, 0, 0, 0);
			current_date.setHours(0, 0, 0, 0);
	
			if (is_returned) {
				$('[name="overdue_period"]').val(0);
				$('[name="status"]').val('Returned');
			} else if (current_date > due_date) {
				let overdue_period = Math.ceil((current_date - due_date) / (1000 * 60 * 60 * 24));
				$('[name="overdue_period"]').val(overdue_period);
				$('[name="status"]').val('Overdue');
			} else {
				$('[name="overdue_period"]').val(0);
				$('[name="status"]').val('Issued');
			}
	
			// After validation, submit the form
			$('form')[0].submit();
		}
	
		$('[name="is_returned"]').on('change', function() {
			handle_checkbox_change();
		});
	
		function handle_checkbox_change() {
			if ($('[name="is_returned"]').is(':checked')) {
				$('[name="status"]').val('Returned');
				$('[name="overdue_period"]').val(0);
			}
		}
	
		function initialize_datepicker(field_name) {
			let today = new Date();
			today.setHours(0, 0, 0, 0); // Ensure the time part is zero for accurate comparison
	
			$(field_name).datepicker({
				dateFormat: 'dd-mm-yyyy',
				minDate: today,
				beforeShowDay: function(date) {
					if (date < today) {
						return [false, 'ui-datepicker-unselectable ui-state-disabled', ''];
					} else {
						return [true, '', ''];
					}
				}
			});
		}
	
		// Initialize date pickers
		initialize_datepicker('[name="issue_date"]');
		initialize_datepicker('[name="due_date"]');
	});
	