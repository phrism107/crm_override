<template>
  <LayoutHeader>
    <template #left-header>
      <div class="flex items-center gap-2">
        <Button variant="ghost" @click="router.push({ name: 'Interactions' })">
          <template #icon>
            <FeatherIcon name="arrow-left" class="h-4 w-4" />
          </template>
        </Button>
        <span class="text-base text-ink-gray-6">{{ __('Interactions') }}</span>
      </div>
    </template>
  </LayoutHeader>

  <div v-if="doc" class="flex h-full">
    <!-- Left: field panel -->
    <div class="flex h-full w-[350px] flex-col overflow-y-auto border-r">
      <div class="border-b p-5">
        <div class="text-xl font-medium text-ink-gray-9">
          {{ doc.subject || __('Interaction') }}
        </div>
      </div>
      <div class="flex flex-col gap-4 p-5">
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

    <!-- Right: Organisation tab -->
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
          @click="openOrganization"
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
  interactionId: { type: String, required: true },
})

const router = useRouter()

const interaction = createResource({
  url: 'frappe.client.get',
  makeParams: () => ({ doctype: 'CRM Interaction', name: props.interactionId }),
  auto: true,
})

const doc = computed(() => interaction.data)

const followUp = computed(() => {
  if (!doc.value) return ''
  if (!doc.value.follow_up) return 'No'
  return doc.value.follow_up_date
    ? `Yes — ${formatDate(doc.value.follow_up_date)}`
    : 'Yes'
})

const fields = computed(() => {
  const d = doc.value || {}
  return [
    { label: __('Contact'), value: d.contact_name || d.contact },
    { label: __('Date'), value: formatDate(d.interaction_date) },
    { label: __('Time'), value: d.interaction_time },
    { label: __('Source'), value: d.source },
    { label: __('Type'), value: d.interaction_type },
    { label: __('Status'), value: d.status },
    { label: __('Follow Up'), value: followUp.value },
    { label: __('Description'), value: d.description || d.notes },
  ]
})

function formatDate(date) {
  if (!date) return ''
  const [y, m, d] = String(date).split(' ')[0].split('-')
  return d && m && y ? `${d}-${m}-${y}` : date
}

function openOrganization() {
  router.push({
    name: 'Organization',
    params: { organizationId: doc.value.organization },
  })
}
</script>
