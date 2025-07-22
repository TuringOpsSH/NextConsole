<script setup lang="ts">
import {
  current_row_item,
  delete_resource,
  download_resource,
  init_upload_manager,
  mousePosition,
  move_resource,
  preview_resource,
  rebuild_resource,
  resource_shortcut_context_menu_flag,
  select_all,
  share_resource,
  show_resource_detail,
  upload_file_Ref
} from '@/components/resource/resource_shortcut/resource_context_menu/context_menu';
import {
  completely_delete_resource,
  search_resource_by_tags
} from '@/components/resource/resource_shortcut/resource_shortcut';
import { switch_resource_layout } from '@/components/resource/resource_shortcut/resource_shortcut_head/resource_shortcut_head';
import {
  prepare_upload_files,
  upload_file_content,
  upload_file_list
} from '@/components/resource/resource_upload/resource_upload';
import { current_resource_usage_percent } from '@/components/resource/resource_panel/panel';
</script>

<template>
  <div
    ref=""
    :style="{ left: mousePosition.x + 'px', top: mousePosition.y + 'px', position: 'absolute' }"
    v-show="resource_shortcut_context_menu_flag"
    id="resource_shortcut_menu_box"
    class="ces-os-context-menu"
  >
    <div class="context-menu-button">
      <el-button text @click="search_resource_by_tags()" style="width: 100%"> 刷新 </el-button>
    </div>
    <div class="context-menu-button">
      <el-button text @click="show_resource_detail()" style="width: 100%"> 详情 </el-button>
    </div>
    <div class="context-menu-button">
      <el-button text @click="switch_resource_layout()" style="width: 100%" v-if="current_row_item.id == -1">
        切换布局
      </el-button>
    </div>
    <div class="context-menu-button">
      <el-button text @click="select_all()" style="width: 100%" v-if="current_row_item.id == -1"> 全选 </el-button>
    </div>
    <el-upload
      multiple
      :show-file-list="false"
      :auto-upload="true"
      name="chunk_content"
      v-model:file-list="upload_file_list"
      :before-upload="prepare_upload_files"
      :on-change="init_upload_manager"
      :http-request="upload_file_content"
      :disabled="current_resource_usage_percent >= 100"
      accept="*"
      action=""
      ref="upload_file_Ref"
    >
      <div class="context-menu-button">
        <el-button text style="width: 100%"> 上传 </el-button>
      </div>
    </el-upload>
    <div class="context-menu-button">
      <el-button text v-if="current_row_item.id > 0" @click="preview_resource()" style="width: 100%"> 查看 </el-button>
    </div>
    <div class="context-menu-button">
      <el-button text v-if="current_row_item.id > 0" @click="download_resource()" style="width: 100%"> 下载 </el-button>
    </div>
    <div class="context-menu-button">
      <el-button text v-if="current_row_item.id > 0" @click="share_resource()" style="width: 100%"> 分享 </el-button>
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
      <el-button
        text
        @click="delete_resource()"
        type="danger"
        v-if="current_row_item.id > 0 && current_row_item.resource_status != '删除'"
        style="width: 100%"
      >
        删除
      </el-button>
      <el-button
        text
        @click="completely_delete_resource(current_row_item)"
        type="danger"
        v-if="current_row_item.id > 0 && current_row_item.resource_status == '删除'"
        style="width: 100%"
      >
        彻底删除
      </el-button>
    </div>
  </div>
</template>

<style scoped>
#resource_shortcut_menu_box {
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
