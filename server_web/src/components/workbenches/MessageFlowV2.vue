<script setup lang="ts">
import 'highlight.js/styles/stackoverflow-light.min.css';
import { Picture as IconPicture } from '@element-plus/icons-vue';
import { ArrowUp, ArrowDown } from '@element-plus/icons-vue';
import markdownItKatex from '@vscode/markdown-it-katex';
import Clipboard from 'clipboard';
import { ElMessage } from 'element-plus';
import hljs from 'highlight.js';
import MarkdownIt from 'markdown-it';
import markdownItMermaid from 'markdown-it-mermaid-plugin';
import MarkdownTasks from 'markdown-it-task-lists';
import mermaid from 'mermaid';
import { nextTick, reactive, ref, watch } from 'vue';
import {
  attachment_get_detail as attachmentGetDetail,
  search_messages as searchMessages,
  search_qa as searchQa,
  search_reference as searchReference,
  search_session as searchSession,
  update_messages as updateMessages
} from '@/api/next-console';
import { download_resource_object as downloadResourceObject } from '@/api/resource-api';
import WorkFlowArea from './WorkFlowArea.vue';
import router from '@/router';
import {
  msg_item as IMsgItem,
  msg_queue_item as IMsgQueueItem,
  qa_item as IQaItem,
  recommend_question_item as IRecommendQuestionItem,
  recommend_question_map as IRecommendQuestionMap,
  IReferenceItem,
  reference_map as IReferenceMap,
  session_item as ISessionItem,
  SessionAttachment,
  workflow_task_item as IWorkflowTaskItem,
  workflow_task_map as IWorkflowTaskMap
} from '@/types/next-console';
import { ResourceItem } from '@/types/resource-type';
import SimpleProgress from './SimpleProgress.vue';
import '@/styles/katex.min.css';
import { useUserInfoStore } from '@/stores/userInfoStore';
import WelComeArea from './WelComeArea.vue';
const props = defineProps({
  sessionCode: {
    type: String,
    default: '',
    required: false
  },
  streaming: {
    type: Boolean,
    default: true,
    required: false
  },
  debug: {
    type: Boolean,
    default: false,
    required: false
  },
  welcomeConfig: {
    type: Object,
    default: () => ({}),
    required: false
  }
});
const currentSessionCode = ref(null);
const showScrollbarButton = ref(window.innerWidth >= 768);
const loadingMessages = ref(false);
const scrollToFlag = ref(false);
const isScrolling = ref(false);
const msgFlowBoxRef = ref<HTMLDivElement>();
const scrollButtonTimeout = ref(null);
const msgFlowScrollbarRef = ref();
const tooltipStyle = ref({});
const showSupDetail = ref(false);
const currentSupDetail = ref<IReferenceItem>();
const msgFlow = ref<IMsgQueueItem[]>([]);
const msgFlowReference = ref<IReferenceMap>({});
const currentSession = reactive<ISessionItem>({});
const qaList = ref<IQaItem[]>([]);
let mdAnswer = new MarkdownIt({
  html: true,
  linkify: true,
  typographer: true,
  breaks: true,
  highlight: function (str, lang) {
    let language = lang ? lang : 'plaintext';
    let languageText = '<span style="">' + language + '</span>';
    let copyButton =
      '<img src="/images/copy.svg" alt="复制" class="answer-code-copy" style="width: 20px;height: 20px;cursor: pointer"/>';
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
          '<code class="hljs-code hljs-line-numbers" >' +
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
      '<code class="hljs-code hljs-line-numbers" >' +
      '<br>' +
      hljs.highlight(str, { language: 'plaintext', ignoreIllegals: true }).value +
      '<br>' +
      '</code></pre>'
    );
  }
});

