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
      <Button
        :label="__('Activity Log')"
        @click="rightTab = 'activity'"
      >
        <template #prefix>
          <FeatherIcon name="clock" class="h-4 w-4" />
        </template>
      </Button>
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

    <!-- Right: Organisation / Activity Log tabs -->
    <div class="flex flex-1 flex-col overflow-hidden">
      <div class="flex items-center gap-6 border-b px-5 min-h-[45px]">
        <button
          class="flex items-center gap-2 border-b py-2.5 text-base"
          :class="
            rightTab === 'organisation'
              ? 'border-ink-gray-9 text-ink-gray-9'
              : 'border-transparent text-ink-gray-5'
          "
          @click="rightTab = 'organisation'"
        >
          <OrganizationsIcon class="h-4 w-4" />
          {{ __('Organisation') }}
        </button>
        <button
          class="flex items-center gap-2 border-b py-2.5 text-base"
          :class="
            rightTab === 'activity'
              ? 'border-ink-gray-9 text-ink-gray-9'
              : 'border-transparent text-ink-gray-5'
          "
          @click="rightTab = 'activity'"
        >
          <FeatherIcon name="clock" class="h-4 w-4" />
          {{ __('Activity Log') }}
          <Badge v-if="activities.length" :label="String(activities.length)" theme="gray" />
        </button>
      </div>

      <!-- Organisation -->
      <div v-if="rightTab === 'organisation'" class="p-5">
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

      <!-- Activity Log -->
      <div v-else class="flex flex-1 flex-col overflow-auto p-5">
        <div class="mb-4 flex items-center justify-between">
          <div class="text-base font-semibold text-ink-gray-9">
            {{ __('Activity Log') }}
          </div>
          <Button
            :label="showForm ? __('Cancel') : __('Add Activity')"
            :iconLeft="showForm ? '' : 'plus'"
            variant="subtle"
            @click="showForm = !showForm"
          />
        </div>

        <!-- Add form -->
        <div
          v-if="showForm"
          class="mb-5 grid grid-cols-2 gap-3 rounded border p-4"
        >
          <FormControl type="date" :label="__('Activity Date')" v-model="form.activity_date" />
          <FormControl type="time" :label="__('Activity Time')" v-model="form.activity_time" />
          <FormControl type="select" :label="__('Activity Type')" :options="typeOptions" v-model="form.activity_type" />
          <FormControl type="select" :label="__('Activity Status')" :options="statusOptionsList" v-model="form.activity_status" />
          <FormControl type="select" :label="__('Communication Method')" :options="methodOptions" v-model="form.communication_method" />
          <FormControl type="text" :label="__('Performed By')" v-model="form.performed_by" />
          <div class="col-span-2">
            <FormControl type="text" :label="__('Subject')" v-model="form.subject" />
          </div>
          <div class="col-span-2">
            <FormControl type="textarea" :label="__('Notes / Description')" v-model="form.notes" />
          </div>
          <div class="col-span-2 flex justify-end">
            <Button :label="__('Save Activity')" variant="solid" @click="addActivity" />
          </div>
        </div>

        <!-- Activity table -->
        <table v-if="activities.length" class="w-full text-base">
          <thead>
            <tr class="border-b text-ink-gray-5 text-sm">
              <th class="py-2 pr-3 text-left font-normal">{{ __('Date') }}</th>
              <th class="py-2 pr-3 text-left font-normal">{{ __('Time') }}</th>
              <th class="py-2 pr-3 text-left font-normal">{{ __('Type') }}</th>
              <th class="py-2 pr-3 text-left font-normal">{{ __('Method') }}</th>
              <th class="py-2 pr-3 text-left font-normal">{{ __('Status') }}</th>
              <th class="py-2 pr-3 text-left font-normal">{{ __('Subject') }}</th>
              <th class="py-2 pr-3 text-left font-normal">{{ __('Performed By') }}</th>
              <th class="py-2 text-right font-normal"></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(a, i) in activities" :key="i" class="border-b text-ink-gray-8">
              <td class="py-2 pr-3 whitespace-nowrap">{{ formatDate(a.activity_date) }}</td>
              <td class="py-2 pr-3 whitespace-nowrap">{{ a.activity_time || '-' }}</td>
              <td class="py-2 pr-3">{{ a.activity_type || '-' }}</td>
              <td class="py-2 pr-3">{{ a.communication_method || '-' }}</td>
              <td class="py-2 pr-3">{{ a.activity_status || '-' }}</td>
              <td class="py-2 pr-3">{{ a.subject || '-' }}</td>
              <td class="py-2 pr-3">{{ a.performed_by || '-' }}</td>
              <td class="py-2 text-right">
                <Button
                  :tooltip="__('Delete activity')"
                  icon="trash-2"
                  theme="red"
                  variant="ghost"
                  @click="deleteActivity(i)"
                />
              </td>
            </tr>
          </tbody>
        </table>
        <div v-else class="py-10 text-center text-ink-gray-5">
          {{ __('No activities logged yet') }}
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
import { sessionStore } from '@/stores/session'
import {
  Avatar,
  Badge,
  Button,
  Dropdown,
  FeatherIcon,
  FormControl,
  createResource,
  call,
  toast,
} from 'frappe-ui'
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps({
  leadId: { type: String, required: true },
})

const router = useRouter()
const { statusOptions, getLeadStatus } = statusesStore()
const { user } = sessionStore()

const { document: lead } = useDocument('CRM Lead', props.leadId)
const doc = computed(() => lead.doc || {})

const showDeleteModal = ref(false)
const rightTab = ref('organisation')
const showForm = ref(false)

const activities = computed(() => doc.value.activity_log || [])

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

// --- Activity Log ---
const typeOptions = ['Referral', 'Proposal', 'Call', 'Meeting', 'Follow-up', 'Other'].map(
  (v) => ({ label: v, value: v }),
)
const statusOptionsList = ['Scheduled', 'Completed', 'Cancelled'].map((v) => ({
  label: v,
  value: v,
}))
const methodOptions = ['Call', 'Email', 'Meeting'].map((v) => ({ label: v, value: v }))

function today() {
  return new Date().toISOString().slice(0, 10)
}

const form = reactive(blankForm())

function blankForm() {
  return {
    activity_date: today(),
    activity_time: '',
    activity_type: '',
    activity_status: 'Scheduled',
    communication_method: '',
    performed_by: user,
    subject: '',
    notes: '',
  }
}

function addActivity() {
  if (!form.subject) {
    toast.error(__('Please add a subject'))
    return
  }
  lead.doc.activity_log = [...(lead.doc.activity_log || []), { ...form }]
  lead.save.submit(null, {
    onSuccess: () => {
      toast.success(__('Activity logged'))
      Object.assign(form, blankForm())
      showForm.value = false
    },
    onError: (e) => toast.error(e?.messages?.[0] || __('Could not save activity')),
  })
}

function deleteActivity(idx) {
  lead.doc.activity_log = activities.value.filter((_, i) => i !== idx)
  lead.save.submit(null, {
    onSuccess: () => toast.success(__('Activity deleted')),
    onError: (e) => toast.error(e?.messages?.[0] || __('Could not delete activity')),
  })
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

function formatDate(date) {
  if (!date) return '-'
  const [y, m, d] = String(date).split(' ')[0].split('-')
  return d && m && y ? `${d}-${m}-${y}` : date
}
</script>
