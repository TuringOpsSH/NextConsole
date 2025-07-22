<script setup lang="ts">
import {ref, watch} from 'vue';
const props = defineProps({
  welcomeConfig: {
    type: Object,
    default: () => ({}),
    required: false
  }
});
const localWelcomeConfig = ref();
watch(
  () => props.welcomeConfig,
  (newVal) => {
    localWelcomeConfig.value = newVal;
  },
  { immediate: true }
);
const emits = defineEmits(['prefixQuestionClick']);
</script>

<template>
  <div class="preview-area">
    <div class="preview-area-top">
      <div class="top-row">
        <div class="icon-area">
          <el-image :src="localWelcomeConfig.image" class="welcome-icon" />
        </div>
        <div>
          <el-text class="title-text">{{ localWelcomeConfig.title }}</el-text>
        </div>
      </div>
      <div>
        <el-text class="desc-text">{{ localWelcomeConfig.description }}</el-text>
      </div>
    </div>
    <div class="preview-area-body"></div>
    <div class="preview-area-foot">
      <el-tag
        v-for="(question, index) in localWelcomeConfig.prefixQuestions"
        :key="index"
        class="prefix-question-tag"
        size="large"
        round
        @click="emits('prefixQuestionClick', question)"
      >
        {{ question }}
      </el-tag>
    </div>
  </div>
</template>

<style scoped>
.preview-area {
  width: calc(100% - 32px);
  display: flex;
  flex-direction: column;
  gap: 16px;
  border-radius: 8px; /* 圆角 */
  padding: 20px; /* 内边距 */
  position: relative; /* 为标题装饰定位 */
}

.preview-area-top {
  background: linear-gradient(95.64772deg, #5ac4ff1f -17%, #ae88ff1f 123%);
  border-radius: 12px;
  width: 100%;
  padding: 19px 16px 13px;
  box-sizing: border-box;
  color: #000000e0;
  font-weight: 400;
}

.preview-area-top {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.top-row {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 12px;
}

.title-text {
  font-size: 20px;
  font-weight: 600;
  line-height: 1.4;
  background: linear-gradient(270deg, #8b5cf6, #3b82f6 43%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.desc-text {
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  color: #000000b3;
}

.preview-area-foot {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  align-items: center;
  gap: 12px;
}

.prefix-question-tag {
  cursor: pointer;
}
.welcome-icon {
  width: 40px;
  height: 40px;
  background: #f2f4f7;
}
</style>
