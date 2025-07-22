import { ref } from 'vue';
import { ResourceItem, ResourceUploadItem } from '@/types/resource_type';
import { ElNotification, UploadRawFile, UploadRequestOptions, UploadUserFile } from 'element-plus';
import { add_upload_task, update_upload_task, upload_resource_object } from '@/api/resource_api';
import { current_resource, search_all_resource_object } from '@/components/resource/resource_list/resource_list';
import { init_my_resource_tree, refresh_panel_count, show_upload_button, switch_panel } from '@/components/resource/resource_panel/panel';
import { show_upload_dialog_multiple } from '@/components/resource/resource_tree/resource_tree';
import sha256 from 'crypto-js/sha256';
import { enc } from 'crypto-js';
export const show_upload_manage_box = ref(false);
export const upload_file_task_list = ref<ResourceUploadItem[]>([]);
export const show_upload_file_detail = ref(true);
export const upload_manager_status = ref('pending');
export const upload_size = ref(1);
export const finish_time_size_map = ref({});
export const upload_parent_resource = ref<ResourceItem>(null);
export const upload_button_Ref = ref(null);
export const folder_upload_parent_resource = ref(null);

// 原始上传文件列表
export const upload_file_list = ref<UploadUserFile[]>([]);
export const show_close_confirm_flag = ref(false);
export async function retry_all_upload_file() {
  // 重试所有上传任务
  show_upload_manage_box.value = true;
  for (let item of upload_file_list.value) {
    item.status = 'ready';
    await upload_file_content(<UploadRequestOptions>{
      file: item.raw,
      data: {},
      headers: {}
    });
  }
}
// 上传管理器控制
export function close_upload_manager(notice: boolean = true) {
  // 关闭上传管理器
  // 检查任务状态，如果有任务正在上传，提示用户是否关闭
  if (notice) {
    for (let i = 0; i < upload_file_task_list.value.length; i++) {
      if (
          upload_file_task_list.value[i].task_status !== 'success' &&
          upload_file_task_list.value[i].task_error_msg !== '空'
      ) {
        show_close_confirm_flag.value = true;
        return false;
      }
    }
  }

  show_upload_manage_box.value = false;
  clean_upload_manager();
}
export function clean_upload_manager() {
  upload_file_list.value = [];
  // 更新后端上传任务状态
  for (let i = 0; i < upload_file_task_list.value.length; i++) {
    if (
        upload_file_task_list.value[i].task_status !== 'success' &&
        upload_file_task_list.value[i].task_status !== 'error' &&
        upload_file_task_list.value[i].task_status !== 'abort' &&
        upload_file_task_list.value[i].id
    ) {
      let params = {
        task_id: upload_file_task_list.value[i].id,
        task_status: 'abort'
      };
      update_upload_task(params);
    }
  }

  upload_file_task_list.value = [];
  upload_manager_status.value = 'pending';
  show_upload_manage_box.value = false;
  show_close_confirm_flag.value = false;
}

