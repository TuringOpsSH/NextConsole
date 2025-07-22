import Clipboard from 'clipboard';
import {ElMessage} from 'element-plus';
import {ref} from 'vue';
import {admin_add_tag, get_session_history_msg, searchSessionLog} from '@/api/feedback_center';
import {msg_queue_item, session_item} from '@/types/next_console';

export const CurrentSessionTotal = ref(0);
export const CurrentSessionPageSize = ref(100);
export const CurrentSessionPageNum = ref(1);
export const CurrentSessionLogList = ref<session_item[]>([]);
export const CurrentSessionAssistantList = ref<string[]>([]);
export const targetAssistantName = ref('');
export const targetSessionRemark = ref(null);
export const targetSessionFavorite = ref(null);
export const targetSessionTimeRange = ref('');
export const targetSessionUser = ref('');
export const SessionTimeRangeShortCuts = [
  {
    text: '上周',
    value: () => {
      const end = new Date();
      const start = new Date();
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 7);
      return [start, end];
    }
  },
  {
    text: '上个月',
    value: () => {
      const end = new Date();
      const start = new Date();
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 30);
      return [start, end];
    }
  },
  {
    text: '上季度',
    value: () => {
      const end = new Date();
      const start = new Date();
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 90);
      return [start, end];
    }
  }
];
export const loadingSessionHistoryMsg = ref(false);
export const targetSessionTopic = ref('');
export const targetSessionTag = ref('');
export const showSessionHistoryMsg = ref(false);
export const targetSession = ref<session_item>();
export const SessionHistoryMsgList = ref<msg_queue_item[]>([]);
export const CurrentSessionSource = ref('next_console');
export const inputSessionTagVisible = ref(false);

export const inputSessionTagValue = ref('');

export const InputSessionTagRef = ref(null);

export async function getSessionLog() {
  const params = {
    page_num: CurrentSessionPageNum.value,
    page_size: CurrentSessionPageSize.value,
    session_source: CurrentSessionSource.value
  };

  if (targetAssistantName.value !== '') {
    params['assistant_name'] = targetAssistantName.value;
  }
  if (targetSessionRemark.value !== null && targetSessionRemark.value !== '') {
    params['session_remark'] = targetSessionRemark.value;
  }
  if (targetSessionFavorite.value !== null && targetSessionFavorite.value !== '') {
    params['session_favorite'] = targetSessionFavorite.value;
  }
  if (targetSessionTimeRange.value !== '') {
    params['create_start_date'] = formatDateToUTC8(targetSessionTimeRange.value[0]);
    params['create_end_date'] = formatDateToUTC8(targetSessionTimeRange.value[1]);
  }
  if (targetSessionTopic.value !== '') {
    params['session_topic'] = targetSessionTopic.value;
  }
  if (targetSessionTag.value !== '') {
    params['tag'] = targetSessionTag.value;
  }
  if (targetSessionUser.value !== '') {
    params['session_user_id'] = targetSessionUser.value;
  }
  const res = await searchSessionLog(params);
  if (!res.error_status) {
    CurrentSessionLogList.value = res.result.data;
    CurrentSessionTotal.value = res.result.total;
    CurrentSessionAssistantList.value = res.result.assistant_name;
  }
}

export function formatDateToUTC8(date) {
  return new Intl.DateTimeFormat('zh-CN', {
    timeZone: 'Asia/Shanghai',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false
  })
    .format(date)
    .replace(/\//g, '-')
    .replace(/,/g, '');
}


export function handle_tag_close(tag: string) {
  // @ts-ignore
  const index = targetSession.value.tag_list.indexOf(tag);
  targetSession.value.tag_list.splice(index, 1);
}
export function handleSessionTagInputConfirm() {
  if (inputSessionTagValue.value) {
    if (inputSessionTagValue.value.length > 100) {
      ElMessage.warning({
        message: '标签过长！请不要超过100个字符',
        type: 'warning',
        duration: 600
      });
      return;
    }
    if (!targetSession.value?.tag_list){
        targetSession.value.tag_list = []
    }
    targetSession.value.tag_list.push(inputSessionTagValue.value);
  }
  inputSessionTagVisible.value = false;
  inputSessionTagValue.value = '';
}
export async function addSessionTag() {
  const params = {
    session_id: targetSession.value.id,
    tag: targetSession.value.tag_list.join(',')
  };
  const res = await admin_add_tag(params);
  if (!res.error_status) {
    targetSession.value.tag_name = targetSession.value.tag_list.join(',');
    await getSessionLog();
  }
}
// 按钮组交互函数
export function version_turn_left(qa: msg_queue_item, model: number) {
  // 将队列最后一个元素移到队列最前面

  const question_id = qa.qa_value.question[0].msg_id;
  if (model == 1) {
    const last_item = qa.qa_value.question.pop();
    qa.qa_value.question.unshift(last_item);
  }
  if (model == 2) {
    const last_item = qa.qa_value.answer[question_id].pop();
    qa.qa_value.answer[question_id].unshift(last_item);
  }
}
export function version_turn_right(qa: msg_queue_item, model: number) {
  // 将队列第一个元素移到队列最后面
  const question_id = qa.qa_value.question[0].msg_id;

  if (model == 1) {
    const first_item = qa.qa_value.question.shift();
    qa.qa_value.question.push(first_item);
  }
  if (model == 2) {
    const first_item = qa.qa_value.answer[question_id].shift();
    qa.qa_value.answer[question_id].push(first_item);
  }
}

export function copy_text(dataToCopy: string) {
  Clipboard.copy(dataToCopy.trim());
  ElMessage({
    message: '复制成功',
    type: 'success',
    duration: 1000
  });
}
