import markdownItKatex from '@vscode/markdown-it-katex';
import { ElMessage } from 'element-plus';
import hljs from 'highlight.js';
import MarkdownIt from 'markdown-it';
import markdownItMermaid from 'markdown-it-mermaid-plugin';
import mermaid from 'mermaid';
import { ref, nextTick } from 'vue';

import { appDetail, initAppSession } from '@/api/appCenterApi';
import {
  create_qa,
  get_workflow_progress_batch,
  search_messages,
  search_qa,
  search_reference,
  update_recommend_question
} from '@/api/next_console';
import { askAgentQuestion, consoleInput } from '@/components/appCenter/ts/agent-console';
import router from '@/router';
import { IAppMetaInfo } from '@/types/appCenterType';
import { assistant } from '@/types/assistant';
import {
  msg_queue_item,
  qa_item,
  recommend_question_item,
  reference_map,
  session_item,
  workflow_task_map,
  running_question_meta
} from '@/types/next_console';
import '@/styles/katex.min.css';
import Clipboard from 'clipboard';
export const CurrentAgentApp = ref<IAppMetaInfo>({ app_code: '' }); // 当前应用
export const CurrentAgentAppSession = ref<session_item>({ id: 0 }); // 当前应用会话
export const CurrentAgentAppQas = ref<qa_item[]>([]); // 当前应用问答
export const LoadingStatus = ref(false); // 加载状态
export const AgentAppMsgFlow = ref<msg_queue_item[]>([]);
export const QAWorkFlowMap = ref<workflow_task_map>({});
export const CurrentAgentReference = ref<reference_map>({});
export const FlowIsScrolling = ref(false);
export const agentFlowBoxRef = ref<HTMLDivElement>();
export const AgentFlowScrollbarRef = ref();
export const AgentScrollButtonTimeout = ref(null);
export const scrollTimer = ref();
export const scrollToFlag = ref(false);
export const CurrentAgent = ref<assistant>({ id: 0 });
export const sessionAttachData = ref(null);
export const running_questions = ref<running_question_meta[]>([]);
export async function initAgentApp(app_code: string, session_code: string) {
  // 初始化应用信息
  LoadingStatus.value = true;
  await getAgentApp(app_code);
  // 初始化会话信息
  await getAgentAppSession(app_code, session_code);
  await initAgentAppQas(app_code, session_code);
  // 有会话，则加载会话的消息
  await initAgentAppMsg(app_code, session_code);
  LoadingStatus.value = false;
}
export async function getAgentApp(code: string) {
  // 获取当前应用
  const result = await appDetail({
    app_code: code
  });
  if (!result.error_status) {
    CurrentAgentApp.value = result.result;
  }
}
export async function getAgentAppSession(app_code: string, session_code: string) {
  if (!app_code) {
    return;
  }
  const result = await initAppSession({
    app_code: app_code,
    session_code: session_code,
    session_test: true
  });
  if (!result.error_status) {
    CurrentAgentAppSession.value = result.result;
    router.replace({
      params: {
        app_code: app_code,
        session_code: CurrentAgentAppSession.value.session_code
      }
    });
  }
}
export async function initAgentAppQas(app_code: string, session: string) {
  if (!CurrentAgentAppSession.value.id) {
    return;
  }
  const result = await search_qa({
    session_id: [CurrentAgentAppSession.value.id]
  });
  if (!result.error_status) {
    CurrentAgentAppQas.value = result.result;
  }
}
export async function addAgentAppQa() {
  const data = await create_qa({
    session_id: CurrentAgentAppSession.value.id,
    qa_topic: consoleInput.value
  });
  CurrentAgentAppQas.value.unshift(data.result);
  return data.result;
}
export async function initAgentAppMsg(app_code: string, session: string) {
  // 更新问答
  if (!CurrentAgentAppQas.value?.length) {
    return;
  }
  const result = await search_messages({
    qa_id: CurrentAgentAppQas.value.map(item => item.qa_id)
  });
  if (!result.error_status) {
    AgentAppMsgFlow.value = result.result;
    for (let i = 0; i < AgentAppMsgFlow.value.length; i++) {
      const item = AgentAppMsgFlow.value[i];
      splitMarkdown(item);
      item.qa_finished = true;
    }
    if (AgentAppMsgFlow.value?.length) {
      initAgentWorkflow();
      initAgentReference();
    }
  }
}

