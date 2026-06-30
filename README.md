# crm_override

Overrides Frappe CRM's sidebar so only **Contacts** and **Organizations** are
shown. Built on the [esafwan/crm_override](https://github.com/esafwan/crm_override)
pattern: at build time, `frontend/custom-build.js` copies the stock `crm`
app's `frontend/src` into this app's `frontend/src`, then overlays
`frontend/src_override/` on top before running `vite build`. Because this app
installs after `crm` on the bench, `/crm` ends up served from this app's
compiled bundle instead of stock `crm`.

## What changed

`frontend/src_override/components/Layouts/AppSidebar.vue` replaces the stock
sidebar's `links` array (Dashboard, Leads, Deals, Contacts, Organizations,
Notes, Tasks, Calendar, Call Logs) with just:

```js
const links = [
  { label: 'Contacts', icon: ContactsIcon, to: 'Contacts' },
  { label: 'Organizations', icon: OrganizationsIcon, to: 'Organizations' },
]
```

Note: any **Public/Pinned Views** the team has saved against other doctypes
(e.g. a saved Leads view) will still appear under those sections, since they
come from `CRM View Settings` data, not the `links` array. Delete those saved
views (or hide them) separately if you want a fully clean sidebar.

## Deploy steps (Frappe Cloud)

1. Push this `crm_override` folder to its own Git repository (e.g.
   `github.com/<you>/crm_override`).
2. In the Frappe Cloud dashboard, go to your **Bench Group** for
   `phrism.frappe.cloud`.
3. **Apps → Add App from Git Repository** → paste the repo URL, branch
   `main`.
4. **Apps → Update** → it will detect `crm_override` as a new app to deploy
   → **Skip & Deploy** (or include in next deploy).
5. Once the bench rebuild finishes, go to **Sites → phrism.frappe.cloud → Apps**
   and **Install App** → select `crm_override`. (Install order matters:
   `crm_override` must install **after** `crm` so its frontend bundle wins.)
6. **Site → Update** to apply.
7. Hard-refresh `https://phrism.frappe.cloud/crm` — only Contacts and
   Organizations should remain in the sidebar.

This requires a Frappe Cloud plan that allows custom apps (Git-based app
installs). If your plan doesn't support it, the alternative is hiding the
data tabs at the doctype/permission level so non-Contact/Organization
sections show "not permitted" when clicked — let me know if you'd rather go
that route instead.
