import { ref } from 'vue';
export interface IConfigArea {
  area: string;
  name: string;
  label: string;
  icon: string;
}
export const configArea = <IConfigArea[]>[
  {
    area: 'welcome',
    name: 'configEdit',
    label: '欢迎页配置',
    icon: 'images/welcome.svg'
  }
];
export const currentAppConfigArea = ref<IConfigArea>({
  area: '',
  name: 'configEdit',
  label: '欢迎页配置',
  icon: 'images/welcome.svg'
});

