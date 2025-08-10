<script setup lang="ts">
import {ArrowRight} from '@element-plus/icons-vue';
import {ref, watch, onMounted} from 'vue';
import {show_resource_list} from '@/components/resource/resource_list/resource_list';
import {currentPathTree,} from '@/components/resource/resource_view/resource_viewer';
import Resource_view_tree from '@/components/resource/resource_tree/resource_view_tree.vue';
import 'vue-json-pretty/lib/styles.css';
import {get_resource_object_path} from "@/api/resource_api";


import router from "@/router";
import ResourcePreviewer from "@/components/resource/resource_view/ResourcePreviewer.vue";
import ResourceEditor from "@/components/resource/resource_view/ResourceEditor.vue";
import ResourceParser from "@/components/resource/resource_view/ResourceParser.vue";
import ResourceChunker from "@/components/resource/resource_view/ResourceChunker.vue";
import ResourceConfig from "@/components/resource/resource_view/ResourceConfig.vue";
const props = defineProps({
  resource_id: {
    type: String,
    default: '',
    required: false
  },
  pane: {
    type: String,
    default: 'preview',
    required: false
  }
});
const currentPane = ref(props.pane);
const currentResourceId = ref();
const resourcePreviewRef = ref(null);
const resourceParserRef = ref(null);
const resourceEditorRef = ref(null);
const resourceChunkerRef = ref(null);
const resourceIndexRef = ref(null);
async function getParentResourceList() {
  if (!currentResourceId.value) {
    currentPathTree.value = [];
    return;
  }
  let params = {
    resource_id: currentResourceId.value
  };
  let res = await get_resource_object_path(params);
  if (!res.error_status) {
    currentPathTree.value = res.result.data;
  }
}
const handleMouseEnter = (event, index) => {
  const target = event.target;
  currentPathTree.value[index].isOverflow = target.scrollWidth > target.clientWidth;
};
async function handlePaneChange(newPane:string) {
  if (newPane == 'preview') {
    await resourcePreviewRef.value?.initResourceViewer();
  } else if (newPane == 'parse') {
    await resourceParserRef.value?.initResourceParser();
  } else if (newPane == 'chunk') {
    await resourceChunkerRef.value?.initResourceIndexer();
  } else if (newPane == 'config') {
    await resourceIndexRef.value?.initResourceConfig();
  }
  router.replace({
    params: {
      ...router.currentRoute.value.params,
    },
    query: {
      ...router.currentRoute.value.query,
      pane: newPane
    }
  })
}
watch(
    () => props.resource_id,
    async (newResourceID) => {
      currentResourceId.value = parseInt(newResourceID);
      getParentResourceList()
    },
    {
      immediate: true,
      deep: true
    }
);
onMounted(() => {
  currentResourceId.value = parseInt(props.resource_id);
  getParentResourceList();
  handlePaneChange(currentPane.value);
});
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
                v-for="(item, index) in currentPathTree"
                :key="item.id"
                @click="show_resource_list(item)"
              >
                <el-tooltip :content="item.resource_name" effect="light" :disabled="!item.isOverflow">
                  <el-text
                    truncated
                    class="resource-sub-path"
                    :class="{
                      'resource-sub-path-last': index == currentPathTree?.length - 1
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
      <el-scrollbar>
        <div class="resource_view_main" >
          <el-tabs v-model="currentPane" type="border-card" style="height: 100%" @tab-change="handlePaneChange">
            <el-tab-pane name="preview" label="预览" style="height: 100%">
              <ResourcePreviewer :resource-id="currentResourceId" ref="resourcePreviewRef"/>
            </el-tab-pane>
            <el-tab-pane name="editor" label="编辑" disabled>
              <ResourceEditor resource-id="" ref="resourceEditorRef"/>
            </el-tab-pane>
            <el-tab-pane name="config" label="配置" style="height: 100%">
              <ResourceConfig :resource-id="currentResourceId" ref="resourceConfigRef"/>
            </el-tab-pane>
            <el-tab-pane name="parse" label="解析" style="height: 100%">
              <ResourceParser :resource-id="currentResourceId" ref="resourceParserRef"/>
            </el-tab-pane>
            <el-tab-pane name="chunk" label="分段" style="height: 100%">
              <ResourceChunker :resource-id="currentResourceId" ref="resourceChunkerRef"/>
            </el-tab-pane>
          </el-tabs>
        </div>
      </el-scrollbar>
    </el-main>
    <el-footer height="48px" style="padding: 0 !important; background-color: #f9fafb" />
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
  font-size: 16px;
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
.resource_view_main {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 100px);
  padding: 0 16px;
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
  justify-content: flex-start;
  align-items: flex-start;
  padding: 4px;
  height: calc(100vh - 120px);
}
#WPS_APP {
  display: flex;
  flex: 1;
  align-items: center;
  justify-content: center;
  height: calc(100vh - 140px);
  width: 100%;
}
#WPS_APP iframe {
  width: 100% !important;
  height: 100% !important;
  border: none;
}
.text-area {
  border-radius: 8px;
  border: 1px solid #e4e7ed;
  background-color: #ffffff;
  word-break: break-word;
  &:hover {
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  }
}
/* 增强表格样式 */
.excel-table table {
  border-collapse: collapse;
  width: 100%;
}
.excel-table td, .excel-table th {
  border: 1px solid #ddd;
  padding: 8px;
}
.excel-table th {
  background-color: #f2f2f2;
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
