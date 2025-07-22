import { saveAs } from 'file-saver';
import { ResourceItem, TAuthType } from '@/types/resource_type';
import { AUTH_TYPE } from './constant';

export function getAuthTypeText(value: TAuthType) {
  return AUTH_TYPE.find(item => item.value === value)?.text;
}
export const isMobile = () => {
  const ua = navigator.userAgent;
  return !!ua.match(/(phone|pad|pod|iPhone|iPod|ios|iPad|Android|Mobile|BlackBerry|IEMobile)/i);
};

export const getPanelWidth = () => {
  return window.innerWidth < 768 ? window.innerWidth - 60 + 'px' : '400px';
};

export function sortResourceList(list: ResourceItem[]) {
  list.sort(handleSortResourceList);
}

export function sortShareResourceList(list: ResourceItem[]) {
  list.sort((a, b) => {
    if (a.resource && b.resource) {
      return handleSortResourceList(a.resource, b.resource);
    } else {
      return handleSortResourceList(a, b);
    }
  });
}

function handleSortResourceList(a: ResourceItem, b: ResourceItem) {
  const targetValue = 'folder';
  if (a.resource_type === targetValue && b.resource_type !== targetValue) return -1;
  if (b.resource_type === targetValue && a.resource_type !== targetValue) return 1;
  if (a.resource_type === targetValue && b.resource_type === targetValue) {
    const reg = /^[a-zA-Z0-9]/;
    const isAEn = reg.test(a.resource_name[0]); // 判断a的首字符是否为英文/数字
    const isBEn = reg.test(b.resource_name[0]); // 判断b的首字符是否为英文/数字
    // 场景1：a是英文/数字，b是中文 → a排前
    if (isAEn && !isBEn) return -1;
    // 场景2：a是中文，b是英文/数字 → b排前
    if (!isAEn && isBEn) return 1;
  }
  return a.resource_name.localeCompare(b.resource_name);
}

export function formatFileSize(bytes: number): string {
  const units = ['B', 'KB', 'MB', 'GB'];
  let unitIndex = 0;

  if (!bytes) {
    return '';
  }
  while (bytes >= 1024 && unitIndex < units.length - 1) {
    bytes /= 1024;
    unitIndex++;
  }

  return `${bytes.toFixed(2)} ${units[unitIndex]}`;
}

export function reformatFileSize(bytes: number) {
  if (!bytes) {
    return '0 B';
  }
  const newBytes = bytes * 1021 * 1024;
  return formatFileSize(newBytes);
}

/**
 * 根据文件类型返回对应的图标标识
 * @param fileType 文件扩展名或类型关键字（如 'jpg', 'document'）
 * @returns 图标标识字符串
 */
export function getFileIcon(fileType: string = ''): string {
  if (!fileType) return 'bar-txt';

  const type = fileType.toLowerCase();

  // 分类映射表（扩展名/类型关键字 -> 图标标识）
  const iconMap: Record<string, string> = {
    // 图像
    jpg: 'bar-image',
    jpeg: 'bar-image',
    png: 'bar-image',
    gif: 'bar-image',
    webp: 'bar-image',
    svg: 'bar-image',
    bmp: 'bar-image',
    ico: 'bar-image',
    // 文档
    pdf: 'bar-pdf',
    doc: 'bar-docx',
    docx: 'bar-docx',
    txt: 'bar-txt',
    md: 'bar-txt',
    rtf: 'bar-txt',
    // 表格
    xls: 'bar-xlsx',
    xlsx: 'bar-xlsx',
    csv: 'bar-xlsx',
    // 演示文稿
    ppt: 'bar-pptx',
    pptx: 'bar-pptx',
    // 压缩文件
    zip: 'bar-zip',
    rar: 'bar-zip',
    '7z': 'bar-zip',
    tar: 'bar-zip',
    gz: 'bar-zip',
    // 音频
    mp3: 'bar-audio',
    wav: 'bar-audio',
    ogg: 'bar-audio',
    // 视频
    mp4: 'bar-video',
    avi: 'bar-video',
    mov: 'bar-video',
    webm: 'bar-video',
    // 代码
    js: 'bar-code',
    ts: 'bar-code',
    html: 'bar-code',
    css: 'bar-code',
    json: 'bar-json',
    xml: 'bar-code',
    // 其他常见类型
    exe: 'bar-exe',
    dll: 'bar-exe',
    ini: 'bar-config',
    log: 'bar-config',
    // 关键字匹配（如参数传入 'document' 而非扩展名）
    document: 'bar-docx',
    image: 'bar-image',
    spreadsheet: 'bar-xlsx',
    presentation: 'bar-pptx',
    archive: 'bar-zip',
    audio: 'bar-audio',
    video: 'bar-video',
    code: 'bar-code'
  };

  return iconMap[type] || 'bar-txt'; // 默认返回文本图标
}

interface IBatchSaveFile {
  download_url: string;
  resource_id: number;
  resource_name: string;
}

export async function batchSaveFile(files: IBatchSaveFile[]) {
  for (const file of files) {
    const response = await fetch(file.download_url);
    const blob = new Blob([await response.arrayBuffer()], {
      type: 'application/octet-stream' // 明确为二进制流
    });
    saveAs(blob, file.resource_name);
  }
}

export function throttle<T extends (...args: any[]) => void>(func: T, delay: number): T {
  let lastTime = 0;
  return function (this: ThisParameterType<T>, ...args: Parameters<T>) {
    const now = Date.now();
    if (now - lastTime >= delay) {
      lastTime = now;
      func.apply(this, args);
    }
  } as T;
}

export function debounce<T extends (...args: any[]) => void>(func: T, delay: number): T {
  let timer: ReturnType<typeof setTimeout> | null = null;
  return function (this: ThisParameterType<T>, ...args: Parameters<T>) {
    if (timer) {
      clearTimeout(timer);
    }
    timer = setTimeout(() => {
      func.apply(this, args);
      timer = null;
    }, delay);
  } as T;
}
