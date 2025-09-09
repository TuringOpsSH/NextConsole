<template>
  <div v-if="resourceEditorLoading" v-loading="resourceEditorLoading" element-loading-text="加载中..." />
  <div v-else-if="currentViewResource?.edit_config?.engine == 'tiptap'">
    <TipTapEditor />
  </div>
  <div v-else-if="currentViewResource?.edit_config?.engine == 'wps'">
    <WpsEditor
      ref="wpsRef"
      :app-id="currentViewResource?.edit_config?.wps_config?.wps_app_id"
      :resource-id="currentViewResource?.id"
      :resource-format="currentViewResource?.resource_format"
    />
  </div>
  <div v-else class="unsupported-editor">
    <div class="unsupported-container">
      <div class="unsupported-icon">
        <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path
            d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.716-2.833L13.716 4.83c-.786-1.167-2.472-1.167-3.258 0L4.226 16.167c-.786 1.166.176 2.833 1.716 2.833z"
          />
        </svg>
      </div>
      <h3 class="unsupported-title">暂不支持在线编辑</h3>
      <p class="unsupported-message">当前文件格式不支持在线编辑功能</p>
      <div class="unsupported-actions">
        <button class="download-btn" @click="handleDownload">下载文件</button>
        <button class="back-btn" @click="handleBack">返回上一页</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ElMessage } from 'element-plus';
import { reactive, watch, ref } from 'vue';
import {
  download_resource_object as downloadResourceObject,
  resource_view_meta_get as resourceViewMetaGet
} from '@/api/resource-api';
import { clientFingerprint, getFingerPrint } from '@/components/global/web_socket';
import TipTapEditor from '@/components/resource/resource-view/TipTapEditor.vue';
import WpsEditor from '@/components/resource/resource-view/WpsEditor.vue';
import { ResourceItem } from '@/types/resource-type';
const props = defineProps({
  resourceId: {
    type: Number,
    default: 0,
    required: true
  }
});
const currentViewResource = reactive<ResourceItem>(
  // @ts-ignore
  {
    sub_rag_file_cnt: 0,
    id: null,
    resource_parent_id: null,
    user_id: null,
    resource_name: null,
    resource_type: null,
    resource_desc: null,
    resource_icon: null,
    resource_format: null,
    resource_path: null,
    // eslint-disable-next-line @typescript-eslint/naming-convention
    resource_size_in_MB: null,
    resource_status: null,
    rag_status: null,
    create_time: null,
    update_time: null,
    delete_time: null,
    show_buttons: null,
    resource_parent_name: null,
    resource_is_selected: null,
    sub_resource_dir_cnt: null,
    sub_resource_file_cnt: null,
    resource_feature_code: '',
    resource_is_supported: false,
    resource_show_url: '',
    resource_source_url: '',
    resource_title: '',
    resource_source: 'resource_center',
    ref_text: null,
    rerank_score: null,
    view_config: {},
    edit_config: {}
  }
);
const resourceEditorLoading = ref(false);
const wpsRef = ref(null);
async function getCurrentResourceObject() {
  if (!clientFingerprint.value) {
    await getFingerPrint();
  }
  let params = {
    resource_id: currentViewResource.id,
    clientFingerprint: clientFingerprint.value
  };
  resourceEditorLoading.value = true;
  let res = await resourceViewMetaGet(params);
  if (!res.error_status) {
    Object.assign(currentViewResource, res.result);
  }
  resourceEditorLoading.value = false;
}
// 处理下载操作
async function handleDownload() {
  let params = {
    resource_id: currentViewResource.id
  };
  let res = await downloadResourceObject(params);
  if (!res.error_status) {
    let downloadUrl = res.result?.download_url;
    if (!downloadUrl) {
      ElMessage.error('下载链接为空');
      return;
    }
    downloadUrl = downloadUrl + '?filename=' + encodeURIComponent(currentViewResource.resource_name);
    // 创建一个隐藏的 <a> 标签
    const link = document.createElement('a');
    link.href = downloadUrl;
    link.download = currentViewResource.resource_name; // 设置下载文件的名称
    link.style.display = 'none';

    // 将 <a> 标签添加到文档中
    document.body.appendChild(link);

    // 触发点击事件
    link.click();

    // 移除 <a> 标签
    document.body.removeChild(link);
  }
}

// 处理返回操作
function handleBack() {
  // 这里可以添加返回上一页的逻辑
  window.history.back();
}

async function initResourceEditor() {
  await getCurrentResourceObject();
  console.log(currentViewResource);
  if (currentViewResource.edit_config?.engine == 'wps') {
    await wpsRef.value?.initWpsDoc();
  } else {
    console.warn('当前文件类型不支持在线编辑');
  }
}
watch(
  () => props.resourceId,
  async newResourceID => {
    currentViewResource.id = newResourceID;
  },
  {
    immediate: true,
    deep: true
  }
);
defineExpose({
  initResourceEditor
});
</script>

<style scoped>
.unsupported-editor {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
  padding: 40px 20px;
}

.unsupported-container {
  text-align: center;
  max-width: 400px;
}

.unsupported-icon {
  color: #ff6b6b;
  margin-bottom: 24px;
}

.unsupported-icon svg {
  stroke-width: 2;
}

.unsupported-title {
  font-size: 24px;
  font-weight: 600;
  color: #2d3748;
  margin-bottom: 12px;
}

.unsupported-message {
  color: #718096;
  font-size: 16px;
  line-height: 1.5;
  margin-bottom: 32px;
}

.unsupported-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
}

.download-btn {
  padding: 12px 24px;
  background-color: #4299e1;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s;
}

.download-btn:hover {
  background-color: #3182ce;
}

.back-btn {
  padding: 12px 24px;
  background-color: #e2e8f0;
  color: #4a5568;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s;
}

.back-btn:hover {
  background-color: #cbd5e0;
}

/* 响应式设计 */
@media (max-width: 480px) {
  .unsupported-actions {
    flex-direction: column;
  }

  .unsupported-title {
    font-size: 20px;
  }

  .unsupported-message {
    font-size: 14px;
  }
}
</style>
