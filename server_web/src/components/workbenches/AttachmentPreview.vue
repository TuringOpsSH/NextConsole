<script setup lang="ts">
import { Close } from '@element-plus/icons-vue';
import { ref, watch } from 'vue';
const localAttachmentList = ref([]);
const props = defineProps({
  attachmentList: {
    type: Array as () => IAttachmentDetail[],
    default: {},
    required: false
  }
});
interface IAttachmentDetail {
  resource_id: number;
  resource_name: string;
  resource_icon: string;
  resource_size: number;
}
function reformatFileSize(bytes: number) {
  if (!bytes) {
    return '0 B';
  }
  let newBytes = bytes * 1021 * 1024;
  const units = ['B', 'KB', 'MB', 'GB'];
  let unitIndex = 0;

  if (!newBytes) {
    return '';
  }
  while (newBytes >= 1024 && unitIndex < units.length - 1) {
    newBytes /= 1024;
    unitIndex++;
  }
  return `${newBytes.toFixed(2)} ${units[unitIndex]}`;
}
watch(
  () => props.attachmentList,
  async newVal => {
    localAttachmentList.value = newVal;
  },
  { immediate: true }
);
const emits = defineEmits(['remove-attachment']);
</script>

<template>
  <el-scrollbar>
    <div class="attachment-list">
      <div v-for="item in attachmentList" :key="item.id" class="attachment-item">
        <div>
          <el-image :src="item.resource_icon" class="attachment-item-img" />
        </div>
        <div class="attachment-item-right">
          <el-tooltip :content="item.resource_name" placement="top">
            <el-text truncated style="width: 120px"> {{ item.resource_name }}</el-text>
          </el-tooltip>
          <div>
            <el-text> {{ reformatFileSize(item.resource_size) }}</el-text>
          </div>
        </div>
        <div class="close-icon">
          <el-popconfirm title="确认移除?" @confirm="emits('remove-attachment', item)">
            <template #reference>
              <Close class="close-icon-icon" />
            </template>
          </el-popconfirm>
        </div>
      </div>
    </div>
  </el-scrollbar>
</template>

<style scoped>
.attachment-list {
  padding: 12px 12px 2px;
  background: #fff;
  box-sizing: border-box;
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
  -ms-flex-wrap: wrap;
  flex-wrap: wrap;
  gap: 8px 9px;
  max-height: 100px;
  overflow-y: auto;
}

/* Webkit浏览器滚动条样式 */
.attachment-list::-webkit-scrollbar {
  width: 8px; /* 垂直滚动条宽度 */
  height: 8px; /* 水平滚动条高度 */
}

.attachment-list::-webkit-scrollbar-track {
  background-color: #f5f5f5; /* 滚动条轨道背景色 */
  -webkit-border-radius: 4px; /* 轨道圆角 */
  border-radius: 4px;
}

.attachment-list::-webkit-scrollbar-thumb {
  background-color: #c1c1c1; /* 滚动条滑块颜色 */
  -webkit-border-radius: 4px; /* 滑块圆角 */
  border-radius: 4px;
}

.attachment-list::-webkit-scrollbar-thumb:hover {
  background-color: #a8a8a8; /* 鼠标悬停时滑块颜色 */
}

/* Firefox浏览器滚动条样式 */
.attachment-list {
  scrollbar-width: thin; /* 滚动条宽度 */
  scrollbar-color: #c1c1c1 #f5f5f5; /* 滑块颜色和轨道颜色 */
}

/* 兼容旧版Firefox */
@-moz-document url-prefix() {
  .attachment-list {
    scrollbar-width: thin;
    scrollbar-face-color: #c1c1c1;
    scrollbar-track-color: #f5f5f5;
  }
}

.attachment-item {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 4px;
  background: #f0f0f0;
  padding: 12px 16px;
  border: 1px solid #d0d5dd;
  border-radius: 6px;
  position: relative;
  transition: all 0.3s ease;
}
.attachment-item :hover {
  box-shadow: 2px 2px 3px rgba(0, 0, 0, 0.15);
}
.attachment-item :hover .close-icon{
  display: flex;
}
.attachment-item-img {
  width: 36px;
  height: 36px;
}
.attachment-item-right {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}
.close-icon {
  position: absolute;
  top: 0;
  right: 0;
  cursor: pointer;
  background: #b4b5b7;
  transition: color 0.3s ease;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  display: none;

}
.close-icon-icon {
  width: 16px;
  height: 16px;
  cursor: pointer;
  background: #fff;
}
.close-icon-icon :focus{
  outline: none;
}
</style>
