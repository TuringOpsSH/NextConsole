import { defineStore } from 'pinia';
import { ref, reactive, computed } from 'vue';
import { IUsers } from '@/types/user-center';

export const useUserInfoStore = defineStore(
  'userInfo',
  () => {
    const userInfo = reactive<IUsers>({
      user_resource_limit: 0,
      user_id: null,
      user_code: null,
      user_name: null,
      user_nick_name: null,
      user_nick_name_py: 'null',
      user_email: null,
      user_phone: null,
      user_gender: null,
      user_age: null,
      user_avatar: null,
      user_department: null,
      user_company: null,
      user_account_type: null,
      create_time: null,
      update_time: null,
      user_expire_time: null,
      last_login_time: null,
      user_role: null,
      user_status: null,
      user_source: null,
      user_wx_nickname: null,
      user_wx_avatar: null,
      user_wx_openid: null,
      user_wx_union_id: null,
      user_position: null,
      user_department_id: null,
      user_company_id: null,
      user_point_account: null
    });
    const token = ref('');
    const expireTime = ref('');
    const userHeader = computed(() => {
      // eslint-disable-next-line @typescript-eslint/naming-convention
      return { Authorization: 'Bearer ' + token.value };
    });
    function updateUserInfo(info: IUsers) {
      Object.assign(userInfo, info);
    }
    function $reset() {
      userInfo.user_id = null;
      userInfo.user_code = null;
      userInfo.user_name = null;
      userInfo.user_nick_name = null;
      userInfo.user_nick_name_py = 'null';
      userInfo.user_email = null;
      userInfo.user_phone = null;
      userInfo.user_point_account = null;
      token.value = '';
      expireTime.value = '';
    }
    function translateUserRole(role: string) {
      switch (role) {
        case 'next_console_admin':
          return '平台管理员';
        case 'super_admin':
          return '超级管理员';
        case 'admin':
          return '管理员';
        case 'user':
          return '用户';
        case 'guest':
          return '访客';
        default:
          return role;
      }
    }
    return { userInfo, token, expireTime, userHeader, updateUserInfo, translateUserRole, $reset };
  },
  {
    persist: true // 启用持久化
  }
);
