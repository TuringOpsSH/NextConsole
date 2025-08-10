<script setup lang="ts">
import {ResourceItem} from "@/types/resource_type";
import {reactive, ref, watch, onMounted} from 'vue';
import {
  resource_chunk_recall,
  resource_chunk_update,
  resource_chunks_delete,
  resource_chunks_get
} from "@/api/resource_api";
import MarkdownIt from "markdown-it";
import hljs from "highlight.js";
import markdownItKatex from "@vscode/markdown-it-katex";
import markdownItMermaid from "markdown-it-mermaid-plugin";
import MarkdownTasks from "markdown-it-task-lists";
import {ElMessage} from "element-plus";
import * as echarts from 'echarts';

const props = defineProps({
  resourceId: {
    type: Number,
    default: 0,
    required: true
  },
})
const currentViewResource = reactive<ResourceItem>(
    // @ts-ignore
    {
      sub_rag_file_cnt: 0,
      id: null,
      resource_parent_id: null,
      user_id: null,
      resource_name: null,
      resource_type: null,
      resource_desc: null,
      resource_icon: null,
      resource_format: null,
      resource_path: null,
      resource_size_in_MB: null,
      resource_status: null,
      rag_status: null,
      create_time: null,
      update_time: null,
      delete_time: null,
      show_buttons: null,
      resource_parent_name: null,
      resource_is_selected: null,
      sub_resource_dir_cnt: null,
      sub_resource_file_cnt: null,
      resource_feature_code: '',
      resource_is_supported: false,
      resource_show_url: '',
      resource_source_url: '',
      resource_title: '',
      resource_source: 'resource_center',
      ref_text: null,
      rerank_score: null,
      view_config: {},
      chunks: null
    }
);
const resourceViewerLoading = ref(false);
const currentChunkIndex = reactive({
  chunk_id: 0,
  chunk_raw_content: '',
  chunk_embedding_content: '',
  chunk_embedding_type: '',
  chunk_embedding: [],
  chunk_size: 0,
  chunk_hit_counts: 0,
  chunk_pane: 'chunk_content',
  test_question: '',
  chart: null,
  status: '正常',
})
const showEditRawContentDialog = ref(false);
const showEditEmbeddingContentDialog = ref(false);
const showEditEmbeddingDialog = ref(false);
const rawContentFormRef = ref(null);
const rawEmbeddingContentFormRef = ref(null);
const rawEmbeddingFormRef = ref(null);
const chunkTestFormRef = ref(null);
let mdAnswer = new MarkdownIt({
  html: true,
  linkify: true,
  typographer: true,
  breaks: true,
  highlight: function (str, lang) {
    let language = lang ? lang : 'plaintext';
    let languageText = '<span style="">' + language + '</span>';
    let copyButton =
        '<img src="images/copy.svg" alt="复制" class="answer-code-copy" style="width: 20px;height: 20px;cursor: pointer"/>';
    let header =
        '<div style="display: flex;justify-content: space-between;border-bottom: 1px solid #D0D5DD;padding: 8px">' +
        languageText +
        copyButton +
        '</div>';

    if (hljs.getLanguage(language)) {
      try {
        return (
            '<pre class="hljs" style="white-space: pre-wrap; overflow: auto ; position: relative;' +
            'border-bottom: 1px solid #D0D5DD;padding: 16px">' +
            header +
            '<code class="hljs-code" >' +
            '<br>' +
            hljs.highlight(str, { language: language, ignoreIllegals: true }).value +
            '<br>' +
            '</code></pre>'
        );
      } catch (__) {}
    }

    return (
        '<pre class="hljs" style="white-space: pre-wrap; overflow: auto ; position: relative;' +
        'border-bottom: 1px solid #D0D5DD;padding: 16px">' +
        header +
        '<code class="hljs-code" >' +
        '<br>' +
        hljs.highlight(str, { language: 'plaintext', ignoreIllegals: true }).value +
        '<br>' +
        '</code></pre>'
    );
  }
});
const defaultTableRule =
    mdAnswer.renderer.rules.table_open ||
    function (tokens, idx, options, env, self) {
      return self.renderToken(tokens, idx, options);
    };
