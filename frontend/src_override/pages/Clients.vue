<template>
  <LayoutHeader>
    <template #left-header>
      <div class="flex items-center gap-2 text-lg font-medium text-ink-gray-9">
        <OrganizationsIcon class="h-5 w-5 text-ink-gray-7" />
        <span>{{ __('Clients') }}</span>
      </div>
    </template>
  </LayoutHeader>

  <div class="flex flex-col overflow-hidden">
    <!-- Filter bar -->
    <div class="flex flex-wrap items-center gap-2 px-5 py-4">
      <FormControl
        type="select"
        :options="organisationOptions"
        v-model="filters.organization"
        :placeholder="__('All organisations')"
        class="w-56"
      />
      <FormControl
        type="select"
        :options="industryOptions"
        v-model="filters.industry"
        :placeholder="__('All industries')"
        class="w-56"
      />
    </div>

    <!-- Table -->
    <div class="flex-1 overflow-auto px-5">
      <table class="w-full text-base">
        <thead>
          <tr class="border-b text-ink-gray-5 text-sm">
            <th class="py-2.5 pr-4 text-left font-normal">{{ __('Organisation') }}</th>
            <th class="py-2.5 pr-4 text-left font-normal">{{ __('Industry') }}</th>
            <th class="py-2.5 pr-4 text-left font-normal">{{ __('Primary Contact') }}</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="row in rows"
            :key="row.name"
            class="border-b text-ink-gray-8 cursor-pointer hover:bg-surface-gray-1"
            @click="openClient(row.name)"
          >
            <td class="py-3 pr-4">
              <span class="flex items-center gap-2">
                <span
                  class="h-2 w-2 flex-shrink-0 rounded-full"
                  :class="
                    row.client_status === 'Inactive'
                      ? 'bg-surface-red-5'
                      : 'bg-surface-green-5'
                  "
                />
                <span class="font-medium text-ink-gray-9">{{ row.name }}</span>
              </span>
            </td>
            <td class="py-3 pr-4">{{ row.industry || '-' }}</td>
            <td class="py-3 pr-4">{{ primaryContact(row.name) }}</td>
          </tr>
          <tr v-if="!rows.length && !clients.loading">
            <td colspan="3" class="py-10 text-center text-ink-gray-5">
              {{ __('No clients found') }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import LayoutHeader from '@/components/LayoutHeader.vue'
import OrganizationsIcon from '@/components/Icons/OrganizationsIcon.vue'
import { FormControl, createResource } from 'frappe-ui'
import { ref, reactive, computed, watch } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
function openClient(name) {
  router.push({ name: 'Organization', params: { organizationId: name } })
}

const filters = reactive({
  organization: '',
  industry: '',
})

const clients = createResource({
  url: 'frappe.client.get_list',
  makeParams() {
    const f = { is_client: 1 }
    if (filters.organization) f.name = filters.organization
    if (filters.industry) f.industry = filters.industry
    return {
      doctype: 'CRM Organization',
      fields: ['name', 'organization_name', 'industry', 'client_status'],
      filters: f,
      order_by: 'name asc',
      limit_page_length: 0,
    }
  },
  auto: true,
})

const rows = computed(() => clients.data || [])

// Filter dropdown options (populated from all client organisations)
const organisationOptions = ref([{ label: __('All organisations'), value: '' }])
const industryOptions = ref([{ label: __('All industries'), value: '' }])
createResource({
  url: 'frappe.client.get_list',
  params: {
    doctype: 'CRM Organization',
    filters: { is_client: 1 },
    fields: ['name', 'industry'],
    order_by: 'name asc',
    limit_page_length: 0,
  },
  auto: true,
  onSuccess(data) {
    organisationOptions.value = [
      { label: __('All organisations'), value: '' },
      ...data.map((o) => ({ label: o.name, value: o.name })),
    ]
    const industries = [...new Set(data.map((o) => o.industry).filter(Boolean))]
    industryOptions.value = [
      { label: __('All industries'), value: '' },
      ...industries.sort().map((i) => ({ label: i, value: i })),
    ]
  },
})

// Primary contact = first Contact whose company_name matches the organisation
const contactMap = ref({})
createResource({
  url: 'frappe.client.get_list',
  params: {
    doctype: 'Contact',
    fields: ['first_name', 'last_name', 'company_name'],
    order_by: 'creation asc',
    limit_page_length: 0,
  },
  auto: true,
  onSuccess(data) {
    const map = {}
    data.forEach((c) => {
      if (!c.company_name) return
      if (map[c.company_name]) return
      map[c.company_name] = `${c.first_name || ''} ${c.last_name || ''}`.trim()
    })
    contactMap.value = map
  },
})

function primaryContact(org) {
  const name = contactMap.value[org]
  return name ? `${name}-${org}` : '-'
}

let debounce
watch(
  filters,
  () => {
    clearTimeout(debounce)
    debounce = setTimeout(() => clients.reload(), 300)
  },
  { deep: true },
)
</script>
