<script setup lang="ts">
import { onBeforeUnmount, reactive, ref, watch } from 'vue';
import WebOfficeSDK from '@/components/global/wps/web-office-sdk-solution-v2.0.7.es.js';
import { useUserInfoStore } from '@/stores/userInfoStore';

const props = defineProps({
  appId: {
    type: String,
    default: '',
    required: false
  },
  resourceId: {
    type: Number,
    default: 0,
    required: true
  },
  resourceFormat: {
    type: String,
    default: '',
    required: false
  }
});
const userInfoStore = useUserInfoStore();
const localAppId = ref('');
const localResourceId = ref();
const localResourceFormat = ref();
const WPSInstance = ref(null);
const wpsContainer = ref<HTMLDivElement | null>(null);

function getWpsType() {
  if (
    [
      'doc',
      'dot',
      'wps',
      'wpt',
      'docx',
      'dotx',
      'docm',
      'dotm',
      'rtf',
      'txt',
      'xml',
      'mhtml',
      'mht',
      'html',
      'htm',
      'uof',
      'uot3'
    ].includes(localResourceFormat.value)
  ) {
    return WebOfficeSDK.OfficeType.Writer;
  }
  if (['xls', 'xlt', 'et', 'ett', 'xlsx', 'xltx', 'xlsm', 'xltm', 'csv'].includes(localResourceFormat.value)) {
    return WebOfficeSDK.OfficeType.Spreadsheet;
  }
  if (
    ['ppt', 'pptx', 'pptm', 'ppsx', 'ppsm', 'pps', 'potx', 'potm', 'dpt', 'dps', 'pot'].includes(
      localResourceFormat.value
    )
  ) {
    return WebOfficeSDK.OfficeType.Presentation;
  }
  if (['pdf', 'ofd'].includes(localResourceFormat.value)) {
    return WebOfficeSDK.OfficeType.Pdf;
  }
  if (localResourceFormat.value == 'otl') {
    return WebOfficeSDK.OfficeType.Otl;
  }
  if (localResourceFormat.value == 'dbt') {
    return WebOfficeSDK.OfficeType.Dbt;
  }
  return WebOfficeSDK.OfficeType.Writer;
}
async function initWpsDoc() {
  // 启用wps 进行渲染
  // @ts-ignore
  const officeType = getWpsType();
  console.log('officeType', localResourceFormat.value, localAppId.value, localResourceId.value);
  WPSInstance.value = WebOfficeSDK.init({
    officeType: officeType,
    appId: localAppId.value,
    fileId: localResourceId.value,
    mount: document.querySelector('#WPS_APP'),
    token: userInfoStore.token
  });
  await WPSInstance.value.ready();
  WPSInstance.value.iframe.style.width = '100vw';
}

watch(
  () => props.resourceId,
  async newResourceID => {
    localResourceId.value = newResourceID;
  },
  {
    immediate: true,
    deep: true
  }
);
watch(
  () => props.appId,
  async newAppID => {
    localAppId.value = newAppID;
  },
  {
    immediate: true,
    deep: true
  }
);
watch(
  () => props.resourceFormat,
  async newResourceFormat => {
    localResourceFormat.value = newResourceFormat.toLowerCase();
  },
  {
    immediate: true,
    deep: true
  }
);
onBeforeUnmount(() => {
  WPSInstance.value?.destroy();
});
defineExpose({
  initWpsDoc
});
</script>

<template>
  <el-scrollbar>
    <div>
      <div id="WPS_APP" ref="wpsContainer" />
    </div>
  </el-scrollbar>
</template>

<style scoped>
.view-area {
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: flex-start;
  height: 100%;
}
#WPS_APP {
  display: flex;
  flex: 1;
  align-items: center;
  justify-content: center;
  height: calc(100vh - 170px);
  width: 100%;
}
#WPS_APP iframe {
  width: 100% !important;
  height: 100% !important;
  border: none;
}
</style>
