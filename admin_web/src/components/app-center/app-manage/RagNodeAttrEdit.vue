<script setup lang="ts">
import { ArrowDown, ArrowRight, Close, QuestionFilled, Search, SuccessFilled } from '@element-plus/icons-vue';
import { nextTick, ref } from 'vue';
import { nodeUpdate } from '@/api/app-center-api';
import TemplateEditor from '@/components/app-center/app-manage/TemplateEditor.vue';
import ResourcesSearch from '@/components/app-center/app-preview/ResourcesSearch.vue';

import { useAppStore } from '@/stores/app-store';
import { useWorkflowStore } from '@/stores/workflow-store';
const appInfoStore = useAppStore();
const workflowStore = useWorkflowStore();
const showRagConfigFlag = ref(false);
const showRagConfigKgFlag = ref(false);
const showRagConfigRerankFlag = ref(false);
const showRagConfigWebFlag = ref(false);
const resourcesSearchRef = ref();
const resourceSearchDialogShow = ref(false);

function fixResourceIcon(url: string) {
  if (!url.includes('/images/') && !url.includes('http')) {
    return '/images/' + url;
  }
  return url;
}
async function removeResource(id: string | number) {
  const targetResource = workflowStore.currentNodeDetail.node_rag_resources.find(item => item.id === id);
  if (targetResource) {
    workflowStore.currentNodeDetail.node_rag_resources = workflowStore.currentNodeDetail.node_rag_resources.filter(
      item => item.id !== id
    );
    nodeUpdate({
      app_code: appInfoStore.currentApp.app_code,
      node_code: workflowStore.currentNodeDetail.node_code,
      node_rag_resources: workflowStore.currentNodeDetail.node_rag_resources
    });
  }
}
async function updateNodePrompt() {
  nodeUpdate({
    app_code: appInfoStore.currentApp.app_code,
    node_code: workflowStore.currentNodeDetail.node_code,
    node_llm_system_prompt_template: workflowStore.currentNodeDetail.node_llm_system_prompt_template,
    node_llm_user_prompt_template: workflowStore.currentNodeDetail.node_llm_user_prompt_template
  });
}
async function handleTemplateChange(newValue, src = '') {
  if (src == 'node_llm_system_prompt_template') {
    workflowStore.currentNodeDetail.node_llm_system_prompt_template = newValue;
    updateNodePrompt();
  } else if (src == 'node_llm_user_prompt_template') {
    workflowStore.currentNodeDetail.node_llm_user_prompt_template = newValue;
    updateNodePrompt();
  } else if (src == 'node_rag_query_template') {
    workflowStore.currentNodeDetail.node_rag_query_template = newValue;
    updateNodeRagConfig();
  }
}
async function updateNodeRagConfig() {
  nodeUpdate({
    app_code: appInfoStore.currentApp.app_code,
    node_code: workflowStore.currentNodeDetail.node_code,
    node_rag_resources: workflowStore.currentNodeDetail.node_rag_resources,
    node_rag_query_template: workflowStore.currentNodeDetail.node_rag_query_template,
    node_rag_recall_config: workflowStore.currentNodeDetail.node_rag_recall_config,
    node_rag_rerank_config: workflowStore.currentNodeDetail.node_rag_rerank_config,
    node_rag_web_search_config: workflowStore.currentNodeDetail.node_rag_web_search_config,
    node_rag_ref_show: workflowStore.currentNodeDetail.node_rag_ref_show
  });
}
async function commitAddChooseResources() {
  resourceSearchDialogShow.value = false;
  const pickResources = resourcesSearchRef.value?.getSelectedResources();
  for (const resource of pickResources) {
    if (!workflowStore.currentNodeDetail.node_rag_resources) {
      workflowStore.currentNodeDetail.node_rag_resources = [];
    }
    const existingResource = workflowStore.currentNodeDetail.node_rag_resources.find(item => item.id === resource.id);
    if (!existingResource) {
      workflowStore.currentNodeDetail.node_rag_resources.push(resource);
    }
  }
  nodeUpdate({
    app_code: appInfoStore.currentApp.app_code,
    node_code: workflowStore.currentNodeDetail.node_code,
    node_rag_resources: workflowStore.currentNodeDetail.node_rag_resources
  });
  resourceSearchDialogShow.value = false;
  await nextTick();
}
</script>

