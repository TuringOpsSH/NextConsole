<script setup lang="ts">
import { Picture as IconPicture } from '@element-plus/icons-vue'
import {
  open_reference,
  reference_drawer_data, retry_get_icon,
  show_reference_drawer
} from "@/components/next_console/messages_flow/reference_drawer";
import {ResourceItem} from "@/types/resource-type";
import {ref} from "vue";
const drawer_width = ref(window.innerWidth < 768 ? '60vw': '15vw');
function getResourceIcon(resource: ResourceItem) {
  // 获取资源图标
  if (resource.resource_icon) {
    if (
      resource.resource_icon.includes('http') ||
      resource.resource_icon.includes('data:image') ||
      resource.resource_icon.includes('/images/')
    ) {
      return resource.resource_icon;
    }
    return '/images/' + resource.resource_icon;
  } else {
    return '/images/html.svg';
  }
}
</script>

<template>
  <el-drawer v-model="show_reference_drawer" title="参考来源" :size="drawer_width">
    <el-scrollbar>
      <div id="reference_drawer_body">
          <div v-for="(item,idx ) in reference_drawer_data" @click="open_reference(item)" class="reference-item">
            <div class="reference-title">
              <div class="std-middle-box">
                <el-image :src="getResourceIcon(item)" v-if="item?.resource_icon"
                          :id="item?.resource_icon"
                          @error="retry_get_icon(item)" class="reference-img">
                  <template #error>
                    <div class="image-slot">
                      <el-icon><icon-picture /></el-icon>
                    </div>
                  </template>
                </el-image>
              </div>
              <div class="std-middle-box">
                <el-text truncated class="reference-site-name">
                  {{item?.resource_name}}
                </el-text>
              </div>
            </div>
            <div class="reference-name">
              <el-text truncated class="reference-name-text">
                {{item.resource_title}}
              </el-text>
            </div>
            <div class="reference-text-box">
              <el-text truncated class="reference-text"  >
                {{item?.ref_text}}
              </el-text>
            </div>
          </div>
      </div>
    </el-scrollbar>
  </el-drawer>
</template>

<style scoped>
#reference_drawer_body{
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.reference-item{
  display: flex;
  flex-direction: column;
  gap: 4px;
  cursor: pointer;
}
.reference-item:hover{
  background-color:  #F3F4F6;
}
.std-middle-box{
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.reference-title{
  display: flex;
  flex-direction: row;
  gap: 4px;
}
.reference-img{
  width: 16px;
  height: 16px;
}
.reference-site-name{
  font-weight: 400;
  font-size: 12px;
  line-height: 18px;
  color: #475467;
}
.reference-name-text{
  font-weight: 500;
  font-size: 14px;
  line-height: 20px;
  color: #101828;
}
.reference-text-box{
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  gap: 4px;
  flex-wrap: wrap;
  width: 100%;
}
.reference-text{
  font-weight: 400;
  font-size: 14px;
  line-height: 20px;
  color: #667085;

}
</style>
