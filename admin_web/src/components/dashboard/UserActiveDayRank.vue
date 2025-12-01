<template>
  <div class="ranking-wrap">
    <h2 class="title">总活跃天数榜</h2>
    <el-scrollbar>
      <ul class="ranking-list" :style="{ height: areaHeight + 'px' }">
        <li v-for="(user, idx) in users" :key="user.id" :class="['ranking-item', { top3: idx < 3 }]">
          <!-- 排名 -->
          <span class="rank" :class="`rank-${idx + 1}`">{{ idx + 1 }}</span>
          <!-- 头像 -->
          <el-avatar v-if="user?.user_avatar" :src="user.user_avatar" />
          <el-avatar v-else style="background: #d1e9ff">
            <el-text style="font-weight: 600; color: #1570ef">
              {{ user.user_nick_name_py }}
            </el-text>
          </el-avatar>
          <!-- 信息 -->
          <div class="info">
            <div>
              <el-text truncated size="large" class="name">
                {{ user.user_id }}: {{ user.name || user.user_nick_name }}
              </el-text>
            </div>
            <span class="days">活跃 {{ user?.active_days }} 天</span>
          </div>
          <!-- 徽章（仅前三名） -->
          <span v-if="idx < 3" class="badge">{{ ['🥇', '🥈', '🥉'][idx] }}</span>
        </li>
      </ul>
    </el-scrollbar>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import { getDashboardIndex } from '@/api/dashboard';
import { IUsers } from '@/types/user-center';

// 模拟数据
const props = defineProps({
  height: {
    type: Number,
    default: 300
  }
});
const users = ref<IUsers[]>([]);
const areaHeight = ref(300);

async function getUserActiveDayRank(beginTime: string, companyId: number) {
  const params = {
    index_name: 'user_rank_active_day',
    begin_time: beginTime,
    top: '',
    company_id: companyId
  };
  const res = await getDashboardIndex(params);
  if (!res.error_status) {
    users.value = res.result.active_day_rank;
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
  getUserActiveDayRank
});
</script>

<style scoped>
/* 整体容器 */
.ranking-wrap {
  max-width: 420px;
  margin: 0 auto;
  font-family: 'Segoe UI', sans-serif;
}

.title {
  text-align: center;
  margin-bottom: 16px;
  color: #333;
}

/* 列表 */
.ranking-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.ranking-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 14px;
  margin-bottom: 8px;
  border-radius: 10px;
  background: #f7f7f7;
  transition: transform 0.2s;
}
.ranking-item:hover {
  transform: translateY(-2px);
}

/* 前三名高亮 */
.top3 {
  background: linear-gradient(135deg, #ffa751 0%, #ff8c42 100%);
  box-shadow: 0 4px 12px rgba(255, 140, 66, 0.4);
}
.top3:nth-child(2) {
  background: linear-gradient(135deg, #ffe259 0%, #ffa751 100%);
  color: #fff;
  box-shadow: 0 4px 12px rgba(255, 167, 81, 0.4);
}
.top3:nth-child(3) {
  background: linear-gradient(135deg, #d7d7d7 0%, #b5b5b5 100%);
  box-shadow: 0 4px 12px rgba(181, 181, 181, 0.4);
}

/* 排名数字 */
.rank {
  width: 28px;
  text-align: center;
  font-weight: bold;
  font-size: 18px;
}
.rank-1,
.rank-2,
.rank-3 {
  color: #fff;
}

/* 信息区 */
.info {
  flex: 1;
  display: flex;
  flex-direction: column;
}
.name {
  font-weight: 600;
  font-size: 16px;
  max-width: 250px;
}
.days {
  font-size: 14px;
  opacity: 0.8;
}

/* 徽章 */
.badge {
  font-size: 24px;
}
</style>