mdAnswer.use(markdownItKatex, {
  throwOnError: false,
  errorColor: '#cc0000',
  strict: false
});
mdAnswer.use(markdownItMermaid);
mdAnswer.renderer.rules.image = function (tokens, idx, options, env) {
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
const showReferenceDrawer = ref(false);
const referenceDrawerData = ref<IReferenceItem[]>([]);
const msgRecommendQuestion = ref<IRecommendQuestionMap>({});
const qaWorkflowMap = ref<IWorkflowTaskMap>({});
const userStopScroll = ref(false);
const scrollTimer = ref();
const questionRunningCnt = ref(0);
const userInfoStore = useUserInfoStore();
const referenceDrawerWidth = ref(window.innerWidth < 768 ? '60%' : '35%');
const chooseModel = ref(false);
const chooseMsgCnt = ref(0);
const chooseMsgAll = ref(false);
const chooseMsgMiddle = ref(false);
const firstQuestion = ref();
const currentDebugInfo = ref([]);
const showDebugInfoFlag = ref(false);
const currentDebugInfoViewModel = ref('table');
const localWelComeConfig = ref({});
function showReferenceDrawerFn(data: IReferenceItem[] | null) {
  referenceDrawerData.value = data;
  showReferenceDrawer.value = true;
}
function scrollToTargetQa(step: number) {
  // 正在滚动中
  if (isScrolling.value) {
    return;
  }
  if (!msgFlowBoxRef.value) {
    return;
  }
  clearTimeout(scrollButtonTimeout.value);
  scrollButtonTimeout.value = setTimeout(() => {
    // 为了保证精度，全部转为int
    isScrolling.value = true;
    // 获取当前页面上方隐藏高度
    let currentHeight = Math.ceil(msgFlowScrollbarRef.value.wrapRef.scrollTop);
    // 获取视窗高度
    let targetHeight = 0;
    if (step > 0) {
      // 向下滚动到下step个问题,
      for (let i = 0; i < msgFlowBoxRef.value.children.length; i++) {
        targetHeight += Math.floor(msgFlowBoxRef.value.children[i].clientHeight);
        if (targetHeight > currentHeight) {
          break;
        }
      }
    } else {
      // 向上滚动到上step个问题
      let index = 0;
      for (let i = 0; i < msgFlowBoxRef.value.children.length; i++) {
        targetHeight += Math.floor(msgFlowBoxRef.value.children[i].clientHeight);
        if (targetHeight > currentHeight) {
          index = i;
          break;
        }
      }
      // index 为下一个问题，targetHeight 为下一个问题的上沿
      // 减去两个问题即可
      targetHeight -= msgFlowBoxRef.value.children[index]?.clientHeight;
      if (targetHeight >= currentHeight) {
        targetHeight -= msgFlowBoxRef.value.children[index - 1]?.clientHeight;
      }
    }
    msgFlowScrollbarRef.value.scrollTo({ top: targetHeight, behavior: 'smooth' });
    if (!targetHeight) {
      ElMessage({
        message: '已经到顶啦！',
        type: 'success',
        duration: 2000
      });
    }

    setTimeout(() => {
      isScrolling.value = false;
    }, 500);
  }, 200);
}
function scrollToBottom() {
  // 正在滚动中
  if (isScrolling.value) {
    return;
  }
  if (userStopScroll.value) {
    return;
  }
  if (!msgFlowScrollbarRef.value) {
    return;
  }
  const scrollMax = msgFlowBoxRef.value.clientHeight;
  clearTimeout(scrollButtonTimeout.value);
  isScrolling.value = true;
  msgFlowScrollbarRef.value.scrollTo({ top: scrollMax, behavior: 'smooth' });
  scrollButtonTimeout.value = setTimeout(() => {
    isScrolling.value = false;
  }, 500);
}
function scrollToTop() {
  // 正在滚动中
  if (isScrolling.value) {
    return;
  }
  clearTimeout(scrollButtonTimeout.value);
  if (!Math.ceil(msgFlowScrollbarRef.value.wrapRef.scrollTop)) {
    ElMessage({
      message: '已经到顶啦！',
      type: 'success',
      duration: 2000
    });
    return;
  }
  isScrolling.value = true;
  msgFlowScrollbarRef.value.scrollTo({ top: 0, behavior: 'smooth' });
  scrollButtonTimeout.value = setTimeout(() => {
    isScrolling.value = false;
  }, 500);
}
async function showSupDetailFn(item: IMsgQueueItem, event) {
  // 检查事件目标是sup或sup内部的a标签
  const target = event.target;
  const isSup = target.tagName.toLowerCase() === 'sup';
  const isSupLink = target.tagName.toLowerCase() === 'a' && target.parentElement?.tagName.toLowerCase() === 'sup';
  if (isSup || isSupLink) {
    showSupDetail.value = true;
    const mouseX = event.clientX;
    const mouseY = event.clientY;
    tooltipStyle.value = {
      position: 'fixed',
      top: `${window.scrollY + mouseY}px`, // 鼠标的Y轴位置
      left: `${window.scrollX + mouseX}px` // 鼠标的X轴位置
    };
    const questionId = item.qa_value.question[0].msg_id;
    let referenceList = msgFlowReference.value?.[questionId]; // 获取 <sup> 的内容
    if (referenceList?.length) {
      currentSupDetail.value = null;
      // 获取目标链接值
      const targetLink = isSupLink ? target.getAttribute('href') : target.querySelector('a')?.getAttribute('href');
      const targetIndex = event.target.textContent;
      let targetIndexNumber = -1;
      // 使用正则表达式匹配 [数字] 格式
      const match = targetIndex.match(/\[(\d+)\]/);
      if (match) {
        // 如果匹配成功，提取第一个捕获组并转为整数
        targetIndexNumber = parseInt(match[1], 10);
      } else {
        // 如果不是 [数字] 格式，尝试直接转为整数
        try {
          targetIndexNumber = parseInt(targetIndex, 10);
        } catch (e) {}
      }
      for (let i = 0; i <= referenceList.length; i++) {
        if (
          (referenceList[i]?.resource_source_url == targetLink && targetLink) ||
          (referenceList[i]?.resource_download_url == targetLink && targetLink) ||
          targetLink?.includes('next_console/resources/resource_viewer/' + referenceList[i]?.resource_id) ||
          i === targetIndexNumber
        ) {
          currentSupDetail.value = referenceList[i];
          break;
        }
      }
    }
  } else {
    showSupDetail.value = false;
  }
}
function checkSelectMsgMiddleStatus() {
  // 更新 选中条数与全选状态
  let selectCnt = 0;
  let allCnt = 0;
  for (let i = 0; i < msgFlow.value.length; i++) {
    let questionId = msgFlow.value[i].qa_value.question[0].msg_id;
    allCnt += 1;
    if (msgFlow.value[i].qa_value.question[0].msg_is_selected) {
      selectCnt += 1;
    }
    if (msgFlow.value[i].qa_value.answer[questionId]) {
      for (let j = 0; j < msgFlow.value[i].qa_value.answer[questionId].length; j++) {
        allCnt += 1;
        if (msgFlow.value[i].qa_value.answer[questionId][j].msg_is_selected) {
          selectCnt += 1;
        }
      }
    }
  }
  chooseMsgCnt.value = selectCnt;
  chooseMsgAll.value = selectCnt === allCnt;
  chooseMsgMiddle.value = selectCnt > 0 && selectCnt < allCnt;
  emit('select-msg', {
    chooseMsgCnt: chooseMsgCnt.value,
    chooseMsgAll: chooseMsgAll.value,
    chooseMsgMiddle: chooseMsgMiddle.value
  });
}
function addQuote(attachments: SessionAttachment[]) {
  const ids = attachments.map(item => item.id);
  emit('add-quote', ids);
}
function copyQuestion(item: IMsgQueueItem) {
  let content = item?.qa_value?.question?.[0]?.msg_content;
  if (!content) {
    return;
  }
  Clipboard.copy(content.trim());
  ElMessage({
    message: '复制成功',
    type: 'success',
    duration: 2000
  });
}
function copyAnswer(item: IMsgQueueItem) {
  let msgParentId = item?.qa_value?.question?.[0]?.msg_id;
  if (!msgParentId) {
    // @ts-ignore
    return;
  }
  let finalData = '';
  for (let subMsg of item?.qa_value?.answer?.[msgParentId]) {
    if (!subMsg?.msg_content) {
      continue;
    }
    console.log(subMsg);
    if (subMsg?.msg_format == 'workflow') {
      continue;
    }
    finalData += subMsg?.msg_content;
  }

  // 去除 <sup> 标签及其内容
  // const cleanedData = content.replace(/<sup>.*?<\/sup>/g, '');
  //
  // const finalData = cleanedData.replace(/\[.*?]:\s*\S+/g, '');
  Clipboard.copy(finalData.trim());
  ElMessage({
    message: '复制成功',
    type: 'success',
    duration: 2000
  });
}
async function getTargetSession() {
  // 获取指定session
  if (currentSessionCode.value) {
    const params = {
      session_codes: [currentSessionCode.value]
    };
    const data = await searchSession(params);
    Object.assign(currentSession, data.result[0]);
  }
}
async function getLastedQa() {
  // 获取最新qa
  if (!currentSession.id) {
    qaList.value = [];
    return false;
  }
  const params = {
    session_id: [currentSession.id]
  };
  let data = await searchQa(params);
  qaList.value = data.result;
}
async function getLastedMessages() {
  if (qaList.value.length === 0) {
    msgFlow.value = [];
    return false;
  }
  const params = {
    qa_id: []
  };
  for (let i = 0; i < qaList.value.length; i++) {
    params.qa_id.push(qaList.value[i].qa_id);
  }
  let data = await searchMessages(params);
  msgFlow.value = data.result;
  for (let i = 0; i < msgFlow.value.length; i++) {
    let item = msgFlow.value[i];
    splitMarkdown(item);
    splitReasonMarkdown(item);
    item.qa_finished = true;
  }
  getLastedReference();
}
function splitReasonMarkdown(item: IMsgQueueItem) {
  // 找到最小粒度的tokens，分别转换为html，然后与存量html比对，不同则替换
  let msgParentId = item.qa_value.question?.[0]?.msg_id;
  if (!msgParentId) {
    return;
  }
  for (let i = 0; i < item.qa_value.answer[msgParentId].length; i++) {
    let msgContent = item.qa_value.answer[msgParentId]?.[i]?.reasoning_content;
    if (!msgContent) {
      continue;
    }
    let tokens = mdAnswer.parse(msgContent, {});
    let finishQueue = [];
    let queue = [];
    // 遍历tokens 将完成的token匹配好存入finishQueue
    tokens.forEach(token => {
      queue.push(token);
      if (token.type.includes('_close')) {
        let openTokenName = token.type.replace('_close', '_open');
        if (queue[0].type === openTokenName) {
          let finishFlag = true;
          queue.forEach((token, index) => {
            if (index > 0 && token.type == openTokenName) {
              finishFlag = false;
            }
          });
          if (finishFlag) {
            finishQueue.push(queue);
            queue = [];
          }
        }
      } else if (!token.type.includes('_open')) {
        if (queue.length == 1) {
          finishQueue.push(queue);
          queue = [];
        }
      }
    });
    if (!item.qa_value.answer[msgParentId][i].msg_reason_content_finish_html) {
      item.qa_value.answer[msgParentId][i].msg_reason_content_finish_html = [];
    }
    finishQueue.forEach((subQueue, index) => {
      let html = mdAnswer.renderer.render(subQueue, mdAnswer.options, {});
      // 两者比对，不同则替换
      if (item.qa_value.answer[msgParentId][i].msg_reason_content_finish_html[index] !== html) {
        item.qa_value.answer[msgParentId][i].msg_reason_content_finish_html[index] = html;
      }
    });
    // 如果完成的html比存量html多，截取，可能原因是搜索时，搜索到的内容比原有的内容多
    if (finishQueue.length < item.qa_value.answer[msgParentId][i].msg_reason_content_finish_html.length) {
      item.qa_value.answer[msgParentId][i].msg_reason_content_finish_html = item.qa_value.answer[msgParentId][
        i
      ].msg_reason_content_finish_html.slice(0, finishQueue.length);
    }
    //如果还剩下没有匹配上的，直接推入
    if (queue.length) {
      let html = mdAnswer.renderer.render(queue, mdAnswer.options, {});
      item.qa_value.answer[msgParentId][i].msg_reason_content_finish_html.push(html);
    }
  }
  renderMermaid();
}
function splitMarkdown(item: IMsgQueueItem) {
  // 找到最小粒度的tokens，分别转换为html，然后与存量html比对，不同则替换
  let msgParentId = item.qa_value.question?.[0]?.msg_id;
  if (!msgParentId) {
    return;
  }
  for (let i = 0; i < item.qa_value.answer[msgParentId].length; i++) {
    let msgContent = item.qa_value.answer[msgParentId]?.[i]?.msg_content;
    if (!msgContent) {
      continue;
    }
    if (item.qa_value.answer[msgParentId]?.[i]?.msg_format == 'workflow') {
      msgContent = JSON.parse(msgContent);
      updateWorkflowItemStatus({
        qa_id: item?.qa_id,
        task_id: item.qa_value.answer[msgParentId]?.[i]?.msg_id,
        task_type: msgContent.title,
        task_result: msgContent.description,
        task_status: 'finished'
      });
      continue;
    } else if (item.qa_value.answer[msgParentId]?.[i]?.msg_format == 'recommendQ') {
      msgContent = JSON.parse(msgContent);
      console.log('recommendQ', msgContent);
      const recommendQuestionList = [];
      try {
        for (let q of msgContent?.questions) {
          recommendQuestionList.push({
            msg_id: msgParentId,
            recommend_question: q
          });
        }
      } catch (e) {
        console.log(e);
      }
      updateRecommendQuestion(recommendQuestionList);
      continue;
    } else if (item.qa_value.answer[msgParentId]?.[i]?.msg_format == 'customize') {
      // 用json代码块包裹
      try {
        msgContent = JSON.parse(msgContent);
      } catch (e) {
        console.error('JSON parse error:', e);
      }
      delete msgContent['msg_format'];
      msgContent = JSON.stringify(msgContent, null, 2);
      msgContent = '```json\n' + msgContent + '\n```';
    }
    let tokens = mdAnswer.parse(msgContent, {});
    let finishQueue = [];
    let queue = [];
    // 遍历tokens 将完成的token匹配好存入finishQueue
    tokens.forEach(token => {
      queue.push(token);
      if (token.type.includes('_close')) {
        let openTokenName = token.type.replace('_close', '_open');
        if (queue[0].type === openTokenName) {
          let finishFlag = true;
          queue.forEach((token, index) => {
            if (index > 0 && token.type == openTokenName) {
              finishFlag = false;
            }
          });
          if (finishFlag) {
            finishQueue.push(queue);
            queue = [];
          }
        }
      } else if (!token.type.includes('_open')) {
        if (queue.length == 1) {
          finishQueue.push(queue);
          queue = [];
        }
      }
    });
    if (!item.qa_value.answer[msgParentId][i].msg_content_finish_html) {
      item.qa_value.answer[msgParentId][i].msg_content_finish_html = [];
    }
    finishQueue.forEach((subQueue, index) => {
      let html = mdAnswer.renderer.render(subQueue, mdAnswer.options, {});
      // 两者比对，不同则替换
      if (item.qa_value.answer[msgParentId][i].msg_content_finish_html[index] !== html) {
        item.qa_value.answer[msgParentId][i].msg_content_finish_html[index] = html;
      }
    });
    // 如果完成的html比存量html多，截取，可能原因是搜索时，搜索到的内容比原有的内容多
    if (finishQueue.length < item.qa_value.answer[msgParentId][i].msg_content_finish_html.length) {
      item.qa_value.answer[msgParentId][i].msg_content_finish_html = item.qa_value.answer[msgParentId][
        i
      ].msg_content_finish_html.slice(0, finishQueue.length);
    }
    //如果还剩下没有匹配上的，直接推入
    if (queue.length) {
      let html = mdAnswer.renderer.render(queue, mdAnswer.options, {});
      item.qa_value.answer[msgParentId][i].msg_content_finish_html.push(html);
    }
  }
  renderMermaid();
}
async function renderMermaid() {
  await nextTick();
  const nodes = document.querySelectorAll('.mermaid');
  // 提前验证至挑选合法的语法进行渲染
  const nodesValid = [];
  for (let node of nodes) {
    let mermaidText = node.textContent;
    if (mermaidText) {
      // gantt 最后渲染
      try {
        await mermaid.parse(mermaidText);
        nodesValid.push(node);
      } catch (e) {}
    }
  }
  await mermaid.run({
    // @ts-ignore
    nodes: Array.from(nodesValid),
    suppressErrors: true
  });
}
async function getLastedReference() {
  let params = {
    msg_id_list: []
  };
  for (let i = 0; i < msgFlow.value.length; i++) {
    for (let j = 0; j < msgFlow.value[i].qa_value.question.length; j++) {
      params.msg_id_list.push(msgFlow.value[i].qa_value.question[j].msg_id);
    }
  }
  let res = await searchReference(params);
  if (!res.error_status) {
    msgFlowReference.value = res.result;
  }
}
async function retryGetIcon(data: IReferenceItem) {
  if (!data.resource_icon) {
    return;
  }
  try {
    const response = await fetch(data.resource_icon, {
      method: 'GET',
      headers: {
        'User-Agent': 'Mozilla/5.0', // 模拟常见浏览器的User-Agent
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1'
      }
    });
    const blob = await response.blob();
    const reader = new FileReader();

    reader.onloadend = () => {
      // 使用类型断言，告诉 TypeScript 这个元素是 HTMLImageElement 类型
      const imgElement = document.getElementById(data.resource_icon) as HTMLImageElement;
      // 将图片数据作为Base64字符串设置为img的src
      if (imgElement) {
        imgElement.src = reader.result as string;
      }
    };

    reader.readAsDataURL(blob);
  } catch (e) {}
}
function openReference(data: IReferenceItem | null) {
  if (data.source_type == 'webpage') {
    // 新标签页打开
    window.open(data.resource_source_url as string);
  } else {
    // 跳转资源预览页面
    const route = router.resolve({
      name: 'resource_viewer',
      params: {
        resource_id: data.resource_id
      }
    });
    window.open(route.href, '_blank');
  }
}
async function addCopyButtonEvent() {
  let copyButtonList = document.getElementsByClassName('answer-code-copy');
  for (let i = 0; i < copyButtonList.length; i++) {
    let button = copyButtonList[i] as HTMLElement;
    if (button.dataset.clickListener === 'true') {
      continue;
    }
    copyButtonList[i].addEventListener('click', function () {
      let code = (this.parentNode.nextElementSibling && this.parentNode.nextElementSibling.innerText) || '';
      Clipboard.copy(code.trim());
      ElMessage({
        message: '复制成功',
        type: 'success',
        duration: 2000
      });
    });
    button.dataset.clickListener = 'true';
  }
  // @ts-ignore
  hljs.highlightAll();
  // 2. 将 hljs 绑定到 window 对象
  window.hljs = hljs;
  await import('highlightjs-line-numbers.js');
  await import('highlightjs-line-numbers.js/dist/highlightjs-line-numbers.min.js');
  document.querySelectorAll('code.hljs-line-numbers').forEach(block => {
    hljs?.lineNumbersBlock(block);
  });
}
function addReferenceHoverEvent() {
  try {
    // 获取页面上所有的 <sup> 标签
    let supTags = document.querySelectorAll('sup');

    // 遍历每个 <sup> 标签
    supTags.forEach(function (supTag) {
      // 获取 <sup> 标签下的所有 <a> 标签
      let aTags = supTag.querySelectorAll('a');

      // 遍历每个 <a> 标签
      aTags.forEach(function (aTag) {
        // 为 <a> 标签添加 target="_blank" 属性
        aTag.setAttribute('target', '_blank');
      });
    });
  } catch (error) {
    console.error('An error occurred:', error);
  }
}
async function addLike(item: IMsgQueueItem) {
  let questionId = item.qa_value.question[0]?.msg_id;
  if (!questionId) {
    return;
  }
  let answerId = item.qa_value.answer[questionId][0]?.msg_id;
  if (!answerId) {
    ElMessage.info({
      message: '请过会儿点击，感谢您的支持！',
      duration: 1000
    });

    return false;
  }
  if (item.qa_value.answer[questionId][0].msg_remark == 1) {
    await updateMessages({
      msg_id: answerId,
      msg_remark: 0
    });
    item.qa_value.answer[questionId][0].msg_remark = 0;
    ElMessage.success({
      message: '取消点赞！'
    });
    return;
  }
  await updateMessages({
    msg_id: answerId,
    msg_remark: 1
  });
  item.qa_value.answer[questionId][0].msg_remark = 1;
  ElMessage.success({
    message: '点赞成功！'
  });
}
async function addDislike(item: IMsgQueueItem) {
  let questionId = item.qa_value.question[0]?.msg_id;
  if (!questionId) {
    return;
  }
  let answerId = item.qa_value.answer[questionId][0]?.msg_id;
  if (!answerId) {
    ElMessage.info({
      message: '请过会儿点击，感谢您的支持！',
      duration: 1000
    });

    return false;
  }
  if (item.qa_value.answer[questionId][0].msg_remark == -1) {
    await updateMessages({
      msg_id: answerId,
      msg_remark: 0
    });
    item.qa_value.answer[questionId][0].msg_remark = 0;
    ElMessage.success({
      message: '取消点踩成功！'
    });
    return;
  }
  await updateMessages({
    msg_id: item.qa_value.answer[questionId][0].msg_id,
    msg_remark: -1
  });
  item.qa_value.answer[questionId][0].msg_remark = -1;
  ElMessage.success({
    message: '感谢您的反馈！我们会尽快改进！'
  });
}
function switchAnswerLength(item: IMsgQueueItem) {
  item.short_answer = !item.short_answer;
}
function getAnswerCreateTime(item: IMsgQueueItem) {
  try {
    const msgParentId = item?.qa_value?.question?.[0].msg_id;
    return item?.qa_value?.answer?.[msgParentId]?.[0].create_time;
  } catch (e) {
    return '';
  }
}
function clickRecommendQuestion(recommendQuestion: IRecommendQuestionItem) {
  // 点击推荐问题,直接提问并更新点击
  emit('click-recommend-question', { question: recommendQuestion?.recommend_question });
}
function handleDragOver(event) {
  event.preventDefault();
}
function handleScroll() {
  if (scrollTimer.value) {
    clearTimeout(scrollTimer.value);
  }
  scrollToFlag.value = true;
  scrollTimer.value = setTimeout(() => {
    scrollToFlag.value = false;
  }, 6000);
}
function handleWheel() {
  if (isScrolling.value && !userStopScroll.value) {
    userStopScroll.value = true;
  }
}
async function refreshMsgFlow() {
  try {
    loadingMessages.value = true;
    await getTargetSession();
    await getLastedQa();
    await getLastedMessages();
    emit('ready', { isEmpty: !msgFlow.value?.length });
    loadingMessages.value = false;
    addCopyButtonEvent();
    addReferenceHoverEvent();
    scrollToBottom();
  } catch (e) {
    console.error(e);
  }
}
function getSelectMsg() {
  let markdownString = '';
  for (let i = 0; i < msgFlow.value.length; i++) {
    let questionId = msgFlow.value[i].qa_value.question[0].msg_id;
    if (msgFlow.value[i].qa_value.question[0].msg_is_selected) {
      markdownString += '> ' + msgFlow.value[i].qa_value.question[0].msg_content;
    }
    if (msgFlow.value[i].qa_value.answer[questionId]) {
      for (let j = 0; j < msgFlow.value[i].qa_value.answer[questionId].length; j++) {
        if (msgFlow.value[i].qa_value.answer[questionId][j].msg_is_selected) {
          markdownString += '> ' + msgFlow.value[i].qa_value.answer[questionId][j].msg_content;
        }
      }
    }
  }
  return markdownString;
}
function unSelectMessages() {
  // 退出模式，将消息流的所有消息都设置为未选中
  for (let i = 0; i < msgFlow.value.length; i++) {
    let questionId = msgFlow.value[i].qa_value.question[0].msg_id;
    msgFlow.value[i].qa_value.question[0].msg_is_selected = false;
    if (msgFlow.value[i].qa_value.answer[questionId]) {
      for (let j = 0; j < msgFlow.value[i].qa_value.answer[questionId].length; j++) {
        msgFlow.value[i].qa_value.answer[questionId][j].msg_is_selected = false;
      }
    }
  }
}
function selectAllMessages() {
  // 退出模式，将消息流的所有消息都设置为未选中
  for (let i = 0; i < msgFlow.value.length; i++) {
    let questionId = msgFlow.value[i].qa_value.question[0].msg_id;
    msgFlow.value[i].qa_value.question[0].msg_is_selected = true;
    if (msgFlow.value[i].qa_value.answer[questionId]) {
      for (let j = 0; j < msgFlow.value[i].qa_value.answer[questionId].length; j++) {
        msgFlow.value[i].qa_value.answer[questionId][j].msg_is_selected = true;
      }
    }
  }
  return msgFlow.value.length;
}
function formatDateTime(date = new Date()) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  const hours = String(date.getHours()).padStart(2, '0');
  const minutes = String(date.getMinutes()).padStart(2, '0');
  const seconds = String(date.getSeconds()).padStart(2, '0');
  return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
}
function waitForLoading() {
  return new Promise(resolve => {
    const check = () => {
      if (!loadingMessages.value) {
        resolve(void 0);
      } else {
        setTimeout(check, 100);
      }
    };
    check();
  });
}
async function beginAnswer(data) {
  if (loadingMessages.value) {
    // 使用方式
    await waitForLoading();
  }
  // 生成问答对占位
  let newQaItem = <IMsgQueueItem>{
    user_qa_id: data.userQaID,
    qa_id: null,
    qa_status: null,
    qa_topic: data.data,
    qa_value: {
      question: [
        <IMsgItem>{
          msg_content: data.data,
          msg_role: 'user',
          msg_parent_id: null,
          create_time: formatDateTime(),
          msg_remark: 0,
          msg_version: 0,
          msg_id: 0,
          msg_del: 0,
          assistant_id: -12345,
          shop_assistant_id: null,
          attachment_list: []
        }
      ],
      answer: {}
    },
    qa_share_picked: 0,
    qa_progress_open: false,
    qa_workflow_open: true,
    show_button_question_area: false,
    show_button_answer_area: false,
    short_answer: null,
    qa_finished: false
  };
  msgFlow.value.push(newQaItem);
  emit('ready', { isEmpty: !msgFlow.value?.length });
  firstQuestion.value = newQaItem;
  questionRunningCnt.value++;
  if (data?.attachments) {
    if (!currentSession.id) {
      return;
    }
    const params = {
      session_id: currentSession.id,
      attachment_source: 'all'
    };
    const res = await attachmentGetDetail(params);
    if (!res.error_status) {
      newQaItem.qa_value.question[0].attachment_list = res.result.filter(subAttachment =>
        data?.attachments.includes(subAttachment.id)
      );
    }
  }
  await nextTick(() => {
    scrollToBottom();
  });
}
async function updateAnswer(data) {
  let userQaID = data.userQaID;
  // 找到对应的问答对
  let lastIndex = msgFlow.value.length - 1;
  for (let i = 0; i < msgFlow.value.length; i++) {
    if (msgFlow.value[i].user_qa_id == userQaID) {
      lastIndex = i;
      break;
    }
  }
  if (props.streaming) {
    let jsonDataStr = new TextDecoder('utf-8').decode(data.data.value);
    const lines = jsonDataStr.split('\n');
    for (let line of lines) {
      if (line.startsWith('data:')) {
        jsonDataStr = line.slice(5).trim(); // 移除"data:"前缀
        let jsonData = {};
        try {
          jsonData = JSON.parse(jsonDataStr);
        } catch (e) {
          return;
        }
        let msgReasonContent = jsonData?.choices[0].delta?.reasoning_content;
        let msgContent = jsonData?.choices[0].delta?.content;
        let newMsgItem = generateNewMsg(jsonData);
        if (!msgFlow.value[lastIndex]?.qa_id) {
          msgFlow.value[lastIndex].qa_id = jsonData?.qa_id;
          msgFlow.value[lastIndex].qa_value.question[0].msg_id = jsonData?.msg_parent_id;
          msgFlow.value[lastIndex].qa_value.answer[jsonData?.msg_parent_id] = [newMsgItem];
        } else {
          let msgIdx = -1;
          for (let i = 0; i < msgFlow.value[lastIndex].qa_value.answer[jsonData?.msg_parent_id]?.length; i++) {
            if (msgFlow.value[lastIndex].qa_value.answer[jsonData?.msg_parent_id][i]?.msg_id == jsonData?.msg_id) {
              // 找到对应的消息
              msgIdx = i;
              if (msgContent !== undefined && msgContent) {
                if (!msgFlow.value[lastIndex].qa_value.answer[jsonData?.msg_parent_id][msgIdx].msg_content) {
                  msgFlow.value[lastIndex].qa_value.answer[jsonData?.msg_parent_id][msgIdx].msg_content = '';
                }
                msgFlow.value[lastIndex].qa_value.answer[jsonData?.msg_parent_id][msgIdx].msg_content += msgContent;
              }
              if (msgReasonContent !== undefined && msgReasonContent) {
                msgFlow.value[lastIndex].qa_value.answer[jsonData?.msg_parent_id][msgIdx].reasoning_content +=
                  msgReasonContent;
              }
              break;
            }
          }
          if (msgIdx == -1) {
            // 没找到则插入到msg_id比自己大的消息前面
            for (let i = 0; i < msgFlow.value[lastIndex].qa_value.answer[jsonData?.msg_parent_id]?.length; i++) {
              if (msgFlow.value[lastIndex].qa_value.answer[jsonData?.msg_parent_id][i]?.msg_id > jsonData?.msg_id) {
                msgIdx = i;
                break;
              }
            }
            if (msgIdx == -1) {
              msgFlow.value[lastIndex].qa_value.answer[jsonData?.msg_parent_id]?.push(newMsgItem);
            } else {
              msgFlow.value[lastIndex].qa_value.answer[jsonData?.msg_parent_id].splice(msgIdx, 0, newMsgItem);
            }
          }
        }
        splitMarkdown(msgFlow.value[lastIndex]);
        splitReasonMarkdown(msgFlow.value[lastIndex]);
        scrollToBottom();
      }
    }
  } else {
    updateAnswerDefault(data, lastIndex);
  }
}
function generateNewMsg(jsonData) {
  let msgReasonContent = jsonData?.choices[0].delta?.reasoning_content;
  let msgContent = jsonData?.choices[0].delta?.content;
  let msgFormat = jsonData?.choices[0].delta?.msg_format;
  let newMsgItem = {};
  if (msgFormat == 'workflow') {
    newMsgItem = <IMsgItem>{
      msg_content: JSON.stringify(jsonData?.choices[0].delta),
      msg_format: 'workflow',
      msg_role: 'assistant',
      msg_parent_id: jsonData?.msg_parent_id,
      create_time: jsonData?.create_time,
      msg_remark: 0,
      msg_version: 0,
      msg_id: jsonData?.msg_id,
      msg_del: 0,
      assistant_id: -12345,
      shop_assistant_id: null
    };
  } else if (msgFormat == 'recommendQ') {
    newMsgItem = <IMsgItem>{
      msg_content: JSON.stringify(jsonData?.choices[0].delta),
      msg_format: 'recommendQ',
      msg_role: 'assistant',
      msg_parent_id: jsonData?.msg_parent_id,
      create_time: jsonData?.create_time,
      msg_remark: 0,
      msg_version: 0,
      msg_id: jsonData?.msg_id,
      msg_del: 0,
      assistant_id: -12345,
      shop_assistant_id: null
    };
  } else if (msgFormat == 'customize') {
    newMsgItem = <IMsgItem>{
      msg_content: JSON.stringify(jsonData?.choices[0].delta),
      msg_format: 'customize',
      msg_role: 'assistant',
      msg_parent_id: jsonData?.msg_parent_id,
      create_time: jsonData?.create_time,
      msg_remark: 0,
      msg_version: 0,
      msg_id: jsonData?.msg_id,
      msg_del: 0,
      assistant_id: -12345,
      shop_assistant_id: null
    };
  } else {
    newMsgItem = <IMsgItem>{
      msg_content: msgContent,
      reasoning_content: msgReasonContent,
      msg_role: 'assistant',
      msg_parent_id: jsonData?.msg_parent_id,
      create_time: jsonData?.create_time,
      msg_remark: 0,
      msg_version: 0,
      msg_id: jsonData?.msg_id,
      msg_del: 0,
      assistant_id: -12345,
      shop_assistant_id: null
    };
  }
  return newMsgItem;
}
function updateAnswerDefault(data, lastIndex) {
  msgFlow.value[lastIndex].qa_id = data.data?.qa_id;
  msgFlow.value[lastIndex].qa_value.question[0].msg_id = data.data?.msg_parent_id;
  msgFlow.value[lastIndex].qa_value.answer[data.data?.msg_parent_id] = [];
  for (let item of data.data?.choices) {
    msgFlow.value[lastIndex].qa_value.answer[data.data?.msg_parent_id].push(<IMsgItem>{
      msg_content: item.content,
      reasoning_content: item.reasoning_content,
      msg_role: 'assistant',
      msg_parent_id: data.data?.msg_parent_id,
      create_time: data.data?.create_time,
      msg_remark: 0,
      msg_version: 0,
      msg_id: item?.msg_id,
      msg_del: 0,
      assistant_id: -12345,
      shop_assistant_id: null
    });
  }
  splitMarkdown(msgFlow.value[lastIndex]);
  splitReasonMarkdown(msgFlow.value[lastIndex]);
  scrollToBottom();
  msgFlow.value[lastIndex].qa_finished = true;
}
async function finishAnswer(data) {
  addCopyButtonEvent();
  addReferenceHoverEvent();
  let msgParentId = 0;
  for (let qaItem of msgFlow.value) {
    if (qaItem.qa_id == data.qaId) {
      qaItem.qa_finished = true;
      qaItem.qa_workflow_open = false;
      msgParentId = qaItem.qa_value.question[0].msg_id;
      break;
    }
  }
  questionRunningCnt.value--;
  userStopScroll.value = false;
  if (msgParentId) {
    getTargetReference(msgParentId);
  }
}
function stopAnswer(data) {
  let userQaID = data.userQaId;
  // 找到对应的问答对
  let lastIndex = msgFlow.value.length - 1;
  let msgParentId = msgFlow.value[lastIndex].qa_value.question[0].msg_id;
  if (userQaID) {
    for (let i = 0; i < msgFlow.value.length; i++) {
      if (msgFlow.value[i].user_qa_id == userQaID) {
        lastIndex = i;
        msgParentId = msgFlow.value[i].qa_value.question[0].msg_id;
        break;
      }
    }
  }
  msgFlow.value[lastIndex].qa_finished = true;
  try {
    msgFlow.value[lastIndex].qa_is_cut_off = true;
  } catch (e) {
    console.error(e);
  }
  getTargetReference(msgParentId);
}
function updateWorkflowItemStatus(data: IWorkflowTaskItem) {
  // 根据传入工作流任务对象更新工作流任务状态
  // 如果不存在则新增，如果存在则更新
  // 剔除占位符
  if (qaWorkflowMap.value[data.qa_id]?.length === 1 && !qaWorkflowMap.value[data.qa_id][0].task_id) {
    qaWorkflowMap.value[data.qa_id] = [];
  }
  if (!qaWorkflowMap.value[data.qa_id]?.length) {
    qaWorkflowMap.value[data.qa_id] = [data];
  } else {
    let findFlag = false;
    for (let i = 0; i < qaWorkflowMap.value[data.qa_id].length; i++) {
      if (qaWorkflowMap.value[data.qa_id][i].task_id === data.task_id) {
        qaWorkflowMap.value[data.qa_id][i] = data;
        findFlag = true;
        break;
      }
    }
    if (!findFlag) {
      qaWorkflowMap.value[data.qa_id].push(data);
    }
  }
  // 打开工作流展示区域
  for (let i = 0; i < msgFlow.value.length; i++) {
    if (msgFlow.value[i].qa_id === data.qa_id) {
      msgFlow.value[i].qa_workflow_open = true;
    }
  }
}
function updateRecommendQuestion(data: IRecommendQuestionItem[]) {
  for (const recommendQuestion of data) {
    if (!msgRecommendQuestion.value?.[recommendQuestion.msg_id]) {
      msgRecommendQuestion.value[recommendQuestion.msg_id] = [recommendQuestion];
    } else {
      let existFlag = false;
      for (let existQ of msgRecommendQuestion.value[recommendQuestion.msg_id]) {
        if (existQ.recommend_question === recommendQuestion.recommend_question) {
          existFlag = true;
          break;
        }
      }
      if (!existFlag) {
        msgRecommendQuestion.value[recommendQuestion.msg_id].push(recommendQuestion);
      }
    }
  }
}
async function getTargetReference(msgId: number) {
  // 为完成的消息获取参考文献
  let params = {
    msg_id_list: [msgId]
  };
  let res = await searchReference(params);
  if (!res.error_status) {
    if (!msgFlowReference.value?.[msgId]) {
      msgFlowReference.value[msgId] = res.result[msgId];
    }
    if (!res.result[msgId]?.length) {
      return;
    }
  }
}
function getResourceIcon(resource: ResourceItem) {
  // 获取资源图标
  if (resource.resource_icon) {
    if (
      resource.resource_icon.includes('http') ||
      resource.resource_icon.includes('data:image') ||
      resource.resource_icon.includes('/images/')
    ) {
      return resource.resource_icon;
    }
    return '/images/' + resource.resource_icon;
  } else {
    return '/images/html.svg';
  }
}
async function downloadAttachment(attachment) {
  if (!attachment?.id) {
    ElMessage.warning('资源不存在!');
    return;
  }
  if (attachment.resource_status == '删除') {
    ElMessage.warning('资源已删除，请恢复后下载!');
    return;
  }
  let params = {
    resource_id: attachment.id
  };
  let res = await downloadResourceObject(params);
  if (!res.error_status) {
    let downloadUrl = res.result?.download_url;
    if (!downloadUrl) {
      ElMessage.error('下载链接为空');
      return;
    }
    downloadUrl = downloadUrl + '?filename=' + encodeURIComponent(attachment.resource_name);
    // 创建一个隐藏的 <a> 标签
    const link = document.createElement('a');
    link.href = downloadUrl;
    link.download = attachment.resource_name; // 设置下载文件的名称
    link.style.display = 'none';

    // 将 <a> 标签添加到文档
    document.body.appendChild(link);
    // 触发点击事件
    link.click();
    // 移除 <a> 标签
    document.body.removeChild(link);
  }
}
function turnOnMsgChooseModel() {
  // 启动消息流选择模式
  chooseModel.value = true;
  chooseMsgAll.value = true;
  chooseMsgCnt.value = 0;
  // 选择模式下，将消息流的所有消息都设置为选中
  for (let i = 0; i < msgFlow.value.length; i++) {
    let questionId = msgFlow.value[i].qa_value.question[0].msg_id;
    msgFlow.value[i].qa_value.question[0].msg_is_selected = true;
    chooseMsgCnt.value += 1;
    if (msgFlow.value[i].qa_value.answer[questionId]) {
      for (let j = 0; j < msgFlow.value[i].qa_value.answer[questionId].length; j++) {
        msgFlow.value[i].qa_value.answer[questionId][j].msg_is_selected = true;
        chooseMsgCnt.value += 1;
      }
    }
  }
  return chooseMsgCnt.value;
}
function turnOffMsgChooseModel() {
  chooseModel.value = false;
  chooseMsgAll.value = false;
  chooseMsgCnt.value = 0;
  // 选择模式下，将消息流的所有消息都设置为选中
  for (let i = 0; i < msgFlow.value.length; i++) {
    let questionId = msgFlow.value[i].qa_value.question[0].msg_id;
    msgFlow.value[i].qa_value.question[0].msg_is_selected = false;
    chooseMsgCnt.value += 1;
    if (msgFlow.value[i].qa_value.answer[questionId]) {
      for (let j = 0; j < msgFlow.value[i].qa_value.answer[questionId].length; j++) {
        msgFlow.value[i].qa_value.answer[questionId][j].msg_is_selected = false;
        chooseMsgCnt.value += 1;
      }
    }
  }
}
function reformatFileSize(bytes: number) {
  if (!bytes) {
    return '0 B';
  }
  let newBytes = bytes * 1021 * 1024;
  const units = ['B', 'KB', 'MB', 'GB'];
  let unitIndex = 0;

  if (!newBytes) {
    return '';
  }
  while (newBytes >= 1024 && unitIndex < units.length - 1) {
    newBytes /= 1024;
    unitIndex++;
  }
  return `${newBytes.toFixed(2)} ${units[unitIndex]}`;
}
function isJson(result: string) {
  try {
    JSON.parse(result);
  } catch (e) {
    return false;
  }
  return true;
}
// onBeforeRouteLeave((to, from, next) => {
//   closeUploadManager();
//   next();
// });
const emit = defineEmits(['update:text', 'click-recommend-question', 'select-msg', 'add-quote', 'ready']);
defineExpose({
  getSelectMsg,
  unSelectMessages,
  selectAllMessages,
  beginAnswer,
  updateAnswer,
  finishAnswer,
  stopAnswer,
  updateWorkflowItemStatus,
  updateRecommendQuestion,
  turnOnMsgChooseModel,
  turnOffMsgChooseModel,
  refreshMsgFlow,
  scrollToBottom
});
watch(
  () => props.sessionCode,
  async newVal => {
    if (newVal && newVal !== currentSessionCode.value) {
      currentSessionCode.value = newVal;
      await refreshMsgFlow();
    }
  },
  { immediate: true }
);
watch(
  () => props.welcomeConfig,
  async newVal => {
    if (newVal) {
      localWelComeConfig.value = newVal;
    }
  },
  { immediate: true }
);
</script>

