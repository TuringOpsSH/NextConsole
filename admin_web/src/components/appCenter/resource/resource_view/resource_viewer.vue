<script setup lang="ts">
import { ArrowRight } from '@element-plus/icons-vue';
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue';
import { show_resource_list } from '@/components/resource/resource_list/resource_list';
import {
  current_path_tree,
  current_view_resource,
  get_current_resource_object,
  get_parent_resource_list,
  resource_viewer_loading,
  view_code_resource_to_md
} from '@/components/resource/resource_view/resource_viewer';
import WebOfficeSDK from '@/components/global/wps/web-office-sdk-solution-v2.0.7.es.js';
import { getToken } from '@/utils/auth';
import { add_copy_button_event } from '@/components/next_console/messages_flow/message_flow';
import Resource_view_tree from '@/components/resource/resource_tree/resource_view_tree.vue';

const props = defineProps({
  resource_id: {
    type: String,
    default: '',
    required: false
  }
});
const wpsContainer = ref<HTMLDivElement | null>(null);
const wpsInstance = ref(null);
const currentFileId = computed(() => props.resource_id);
const isLoading = ref(false);
onMounted(async () => {
  if (props.resource_id) {
    try {
      isLoading.value = true;
      await get_current_resource_object(parseInt(props.resource_id));
      isLoading.value = false;
    } catch (e) {
      isLoading.value = false;
    }
    // 获取当前目录的父目录用于导航栏
    await initWPSInstance();
  }
});

onBeforeUnmount(() => {
  wpsInstance.value?.destroy();
});
watch(
  () => currentFileId.value,
  async () => {
    console.log('resource_id', props.resource_id);
    await initWPSInstance();
  }
);

async function initWPSInstance() {
  if (
    current_view_resource.resource_type == 'document' &&
    current_view_resource.resource_view_support &&
    !current_view_resource.resource_content
  ) {
    const token = getToken();
    if (!wpsContainer.value) {
      console.log('未实例化wps_app');
      return;
    }
    // 清空Wps容器
    wpsContainer.value.innerHTML = '';
    wpsInstance.value = WebOfficeSDK.init({
      officeType: get_wps_type(),
      appId: import.meta.env.VITE_APP_WPS_APP_ID,
      fileId: currentFileId.value,
      mount: wpsContainer.value,
      token: token
      // wordOptions: {
      //   isShowDocMap: false // 关闭默认大纲
      // }
    });
    await wpsInstance.value.ready().then(() => {
      // console.log('wps_app实例化成功');
      // // 动态创建右侧容器
      // const rightPanel = document.createElement('div');
      // rightPanel.style.cssText = 'position: fixed; right: 0; width: 300px; height: 100%;';
      // document.body.appendChild(rightPanel);
      // const app = wpsInstance.value.Application;

      // app.ActiveDocument.ActiveWindow.DocumentMap = true; // 启用大纲
      // rightPanel.appendChild(document.querySelector('.w-docmap-panel-wrapper'));
      const iframe: HTMLIFrameElement | null = document.querySelector('.web-office-iframe');
      console.log('🚀iframe', iframe);
      iframe.onload = () => {
        console.log('🚀', 'jiazai');
        const iframeDoc = iframe.contentDocument;
        const style = iframeDoc.createElement('style');
        style.textContent = `
    .web-office-docmap {
      right: 0 !important;
      left: auto !important;
      transform: translateX(0) !important;
    }
  `;
        iframeDoc.head.appendChild(style);
      };
    });
  } else {
    add_copy_button_event();
  }
}

function get_wps_type() {
  if (!current_view_resource.resource_format) {
    return '';
  }
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
    ].includes(current_view_resource.resource_format)
  ) {
    return WebOfficeSDK.OfficeType.Writer;
  }
  if (
    ['xls', 'xlt', 'et', 'ett', 'xlsx', 'xltx', 'xlsm', 'xltm', 'csv'].includes(current_view_resource.resource_format)
  ) {
    return WebOfficeSDK.OfficeType.Spreadsheet;
  }
  if (
    ['ppt', 'pptx', 'pptm', 'ppsx', 'ppsm', 'pps', 'potx', 'potm', 'dpt', 'dps', 'pot'].includes(
      current_view_resource.resource_format
    )
  ) {
    return WebOfficeSDK.OfficeType.Presentation;
  }
  if (['pdf', 'ofd'].includes(current_view_resource.resource_format)) {
    return WebOfficeSDK.OfficeType.Pdf;
  }
  if (current_view_resource.resource_format == 'otl') {
    return WebOfficeSDK.OfficeType.Otl;
  }
  if (current_view_resource.resource_format == 'dbt') {
    return WebOfficeSDK.OfficeType.Dbt;
  }
  return WebOfficeSDK.OfficeType.Writer;
}

const handleMouseEnter = (event, index) => {
  const target = event.target;
  current_path_tree.value[index].isOverflow = target.scrollWidth > target.clientWidth;
};
</script>

