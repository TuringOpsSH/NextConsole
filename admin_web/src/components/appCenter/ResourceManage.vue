<script setup lang="ts">
import {watch, ref} from 'vue';
import router from "@/router";
const props = defineProps ({
  viewModel: {
    type: String,
    default: 'resource',
    required: false
  }
});
const currentViewModel = ref('resource');
async function handleViewModelChange(newVal: string) {
  currentViewModel.value = newVal;
  await router.replace({
    query: { viewModel: newVal }
  });
}
watch(() => props.viewModel, (newVal) => {
  currentViewModel.value = newVal;
  router.replace ({
    query: { viewModel: newVal }
  })
}, { immediate: true });
</script>

<template>
<el-container>
  <el-main>
    <el-tabs v-model="currentViewModel" @tab-change="handleViewModelChange">
      <el-tab-pane label="资源管理" name="resource">
      </el-tab-pane>
      <el-tab-pane label="数据源管理" name="data">
      </el-tab-pane>
      <el-tab-pane label="知识库管理" name="knowledge">
      </el-tab-pane>
    </el-tabs>
  </el-main>
</el-container>
</template>

<style scoped>

</style>
