# Copyright (c) 2024, ateeq and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class LibraryMembership(Document):
	pass

import frappe
from frappe.model.document import Document
from frappe.model.docstatus import DocStatus


class LibraryMembership(Document):
    # check before submitting this document
    def before_submit(self):
        exists = frappe.db.exists(
            "Library Membership",
            {
                "library_member": self.library_member,
                "docstatus": DocStatus.submitted(),
                # check if the membership's end date is later than this membership's start date
                "to_date": (">", self.from_date),
            },
        )
        if exists:
            frappe.throw("There is an active membership for this member")


import frappe
from frappe.model.document import Document
from frappe.model.docstatus import DocStatus


class LibraryTransaction(Document):
    def before_submit(self):
        if self.type == "Lend.":
            self.validate_Lend()
            self.validate_maximum_limit()
            # set the article status to be Lend.d
            article = frappe.get_doc("Article", self.article)
            article.status = "Lend."
            article.save()

        elif self.type == "Return":
            self.validate_return()
            # set the article status to be Available
            article = frappe.get_doc("Article", self.article)
            article.status = "Available"
            article.save()

    def validate_Lend(self):
        self.validate_membership()
        article = frappe.get_doc("Article", self.article)
        # article cannot be Lend.d if it is already Lend.d
        if article.status == "Lend.":
            frappe.throw("Article is already Lend. by another member")

    def validate_return(self):
        article = frappe.get_doc("Article", self.article)
        # article cannot be returned if it is not Lend.d first
        if article.status == "Available":
            frappe.throw("Article cannot be returned without being Lend.d first")

    def validate_maximum_limit(self):
        max_articles = frappe.db.get_single_value("Library Settings", "max_articles")
        count = frappe.db.count(
            "Library Transaction",
            {"library_member": self.library_member, "type": "Lend.", "docstatus": DocStatus.submitted()},
        )
        if count >= max_articles:
            frappe.throw("Maximum limit reached for issuing articles")

    def validate_membership(self):
        # check if a valid membership exist for this library member
        valid_membership = frappe.db.exists(
            "Library Membership",
            {
                "library_member": self.library_member,
                "docstatus": DocStatus.submitted(),
                "from_date": ("<", self.date),
                "to_date": (">", self.date),
            },
        )
        if not valid_membership:
            frappe.throw("The member does not have a valid membership")


import frappe
from frappe.model.document import Document
from frappe.model.docstatus import DocStatus
from frappe.utils import today, getdate

class LibraryMembership(Document):
    # check before saving or submitting this document
    def validate(self):
        self.validate_membership_date()

    def before_submit(self):
        self.validate_membership_date()
        exists = frappe.db.exists(
            "Library Membership",
            {
                "library_member": self.library_member,
                "docstatus": DocStatus.submitted(),
                # check if the membership's end date is later than this membership's start date
                "expiry_date": (">", self.from_date),
            },
        )
        if exists:
            frappe.throw("There is an active membership for this member")

    def validate_membership_date(self):
        if getdate(self.from_date) < getdate(today()):
            frappe.throw("Membership joining date cannot be before today")



import frappe
from frappe.utils import add_days, getdate

@frappe.whitelist()
def send_reminder(membership):
    # Get the current date and the threshold date for expiry
    expiry_threshold = getdate(add_days(frappe.utils.today(), 30))
    
    # Fetch the particular membership
    membership_doc = frappe.get_doc('Library Membership', membership)
    
    # Convert expiry_date to a date object if it's a string
    expiry_date = membership_doc.expiry_date
    if isinstance(expiry_date, str):
        expiry_date = getdate(expiry_date)
    
    # Check if the membership is expiring within the next 30 days
    if expiry_date <= expiry_threshold:
        message = (f"Membership expiring soon:\n"
                   f"Member: {membership_doc.library_member}, "
                   f"Email: {membership_doc.email}, "
                   f"Expiry Date: {expiry_date}\n")
        return message
    else:
        return "This membership is not expiring soon."
