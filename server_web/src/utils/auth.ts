import {get_user} from "@/api/user_center";
import {config} from "@/utils/config";
import router from "@/router";
import {socket} from "@/components/global/web_socket/web_socket";


export function getToken() {
  try {
    if (localStorage.getItem(config?.TokenKey)){
      return localStorage.getItem(config?.TokenKey)
    }

    else {
      return null
    }
  } catch (e) {
    return null
  }

}

export function setToken(token :string) {
  try {
    localStorage.setItem(config.TokenKey, token)
  }catch (e) {
    console.error(e)
  }
  return
}

export function removeToken() {
  localStorage.removeItem(config.TokenKey)
  return true
}

export async function getInfo(refresh:boolean = false) {
  let user_info = null
  if (refresh){
    user_info = (await get_user({})).result
    setInfo(user_info)
  } else {
    try {
      user_info = localStorage.getItem(config.InfoKey)
      user_info = JSON.parse(user_info)

    } catch (e) {
      user_info = {}
    }

  }

  if (user_info){
    return user_info
  }

  else {
    if (refresh){
      router.push({
        name: 'defaultPage'
      })
    }

  }

}

export function setInfo(info:object) {
  localStorage.setItem(config.InfoKey, JSON.stringify(info))

  return true
}

export function removeInfo() {
  localStorage.removeItem(config.InfoKey)

  return true
}
export function login_save(res:object){
  // 保存token和用户信息
  // @ts-ignore
  setToken(res.token)
  // @ts-ignore
  setInfo(res.userinfo)
}
export function logout() {
  removeToken()
  removeInfo()
  if (socket.value){
    socket.value?.close()
  }
  return true
}
export function login_out(){
  logout()
  router.push({name: 'login'})
}
