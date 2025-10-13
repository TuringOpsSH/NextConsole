import { ElMessage } from 'element-plus';
import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router';
import AgentApp from '@/components/app-center/AgentApp.vue';
import ContactsPage from '@/components/contacts/ContactsPage.vue';
import CompanyStructure from '@/components/contacts/company-structure/company_structure.vue';
import friends from '@/components/contacts/friends/friends.vue';
import groupsChat from '@/components/contacts/groups_chat/groups_chat.vue';
import consoleMain from '@/components/next-console/ConsoleMain.vue';
import sessionHistory from '@/components/next-console/SessionHistory.vue';
import NextConsoleWelcomeHome from '@/components/next-console/WelcomeHome.vue';
import messageFlow from '@/components/next-console/messages-flow/MessageFlowMain.vue';
import ResourceViewer from '@/components/resource/resource-view/ResourceViewer.vue';
import ResourceCooling from '@/components/resource/resource_cooling/resource_cooling.vue';
import ResourceList from '@/components/resource/resource_list/resource_list.vue';
import ResourceMain from '@/components/resource/resource_main.vue';
import { parseResourceType, parseTagId } from '@/components/resource/resource_shortcut/resource_shortcut';
import ResourceShortcut from '@/components/resource/resource_shortcut/resource_shortcut.vue';
import MyFavorite from '@/components/resource/resources_favorite/my_resource_favorite.vue';
import ShareResources from '@/components/resource/share_resources/share_resources.vue';
import UserInfo from '@/components/user-center/UserInfo.vue';
import WxLoginCheck from '@/components/user-center/WxLoginCheck.vue';
import AgentAppV2 from '@/components/workbenches/AgentApp.vue';
import AppCenter from '@/pages/AppCenter.vue';
import Contract from '@/pages/Contract.vue';
import DefaultPage from '@/pages/DefaultPage.vue';
import Login from '@/pages/Login.vue';
import NextConsole from '@/pages/NextConsole.vue';
import Page403 from '@/pages/Page403.vue';
import Page404 from '@/pages/Page404.vue';
import PrivacyPolicy from '@/pages/PrivacyPolicy.vue';
import ResetPassword from '@/pages/ResetPassword.vue';
import invitation from '@/pages/invitation.vue';
import unsubscribe from '@/pages/unsubscribe.vue';
import { useUserInfoStore } from '@/stores/user-info-store';