<template>
  <el-scrollbar
    ref="msgFlowScrollbarRef"
    v-loading="loadingMessages"
    element-loading-text="记忆加载中..."
    wrap-style="width: 100%;"
    view-style="width: 100%;height: 100%;"
    @scroll="handleScroll"
    @wheel="handleWheel"
  >
    <el-container>
      <el-main class="msg-main" @dragover.prevent="handleDragOver">
        <el-row style="width: 100%">
          <el-col :span="2" :xs="1" />
          <el-col :span="20" :xs="22">
            <div id="message-flow-box" ref="msgFlowBoxRef">
              <WelComeArea
                v-show="(!msgFlow?.length && !loadingMessages) || localWelComeConfig?.keep"
                :welcome-config="localWelComeConfig"
                @prefix-question-click="args => emit('click-recommend-question', { question: args })"
              />
              <div
                v-for="(item, idx) in msgFlow"
                :key="idx"
                class="msg-flow-qa-box"
                @mouseleave="
                  item.show_button_question_area = false;
                  item.show_button_answer_area = false;
                "
              >
                <div class="msg-flow-question-box" @mouseenter="item.show_button_question_area = true">
                  <div v-if="item?.qa_value?.question?.[0] && chooseModel" class="msg-check-box">
                    <el-checkbox
                      v-model="item.qa_value.question[0].msg_is_selected"
                      @change="checkSelectMsgMiddleStatus"
                    />
                  </div>
                  <div class="msg-flow-question-content">
                    <div v-show="item?.show_button_question_area" class="msg-question-head-button-area">
                      <div class="question-create-time-box">
                        <el-text class="msg-tips-text" style="min-width: 122px">
                          {{ item?.qa_value.question[0].create_time }}
                        </el-text>
                      </div>
                      <div class="question-button-box">
                        <div class="quote-right-container">
                          <el-tooltip content="引用" placement="top">
                            <SvgIcon
                              name="quote-right"
                              :width="16"
                              :height="16"
                              @click="addQuote(item.qa_value.question[0]?.attachment_list)"
                            />
                          </el-tooltip>
                        </div>
                        <div class="question-button" @click="copyQuestion(item)">
                          <el-image class="question-button-icon" src="/images/copy.svg" />
                        </div>
                      </div>
                    </div>
                    <div class="attachment-area">
                      <div v-for="(attachment, idx2) in item.qa_value.question[0]?.attachment_list" :key="idx2">
                        <div v-if="attachment.resource_type == 'image'" class="attachment-item">
                          <el-image
                            :zoom-rate="1.2"
                            :max-scale="7"
                            :min-scale="0.2"
                            fit="cover"
                            :src="attachment.resource_download_url || attachment.resource_show_url"
                            :preview-src-list="[attachment.resource_download_url || attachment.resource_show_url]"
                            class="attachment-item-img"
                          />
                        </div>
                        <template v-else-if="attachment.resource_type == 'document'">
                          <slot
                            v-if="$slots['document-attachment']"
                            name="document-attachment"
                            :attachment="attachment"
                          />
                          <div v-else class="attachment-item" @click="downloadAttachment(attachment)">
                            <div class="std-middle-box">
                              <el-image
                                :src="getResourceIcon({ resource_icon: attachment.resource_icon } as ResourceItem)"
                                class="attachment-item-img"
                              />
                            </div>
                            <div class="attachment-item-right">
                              <el-text style="width: 120px" truncated>
                                {{ attachment.resource_name }}
                              </el-text>
                              <div>
                                <el-text class="msg-tips-text" style="font-size: 12px; color: #909399">
                                  {{ reformatFileSize(attachment.resource_size_in_MB) }}
                                </el-text>
                              </div>
                            </div>
                          </div>
                        </template>
                        <template v-else-if="attachment.resource_type == 'code'">
                          <slot
                            v-if="$slots['document-attachment']"
                            name="document-attachment"
                            :attachment="attachment"
                          />
                          <div v-else class="attachment-item" @click="downloadAttachment(attachment)">
                            <div class="std-middle-box">
                              <el-image
                                :src="getResourceIcon({ resource_icon: attachment.resource_icon } as ResourceItem)"
                                class="attachment-item-img"
                              />
                            </div>
                            <div class="attachment-item-right">
                              <el-text style="width: 120px" truncated>
                                {{ attachment.resource_name }}
                              </el-text>
                              <div>
                                <el-text class="msg-tips-text" style="font-size: 12px; color: #909399">
                                  {{ reformatFileSize(attachment.resource_size_in_MB) }}
                                </el-text>
                              </div>
                            </div>
                          </div>
                        </template>
                        <div v-else-if="attachment.resource_type == 'video'" class="attachment-item">
                          <video controls style="height: 120px; width: 160px">
                            <source
                              :src="attachment.resource_download_url || attachment.resource_show_url"
                              type="video/mp4"
                            />
                            <source
                              :src="attachment.resource_download_url || attachment.resource_show_url"
                              type="video/webm"
                            />
                            <source
                              :src="attachment.resource_download_url || attachment.resource_show_url"
                              type="video/ogg"
                            />
                            Your browser does not support the video tag.
                          </video>
                        </div>
                        <div v-else-if="attachment.resource_type == 'audio'" class="attachment-item">
                          <audio controls>
                            <source
                              :src="attachment.resource_download_url || attachment.resource_show_url"
                              type="audio/mpeg"
                            />
                            <source
                              :src="attachment.resource_download_url || attachment.resource_show_url"
                              type="audio/ogg"
                            />
                            <source
                              :src="attachment.resource_download_url || attachment.resource_show_url"
                              type="audio/wav"
                            />
                            <source
                              :src="attachment.resource_download_url || attachment.resource_show_url"
                              type="audio/mp4"
                            />
                            <source
                              :src="attachment.resource_download_url || attachment.resource_show_url"
                              type="audio/x-m4a"
                            />
                            Your browser does not support the audio tag.
                          </audio>
                        </div>
                        <div v-else class="attachment-item" @click="downloadAttachment(attachment)">
                          <div class="std-middle-box">
                            <el-image src="/images/file.svg" class="attachment-item-img" />
                          </div>
                          <div class="attachment-item-right">
                            <el-text style="width: 120px" truncated>
                              {{ attachment.resource_name }}
                            </el-text>
                            <div>
                              <el-text class="msg-tips-text" style="font-size: 12px; color: #909399">
                                {{ reformatFileSize(attachment.resource_size_in_MB) }}
                              </el-text>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                    <div class="question-content">
                      <el-text class="question-content-text">
                        {{ item?.qa_value.question[0].msg_content }}
                      </el-text>
                    </div>
                  </div>
                  <div class="msg-flow-question-avatar">
                    <el-avatar
                      v-if="userInfoStore.userInfo?.user_avatar"
                      :src="userInfoStore.userInfo?.user_avatar"
                      style="background-color: white"
                    />
                    <el-avatar v-else style="background: #d1e9ff; cursor: pointer">
                      <el-text style="font-weight: 600; color: #1570ef">
                        {{ userInfoStore.userInfo?.user_nick_name_py }}
                      </el-text>
                    </el-avatar>
                  </div>
                </div>
                <div class="msg-flow-answer-box" @mouseenter="item.show_button_answer_area = true">
                  <div
                    v-if="item.qa_value.answer[item.qa_value.question[0]?.msg_id]?.[0] && chooseModel"
                    class="msg-check-box"
                  >
                    <el-checkbox
                      v-model="item.qa_value.answer[item.qa_value.question[0].msg_id][0].msg_is_selected"
                      @change="checkSelectMsgMiddleStatus"
                    />
                  </div>
                  <div class="msg-flow-answer-avatar">
                    <el-image
                      :src="currentSession?.app_icon || currentSession?.session_assistant_avatar"
                      style="background-color: white"
                      shape="square"
                      class="answer-avatar"
                      :style="'margin-top: ' + (qaWorkflowMap?.[item.qa_id]?.length ? '0' : '20px')"
                    />
                  </div>
                  <div class="msg-flow-answer-content">
                    <WorkFlowArea
                      :qa-finished="item.qa_finished"
                      :qa-workflow-open="item.qa_workflow_open"
                      :workflow-task="qaWorkflowMap?.[item.qa_id]"
                    />
                    <div class="msg-flow-answer-inner" :class="{ 'msg-flow-answer-inner-short': item?.short_answer }">
                      <div
                        v-for="(sub_finish_msg, idx) in item.qa_value.answer[item.qa_value.question[0]?.msg_id]"
                        style="width: 100%"
                      >
                        <div v-show="sub_finish_msg?.msg_reason_content_finish_html?.length" class="reason-container">
                          <div class="reason-header">
                            <el-button
                              v-if="!sub_finish_msg?.msg_reason_content_hide"
                              :icon="ArrowUp"
                              @click="sub_finish_msg.msg_reason_content_hide = true"
                            >
                              收起推理过程
                            </el-button>
                            <el-button
                              v-if="sub_finish_msg?.msg_reason_content_hide"
                              :icon="ArrowDown"
                              @click="sub_finish_msg.msg_reason_content_hide = false"
                            >
                              > 展开推理过程
                            </el-button>
                          </div>
                          <Transition name="slide">
                            <div v-show="!sub_finish_msg?.msg_reason_content_hide" class="reason-box">
                              <div
                                v-for="(sub_finish_msg_content, idx) in sub_finish_msg?.msg_reason_content_finish_html"
                                :key="idx"
                                style="width: 100%"
                                @mouseover="showSupDetailFn(item, $event)"
                                v-html="sub_finish_msg_content"
                              />
                            </div>
                          </Transition>
                        </div>
                        <div
                          v-for="(sub_finish_msg_content, idx) in sub_finish_msg?.msg_content_finish_html"
                          :key="idx"
                          style="width: 100%"
                          @mouseover="showSupDetailFn(item, $event)"
                          v-html="sub_finish_msg_content"
                        />
                      </div>
                      <SimpleProgress v-if="item?.qa_finished == false && !item?.qa_workflow_open" />
                      <div v-if="item?.qa_is_cut_off">
                        <el-text style="color: #c8cad9; font-size: 12px"> 此回答已停止 </el-text>
                      </div>
                    </div>
                  </div>
                  <div
                    v-if="showScrollbarButton"
                    v-show="item.show_button_answer_area == true || item?.short_answer"
                    class="msg-answer-right-button-area"
                  >
                    <div class="answer-button-box">
                      <div class="answer-button" @click="switchAnswerLength(item)">
                        <el-image v-if="item?.short_answer" src="/images/arrow_down_grey.svg" />
                        <el-image v-else class="answer-button-icon" src="/images/arrow_up_grey.svg" />
                      </div>
                    </div>
                  </div>
                </div>
                <div class="msg-flow-footer-box">
                  <div class="msg-flow-answer-button-area">
                    <div class="msg-flow-answer-button-area-left">
                      <div
                        v-show="msgFlowReference?.[item.qa_value.question?.[0]?.msg_id]"
                        @click="showReferenceDrawerFn(msgFlowReference?.[item.qa_value.question?.[0]?.msg_id])"
                      >
                        <el-text class="reference-link-text"> 参考来源 </el-text>
                      </div>
                      <div class="reference-link-box">
                        <el-text class="reference-link-cnt">
                          {{ msgFlowReference?.[item.qa_value.question?.[0]?.msg_id]?.length }}
                        </el-text>
                      </div>
                      <el-divider
                        v-show="msgFlowReference?.[item.qa_value.question?.[0]?.msg_id]"
                        direction="vertical"
                      />
                      <div class="answer-create-time-box">
                        <el-text class="msg-tips-text">
                          {{ getAnswerCreateTime(item) }}
                        </el-text>
                      </div>
                    </div>
                    <div class="msg-flow-answer-button-area-right">
                      <div class="msg-flow-answer-button" @click="copyAnswer(item)">
                        <div class="msg-flow-answer-button-icon-box">
                          <el-image class="msg-flow-answer-button-icon" src="/images/copy.svg" />
                        </div>
                      </div>
                      <div class="msg-flow-answer-button" @click="addLike(item)">
                        <div class="msg-flow-answer-button-icon-box">
                          <el-image
                            v-if="item?.qa_value?.answer?.[item?.qa_value?.question?.[0]?.msg_id]?.[0]?.msg_remark == 1"
                            class="msg-flow-answer-button-icon"
                            src="/images/thumbs_up_green.svg"
                          />
                          <el-image v-else class="msg-flow-answer-button-icon" src="/images/thumbs_up_grey.svg" />
                        </div>
                      </div>
                      <div class="msg-flow-answer-button" @click="addDislike(item)">
                        <div class="msg-flow-answer-button-icon-box">
                          <el-image
                            v-if="
                              item?.qa_value?.answer?.[item?.qa_value?.question?.[0]?.msg_id]?.[0]?.msg_remark == -1
                            "
                            class="msg-flow-answer-button-icon"
                            src="/images/thumbs_down_red.svg"
                          />
                          <el-image v-else class="msg-flow-answer-button-icon" src="/images/thumbs_down_grey.svg" />
                        </div>
                      </div>
                    </div>
                  </div>
                  <div class="msg-flow-recommend-area">
                    <div
                      v-for="(sub_question, index) in msgRecommendQuestion?.[item?.qa_value.question?.[0]?.msg_id]"
                      :key="index"
                      class="msg-flow-recommend-box"
                      @click="clickRecommendQuestion(sub_question)"
                    >
                      <el-text>
                        {{ sub_question.recommend_question }}
                      </el-text>
                      <div class="relate-question-button">
                        <el-image src="/images/arrow_right_grey.svg" style="width: 12px; height: 12px" />
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </el-col>
          <el-col :span="2" :xs="1" />
        </el-row>
        <div
          v-show="scrollToFlag && showScrollbarButton"
          class="to-bottom-box"
          @click="scrollToTargetQa(1)"
          @dblclick="scrollToBottom()"
        >
          <el-button class="to-top-button">
            <el-image src="/images/to_bottom.svg" class="to-top-button-icon" />
          </el-button>
        </div>
        <div
          v-show="scrollToFlag && showScrollbarButton"
          class="to-top-box"
          @click="scrollToTargetQa(-1)"
          @dblclick="scrollToTop()"
        >
          <el-button class="to-top-button">
            <el-image src="/images/to_top.svg" class="to-top-button-icon" />
          </el-button>
        </div>
        <div v-if="showSupDetail" id="sup_detail_box" :style="tooltipStyle" @mouseleave="showSupDetail = false">
          <div class="reference-title">
            <div class="std-middle-box">
              <el-image
                v-if="currentSupDetail?.resource_icon"
                :id="currentSupDetail?.resource_icon"
                :src="getResourceIcon(currentSupDetail)"
                class="reference-img"
                @error="retryGetIcon(currentSupDetail)"
              >
                <template #error>
                  <div class="image-slot">
                    <el-icon><IconPicture /></el-icon>
                  </div>
                </template>
              </el-image>
            </div>
            <div class="std-middle-box" style="max-width: 95%; justify-content: flex-start">
              <el-text truncated class="reference-site-name">
                {{ currentSupDetail?.resource_name }}
              </el-text>
            </div>
          </div>
          <div class="reference-name">
            <el-text truncated class="reference-name-text" @click="openReference(currentSupDetail)">
              {{ currentSupDetail?.resource_title }}
            </el-text>
          </div>
          <div class="reference-text-box">
            <el-text line-clamp="2" class="reference-text">
              {{ currentSupDetail?.ref_text }}
            </el-text>
          </div>
        </div>
        <el-drawer v-model="showReferenceDrawer" title="参考来源" :size="referenceDrawerWidth">
          <el-scrollbar>
            <div id="reference_drawer_body">
              <div v-for="(item, idx) in referenceDrawerData" :key="idx" class="reference-item">
                <div class="reference-title">
                  <div class="std-middle-box">
                    <el-image
                      v-if="item?.resource_icon"
                      :id="item?.resource_icon"
                      :src="getResourceIcon(item)"
                      class="reference-img"
                      @error="retryGetIcon(item)"
                    >
                      <template #error>
                        <div class="image-slot">
                          <el-icon><IconPicture /></el-icon>
                        </div>
                      </template>
                    </el-image>
                  </div>
                  <div class="std-middle-box">
                    <el-text truncated class="reference-site-name">
                      {{ item?.resource_name }}
                    </el-text>
                  </div>
                </div>
                <div class="reference-name" @click="openReference(item)">
                  <el-text truncated class="reference-name-text">
                    {{ item.resource_title }}
                  </el-text>
                </div>
                <div class="reference-text-box">
                  <div
                    v-show="item?.showAll"
                    style="cursor: pointer"
                    @click="item.showAll = false"
                    v-html="mdAnswer.render(item?.ref_text)"
                  />
                  <el-text
                    v-show="!item?.showAll"
                    truncated
                    class="reference-text"
                    style="cursor: pointer"
                    @click="item.showAll = true"
                  >
                    {{ item?.ref_text }}
                  </el-text>
                </div>
              </div>
            </div>
          </el-scrollbar>
        </el-drawer>
        <el-dialog v-model="showDebugInfoFlag" title="工作流明细" width="90vw" :fullscreen="true">
          <el-tabs v-model="currentDebugInfoViewModel">
            <el-tab-pane label="表格" name="table">
              <el-table :data="currentDebugInfo" stripe border highlight-current-row height="80vh">
                <el-table-column prop="id" label="ID" width="100" sortable />
                <el-table-column prop="user_id" label="用户ID" width="100" sortable />
                <el-table-column prop="workflow_id" label="工作流ID" width="120" sortable />
                <el-table-column prop="workflow_node_id" label="节点ID" width="100" sortable />
                <el-table-column prop="workflow_node_name" label="节点名称" width="160">
                  <template #default="scope">
                    <div class="workflow_node_name">
                      <div class="std-middle-box">
                        <el-image :src="scope.row.workflow_node_icon" class="node-icon" />
                      </div>
                      <div class="std-middle-box">
                        <el-tooltip :content="scope.row.workflow_node_desc" placement="top">
                          <el-text>{{ scope.row.workflow_node_name }}</el-text>
                        </el-tooltip>
                      </div>
                    </div>
                  </template>
                </el-table-column>
                <el-table-column prop="task_status" label="执行状态" width="120" sortable />
                <el-table-column prop="task_params" label="任务参数" min-width="120" show-overflow-tooltip>
                  <template #default="scope">
                    <div>
                      <el-text>{{ scope.row.task_params }}</el-text>
                    </div>
                  </template>
                </el-table-column>
                <el-table-column prop="task_retry_cnt" label="任务重试" width="120" />
                <el-table-column prop="task_result" label="任务提示词" min-width="120" show-overflow-tooltip>
                  <template #default="scope">
                    <div>
                      <el-text>
                        {{ scope.row.task_prompt }}
                      </el-text>
                    </div>
                  </template>
                </el-table-column>
                <el-table-column prop="task_result" label="执行结果" min-width="120" show-overflow-tooltip>
                  <template #default="scope">
                    <div>
                      <el-text v-if="isJson(scope.row.task_result)">
                        {{ JSON.parse(scope.row.task_result, null) }}
                      </el-text>
                      <el-text v-else>
                        {{ scope.row.task_result }}
                      </el-text>
                    </div>
                  </template>
                </el-table-column>
                <el-table-column prop="task_trace_log" label="异常日志" min-width="120">
                  <template #default="scope">
                    <div>
                      <el-text truncated>
                        {{ scope.row.task_trace_log }}
                      </el-text>
                    </div>
                  </template>
                </el-table-column>
                <el-table-column prop="begin_time" label="开始时间" width="180" sortable />
                <el-table-column prop="end_time" label="完成时间" width="180" sortable />
                <el-table-column prop="duration" label="耗时（秒）" width="180" sortable />
              </el-table>
            </el-tab-pane>
          </el-tabs>
        </el-dialog>
      </el-main>
    </el-container>
    <div
      v-show="questionRunningCnt"
      class="scroll-box"
      :style="{ left: '50%' }"
      :class="{ 'glowing-border': !userStopScroll }"
      @click="
        userStopScroll = !userStopScroll;
        scrollToBottom();
      "
    >
      <el-button class="to-top-button">
        <el-image src="/images/to_bottom.svg" class="to-top-button-icon" />
      </el-button>
    </div>
  </el-scrollbar>
