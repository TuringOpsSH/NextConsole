<script setup lang="ts">
import {
  add_new_dir,
  add_new_dir_dialog_flag,
  cancel_upload_resource,
  choose_folder_resource,
  confirm_mv_resource,
  confirm_upload_resource,
  convert_to_single_choose,
  current_move_resource_list,
  folder_upload_tree_data,
  get_move_resource_tree,
  get_upload_resource_tree,
  mv_confirm_flag,
  mv_double_check,
  new_resource_dir,
  props,
  resource_mv_tree_data,
  resource_mv_tree_Ref,
  resource_upload_tree_data,
  resource_upload_tree_Ref,
  show_add_new_dir_dialog,
  show_mv_resource_tree,
  show_upload_folder_tree,
  show_upload_resource_tree,
  upload_confirm_flag,
  upload_double_check,
  upload_folder_confirm_flag,
  folder_upload_tree_Ref,
  folder_upload_double_check,
  cancel_upload_folder,
  confirm_upload_folder
} from '@/components/resource/resource_tree/resource_tree';
import { get_resource_icon } from '@/components/resource/resource_list/resource_list';
import { ref } from 'vue';

const dialog_width = ref(window.innerWidth < 768 ? '90%' : '600px');
</script>

<template>
  <el-dialog
    v-model="show_upload_resource_tree"
    title="上传资源至目录"
    draggable
    style="max-width: 700px"
    :show-close="false"
    :close-on-click-modal="false"
    :close-on-press-escape="false"
    :width="dialog_width"
  >
    <div id="resource-move-dialog">
      <div id="resource-move-tree">
        <el-scrollbar>
          <el-tree
            :data="resource_upload_tree_data"
            :lazy="true"
            :load="get_upload_resource_tree"
            :props="props"
            :check-on-click-node="true"
            :check-strictly="true"
            :expand-on-click-node="true"
            ref="resource_upload_tree_Ref"
            :highlight-current="true"
            node-key="resource_id"
            @current-change="convert_to_single_choose"
          >
            <template #default="{ node, data }">
              <div
                style="display: flex; flex-direction: row; gap: 6px; align-items: center; justify-content: flex-start"
              >
                <div>
                  <el-image :src="get_resource_icon(node.data)" style="width: 12px; height: 12px" />
                </div>
                <div>
                  <el-text>{{ node.data.label }}</el-text>
                </div>
              </div>
            </template>
          </el-tree>
        </el-scrollbar>
      </div>
      <div id="resource-move-button-box">
        <div>
          <el-button text @click="show_add_new_dir_dialog(resource_upload_tree_Ref)"> 新建目录 </el-button>
        </div>
        <div id="resource-move-button-box">
          <div>
            <el-button text type="primary" @click="upload_double_check()"> 确定 </el-button>
          </div>
          <div>
            <el-button text @click="cancel_upload_resource()"> 取消 </el-button>
          </div>
        </div>
      </div>
    </div>
  </el-dialog>
  <el-dialog
    v-model="upload_confirm_flag"
    title="上传确认"
    draggable
    style="max-width: 700px"
    :show-close="false"
    :close-on-click-modal="false"
    :close-on-press-escape="false"
    :width="dialog_width"
  >
    <el-result
      icon="info"
      :title="`是否将选中资源上传至新目录:'${choose_folder_resource.label}'?`"
      sub-title="上传后资源会同步继承父目录的权限"
    />
    <div class="resource-move-button-area">
      <el-button @click="upload_confirm_flag = false">取消</el-button>
      <el-button type="primary" @click="confirm_upload_resource()">确认</el-button>
    </div>
  </el-dialog>

  <el-dialog
    v-model="show_upload_folder_tree"
    title="上传文件夹"
    draggable
    style="max-width: 700px"
    :show-close="false"
    :close-on-click-modal="false"
    :close-on-press-escape="false"
    :width="dialog_width"
  >
    <div id="resource-move-dialog">
      <div id="resource-move-tree">
        <el-scrollbar>
          <el-tree
            :data="folder_upload_tree_data"
            :lazy="true"
            :load="get_upload_resource_tree"
            :props="props"
            :check-on-click-node="true"
            :check-strictly="true"
            :expand-on-click-node="true"
            ref="folder_upload_tree_Ref"
            :highlight-current="true"
            node-key="resource_id"
            @current-change="convert_to_single_choose"
          >
            <template #default="{ node, data }">
              <div
                style="display: flex; flex-direction: row; gap: 6px; align-items: center; justify-content: flex-start"
              >
                <div>
                  <el-image :src="get_resource_icon(node.data)" style="width: 12px; height: 12px" />
                </div>
                <div>
                  <el-text>{{ node.data.label }}</el-text>
                </div>
              </div>
            </template>
          </el-tree>
        </el-scrollbar>
      </div>
      <div id="resource-move-button-box">
        <div>
          <el-button text @click="show_add_new_dir_dialog(folder_upload_tree_Ref)"> 新建目录 </el-button>
        </div>
        <div id="resource-move-button-box">
          <div>
            <el-button text type="primary" @click="folder_upload_double_check()"> 确定 </el-button>
          </div>
          <div>
            <el-button text @click="cancel_upload_folder()"> 取消 </el-button>
          </div>
        </div>
      </div>
    </div>
  </el-dialog>
  <el-dialog
    v-model="upload_folder_confirm_flag"
    title="上传文件夹确认"
    draggable
    style="max-width: 700px"
    :show-close="false"
    :close-on-click-modal="false"
    :close-on-press-escape="false"
    :width="dialog_width"
  >
    <el-result
      icon="info"
      :title="`是否将选中资源上传至新目录:'${choose_folder_resource.label}'?`"
      sub-title="上传后资源会同步继承父目录的权限"
    />
    <div class="resource-move-button-area">
      <el-button @click="upload_folder_confirm_flag = false">取消</el-button>
      <el-button type="primary" @click="confirm_upload_folder()">确认</el-button>
    </div>
  </el-dialog>

  <el-dialog
    v-model="show_mv_resource_tree"
    title="移动资源至新目录"
    draggable
    style="max-width: 700px"
    :width="dialog_width"
  >
    <div id="resource-move-dialog">
      <div id="resource-move-tree">
        <el-scrollbar>
          <el-tree
            :data="resource_mv_tree_data"
            :lazy="true"
            :load="get_move_resource_tree"
            :props="props"
            :check-on-click-node="true"
            :check-strictly="true"
            :expand-on-click-node="true"
            ref="resource_mv_tree_Ref"
            :highlight-current="true"
            node-key="resource_id"
            @current-change="convert_to_single_choose"
          >
            <template #default="{ node, data }">
              <div
                style="display: flex; flex-direction: row; gap: 6px; align-items: center; justify-content: flex-start"
              >
                <div>
                  <el-image :src="get_resource_icon(node.data)" style="width: 12px; height: 12px" />
                </div>
                <div>
                  <el-text>{{ node.data.label }}</el-text>
                </div>
              </div>
            </template>
          </el-tree>
        </el-scrollbar>
      </div>
      <div id="resource-move-button-box">
        <div>
          <el-button text @click="show_add_new_dir_dialog(resource_mv_tree_Ref)"> 新建目录 </el-button>
        </div>
        <div id="resource-move-button-box">
          <div>
            <el-button text type="primary" @click="mv_double_check()"> 确定 </el-button>
          </div>
          <div>
            <el-button text @click="show_mv_resource_tree = false"> 取消 </el-button>
          </div>
        </div>
      </div>
    </div>
  </el-dialog>
  <el-dialog
    v-model="mv_confirm_flag"
    title="移动确认"
    draggable
    style="max-width: 700px"
    :show-close="false"
    :close-on-click-modal="false"
    :close-on-press-escape="false"
    :width="dialog_width"
  >
    <el-result
      icon="warning"
      :title="`是否将选中的${current_move_resource_list.length}个资源移动至新目录:'${choose_folder_resource.label}'?`"
      sub-title="移动后资源会同步继承父目录的权限"
    />
    <div class="resource-move-button-area">
      <el-button @click="mv_confirm_flag = false">取消</el-button>
      <el-button type="primary" @click="confirm_mv_resource">确认</el-button>
    </div>
  </el-dialog>

  <el-dialog
    v-model="add_new_dir_dialog_flag"
    title="新增资源目录"
    draggable
    style="max-width: 700px"
    :width="dialog_width"
  >
    <el-form :model="new_resource_dir" label-position="top">
      <el-form-item label="目录名称" required prop="resource_name">
        <el-input v-model="new_resource_dir.resource_name" placeholder="请输入目录名称" @keydown.enter.prevent />
      </el-form-item>
      <el-form-item label="目录描述" prop="resource_desc">
        <el-input
          v-model="new_resource_dir.resource_desc"
          placeholder="请输入目录描述"
          type="textarea"
          :rows="3"
          maxlength="200"
          show-word-limit
        />
      </el-form-item>
      <el-form-item>
        <div class="resource-move-button-area">
          <el-button type="primary" @click="add_new_dir()">确定</el-button>
          <el-button @click="add_new_dir_dialog_flag = false">取消</el-button>
        </div>
      </el-form-item>
    </el-form>
  </el-dialog>
</template>

<style scoped>
#resource-move-dialog {
  display: flex;
  justify-content: space-between;
  flex-direction: column;
  min-height: 300px;
  height: 600px;

  gap: 12px;
}
#resource-move-tree {
  height: 540px;
}
#resource-move-button-box {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  align-items: center;
  flex-direction: row;
}
.resource-move-button-area {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  gap: 12px;
  width: 100%;
}
</style>
