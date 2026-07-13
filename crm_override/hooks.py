app_name = "crm_override"
app_title = "Phrism CRM Override"
app_publisher = "Phrism"
app_description = "Overrides Frappe CRM to expose the pHRism tabs: Organisations, Contacts, Interactions, Projects, Leads, Clients."
app_email = "phrism107@gmail.com"
app_license = "mit"

# Fixtures
# -----------------------------------------------------------------------------
# Ship the client-flag custom fields added to the stock CRM Organization
# doctype so they are recreated on every site the app is installed on.
fixtures = [
	{
		"dt": "Custom Field",
		"filters": [
			["dt", "in", ["CRM Organization", "CRM Deal", "CRM Lead"]]
		],
	}
]
