<template>
  <div class="issues-container">
    <div class="header">
      <h3>最新问题列表</h3>
    </div>
    <el-scrollbar>
      <div class="issues-list" :style="{ height: areaHeight + 'px' }">
        <div v-for="issue in messages" :key="issue.msg_id" class="issue-item">
          <div class="issue-main">
            <div>
              <el-text bold>{{ issue.msg_content }}</el-text>
            </div>
            <div class="issue-meta">
              <el-text truncated>
                由
                <el-tag>{{ issue?.user_info.name || issue?.user_info.user_nick_name }}</el-tag>
                创建于
              </el-text>
              <el-tag>{{ issue.create_time }}</el-tag>
            </div>
          </div>
        </div>
      </div>
    </el-scrollbar>
    <div v-if="messages.length === 0" class="empty-state">暂无相关问题</div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import { getDashboardIndex } from '@/api/dashboard';
import { IMsgItem } from '@/types/next-console';
const props = defineProps({
  height: {
    type: Number,
    default: 300
  }
});
const areaHeight = ref(300);
// 响应式数据
const messages = ref<IMsgItem[]>([]);

async function getUserLatestQuestions(beginTime: string, companyId: number) {
  const params = {
    index_name: 'user_latest_questions',
    begin_time: beginTime,
    top: '',
    company_id: companyId
  };
  const res = await getDashboardIndex(params);
  if (!res.error_status) {
    messages.value = res.result.latest_questions;
  }
}
watch(
  () => props.height,
  newValue => {
    if (newValue) {
      areaHeight.value = newValue;
    }
  },
  {
    immediate: true
  }
);
defineExpose({
  getUserLatestQuestions
});
</script>

<style scoped>
.issues-container {
  max-width: 500px;
  margin: 0 auto;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header h2 {
  margin: 0;
  color: #333;
}

.controls {
  display: flex;
  gap: 10px;
}

.sort-select,
.filter-select {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: white;
}

.issues-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.issue-item {
  display: flex;
  justify-content: space-between;
  padding: 16px;
  border: 1px solid #e1e4e8;
  border-radius: 6px;
  background-color: white;
  transition: box-shadow 0.2s;
}

.issue-item:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.issue-main {
  flex: 1;
}

.issue-title {
  margin: 0 0 8px 0;
  font-size: 16px;
  color: #24292e;
}

.issue-description {
  margin: 0 0 12px 0;
  color: #586069;
  font-size: 14px;
  line-height: 1.4;
}

.issue-meta {
  display: flex;
  gap: 12px;
  font-size: 12px;
  color: #6a737d;
  margin-top: 6px;
}

.empty-state {
  text-align: center;

  padding: 40px;

  color: #6a737d;

  font-style: italic;
}
</style>
