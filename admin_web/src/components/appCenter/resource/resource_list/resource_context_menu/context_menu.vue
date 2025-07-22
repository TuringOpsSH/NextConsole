<script setup lang="ts">
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
} from '@/components/resource/resource_list/resource_context_menu/context_menu';
import { search_all_resource_object, current_resource_list } from '@/components/resource/resource_list/resource_list';
import {
  show_add_dir_dialog,
  show_add_document_dialog,
  switch_resource_layout
} from '@/components/resource/resource_list/resource_head/resource_head';
import {
  prepare_upload_files,
  upload_file_content,
  upload_file_list
} from '@/components/resource/resource_upload/resource_upload';
import { current_resource_usage_percent, init_upload_manager } from '@/components/resource/resource_panel/panel';
import { computed, inject, Ref } from 'vue';

const isSelectedAll = computed(() => {
  return current_resource_list.value.every(item => item.resource_is_selected);
});
const isMultipleSelection = inject<Ref<boolean>>('isMultipleSelection');
</script>

<template>
  <div
    ref=""
    :style="{ left: mousePosition.x + 'px', top: mousePosition.y + 'px', position: 'absolute' }"
    v-show="resource_list_context_menu_flag"
    id="resource_list_menu_box"
    class="ces-os-context-menu"
  >
    <div class="context-menu-button">
      <el-button text @click="search_all_resource_object()" style="width: 100%"> 刷新 </el-button>
    </div>
    <!-- <div class="context-menu-button">
      <el-button text @click="show_resource_detail()" style="width: 100%">
        详情
      </el-button>
    </div> -->
    <div class="context-menu-button">
      <el-button text @click="switch_resource_layout()" style="width: 100%" v-if="current_row_item.id == -1">
        切换布局
      </el-button>
    </div>
    <div class="context-menu-button">
      <el-button text @click="show_add_document_dialog()" style="width: 100%" v-if="current_row_item.id == -1">
        新建文档
      </el-button>
    </div>
    <div class="context-menu-button">
      <el-button text @click="show_add_dir_dialog()" style="width: 100%" v-if="current_row_item.id == -1">
        新建文件夹
      </el-button>
    </div>
    <div class="context-menu-button">
      <el-button text @click="select_all(isSelectedAll)" style="width: 100%" v-if="current_row_item.id == -1">
        {{ isSelectedAll ? '取消全选' : '全选' }}
      </el-button>
    </div>

    <el-upload
      multiple
      :show-file-list="false"
      :auto-upload="true"
      name="chunk_content"
      action=""
      v-model:file-list="upload_file_list"
      :before-upload="prepare_upload_files"
      :on-change="init_upload_manager"
      :http-request="upload_file_content"
      :disabled="current_resource_usage_percent >= 100"
      accept="*"
      style="width: 100%; display: flex; align-items: center; justify-content: center"
      :on-success="search_all_resource_object"
      ref="upload_file_Ref"
    >
      <div class="context-menu-button">
        <el-button text style="width: 100%"> 上传 </el-button>
      </div>
    </el-upload>

    <div v-if="!isMultipleSelection" class="context-menu-button">
      <el-button text @click="share_resource()" style="width: 100%"> 分享 </el-button>
    </div>
    <div class="context-menu-button">
      <el-button text v-if="current_row_item.id > 0" @click="preview_resource()" style="width: 100%"> 查看 </el-button>
    </div>
    <div class="context-menu-button">
      <el-button text v-if="current_row_item.id > 0" @click="download_resource()" style="width: 100%"> 下载 </el-button>
    </div>
    <div class="context-menu-button">
      <el-button text @click="move_resource()" v-if="current_row_item.id > 0" style="width: 100%"> 移动到 </el-button>
    </div>
    <div class="context-menu-button">
      <el-button text @click="rebuild_resource()" v-if="current_row_item.id > 0" style="width: 100%">
        重新构建
      </el-button>
    </div>

    <div class="context-menu-button">
      <el-button text @click="delete_resource()" type="danger" v-if="current_row_item.id > 0" style="width: 100%">
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
