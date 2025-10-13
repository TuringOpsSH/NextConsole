import { ElMessage } from 'element-plus';
import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router';
import AppCenter from '@/components/app-center/AppCenter.vue';
import AppDetail from '@/components/app-center/app-manage/AppDetail.vue';
import AppList from '@/components/app-center/app-manage/AppList.vue';
import ConfigEditor from '@/components/app-center/app-manage/ConfigEditor.vue';
import effectManage from '@/components/app-center/app-manage/EffectManage.vue';
import resourceManage from '@/components/app-center/app-manage/ResourceManage.vue';
import workflowEdit from '@/components/app-center/app-manage/WorkflowEdit.vue';
import LLMCreate from '@/components/app-center/model-manage/LLMCreate.vue';
import LLMDetail from '@/components/app-center/model-manage/LLMDetail.vue';
import LlmManage from '@/components/app-center/model-manage/LlmManage.vue';
import PublishConnector from '@/components/app-center/publish-manage/PublishConnector.vue';
import PublishCreate from '@/components/app-center/publish-manage/PublishCreate.vue';
import PublishDetail from '@/components/app-center/publish-manage/PublishDetail.vue';
import PublishList from '@/components/app-center/publish-manage/PublishList.vue';
import Dashboard from '@/components/dashboard/Dashboard.vue';
import UserActivity from '@/components/dashboard/UserActivity.vue';
import Feedback from '@/components/feedback-center/Feedback.vue';
import SearchModel from '@/components/feedback-center/SearchModel.vue';
import MarketingCampaign from '@/components/user-center/MarketingCampaign.vue';
import MarketingCampaignDetail from '@/components/user-center/MarketingCampaignDetail.vue';
import UserCenter from '@/components/user-center/UserCenter.vue';
import UserInfo from '@/components/user-center/UserInfo.vue';
import UserManage from '@/components/user-center/UserManage.vue';
import WxLoginCheck from '@/components/user-center/WxLoginCheck.vue';
import UserNoticeDetail from '@/components/user-center/user-notice/UserNoticeDetail.vue';
import UserNotification from '@/components/user-center/user-notice/UserNotification.vue';
import UserNotificationList from '@/components/user-center/user-notice/UserNotificationList.vue';
import Contract from '@/pages/Contract.vue';
import Login from '@/pages/Login.vue';
import NextConsole from '@/pages/NextConsole.vue';
import Page404 from '@/pages/Page404.vue';
import ResetPassword from '@/pages/ResetPassword.vue';
import PrivacyPolicy from '@/pages/privacyPolicy.vue';
import { useUserInfoStore } from '@/stores/user-info-store';

