<script setup lang="ts">
import { computed, reactive } from 'vue';
import { ref } from 'vue';
import ConsoleInput from '@/components/next-console/messages-flow/ConsoleInput.vue';
import { consoleInputRef } from '@/components/next-console/messages-flow/console_input';
import router from '@/router';
import { useSessionStore } from '@/stores/sessionStore';
import {useUserInfoStore} from "@/stores/userInfoStore";

const store = useSessionStore();
const userInfoStore = useUserInfoStore()
const recommendArea = reactive([
  {
    title: '联网搜索',
    sub_title: '智能搜索，洞察无限',
    icon: '/images/search_internet.svg',
    url: '/next_console/search'
  },
  {
    title: '知识问答',
    sub_title: '私有知识问答，更懂你的AI助手',
    icon: '/images/knowledge_folder.svg',
    url: '/next_console/knowledge'
  },
  {
    title: 'Agent应用',
    sub_title: '个性支持，专业高效',
    icon: '/images/expert_service.svg',
    url: '/next_console/knowledge'
  },
  {
    title: '更多',
    sub_title: '更多功能，敬请期待',
    icon: '/images/todo_love.svg',
    url: '/next_console/knowledge'
  }
]);
const mainStyle = computed(() => ({
  height: `calc(100vh - ${consoleInputHeight.value}px)`,
  padding: '0 !important'
}));
const moreFeatures = ref(false);
const consoleInputHeight = ref(150);
function handleClickRecommendArea(item: any) {
  if (item.title == '联网搜索') {
    consoleInputRef.value?.switchOnAiSearch();
  } else if (item.title == '知识问答') {
    consoleInputRef.value?.switchOnResourceSearch();
  } else if (item.title == '专家服务') {
    router.push({
      name: 'online_service'
    });
  } else if (item.title == '更多') {
    moreFeatures.value = true;
  }
}
async function handleCreateSession() {
  if (store.getLatestSessionListRef) {
    await store.getLatestSessionListRef();
  }
}
</script>

<template>
  <el-container>
    <el-main :style="mainStyle">
      <div id="center-box">
        <div id="center-area">
          <div id="hello-world">
            <div class="">
              <el-text class="hello-text"> 你好，{{ userInfoStore.userInfo?.user_nick_name }} </el-text>
            </div>
            <div>
              <el-text class="hello-text"> 有问题欢迎随时问我！</el-text>
            </div>
          </div>
          <div id="recommend-area">
            <div
                v-for="item in recommendArea"
                :key="item.title"
                class="recommend-box"
                @click="handleClickRecommendArea(item)"
            >
              <div>
                <el-image :src="item.icon" class="recommend-box-icon" />
              </div>
              <div class="recommend-box-right">
                <div>
                  <el-text class="recommend-box-title">{{ item.title }}</el-text>
                </div>
                <div>
                  <el-text class="recommend-box-sub-title">{{ item.sub_title }}</el-text>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </el-main>
    <el-footer :height="consoleInputHeight.toString() + 'px'">
      <ConsoleInput
          ref="consoleInputRef"
          :height="consoleInputHeight.toString() + 'px'"
          @height-change="args => (consoleInputHeight = args.newHeight)"
          @create-session="args => handleCreateSession()"
      />
    </el-footer>
  </el-container>
</template>

<style scoped>
.std-middle-box {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}
#center-box {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  width: calc(100% - 48px);
  padding: 0 20px;
}
#center-area {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: flex-start;
  gap: 32px;
}
#hello-world {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: flex-start;
  gap: 12px;
  width: 100%;
}
.hello-text {
  font-size: 24px;
  line-height: 32px;
  font-weight: 600;
  color: #101828;
}
#recommend-area {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  max-width: 900px;
  gap: 24px;
}
.recommend-box {
  display: flex;
  flex-direction: row;
  border-radius: 12px;
  padding: 12px;
  gap: 12px;
  border: 1px solid #d0d5dd;
  width: 300px;
  cursor: pointer;
}
.recommend-box-title {
  font-weight: 600;
  font-size: 18px;
  line-height: 28px;
  color: #101828;
  transition: box-shadow 0.3s ease; /* 添加过渡效果 */
}
.recommend-box:hover {
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2); /* 底部立体阴影 */
}
.recommend-box:active {
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.5); /* 更明显的阴影 */
}
.recommend-box-sub-title {
  font-weight: 400;
  font-size: 18px;
  line-height: 28px;
  color: #475467;
}
.feature-item {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 12px;
}
#more-feature-box {
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  gap: 24px;
}
#market_area {
  max-width: 670px;
  cursor: pointer;
  border-radius: 12px;
  overflow: hidden;
}
@media (width < 600px) {
  #hello-world {
    margin-left: 20px;
  }
  #recommend-area {
    gap: 8px;
  }
  .recommend-box {
    width: 100%;
  }
  .recommend-box-title {
    font-size: 16px;
    line-height: 20px;
    font-weight: 600;
  }
  .recommend-box-sub-title {
    font-size: 14px;
  }
}
</style>
