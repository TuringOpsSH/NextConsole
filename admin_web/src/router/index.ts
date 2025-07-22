import { ElMessage } from 'element-plus';
import { createRouter, createWebHashHistory, RouteRecordRaw } from 'vue-router';
import appCenter from '@/components/appCenter/AppCenter.vue';
import appDetail from '@/components/appCenter/AppDetail.vue';
import appList from '@/components/appCenter/AppList.vue';
import ConfigEditor from '@/components/appCenter/ConfigEditor.vue';
import effectManage from '@/components/appCenter/EffectManage.vue';
import llmManage from '@/components/appCenter/LlmManage.vue';
import resourceManage from '@/components/appCenter/ResourceManage.vue';
import workflowEdit from '@/components/appCenter/WorkflowEdit.vue';
import PublishConnector from '@/components/appCenter/publish/PublishConnector.vue';
import PublishCreate from '@/components/appCenter/publish/PublishCreate.vue';
import PublishDetail from '@/components/appCenter/publish/PublishDetail.vue';
import PublishList from '@/components/appCenter/publish/PublishList.vue';
import costExpenses from '@/components/dashboard/cost_expenses.vue';
import dashboard from '@/components/dashboard/dashboard.vue';
import system from '@/components/dashboard/system.vue';
import userActivity from '@/components/dashboard/user_activity.vue';
import Feedback from '@/components/feedback_center/Feedback.vue';
import SearchModel from '@/components/feedback_center/SearchModel.vue';
import MarketingCampaign from '@/components/user_center/MarketingCampaign.vue';
import MarketingCampaignDetail from '@/components/user_center/MarketingCampaignDetail.vue';
import userCenter from '@/components/user_center/user_center.vue';
import userInfo from '@/components/user_center/user_info.vue';
import userManage from '@/components/user_center/user_manage.vue';
import userNoticeDetail from '@/components/user_center/user_notice/user_notice_detail.vue';
import userNotification from '@/components/user_center/user_notice/user_notification.vue';
import userNotificationList from '@/components/user_center/user_notice/user_notification_list.vue';
import wxLoginCheck from '@/components/user_center/wx_login_check.vue';
import Contract from '@/pages/Contract.vue';
import defaultPage from '@/pages/defaultPage.vue';
import login from '@/pages/login.vue';
import page403 from '@/pages/login.vue';
import nextConsole from '@/pages/next_console.vue';
import page404 from '@/pages/page_404.vue';
import privacyPolicy from '@/pages/privacy_policy.vue';
import resetPassword from '@/pages/reset_password.vue';

import { getInfo, getToken } from '@/utils/auth';

