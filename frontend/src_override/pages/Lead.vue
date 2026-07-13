<template>
  <LayoutHeader v-if="doc.name">
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
    <template #right-header>
      <Dropdown v-if="doc.status" :options="statuses" placement="right">
        <template #default="{ open }">
          <Button
            :label="doc.status"
            :iconRight="open ? 'chevron-up' : 'chevron-down'"
          >
            <template #prefix>
              <span
                class="h-2 w-2 rounded-full"
                :style="{ backgroundColor: statusColor }"
              />
            </template>
          </Button>
        </template>
      </Dropdown>
      <Button
        :label="__('Convert to Project')"
        variant="solid"
        @click="convertToProject"
      />
    </template>
  </LayoutHeader>

  <div v-if="doc.name" class="flex h-full">
    <!-- Left: editable Details + Person -->
    <div class="flex h-full w-[360px] flex-col overflow-y-auto border-r">
      <div class="border-b p-5">
        <div class="text-sm text-ink-gray-6">{{ leadId }}</div>
        <div class="mt-3 flex items-center gap-3">
          <Avatar size="2xl" :label="doc.lead_name || leadId" />
          <div class="text-xl font-medium text-ink-gray-9">
            {{ doc.lead_name || leadId }}
          </div>
        </div>
        <div class="mt-3 flex gap-1.5">
          <Button :tooltip="__('Copy link')" icon="link" @click="copyLink" />
          <Button
            :tooltip="__('Delete')"
            icon="trash-2"
            theme="red"
            variant="subtle"
            @click="showDeleteModal = true"
          />
        </div>
      </div>
      <div v-if="sections.data" class="flex-1 overflow-y-auto">
        <SidePanelLayout
          :sections="sections.data"
          doctype="CRM Lead"
          :docname="doc.name"
          @reload="sections.reload"
          @beforeFieldChange="() => lead.save.submit()"
        />
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

  <DeleteLinkedDocModal
    v-if="showDeleteModal"
    v-model="showDeleteModal"
    doctype="CRM Lead"
    :docname="leadId"
    name="Leads"
  />
</template>

<script setup>
import LayoutHeader from '@/components/LayoutHeader.vue'
import SidePanelLayout from '@/components/SidePanelLayout.vue'
import DeleteLinkedDocModal from '@/components/DeleteLinkedDocModal.vue'
import OrganizationsIcon from '@/components/Icons/OrganizationsIcon.vue'
import { useDocument } from '@/data/document'
import { statusesStore } from '@/stores/statuses'
import {
  Avatar,
  Button,
  Dropdown,
  FeatherIcon,
  createResource,
  call,
  toast,
} from 'frappe-ui'
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps({
  leadId: { type: String, required: true },
})

const router = useRouter()
const { statusOptions, getLeadStatus } = statusesStore()

const { document: lead } = useDocument('CRM Lead', props.leadId)
const doc = computed(() => lead.doc || {})

const showDeleteModal = ref(false)

const sections = createResource({
  url: 'crm.fcrm.doctype.crm_fields_layout.crm_fields_layout.get_sidepanel_sections',
  cache: ['sidePanelSections', 'CRM Lead'],
  params: { doctype: 'CRM Lead' },
  auto: true,
})

const statuses = computed(() => statusOptions('lead', [], triggerStatusChange))

const statusColor = computed(() => {
  const map = {
    gray: '#8f8f8f', blue: '#3b82f6', green: '#22c55e', red: '#ef4444',
    orange: '#f97316', amber: '#f59e0b', yellow: '#eab308', teal: '#14b8a6',
    purple: '#a855f7', pink: '#ec4899', cyan: '#06b6d4', black: '#1f1f1f',
  }
  const c = doc.value.status && getLeadStatus(doc.value.status)?.color
  return map[c] || '#8f8f8f'
})

function triggerStatusChange(value) {
  lead.doc.status = value
  lead.save.submit()
}

async function convertToProject() {
  try {
    const deal = await call(
      'crm.fcrm.doctype.crm_lead.crm_lead.convert_to_deal',
      { lead: props.leadId },
    )
    if (deal) {
      toast.success(__('Converted to Project'))
      router.push({ name: 'Deal', params: { dealId: deal } })
    }
  } catch (e) {
    toast.error(e.messages?.[0] || __('Could not convert to project'))
  }
}

function copyLink() {
  navigator.clipboard?.writeText(window.location.href)
  toast.success(__('Link copied'))
}
</script>
