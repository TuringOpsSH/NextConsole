<template>
  <div class="back-top" :style="positionStyle">
    <el-tooltip v-if="showBackTop" content="回到顶部" placement="top">
      <SvgIcon name="knowledge-back-top" width="32" height="32" color="#1890ff" @click="scrollToTop" />
    </el-tooltip>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue';

// 获取目标元素
const targetElement = ref<HTMLElement | null>(null);
// 控制返回顶部按钮的显示/隐藏
const showBackTop = ref<boolean>(false);
interface Props {
  // 目标元素的id
  targetId: string;
  // 滚动距离阈值，超过该阈值显示按钮
  scrollThreshold?: number;
  // 按钮位置
  position?: {
    bottom?: number;
    right?: number;
  };
}
const { targetId, scrollThreshold = 200, position } = defineProps<Props>();
const positionStyle = computed(() => ({
  bottom: `${position.bottom ?? 100}px`,
  right: `${position.right ?? 50}px`
}));

// 获取目标元素
const getTargetElement = () => {
  return document.getElementById(targetId) as HTMLElement;
};

// 滚动事件处理函数
const handleScroll = () => {
  if (!targetElement.value) {
    return;
  }
  const scrollTop = targetElement.value.scrollTop;
  showBackTop.value = scrollTop > scrollThreshold;
};

onMounted(() => {
  targetElement.value = getTargetElement();
  if (targetElement.value) {
    targetElement.value.addEventListener('scroll', handleScroll);
  }
});

onUnmounted(() => {
  if (targetElement.value) {
    targetElement.value.removeEventListener('scroll', handleScroll);
  }
});

// 回到顶部的方法
const scrollToTop = () => {
  if (targetElement.value) {
    targetElement.value.scrollTo({
      top: 0,
      behavior: 'smooth' // 平滑滚动，可根据需求设置
    });
  }
};
</script>

<style scoped lang="scss">
.back-top {
  position: fixed;
  z-index: 9999;
  opacity: 1;
  svg {
    background-color: #fff;
    border-radius: 50%;
    &:hover {
      box-shadow: 0 0 12px rgb(57, 136, 255);
    }
  }
}
</style>
