import {enc} from 'crypto-js';
import sha256 from 'crypto-js/sha256';
import {ElNotification, UploadRawFile, UploadRequestOptions, UploadUserFile} from 'element-plus';
import {ref} from 'vue';
import {add_upload_task, update_upload_task, upload_resource_object} from '@/api/resource-api';
import {current_resource, search_all_resource_object} from '@/components/resource/resource-list/resource-list';
import {init_my_resource_tree, show_upload_button} from '@/components/resource/resource-panel/panel';
import {showUploadDialogMultiple} from '@/components/resource/resource_tree/resource-tree';
import {IResourceItem, IResourceUploadItem} from '@/types/resource-type';
import router from "@/router";

export const show_upload_manage_box = ref(false);
export const upload_file_task_list = ref<IResourceUploadItem[]>([]);

export const upload_manager_status = ref('pending');
export const upload_size = ref(1);
export const finish_time_size_map = ref({});
export const upload_parent_resource = ref<IResourceItem>(null);
export const upload_button_Ref = ref(null);
export const folder_upload_parent_resource = ref(null);

// 原始上传文件列表
export const upload_file_list = ref<UploadUserFile[]>([]);
export const show_close_confirm_flag = ref(false);
export async function retry_all_upload_file() {
  // 重试所有上传任务
  show_upload_manage_box.value = true;
  for (const item of upload_file_list.value) {
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
      const params = {
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
      return;
    }
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
  } catch (e) {
    return;
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
  // 1. 计算文件的MD5值
  let fileSHA256 = '';
  try {
    fileSHA256 = await calculateMD5(uploadFile);
    if (!fileSHA256) {
      fileSHA256 = await calculateSHA256(uploadFile);
    }
  } catch (e) {
    fileSHA256 = await calculateSHA256(uploadFile);
  }
  if (!fileSHA256) {
    ElNotification.error({
      title: '系统通知',
      message: '文件上传失败，无法计算文件特征值！',
      duration: 5000
    });
    return false;
  }
  // 2. 准备参数
  const resourceSize = uploadFile.size / 1024 / 1024;
  const contentMaxidx = Math.floor(resourceSize / upload_size.value);
  // 前端临时可视化文件类型和格式
  let resourceType = '';
  let resourceFormat = '';

  if (uploadFile.name.indexOf('.') > -1) {
    resourceFormat = uploadFile.name.split('.').pop().toLowerCase();
  }
  resourceType = uploadFile.type;
  const taskIcon = get_task_icon(resourceType, resourceFormat);
  const newUploadFileTask = <IResourceUploadItem>{
    id: null,
    resource_parent_id: current_resource.id,
    resource_id: null,
    resource_name: uploadFile.name,
    resource_size_in_mb: resourceSize,
    resource_type: resourceType,
    resource_format: resourceFormat,
    content_max_idx: contentMaxidx,
    content_finish_idx: -1,
    resource_md5: fileSHA256,
    raw_file: uploadFile,
    task_icon: taskIcon,
    task_status: 'pending'
  };
  upload_file_task_list.value.push(newUploadFileTask);
  if (['resource_shortcut', 'resource_search', 'resource_share'].includes(router.currentRoute.value.name as string)) {
    upload_parent_resource.value.id = null;
  }
  if (!upload_parent_resource.value?.id) {
    // console.log('无选择父资源')
    upload_button_Ref.value?.handleStart(uploadFile);
    upload_file_list.value.push(uploadFile);
    await showUploadDialogMultiple(retry_all_upload_file);
    return false;
  }
}
export async function upload_file_content(options: UploadRequestOptions) {
  // 分块上传文件内容
  const { file, data, headers } = options;
  const targetUploadTask = upload_file_task_list.value.find(item => item?.raw_file?.uid === file?.uid);
  console.log(targetUploadTask, file)
  if (!targetUploadTask) {
    return false;
  }
  if (!targetUploadTask.id) {
    const uploadTaskParams = {
      resource_parent_id: targetUploadTask.resource_parent_id,
      resource_name: targetUploadTask.resource_name,
      resource_size: targetUploadTask.resource_size_in_mb,
      resource_type: targetUploadTask.resource_type,
      resource_format: targetUploadTask.resource_format,
      task_source: targetUploadTask.task_source,
      content_max_idx: targetUploadTask.content_max_idx,
      resource_md5: targetUploadTask.resource_md5
    };

    // 3. 生成上传任务
    const res = await add_upload_task(uploadTaskParams);
    if (!res.error_status && !res.error_message) {
      // 4. 更新上传任务列表
      targetUploadTask.id = res.result.id;
      upload_manager_status.value = 'uploading';
      targetUploadTask.resource_name = res.result.resource_name;
      targetUploadTask.resource_type = res.result.resource_type;
      targetUploadTask.resource_format = res.result.resource_format;
      targetUploadTask.task_icon = res.result.task_icon;
      targetUploadTask.task_status = res.result.task_status;
    } else {
      targetUploadTask.task_status = 'error';
      targetUploadTask.task_error_msg = '空';
      return false;
    }
  }
  targetUploadTask.task_status = 'uploading';
  // 循环上传文件内容
  const contentSize = 1024 * 1024 * upload_size.value;
  let content = null;
  const arrayBuffer = null;
  const hashBuffer = null;
  const hashArray = null;
  let chunkMD5 = '';
  // 从已经上传的位置开始上传，默认为-1
  let res = null;
  try {
    const beginIdx = targetUploadTask.content_finish_idx + 1;
    for (let i = beginIdx; i <= targetUploadTask.content_max_idx; i++) {
      if (targetUploadTask.task_status === 'pause') {
        return false;
      }
      const startIdx = i * contentSize;
      let endIdx = (i + 1) * contentSize;
      if (endIdx > targetUploadTask.raw_file.size) {
        endIdx = targetUploadTask.raw_file.size;
      }
      content = targetUploadTask.raw_file.slice(startIdx, endIdx);
      try {
        chunkMD5 = await calculateMD5(content);
        if (!chunkMD5) {
          chunkMD5 = await calculateSHA256(content);
        }
      } catch (e) {
        chunkMD5 = await calculateSHA256(content);
      }
      // // console.log('上传文件chunkMD5', startIdx, endIdx, i, chunkMD5  )
      const uploadContentForm = new FormData();
      uploadContentForm.append('chunk_task_id', targetUploadTask.id.toString());
      uploadContentForm.append('chunk_index', i.toString());
      uploadContentForm.append('chunk_content', content);
      uploadContentForm.append('chunk_MD5', chunkMD5);
      uploadContentForm.append('chunk_size', content.size);
      res = await upload_resource_object(uploadContentForm);
      if (!res.error_status) {
        init_my_resource_tree();
        // 上传成功，更新位置
        targetUploadTask.content_finish_idx = i;
        const finishTime = Date.now();
        if (!finish_time_size_map.value[finishTime]) {
          finish_time_size_map.value[finishTime] = 0;
        }
        finish_time_size_map.value[finishTime] += endIdx - startIdx;
      } else {
        targetUploadTask.task_status = 'error';
        return false;
      }
    }
  } catch (e) {
    targetUploadTask.task_status = 'error';
    ElNotification.error({
      title: '系统通知',
      message: '上传文件内容失败' + e,
      duration: 5000
    });
    return false;
  }
  // 上传成功，更新状态
  targetUploadTask.task_status = 'success';
  // 更新后端上传任务状态
  const params = {
    task_id: targetUploadTask.id,
    task_status: 'success'
  };
  update_upload_task(params);
  search_all_resource_object();
  let failFlag = false;
  for (let i = 0; i < upload_file_task_list.value.length; i++) {
    if (upload_file_task_list.value[i].task_status !== 'success') {
      failFlag = true;
      break;
    }
  }
  if (!failFlag) {
    upload_manager_status.value = 'success';
  }
  return res;
}

// 获取可视化要素
export function get_task_icon(resource_type: string, resource_format: string) {
  // 获取任务图标
  const icon_base_url = '/images/';
  let icon_url = 'other.svg';
  const icon_format_map = {
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
  const icon_type_map = {};
  if (icon_type_map[resource_type]) {
    return icon_type_map[resource_type];
  }
  return icon_base_url + icon_url;
}
