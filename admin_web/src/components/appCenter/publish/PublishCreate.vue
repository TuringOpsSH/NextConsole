<script setup lang="ts">
import { Back, Location } from '@element-plus/icons-vue';
import { ElMessage } from 'element-plus';
import { defineProps, onMounted, reactive, ref } from 'vue';

import { publishCreate } from '@/api/appCenterApi';
import router from '@/router';
const newPublish = reactive({
  appCode: '',
  publishName: '',
  publishDesc: '',
  publishConfig: {
    connectors: [
      {
        id: 1,
        name: 'NextConsole智能体服务平台',
        icon: 'images/logo.svg',
        desc: '智能应用将会可以在NextConsole智能体服务平台上进行直接使用~',
        status: '已授权',
        type: 'connector',
        picked: false,
        able: true
      },
      {
        id: 2,
        name: 'NC-API',
        icon: 'images/logo.svg',
        desc: '智能应用将提供对外API',
        status: '已授权',
        type: 'connector',
        picked: false,
        able: false
      },
      {
        id: 3,
        name: 'NC-SDK',
        icon: 'images/logo.svg',
        desc: '智能应用将提供可嵌入的前端SDK',
        status: '已授权',
        type: 'connector',
        picked: false,
        able: false
      },
      {
        id: 4,
        name: '微信',
        icon: 'images/wx_logo.svg',
        desc: '智能应用将会可以在微信上进行直接使用~',
        status: '已授权',
        type: 'connector',
        picked: false,
        able: false
      },
      {
        id: 5,
        name: '企业微信',
        icon: 'images/qy_wx_logo.svg',
        desc: '智能应用将会可以在企业微信上进行直接使用~',
        status: '已授权',
        type: 'connector',
        picked: false,
        able: false
      },
      {
        id: 6,
        name: '飞书',
        icon: 'images/feishu_logo.svg',
        desc: '智能应用将会可以在飞书中进行直接使用~',
        status: '已授权',
        type: 'connector',
        picked: false,
        able: false
      },
      {
        id: 7,
        name: '钉钉',
        icon: 'images/ding_ding_logo.svg',
        desc: '智能应用将会可以在钉钉中进行直接使用~',
        status: '已授权',
        type: 'connector',
        picked: false,
        able: false
      },
      {
        id: 8,
        name: '抖音',
        icon: 'images/douyin_logo.jpg',
        desc: '智能应用将会可以在抖音中进行直接使用~',
        status: '已授权',
        type: 'connector',
        picked: false,
        able: false
      }
    ]
  }
});
const prop = defineProps({
  appCode: {
    type: String,
    default: ''
  }
});
const publishFormRef = ref();
const publishing = ref(false);
const rules = {
  publishName: [
    {
      required: true,
      message: '请输入发布名称',
      trigger: 'blur'
    },
    {
      max: 100,
      message: '发布名称过长',
      trigger: 'blur'
    }
  ],
  publishDesc: [
    {
      required: false,
      message: '请输入发布描述',
      trigger: 'blur'
    },
    {
      max: 2500,
      message: '发布描述过长',
      trigger: 'blur'
    }
  ],
  publishConfig: [
    {
      required: true,
      message: '请选择发布渠道',
      trigger: 'blur'
    },
    {
      validator: (rule, value, callback) => {
        if (newPublish.publishConfig.connectors.every(item => !item.picked)) {
          callback(new Error('请选择发布渠道'));
        } else {
          callback();
        }
      },
      trigger: 'blur',
      message: '请选择发布渠道'
    }
  ]
};
onMounted(async () => {
  if (!prop.appCode) {
    await router.push({
      name: 'publishList'
    });
  }
  newPublish.appCode = prop.appCode;
});
async function createNewPublish() {
  // 表单验证
  const valid = await publishFormRef.value?.validate();
  if (!valid) {
    return;
  }
  const params = {
    app_code: newPublish.appCode,
    publish_name: newPublish.publishName,
    publish_desc: newPublish.publishDesc,
    publish_config: newPublish.publishConfig
  };
  publishing.value = true;
  const res = await publishCreate(params);
  if (!res.error_status) {
    if (res.result?.publish_status != '成功') {
      ElMessage.error('发布失败');
      return;
    }
    ElMessage.success('发布成功');
    await router.push({
      name: 'publishList'
    });
  }
  publishing.value = false;
}
</script>

<template>
  <el-container>
    <el-header style="padding: 0">
      <div class="publish-head">
        <div class="publish-head-left">
          <div><el-button text :icon="Back" @click="$router.back()" /></div>
          <div><h3>新的发布</h3></div>
        </div>
        <div class="publish-head-right">
          <el-popconfirm title="确认发布至该渠道？生产环境版本将会自动替换！" @confirm="createNewPublish">
            <template #reference>
              <el-button type="primary" size="large"> 确认发布 </el-button>
            </template>
          </el-popconfirm>
        </div>
      </div>
    </el-header>
    <el-main>
      <div v-loading="publishing" element-loading-text="努力发布中..." class="publish-form-area">
        <el-form ref="publishFormRef" :model="newPublish" label-position="top" class="publish-form" :rules="rules">
          <el-form-item label="发布名称" prop="publishName" required>
            <el-input v-model="newPublish.publishName" placeholder="请输入发布名称" />
          </el-form-item>
          <el-form-item label="发布描述" prop="publishDesc">
            <el-input v-model="newPublish.publishDesc" placeholder="请输入发布说明" type="textarea" :rows="12" />
          </el-form-item>
          <el-form-item label="发布渠道" prop="publishConfig">
            <div class="connectors-area">
              <div v-for="connector in newPublish.publishConfig.connectors" :key="connector.id" class="connector-item">
                <div class="connector-item-left">
                  <div class="connector-item-type">
                    <div>
                      <el-checkbox v-model="connector.picked" size="large" :disabled="!connector.able" />
                    </div>
                    <div>
                      <el-image shape="circle" :src="connector.icon" style="width: 36px; height: 36px" />
                    </div>
                    <div>
                      <el-text class="connector-name" :style="{ color: connector.picked ? '#000' : '#999' }">
                        {{ connector.name }}
                      </el-text>
                    </div>
                    <div>
                      <el-tooltip class="connector-desc" :content="connector.desc">
                        <el-icon>
                          <Location />
                        </el-icon>
                      </el-tooltip>
                    </div>
                  </div>
                  <div class="connector-item-tags">
                    <el-tag type="primary"> {{ connector.status }} </el-tag>
                  </div>
                </div>

                <div class="connector-item-right">
                  <el-button text type="primary" disabled> 配置 </el-button>
                </div>
              </div>
            </div>
          </el-form-item>
        </el-form>
      </div>
    </el-main>
  </el-container>
</template>

<style scoped>
.publish-head {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  padding: 12px;
  border-bottom: 1px solid #f0f0f0;
}
.publish-head-left {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  gap: 4px;
}
.publish-form-area {
  height: calc(100vh - 200px);
  width: 100%;
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  justify-content: center;
}
.publish-form {
  max-width: 600px;
  width: 100%;
  margin-top: 40px;
}
.connectors-area {
  display: flex;
  flex-direction: column;
  gap: 6px;
  width: 100%;
}
.connector-item {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  width: 100%;
}
.connector-item-left {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 12px;
}
.connector-item-type {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 12px;
  width: 250px;
}
</style>
