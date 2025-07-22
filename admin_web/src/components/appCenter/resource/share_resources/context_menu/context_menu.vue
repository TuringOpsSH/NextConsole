<script setup lang="ts">
import { computed, inject, Ref } from 'vue';
import {
  current_row_item,
  download_resource,
  mousePosition,
  preview_share_resource,
  resource_share_context_menu_flag,
  select_all,
  share_resource,
  show_resource_detail
} from '@/components/resource/share_resources/context_menu/context_menu';
import { switch_resource_layout } from '@/components/resource/share_resources/resource_head/resource_head';
import {
  search_all_resource_share_object,
  share_resource_list
} from '@/components/resource/share_resources/share_resources';

const isSelectedAll = computed(() => {
  return share_resource_list.value.every(item => item.resource_is_selected);
});
const isMultipleSelection = inject<Ref<boolean>>('isMultipleSelection');
</script>

<template>
  <div
    ref=""
    :style="{ left: mousePosition.x + 'px', top: mousePosition.y + 'px', position: 'absolute' }"
    v-show="resource_share_context_menu_flag"
    id="resource_share_menu_box"
    class="ces-os-context-menu"
  >
    <div class="context-menu-button">
      <el-button text @click="search_all_resource_share_object()" style="width: 100%"> 刷新 </el-button>
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
      <el-button text @click="select_all(isSelectedAll)" style="width: 100%" v-if="current_row_item.id == -1">
        {{ isSelectedAll ? '取消全选' : '全选' }}
      </el-button>
    </div>

    <div v-if="!isMultipleSelection" class="context-menu-button">
      <el-button text @click="share_resource()" style="width: 100%"> 分享 </el-button>
    </div>
    <div class="context-menu-button">
      <el-button text v-if="current_row_item.id > 0" @click="preview_share_resource()" style="width: 100%">
        查看
      </el-button>
    </div>
    <div class="context-menu-button">
      <el-button text v-if="current_row_item.id > 0" @click="download_resource()" style="width: 100%"> 下载 </el-button>
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
