<script setup lang="ts">
import { useSessionStorage } from '@vueuse/core';
import { ElMessage } from 'element-plus';
import { inject, Ref, ref, watch } from 'vue';
import {
  current_row_item,
  download_resource,
  mousePosition,
  preview_share_resource,
  resource_share_context_menu_flag
} from '@/components/resource/resource-share/context_menu/context-menu';
import { turn_on_share_selector } from '@/components/resource/resource-share-selector/resource_share_selector';
import router from '@/router';
import { TResourceListStatus } from '@/types/resource-type';

const props = defineProps({
  resourceId: {
    required: true,
    type: Number || null || String
  }
});
const currentResourceID = ref(0);

const isMultipleSelection = inject<Ref<boolean>>('isMultipleSelection');
function switchResourceLayout() {
  //   search_all_resource_share_object();
  const shareListStatus = useSessionStorage<TResourceListStatus>('shareListStatus', 'card');
  if (shareListStatus.value === 'list') {
    shareListStatus.value = 'card';
  } else {
    shareListStatus.value = 'list';
  }
  // 更新至url
  router.push({
    params: { ...router.currentRoute.value.params },
    query: {
      ...router.currentRoute.value.query,
      view_model: shareListStatus.value
    }
  });
}
async function shareResource() {
  if (!current_row_item?.id) {
    ElMessage.warning('资源不存在!');
    return;
  }
  if (current_row_item.resource_status == '删除') {
    ElMessage.warning('资源已删除，请先恢复后再操作!');
    return;
  }
  // 分享资源
  if (current_row_item?.id == -1) {
    current_row_item.id = currentResourceID;
  }
  await turn_on_share_selector(current_row_item);
}
const emits = defineEmits(['selectAll']);
watch(
  () => props.resourceId,
  () => {
    currentResourceID.value = props.resourceId;
  }
);
</script>

<template>
  <div
    v-show="resource_share_context_menu_flag"
    id="resource_share_menu_box"
    :style="{ left: mousePosition.x + 'px', top: mousePosition.y + 'px', position: 'absolute' }"
    class="ces-os-context-menu"
  >
    <div class="context-menu-button">
      <el-button v-if="current_row_item.id == -1" text style="width: 100%" @click="switchResourceLayout">
        切换布局
      </el-button>
    </div>
    <div class="context-menu-button">
      <el-button v-if="current_row_item.id == -1" text style="width: 100%" @click="emits['selectAll']">
        {{ '全选' }}
      </el-button>
    </div>

    <div v-if="!isMultipleSelection" class="context-menu-button">
      <el-button text style="width: 100%" @click="shareResource"> 分享 </el-button>
    </div>
    <div class="context-menu-button">
      <el-button v-if="current_row_item.id > 0" text style="width: 100%" @click="preview_share_resource">
        查看
      </el-button>
    </div>
    <div class="context-menu-button">
      <el-button v-if="current_row_item.id > 0" text style="width: 100%" @click="download_resource"> 下载 </el-button>
    </div>
  </div>
</template>

<style scoped>
#resource_share_menu_box {
  background: #fff;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  padding: 5px;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  min-width: 80px;
  min-height: 100px;
}
.context-menu-button {
  width: 100%;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
}
</style>