const routes: RouteRecordRaw[] = [
  {
    path: '/next-console',
    name: 'next_console',
    component: NextConsole,
    strict: true,
    redirect: '/next-console/console/welcome',
    meta: { requiresAuth: false },
    children: [
      {
        path: 'user_info',
        name: 'next_console_user_info',
        component: UserInfo,
        meta: { requiresAuth: true },
        strict: true,
        props: route => ({
          tab: route.query.tab || 'base'
        })
      },
      {
        path: 'console',
        name: 'next_console_main',
        component: consoleMain,
        meta: { requiresAuth: true },
        strict: true,
        redirect: '/next_console/console/welcome',
        children: [
          {
            path: 'welcome',
            name: 'next_console_welcome_home',
            component: NextConsoleWelcomeHome,
            meta: { requiresAuth: true },
            strict: true
          },
          {
            path: 'workbenches/:appCode/:sessionCode?',
            name: 'workbenches',
            component: AgentAppV2,
            meta: { requiresAuth: true },
            props: route => ({
              appCode: route.params.appCode,
              sessionCode: route.params.sessionCode
            }),
            strict: true
          },
          {
            path: 'message_flow/:session_code?',
            name: 'message_flow',
            component: messageFlow,
            meta: { requiresAuth: true },
            strict: true,
            props: route => ({
              sessionCode: route.params.session_code || 'default',
              task_id: route.query.task_id || '',
              resource_key_word: route.query.resource_key_word,
              resource_type: route.query.resource_type,
              resource_format: route.query.resource_format,
              auto_ask: route.query.auto_ask === 'true',
              show_panel: route.query.show_panel === 'true'
            })
          },
          {
            path: 'session_history/:sessionSource',
            name: 'session_history',
            component: sessionHistory,
            meta: { requiresAuth: true },
            strict: true,
            props: route => ({
              sessionSource: route.params.sessionSource
            })
          }
        ]
      },
      {
        path: 'resources',
        name: 'resources',
        component: ResourceMain,
        meta: { requiresAuth: true },
        strict: true,
        children: [
          {
            path: 'resource_list/:resource_id?',
            name: 'resource_list',
            component: ResourceList,
            meta: { requiresAuth: true },
            strict: true,
            props: route => ({
              resource_id: route.params.resource_id
              // resource_view_model: route.query.view_model || 'card'
            })
          },
          {
            path: 'resource_shortcut/:tag_source?',
            name: 'resource_shortcut',
            component: ResourceShortcut,
            meta: { requiresAuth: true },
            strict: true,
            props: route => ({
              // 标签值

              tag_source: route.params.tag_source,
              tag_value: route.query.tag_value,
              tag_id: parseTagId(route.query.tag_id) || [],
              resource_key_word: route.query.resource_key_word,
              resource_format: parseResourceType(route.query.resource_format) || [],
              resource_type: parseResourceType(route.query.resource_type) || [],
              resource_view_model: route.query.view_model || 'card',
              //@ts-ignore
              page_size: parseInt(route.query.page_size) || 20,
              //@ts-ignore
              page_num: parseInt(route.query.page_num) || 1
            })
          },
          {
            path: 'resource_search/:tag_source?',
            name: 'resource_search',
            component: ResourceShortcut,
            meta: { requiresAuth: true },
            strict: true,
            props: route => ({
              // 标签值
              tag_source: route.params.tag_source,
              tag_value: route.query.tag_value,
              tag_id: parseTagId(route.query.tag_id) || [],
              resource_keyword: route.query.resource_keyword,
              resource_format: parseResourceType(route.query.resource_format) || [],
              resource_type: parseResourceType(route.query.resource_type) || [],
              resource_view_model: route.query.view_model || 'card',
              //@ts-ignore
              page_size: parseInt(route.query.page_size) || 20,
              //@ts-ignore
              page_num: parseInt(route.query.page_num) || 1,
              rag_enhance: route.query.rag_enhance === 'true'
            })
          },
          {
            name: 'resource_favorite',
            path: 'resource_favorite',
            component: MyFavorite,
            meta: { requiresAuth: true },
            strict: true
          },
          {
            path: 'resource_share/:resource_id?',
            name: 'resource_share',
            component: ShareResources,
            meta: { requiresAuth: true },
            strict: true,
            props: route => ({
              resource_id: route.params.resource_id
              // resource_view_model: route.query.view_model || 'card'
            })
          },
          {
            path: 'resource_recycle_bin/:tag_source?',
            name: 'resource_recycle_bin',
            component: ResourceShortcut,
            meta: { requiresAuth: true },
            strict: true,
            props: route => ({
              tag_id: parseTagId(route.query.tag_id) || [],
              tag_value: route.query.tag_value,
              resource_key_word: route.query.resource_key_word,
              resource_format: parseResourceType(route.query.resource_format) || [],
              resource_type: parseResourceType(route.query.resource_type) || [],
              resource_view_model: route.query.view_model || 'card',
              //@ts-ignore
              page_size: parseInt(route.query.page_size) || 20,
              //@ts-ignore
              page_num: parseInt(route.query.page_num) || 1
            })
          },
          {
            path: 'resource_viewer/:resource_id?',
            name: 'resource_viewer',
            component: ResourceViewer,
            meta: { requiresAuth: true },
            strict: true,
            props: route => ({
              resourceId: route.params.resource_id,
              pane: route.query.pane || 'preview'
            })
          },
          {
            name: 'resource_cooling',
            path: 'resource_cooling/:cooling_id?',
            component: ResourceCooling,
            meta: { requiresAuth: true },
            strict: true,
            props: route => ({
              cooling_id: route.params.cooling_id
            })
          }
        ]
      },
      {
        path: 'contacts',
        name: 'contacts',
        component: ContactsPage,
        meta: { requiresAuth: true },
        strict: true,
        children: [
          {
            name: 'company_structure',
            path: 'company_structure',
            component: CompanyStructure,
            meta: { requiresAuth: true },
            strict: true
          },
          {
            name: 'friends',
            path: 'friends',
            component: friends,
            meta: { requiresAuth: true },
            strict: true
          },
          {
            name: 'groups_chat',
            path: 'groups_chat',
            component: groupsChat,
            meta: { requiresAuth: true },
            strict: true
          }
        ]
      },
      {
        name: 'next_console_privacy_policy',
        path: 'privacy_policy',
        component: Contract,
        meta: { requiresAuth: true },
        strict: true
      }
    ]
  },
  {
    path: '/app_center',
    name: 'app_center',
    component: AppCenter,
    meta: { requiresAuth: false },
    strict: true,
    props: route => ({
      token: route.query.token
    }),
    children: [
      {
        name: 'agent_app',
        path: 'agent_app/:app_code/:session_code?',
        component: AgentApp,
        meta: { requiresAuth: false },
        strict: true,
        props: route => ({
          app_code: route.params.app_code,
          session_code: route.params.session_code,
          token: route.query.token
        })
      }
    ]
  },
  {
    path: '/login',
    name: 'login',
    component: Login,
    strict: true,
    meta: { requiresAuth: false },
    props: route => ({
      loginType: route.query.login_type || 'code',
      inviteViewId: Number(route.query.invite_view_id) || 0
    })
  },
  {
    path: '/login/wx_login',
    name: 'wx_login',
    component: WxLoginCheck,
    meta: { requiresAuth: false },
    props: route => ({
      code: route.query.code,
      state: route.query.state
    })
  },
  {
    path: '/reset_password',
    name: 'reset_password',
    component: ResetPassword,
    strict: true,
    meta: { requiresAuth: false }
  },
  {
    path: '/contract',
    name: 'contract',
    component: Contract,
    strict: true,
    meta: { requiresAuth: false }
  },
  {
    path: '/privacy_policy',
    name: 'privacy_policy',
    component: PrivacyPolicy,
    strict: true,
    meta: { requiresAuth: false }
  },
  {
    path: '/403',
    name: '403',
    component: Page403,
    strict: true,
    meta: { requiresAuth: false }
  },
  {
    name: 'invitation',
    path: '/invitation',
    component: invitation,
    strict: true,
    meta: { requiresAuth: false },
    props: route => ({
      inviteCode: route.query.invite_code,
      inviteType: route.query.invite_type,
      marketingCode: route.query.marketing_code
    })
  },
  {
    name: 'unsubscribe',
    path: '/unsubscribe',
    component: unsubscribe,
    strict: true,
    meta: { requiresAuth: true }
  },
  {
    path: '/resourceRemoved',
    name: 'resourceRemoved',
    component: () => import('@/components/resource/ResourceRemoved.vue'),
    meta: { requiresAuth: true },
    strict: true
  },
  {
    path: '/',
    name: 'defaultPage',
    component: DefaultPage,
    strict: true,
    meta: { requiresAuth: true },
    beforeEnter: (to, from, next) => {
      const userInfoStore = useUserInfoStore();
      if (userInfoStore.token) {
        router.push({ name: 'next_console_welcome_home' });
      } else {
        next();
      }
    }
  },
  {
    path: '/:pathMatch(.*)+',
    name: '404',
    component: Page404,
    meta: { requiresAuth: false }
  }
];

