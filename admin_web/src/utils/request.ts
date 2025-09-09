import axios from 'axios';
import { ElNotification } from 'element-plus';
import { useUserInfoStore } from '@/stores/userInfoStore';
import router from '../router';
function logOut() {
  const userInfoStore = useUserInfoStore();
  userInfoStore.$reset();
  router.push({ name: 'login' });
}
const request = axios.create({
  baseURL: '',
  method: 'post' // 项目默认请求数据方式为post
});

// 异常拦截处理器
const errorHandler = error => {
  if (error.response) {
    const data = error.response.data;
    if (error.response.error_code === 403) {
      ElNotification({
        title: '请求异常',
        message: data.error_message || 'Error',
        type: 'error',
        duration: 2500
      });
      router.push('/403');
    }
    if (error.response.error_code === 401) {
      ElNotification({
        title: '请求异常',
        message: data.error_message || 'Error',
        type: 'error',
        duration: 2500
      });
      const userInfoStore = useUserInfoStore();
      if (userInfoStore.token) {
        // 保存当前路由信息
        sessionStorage.setItem('redirectRoute', JSON.stringify(router.currentRoute.value));
        router.push({
          name: 'login',
          query: {
            invite_view_id: router.currentRoute.value.query?.invite_view_id
          }
        });
      }
    }
    if (error.response.status === 401 || error.response.status === 422) {
      logOut();
      // 保存当前路由信息
      sessionStorage.setItem('redirectRoute', JSON.stringify(router.currentRoute.value));
      router.push({
        name: 'login',
        query: {
          invite_view_id: router.currentRoute.value.query?.invite_view_id
        }
      });
    }
  }
  return Promise.reject(error);
};

// 请求拦截
request.interceptors.request.use(config => {
  // @ts-ignore
  if (config.noAuth) {
    // 直接返回配置，不做token处理
    return config;
  }
  const userInfoStore = useUserInfoStore();
  if (userInfoStore.token) {
    config.headers.Authorization = `Bearer ${userInfoStore.token}`;
  } else {
    ElNotification.warning({
      title: '系统通知',
      message: '登录状态失效，请重新登录',
      duration: 3666
    });
    // 保存当前路由信息
    sessionStorage.setItem('redirectRoute', JSON.stringify(router.currentRoute.value));
    router.push('/login');
    return Promise.reject('登录状态失效，请重新登录');
  }

  config.params = {
    ...config.params
    // t: new Date().getTime() // 加上随机参数t，避免缓存请求
  };
  return config;
}, errorHandler);

// 响应拦截
request.interceptors.response.use(response => {
  //json返回拦截
  if (response.data.error_status) {
    ElNotification.error({
      title: '请求异常',
      message: response.data.error_message,
      showClose: true,
      duration: 2500
    });
    // token失效处理
    if (response.data.error_code === 401) {
      logOut();
    }

    if (response.data.msg && response.data.msg === 'Token has expired') {
      logOut();
      // 保存当前路由信息
      sessionStorage.setItem('redirectRoute', JSON.stringify(router.currentRoute.value));
      router.push({
        name: 'login'
      });
    }
  }
  return response.data;
}, errorHandler);
//
export default request;
