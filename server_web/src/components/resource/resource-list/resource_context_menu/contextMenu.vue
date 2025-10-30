<script setup lang="ts">
import { computed, inject, Ref } from 'vue';
import {
  current_row_item,
  delete_resource,
  download_resource,
  mousePosition,
  move_resource,
  preview_resource,
  rebuild_resource,
  resource_list_context_menu_flag,
  select_all,
  share_resource,
  show_resource_detail,
  upload_file_Ref
} from '@/components/resource/resource-list/resource_context_menu/context_menu';
import {
  show_add_dir_dialog,
  show_add_document_dialog,
  switch_resource_layout
} from '@/components/resource/resource-list/resource_head/resource_head';
import { search_all_resource_object, current_resource_list } from '@/components/resource/resource-list/resource_list';
import { current_resource_usage_percent, init_upload_manager } from '@/components/resource/resource-panel/panel';
import {
  prepare_upload_files,
  upload_file_content,
  upload_file_list
} from '@/components/resource/resource-upload/resource-upload';

const isSelectedAll = computed(() => {
  return current_resource_list.value.every(item => item.resource_is_selected);
});
const isMultipleSelection = inject<Ref<boolean>>('isMultipleSelection');
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
    <!-- <div class="context-menu-button">
      <el-button text @click="show_resource_detail()" style="width: 100%">
        详情
      </el-button>
    </div> -->
    <div class="context-menu-button">
      <el-button v-if="current_row_item.id == -1" text style="width: 100%" @click="switch_resource_layout()">
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

    <el-upload
      ref="upload_file_Ref"
      v-model:file-list="upload_file_list"
      multiple
      :show-file-list="false"
      :auto-upload="true"
      name="chunk_content"
      action=""
      :before-upload="prepare_upload_files"
      :on-change="init_upload_manager"
      :http-request="upload_file_content"
      :disabled="current_resource_usage_percent >= 100"
      accept="*"
      style="width: 100%; display: flex; align-items: center; justify-content: center"
      :on-success="search_all_resource_object"
    >
      <div class="context-menu-button">
        <el-button text style="width: 100%"> 上传 </el-button>
      </div>
    </el-upload>

    <div v-if="!isMultipleSelection" class="context-menu-button">
      <el-button text style="width: 100%" @click="share_resource()"> 分享 </el-button>
    </div>
    <div class="context-menu-button">
      <el-button v-if="current_row_item.id > 0" text style="width: 100%" @click="preview_resource()"> 查看 </el-button>
    </div>
    <div class="context-menu-button">
      <el-button v-if="current_row_item.id > 0" text style="width: 100%" @click="download_resource()"> 下载 </el-button>
    </div>
    <div class="context-menu-button">
      <el-button v-if="current_row_item.id > 0" text style="width: 100%" @click="move_resource"> 移动到 </el-button>
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
