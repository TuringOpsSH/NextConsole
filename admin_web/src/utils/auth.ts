import { getUser } from '@/api/user_center';
import router from '@/router';
import { config } from '@/utils/config';

export function getToken() {
  try {
    if (localStorage.getItem(config.TokenKey)) {
      return localStorage.getItem(config.TokenKey);
    } else {
      return null;
    }
  } catch (e) {
    console.info(e);
  }
}

export function setToken(token: string) {
  try {
    localStorage.setItem(config.TokenKey, token);
  } catch (e) {
    console.error(e);
  }
  return;
}

export function removeToken() {
  localStorage.removeItem(config.TokenKey);
  return true;
}

export async function getInfo(refresh: boolean = false) {
  let userInfo = null;
  if (refresh) {
    userInfo = (await getUser({})).result;
    setInfo(userInfo);
  } else {
    try {
      userInfo = localStorage.getItem(config.InfoKey);
      userInfo = JSON.parse(userInfo);
    } catch (e) {
      userInfo = {};
    }
  }

  if (userInfo) {
    return userInfo;
  } else {
    if (refresh) {
      await router.push({
        name: 'defaultPage'
      });
    }
  }
}

export function setInfo(info: object) {
  localStorage.setItem(config.InfoKey, JSON.stringify(info));
  return true;
}

export function removeInfo() {
  localStorage.removeItem(config.InfoKey);
  return true;
}
export function loginSave(res: object) {
  // 保存token和用户信息
  // @ts-ignore
  setToken(res.token);
  // @ts-ignore
  setInfo(res.userinfo);
}
export function logout() {
  removeToken();
  removeInfo();
  return true;
}
export function loginOut() {
  logout();
  router.push({ name: 'login' });
}
