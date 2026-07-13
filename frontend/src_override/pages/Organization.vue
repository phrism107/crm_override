<template>
  <LayoutHeader v-if="organization.doc">
    <template #left-header>
      <Breadcrumbs :items="breadcrumbs">
        <template #prefix="{ item }">
          <Icon v-if="item.icon" :icon="item.icon" class="mr-2 h-4" />
        </template>
      </Breadcrumbs>
    </template>
    <template #right-header>
      <CustomActions
        v-if="organization._actions?.length"
        :actions="organization._actions"
      />
    </template>
  </LayoutHeader>
  <div v-if="organization.doc" ref="parentRef" class="flex h-full">
    <Resizer
      v-if="organization.doc"
      :parent="$refs.parentRef"
      class="flex h-full flex-col overflow-hidden border-r"
    >
      <div class="border-b">
        <FileUploader
          :validateFile="validateIsImageFile"
          @success="changeOrganizationImage"
        >
          <template #default="{ openFileSelector, error }">
            <div class="flex flex-col items-start justify-start gap-4 p-5">
              <div class="flex gap-4 items-center">
                <div class="group relative h-15.5 w-15.5">
                  <Avatar
                    size="3xl"
                    class="h-15.5 w-15.5"
                    :label="organization.doc.organization_name"
                    :image="organization.doc.organization_logo"
                  />
                  <component
                    :is="organization.doc.organization_logo ? Dropdown : 'div'"
                    v-bind="
                      organization.doc.organization_logo
                        ? {
                            options: [
                              {
                                icon: 'upload',
                                label: organization.doc.organization_logo
                                  ? __('Change Image')
                                  : __('Upload Image'),
                                onClick: openFileSelector,
                              },
                              {
                                icon: 'trash-2',
                                label: __('Remove Image'),
                                onClick: () => changeOrganizationImage(''),
                              },
                            ],
                          }
                        : { onClick: openFileSelector }
                    "
                    class="!absolute bottom-0 left-0 right-0"
                  >
                    <div
                      class="z-1 absolute bottom-0 left-0 right-0 flex h-14 cursor-pointer items-center justify-center rounded-b-full bg-black bg-opacity-40 pt-5 opacity-0 duration-300 ease-in-out group-hover:opacity-100"
                      style="
                        -webkit-clip-path: inset(22px 0 0 0);
                        clip-path: inset(22px 0 0 0);
                      "
                    >
                      <CameraIcon class="h-6 w-6 cursor-pointer text-white" />
                    </div>
                  </component>
                </div>
                <div class="flex flex-col gap-2 truncate">
                  <div class="truncate text-2xl font-medium text-ink-gray-9">
                    <span>{{ organization.doc.name }}</span>
                  </div>
                  <div
                    v-if="organization.doc.website"
                    class="flex items-center gap-1.5 text-base text-ink-gray-8"
                  >
                    <WebsiteIcon class="size-4" />
                    <span>{{ website(organization.doc.website) }}</span>
                  </div>
                  <ErrorMessage :message="__(error)" />
                </div>
              </div>
              <div class="flex gap-1.5">
                <Button
                  v-if="canDelete"
                  :label="__('Delete')"
                  theme="red"
                  size="sm"
                  iconLeft="trash-2"
                  @click="deleteOrganization()"
                />
                <Button
                  :tooltip="__('Open Website')"
                  icon="link"
                  @click="openWebsite"
                />
              </div>
            </div>
          </template>
        </FileUploader>
      </div>
      <div
        v-if="sections.data"
        class="flex flex-1 flex-col justify-between overflow-hidden"
      >
        <SidePanelLayout
          :sections="sections.data"
          doctype="CRM Organization"
          :docname="organization.doc.name"
          @reload="sections.reload"
          @beforeFieldChange="beforeFieldChange"
        />
      </div>
    </Resizer>
    <Tabs
      v-model="tabIndex"
      as="div"
      :tabs="tabs"
      class="flex flex-1 overflow-hidden flex-col [&_[role='tablist']]:gap-7.5 [&_[role='tablist']]:px-5 [&_[role='tablist']::-webkit-scrollbar]:h-0 [&_[role='tablist']]:min-h-[45px] [&_[role='tabpanel']:not([hidden])]:flex [&_[role='tabpanel']:not([hidden])]:grow"
    >
      <template #tab-item="{ tab, selected }">
        <button
          class="group flex items-center gap-2 border-b border-transparent py-2.5 text-base text-ink-gray-5 duration-300 ease-in-out hover:text-ink-gray-9"
          :class="{ 'text-ink-gray-9': selected }"
        >
          <component :is="tab.icon" v-if="tab.icon" class="h-5" />
          {{ __(tab.label) }}
          <Badge
            class="group-hover:bg-surface-gray-7"
            :class="[selected ? 'bg-surface-gray-7' : 'bg-gray-600']"
            variant="solid"
            theme="gray"
            size="sm"
          >
            {{ tab.count }}
          </Badge>
        </button>
      </template>
      <template #tab-panel="{ tab }">
        <div v-if="rows.length" class="flex-1 overflow-auto px-5">
          <table class="w-full text-base">
            <thead>
              <tr class="border-b text-ink-gray-5 text-sm">
                <th
                  v-for="col in tab.columns"
                  :key="col.key"
                  class="py-2.5 pr-4 text-left font-normal"
                >
                  {{ __(col.label) }}
                </th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="row in rows"
                :key="row.name"
                class="border-b text-ink-gray-8"
                :class="tab.route ? 'cursor-pointer hover:bg-surface-gray-1' : ''"
                @click="tab.route && openRecord(tab, row.name)"
              >
                <td
                  v-for="(col, i) in tab.columns"
                  :key="col.key"
                  class="py-3 pr-4"
                  :class="i === 0 ? 'font-medium text-ink-gray-9' : ''"
                >
                  {{ row[col.key] || '-' }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <EmptyState v-else :icon="tab.icon" :name="__(tab.label)" />
      </template>
    </Tabs>
  </div>
  <ErrorPage
    v-else-if="errorTitle"
    :errorTitle="errorTitle"
    :errorMessage="errorMessage"
  />
  <DeleteLinkedDocModal
    v-if="showDeleteLinkedDocModal"
    v-model="showDeleteLinkedDocModal"
    :doctype="'CRM Organization'"
    :docname="props.organizationId"
    name="Organizations"
  />
</template>

<script setup>
import ErrorPage from '@/components/ErrorPage.vue'
import Resizer from '@/components/Resizer.vue'
import SidePanelLayout from '@/components/SidePanelLayout.vue'
import Icon from '@/components/Icon.vue'
import LayoutHeader from '@/components/LayoutHeader.vue'
import EmptyState from '@/components/ListViews/EmptyState.vue'
import WebsiteIcon from '@/components/Icons/WebsiteIcon.vue'
import CameraIcon from '@/components/Icons/CameraIcon.vue'
import DealsIcon from '@/components/Icons/DealsIcon.vue'
import ContactsIcon from '@/components/Icons/ContactsIcon.vue'
import PhoneIcon from '@/components/Icons/PhoneIcon.vue'
import LeadsIcon from '@/components/Icons/LeadsIcon.vue'
import DeleteLinkedDocModal from '@/components/DeleteLinkedDocModal.vue'
import CustomActions from '@/components/CustomActions.vue'
import { useDocument } from '@/data/document'
import { getSettings } from '@/stores/settings'
import { globalStore } from '@/stores/global'
import { getMeta } from '@/stores/meta'
import { usersStore } from '@/stores/users'
import { statusesStore } from '@/stores/statuses'
import { getView } from '@/utils/view'
import {
  validateIsImageFile,
  setupCustomizations,
  openWebsite as openExternalWebsite,
} from '@/utils'
import {
  Breadcrumbs,
  Avatar,
  FileUploader,
  Dropdown,
  Tabs,
  createListResource,
  usePageMeta,
  createResource,
  toast,
  call,
} from 'frappe-ui'
import { useDoctypeModal } from '@/composables/doctypeModal'
import { useTelemetry } from 'frappe-ui/frappe'
import { computed, ref, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const props = defineProps({
  organizationId: { type: String, required: true },
})

const { brand } = getSettings()
const { $dialog, $socket } = globalStore()
const { getUser } = usersStore()
const { getDealStatus } = statusesStore()
const { doctypeMeta } = getMeta('CRM Organization')
const { capture } = useTelemetry()

const route = useRoute()
const router = useRouter()

const errorTitle = ref('')
const errorMessage = ref('')

const showDeleteLinkedDocModal = ref(false)

const {
  document: organization,
  permissions,
  scripts,
  triggerOnRender,
} = useDocument('CRM Organization', props.organizationId)

const canDelete = computed(() => permissions.data?.permissions?.delete || false)

onMounted(async () => {
  if (organization.doc) await triggerOnRender()
})

const breadcrumbs = computed(() => {
  let items = [{ label: __('Organizations'), route: { name: 'Organizations' } }]

  if (route.query.view || route.query.viewType) {
    let view = getView(
      route.query.view,
      route.query.viewType,
      'CRM Organization',
    )
    if (view) {
      items.push({
        label: __(view.label),
        icon: view.icon,
        route: {
          name: 'Organizations',
          params: { viewType: route.query.viewType },
          query: { view: route.query.view },
        },
      })
    }
  }

  items.push({
    label: title.value,
    route: {
      name: 'Organization',
      params: { organizationId: props.organizationId },
    },
  })
  return items
})

const title = computed(() => {
  let t = doctypeMeta.value?.title_field || 'name'
  return organization.doc?.[t] || props.organizationId
})

usePageMeta(() => {
  return {
    title: title.value,
    icon: brand.favicon,
  }
})

async function deleteOrganization() {
  showDeleteLinkedDocModal.value = true
}

function changeOrganizationImage(file) {
  organization.setValue.submit({
    organization_logo: file?.file_url || null,
  })
}

function beforeFieldChange(data) {
  if (Object.hasOwn(data ?? {}, 'organization_name')) {
    call('frappe.client.rename_doc', {
      doctype: 'CRM Organization',
      old_name: props.organizationId,
      new_name: data.organization_name,
    }).then(() => {
      router.push({
        name: 'Organization',
        params: { organizationId: data.organization_name },
      })
    })
  } else {
    organization.save.submit()
  }
}

function website(url) {
  return url && url.replace(/^(?:https?:\/\/)?(?:www\.)?/i, '')
}

function openWebsite() {
  if (!organization.doc.website) {
    toast.error(__('No Website Found'))
    return
  }

  openExternalWebsite(organization.doc.website)
}

const sections = createResource({
  url: 'crm.fcrm.doctype.crm_fields_layout.crm_fields_layout.get_sidepanel_sections',
  cache: ['sidePanelSections', 'CRM Organization'],
  params: { doctype: 'CRM Organization' },
  auto: true,
  transform: (data) => getParsedSections(data),
})

function getParsedSections(_sections) {
  return _sections.map((section) => {
    section.columns = section.columns.map((column) => {
      column.fields = column.fields.map((field) => {
        if (field.fieldname === 'address') {
          return {
            ...field,
            create: (value, close) => {
              showAddressModal()
              close()
            },
            edit: (address) => showAddressModal(address),
          }
        } else {
          return field
        }
      })
      return column
    })
    return section
  })
}

// ---------------------------------------------------------------------------
// PHRISM: related tabs -> Projects, Contacts, Interactions, Leads
// ---------------------------------------------------------------------------
function formatDate(date) {
  if (!date) return ''
  const [y, m, d] = String(date).split(' ')[0].split('-')
  return d && m && y ? `${d}-${m}-${y}` : date
}

const projects = createListResource({
  type: 'list',
  doctype: 'CRM Deal',
  cache: ['org-projects', props.organizationId],
  fields: [
    'name',
    'project_title',
    'organization_name',
    'engagement_type',
    'status',
    'engagement_start_date',
  ],
  filters: { organization: props.organizationId },
  orderBy: 'modified desc',
  pageLength: 50,
  auto: true,
})

const contacts = createListResource({
  type: 'list',
  doctype: 'Contact',
  cache: ['org-contacts', props.organizationId],
  fields: ['name', 'full_name', 'email_id', 'mobile_no'],
  filters: { company_name: props.organizationId },
  orderBy: 'modified desc',
  pageLength: 50,
  auto: true,
})

const interactions = createListResource({
  type: 'list',
  doctype: 'CRM Interaction',
  cache: ['org-interactions', props.organizationId],
  fields: [
    'name',
    'subject',
    'interaction_type',
    'source',
    'contact_name',
    'interaction_date',
  ],
  filters: { organization: props.organizationId },
  orderBy: 'interaction_date desc',
  pageLength: 50,
  auto: true,
})

const leads = createListResource({
  type: 'list',
  doctype: 'CRM Lead',
  cache: ['org-leads', props.organizationId],
  fields: ['name', 'lead_name', 'status', 'source', 'lead_received_date'],
  filters: { organization: props.organizationId },
  orderBy: 'modified desc',
  pageLength: 50,
  auto: true,
})

const tabIndex = ref(0)
const tabs = [
  {
    label: 'Projects',
    icon: DealsIcon,
    route: 'Deal',
    resource: projects,
    count: computed(() => projects.data?.length || 0),
    columns: [
      { label: 'Project Name', key: 'project_title' },
      { label: 'Engagement Type', key: 'engagement_type' },
      { label: 'Status', key: 'status' },
      { label: 'Engagement Start Date', key: 'engagement_start_date' },
    ],
    transform: (d) => ({
      name: d.name,
      project_title: d.project_title || d.organization_name || d.name,
      engagement_type: d.engagement_type,
      status: d.status,
      engagement_start_date: formatDate(d.engagement_start_date),
    }),
  },
  {
    label: 'Contacts',
    icon: ContactsIcon,
    route: 'Contact',
    resource: contacts,
    count: computed(() => contacts.data?.length || 0),
    columns: [
      { label: 'Name', key: 'full_name' },
      { label: 'Email', key: 'email_id' },
      { label: 'Phone', key: 'mobile_no' },
    ],
    transform: (c) => ({
      name: c.name,
      full_name: c.full_name,
      email_id: c.email_id,
      mobile_no: c.mobile_no,
    }),
  },
  {
    label: 'Interactions',
    icon: PhoneIcon,
    route: null,
    resource: interactions,
    count: computed(() => interactions.data?.length || 0),
    columns: [
      { label: 'Subject', key: 'subject' },
      { label: 'Type', key: 'interaction_type' },
      { label: 'Source', key: 'source' },
      { label: 'Contact', key: 'contact_name' },
      { label: 'Date', key: 'interaction_date' },
    ],
    transform: (i) => ({
      name: i.name,
      subject: i.subject,
      interaction_type: i.interaction_type,
      source: i.source,
      contact_name: i.contact_name,
      interaction_date: formatDate(i.interaction_date),
    }),
  },
  {
    label: 'Leads',
    icon: LeadsIcon,
    route: 'Lead',
    resource: leads,
    count: computed(() => leads.data?.length || 0),
    columns: [
      { label: 'Name', key: 'lead_name' },
      { label: 'Status', key: 'status' },
      { label: 'Source', key: 'source' },
      { label: 'Lead Received', key: 'lead_received_date' },
    ],
    transform: (l) => ({
      name: l.name,
      lead_name: l.lead_name,
      status: l.status,
      source: l.source,
      lead_received_date: formatDate(l.lead_received_date),
    }),
  },
]

const rows = computed(() => {
  const tab = tabs[tabIndex.value]
  const data = tab.resource.data || []
  return data.map(tab.transform)
})

function openRecord(tab, name) {
  if (!tab.route) return
  const paramKey =
    tab.route === 'Deal'
      ? 'dealId'
      : tab.route === 'Contact'
        ? 'contactId'
        : 'leadId'
  router.push({ name: tab.route, params: { [paramKey]: name } })
}

const { showModal } = useDoctypeModal()

function showAddressModal(_address) {
  showModal({
    name: _address || null,
    doctype: 'Address',
    callbacks: {
      afterInsert: (d) => {
        capture('address_created')
        organization.doc.address = d.name
        organization.save.submit()
      },
    },
  })
}

// Setup custom actions from Form Scripts
watch(
  () => organization.doc,
  async (_doc) => {
    if (scripts.data?.length) {
      let s = await setupCustomizations(scripts.data, {
        doc: _doc,
        $dialog,
        $socket,
        router,
        toast,
        updateField: organization.setValue.submit,
        createToast: toast.create,
        deleteDoc: deleteOrganization,
        call,
      })
      organization._actions = s.actions || []
    }
  },
  { once: true },
)
</script>