const routes: RouteRecordRaw[] = [
  {
    path: '/next-console',
    name: 'next_console',
    component: NextConsole,
    strict: true,
    meta: { requiresAuth: true },
    children: [
      {
        path: 'user-center',
        name: 'user_center',
        meta: {
          requiresAuth: true,
          requiresAuthRole: ['admin', 'super_admin', 'next_console_admin', 'next_console_reader_admin']
        },
        component: UserCenter,
        strict: true,
        children: [
          {
            path: 'user-manage',
            name: 'user_manage',
            meta: {
              requiresAuth: true,
              requiresAuthRole: ['admin', 'super_admin', 'next_console_admin', 'next_console_reader_admin']
            },
            strict: true,
            component: UserManage
          },
          {
            path: 'enterpriseManagement',
            name: 'enterpriseManagement',
            meta: {
              requiresAuth: true,
              requiresAuthRole: ['admin', 'super_admin', 'next_console_admin', 'next_console_reader_admin']
            },
            strict: true,
            component: () => import('@/components/views/enterpriseManagement/Index.vue')
          },
          {
            path: 'user_notification',
            name: 'user_notification',
            meta: {
              requiresAuth: true,
              requiresAuthRole: ['next_console_admin']
            },
            strict: true,
            component: UserNotification,
            children: [
              {
                path: 'detail',
                name: 'user_notice_detail',
                strict: true,
                meta: {
                  requiresAuth: true,
                  requiresAuthRole: ['next_console_admin']
                },
                component: UserNoticeDetail,
                props: route => ({
                  //@ts-ignore
                  task_id: parseInt(route.query.task_id) || null
                })
              },
              {
                path: 'list',
                name: 'user_notification_list',
                meta: {
                  requiresAuth: true,
                  requiresAuthRole: ['next_console_admin']
                },
                strict: true,
                component: UserNotificationList,
                props: route => ({
                  //@ts-ignore
                  pageSize: parseInt(route.query.page_size) || 20,
                  //@ts-ignore
                  pageNum: parseInt(route.query.page_num) || 1
                })
              }
            ]
          },
          {
            path: 'marketing_campaign',
            name: 'marketing_campaign',
            meta: {
              requiresAuth: true,
              requiresAuthRole: ['next_console_admin']
            },
            strict: true,
            component: MarketingCampaign
          },
          {
            path: 'marketing_campaign/:campaign_id',
            name: 'marketing_campaign_detail',
            meta: {
              requiresAuth: true,
              requiresAuthRole: ['next_console_admin']
            },
            strict: true,
            component: MarketingCampaignDetail,
            props: route => ({
              // @ts-ignore
              campaignId: parseInt(route.params.campaign_id) || null,
              viewPane: route.query.viewPane || 'meta'
            })
          }
        ]
      },
      {
        path: 'user_info',
        name: 'next_console_user_info',
        meta: {
          requiresAuth: true,
          requiresAuthRole: ['admin', 'super_admin', 'next_console_admin', 'next_console_reader_admin']
        },
        component: UserInfo,
        props: route => ({
          tab: route.query.tab || 'info'
        })
      },
      {
        path: 'dashboard',
        name: 'dashboard',
        meta: {
          requiresAuth: true,
          requiresAuthRole: ['admin', 'super_admin', 'next_console_admin', 'next_console_reader_admin']
        },
        component: Dashboard,
        children: [
          {
            path: 'user_activity',
            name: 'user_activity',
            meta: { requiresAuth: true },
            component: UserActivity,
            props: route => ({
              tab: route.query.tab || 'user'
            })
          }
        ]
      },
      {
        path: '/feedback',
        name: 'feedback',
        component: Feedback,
        meta: {
          requiresAuth: true,
          requiresAuthRole: ['admin', 'super_admin', 'next_console_admin', 'next_console_reader_admin']
        },
        children: [
          {
            path: 'search_model',
            name: 'search_model',
            meta: {
              requiresAuth: true
            },
            component: SearchModel
          }
        ]
      },
      {
        name: 'appCenter',
        path: 'app-center',
        meta: {
          requiresAuth: true,
          requiresAuthRole: ['next_console_admin', 'admin', 'super_admin']
        },
        component: AppCenter,
        children: [
          {
            name: 'appList',
            path: 'app-list',
            meta: {
              requiresAuth: true,
              requiresAuthRole: ['next_console_admin', 'admin', 'super_admin']
            },
            component: AppList
          },
          {
            name: 'appDetail',
            path: 'app-detail/:app_code',
            meta: {
              requiresAuth: true,
              requiresAuthRole: ['next_console_admin', 'admin', 'super_admin']
            },
            component: AppDetail,
            props: route => ({
              appCode: route.params.app_code || ''
            }),
            children: [
              {
                name: 'workflowEdit',
                path: 'workflowEdit/:workflowCode',
                meta: {
                  requiresAuth: true,
                  requiresAuthRole: ['next_console_admin', 'admin', 'super_admin']
                },
                component: workflowEdit,
                props: route => ({
                  appCode: route.params.app_code || '', // 传递 app_code
                  workflowCode: route.params.workflowCode || ''
                })
              },
              {
                name: 'configEdit',
                path: 'configEdit/:area',
                meta: {
                  requiresAuth: true,
                  requiresAuthRole: ['next_console_admin', 'admin', 'super_admin']
                },
                component: ConfigEditor,
                props: route => ({
                  appCode: route.params.app_code || '', // 传递 app_code
                  area: route.params.area
                })
              }
            ]
          },
          {
            name: 'publishList',
            path: 'publish-list',
            meta: {
              requiresAuth: true,
              requiresAuthRole: ['next_console_admin', 'admin', 'super_admin']
            },
            component: PublishList
          },
          {
            name: 'publishCreate',
            path: 'publish-create/:app_code',
            meta: {
              requiresAuth: true,
              requiresAuthRole: ['next_console_admin', 'admin', 'super_admin']
            },
            component: PublishCreate,
            props: route => ({
              appCode: route.params.app_code || ''
            })
          },
          {
            name: 'publishConnector',
            path: 'publish-connector',
            meta: {
              requiresAuth: true,
              requiresAuthRole: ['next_console_admin', 'admin', 'super_admin']
            },
            component: PublishConnector
          },
          {
            name: 'publishDetail',
            path: 'publish-detail/:app_code',
            meta: {
              requiresAuth: true,
              requiresAuthRole: ['next_console_admin', 'admin', 'super_admin']
            },
            component: PublishDetail,
            props: route => ({
              appCode: route.params.app_code || '',
              viewTab: route.query.viewTab || 'history',
              accessType: route.query.accessType
            })
          },
          {
            name: 'resourceManage',
            path: 'resource-manage',
            meta: {
              requiresAuth: true,
              requiresAuthRole: ['next_console_admin', 'admin', 'super_admin']
            },
            component: resourceManage
          },
          {
            name: 'llmManage',
            path: 'llm-manage',
            meta: {
              requiresAuth: true,
              requiresAuthRole: ['next_console_admin', 'admin', 'super_admin']
            },
            component: LlmManage,
            props: route => ({
              subpage: route.params.subpage || 'llm',
              page_num: route.query.page_num,
              page_size: route.query.page_size,
              keyword: route.query.keyword,
              status: route.query.status,
              type: route.query.type
            })
          },
          {
            name: 'llmCreate',
            path: 'llm-create',
            meta: {
              requiresAuth: true,
              requiresAuthRole: ['next_console_admin', 'admin', 'super_admin']
            },
            component: LLMCreate,
            props: route => ({
              step: route.query.step
            })
          },
          {
            name: 'llmDetail',
            path: 'llm-detail/:llmCode',
            meta: {
              requiresAuth: true,
              requiresAuthRole: ['next_console_admin', 'admin', 'super_admin']
            },
            component: LLMDetail,
            props: route => ({
              llmCode: route.params.llmCode,
              tab: route.query.tab
            })
          },
          {
            name: 'effectManage',
            path: 'effect_manage',
            meta: {
              requiresAuth: true,
              requiresAuthRole: ['next_console_admin']
            },
            component: effectManage
          }
        ]
      }
    ]
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
    path: '/login',
    name: 'login',
    component: Login,
    strict: true,
    meta: { requiresAuth: false },
    props: route => ({
      login_type: route.query.login_type || 'code'
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
    path: '/403',
    name: '403',
    component: Login,
    strict: true,
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    name: 'defaultPage',
    strict: true,
    meta: { requiresAuth: false },
    component: AppCenter,
    beforeEnter: (to, from, next) => {
      const userInfoStore = useUserInfoStore();
      if (userInfoStore.token) {
        router.push({ name: 'appCenter' });
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
  // 1. 检测是否带 `/#/` 前缀
  if (to.fullPath.startsWith('/#/')) {
    const normalizedPath = to.fullPath.replace('/#/', '/'); // 去掉 `/#/` 前缀
    return next({
      path: normalizedPath,
      query: to.query,
      hash: to.hash,
      replace: true
    });
  }
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