const router = createRouter({
  end: undefined,
  sensitive: undefined,
  strict: true,
  history: createWebHistory(),
  routes
});
router.beforeEach(async (to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
  const isRemoved = to.matched.some(record => record.meta.isRemoved);
  const requiresAuthRole = to.matched.some(record => record.meta.requiresAuthRole);
  const userInfoStore = useUserInfoStore();
  if (requiresAuth) {
    // 需要鉴权页面
    if (!requiresAuthRole) {
      // 不需要特定角色
      if (userInfoStore.token) {
        // 如果当前有用户登录token
        next();
        return;
      }
      ElMessage.warning('登录已超时，请重新登录！');
      // 保存当前路由信息
      sessionStorage.setItem('redirectRoute', JSON.stringify(to));
      next({
        name: 'login',
        query: {
          ...to.query
        }
      });
    } else {
      // 需要特定角色
      if (userInfoStore.token) {
        const requiredRoles: string[] = to.meta.requiresAuthRole as string[];
        // @ts-ignore
        const overlappingValues = requiredRoles.filter(value => userInfoStore.userInfo.user_role.includes(value));
        if (overlappingValues.length > 0) {
          // 如果用户角色包含所需角色,放行
          next();
          return;
        } else {
          next('/403'); // 如果用户角色不包含所需角色，跳转到403页面
          return;
        }
      }
      ElMessage.warning('登录已超时，请重新登录！');
      // 保存当前路由信息
      sessionStorage.setItem('redirectRoute', JSON.stringify(to));
      next({
        name: 'login',
        query: {
          ...to.query
        }
      });
    }
  } else if (isRemoved) {
    next({ name: 'resourceRemoved' });
  } else {
    next();
  }
});
export default router;
