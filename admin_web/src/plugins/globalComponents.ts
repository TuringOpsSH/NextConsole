import type { App } from 'vue';
import SvgIcon from '@/pages/components/SvgIcon.vue';

// 自动注册全局组件插件
const globalComponent = {
  install(app: App) {
    app.component('SvgIcon', SvgIcon);
  }
};

export default globalComponent;
