# Copyright (c) 2024, ateeq and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class ArticleManagement(Document):
	pass


'''import frappe
from frappe.model.document import Document

class ArticleIssue(Document):
    pass

@frappe.whitelist()
def lend_article(article, quantity):
    article_doc = frappe.get_doc("Article Management", article)
    print(f"Lending Article: {article}, Quantity: {quantity}")
    print(f"Current Quantity Available: {article_doc.quantity_available}")
    if article_doc.quantity_available < int(quantity):
        frappe.throw("Not enough articles available to lend.")
    article_doc.quantity_available = article_doc.quantity_available - int(quantity)
    article_doc.save()
    print(f"New Quantity Available: {article_doc.quantity_available}")
    return f"Article lent successfully. {int(quantity)} articles updated."

@frappe.whitelist()
def return_article(article, quantity):
    article_doc = frappe.get_doc("Article Management", article)
    print(f"Returning Article: {article}, Quantity: {quantity}")
    print(f"Current Quantity Available: {article_doc.quantity_available}")
    article_doc.quantity_available = article_doc.quantity_available + int(quantity)
    article_doc.save()
    print(f"New Quantity Available: {article_doc.quantity_available}")
    return f"Article returned successfully. {int(quantity)} articles updated."'''
def after_save(self, method):
    # try:
        # Fetch the Library Management document
        library_management = frappe.get_doc("Library Management", self.library)

        # Check if the action is "Issue"
        if self.action == "Issue":
            # If quantity available is 0, prevent issuing
            if library_management.quantity_available == 0:
                frappe.throw("Cannot issue article. Quantity available is 0.")

        # Check if the action is "Return"
        elif self.action == "Return":
            # Allow returning articles regardless of quantity available

            # Optional: You may want to add a check if quantity_available was already 0 and log a message
            if library_management.quantity_available == 0:
                frappe.msgprint("Warning: Quantity available is already 0.")

