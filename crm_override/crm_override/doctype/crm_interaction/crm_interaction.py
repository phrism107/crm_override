# Copyright (c) 2026, Phrism and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class CRMInteraction(Document):
	def before_save(self):
		# Keep the denormalised contact_name in sync with the linked Contact
		# so the Interactions list can display/filter it without a join.
		if self.contact and not self.contact_name:
			self.contact_name = frappe.db.get_value("Contact", self.contact, "full_name")
