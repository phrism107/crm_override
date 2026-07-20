import frappe


def sync_lead_organization(doc, method=None):
	"""Ensure the organization named on a CRM Lead exists as a CRM Organization.

	CRM Lead.organization is a plain Data field, so typing an organisation
	name on a lead does not create a CRM Organization record (stock CRM only
	creates one on lead conversion). This doc-event hook creates the record
	on lead save, carrying over whatever detail the lead already holds, so
	the Organizations tab always reflects organisations named on leads.
	"""
	org = (doc.organization or "").strip()
	if not org or frappe.db.exists("CRM Organization", org):
		return

	organization = frappe.new_doc("CRM Organization")
	organization.organization_name = org
	for source_field, target_field in (
		("website", "website"),
		("industry", "industry"),
		("territory", "territory"),
		("no_of_employees", "no_of_employees"),
		("annual_revenue", "annual_revenue"),
	):
		value = doc.get(source_field)
		if value:
			organization.set(target_field, value)
	organization.insert(ignore_permissions=True)
