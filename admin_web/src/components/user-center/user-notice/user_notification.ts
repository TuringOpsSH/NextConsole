import { ElMessage } from 'element-plus';
import { ref } from 'vue';
import { delete_task, list_task, search_task } from '@/api/user-notice';
import { user_notice_task_info } from '@/types/user-center';

export const notification_data = ref<user_notice_task_info[]>([]);
export const current_page_num = ref(1);
export const current_page_size = ref(10);
export const current_total = ref(0);
export const search_keyword = ref('');
export const pick_status = ref([]);
export const pick_type = ref([]);

export async function get_notification_data() {
  // 获取通知列表
  // @ts-ignore
  const res = await list_task({
    page_num: current_page_num.value,
    page_size: current_page_size.value
  });
  if (!res.error_status) {
    notification_data.value = res.result.data;
    current_total.value = res.result.total;
  }
}

export async function handle_size_change(val: number) {
  current_page_size.value = val;
  await get_notification_data();
}
export async function handle_num_change(val: number) {
  current_page_num.value = val;
  await get_notification_data();
}

export async function search_notification() {
  const params = {
    keyword: search_keyword.value,
    fetch_all: true,
    task_status: pick_status.value,
    notice_type: pick_type.value
  };
  const res = await search_task(params);
  if (!res.error_status) {
    notification_data.value = res.result.data;
    current_total.value = res.result.total;
  }
}
export async function handle_search_by_keyword() {
  if (!search_keyword.value) {
    return;
  }
  await search_notification();
}

export async function delete_notification(item: user_notice_task_info) {
  if (item.task_status == '执行中') {
    ElMessage.warning({
      message: '运行中的任务不能删除！请先暂停或者终止',
      duration: 5000
    });
    return;
  }
  const res = await delete_task({
    task_id: item.id
  });
  if (!res.error_status) {
    ElMessage.success({
      message: '删除成功',
      duration: 3000
    });
    await get_notification_data();
  }
}
