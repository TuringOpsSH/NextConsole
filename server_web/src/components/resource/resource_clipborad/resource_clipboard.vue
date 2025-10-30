<script setup lang="ts">

import {
  clean_all_clipboard,
  current_resource_clipboard, init_clipboard, paste_resource, paste_resource_confirm, paste_resource_dialog,
  remove_copy_resource, resource_clipboard
} from "@/components/resource/resource_clipborad/resource_clipboard";
import {get_resource_icon} from "@/components/resource/resource-list/resource_list";
import {onMounted} from "vue";
onMounted(() => {
  init_clipboard()
})
</script>

<template>
  <el-popover trigger="click" placement="bottom" width="400" ref="resource_clipboard"
              @before-enter="init_clipboard"
  >
    <template #reference>
      <div id="clipboard_button">
        <div class="resource-head-button" :style="{
              'background': current_resource_clipboard?.length>0 ? '#EFF8FF' : '#F2F4F7',
            }">
          <el-image v-show="current_resource_clipboard?.length>0"
                    src="/images/resource_clipboard_active.svg"
                    class="resource-head-button-icon"/>
          <el-image v-show="!current_resource_clipboard?.length "
                    src="/images/resource_clipboard.svg"
                    class="resource-head-button-icon"/>

        </div>
        <div v-show="current_resource_clipboard?.length>0" id="copy_resource_cnt">
          <el-text style="color: #175CD3;font-size: 12px;font-weight: 500;line-height: 18px;">
            {{ current_resource_clipboard?.length }}
          </el-text>
        </div>
      </div>
    </template>
    <el-scrollbar style="width: 100%">
      <div class="clipboard-resources-area">
        <div v-for="(resource,idx) in current_resource_clipboard" class="copy-resource">
          <div class="std-middle-box" style="justify-content: flex-start; gap: 6px;cursor: pointer"
               @click="">
            <div class="std-middle-box">
              <el-image :src="get_resource_icon(resource)" class="resource-head-button-icon"/>
            </div>
            <div class="std-middle-box">
              <el-text truncated style="width: 300px">
                {{ resource?.resource_name }}
              </el-text>
            </div>
          </div>

          <div class="std-middle-box" style="cursor:pointer;" @click="remove_copy_resource(idx)">
            <el-image src="/images/delete_red.svg" class="resource-head-button-icon"/>
          </div>

        </div>
      </div>
    </el-scrollbar>
    <div class="std-middle-box" style="width: 100%;gap: 24px">
      <el-button @click="clean_all_clipboard()">清空</el-button>
      <el-button type="primary" @click="paste_resource_confirm()" disabled>粘贴</el-button>
    </div>

  </el-popover>
  <el-dialog v-model="paste_resource_dialog" :close-on-click-modal="false" :show-close="false" :draggable="true"
             :close-on-press-escape="false"
  >
    <el-result icon="warning" sub-title="是否将选择资源粘贴至当前页面？">

    </el-result>
    <div class="std-middle-box" style="width: 100%;gap: 24px">
      <el-button @click="paste_resource_dialog=false">取消</el-button>
      <el-button type="primary" @click="paste_resource()">确定</el-button>
    </div>
  </el-dialog>
</template>

<style scoped>
.std-middle-box{
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}
.resource-head-button{
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  border-radius: 4px;
  padding: 2px;
}
.resource-head-button-icon{
  width: 16px;
  height: 16px;
}
.resource-head-button:hover{
  background: #EFF8FF;

}

.clipboard-resources-area {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 8px;
  align-items: flex-start;
  justify-content: flex-start;
  max-height: 400px;
}

#clipboard_button{
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  gap: 6px;
  cursor: pointer;

}
#copy_resource_cnt{
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;

  padding: 0 4px;
  border-radius: 3px;
  background: #D1E9FF;


}
.copy-resource{
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  gap: 4px;
  padding: 6px 6px;
  border: 1px solid #D0D5DD;
  border-radius: 6px;
  width: calc(100% - 12px);
}
.copy-resource:hover{
  background: #EFF8FF;
}
</style>