<template>
  <el-container class="resource-viewer-container">
    <el-header style="padding: 0 !important">
      <div id="resource_header_area">
        <div id="resource_header">
          <div id="resource_path">
            <el-breadcrumb
              :separator-icon="ArrowRight"
              style="display: flex; flex-direction: row; align-items: center; justify-content: flex-start"
            >
              <el-breadcrumb-item
                v-for="(item, index) in current_path_tree"
                :key="item.id"
                @click="show_resource_list(item)"
              >
                <el-tooltip :content="item.resource_name" effect="light" :disabled="!item.isOverflow">
                  <el-text
                    truncated
                    class="resource-sub-path"
                    :class="{
                      'resource-sub-path-last': index == current_path_tree?.length - 1
                    }"
                    @mouseenter="handleMouseEnter($event, index)"
                  >
                    {{ item?.resource_name }}
                  </el-text>
                </el-tooltip>
              </el-breadcrumb-item>
            </el-breadcrumb>
          </div>
        </div>
      </div>
    </el-header>
    <el-main style="padding: 0 !important">
      <div id="resource_view_main" v-loading="isLoading" element-loading-text="加载中">
        <el-scrollbar style="width: 100%">
          <div v-if="current_view_resource?.resource_view_support">
            <div v-if="current_view_resource?.resource_content?.length" class="view-area">
              <div v-html="view_code_resource_to_md()" style="width: 100%" />
            </div>
            <div v-else>
              <div v-if="current_view_resource.resource_type == 'image'" class="view-area">
                <div class="std-middle-box">
                  <el-image :src="current_view_resource.resource_show_url" />
                </div>
              </div>
              <div v-else-if="current_view_resource.resource_type == 'video'" class="view-area">
                <div style="width: 100%; height: 100%" class="std-middle-box">
                  <video controls width="600">
                    <source :src="current_view_resource.resource_show_url" type="video/mp4" />
                    <source :src="current_view_resource.resource_show_url" type="video/webm" />
                    <source :src="current_view_resource.resource_show_url" type="video/ogg" />
                    Your browser does not support the video tag.
                  </video>
                </div>
              </div>
              <div v-else-if="current_view_resource.resource_type == 'audio'" class="view-area">
                <div style="width: 100%; height: 100%" class="std-middle-box">
                  <audio controls>
                    <source :src="current_view_resource.resource_show_url" type="audio/mpeg" />
                    <source :src="current_view_resource.resource_show_url" type="audio/ogg" />
                    <source :src="current_view_resource.resource_show_url" type="audio/wav" />
                    <source :src="current_view_resource.resource_show_url" type="audio/mp4" />
                    <source :src="current_view_resource.resource_show_url" type="audio/x-m4a" />
                    Your browser does not support the video tag.
                  </audio>
                </div>
              </div>
              <div v-else-if="current_view_resource.resource_type == 'code'" class="view-area">
                <div style="padding: 16px" class="std-middle-box">
                  <div v-html="view_code_resource_to_md()" style="width: 100%" />
                </div>
              </div>
              <div v-else-if="current_view_resource.resource_type == 'webpage'" class="view-area">
                <div style="padding: 16px" class="std-middle-box">
                  <div v-html="view_code_resource_to_md()" style="width: 100%" />
                </div>
              </div>
              <div v-else-if="current_view_resource.resource_type == 'document'" class="view-area mydocument">
                <div id="WPS_APP" ref="wpsContainer" />
              </div>
            </div>
          </div>
          <div v-else-if="resource_viewer_loading">
            <el-result icon="info" title="文件加载中" />
          </div>
          <div v-else class="view-area">
            <el-result
              v-show="!isLoading"
              icon="info"
              title="此文件暂不支持在线查看"
              sub-title="Sorry, This file does not currently support online viewing"
            />
          </div>
        </el-scrollbar>
      </div>
    </el-main>
    <el-footer height="48px" style="padding: 0 !important; background-color: #f9fafb"> </el-footer>
  </el-container>
  <resource_view_tree />
</template>

<style scoped lang="scss">
#resource_header_area {
  display: flex;
  flex-direction: column;
  width: 100%;

  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.1);
}
#resource_header {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  height: 24px;
}
#resource_path {
  display: flex;
  flex-direction: row;
  align-items: center;
  padding: 0 16px;
  width: calc(100% - 32px);
}
.resource-sub-path {
  cursor: pointer;
  font-size: 14px;
  max-width: 250px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.resource-sub-path:hover {
  color: #8ec5fc;
}
.resource-sub-path-last {
  font-weight: 600;
  font-size: 16px;
  line-height: 24px;
  color: #101828;
}
#resource_view_main {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 108px);
  flex: 1;
}
.std-middle-box {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  height: 100%;
  width: 100%;
}
.view-area {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  padding: 16px;
}
#WPS_APP {
  display: flex;
  flex: 1;
  align-items: center;
  justify-content: center;
  height: calc(100vh - 140px);
  width: 100%;
}
@media (width < 768px) {
  .resource-sub-path {
    cursor: pointer;
    font-size: 12px;
  }
  .resource-sub-path-last {
    font-weight: 600;
    font-size: 12px;
    line-height: 14px;
    color: #101828;
    cursor: default;
  }
}
</style>
<style>
#WPS_APP iframe {
  width: 100% !important;
  height: 100% !important;
  border: none;
}
.w-docmap-panel-wrapper {
  order: 2; /* 在flex布局中调整顺序 */
  right: 0 !important;
  left: auto !important;
}
</style>
