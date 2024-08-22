# library_management/tasks/tasks.py

import frappe
from frappe.utils import today, add_days

def check_overdue_articles():
    # Fetch overdue period from library settings
    library_settings = frappe.get_single('Library Settings')
    overdue_period = library_settings.overdue_period

    # Fetch all issued articles that are not yet returned
    issued_articles = frappe.get_all('Article Issue', filters={'status': 'Issued'})

    if not issued_articles:
        frappe.log_error("No issued articles found.")
        return

    frappe.log_error(f"Found {len(issued_articles)} issued articles to check for overdue.")

    for article in issued_articles:
        article_doc = frappe.get_doc('Article Issue', article.name)
        
        # Calculate overdue date
        overdue_date = add_days(article_doc.due_date, overdue_period)

        # Check if the overdue date has passed
        if article_doc.due_date and overdue_date < today():
            frappe.log_error(f"Article {article_doc.name} is overdue. Updating status.")
            # Update the status to 'Not Returned' and 'Overdue'
            article_doc.status = 'Not Returned'
            article_doc.overdue = 1
            article_doc.save()
            frappe.log_error(f"Article {article_doc.name} status updated to Not Returned and Overdue.")

            # Optionally, you can also update the member status or any other related data
            member_doc = frappe.get_doc('Library Member', article_doc.member)
            member_doc.has_overdue = 1
            member_doc.save()
            frappe.log_error(f"Member {member_doc.name} marked as having overdue articles.")
        else:
            frappe.log_error(f"Article {article_doc.name} is not overdue. Due date: {article_doc.due_date}, Today: {today()}.")