// 核心上传逻辑
// 核心上传逻辑
export async function calculateMD5(file: UploadRawFile): Promise<string> {
  // 计算文件的MD5值
  try {
    const arrayBuffer = await file.arrayBuffer();
    const hashBuffer = await crypto.subtle?.digest('SHA-256', arrayBuffer);
    if (!hashBuffer) {
      return
    }
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
  } catch (e) {
    return
  }

}
export async function calculateSHA256(file: UploadRawFile): Promise<string> {
  // 计算文件的SHA256值
  const arrayBuffer = await file.arrayBuffer();
  const wordArray = enc.Latin1.parse(
      Array.from(new Uint8Array(arrayBuffer))
          .map(byte => String.fromCharCode(byte))
          .join('')
  );
  return sha256(wordArray).toString(enc.Hex);
}
export async function prepare_upload_files(uploadFile: UploadRawFile) {
  // 正对于新上传的文件，需要进行一些准备工作，然后生成一个上传任务
  // 如果没有选择父资源，那么需要打开资源选择器
  show_upload_manage_box.value = true;
  if (show_upload_button.value) {
    show_upload_button.value?.hide();
  }
  if (window.innerWidth < 768) {
    switch_panel('close');
  }
  // 1. 计算文件的MD5值
  let fileSHA256  = ''
  try {
    fileSHA256 = await calculateMD5(uploadFile)
    if (!fileSHA256) {
      fileSHA256 = await calculateSHA256(uploadFile)
    }
  }
  catch (e) {
    fileSHA256 = await calculateSHA256(uploadFile)
  }
  if (!fileSHA256 ) {
    ElNotification.error({
      title: '系统通知',
      message: '文件上传失败，无法计算文件特征值！',
      duration: 5000,
    })
    return false;
  }
  // 2. 准备参数
  let resource_size = uploadFile.size / 1024 / 1024;
  let content_max_idx = Math.floor(resource_size / upload_size.value);
  // 前端临时可视化文件类型和格式
  let resource_type = '';
  let resource_format = '';

  if (uploadFile.name.indexOf('.') > -1) {
    resource_format = uploadFile.name.split('.').pop().toLowerCase();
  }
  resource_type = uploadFile.type;
  let task_icon = get_task_icon(resource_type, resource_format);
  let new_upload_file_task = <ResourceUploadItem>{
    id: null,
    resource_parent_id: current_resource.id,
    resource_id: null,
    resource_name: uploadFile.name,
    resource_size_in_mb: resource_size,
    resource_type: resource_type,
    resource_format: resource_format,
    content_max_idx: content_max_idx,
    content_finish_idx: -1,
    resource_md5: fileSHA256,
    raw_file: uploadFile,
    task_icon: task_icon,
    task_status: 'pending'
  };
  upload_file_task_list.value.push(new_upload_file_task);
  if (!upload_parent_resource.value?.id) {
    // console.log('无选择父资源')
    upload_button_Ref.value?.handleStart(uploadFile);
    upload_file_list.value.push(uploadFile);
    await show_upload_dialog_multiple(retry_all_upload_file);
    return false;
  }
}
export async function upload_file_content(options: UploadRequestOptions) {
  // 分块上传文件内容
  let { file, data, headers } = options;
  let target_upload_task = upload_file_task_list.value.find(item => item.raw_file.uid === file.uid);
  if (!target_upload_task) {
    return false;
  }
  if (!target_upload_task.id) {
    let upload_task_params = {
      resource_parent_id: target_upload_task.resource_parent_id,
      resource_name: target_upload_task.resource_name,
      resource_size: target_upload_task.resource_size_in_mb,
      resource_type: target_upload_task.resource_type,
      resource_format: target_upload_task.resource_format,
      task_source: target_upload_task.task_source,
      content_max_idx: target_upload_task.content_max_idx,
      resource_md5: target_upload_task.resource_md5
    };

    // 3. 生成上传任务
    let res = await add_upload_task(upload_task_params);
    if (!res.error_status && !res.error_message) {
      // 4. 更新上传任务列表
      target_upload_task.id = res.result.id;
      upload_manager_status.value = 'uploading';
      target_upload_task.resource_name = res.result.resource_name;
      target_upload_task.resource_type = res.result.resource_type;
      target_upload_task.resource_format = res.result.resource_format;
      target_upload_task.task_icon = res.result.task_icon;
      target_upload_task.task_status = res.result.task_status;
    } else {
      target_upload_task.task_status = 'error';
      target_upload_task.task_error_msg = '空';
      return false;
    }
  }
  target_upload_task.task_status = 'uploading';
  // 循环上传文件内容
  let content_size = 1024 * 1024 * upload_size.value;
  let content = null;
  let arrayBuffer = null;
  let hashBuffer = null;
  let hashArray = null;
  let chunk_MD5 = '';
  // 从已经上传的位置开始上传，默认为-1
  let res = null;
  try {
    let begin_idx = target_upload_task.content_finish_idx + 1;
    for (let i = begin_idx; i <= target_upload_task.content_max_idx; i++) {
      if (target_upload_task.task_status === 'pause') {
        return false;
      }
      let start_idx = i * content_size;
      let end_idx = (i + 1) * content_size;
      if (end_idx > target_upload_task.raw_file.size) {
        end_idx = target_upload_task.raw_file.size;
      }
      content = target_upload_task.raw_file.slice(start_idx, end_idx);
      try {
        chunk_MD5 = await calculateMD5(content)
        if (!chunk_MD5) {
          chunk_MD5 = await calculateSHA256(content)
        }
      } catch (e) {
        chunk_MD5 = await calculateSHA256(content)
      }
      // // console.log('上传文件chunk_MD5', start_idx, end_idx, i, chunk_MD5  )
      let upload_content_form = new FormData();
      upload_content_form.append('chunk_task_id', target_upload_task.id.toString());
      upload_content_form.append('chunk_index', i.toString());
      upload_content_form.append('chunk_content', content);
      upload_content_form.append('chunk_MD5', chunk_MD5);
      upload_content_form.append('chunk_size', content.size);
      res = await upload_resource_object(upload_content_form);
      if (!res.error_status) {
        init_my_resource_tree();
        // 上传成功，更新位置
        target_upload_task.content_finish_idx = i;
        let finish_time = Date.now();
        if (!finish_time_size_map.value[finish_time]) {
          finish_time_size_map.value[finish_time] = 0;
        }
        finish_time_size_map.value[finish_time] += end_idx - start_idx;
      } else {
        target_upload_task.task_status = 'error';
        return false;
      }
    }
  } catch (e) {
    target_upload_task.task_status = 'error';
    ElNotification.error({
      title: '系统通知',
      message: '上传文件内容失败' + e,
      duration: 5000
    });
    return false;
  }
  // 上传成功，更新状态
  target_upload_task.task_status = 'success';
  // 更新后端上传任务状态
  let params = {
    task_id: target_upload_task.id,
    task_status: 'success'
  };
  update_upload_task(params);
  refresh_panel_count();
  search_all_resource_object();
  let fail_flag = false;
  for (let i = 0; i < upload_file_task_list.value.length; i++) {
    if (upload_file_task_list.value[i].task_status !== 'success') {
      fail_flag = true;
      break;
    }
  }
  if (!fail_flag) {
    upload_manager_status.value = 'success';
  }
  return res;
}