export async function initAgentWorkflow() {
  const res = await get_workflow_progress_batch({
    qa_ids: CurrentAgentAppQas.value.map(item => item.qa_id)
  });
  if (!res.error_status) {
    QAWorkFlowMap.value = res.result;
  }
}
export async function initAgentReference() {
  const params = { msg_id_list: [] };
  for (let i = 0; i < AgentAppMsgFlow.value.length; i++) {
    for (let j = 0; j < AgentAppMsgFlow.value[i].qa_value.question.length; j++) {
      params.msg_id_list.push(AgentAppMsgFlow.value[i].qa_value.question[j].msg_id);
    }
  }
  const res = await search_reference(params);
  if (!res.error_status) {
    CurrentAgentReference.value = res.result;
    if (CurrentAgentReference.value) {
      for (const msg_item of AgentAppMsgFlow.value) {
        for (const question of msg_item.qa_value.question) {
          if (CurrentAgentReference.value?.[question.msg_id]) {
            // 生成参考文献链接，并添加至msg_content 后
            let reference_markdown_text = '';
            const reference_list = CurrentAgentReference.value[question.msg_id];
            for (let i = 0; i < reference_list.length; i++) {
              const base_url = window.location.origin;
              if (reference_list[i].source_type == 'resource') {
                reference_markdown_text += `\n\n [${i + 1}]: ${base_url}/#/next_console/resources/resource_viewer/${reference_list[i].resource_id} `;
              } else if (reference_list[i].source_type == 'webpage') {
                reference_markdown_text += `\n\n [${i + 1}]: ${reference_list[i].resource_id} `;
              }
            }
            if (!msg_item.qa_value.answer[question.msg_id][0]?.msg_reference_finish) {
              msg_item.qa_value.answer[question.msg_id][0].msg_content += reference_markdown_text;
              splitMarkdown(msg_item);
              msg_item.qa_value.answer[question.msg_id][0].msg_reference_finish = true;
            }
          }
        }
      }
    }
  }
}
export async function getTargetAgentReference(msgId: number) {
  // 为完成的消息获取参考文献
  const params = {
    msg_id_list: [msgId]
  };
  const res = await search_reference(params);
  if (!res.error_status) {
    if (!CurrentAgentReference.value?.[msgId]) {
      CurrentAgentReference.value[msgId] = res.result[msgId];
    }
    if (!res.result[msgId]?.length) {
      return;
    }
    let reference_markdown_text = '';
    for (let i = 0; i < res.result[msgId].length; i++) {
      const base_url = window.location.origin;
      if (res.result[msgId][i].source_type == 'resource') {
        reference_markdown_text += `\n\n [${i + 1}]: ${base_url}/#/next_console/resources/resource_viewer/${res.result[msgId][i].resource_id} `;
      } else if (res.result[msgId][i].source_type == 'webpage') {
        reference_markdown_text += `\n\n [${i + 1}]: ${res.result[msgId][i].resource_id} `;
      }
    }
    // 等待问题加载完成
    await checkQuestionStatus(msgId, 100);
    for (const msg_item of AgentAppMsgFlow.value) {
      for (const question of msg_item.qa_value.question) {
        if (question.msg_id == msgId) {
          if (!msg_item.qa_value.answer[question.msg_id][0]?.msg_reference_finish) {
            msg_item.qa_value.answer[question.msg_id][0].msg_content += reference_markdown_text;
            splitMarkdown(msg_item);
            msg_item.qa_value.answer[question.msg_id][0].msg_reference_finish = true;
          }
        }
      }
    }
  }
}
export async function checkQuestionStatus(msg_id: number, delay: number) {
  // 周期性检查图片附件上传情况
  return new Promise(resolve => {
    const intervalId = setInterval(() => {
      // 这里添加你的检查逻辑
      let check_condition = true;

      for (const i of running_questions.value) {
        if (AgentAppMsgFlow.value[i.qa_item_idx].qa_value.question[0]?.msg_id == msg_id) {
          if (!AgentAppMsgFlow.value[i.qa_item_idx]?.qa_finished) {
            check_condition = false;
          }
        }
      }
      if (check_condition) {
        clearInterval(intervalId);
        resolve(true);
      }
    }, delay);
  });
}
export function scrollToBottom() {
  // 正在滚动中
  if (FlowIsScrolling.value) {
    return;
  }
  if (!agentFlowBoxRef.value) {
    console.log('AgentFlowScrollbarRef 不存在');
    return;
  }
  const scrollMax = agentFlowBoxRef.value.clientHeight;

  clearTimeout(AgentScrollButtonTimeout.value);
  FlowIsScrolling.value = true;
  AgentFlowScrollbarRef.value.scrollTo({ top: scrollMax, behavior: 'smooth' });
  AgentScrollButtonTimeout.value = setTimeout(() => {
    FlowIsScrolling.value = false;
  }, 500);
}
export function scrollToTop() {
  // 正在滚动中
  if (FlowIsScrolling.value) {
    return;
  }
  clearTimeout(AgentScrollButtonTimeout.value);
  if (!Math.ceil(AgentFlowScrollbarRef.value.wrapRef.scrollTop)) {
    ElMessage({
      message: '已经到顶啦！',
      type: 'success',
      duration: 2000
    });
    return;
  }

  FlowIsScrolling.value = true;

  AgentFlowScrollbarRef.value.scrollTo({ top: 0, behavior: 'smooth' });

  AgentScrollButtonTimeout.value = setTimeout(() => {
    FlowIsScrolling.value = false;
  }, 500);
}
export function scrollToQA(step: number) {
  // 正在滚动中
  if (FlowIsScrolling.value) {
    return;
  }
  if (!agentFlowBoxRef.value) {
    return;
  }
  clearTimeout(AgentScrollButtonTimeout.value);
  AgentScrollButtonTimeout.value = setTimeout(() => {
    // 为了保证精度，全部转为int
    FlowIsScrolling.value = true;
    // 第i个回答的下沿

    // 获取当前页面上方隐藏高度
    const currentHeight = Math.ceil(AgentFlowScrollbarRef.value.wrapRef.scrollTop);
    // 获取视窗高度
    const viewHeight = Math.ceil(AgentFlowScrollbarRef.value.wrapRef.clientHeight);
    const viewBottom = currentHeight + viewHeight;
    let targetHeight = 0;
    if (step > 0) {
      // 向下滚动到下step个问题,
      for (let i = 0; i < agentFlowBoxRef.value.children.length; i++) {
        targetHeight += Math.floor(agentFlowBoxRef.value.children[i].clientHeight);
        if (targetHeight > currentHeight) {
          break;
        }
      }
    } else {
      // 向上滚动到上step个问题
      let index = 0;
      for (let i = 0; i < agentFlowBoxRef.value.children.length; i++) {
        targetHeight += Math.floor(agentFlowBoxRef.value.children[i].clientHeight);
        if (targetHeight > currentHeight) {
          index = i;
          break;
        }
      }
      // index 为下一个问题，targetHeight 为下一个问题的上沿
      // 减去两个问题即可
      targetHeight -= agentFlowBoxRef.value.children[index]?.clientHeight;
      if (targetHeight >= currentHeight) {
        targetHeight -= agentFlowBoxRef.value.children[index - 1]?.clientHeight;
      }
    }
    AgentFlowScrollbarRef.value.scrollTo({ top: targetHeight, behavior: 'smooth' });
    if (!targetHeight) {
      ElMessage({
        message: '已经到顶啦！',
        type: 'success',
        duration: 2000
      });
    }

    setTimeout(() => {
      FlowIsScrolling.value = false;
    }, 500);
  }, 200);
}
export function handleScroll() {
  if (scrollTimer.value) {
    clearTimeout(scrollTimer.value);
  }
  scrollToFlag.value = true;
  scrollTimer.value = setTimeout(() => {
    scrollToFlag.value = false;
  }, 6000);
}
export async function clickRecommendQuestion(recommend_question: recommend_question_item) {
  // 点击推荐问题,直接提问并更新点击
  consoleInput.value = recommend_question.recommend_question;
  if (recommend_question.id) {
    update_recommend_question({ recommend_question_id: recommend_question.id });
  }
  // 追加提问
  await askAgentQuestion();
}
export function sendMessageToParent(data) {
  window.parent.postMessage(data, '*'); // '*' 表示不限制目标域名
}
export function splitMarkdown(item: msg_queue_item) {
  // 找到最小粒度的tokens，分别转换为html，然后与存量html比对，不同则替换
  let msg_parent_id = item.qa_value.question?.[0]?.msg_id;
  if (!msg_parent_id) {
    // @ts-ignore
    msg_parent_id = 'null';
  }
  const msg_content = item.qa_value.answer[msg_parent_id]?.[0]?.msg_content;
  if (!msg_content) {
    return;
  }
  const tokens = md_answer.parse(msg_content, {});
  const finish_queue = [];
  let queue = [];
  // 遍历tokens 将完成的token匹配好存入finish_queue
  tokens.forEach((token, index) => {
    queue.push(token);
    if (token.type.includes('_close')) {
      const open_token_name = token.type.replace('_close', '_open');
      if (queue[0].type === open_token_name) {
        let finish_flag = true;
        queue.forEach((token, index) => {
          if (index > 0 && token.type == open_token_name) {
            finish_flag = false;
          }
        });
        if (finish_flag) {
          finish_queue.push(queue);
          queue = [];
        }
      }
    } else if (!token.type.includes('_open')) {
      if (queue.length == 1) {
        finish_queue.push(queue);
        queue = [];
      }
    }
  });
  if (!item.qa_value.answer[msg_parent_id][0].msg_content_finish_html) {
    item.qa_value.answer[msg_parent_id][0].msg_content_finish_html = [];
  }
  finish_queue.forEach((sub_queue, index) => {
    const html = md_answer.renderer.render(sub_queue, md_answer.options, {
      is_last: index == finish_queue.length - 1 && running_questions.value.length > 0
    });
    // 两者比对，不同则替换
    if (item.qa_value.answer[msg_parent_id][0].msg_content_finish_html[index] !== html) {
      item.qa_value.answer[msg_parent_id][0].msg_content_finish_html[index] = html;
    }
  });
  // 如果完成的html比存量html多，截取，可能原因是搜索时，搜索到的内容比原有的内容多
  if (finish_queue.length < item.qa_value.answer[msg_parent_id][0].msg_content_finish_html.length) {
    item.qa_value.answer[msg_parent_id][0].msg_content_finish_html = item.qa_value.answer[
      msg_parent_id
    ][0].msg_content_finish_html.slice(0, finish_queue.length);
  }
  //如果还剩下没有匹配上的，直接推入
  if (queue.length) {
    const html = md_answer.renderer.render(queue, md_answer.options, {});
    item.qa_value.answer[msg_parent_id][0].msg_content_finish_html.push(html);
  }
  render_mermaid();
}