mdAnswer.renderer.rules.table_open = function (tokens, idx, options, env, self) {
  tokens[idx].attrPush(['class', 'custom-table']);
  return defaultTableRule(tokens, idx, options, env, self);
};
mdAnswer.use(markdownItKatex, {
  throwOnError: false,
  errorColor: ' #cc0000',
  strict: false // 允许非标准语法
});
mdAnswer.use(markdownItMermaid);
const customTableStyle = `
    <style>
    .custom-table {
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 1rem;
    }
    .custom-table th, .custom-table td {
        border: 1px solid #D0D5DD;
        padding: 8px;
        text-align: left;
    }
    .custom-table th {
        background-color: #f2f2f2;
    }
    </style>
`;
document.head.insertAdjacentHTML('beforeend', customTableStyle);
mdAnswer.renderer.rules.image = function (tokens, idx, options, env, self) {
  const token = tokens[idx];
  const src = token.attrGet('src');
  const alt = token.content;
  const title = token.attrGet('title');
  const isLast = env.is_last;
  const imgHtml = `<img src="${src}" alt="${alt}" title="${title}" style="max-width: 100%">`;

  if (isLast) {
    return ` <div style="text-align: center;">${src}</div> `;
  }

  return ` <div style="text-align: center;">${imgHtml}</div> `;
};
// 自定义链接样式
mdAnswer.renderer.rules.link_open = function (tokens, idx, options, env, self) {
  const aIndex = tokens[idx].attrIndex('target');

  if (aIndex < 0) {
    tokens[idx].attrPush(['target', '_blank']); // 添加 target="_blank"
  } else {
    tokens[idx].attrs[aIndex][1] = '_blank';
  }
  return self.renderToken(tokens, idx, options);
};
// 自定义引用样式
mdAnswer.renderer.rules.blockquote_open = function (tokens, idx, options, env, self) {
  tokens[idx].attrSet('class', 'my-custom-quote');
  return self.renderToken(tokens, idx, options);
};
// 任务列表
mdAnswer.use(MarkdownTasks);
async function initResourceIndexer() {
  resourceViewerLoading.value = true;
  try {
    const res = await resource_chunks_get({
      resource_id: currentViewResource.id,
      show_index: true
    });
    if (!res.error_message) {
      currentViewResource.chunks = res.result;
      currentViewResource.chunks.forEach((chunk) => {
        chunk.chunk_pane = 'chunk_raw_content';
      });
    } else {
      console.error(res.error_message);
    }
  } catch (error) {
    console.error('Error fetching resource chunks:', error);
  } finally {
    resourceViewerLoading.value = false;
  }
}
function renderMarkdown(chunk_content: string): string {
  if (!chunk_content) {
    return '<div class="std-middle-box"><div class="view-area">暂无内容</div></div>';
  }
  return mdAnswer.render(chunk_content);
}
async function handleDeleteRawChunk(chunk_id: number) {
  const res = await resource_chunks_delete({
    chunk_ids : [chunk_id],
  })
  if (!res.error_status) {
    ElMessage.success('删除分段成功');
    // 重新加载分段数据
    await initResourceIndexer();
    return;
  }
}
async function handleSwitchRawChunk(chunk_id: number, status: string) {
  const res = await resource_chunk_update({
    chunk_id : chunk_id,
    chunk_status: status
  })
  if (!res.error_status) {
    ElMessage.success(`分段状态已更新为 ${status}`);
    // 重新加载分段数据
    await initResourceIndexer();
    return;
  }
}
async function handleBeginUpdateChunk(chunk) {

  currentChunkIndex.chunk_id = chunk.chunk_id;
  currentChunkIndex.chunk_raw_content = chunk.chunk_raw_content;
  currentChunkIndex.chunk_embedding_content = chunk.chunk_embedding_content;
  currentChunkIndex.chunk_embedding = chunk.chunk_embedding;
  currentChunkIndex.chunk_pane = chunk.chunk_pane ;
  if (currentChunkIndex.chunk_pane == "chunk_raw_content") {
    showEditRawContentDialog.value = true;
  }
  else if (currentChunkIndex.chunk_pane == "chunk_embedding_content") {
    showEditEmbeddingContentDialog.value = true;
  }
  else if (currentChunkIndex.chunk_pane == "chunk_embedding") {
    showEditEmbeddingDialog.value = true;
  }

}
async function confirmUpdateChunk() {
  try {
    const validResponse = await rawContentFormRef.value?.validate();
    if (!validResponse) {
      return;
    }
  } catch (e) {
    return;
  }
  const res = await resource_chunk_update({
    chunk_id: currentChunkIndex.chunk_id,
    chunk_raw_content: currentChunkIndex.chunk_raw_content
  });
  if (!res.error_status) {
    ElMessage.success('嵌入分段内容更新成功！');
    showEditRawContentDialog.value = false;
    // 重新加载分段数据
    await initResourceIndexer();
    return;
  } else {
    ElMessage.error('嵌入分段内容更新失败: ' + res.error_message);
  }
  showEditRawContentDialog.value = false;
}
async function confirmUpdateEChunk() {
  try {
    const validResponse = await rawEmbeddingContentFormRef.value?.validate();
    if (!validResponse) {
      return;
    }
  } catch (e) {
    return;
  }
  const res = await resource_chunk_update({
    chunk_id: currentChunkIndex.chunk_id,
    chunk_embedding_content: currentChunkIndex.chunk_embedding_content
  });
  if (!res.error_status) {
    ElMessage.success('嵌入分段内容更新成功！');
    showEditEmbeddingContentDialog.value = false;
    // 重新加载分段数据
    await initResourceIndexer();
    return;
  } else {
    ElMessage.error('嵌入分段内容更新失败: ' + res.error_message);
  }
  showEditEmbeddingContentDialog.value = false;
}
async function confirmUpdateEmbedding() {
  try {
    const validResponse = await rawEmbeddingFormRef.value?.validate();
    if (!validResponse) {
      return;
    }
  } catch (e) {
    return;
  }
  const res = await resource_chunk_update({
    chunk_id: currentChunkIndex.chunk_id,
    chunk_embedding: currentChunkIndex.chunk_embedding
  });
  if (!res.error_status) {
    ElMessage.success('嵌入向量更新成功！');
    showEditEmbeddingDialog.value = false;
    // 重新加载分段数据
    await initResourceIndexer();
    return;
  } else {
    ElMessage.error('嵌入向量更新失败: ' + res.error_message);
  }
  showEditEmbeddingDialog.value = false;
}
function translateSplitMethod(splitMethod: string): string {
  switch (splitMethod) {
    case 'length':
      return '长度切分';
    case 'layout':
      return '布局切分';
    case 'symbol':
      return '分隔符切分';
    case 'custom':
      return '自定义分割器';
    default:
      return splitMethod;
  }
}
function ValidNewEmbedding(rule, value, callback) {
  if (typeof value === 'object') {
    // 检查数组中的每个元素是否都是有效的数字
    for (let i = 0; i < value.length; i++) {
      const num = parseFloat(value[i]);
      if (isNaN(num)) {
        callback(new Error('嵌入向量中的每个元素都必须是有效的数字'));
        return;
      }
    }

    // 检查数组的长度是否等于 1024
    if (value.length!== 1024) {
      callback(new Error('嵌入向量的维度必须等于 1024'));
      return;
    }
    callback();
    return;
  }
  console.log(value, typeof value);

  // 检查值是否由数字和逗号组成
  if (!/^[0-9.,-]+$/.test(value)) {
    callback(new Error('嵌入向量只能由数字和逗号组成'));
    return;
  }
  // 将字符串按逗号分割成数组
  const vectorArray = value.split(',');
  // 检查数组的长度是否等于 1024
  if (vectorArray.length!== 1024) {
    callback(new Error('嵌入向量的维度必须等于 1024'));
    return;
  }
  // 检查数组中的每个元素是否都是有效的数字
  for (let i = 0; i < vectorArray.length; i++) {
    const num = parseFloat(vectorArray[i]);
    if (isNaN(num)) {
      callback(new Error('嵌入向量中的每个元素都必须是有效的数字'));
      return;
    }
  }
  // 如果所有检查都通过，则调用回调函数表示验证通过
  callback();
}
async function handleTestChunk(chunk) {
  const res = await resource_chunk_recall({
    chunk_id: chunk.chunk_id,
    query_text: chunk.test_question
  });
  if (!res.error_status) {
    chunk.test_score = res.result.similarity_score;
    if (!chunk.chart) {
      await initChart(chunk);
    }
    chunk.chart.setOption({
      series: [{
        data: [{ value: chunk.test_score, name: '相似度' }]
      }]
    });
    ElMessage.success('测试成功，分段内容召回评分：' + chunk.test_score);
  } else {
    ElMessage.error('测试失败: ' + res.error_message);
  }
}
async function initChart(chunk) {
  const chartDom = document.getElementById(chunk.chunk_id.toString());
  if (!chartDom) {
    console.error('Chart container not found for chunk_id:', chunk_id);
    return;
  }
  const chart = echarts.init(chartDom);
  chunk.chart = chart;
  // 配置项
  const option = {
    series: [
      {
        type: 'gauge',
        min: 0,
        max: 1,
        axisLine: {
          lineStyle: {
            width: 6,
            color: [
              [0.5, '#FF6E76'],
              [0.65, '#FDDD60'],
              [0.75, '#58D9F9'],
              [1, '#7CFFB2']
            ]
          }
        },
        data: [{ value: 0  }]
      }
    ],
    graphic: [
      {
        type: 'rect',
        left: '5%',
        top: '80%',
        shape: { width: 15, height: 15 },
        style: { fill: '#FF6E76' }
      },
      {
        type: 'text',
        left: '12%',
        top: '80%',
        style: {
          text: '0.5以下: 基本不相关（如"猫"和"建筑"）',
          font: '12px "Microsoft YaHei"',
          fill: '#666'
        }
      },
      {
        type: 'rect',
        left: '5%',
        top: '85%',
        shape: { width: 15, height: 15 },
        style: { fill: '#FDDD60' }
      },
      {
        type: 'text',
        left: '12%',
        top: '85%',
        style: {
          text: '0.5 - 0.65: 弱相关（如"猫"和"宠物"）',
          font: '12px "Microsoft YaHei"',
          fill: '#666'
        }
      },
      {
        type: 'rect',
        left: '5%',
        top: '90%',
        shape: { width: 15, height: 15 },
        style: { fill: '#58D9F9' }
      },
      {
        type: 'text',
        left: '12%',
        top: '90%',
        style: {
          text: '0.65 - 0.75: 主题相关（如"机器学习"和"深度学习"）',
          font: '12px "Microsoft YaHei"',
          fill: '#666'
        }
      },
      {
        type: 'rect',
        left: '5%',
        top: '95%',
        shape: { width: 15, height: 15 },
        style: { fill: '#7CFFB2' }
      },
      {
        type: 'text',
        left: '12%',
        top: '95%',
        style: {
          text: '0.75+: 同义/高度相关（如"AI"和"人工智能"）',
          font: '12px "Microsoft YaHei"',
          fill: '#666'
        }
      }
    ]
  };

  // 设置配置项
  chart.setOption(option);

  // 窗口大小改变时调整图表大小
  window.addEventListener('resize', () => {
    chart.resize();
  });
}
watch(
    () => props.resourceId,
    async (newResourceID) => {
      currentViewResource.id = newResourceID;
    },
    {
      immediate: true,
      deep: true
    }
);
defineExpose({
  initResourceIndexer
});
</script>

