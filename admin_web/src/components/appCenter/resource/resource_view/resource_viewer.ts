import { reactive, ref } from 'vue';
import { ResourceItem } from '@/types/resource_type';
import { get_resource_object_path, resource_view_meta_get } from '@/api/resource_api';
import { add_copy_button_event, md_answer } from '@/components/next_console/messages_flow/message_flow';
import { getToken } from '@/utils/auth';
import { user_info } from '@/components/user_center/user';
import WebOfficeSDK from '@/components/global/wps/web-office-sdk-solution-v2.0.7.es.js';
import { clientFingerprint, getFingerPrint } from '@/components/global/web_socket/web_socket';
export const current_path_tree = ref<ResourceItem[]>([]);
export const resource_viewer_loading = ref(false);
export const current_view_resource = reactive<ResourceItem>(
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
    rerank_score: null
  }
);
export const WPS_Instance = ref(null);
export async function get_parent_resource_list() {
  if (!current_view_resource.id) {
    current_path_tree.value = [];
    return;
  }
  if (current_view_resource.user_id === user_info.value.user_id) {
    current_path_tree.value.push(
      // @ts-ignore
      {
        id: null,
        resource_name: '我的资源',
        resource_type: 'folder',
        resource_status: '正常',
        resource_type_cn: '文件夹'
      }
    );
  } else {
    current_path_tree.value.push(
      // @ts-ignore
      {
        id: null,
        resource_name: '共享资源',
        resource_type: 'folder',
        resource_status: '正常',
        resource_type_cn: '文件夹'
      }
    );
  }

  let params = {
    resource_id: current_view_resource.id
  };
  let res = await get_resource_object_path(params);
  if (!res.error_status) {
    current_path_tree.value = res.result.data;
  }
}
export async function get_current_resource_object(resource_id: number) {
  if (!clientFingerprint.value) {
    await getFingerPrint();
  }
  let params = {
    resource_id: resource_id,
    clientFingerprint: clientFingerprint.value
  };
  resource_viewer_loading.value = true;
  let res = await resource_view_meta_get(params);
  if (!res.error_status) {
    Object.assign(current_view_resource, res.result);
  }
  resource_viewer_loading.value = false;
}

export function view_code_resource_to_md() {
  let code = current_view_resource.resource_content;
  if (!code) {
    return '';
  }
  // 新增md代码块
  if (current_view_resource.resource_format === 'md') {
    return md_answer.render(code);
  }
  code = '```' + current_view_resource.resource_format + '\n' + code + '\n```';
  // 渲染
  return md_answer.render(code);
}
function get_wps_type() {
  if (!current_view_resource.resource_format) {
    return '';
  }
  if (
    [
      'doc',
      'dot',
      'wps',
      'wpt',
      'docx',
      'dotx',
      'docm',
      'dotm',
      'rtf',
      'txt',
      'xml',
      'mhtml',
      'mht',
      'html',
      'htm',
      'uof',
      'uot3'
    ].includes(current_view_resource.resource_format)
  ) {
    return WebOfficeSDK.OfficeType.Writer;
  }
  if (
    ['xls', 'xlt', 'et', 'ett', 'xlsx', 'xltx', 'xlsm', 'xltm', 'csv'].includes(current_view_resource.resource_format)
  ) {
    return WebOfficeSDK.OfficeType.Spreadsheet;
  }
  if (
    ['ppt', 'pptx', 'pptm', 'ppsx', 'ppsm', 'pps', 'potx', 'potm', 'dpt', 'dps', 'pot'].includes(
      current_view_resource.resource_format
    )
  ) {
    return WebOfficeSDK.OfficeType.Presentation;
  }
  if (['pdf', 'ofd'].includes(current_view_resource.resource_format)) {
    return WebOfficeSDK.OfficeType.Pdf;
  }
  if (current_view_resource.resource_format == 'otl') {
    return WebOfficeSDK.OfficeType.Otl;
  }
  if (current_view_resource.resource_format == 'dbt') {
    return WebOfficeSDK.OfficeType.Dbt;
  }
  return WebOfficeSDK.OfficeType.Writer;
}

export async function init_wps_doc(resource_id: number) {
  if (!resource_id) {
    return;
  }
  current_view_resource.resource_content = '';
  await get_current_resource_object(resource_id);
  get_parent_resource_list();
  if (
    current_view_resource.resource_type == 'document' &&
    current_view_resource.resource_view_support &&
    !current_view_resource.resource_content
  ) {
    // 启用wps 进行渲染
    let token = getToken();
    let mount_div = document.querySelector('#WPS_APP');
    if (!mount_div) {
      return;
    }
    // 判断是否已经初始化过
    if (mount_div.children.length > 0) {
      return;
    }
    // @ts-ignore
    const instance = WebOfficeSDK.init({
      officeType: get_wps_type(),
      appId: import.meta.env.VITE_APP_WPS_APP_ID,
      fileId: resource_id,
      mount: document.querySelector('#WPS_APP'),
      token: token
    });
    await instance.ready();
  } else {
    add_copy_button_event();
  }
}
