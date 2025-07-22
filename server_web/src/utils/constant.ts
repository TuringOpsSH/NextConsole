import { IResourceFormat } from '@/types/resource_type';

export const AUTH_TYPE = [
  { value: 'read', text: '阅读' },
  { value: 'download', text: '下载' },
  { value: 'edit', text: '编辑' },
  { value: 'manage', text: '管理' }
];

export const RESOURCE_FORMATS: IResourceFormat[] = [
  {
    text: '智能文档',
    value: 'otl',
    formats: 'otl'
  },
  { text: '多维表格', value: 'dbt', formats: 'dbt' },
  { text: '文字', value: 'doc', formats: 'wps,wpt,doc,docx,dot,rtf,xml,docm,dotm,wdoc,txt' },
  { text: '演示', value: 'ppt', formats: 'dps,dpt,pptx,ppt,pptm,ppsx,pps,ppsm,potx,pot,potm,wpd,wppt' },
  {
    text: '表格',
    value: 'xls',
    formats: 'et,ett,xls,xlsx,xlsm,xlsb,xlam,xltx,xltm,xls,xlt,xla,xlw,odc,uxdc,dbf,prn,wxls,csv'
  },
  { text: 'PDF', value: 'pdf', formats: 'pdf' },
  { text: '未知', value: '', formats: '' }
];
