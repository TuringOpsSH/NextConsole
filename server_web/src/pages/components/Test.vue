<template>
  <div class="raffle-list">
    <div
      v-for="(item, index) in raffleList"
      :key="index"
      :class="['raffle-item', { 'raffle-active': raffleActive === index }]"
    >
      <span>{{ item }}</span>
    </div>
    <button @click="startAnimation">开始抽奖</button>
  </div>
</template>

<script setup lang="ts">
import { gsap } from 'gsap';
import { ref } from 'vue';

const raffleList = ref(['50积分', '20元京东E卡', '再来一次', '25积分', '10元京东E卡', '谢谢参与']);
const raffleActive = ref(-1);
let animation: gsap.core.Timeline | null = null;

// 顺时针高亮路径（3x2网格路径）
const highlightPath = [0, 1, 2, 5, 4, 3]; // 顺时针运动路径

const startAnimation = () => {
  if (animation?.isActive()) return;

  animation = gsap.timeline({
    onComplete: () => {
      // 精准停止到第四项（索引3）
      gsap.to(raffleActive, {
        value: 3,
        duration: 0.8,
        ease: 'elastic.out(1, 0.3)',
        modifiers: { value: v => Math.round(v) % 6 },
        onComplete: () => (raffleActive.value = 3)
      });
    }
  });

  // 循环高亮路径
  highlightPath.forEach((index, i) => {
    animation!.to(
      raffleActive,
      {
        value: index,
        duration: 0.2,
        ease: 'power2.inOut',
        modifiers: { value: v => Math.round(v) % 6 },
        onUpdate: () => (raffleActive.value = Math.round(animation!.progress() * highlightPath.length))
      },
      i * 0.2
    );
  });
};
</script>

<style scoped lang="scss">
@use 'sass:color';
.flex-center {
  display: flex;
  align-items: center;
  justify-content: center;
}
.raffle-list {
  display: grid;
  /* 创建3个等宽列 */
  grid-template-columns: repeat(3, 1fr);
  gap: 13px;
  margin-top: 25px;
  margin-bottom: 40px;
  $primary-font: 'Alibaba PuHuiTi 3.0';

  .raffle-item {
    $bg-color: #c4c4c4;
    box-sizing: border-box;
    padding: 16px;
    height: 100px;
    color: #000000;
    font-family: $primary-font;
    font-size: 20px;
    font-weight: 400;
    line-height: 1.5;
    background: $bg-color;
    border-radius: 10px;
    will-change: transform, box-shadow; // 启用GPU加速
    backface-visibility: hidden;
    flex: none;
    @extend .flex-center;
    &:hover {
      background: color.adjust($bg-color, $lightness: 10%);
    }
    &:active {
      background: color.scale($bg-color, $lightness: 10%);
    }
    span {
      text-align: center;
      word-break: break-all;
      display: -webkit-box;
      -webkit-box-orient: vertical;
      -webkit-line-clamp: 2; // 显示行数
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: normal; // 需要恢复默认换行
    }
  }
  .raffle-active {
    position: relative;
    z-index: 2;
    box-shadow: 0 0 15px rgba(66, 144, 252, 0.5);
    transform: scale(1.05);
    transition: all 0.3s cubic-bezier(0.68, -0.55, 0.27, 1.55);

    &::after {
      content: '';
      position: absolute;
      top: -5px;
      left: -5px;
      right: -5px;
      bottom: -5px;
      border-radius: 15px;
      background: linear-gradient(45deg, #222223, rgb(66, 144, 252));
      opacity: 0.3;
      z-index: -1;
      animation: pulse-glow 0.8s ease infinite alternate;
    }
    span {
      color: #fff;
    }
    $active-bg-color: #000;
    background: $active-bg-color;
    &:hover {
      background: color.adjust($active-bg-color, $lightness: 30%);
    }
    &:active {
      background: color.adjust($active-bg-color, $lightness: -40%);
    }
  }
}
@keyframes pulse-glow {
  0%,
  100% {
    opacity: 0.3;
  }
  50% {
    opacity: 0.6;
  }
}
</style>
