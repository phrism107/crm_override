<template>
  <LayoutHeader>
    <template #left-header>
      <div class="flex items-center gap-2 text-lg font-medium text-ink-gray-9">
        <PhoneIcon class="h-5 w-5 text-ink-gray-7" />
        <span>{{ __('Interactions') }}</span>
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
        :options="typeOptions"
        v-model="filters.interaction_type"
        :placeholder="__('All types')"
        class="w-40"
      />
      <FormControl
        type="select"
        :options="sourceOptions"
        v-model="filters.source"
        :placeholder="__('All sources')"
        class="w-40"
      />
      <FormControl
        type="text"
        v-model="filters.contact"
        :placeholder="__('Contact...')"
        class="w-52"
      />
    </div>

    <!-- Table -->
    <div class="flex-1 overflow-auto px-5">
      <table class="w-full text-base">
        <thead>
          <tr class="border-b text-ink-gray-5 text-sm">
            <th class="py-2.5 pr-4 text-left font-normal">{{ __('Organisation') }}</th>
            <th class="py-2.5 pr-4 text-left font-normal">{{ __('Type') }}</th>
            <th class="py-2.5 pr-4 text-left font-normal">{{ __('Source') }}</th>
            <th class="py-2.5 pr-4 text-left font-normal">{{ __('Contact') }}</th>
            <th class="py-2.5 pr-4 text-left font-normal">{{ __('Subject') }}</th>
            <th class="py-2.5 pr-4 text-right font-normal">{{ __('Date') }}</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="row in rows"
            :key="row.name"
            class="border-b text-ink-gray-8 hover:bg-surface-gray-1"
          >
            <td class="py-3 pr-4">{{ row.organization }}</td>
            <td class="py-3 pr-4">{{ row.interaction_type }}</td>
            <td class="py-3 pr-4">{{ row.source }}</td>
            <td class="py-3 pr-4">{{ row.contact_name || row.contact }}</td>
            <td class="py-3 pr-4">{{ row.subject }}</td>
            <td class="py-3 pr-4 text-right whitespace-nowrap">
              {{ formatDMY(row.interaction_date) }}
            </td>
          </tr>
          <tr v-if="!rows.length && !interactions.loading">
            <td colspan="6" class="py-10 text-center text-ink-gray-5">
              {{ __('No interactions found') }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import LayoutHeader from '@/components/LayoutHeader.vue'
import PhoneIcon from '@/components/Icons/PhoneIcon.vue'
import { FormControl, createResource } from 'frappe-ui'
import { ref, reactive, computed, watch } from 'vue'

const filters = reactive({
  organization: '',
  interaction_type: '',
  source: '',
  contact: '',
})

const typeOptions = [
  { label: __('All types'), value: '' },
  { label: 'Lead', value: 'Lead' },
  { label: 'Project', value: 'Project' },
  { label: 'General', value: 'General' },
]

const sourceOptions = [
  { label: __('All sources'), value: '' },
  { label: 'Call', value: 'Call' },
  { label: 'Email', value: 'Email' },
  { label: 'In person', value: 'In person' },
]

// Organisation filter options
const organisationOptions = ref([{ label: __('All organisations'), value: '' }])
createResource({
  url: 'frappe.client.get_list',
  params: {
    doctype: 'CRM Organization',
    fields: ['name'],
    order_by: 'name asc',
    limit_page_length: 0,
  },
  auto: true,
  onSuccess(data) {
    organisationOptions.value = [
      { label: __('All organisations'), value: '' },
      ...data.map((o) => ({ label: o.name, value: o.name })),
    ]
  },
})

const interactions = createResource({
  url: 'frappe.client.get_list',
  makeParams() {
    const f = {}
    if (filters.organization) f.organization = filters.organization
    if (filters.interaction_type) f.interaction_type = filters.interaction_type
    if (filters.source) f.source = filters.source
    if (filters.contact) f.contact_name = ['like', `%${filters.contact}%`]
    return {
      doctype: 'CRM Interaction',
      fields: [
        'name',
        'organization',
        'interaction_type',
        'source',
        'contact',
        'contact_name',
        'subject',
        'interaction_date',
      ],
      filters: f,
      order_by: 'interaction_date desc',
      limit_page_length: 0,
    }
  },
  auto: true,
})

const rows = computed(() => interactions.data || [])

let debounce
watch(
  filters,
  () => {
    clearTimeout(debounce)
    debounce = setTimeout(() => interactions.reload(), 300)
  },
  { deep: true },
)

function formatDMY(date) {
  if (!date) return ''
  const [y, m, d] = date.split('-')
  return `${d}-${m}-${y}`
}
</script>