<template>
  <div v-if="workflowStore.currentNodeDetail?.node_type == 'rag'" class="config-item">
    <div class="config-head">
      <div class="std-middle-box">
        <el-icon v-if="showRagConfigKgFlag" class="config-arrow" @click="showRagConfigKgFlag = false">
          <ArrowDown />
        </el-icon>
        <el-icon v-else class="config-arrow" @click="showRagConfigKgFlag = true">
          <ArrowRight />
        </el-icon>
      </div>
      <div class="std-middle-box">
        <el-text> 知识库选择 </el-text>
      </div>
      <div>
        <el-tooltip content="配置知识来源">
          <el-icon>
            <QuestionFilled />
          </el-icon>
        </el-tooltip>
      </div>
    </div>
    <div v-show="showRagConfigKgFlag" class="config-area">
      <div>
        <el-form label-position="top">
          <el-form-item label="查询语句" style="padding: 0 12px">
            <TemplateEditor
              id="node_rag_query_template"
              :value="workflowStore.currentNodeDetail.node_rag_query_template"
              style="width: 100%"
              placeholder="请输入需要查询知识的语句，如选择系统变量USER_INPUT"
              :node="workflowStore.currentNodeDetail"
              @update:value="newValue => handleTemplateChange(newValue, 'node_rag_query_template')"
            />
          </el-form-item>
          <el-form-item label="召回知识库" style="padding: 0 12px">
            <div class="rag-area">
              <div class="rag-title">
                <el-button :icon="Search" round style="width: 100%" @click="resourceSearchDialogShow = true">
                  搜索知识库
                </el-button>
              </div>
              <div class="rag-body">
                <div
                  v-for="item in workflowStore.currentNodeDetail?.node_rag_resources"
                  :key="item.id"
                  class="resource-item"
                >
                  <div class="resource-item-left">
                    <div class="resource-status">
                      <el-icon style="color: green">
                        <SuccessFilled />
                      </el-icon>
                    </div>
                    <div class="resource-icon">
                      <el-image :src="fixResourceIcon(item?.resource_icon)" />
                    </div>
                    <div class="resource-title">
                      <el-text truncated>
                        {{ item?.resource_name }}
                      </el-text>
                    </div>
                  </div>
                  <div class="resource-remove">
                    <el-button :icon="Close" round @click="removeResource(item?.id)" />
                  </div>
                </div>
              </div>
            </div>
          </el-form-item>
        </el-form>
      </div>
    </div>
  </div>
  <div v-if="workflowStore.currentNodeDetail?.node_type == 'rag'" class="config-item">
    <div class="config-head">
      <div class="std-middle-box">
        <el-icon v-if="showRagConfigFlag" class="config-arrow" @click="showRagConfigFlag = false">
          <ArrowDown />
        </el-icon>
        <el-icon v-else class="config-arrow" @click="showRagConfigFlag = true">
          <ArrowRight />
        </el-icon>
      </div>
      <div class="std-middle-box">
        <el-text> 召回设置 </el-text>
      </div>
      <div>
        <el-tooltip content="调用向量模型匹配最佳参考知识">
          <el-icon>
            <QuestionFilled />
          </el-icon>
        </el-tooltip>
      </div>
    </div>
    <div v-show="showRagConfigFlag" class="config-area">
      <el-form :model="workflowStore.currentNodeDetail" label-position="top">
        <el-form-item label="相似度度量方法" style="padding: 0 12px">
          <el-select
            v-model="workflowStore.currentNodeDetail.node_rag_recall_config.recall_similarity"
            @change="updateNodeRagConfig"
          >
            <el-option value="ip" label="最大内积" />
            <el-option value="cosine" label="余弦相似度" />
          </el-select>
        </el-form-item>
        <el-form-item label="召回阈值" style="padding: 0 12px">
          <el-slider
            v-model="workflowStore.currentNodeDetail.node_rag_recall_config.recall_threshold"
            show-input
            :show-input-controls="false"
            :min="0"
            :max="1"
            :step="0.01"
            @change="updateNodeRagConfig"
          />
        </el-form-item>
        <el-form-item label="最大召回数" style="padding: 0 12px">
          <el-input-number
            v-model="workflowStore.currentNodeDetail.node_rag_recall_config.recall_k"
            :min="1"
            :max="500"
            @change="updateNodeRagConfig"
          />
        </el-form-item>
      </el-form>
    </div>
  </div>
  <div v-if="workflowStore.currentNodeDetail?.node_type == 'rag'" class="config-item">
    <div class="config-head">
      <div class="std-middle-box">
        <el-icon v-if="showRagConfigRerankFlag" class="config-arrow" @click="showRagConfigRerankFlag = false">
          <ArrowDown />
        </el-icon>
        <el-icon v-else class="config-arrow" @click="showRagConfigRerankFlag = true">
          <ArrowRight />
        </el-icon>
      </div>
      <div class="std-middle-box">
        <el-text> 重排序设置 </el-text>
      </div>
      <div>
        <el-tooltip content="调用重排序模型对召回结果进行精排序">
          <el-icon>
            <QuestionFilled />
          </el-icon>
        </el-tooltip>
      </div>
    </div>
    <div v-show="showRagConfigRerankFlag" class="config-area">
      <el-form :model="workflowStore.currentNodeDetail" label-position="top">
        <el-form-item label="启用重排序" style="padding: 0 12px">
          <el-switch
            v-model="workflowStore.currentNodeDetail.node_rag_rerank_config.rerank_enabled"
            @change="updateNodeRagConfig"
          />
        </el-form-item>
        <el-form-item label="文档中生成的最大块数" style="padding: 0 12px">
          <el-input-number
            v-model="workflowStore.currentNodeDetail.node_rag_rerank_config.max_chunk_per_doc"
            :disabled="!workflowStore.currentNodeDetail.node_rag_rerank_config.rerank_enabled"
            @change="updateNodeRagConfig"
          />
        </el-form-item>
        <el-form-item label="标记重叠数量" style="padding: 0 12px">
          <el-input-number
            v-model="workflowStore.currentNodeDetail.node_rag_rerank_config.overlap_tokens"
            :min="1"
            :max="80"
            :disabled="!workflowStore.currentNodeDetail.node_rag_rerank_config.rerank_enabled"
            @change="updateNodeRagConfig"
          />
        </el-form-item>
        <el-form-item label="召回阈值" style="padding: 0 12px">
          <el-slider
            v-model="workflowStore.currentNodeDetail.node_rag_rerank_config.rerank_threshold"
            :disabled="!workflowStore.currentNodeDetail.node_rag_rerank_config.rerank_enabled"
            show-input
            :show-input-controls="false"
            :min="0"
            :max="1"
            :step="0.01"
            @change="updateNodeRagConfig"
          />
        </el-form-item>
        <el-form-item label="最大召回数" style="padding: 0 12px">
          <el-input-number
            v-model="workflowStore.currentNodeDetail.node_rag_rerank_config.rerank_k"
            :disabled="!workflowStore.currentNodeDetail.node_rag_rerank_config.rerank_enabled"
            :min="1"
            :max="500"
            @change="updateNodeRagConfig"
          />
        </el-form-item>
      </el-form>
    </div>
  </div>
  <div v-if="workflowStore.currentNodeDetail?.node_type == 'rag'" class="config-item">
    <div class="config-head">
      <div class="std-middle-box">
        <el-icon v-if="showRagConfigWebFlag" class="config-arrow" @click="showRagConfigWebFlag = false">
          <ArrowDown />
        </el-icon>
        <el-icon v-else class="config-arrow" @click="showRagConfigWebFlag = true">
          <ArrowRight />
        </el-icon>
      </div>
      <div class="std-middle-box">
        <el-text class="config-head-text"> 联网搜索设置 </el-text>
      </div>
      <div>
        <el-tooltip content="调用搜索引擎补充实时网页数据">
          <el-icon>
            <QuestionFilled />
          </el-icon>
        </el-tooltip>
      </div>
    </div>
    <div v-show="showRagConfigWebFlag" class="config-area">
      <el-form :model="workflowStore.currentNodeDetail" label-position="top">
        <el-form-item label="启用联网搜索" style="padding: 0 12px">
          <el-switch
            v-model="workflowStore.currentNodeDetail.node_rag_web_search_config.search_engine_enhanced"
            @change="updateNodeRagConfig"
          />
        </el-form-item>
        <el-form-item label="最大返回网页数" style="padding: 0 12px">
          <el-input-number
            v-model="workflowStore.currentNodeDetail.node_rag_web_search_config.num"
            :disabled="!workflowStore.currentNodeDetail.node_rag_web_search_config.search_engine_enhanced"
            :min="1"
            :max="50"
            @change="updateNodeRagConfig"
          />
        </el-form-item>
        <el-form-item label="最大超时" style="padding: 0 12px">
          <el-slider
            v-model="workflowStore.currentNodeDetail.node_rag_web_search_config.timeout"
            :disabled="!workflowStore.currentNodeDetail.node_rag_web_search_config.search_engine_enhanced"
            :min="1"
            :max="60"
            show-input
            :show-input-controls="false"
            :step="1"
            @change="updateNodeRagConfig"
          />
        </el-form-item>
      </el-form>
    </div>
  </div>

  <ResourcesSearch
    v-if="workflowStore.currentNodeDetail.node_type == 'rag'"
    ref="resourcesSearchRef"
    :model="resourceSearchDialogShow"
    @close="resourceSearchDialogShow = false"
    @commit="
      args => {
        commitAddChooseResources();
      }
    "
  />
</template>

<style scoped>
.std-middle-box {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: row;
}
.config-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 6px;
  border-bottom: 1px solid #f0f0f0;
}
.config-head {
  display: flex;
  flex-direction: row;
  gap: 6px;
  align-items: center;
  justify-content: flex-start;
  padding: 6px;
}
.config-arrow {
  cursor: pointer;
  width: 12px;
  height: 12px;
}
.config-area {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.rag-area {
  display: flex;
  flex-direction: column;
  gap: 4px;
  width: 100%;
}
.rag-body {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.resource-item {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  gap: 4px;
  width: calc(100% - 24px);
  height: 40px;
  padding: 4px 12px;
  background-color: #eff8ff;
  border-radius: 8px;
}
.resource-item-left {
  display: flex;
  flex-direction: row;
  gap: 8px;
}
.resource-icon {
  width: 24px;
  height: 24px;
}
</style>
