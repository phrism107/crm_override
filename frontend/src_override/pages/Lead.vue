<template>
  <LayoutHeader>
    <template #left-header>
      <div class="flex items-center gap-2">
        <Button variant="ghost" @click="router.push({ name: 'Leads' })">
          <template #icon>
            <FeatherIcon name="arrow-left" class="h-4 w-4" />
          </template>
        </Button>
        <span class="text-base text-ink-gray-6">{{ __('Leads') }}</span>
        <span class="text-base text-ink-gray-9">/ {{ doc.lead_name || leadId }}</span>
      </div>
    </template>
  </LayoutHeader>

  <div v-if="doc.name" class="flex h-full">
    <!-- Left: Details + Person -->
    <div class="flex h-full w-[360px] flex-col overflow-y-auto border-r">
      <div class="border-b p-5 text-sm text-ink-gray-6">{{ leadId }}</div>
      <div class="p-5">
        <div class="mb-3 text-base font-semibold text-ink-gray-9">
          {{ __('Details') }}
        </div>
        <div class="flex flex-col gap-4">
          <div v-for="f in details" :key="f.label" class="flex flex-col gap-1">
            <div class="text-xs uppercase tracking-wide text-ink-gray-5">
              {{ f.label }}
            </div>
            <div class="text-base text-ink-gray-8">{{ f.value || '-' }}</div>
          </div>
        </div>

        <div class="mb-3 mt-6 text-base font-semibold text-ink-gray-9">
          {{ __('Person') }}
        </div>
        <div class="flex flex-col gap-4">
          <div v-for="f in person" :key="f.label" class="flex flex-col gap-1">
            <div class="text-xs uppercase tracking-wide text-ink-gray-5">
              {{ f.label }}
            </div>
            <div class="text-base text-ink-gray-8">{{ f.value || '-' }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Right: Organisation -->
    <div class="flex flex-1 flex-col overflow-hidden">
      <div class="flex items-center gap-2 border-b px-5 min-h-[45px]">
        <div
          class="flex items-center gap-2 border-b border-ink-gray-9 py-2.5 text-base text-ink-gray-9"
        >
          <OrganizationsIcon class="h-4 w-4" />
          {{ __('Organisation') }}
        </div>
      </div>
      <div class="p-5">
        <div
          v-if="doc.organization"
          class="cursor-pointer rounded border px-4 py-3 text-base text-ink-blue-3 hover:bg-surface-gray-1"
          @click="
            router.push({
              name: 'Organization',
              params: { organizationId: doc.organization },
            })
          "
        >
          {{ doc.organization }}
        </div>
        <div v-else class="text-base text-ink-gray-5">
          {{ __('No organisation linked') }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import LayoutHeader from '@/components/LayoutHeader.vue'
import OrganizationsIcon from '@/components/Icons/OrganizationsIcon.vue'
import { Button, FeatherIcon, createResource } from 'frappe-ui'
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps({
  leadId: { type: String, required: true },
})

const router = useRouter()

const lead = createResource({
  url: 'frappe.client.get',
  makeParams: () => ({ doctype: 'CRM Lead', name: props.leadId }),
  auto: true,
})

const doc = computed(() => lead.data || {})

function formatDate(date) {
  if (!date) return ''
  const [y, m, d] = String(date).split(' ')[0].split('-')
  return d && m && y ? `${d}-${m}-${y}` : date
}

const details = computed(() => {
  const d = doc.value
  return [
    { label: __('Organisation'), value: d.organization },
    { label: __('Source'), value: d.source },
    { label: __('Status'), value: d.status },
    { label: __('Lead Received Date'), value: formatDate(d.lead_received_date) },
    { label: __('Whose Lead'), value: d.whose_lead },
  ]
})

const person = computed(() => {
  const d = doc.value
  return [
    { label: __('First Name'), value: d.first_name },
    { label: __('Last Name'), value: d.last_name },
    { label: __('Email'), value: d.email },
    { label: __('Mobile No.'), value: d.mobile_no },
  ]
})
</script>
