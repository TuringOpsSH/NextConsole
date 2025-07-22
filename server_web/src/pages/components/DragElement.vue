<template>
  <div class="drag-container">
    <div class="drag-panel" :style="{ width: panelWidth + 'px' }">
      <slot></slot>
    </div>
    <div
        class="drag-bar"
        :style="{
        order: direction === 'left' ? -1 : 0
      }"
        @mousedown.left="startDrag"
        @touchstart.passive="startDrag"
    ></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onUnmounted } from 'vue';
interface IProps {
  width: number;
  minWidth?: number;
  maxWidth?: number;
  onResize?: (width: number) => void;
  direction?: 'left' | 'right';
}

const { width = 200, minWidth = 200, maxWidth = 400, onResize, direction = 'right' } = defineProps<IProps>();
const panelWidth = ref(width); // 初始宽度
const isDragging = ref(false); // 拖拽状态锁

// 统一处理移动事件
const handleMove = (event: MouseEvent | TouchEvent) => {
  if (!isDragging.value) {
    return;
  }

  // 计算坐标（兼容触摸事件）
  const clientX = 'touches' in event ? event.touches[0].clientX : event.clientX;
  const currentWidth = direction === 'left' ? window.innerWidth - clientX : clientX;
  // 限制宽度范围（示例范围 100px~500px）
  const newWidth = Math.max(minWidth, Math.min(currentWidth, maxWidth));
  panelWidth.value = newWidth;
  onResize?.(newWidth);
};

// 开始拖拽
const startDrag = (event: MouseEvent | TouchEvent) => {
  // 过滤非左键点击
  if (event instanceof MouseEvent && event.button !== 0) return;

  isDragging.value = true;

  // 添加事件监听（注意使用 { passive: true } 优化触控性能）
  window.addEventListener('mousemove', handleMove);
  window.addEventListener('touchmove', handleMove, { passive: true });
  window.addEventListener('mouseup', stopDrag);
  window.addEventListener('touchend', stopDrag);
};

// 停止拖拽
const stopDrag = () => {
  isDragging.value = false;
  removeEventListeners();
};

// 清理事件监听
const removeEventListeners = () => {
  window.removeEventListener('mousemove', handleMove);
  window.removeEventListener('touchmove', handleMove);
  window.removeEventListener('mouseup', stopDrag);
  window.removeEventListener('touchend', stopDrag);
};

// 组件卸载时清理
onUnmounted(removeEventListeners);
</script>

<style lang="scss" scoped>
.drag-container {
  height: 100vh;
  background-color: initial;
  display: flex;

  .drag-panel {
    height: 100%;
    background-color: initial;
    transition: width 0.1s linear; // 添加过渡动画
    order: 0;
  }

  .drag-bar {
    width: 4px;
    height: 100%;
    background-color: initial;

    cursor:
        url(@/assets/extend.svg) 12 0,
        col-resize;
    user-select: none; // 禁止文本选中干扰
  }
}
</style>
