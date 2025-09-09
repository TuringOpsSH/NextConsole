import 'element-plus/dist/index.css';
import ElementPlus from 'element-plus';
import zhCn from 'element-plus/dist/locale/zh-cn.mjs';
import { createPinia } from 'pinia';
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate';
import { createApp } from 'vue';
import App from './App.vue';
import directives from './plugins/directives';
import globalComponent from './plugins/globalComponents';
import router from './router';
const pinia = createPinia();

pinia.use(piniaPluginPersistedstate);
createApp(App)
  .use(router)
  .use(ElementPlus, { locale: zhCn })
  .use(globalComponent)
  .use(directives)
  .use(pinia)
  .mount('#app');