</template>

<style scoped lang="scss">
.msg-main {
  height: 100%;
  padding: 0 !important;
  position: relative;
}
:deep(.hljs) {
  font-size: 14px !important;
  line-height: 21px !important;
}
:deep(code) {
  max-width: 751px;
  margin: 3px 5px;
  border-radius: 6px;
  font-size: 14px !important;
  line-height: 21px !important;
  white-space: pre-wrap;
  overflow: auto;
}
:deep(code:not([class])) {
  background: rgba(0, 0, 0, 0.06);
}
:deep(pre:not([class])) {
  background: rgba(0, 0, 0, 0.06);
  overflow: auto;
  white-space: pre-wrap;
}
:deep(pre:not([class]) code:not([class])) {
  background: transparent;
}
#message-flow-box {
  display: flex;
  flex-direction: column;
  gap: 12px;
  align-items: flex-start;
  justify-content: space-between;
  width: 100%;
  margin-top: 24px;
  position: relative;
}
.to-bottom-box {
  position: absolute;
  bottom: 20px;
  z-index: 999;
  right: 20px;
}
.to-top-button {
  width: 40px;
  height: 40px;
  border: 1px solid #eaecf0;
  box-shadow: 0 1px 2px 0 #1018280d;
  border-radius: 20px;
}
.scroll-box {
  position: absolute;
  bottom: 60px;
  z-index: 999;
  border: 2px solid transparent; /* 初始边框为透明 */
  border-radius: 24px;
  transition: box-shadow 0.3s ease-in-out; /* 添加过渡效果 */
}
.node-icon {
  width: 24px;
  height: 24px;
}
@keyframes glowing {
  0% {
    box-shadow:
      0 0 5px #00aaff,
      0 0 10px #00aaff,
      0 0 20px #00aaff;
    border-color: #00aaff;
  }
  50% {
    box-shadow:
      0 0 20px #00aaff,
      0 0 40px #00aaff,
      0 0 60px #00aaff;
    border-color: #00aaff;
  }
  100% {
    box-shadow:
      0 0 5px #00aaff,
      0 0 10px #00aaff,
      0 0 20px #00aaff;
    border-color: #00aaff;
  }
}
.glowing-border {
  box-shadow:
    0 0 10px #00aaff,
    0 0 20px #00aaff,
    0 0 30px #00aaff; /* 绿色发光效果 */
  border: 2px solid #00aaff; /* 发光边框 */
  animation: glowing 1.5s infinite; /* 1.5秒循环动画 */
}
.to-top-button-icon {
  width: 20px;
  height: 20px;
}
.to-top-box {
  position: absolute;
  top: 20px;
  z-index: 999;
  right: 20px;
}
.msg-flow-qa-box {
  display: flex;
  flex-direction: column;
  padding: 16px 0;
  gap: 16px;
  align-items: flex-start;
  justify-content: center;
  width: 100%;
}
.msg-tips-text {
  font-weight: 400;
  font-size: 12px;
  line-height: 20px;
  color: #475467;
}
.msg-flow-question-box {
  display: flex;
  flex-direction: row;
  gap: 12px;
  width: 100%;
  justify-content: flex-end;
  position: relative;
}
.msg-flow-question-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
  max-width: calc(100% - 130px);
  align-items: flex-end;
  justify-content: center;
  /* background: rgb(209, 233, 255); */
  padding: 8px 12px;
  border-radius: 8px;
  position: relative;
}
.msg-question-head-button-area {
  position: absolute;
  top: -28px;
  right: 0;
  display: flex;
  flex-direction: row-reverse;
  justify-content: flex-start;
  width: 100%;
  align-items: center;
  gap: 6px;
}
.question-button-box {
  display: flex;
  flex-direction: row;
  gap: 8px;
}
.question-button {
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  border-radius: 4px;
}
.quote-right-container {
  width: 22px;
  height: 22px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  &:hover {
    background: #f0f9ff;
  }
}
.question-button:hover {
  background: #f0f9ff;
}
.question-button:active {
  background: #d9d9d9;
  transform: scale(0.95);
}
.question-button-icon {
  width: 20px;
  height: 20px;
}
.question-create-time-box {
  display: flex;
  flex-direction: row;
  gap: 8px;
}
.msg-flow-answer-box {
  display: flex;
  flex-direction: row;
  gap: 12px;
  width: 100%;
  justify-content: flex-start;
  position: relative;
}
.msg-flow-answer-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
  width: calc(100% - 130px);
  align-items: flex-start;
  justify-content: center;
  background: #ffffff;
  padding: 0 12px;
  border-radius: 8px;
  position: relative;
}
.msg-flow-answer-inner {
  display: flex;
  flex-direction: column;
  position: relative;
  width: 100%;
  align-items: flex-start;
  justify-content: space-between;
  overflow: hidden;
}
.msg-flow-answer-inner-short {
  max-height: 300px;
  position: relative;
}
.msg-flow-answer-inner-short::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 80px; /* 羽化的高度 */
  background: linear-gradient(to bottom, rgba(255, 255, 255, 0), rgba(255, 255, 255, 0.8), rgba(255, 255, 255, 1));
  pointer-events: none; /* 确保不影响交互 */
}
.msg-answer-right-button-area {
  display: flex;
  flex-direction: row-reverse;
  justify-content: space-between;
  align-items: flex-start;
  z-index: 40;
}
.answer-button-box {
  display: flex;
  flex-direction: row;
  gap: 8px;
}
.answer-button {
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  border-radius: 4px;
  padding: 4px;
}
.answer-button:hover {
  background: #f0f9ff;
}
.answer-button:active {
  background: #d9d9d9;
  transform: scale(0.95);
}
.answer-button-icon {
  width: 12px;
  height: 12px;
}
.msg-flow-footer-box {
  display: flex;
  flex-direction: column;
  gap: 12px;
  width: 100%;
  justify-content: flex-start;
  position: relative;
}
.msg-flow-answer-button-area {
  display: flex;
  flex-direction: row;
  gap: 8px;
  align-items: center;
  justify-content: space-between;
  position: absolute;
  top: -15px;
  left: 50px;
  width: calc(100% - 100px);
}
.msg-flow-answer-button {
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}
.msg-flow-answer-button-icon-box {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  border-radius: 4px;
}
.msg-flow-answer-button-icon {
  width: 20px;
  height: 20px;
  &:hover {
    background: #f0f9ff;
  }
}
.msg-flow-recommend-area {
  margin-top: 16px;
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  gap: 8px;
  margin-left: 50px;
  margin-right: 50px;
}
.msg-flow-recommend-box {
  display: flex;
  flex-direction: row;
  gap: 8px;
  align-items: center;
  justify-content: center;
  padding: 4px 8px;
  border-radius: 4px;
  background-color: white;
  cursor: pointer;
}
.msg-flow-recommend-box:hover {
  background-color: #f0f9ff;
}
.msg-flow-recommend-box:active {
  background-color: #d9d9d9;
  transform: scale(0.95);
}
.reference-link-text {
  font-size: 12px;
  font-weight: 400;
  cursor: pointer;
  line-height: 20px;
  color: #1570ef;
}
.reference-link-box {
  background-color: #f2f4f7;
  padding: 0 4px;
  border-radius: 3px;
}
.reference-link-cnt {
  font-size: 12px;
  font-weight: 500;
  line-height: 18px;
  color: #34495e;
}
.msg-flow-answer-button-area-left {
  display: flex;
  flex-direction: row;
  gap: 4px;
  align-items: center;
  justify-content: flex-start;
}
.msg-flow-answer-button-area-right {
  display: flex;
  flex-direction: row;
  gap: 4px;
  align-items: center;
  justify-content: flex-start;
}
sup {
  border-radius: 4px;
  background: #f9f9f9 !important;
  /* 添加其他样式属性 */
}
#sup_detail_box {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 8px 12px;
  background: #ffffff;
  border-radius: 8px;
  position: absolute;
  z-index: 999;
  top: 0;
  left: 0;
  width: 300px;
  max-height: 150px;
  box-shadow: 0 12px 16px -4px #10182814;
}
.std-middle-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
.reference-title {
  display: flex;
  flex-direction: row;
  gap: 4px;
}
.reference-img {
  width: 16px;
  height: 16px;
}
.reference-site-name {
  font-weight: 400;
  font-size: 12px;
  line-height: 18px;
  color: #475467;
}
.reference-name-text {
  font-weight: 500;
  font-size: 14px;
  line-height: 20px;
  color: #101828;
  cursor: pointer;
}
.reference-name-text:hover {
  color: #1570ef;
}
.reference-text-box {
  display: flex;
  flex-direction: column;
  align-items: flex-start; /* 左对齐内容 */
  justify-content: flex-start;
  gap: 8px; /* 增加元素间的间距 */
  flex-wrap: wrap;
  width: 100%;
  padding: 16px; /* 添加内边距 */
  margin: 16px 0; /* 添加外边距 */
  border: 1px solid #e5e7eb; /* 添加边框 */
  border-radius: 8px; /* 圆角边框 */
  background-color: #f9fafb; /* 背景颜色 */
  box-sizing: border-box; /* 确保内边距和边框不影响宽度 */
}
.reference-text {
  font-family: 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif; /* 更换字体 */
  font-weight: 400;
  font-size: 14px;
  line-height: 22px; /* 增加行高，提高可读性 */
  color: #4b5563; /* 调整文字颜色 */
  width: 100%; /* 确保文本宽度一致 */
  overflow: hidden; /* 隐藏溢出内容 */
  text-overflow: ellipsis; /* 添加省略号 */
  display: -webkit-box;
  -webkit-line-clamp: 3; /* 截断为 3 行 */
  -webkit-box-orient: vertical;
}
.attachment-area {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-end;
  flex-wrap: wrap;
  gap: 8px;
}

