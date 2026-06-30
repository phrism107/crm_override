<template>
  <div
    class="relative flex h-full flex-col justify-between transition-all duration-300 ease-in-out"
    :class="isSidebarCollapsed ? 'w-12' : 'w-[220px]'"
  >
    <div class="p-2">
      <UserDropdown :isCollapsed="isSidebarCollapsed" />
    </div>
    <div class="flex-1 overflow-y-auto">
      <div v-for="view in allViews" :key="view.label">
        <div class="mx-2 my-1.5" />
        <CollapsibleSection
          :label="view.name"
          :hideLabel="view.hideLabel"
          :opened="view.opened"
        >
          <template #header="{ opened, hide, toggle }">
            <div
              v-if="!hide"
              class="flex items-center cursor-pointer gap-1.5 text-base text-ink-gray-5 transition-all duration-300 ease-in-out"
              :class="
                isSidebarCollapsed
                  ? 'h-0 overflow-hidden opacity-0'
                  : 'px-4 pt-[11px] pb-2.5 w-auto opacity-100'
              "
              @click="toggle()"
            >
              <span
                class="lucide-chevron-right h-4 text-ink-gray-9 transition-all duration-300 ease-in-out"
                :class="{ 'rotate-90': opened }"
                aria-hidden="true"
              />
              <span>{{ __(view.name) }}</span>
            </div>
          </template>
          <nav class="flex flex-col">
            <SidebarLink
              v-for="link in view.views"
              :key="link.label"
              :icon="link.icon"
              :label="__(link.label)"
              :to="link.to"
              :isCollapsed="isSidebarCollapsed"
              class="mx-2 my-[1.5px]"
            />
          </nav>
        </CollapsibleSection>
      </div>
    </div>
    <div class="m-2 flex flex-col gap-1">
      <SidebarLink
        :label="isSidebarCollapsed ? __('Expand') : __('Collapse')"
        :isCollapsed="isSidebarCollapsed"
        class=""
        @click="isSidebarCollapsed = !isSidebarCollapsed"
      >
        <template #icon>
          <span class="grid h-4 w-4 flex-shrink-0 place-items-center">
            <CollapseSidebar
              class="h-4 w-4 text-ink-gray-7 duration-300 ease-in-out"
              :class="{ '[transform:rotateY(180deg)]': isSidebarCollapsed }"
            />
          </span>
        </template>
      </SidebarLink>
    </div>
  </div>
</template>

<script setup>
import ContactsIcon from '@/components/Icons/ContactsIcon.vue'
import OrganizationsIcon from '@/components/Icons/OrganizationsIcon.vue'
import CollapsibleSection from '@/components/CollapsibleSection.vue'
import UserDropdown from '@/components/UserDropdown.vue'
import CollapseSidebar from '@/components/Icons/CollapseSidebar.vue'
import SidebarLink from '@/components/SidebarLink.vue'
import { viewsStore } from '@/stores/views'
import { useStorage } from '@vueuse/core'
import { computed } from 'vue'

const { getPinnedViews, getPublicViews } = viewsStore()

const isSidebarCollapsed = useStorage('isSidebarCollapsed', false)

// PHRISM: only Contacts and Organizations are exposed in the sidebar.
// Original Frappe CRM links (Dashboard, Leads, Deals, Notes, Tasks,
// Calendar, Call Logs, Notifications) intentionally removed.
const links = [
  {
    label: 'Contacts',
    icon: ContactsIcon,
    to: 'Contacts',
  },
  {
    label: 'Organizations',
    icon: OrganizationsIcon,
    to: 'Organizations',
  },
]

const allViews = computed(() => {
  let _views = [
    {
      name: 'All Views',
      hideLabel: true,
      opened: true,
      views: links,
    },
  ]
  if (getPublicViews().length) {
    _views.push({
      name: 'Public Views',
      opened: true,
      views: parseView(getPublicViews()),
    })
  }
  if (getPinnedViews().length) {
    _views.push({
      name: 'Pinned Views',
      opened: true,
      views: parseView(getPinnedViews()),
    })
  }
  return _views
})

function parseView(views) {
  return views.map((view) => {
    return {
      label: view.label,
      icon: getIcon(view.route_name, view.icon),
      to: {
        name: view.route_name,
        params: { viewType: view.type || 'list' },
        query: { view: view.name },
      },
    }
  })
}

function getIcon(routeName, icon) {
  if (icon) return icon
  switch (routeName) {
    case 'Contacts':
      return ContactsIcon
    case 'Organizations':
      return OrganizationsIcon
    default:
      return ContactsIcon
  }
}
</script>
