<script setup lang="ts">
import {computed, inject, Ref} from 'vue';
import {
  current_row_item,
  delete_resource,
  download_resource,
  mousePosition,
  preview_resource,
  rebuild_resource,
  resource_list_context_menu_flag,
  select_all,
  share_resource
} from '@/components/resource/resource-list/resource_context_menu/context-menu';
import {
  show_add_dir_dialog,
  show_add_document_dialog
} from '@/components/resource/resource-list/resource_head/resource_head';
import {current_resource_list, search_all_resource_object} from '@/components/resource/resource-list/resource-list';
import {ElMessage} from "element-plus";
import {useSessionStorage} from "@vueuse/core";
import {TResourceListStatus} from "@/types/resource-type";
import router from "@/router";
const emits = defineEmits(['moveDialogMultiple']);
const isSelectedAll = computed(() => {
  return current_resource_list.value.every(item => item.resource_is_selected);
});
const isMultipleSelection = inject<Ref<boolean>>('isMultipleSelection');
async function moveResource() {
  if (!current_row_item?.id) {
    ElMessage.warning('资源不存在!');
    return;
  }
  if (current_row_item.resource_status == '删除') {
    ElMessage.warning('资源已删除，请先恢复后再操作!');
    return;
  }
  // 移动资源
  emits('moveDialogMultiple', [current_row_item.id], search_all_resource_object);
}
async function switchResourceLayout() {
  // 切换面板展示时暂不刷新数据
  const resourceListStatus = useSessionStorage<TResourceListStatus>('resourceListStatus', 'card');
  if (resourceListStatus.value === 'list') {
    resourceListStatus.value = 'card';
  } else {
    resourceListStatus.value = 'list';
  }
  // 更新至url
  router.push({
    params: { ...router.currentRoute.value.params },
    query: {
      ...router.currentRoute.value.query,
      view_model: resourceListStatus.value
    }
  });
}
</script>

<template>
  <div
    v-show="resource_list_context_menu_flag"
    id="resource_list_menu_box"
    :style="{ left: mousePosition.x + 'px', top: mousePosition.y + 'px', position: 'absolute' }"
    class="ces-os-context-menu"
  >
    <div class="context-menu-button">
      <el-button text style="width: 100%" @click="search_all_resource_object"> 刷新 </el-button>
    </div>
    <div class="context-menu-button">
      <el-button v-if="current_row_item.id == -1" text style="width: 100%" @click="switchResourceLayout">
        切换布局
      </el-button>
    </div>
    <div class="context-menu-button">
      <el-button v-if="current_row_item.id == -1" text style="width: 100%" @click="show_add_document_dialog">
        新建文档
      </el-button>
    </div>
    <div class="context-menu-button">
      <el-button v-if="current_row_item.id == -1" text style="width: 100%" @click="show_add_dir_dialog">
        新建文件夹
      </el-button>
    </div>
    <div class="context-menu-button">
      <el-button v-if="current_row_item.id == -1" text style="width: 100%" @click="select_all(isSelectedAll)">
        {{ isSelectedAll ? '取消全选' : '全选' }}
      </el-button>
    </div>
    <div v-if="!isMultipleSelection" class="context-menu-button">
      <el-button text style="width: 100%" @click="share_resource"> 分享 </el-button>
    </div>
    <div class="context-menu-button">
      <el-button v-if="current_row_item.id > 0" text style="width: 100%" @click="preview_resource"> 查看 </el-button>
    </div>
    <div class="context-menu-button">
      <el-button v-if="current_row_item.id > 0" text style="width: 100%" @click="download_resource"> 下载 </el-button>
    </div>
    <div class="context-menu-button">
      <el-button v-if="current_row_item.id > 0" text style="width: 100%" @click="moveResource"> 移动到 </el-button>
    </div>
    <div class="context-menu-button">
      <el-button v-if="current_row_item.id > 0" text style="width: 100%" @click="rebuild_resource">
        重新构建
      </el-button>
    </div>

    <div class="context-menu-button">
      <el-button v-if="current_row_item.id > 0" text type="danger" style="width: 100%" @click="delete_resource">
        删除
      </el-button>
    </div>
  </div>
</template>

<style scoped>
#resource_list_menu_box {
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
