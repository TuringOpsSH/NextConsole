<script setup lang="ts">

import {onMounted, ref} from "vue";
import {onBeforeMount} from "vue-demi";

const progress_index = ref(1)
const interval = ref()
onMounted(() => {
  interval.value = setInterval(() => {
    progress_index.value = progress_index.value === 3 ? 1 : progress_index.value + 1;
  }, 500);
});
onBeforeMount(
    () => {
      clearInterval(interval.value)
    }
)


</script>

<template>
  <div id="simple_progress" >
    <div class="small-circle"
         :style="{ background: progress_index === 1 ? '#F04438' : '#Fef3f2' }" />
    <div class="small-circle"
         :style="{ background: progress_index === 2 ? '#EAAA08' : '#FEFBE8' }" />
    <div class="small-circle"
         :style="{ background: progress_index === 3 ? '#2E90FA' : '#EFF8FF' }" />
  </div>
</template>

<style scoped>
#simple_progress{
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  width: 100%;
  gap: 4px;
}
.small-circle{
  width: 12px;
  height: 12px;
  border-radius: 50%;
}
</style>
