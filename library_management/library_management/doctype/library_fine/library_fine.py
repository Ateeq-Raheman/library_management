# Copyright (c) 2024, ateeq and contributors
# For license information, please see license.txt

# import frappe
from pydoc import doc
from frappe.model.document import Document


class Libraryfine(Document):
	pass


# library_management/library_management/doctype/library_fine/library_fine.py

# import frappe
# from frappe.model.document import Document

# class LibraryFine(Document):
#     def validate(self):
#         self.calculate_fine_amount()

#     def calculate_fine_amount(self):
#         if self.overdue_days and self.fine_per_day:
#             self.fine_amount = self.overdue_days * self.fine_per_day
#         else:
#             self.fine_amount = 0.00


# import frappe

# def calculate_fine_for_article(library_fine_name):
#     try:
#         # Fetch the Library Fine document
#         library_fine = frappe.get_doc('Library Fine', library_fine_name)
        
#         # Get the overdue days from the document
#         overdue_days = library_fine.get('overdue_days')
        
#         # Get the fine per day from the document
#         fine_per_day = library_fine.get('fine_per_day')
        
#         # Check if overdue_days and fine_per_day are not None
#         if overdue_days is None:
#             print(f"No overdue days specified for document {library_fine_name}.")
#             return 0
#         if fine_per_day is None:
#             print(f"No fine per day specified for document {library_fine_name}.")
#             return 0
        
#         # Calculate the total fine
#         total_fine = overdue_days * fine_per_day
        
#         # Update the Fine Amount field in the document
#         library_fine.fine_amount = total_fine
        
#         # Save the document
#         library_fine.save()
        
#         print(f"Fine for document {library_fine_name} updated successfully: Rs {total_fine}")
        
#         return total_fine
#     except frappe.DoesNotExistError:
#         print(f"Document {library_fine_name} does not exist.")
#         return 0
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return 0

# # Example usage
# library_fine_name = 'LIBRARY-FINE-001'  # Replace with the actual Library Fine document name
# fine = calculate_fine_for_article(library_fine_name)
# print(f"The fine for the library fine document {library_fine_name} is: Rs {fine}")


# # Import necessary modules
# from __future__ import unicode_literals
# import frappe


# library_management/library_management/doctype/library_management/library_management.py

import frappe

# def before_save(doc, method):
#     overdue_days_value = doc.overdue_days if doc.overdue_days else 0
#     fine_per_day_value = doc.fine_per_day if doc.fine_per_day else 0
#     result = overdue_days_value * fine_per_day_value
#     doc.fine_amount = result
# before_save(doc)

# import frappe
# from frappe.model.document import Document
# from frappe import _

# class LibraryFine(Document):
#     def validate(self):
#         self.check_duplicate_fine()

#     def check_duplicate_fine(self):
#         existing_fine = frappe.db.exists('Library Fine', {
#             'article': self.article,
#             'member': self.member,
#             'due_date': self.due_date
#         })

#         if existing_fine:
#             frappe.throw(_("A fine for this article, member, and due date already exists: {0}").format(existing_fine), frappe.DuplicateEntryError)

