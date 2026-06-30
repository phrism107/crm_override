# Reuses the real Frappe CRM page controller (permission check + boot
# context) for our overridden www/crm.html, since Frappe's website router
# requires a matching <route>.py controller to build the Jinja render
# context (window.boot) for any www page that embeds boot-data templating.

from crm.www.crm import get_context as _get_context

no_cache = 1


def get_context():
	return _get_context()