.attachment-item {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 4px;
  background: #f0f0f0;
  padding: 12px 16px;
  border: 1px solid #d0d5dd;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  transition: all 0.3s ease;
  &:hover {
    box-shadow: 2px 2px 3px rgba(0, 0, 0, 0.15);
    .attachment-options {
      display: inline-block;
    }
  }
}
.attachment-item-img {
  width: 36px;
  height: 36px;
}
.attachment-item-right {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}
.msg-flow-workflow-box {
  width: 100%;
}
.open-workflow-head-left {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 8px;
}
.close-workflow-area {
  min-width: 144px;
  padding: 6px 12px;
  background: #f9fafb;
  border-radius: 8px;
  border: 1px solid #f2f4f7;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}
.close-workflow-area-left {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 6px;
}
.open-workflow-area {
  border: 1px solid #d0d5dd;
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 12px;
  border-radius: 8px;
  width: calc(100% - 24px);
  max-height: 160px;
  overflow: hidden;
}
.open-workflow-head {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
}
.sub-workflow-area {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 8px;
}
.sub-workflow-head {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 4px;
  min-width: 80px;
}
.sub-workflow-show-info {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  padding: 4px 8px;
  background-color: #f9f9fb;
  gap: 16px;
  max-width: calc(100% - 16px);
}
.msg-check-box {
  position: absolute;
  left: -30px;
  top: 10px;
}
#choose-model-area {
  display: flex;
  flex-direction: row;
  gap: 12px;
  align-items: center;
  justify-content: space-between;
  width: calc(100% - 24px);
  max-width: 900px;
  padding: 12px;
  background: #f9f9f9;
  border-radius: 8px;
}
.question-content {
  width: 100%;
  display: flex;
  flex-direction: row;
  justify-content: flex-end;
}
.question-content-text {
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  color: #101828;
  background: rgb(209, 233, 255);
  padding: 8px 8px 8px 16px;
  border-radius: 10px;
  max-width: 100%;
  white-space: pre-line;
  word-break: break-word;
}
.reason-box {
  width: calc(100% - 30px);
  /* 盒子的内边距，上下 20px，左右 30px */
  padding: 6px 12px;
  /* 盒子的边框样式，1px 宽的浅灰色实线 */
  border: 1px solid #e0e0e0;
  /* 盒子的圆角半径为 8px */
  border-radius: 8px;
  /* 盒子内部文字颜色 */
  color: #333;
  /* 盒子内文字字体 */
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  /* 盒子内文字大小 */
  font-size: 16px;
  /* 盒子内文字行高 */
  line-height: 1.6;
  /* 盒子的阴影效果，水平偏移 0px，垂直偏移 2px，模糊半径 5px，颜色为浅灰色半透明 */
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  border-left: 4px solid #1570ef; /* 在引用块左侧添加蓝色边框 */
  background-color: #f0f7ff; /* 设置引用块的背景颜色 */
  font-style: italic; /* 设置引用内容为斜体 */
}
#reference_drawer_body {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.reference-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.std-middle-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.reference-title {
  display: flex;
  flex-direction: row;
  gap: 4px;
}
.reference-img {
  width: 16px;
  height: 16px;
}
.reference-site-name {
  font-weight: 400;
  font-size: 12px;
  line-height: 18px;
  color: #475467;
}
.reference-name-text {
  font-weight: 500;
  font-size: 14px;
  line-height: 20px;
  color: #101828;
}
.reference-text-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  gap: 4px;
  flex-wrap: wrap;
  width: 100%;
}
.reference-text {
  font-weight: 400;
  font-size: 14px;
  line-height: 20px;
  color: #667085;
}
.workflow_node_name {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 4px;
}
.answer-avatar {
  width: 40px;
  height: 40px;
  border-radius: 6px;
}
.reason-container {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  align-content: flex-start;
  gap: 6px;
}
.reason-header {
  /* 增大圆角半径，使盒子更圆润 */

  display: flex;
  justify-content: flex-start;
  align-items: flex-start;
}

