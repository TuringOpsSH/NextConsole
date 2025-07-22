import 'element-plus/dist/index.css';
import ElementPlus from 'element-plus';
import zhCn from 'element-plus/dist/locale/zh-cn.mjs';
import { createPinia } from 'pinia';
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate';
import { createApp } from 'vue';
import App from './App.vue';
import { i18n } from '@/locales';
import router from '@/router';

const app = createApp(App);
const pinia = createPinia();

pinia.use(piniaPluginPersistedstate);
app.use(router);
app.use(ElementPlus, { locale: zhCn });
app.use(pinia);
app.use(i18n);

app.mount('#app');