<template>
  <el-scrollbar>
    <div v-loading="resourceViewerLoading" element-loading-text="加载中" style="height: 100%" class="chunk-main">
      <div class="chunk-box" v-for="(chunk, idx) in currentViewResource?.chunks" :key="chunk.chunk_id">
        <div class="chunk-info" >
          <div class="chunk-info-text">
            <el-tag>编号: {{ chunk.chunk_id }}</el-tag>
            <el-tag>命中次数: {{ chunk.chunk_hit_counts }}</el-tag>
            <el-tag :type="chunk.chunk_size < 20 ? 'primary' : 'warning'">大小: {{ chunk.chunk_size }}KB</el-tag>
            <el-tag>切分算法: {{ translateSplitMethod(chunk.split_method) }}</el-tag>
            <el-tag>向量类型: {{ chunk.chunk_embedding_type }}</el-tag>
            <el-tag>向量维度: {{ chunk.chunk_embedding_length }}</el-tag>
          </div>
          <div class="chunk-manage-buttons">
            <el-button text type="primary" @click="handleBeginUpdateChunk(chunk)"
                       v-show="chunk.chunk_pane != 'chunk_embedding_test'">
              编辑
            </el-button>
            <el-popconfirm title="确认删除此分段，此操作无法撤销！" confirm-button-type="danger"
                           @confirm="(e: MouseEvent) => handleDeleteRawChunk(chunk.chunk_id)"
                           cancel-button-text="取消" confirm-button-text="删除"
            >
              <template #reference>
                <el-button text type="danger">删除</el-button>
              </template>
            </el-popconfirm>
            <el-popconfirm v-if = "chunk.status == '正常'"
                           title="确认暂时禁用此分段？" confirm-button-type="warning"

                           @confirm="(e: MouseEvent) => handleSwitchRawChunk(chunk.chunk_id, '禁用')"
                           cancel-button-text="取消" confirm-button-text="禁用"
            >
              <template #reference>
                <el-button text type="warning">禁用</el-button>
              </template>
            </el-popconfirm>
            <el-popconfirm v-if = "chunk.status == '禁用'"
                           title="确认启用此分段？" confirm-button-type="primary"
                           @confirm="(e: MouseEvent) => handleSwitchRawChunk(chunk.chunk_id, '正常')"
                           cancel-button-text="取消" confirm-button-text="禁用"
            >
              <template #reference>
                <el-button text type="primary">启用</el-button>
              </template>
            </el-popconfirm>
          </div>
        </div>
        <el-tabs tab-position="left" v-model="chunk.chunk_pane" class="chunk-tabs">
          <el-tab-pane label="分段内容" name="chunk_raw_content">
            <div class="chunk-content" v-html="renderMarkdown(chunk.chunk_raw_content)"/>
          </el-tab-pane>
          <el-tab-pane label="嵌入内容" name="chunk_embedding_content">
            <div class="chunk-content" v-html="renderMarkdown(chunk.chunk_embedding_content)"/>
          </el-tab-pane>
          <el-tab-pane label="嵌入向量" name="chunk_embedding">
            <div class="chunk-content">
              <el-text>{{ chunk.chunk_embedding }}</el-text>
            </div>
          </el-tab-pane>
          <el-tab-pane label="问答测试" name="chunk_embedding_test" @click="initChart(chunk)">
            <div class="test-area">
              <div :id="chunk.chunk_id" style="width: 600px; height: 400px;"></div>
              <el-form :model="chunk" label-width="100px" class="chunk-test-form"
                       ref="chunkTestFormRef"
                       v-if="chunk.chunk_pane === 'chunk_embedding_test'"
                       :rules="{
                            test_question: [{ required: true, message: '测试问题不能为空', trigger: 'blur' }]
                          }">
                <el-form-item label-position="top" label="测试文本" prop="test_question">
                  <el-input type="textarea" v-model="chunk.test_question"
                            placeholder="请输入测试问题，系统会返回分段内容的召回评分"
                            :rows="5" show-word-limit :maxlength="1000" :minlength="1"
                            resize="none"
                  />
                </el-form-item>
              </el-form>
              <div>
                <el-button @click="handleTestChunk(chunk)" type="primary">测试</el-button>
              </div>
            </div>
          </el-tab-pane>
        </el-tabs>
        <div v-if="chunk.status === '禁用'" class="chunk-disabled-mask">
          <div class="chunk-disabled-text">已禁用</div>
        </div>
      </div>
      <div v-if="!currentViewResource?.chunks?.length">
        <el-empty description="暂无分段"></el-empty>
      </div>
    </div>
  </el-scrollbar>
  <el-dialog title="编辑原始分段内容" v-model="showEditRawContentDialog" :fullscreen="true">
    <el-form
        :model="currentChunkIndex" label-width="100px" class="chunk-edit-form"  :rules="{
        chunk_raw_content: [{  required: true, message: '分段内容不能为空', trigger: 'blur' }]}">
      <el-form-item label="分段内容" prop="chunk_raw_content" required label-position="top" ref="rawContentFormRef">
        <el-input type="textarea" v-model="currentChunkIndex.chunk_raw_content" :rows="20"
                  placeholder="建议输入 Markdown 格式的内容，支持代码块、公式、表格等"
        />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="showEditRawContentDialog = false">取消</el-button>
      <el-popconfirm title="确认更新分段内容？此操作将会影响召回的文本" confirm-button-type="primary"
                     @confirm="confirmUpdateChunk" cancel-button-text="取消" confirm-button-text="更新"
                     width="180"
      >
        <template #reference>
          <el-button type="primary">更新</el-button>
        </template>
      </el-popconfirm>

    </template>
  </el-dialog>
  <el-dialog title="编辑嵌入分段内容" v-model="showEditEmbeddingContentDialog" :fullscreen="true">
    <el-form
        :model="currentChunkIndex" label-width="100px" class="chunk-edit-form"  :rules="{
        chunk_embedding_content: [{  required: true, message: '嵌入分段内容不能为空', trigger: 'blur' }]}">
      <el-form-item label="分段内容" prop="chunk_embedding_content" required label-position="top"
                    ref="rawEmbeddingContentFormRef">
        <el-input type="textarea" v-model="currentChunkIndex.chunk_embedding_content" :rows="20"
                  placeholder="建议输入 Markdown 格式的内容，支持代码块、公式、表格等，嵌入分段开头可添加文件来源等信息"
        />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="showEditEmbeddingContentDialog = false">取消</el-button>
      <el-popconfirm title="确认更新嵌入分段内容？系统会自动更新嵌入向量" confirm-button-type="primary"
                     @confirm="confirmUpdateEChunk" cancel-button-text="取消" confirm-button-text="更新"
                     width="180"
      >
        <template #reference>
          <el-button type="primary">更新</el-button>
        </template>
      </el-popconfirm>

    </template>
  </el-dialog>
  <el-dialog title="编辑嵌入向量" v-model="showEditEmbeddingDialog" :fullscreen="true">
    <el-form
        :model="currentChunkIndex" label-width="100px" class="chunk-edit-form"  :rules="{
        chunk_embedding: [
            {  required: true, message: '嵌入向量不能为空', trigger: 'blur' },
            { validator: ValidNewEmbedding, trigger: 'blur' }
            ]}">
      <el-form-item label="嵌入向量" prop="chunk_embedding" required label-position="top" ref="rawEmbeddingFormRef">
        <el-input type="textarea" v-model="currentChunkIndex.chunk_embedding" :rows="20"
                  placeholder="不建议手动修改向量，请使用重新构建自动更新向量"
        />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="showEditEmbeddingDialog = false">取消</el-button>
      <el-popconfirm title="确认手动更新向量？建议使用自动更新向量" confirm-button-type="danger"
                     @confirm="confirmUpdateEmbedding" cancel-button-text="取消" confirm-button-text="手动更新"
                     width="180"
      >
        <template #reference>
          <el-button type="danger">更新</el-button>
        </template>
      </el-popconfirm>

    </template>
  </el-dialog>