// 获取可视化要素
export function get_task_icon(resource_type: string, resource_format: string) {
  // 获取任务图标
  let icon_base_url = 'images/';
  let icon_url = 'other.svg';
  let icon_format_map = {
    // 文档类型
    doc: 'doc.svg',
    docx: 'doc.svg',
    xls: 'xls.svg',
    xlsx: 'xls.svg',
    csv: 'csv.svg',
    ppt: 'ppt.svg',
    pptx: 'pptx.svg',
    pdf: 'pdf.svg',
    txt: 'txt.svg',
    // 图片类型
    jpeg: 'jpeg.svg',
    jpg: 'jpg.svg',
    png: 'png.svg',
    gif: 'gif.svg',
    bmp: 'bmp.svg',
    webp: 'webp.svg',
    svg: 'svg.svg',
    // 视频类型
    mp4: 'mp4.svg',
    avi: 'avi.svg',
    mkv: 'mkv.svg',
    flv: 'flv.svg',
    mov: 'mov.svg',
    wmv: 'wmv.svg',
    webm: 'webm.svg',
    mpg: 'mpg.svg',
    '3gp': '3gp.svg',
    mpeg: 'mpeg.svg',
    // 音频类型
    mp3: 'mp3.svg',
    wav: 'wav.svg',
    wma: 'wma.svg',
    flac: 'flac.svg',
    aac: 'aac.svg',
    ogg: 'ogg.svg',
    m4a: 'm4a.svg',
    amr: 'amr.svg',
    aiff: 'aiff.svg',
    aif: 'aif.svg',
    ra: 'ra.svg',
    // 代码
    css: 'css.svg',
    js: 'js.svg',
    json: 'json.svg',
    xml: 'xml.svg',
    java: 'java.svg',
    cpp: 'cpp.svg',
    c: 'c.svg',
    py: 'py.svg',
    php: 'php.svg',
    go: 'go.svg',
    h: 'h.svg',
    hpp: 'hpp.svg',
    rb: 'rb.svg',
    cs: 'cs.svg',
    sh: 'sh.svg',
    bat: 'bat.svg',
    swift: 'swift.svg',
    kt: 'kt.svg',
    ts: 'ts.svg',
    pl: 'pl.svg',
    lua: 'lua.svg',
    r: 'r.svg',
    scala: 'scala.svg',
    sql: 'sql.svg',
    vb: 'vb.svg',
    vbs: 'vbs.svg',
    yaml: 'yaml.svg',
    yml: 'yml.svg',
    md: 'md.svg',
    ps1: 'ps1.svg',
    ini: 'ini.svg',
    conf: 'conf.svg',
    properties: 'properties.svg',
    cmd: 'cmd.svg',
    vue: 'vue.svg',
    jsx: 'jsx.svg',
    perl: 'perl.svg',
    db2: 'db2.svg',
    rs: 'rs.svg',
    mm: 'mm.svg',
    m: 'm.svg',
    plsql: 'plsql.svg',
    hs: 'hs.svg',
    hsc: 'hsc.svg',
    Dockerfile: 'Dockerfile.svg',
    dart: 'dart.svg',
    pm: 'pm.svg',
    bash: 'bash.svg',
    svelte: 'svelte.svg',

    // 压缩包
    zip: 'zip.svg',
    rar: 'rar.svg',
    '7z': '7z.svg',
    gz: 'gz.svg',
    tar: 'tar.svg',
    // 网页
    html: 'html.svg',
    htm: 'htm.svg.svg',
    // 二进制程序
    exe: 'exe.svg',
    apk: 'apk.svg',
    ipa: 'ipa.svg',
    deb: 'deb.svg',
    rpm: 'rpm.svg',
    dmg: 'dmg.svg',
    msi: 'msi.svg',
    bin: 'bin.svg',
    iso: 'iso.svg'
  };
  if (icon_format_map[resource_format]) {
    icon_url = icon_format_map[resource_format];
    return icon_base_url + icon_url;
  }
  let icon_type_map = {};
  if (icon_type_map[resource_type]) {
    return icon_type_map[resource_type];
  }
  return icon_base_url + icon_url;
}
export function get_success_upload_task() {
  // 获取已经上传成功的文件数量
  let count = 0;
  for (let i = 0; i < upload_file_task_list.value.length; i++) {
    if (upload_file_task_list.value[i].task_status === 'success') {
      count++;
    }
  }
  return count;
}
export function get_success_upload_size() {
  // 获取已经上传成功的文件大小
  let size = 0;
  for (let i = 0; i < upload_file_task_list.value.length; i++) {
    if (upload_file_task_list.value[i].task_status === 'success') {
      size += upload_file_task_list.value[i].resource_size_in_mb;
    }
  }
  return parseFloat(size.toFixed(4));
}
export function get_upload_task_progress(item: ResourceUploadItem, output: string = 'number') {
  // 获取上传任务进度,以MB为单位或者以比例返回
  if (item.content_finish_idx === -1) {
    return 0;
  }
  if (output === 'number') {
    if (item.task_status === 'success') {
      return parseFloat(item.resource_size_in_mb.toFixed(4));
    }
    return item.content_finish_idx * upload_size.value;
  }
  let progress = Math.floor(((item.content_finish_idx * upload_size.value) / item.resource_size_in_mb) * 100);
  return parseFloat(progress.toFixed(4));
}
export function get_upload_speed() {
  // 获取上传速度: 3s内上传的文件大小
  let current_time = Date.now();
  let last_time = current_time - 3000;
  let finish_upload_size_in_3s = 0;
  for (let key in finish_time_size_map.value) {
    if (parseInt(key) > last_time) {
      finish_upload_size_in_3s += finish_time_size_map.value[key];
    }
  }
  return parseFloat((finish_upload_size_in_3s / 1024 / 1024 / 3).toFixed(2));
}

