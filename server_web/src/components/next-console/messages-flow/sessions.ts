import { ElMessage } from 'element-plus';
import { reactive, ref } from 'vue';
import { create_session, search_session } from '@/api/next-console';
import router from '@/router';
import { session_item } from '@/types/next-console';
import { emitter, eventKeys } from '@/utils/eventBus';

export const session_history_top5 = ref<session_item[]>([]);
export const current_session = reactive<session_item>({
  session_shop_assistant_avatar: null,
  session_shop_assistant_desc: null,
  session_shop_assistant_id: null,
  session_shop_assistant_name: null,
  id: null,
  session_code: '',
  user_id: null,
  session_topic: null,
  session_status: null,
  session_remark: null,
  session_vis: null,
  session_favorite: null,
  session_like_cnt: null,
  session_dislike_cnt: null,
  session_share_cnt: null,
  session_update_cnt: null,
  session_assistant_id: null,
  session_assistant_name: null,
  session_assistant_desc: null,
  session_assistant_avatar: null,
  session_task_id: null,
  session_task_type: null,
  session_source: null,
  session_llm_code: null,
  create_time: null,
  update_time: null,
  is_edit: false,
  history_is_edit: false,
  session_summary: null,
  session_search_engine_language_type: null,
  session_search_engine_resource_type: 'search',
  session_search_engine_switch: null,
  session_local_resource_switch: false,
  session_local_resource_use_all: false,
  session_attachment_image_switch: false,
  session_attachment_file_switch: false,
  session_attachment_webpage_switch: false
});
export const current_session_task_id = ref(null);
export const current_session_task_type = ref('general_search');
export const current_session_code = ref();
export async function addNewSession() {
  // 清空当前会话
  if (router.currentRoute.value.name == 'next_console_welcome_home') {
    ElMessage.success('已经为最新会话啦');
    return;
  }
  await router.push({ name: 'next_console_welcome_home' });
}
export async function create_new_session() {
  // 创建新的搜索会话
  const params = {
    session_assistant_id: -12345,
    session_status: '进行中',
    session_task_id: current_session_task_id.value,
    session_source: 'next_search',
    session_task_type: current_session_task_type.value,
    session_search_engine_switch: current_session.session_search_engine_switch,
    session_search_engine_language_type: current_session.session_search_engine_language_type,
    session_search_engine_resource_type: current_session.session_search_engine_resource_type,
    session_llm_code: current_session.session_llm_code,
    session_attachment_image_switch: current_session.session_attachment_image_switch,
    session_attachment_file_switch: current_session.session_attachment_file_switch,
    session_attachment_webpage_switch: current_session.session_attachment_webpage_switch,
    session_local_resource_switch: current_session.session_local_resource_switch,
    session_local_resource_use_all: current_session.session_local_resource_use_all
  };
  const res = await create_session(params);
  if (!res.error_status) {
    Object.assign(current_session, res.result);
    session_history_top5.value.unshift(res.result);
    current_session_code.value = current_session.session_code;
  }
}
export async function getLastedSession() {
  // 获取最新session，并填充至session-list
  const params = {
    page_num: 1,
    page_size: 30
  };
  const data = await search_session(params);
  session_history_top5.value = data.result;
}
export async function changeCurrentSession(targetSession: session_item, event: any) {
  if (targetSession.is_edit) {
    return;
  }
  // 拦截点击更多按钮
  if (
    event.target.className.includes('session-more-button') ||
    event.target.className.includes('el-image__inner') ||
    event.target.className.includes('el-image')
  ) {
    return;
  }
  emitter.emit(eventKeys.SIDEBAR.CHANGE_SESSION, {
    sessionId: targetSession.id,
    sessionCode: targetSession.session_code,
    taskId: targetSession.session_task_id
  });
  // console.log('跳转')
  // router.push({
  //   name: 'message_flow',
  //   params: { session_code: targetSession.session_code },
  //   query: {
  //     task_id: targetSession.session_task_id
  //   }
  // });
}
