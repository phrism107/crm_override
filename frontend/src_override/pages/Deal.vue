<template>
  <LayoutHeader>
    <template #left-header>
      <div class="flex items-center gap-2">
        <Button variant="ghost" @click="router.push({ name: 'Deals' })">
          <template #icon>
            <FeatherIcon name="arrow-left" class="h-4 w-4" />
          </template>
        </Button>
        <span class="text-base text-ink-gray-6">{{ __('Projects') }}</span>
        <span class="text-base text-ink-gray-9">/ {{ doc.project_title || dealId }}</span>
      </div>
    </template>
  </LayoutHeader>

  <div v-if="doc.name" class="flex h-full">
    <!-- Left: Project Details -->
    <div class="flex h-full w-[360px] flex-col overflow-y-auto border-r">
      <div class="border-b p-5 text-sm text-ink-gray-6">{{ dealId }}</div>
      <div class="p-5">
        <div class="mb-3 text-base font-semibold text-ink-gray-9">
          {{ __('Project Details') }}
        </div>
        <div class="flex flex-col gap-4">
          <div v-for="f in fields" :key="f.label" class="flex flex-col gap-1">
            <div class="text-xs uppercase tracking-wide text-ink-gray-5">
              {{ f.label }}
            </div>
            <div class="text-base text-ink-gray-8 whitespace-pre-line">
              {{ f.value || '-' }}
            </div>
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
  dealId: { type: String, required: true },
})

const router = useRouter()

const deal = createResource({
  url: 'frappe.client.get',
  makeParams: () => ({ doctype: 'CRM Deal', name: props.dealId }),
  auto: true,
})

const doc = computed(() => deal.data || {})

function formatDate(date) {
  if (!date) return ''
  const [y, m, d] = String(date).split(' ')[0].split('-')
  return d && m && y ? `${d}-${m}-${y}` : date
}

function money(v) {
  if (v === undefined || v === null || v === '') return ''
  return '£ ' + Number(v).toLocaleString('en-GB', { minimumFractionDigits: 2 })
}

const fields = computed(() => {
  const d = doc.value
  const contact = [d.first_name, d.last_name].filter(Boolean).join(' ') || d.contact
  return [
    { label: __('Project Title'), value: d.project_title },
    { label: __('Organisation'), value: d.organization },
    { label: __('Contact'), value: contact },
    { label: __('Engagement Type'), value: d.engagement_type },
    { label: __('Status'), value: d.status },
    { label: __('Project Size'), value: money(d.project_size || d.annual_revenue) },
    { label: __('Engagement Start Date'), value: formatDate(d.engagement_start_date) },
    { label: __('Engagement End Date'), value: formatDate(d.engagement_end_date) },
    { label: __('Primary email'), value: d.email },
    { label: __('Primary mobile no'), value: d.mobile_no },
    { label: __('Brief Detail'), value: d.brief_detail },
  ]
})
</script>
