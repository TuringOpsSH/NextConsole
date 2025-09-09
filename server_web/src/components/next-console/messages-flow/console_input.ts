import {ref} from 'vue';
import {ElNotification} from 'element-plus';
import {create_new_session, current_session} from '@/components/next-console/messages-flow/sessions';
import {add_messages, search_messages} from '@/api/next-console';
import {add_new_qa, current_qa_id, qa_list} from '@/components/next-console/messages-flow/qas';
import {msg_item, msg_queue_item, running_question_meta} from '@/types/next-console';
import {
  add_copy_button_event,
  get_target_reference,
  msg_flow,
  qa_workflow_map,
  scroll_to_bottom,
  splitMarkdown,
  userStopScroll
} from '@/components/next-console/messages-flow/message_flow';
import router from '@/router';

export const user_input = ref('');
export const user_batch_size = ref(0);
export const running_questions = ref<running_question_meta[]>([]);
export const consoleInputRef = ref();
export const console_inner_type = ref('ai_search');
export const console_input_Ref = ref();
export const console_input_height = ref(130);
export const show_console_inner_head = ref(false);
export async function ask_question() {
  // 判断是否为空
  if (!user_input.value || user_input.value.trim() === '') {
    ElNotification.warning({
      title: '系统消息',
      message: '请输入有效问题！',
      duration: 2000
    });
    return false;
  }
  // 判断是否达到并发限制
  if (user_batch_size.value >= 3) {
    ElNotification.warning({
      title: '系统消息',
      message: '请等待当前问题处理完毕！',
      duration: 2000
    });
    return false;
  }
  // 判断会话情况
  if (!current_session.id) {
    await create_new_session();
    if (router.currentRoute.value.name === 'next_console_welcome_home') {
      // console.log('跳转')
      router.push({
        name: 'message_flow',
        params: { session_code: current_session.session_code },
        query: { ...router.currentRoute.value.query, auto_ask: 'true' } // 保持既有参数
      });
      return false;
    }
    // 初始化队列
  }
  // 用户输入预处理：将换行符替换为两个换行符
  let user_msg_content = user_input.value.replace(/\n/g, '\n\n');
  // 生成问答对占位
  let new_qa_item_idx = msg_flow.value.length;
  let new_qa_item = <msg_queue_item>{
    qa_id: null,
    qa_status: null,
    qa_topic: null,
    qa_value: {
      question: [
        <msg_item>{
          msg_content: user_msg_content,
          msg_role: 'user',
          msg_parent_id: 0,
          create_time: getCurrentTimestamp(),
          msg_remark: 0,
          msg_version: 0,
          msg_id: 0,
          msg_del: 0,
          assistant_id: -12345,
          shop_assistant_id: null
        }
      ],
      answer: {}
    },
    qa_share_picked: 0,
    qa_progress_open: false,
    qa_workflow_open: false,
    show_button_question_area: false,
    show_button_answer_area: false,
    short_answer: null,
    qa_finished: false
  };

  msg_flow.value.push(new_qa_item);

  let new_qa = await add_new_qa();
  if (!new_qa?.qa_id) {
    return;
  }

  msg_flow.value[new_qa_item_idx].qa_id = new_qa.qa_id;
  msg_flow.value[new_qa_item_idx].qa_status = new_qa.qa_status;
  msg_flow.value[new_qa_item_idx].qa_topic = new_qa.qa_topic;
  scroll_to_bottom();
  // 如果启动了rag，则打开工作流占位符
  if (
    current_session.session_search_engine_switch ||
    current_session.session_attachment_image_switch ||
    current_session.session_local_resource_switch ||
    current_session.session_attachment_file_switch
  ) {
    qa_workflow_map.value[new_qa.qa_id] = [
      {
        qa_id: new_qa_item_idx,
        msg_id: null,
        task_id: null,
        task_type: null,
        task_instruction: null,
        task_params: null,
        task_result: null,
        task_create_time: null,
        task_begin_time: null,
        task_update_time: null,
        task_end_time: null,
        task_status: null
      }
    ];
  }

  // 保存问题
  let question_params = {
    session_id: current_session.id,
    qa_id: new_qa.qa_id,
    msg_content: user_msg_content,
    stream: false,
    session_source: 'next_search',
    msg_answer_flag: false
  };
  let data = await add_messages(question_params, null);
  if (data.error_status) {
    return;
  }
  let msg_parent_id = data.result.msg_id;
  let msg_abort_controller = new AbortController();
  // 更新数据
  msg_flow.value[new_qa_item_idx].qa_value.question[0].msg_id = msg_parent_id;
  msg_flow.value[new_qa_item_idx].qa_value.answer[msg_parent_id] = [
    <msg_item>{
      msg_content: '',
      msg_role: 'assistant',
      msg_parent_id: 0,
      create_time: getCurrentTimestamp(),
      msg_remark: 0,
      msg_version: 0,
      msg_id: 0,
      msg_del: 0,
      assistant_id: -12345,
      shop_assistant_id: null
    }
  ];

  let target_question = {
    qa_item_idx: new_qa_item_idx,
    begin_time: performance.now(),
    abort_controller: msg_abort_controller,
    end_time: null,
    status: 'running'
  };
  running_questions.value.push(target_question);

  // 开始启动
  current_qa_id.value = qa_list.value[0].qa_id;
  user_input.value = null;
  scroll_to_bottom();
  let params = {
    session_id: current_session.id,
    qa_id: qa_list.value[0].qa_id,
    msg_content: user_msg_content,
    stream: true,
    session_source: 'next_search',
    msg_parent_id: msg_parent_id
    // 是否开启query-agent
    // query_agent_open_flag: true
  };
  const startTime = performance.now();
  user_batch_size.value += 1;
  try {
    let data = await add_messages(params, msg_abort_controller.signal);
    // 处理流式响应来更新消息
    const reader = data.body.getReader();
    let chunk = await reader.read();
    while (!chunk.done) {
      // 当第一个字符出现时，获取参考文献，关闭工作流展示区
      if (!msg_flow.value[new_qa_item_idx].qa_value.answer[msg_parent_id][0].msg_content) {
        get_target_reference(msg_parent_id);
        msg_flow.value[new_qa_item_idx].qa_workflow_open = false;
      }
      msg_flow.value[new_qa_item_idx].qa_value.answer[msg_parent_id][0].msg_content += new TextDecoder('utf-8').decode(
        chunk.value
      );

      chunk = await reader.read();
      splitMarkdown(msg_flow.value[new_qa_item_idx]);
      scroll_to_bottom();
    }
  } catch (e) {
    if (e.name == 'AbortError') {
    }
  }
  user_batch_size.value -= 1;
  // 完成后更新回答结果的id
  let data2 = await search_messages({
    qa_id: [qa_list.value[0].qa_id]
  });
  if (!data2.error_status) {
    try {
      msg_flow.value[new_qa_item_idx].qa_value.answer[msg_parent_id][0].msg_id =
        data2.result[0]?.qa_value.answer[msg_parent_id][0].msg_id;
    } catch (e) {
      // console.log(e)
    }
  }
  add_copy_button_event();
  // 更新问题状态
  let idx = running_questions.value.indexOf(target_question);
  running_questions.value.splice(idx, 1);
  msg_flow.value[new_qa_item_idx].qa_finished = true;
  userStopScroll.value = false;
}

export function get_running_progress(target_question: running_question_meta) {
  try {
    let msg_parent_id = msg_flow.value[target_question.qa_item_idx].qa_value.question[0].msg_id;
    return msg_flow.value[target_question.qa_item_idx].qa_value.answer[msg_parent_id][0].msg_content?.length;
  } catch (e) {
    console.error(e);
    return 0;
  }
}

function getCurrentTimestamp() {
  const date = new Date();

  const year = date.getFullYear();

  const month = (date.getMonth() + 1).toString().padStart(2, '0');

  const day = date.getDate().toString().padStart(2, '0');

  const hour = date.getHours().toString().padStart(2, '0');

  const minute = date.getMinutes().toString().padStart(2, '0');

  const second = date.getSeconds().toString().padStart(2, '0');

  return year + '-' + month + '-' + day + ' ' + hour + ':' + minute + ':' + second;
}