const routes: RouteRecordRaw[] = [
    {
        path: '/next_console',
        name: 'next_console',
        component: nextConsole,
        strict: true,
        meta: { requiresAuth: true },
        children: [
            {
                path: 'user_center',
                name: 'user_center',
                meta: {
                    requiresAuth: true,
                    requiresAuthRole: ['admin', 'super_admin', 'next_console_admin', 'next_console_reader_admin']
                },
                component: userCenter,
                strict: true,
                children: [
                    {
                        path: 'user_manage',
                        name: 'user_manage',
                        meta: {
                            requiresAuth: true,
                            requiresAuthRole: ['admin', 'super_admin', 'next_console_admin', 'next_console_reader_admin']
                        },
                        strict: true,
                        component: userManage
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
                        component: userNotification,
                        children: [
                            {
                                path: 'detail',
                                name: 'user_notice_detail',
                                strict: true,
                                meta: {
                                    requiresAuth: true,
                                    requiresAuthRole: ['next_console_admin']
                                },
                                component: userNoticeDetail,
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
                                component: userNotificationList,
                                props: route => ({
                                    //@ts-ignore
                                    page_size: parseInt(route.query.page_size) || 20,
                                    //@ts-ignore
                                    page_num: parseInt(route.query.page_num) || 1
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
                component: userInfo
            },
            {
                path: 'dashboard',
                name: 'dashboard',
                meta: {
                    requiresAuth: true,
                    requiresAuthRole: ['admin', 'super_admin', 'next_console_admin', 'next_console_reader_admin']
                },
                component: dashboard,
                children: [
                    {
                        path: 'user_activity',
                        name: 'user_activity',
                        meta: { requiresAuth: true },
                        component: userActivity
                    },
                    {
                        path: 'system',
                        name: 'system',
                        meta: { requiresAuth: true },
                        component: system
                    },
                    {
                        path: 'cost_expenses',
                        name: 'cost_expenses',
                        meta: { requiresAuth: true },
                        component: costExpenses
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
                path: 'app_center',
                meta: {
                    requiresAuth: true,
                    requiresAuthRole: ['next_console_admin', 'admin', 'super_admin']
                },
                component: appCenter,
                children: [
                    {
                        name: 'appList',
                        path: 'app_list',
                        meta: {
                            requiresAuth: true,
                            requiresAuthRole: ['next_console_admin', 'admin', 'super_admin']
                        },
                        component: appList
                    },
                    {
                        name: 'appDetail',
                        path: 'app_detail/:app_code',
                        meta: {
                            requiresAuth: true,
                            requiresAuthRole: ['next_console_admin', 'admin', 'super_admin']
                        },
                        component: appDetail,
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
                        path: 'publish_list',
                        meta: {
                            requiresAuth: true,
                            requiresAuthRole: ['next_console_admin', 'admin', 'super_admin']
                        },
                        component: PublishList
                    },
                    {
                        name: 'publishCreate',
                        path: 'publish_create/:app_code',
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
                        path: 'publish_connector',
                        meta: {
                            requiresAuth: true,
                            requiresAuthRole: ['next_console_admin', 'admin', 'super_admin']
                        },
                        component: PublishConnector
                    },
                    {
                        name: 'publishDetail',
                        path: ':app_code/publish_detail',
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
                        path: 'resource_manage',
                        meta: {
                            requiresAuth: true,
                            requiresAuthRole: ['next_console_admin', 'admin', 'super_admin']
                        },
                        component: resourceManage
                    },
                    {
                        name: 'llmManage',
                        path: 'llm_manage/:subpage',
                        meta: {
                            requiresAuth: true,
                            requiresAuthRole: ['next_console_admin', 'admin', 'super_admin']
                        },
                        component: llmManage,
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
        component: privacyPolicy,
        strict: true,
        meta: { requiresAuth: false }
    },
    {
        path: '/login',
        name: 'login',
        component: login,
        strict: true,
        meta: { requiresAuth: false },
        props: route => ({
            login_type: route.query.login_type || 'code'
        })
    },
    {
        path: '/login/wx_login',
        name: 'wx_login',
        component: wxLoginCheck,
        meta: { requiresAuth: false },
        props: route => ({
            code: route.query.code,
            state: route.query.state
        })
    },
    {
        path: '/reset_password',
        name: 'reset_password',
        component: resetPassword,
        strict: true,
        meta: { requiresAuth: false }
    },
    {
        path: '/403',
        name: '403',
        component: page403,
        strict: true,
        meta: { requiresAuth: false }
    },
    {
        path: '/',
        name: 'defaultPage',
        component: defaultPage,
        strict: true,
        meta: { requiresAuth: false },
        beforeEnter: (to, from, next) => {
            if (getToken()) {
                router.push({ name: 'user_activity' });
            } else {
                next();
            }
        }
    },
    {
        path: '/:pathMatch(.*)+',
        name: '404',
        component: page404,
        meta: { requiresAuth: false }
    }
];

const router = createRouter({
    end: undefined,
    sensitive: undefined,
    strict: true,
    history: createWebHashHistory(),
    routes
});
router.beforeEach(async (to, from, next) => {
    const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
    const requiresAuthRole = to.matched.some(record => record.meta.requiresAuthRole);
    if (requiresAuth) {
        // 需要鉴权页面
        const currentUserToken = getToken();
        if (!requiresAuthRole) {
            // 不需要特定角色
            if (currentUserToken) {
                // 如果当前有用户登录token
                next();
                return;
            }
            ElMessage.warning('登录已超时，请重新登录！');
            // 保存当前路由信息
            sessionStorage.setItem('redirectRoute', JSON.stringify(to));
            next('login');
        } else {
            // 需要特定角色
            if (currentUserToken) {
                const userinfo = await getInfo();
                const requiredRoles: string[] = to.meta.requiresAuthRole as string[];
                // @ts-ignore
                const overlappingValues = requiredRoles.filter(value => userinfo.user_role?.includes(value));
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
            next('/login');
        }
    } else {
        // 不需要鉴权页面
        next();
    }
});

export default router;
