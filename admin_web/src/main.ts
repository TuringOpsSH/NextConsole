import 'element-plus/dist/index.css';
import ElementPlus from 'element-plus';
import zhCn from 'element-plus/dist/locale/zh-cn.mjs';
import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import directives from './plugins/directives';
import globalComponent from './plugins/globalComponents';
createApp(App)
  .use(router)
  .use(ElementPlus, { locale: zhCn }).use(globalComponent)
  .use(directives)
  .mount('#app');
