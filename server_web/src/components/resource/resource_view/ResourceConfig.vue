<script setup lang="ts">
import {ResourceItem} from "@/types/resource_type";
import {reactive, ref, watch, onMounted} from 'vue';
import {ElMessage} from "element-plus";
const props = defineProps({
  resourceId: {
    type: Number,
    default: 0,
    required: true
  },
})
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
      chunks: null
    }
);
const resourceViewerLoading = ref(false);
const currentRagRef = reactive({});
async function initResourceConfig() {

}
watch(
    () => props.resourceId,
    async (newResourceID) => {
      currentViewResource.id = newResourceID;
    },
    {
      immediate: true,
      deep: true
    }
);
defineExpose({
  initResourceConfig
});
</script>

<template>
  <el-scrollbar>
    <div v-loading="resourceViewerLoading" element-loading-text="加载中" style="height: 100%" class="chunk-main">
      <el-empty description="即将发布" ></el-empty>
    </div>
  </el-scrollbar>
</template>

<style scoped>
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
  justify-content: flex-start;
  align-items: flex-start;
}
.chunk-main {
  display: flex;
  flex-direction: column;
  padding: 6px;
  gap: 10px;
}
</style>