export const md_answer = new MarkdownIt({
  html: true,
  linkify: true,
  typographer: true,
  breaks: true,
  highlight: function (str, lang) {
    const language = lang ? lang : 'plaintext';
    const language_text = '<span style="">' + language + '</span>';
    const copy_button =
      '<img src="images/copy.svg" alt="复制" class="answer-code-copy" style="width: 20px;height: 20px;cursor: pointer"/>';
    const header =
      '<div style="display: flex;justify-content: space-between;border-bottom: 1px solid #D0D5DD;padding: 8px">' +
      language_text +
      copy_button +
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
// 添加数学公式支持
md_answer.use(markdownItKatex, {
  throwOnError: false,
  errorColor: ' #cc0000',
  strict: false // 允许非标准语法
});
// 添加mermaid支持
// 使用 mermaid 插件
md_answer.use(markdownItMermaid);
// 自定义表格渲染
const defaultTableRule =
  md_answer.renderer.rules.table_open ||
  function (tokens, idx, options, env, self) {
    return self.renderToken(tokens, idx, options);
  };
md_answer.renderer.rules.table_open = function (tokens, idx, options, env, self) {
  tokens[idx].attrPush(['class', 'custom-table']);
  return defaultTableRule(tokens, idx, options, env, self);
};
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

// 自定义图片样式
md_answer.renderer.rules.image = function (tokens, idx, options, env, self) {
  const token = tokens[idx];
  const src = token.attrGet('src');
  const alt = token.content;
  const title = token.attrGet('title');
  const is_last = env.is_last;
  const imgHtml = `<img src="${src}" alt="${alt}" title="${title}" style="max-width: 100%">`;

  if (is_last) {
    return ` <div style="text-align: center;">${src}</div> `;
  }

  return ` <div style="text-align: center;">${imgHtml}</div> `;
};

// 自定义链接样式
md_answer.renderer.rules.link_open = function (tokens, idx, options, env, self) {
  const aIndex = tokens[idx].attrIndex('target');

  if (aIndex < 0) {
    tokens[idx].attrPush(['target', '_blank']); // 添加 target="_blank"
  } else {
    tokens[idx].attrs[aIndex][1] = '_blank'; // 替换现有的 target 属性
  }

  return self.renderToken(tokens, idx, options);
};
// 自定义引用样式
md_answer.renderer.rules.blockquote_open = function (tokens, idx, options, env, self) {
  tokens[idx].attrSet('class', 'my-custom-quote');
  return self.renderToken(tokens, idx, options);
};
mermaid.initialize({
  startOnLoad: false,
  securityLevel: 'loose',
  gantt: {
    axisFormat: '%Y-%m-%d'
  }
});
export async function render_mermaid() {
  await nextTick();
  const nodes = document.querySelectorAll('.mermaid');

  // 提前验证至挑选合法的语法进行渲染
  const nodes_valid = [];
  for (const node of nodes) {
    const mermaid_text = node.textContent;

    if (mermaid_text) {
      // gantt 最后渲染
      try {
        await mermaid.parse(mermaid_text);
        nodes_valid.push(node);
      } catch (e) {}
    }
  }

  await mermaid.run({
    // @ts-ignore
    nodes: Array.from(nodes_valid),
    suppressErrors: true
  });
}
export function getMsgItemAnswerCreateTime(item: msg_queue_item) {
  try {
    const msgParentId = item?.qa_value?.question?.[0].msg_id;
    return item?.qa_value?.answer?.[msgParentId]?.[0].create_time;
  } catch (e) {
    return '';
  }
}
