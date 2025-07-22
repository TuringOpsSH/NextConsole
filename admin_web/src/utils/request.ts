import axios from 'axios';
import { ElNotification } from 'element-plus';
import { getToken, logout } from '@/utils/auth';
import router from '../router';

const request = axios.create({
  baseURL: '',
  method: 'post' // 项目默认请求数据方式为post
});

// 异常拦截处理器
const errorHandler = error => {
  if (error.response) {
    const data = error.response.data;
    const token = getToken();
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
      if (token) {
        router.push('/login');
      }
    }
    if (error.response.status === 401 || error.response.status === 422) {
      logout();
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
  const token = getToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  } else {
    ElNotification.warning({
      title: '系统通知',
      message: '登录状态失效，请重新登录',
      duration: 3666
    });
    // console.log('登录状态失效，请重新登录' ,config)
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
      logout();
    }

    if (response.data.msg && response.data.msg === 'Token has expired') {
      logout();
    }
  }
  return response.data;
}, errorHandler);
//
export default request;

export const download_request = axios.create({
  baseURL: '',
  method: 'post' // 项目默认请求数据方式为post
});
// 下载请求拦截
download_request.interceptors.request.use(config => {
  const token = getToken();

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  } else {
    ElNotification.warning({
      title: '系统通知',
      message: '登录状态失效，请重新登录',
      duration: 3666
    });
    router.push('/login');
  }

  config.params = {
    ...config.params
    // t: new Date().getTime() // 加上随机参数t，避免缓存请求
  };
  return config;
}, errorHandler);