// 控制上传任务
export async function pause_upload_task(item: ResourceUploadItem) {
  // 暂停上传任务,修改任务状态为pause
  item.task_status = 'pause';
  item.content_finish_idx -= 1;
  // // console.log(
  //     '触发暂停上传任务',
  //     item.content_finish_idx, item.content_max_idx
  // )
  // 更新后端上传任务状态
  let params = {
    task_id: item.id,
    task_status: 'pause'
  };
  update_upload_task(params);
  // 更新管理器状态：如果所有任务都暂停了，那么管理器状态也为pause
  let all_pause = true;
  for (let i = 0; i < upload_file_task_list.value.length; i++) {
    if (upload_file_task_list.value[i].task_status !== 'pause') {
      all_pause = false;
      break;
    }
  }
  if (all_pause) {
    upload_manager_status.value = 'pause';
  }
}
export async function pause_all_upload_task() {
  // 暂停所有上传任务
  for (let i = 0; i < upload_file_task_list.value.length; i++) {
    if (upload_file_task_list.value[i].task_status !== 'uploading') {
      continue;
    }
    upload_file_task_list.value[i].task_status = 'pause';
    upload_file_task_list.value[i].content_finish_idx -= 1;
    // 更新后端上传任务状态
    let params = {
      task_id: upload_file_task_list.value[i].id,
      task_status: 'pause'
    };
    update_upload_task(params);
  }
  upload_manager_status.value = 'pause';
}
export async function continue_upload_task(item: ResourceUploadItem) {
  // 更新后端上传任务状态
  let params = {
    task_id: item.id,
    task_status: 'uploading'
  };
  await update_upload_task(params);
  // 继续上传任务,修改任务状态为uploading，然后继续上传
  item.task_status = 'uploading';
  // // console.log(
  //     '触发继续上传任务',
  //     item.content_finish_idx, item.content_max_idx
  // )
  upload_file_content(<UploadRequestOptions>{
    file: item.raw_file,
    data: {},
    headers: {}
  });
  // 更新管理器状态
  upload_manager_status.value = 'uploading';
}
export async function continue_all_upload_task() {
  // 继续所有上传任务
  for (let i = 0; i < upload_file_task_list.value.length; i++) {
    if (upload_file_task_list.value[i].task_status === 'pause') {
      // 更新后端上传任务状态
      let params = {
        task_id: upload_file_task_list.value[i].id,
        task_status: 'uploading'
      };
      await update_upload_task(params);

      upload_file_task_list.value[i].task_status = 'uploading';
      upload_file_content(<UploadRequestOptions>{
        file: upload_file_task_list.value[i].raw_file,
        data: {},
        headers: {}
      });
    }
  }
  upload_manager_status.value = 'uploading';
}
export async function remove_upload_task(item: ResourceUploadItem) {
  // 删除上传任务
  let index = upload_file_task_list.value.findIndex(value => value.id === item.id);
  upload_file_task_list.value.splice(index, 1);
  // 更新后端上传任务状态
  let params = {
    task_id: item.id,
    task_status: 'abort'
  };
  update_upload_task(params);
}
export async function retry_upload_task(item: ResourceUploadItem) {
  // 重试上传任务
  if (item.task_status === 'error') {
    // 更新后端上传任务状态
    let params = {
      task_id: item.id,
      task_status: 'pending'
    };
    await update_upload_task(params);
    item.task_status = 'pending';
    item.content_finish_idx = -1;
    await upload_file_content(<UploadRequestOptions>{
      file: item.raw_file,
      data: {},
      headers: {}
    });
    // 更新管理器状态
    upload_manager_status.value = 'uploading';
  } else {
    ElNotification.error({
      title: '系统通知',
      message: '任务状态不是错误状态，无法重试',
      duration: 5000
    });
  }
}