/* 定义淡入淡出动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
}
:deep(.msg-flow-answer-inner table) {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 1rem;
  margin-top: 1rem;
}
:deep(.msg-flow-answer-inner th) {
  border: 1px solid #d0d5dd;
  padding: 8px;
  text-align: left;
}
:deep(.msg-flow-answer-inner) {
  .hljs-code {
    td {
      border: none;
      padding: 0 0 0 8px;
      width: calc(100% - 8px);
    }
  }
  td {
    border: 1px solid #d0d5dd;
    padding: 8px;
    text-align: left;
  }
}
:deep(.msg-flow-answer-inner th) {
  background-color: #f2f2f2;
}

/* 定义 slide 过渡的入场动画 */
.slide-enter-active {
  animation: slide-down 0.3s ease-out;
}
/* 定义 slide 过渡的出场动画 */
.slide-leave-active {
  animation: slide-up 0.3s ease-in;
}
/* 定义向下滑动的动画 */
@keyframes slide-down {
  from {
    max-height: 0;
    opacity: 0;
  }
  to {
    max-height: 500px; /* 根据实际内容调整最大高度 */
    opacity: 1;
  }
}
/* 定义向上滑动的动画 */
@keyframes slide-up {
  from {
    max-height: 500px; /* 根据实际内容调整最大高度 */
    opacity: 1;
  }
  to {
    max-height: 0;
    opacity: 0;
  }
}

