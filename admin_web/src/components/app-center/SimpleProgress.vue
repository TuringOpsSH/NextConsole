<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { onBeforeMount } from 'vue-demi';

const progressIndex = ref(1);
const interval = ref();
onMounted(() => {
  interval.value = setInterval(() => {
    progressIndex.value = progressIndex.value === 3 ? 1 : progressIndex.value + 1;
  }, 500);
});
onBeforeMount(() => {
  clearInterval(interval.value);
});
</script>

<template>
  <div id="simple_progress">
    <div class="small-circle" :style="{ background: progressIndex === 1 ? '#F04438' : '#Fef3f2' }" />
    <div class="small-circle" :style="{ background: progressIndex === 2 ? '#EAAA08' : '#FEFBE8' }" />
    <div class="small-circle" :style="{ background: progressIndex === 3 ? '#2E90FA' : '#EFF8FF' }" />
  </div>
</template>

<style scoped>
#simple_progress {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  width: 100%;
  gap: 4px;
}
.small-circle {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}
</style>