</template>

<style scoped>
.std-middle-box {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  height: 100%;
  width: 100%;
}
.view-area {
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: flex-start;
}
.chunk-main {
  display: flex;
  flex-direction: column;
  padding: 6px;
  gap: 10px;
}
/* chunk 盒子样式 */
.chunk-box {
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
  transition: all 0.3s ease;
  padding: 6px;
  position: relative;
}

.chunk-box:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.4);
}
/* chunk 禁用遮罩层样式 */
.chunk-disabled-mask {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: calc(100% - 40px);
  background-color: rgba(0, 0, 0, 0.5); /* 半透明黑色遮罩 */
  border-radius: 8px;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1; /* 确保遮罩层显示在内容之上 */
}

.chunk-disabled-text {
  color: white;
  font-size: 24px;
  font-weight: bold;
}

.chunk-info {
  display: flex;
  justify-content: space-between;
  gap: 6px;
  margin-bottom: 10px;
  color: #888;
  font-size: 14px;
}
.chunk-info-text {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  gap: 4px;
}
.chunk-manage-buttons {
  display: flex;
}
.test-area {
  display: flex;
  flex-direction: column;
  width: 100%;
  justify-content: flex-start;
  align-items: center;
  gap: 12px;
}
.chunk-test-form {
  width: 100%;
}
.percentage-value {
  display: block;
  margin-top: 10px;
  font-size: 28px;
}
.percentage-label {
  display: block;
  margin-top: 10px;
  font-size: 12px;
}
</style>
