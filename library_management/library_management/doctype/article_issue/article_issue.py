# Copyright (c) 2024, ateeq and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.docstatus import DocStatus


class ArticleIssue (Document):
    def before_submit(self):
        if self.type == "Issue":
            self.validate_issue()
            self.validate_maximum_limit()
            # set the article status to be Issued
            article = frappe.get_doc("Article", self.article)
            article.status = "Issued"
            article.save()

        elif self.type == "Return":
            self.validate_return()
            # set the article status to be Available
            article = frappe.get_doc("Article", self.article)
            article.status = "Available"
            article.save()

    def validate_issue(self):
        self.validate_membership()
        article = frappe.get_doc("Article", self.article)
        # article cannot be issued if it is already issued
        if article.status == "Issued":
            frappe.throw("Article is already issued by another member")

    def validate_return(self):
        article = frappe.get_doc("Article", self.article)
        # article cannot be returned if it is not issued first
        if article.status == "Available":
            frappe.throw("Article cannot be returned without being issued first")

    def validate_maximum_limit(self):
        max_articles = frappe.db.get_single_value("Library Settings", "max_articles")
        count = frappe.db.count(
            "Article Issue",
            {"member": self.member, "type": "Issue", "docstatus": DocStatus.submitted()},
        )
        
        if count >= max_articles:
            frappe.throw("Maximum limit reached for issuing articles")

    def validate_membership(self):
        # check if a valid membership exist for this library member
        valid_membership = frappe.db.exists(
            "Library Membership",
            {
                "member": self.member,
                "docstatus": DocStatus.submitted(),
                "from_date": ("<", self.date),
                "to_date": (">", self.date),
            },
        )
        if not valid_membership:
            frappe.throw("The member does not have a valid membership")


import frappe
from frappe.utils import getdate, nowdate
from frappe.model.document import Document

class ArticleIssue(Document):
    def validate(self):
        self.validate_membership()
        # self.validate_issue_date()

    def validate_membership(self):
        if not self.valid_membership():
            frappe.throw("The member does not have a valid membership")

    # def validate_issue_date(self):
    #     if getdate(self.issue_date) < getdate(nowdate()):
    #         frappe.throw("You cannot select a date before today.")


    def valid_membership(self):
        # Your logic to validate membership
        return True

    def validate_issue(self):
        # Your logic to validate the issue process
        pass


    # def before_save(self):
    #     article_management = frappe.get_doc("Article Management", self.article)
    #     validate_issue(self)
        
    #     # Decrement the count of available articles when issuing
    #     if self.action == "Lend.":
    #         article_management.quantity_available -= self.quantity
    #         article_management.save()
    #         validate(self)
    #         frappe.msgprint(f"{self.quantity} Article issued from the Library for {article_management.name}")

    #     # Increment the count of available articles when returning
    #     elif self.action == "Return.":
    #         article_management.quantity_available += self.quantity
    #         article_management.save()
    #         self.status = "Returned"  # Set the status field to "Returned"
    #         validate(self)
    #         frappe.msgprint(f"{self.quantity} Article returned to the Library for {article_management.name}")
    # def on_update(self):
    #     # Ensure the status is updated when returning an article
    #     if self.action == "Return.":
    #         self.status = "Returned"
    #         frappe.msgprint(f"Status updated to 'Returned' for {self.name}")
    def before_save(self):
        article_management = frappe.get_doc("Article Management", self.article)
        validate_issue(self)
        
        # Decrement the count of available articles when issuing
        if self.action == "Lend.":
            if self.status == "Returned":
                frappe.throw("An article once returned cannot be issued again So Please assign Again a new Document.")
            article_management.quantity_available -= self.quantity
            article_management.save()
            validate(self)
            frappe.msgprint(f"{self.quantity} Article issued from the Library for {article_management.name}")

        # Increment the count of available articles when returning
        elif self.action == "Return.":
            article_management.quantity_available += self.quantity
            article_management.save()
            self.status = "Returned"  # Set the status field to "Returned"
            validate(self)
            frappe.msgprint(f"{self.quantity} Article returned to the Library for {article_management.name}")

    def on_update(self):
        # Ensure the status is updated when returning an article
        if self.action == "Return.":
            self.status = "Returned"
            frappe.msgprint(f"Status updated to 'Returned' for {self.name}")


        
# check if the aricle is available or rented


def validate(doc):
    article_management = frappe.get_doc("Article Management", doc.article)
    if article_management.quantity_available == 0:
        article_management.status= 'out of stock'
        article_management.save()

    elif article_management.quantity_available > 0:
        article_management.status= 'Available'
        article_management.save()


# if the article is not in stock then the article will not be issued 

def validate_issue(doc):
    article_management = frappe.get_doc("Article Management", doc.article)

    if doc.action == "Lend.":
        if article_management.quantity_available < doc.quantity:
            frappe.throw(f"Out Of Stock {article_management.quantity_available}.Articles available in the Library")

    elif doc.action == "Return.":
        if article_management.quantity_available == 0:
            frappe.msgprint("Article has been Restocked Now.")