@media (width<768px) {
  #message-flow-box {
    gap: 0;
  }
  .msg-flow-qa-box {
    padding: 8px 0;
    gap: 8px;
  }
  .msg-flow-question-box {
    gap: 4px;
  }
  .question-button-icon {
    width: 14px;
    height: 14px;
  }
  .msg-flow-question-content {
    max-width: calc(100% - 72px);
  }
  .question-content-text {
    font-size: 14px;
    line-height: 20px;
  }
  .msg-flow-answer-button-area {
    top: -10px;
    left: 0;
    width: 100%;
  }
  .msg-flow-answer-button-icon {
    width: 14px;
    height: 14px;
  }
  .msg-flow-answer-box {
    gap: 4px;
  }
  .msg-flow-answer-content {
    width: calc(100% - 50px);
    padding: 0;
  }
  :deep(.hljs) {
    font-size: 14px !important;
    line-height: 20px !important;
  }
  :deep(p) {
    font-size: 14px !important;
    line-height: 20px !important;
  }
  :deep(li) {
    font-size: 14px !important;
    line-height: 20px !important;
  }
  .open-workflow-area {
    gap: 6px;
    padding: 8px;
  }
  .sub-workflow-area {
    overflow: scroll;
  }
  .msg-check-box {
    position: absolute;
    left: -12px;
  }
  #choose-model-area {
    padding: 8px;
    gap: 6px;
  }
}
</style>
