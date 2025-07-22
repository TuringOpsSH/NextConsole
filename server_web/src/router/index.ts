import {ElMessage} from 'element-plus';
import {createRouter, createWebHashHistory, RouteRecordRaw} from 'vue-router';
import CompanyStructure from '@/components/contacts/company_structure/company_structure.vue';
import ContactsPage from '@/components/contacts/contacts_page.vue';
import friends from '@/components/contacts/friends/friends.vue';
import groupsChat from '@/components/contacts/groups_chat/groups_chat.vue';
import sessionHistory from '@/components/next_console/SessionHistory.vue';
import NextConsoleWelcomeHome from '@/components/next_console/WelcomeHome.vue';
import consoleMain from '@/components/next_console/ConsoleMain.vue';
import messageFlow from '@/components/next_console/messages_flow/MessageFlowMain.vue';
import ResourceCooling from '@/components/resource/resource_cooling/resource_cooling.vue';
import ResourceList from '@/components/resource/resource_list/resource_list.vue';
import ResourceMain from '@/components/resource/resource_main.vue';
import {parseResourceType, parseTagId} from '@/components/resource/resource_shortcut/resource_shortcut';
import ResourceShortcut from '@/components/resource/resource_shortcut/resource_shortcut.vue';
import ResourceViewer from '@/components/resource/resource_view/ResourceViewer.vue';
import MyFavorite from '@/components/resource/resources_favorite/my_resource_favorite.vue';
import ShareResources from '@/components/resource/share_resources/share_resources.vue';
import userInfo from '@/components/user_center/user_info.vue';
import wxLoginCheck from '@/components/user_center/wx_login_check.vue';
import contract from '@/pages/contract.vue';
import defaultPage from '@/pages/defaultPage.vue';
import invitation from '@/pages/invitation.vue';
import login from '@/pages/login.vue';
import nextConsole from '@/pages/next_console.vue';
import Page403 from '@/pages/page_403.vue';
import Page404 from '@/pages/page_404.vue';
import PrivacyPolicy from '@/pages/privacy_policy.vue';
import resetPassword from '@/pages/reset_password.vue';
import unsubscribe from '@/pages/unsubscribe.vue';
import AgentApp from "@/components/app_center/AgentApp.vue";
import AppCenter from '@/pages/AppCenter.vue';
import AgentAppV2 from '@/components/workbenches/AgentApp.vue'
import {getInfo, getToken} from '@/utils/auth';

const routes: RouteRecordRaw[] = [
    {
        path: '/next_console',
        name: 'next_console',
        component: nextConsole,
        strict: true,
        redirect: '/next_console/console/welcome',
        meta: { requiresAuth: false },
        children: [
            {
                path: 'user_info',
                name: 'next_console_user_info',
                component: userInfo,
                meta: { requiresAuth: true },
                strict: true
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
                            sessionCode: route.params.sessionCode,
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
                            sessionSource: route.params.sessionSource,
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
                            resource_id: route.params.resource_id
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
                component: contract,
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
            },
        ]
    },
    {
        path: '/login',
        name: 'login',
        component: login,
        strict: true,
        meta: { requiresAuth: false },
        props: route => ({
            login_type: route.query.login_type || 'code',
            invite_view_id: Number(route.query.invite_view_id) || 0
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
        path: '/contract',
        name: 'contract',
        component: contract,
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
            invite_code: route.query.invite_code,
            invite_type: route.query.invite_type,
            marketing_code: route.query.marketing_code
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
        component: defaultPage,
        strict: true,
        meta: { requiresAuth: true },
        beforeEnter: (to, from, next) => {
            if (getToken()) {
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
    history: createWebHashHistory(),
    routes
});
router.beforeEach(async (to, from, next) => {
    const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
    const isRemoved = to.matched.some(record => record.meta.isRemoved);
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
            next({
                name: 'login',
                query: {
                    ...to.query
                }
            });
        } else {
            // 需要特定角色
            if (currentUserToken) {
                const userinfo = await getInfo();
                const requiredRoles: string[] = to.meta.requiresAuthRole as string[];
                // @ts-ignore
                const overlappingValues = requiredRoles.filter(value => userinfo.user_role.includes(value));
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
