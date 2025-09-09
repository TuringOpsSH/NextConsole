import {ref,reactive} from "vue";
import {task_instance, user_notice_task_info, UserCenter} from "@/types/user-center";
import {
    delete_task,
    get_task_detail,
    init_task, list_task_instance, pause_task, resume_task,
    search_notice_company,
    search_notice_department, search_notice_user, start_task, stop_task,
    update_task
} from "@/api/user-notice";
import router from "@/router";
import {ElMessage} from "element-plus";
import DOMPurify from 'dompurify';
import {Company, Department} from "@/types/contacts";
import {get_notification_data} from "@/components/user-center/user-notice/user_notification";
export const current_notice_task = reactive<user_notice_task_info>({} as user_notice_task_info)
export const current_notice_template_valid = ref(false)
export const previewContent = ref('')
export const area_shortcut = ref([])
export const notice_task_Ref = ref(null)
export const task_loading = ref(false)
export const loading_text = ref('加载中...')
export const notice_task_rules = reactive({
    task_name: [
        { required: true, message: '请输入任务名称', trigger: 'blur' }
    ],
    task_desc: [
        { required: true, message: '请输入任务描述', trigger: 'blur' }
    ],

    notice_template: [
        { validator: valid_template, trigger: 'blur' }
    ],
    notice_params: [
        { validator: valid_notice_params, trigger: 'blur' }
    ],
    notice_type: [
        { required: true, message: '请选择通知类型', trigger: 'blur' }
    ],
    plan_begin_time: [
        { validator: valid_plan_time, trigger: 'blur' }
    ],
    plan_end_time:[
        { validator: valid_plan_time, trigger: 'blur' }
    ],
    run_now: [
        { validator: valid_right_now, message: '请选择是否立即执行', trigger: 'blur' }
    ],
})


export const area_target_companies = ref<Company[]>([])
export const area_target_departments = ref<Department[]>([])
export const area_target_users = ref<UserCenter[]>([])

export const area_company_options = ref<Company[]>([])
export const area_department_options = ref<Department[]>([])
export const area_user_options = ref<UserCenter[]>([])
export const refresh_interval = ref(null)
export const current_task_instances = ref<task_instance[]>([])
export async function init_current_task (task_id:number){
    if (task_id){
        // @ts-ignore
        let res = await get_task_detail({
            task_id: task_id
        })
        if (!res.error_status){
            Object.assign(current_notice_task, res.result)
        }
        if (current_notice_task.task_status != "新建中"){
            let instances = await list_task_instance({
                task_id: task_id,
                page_num: 1,
                page_size: current_notice_task.task_instance_total
            })
            if (!instances.error_status){
                current_task_instances.value = instances.result.data
            }
        } else {
            current_task_instances.value = []
        }
    }
    else {
        let res = await init_task({})
        if (!res.error_status){
            Object.assign(current_notice_task, res.result)
            router.push({
                name: 'user_notice_detail',
                query: {
                    task_id: current_notice_task.id
                }
            })
        }
    }
    check_html_valid()
    // 获取快捷区域
    area_shortcut.value = []
    if (current_notice_task.notice_params.all_user ){
        area_shortcut.value.push('all_user')
    }
    if (current_notice_task.notice_params.all_company_user){
        area_shortcut.value.push('all_company_user')
    }
    if (current_notice_task.notice_params.all_person_user){
        area_shortcut.value.push('all_person_user')
    }
    if (current_notice_task.notice_params.all_subscribe_email){
        area_shortcut.value.push('all_subscribe_email')
    }
    if (current_notice_task.notice_params.target_company){
        area_shortcut.value.push('target_company')
    }
    if (current_notice_task.notice_params.target_department){
        area_shortcut.value.push('target_department')
    }
    if (current_notice_task.notice_params.target_user){
        area_shortcut.value.push('target_user')
    }
    if (current_notice_task.notice_params.target_company){
        area_target_companies.value = current_notice_task.notice_params.target_companies
        area_company_options.value = current_notice_task.notice_params.target_companies
    }
    if (current_notice_task.notice_params.target_department){
        area_target_departments.value = current_notice_task.notice_params.target_departments
        area_department_options.value = current_notice_task.notice_params.target_departments

    }
    if (current_notice_task.notice_params.target_user){
        area_target_users.value = current_notice_task.notice_params.target_users
        area_user_options.value = current_notice_task.notice_params.target_users
    }
}

export async function update_current_task(){
    let valid_res = await notice_task_Ref.value?.validate()
    if (!valid_res){
        return
    }
    let params = {
        task_id: current_notice_task.id,
        task_name: current_notice_task.task_name,
        task_desc: current_notice_task.task_desc,
        plan_begin_time: current_notice_task.plan_begin_time,
        plan_finish_time: current_notice_task.plan_finish_time,
        notice_template: current_notice_task.notice_template,
        notice_params: current_notice_task.notice_params,
        notice_type: current_notice_task.notice_type,
        run_now: current_notice_task.run_now,
        batch_size: current_notice_task.task_instance_batch_size
    }
    task_loading.value = true
    loading_text.value = '保存中...'
    let res = await update_task(params)
    if (!res.error_status){
        ElMessage.success({
            message: "保存成功",
            duration: 6000
        })
        Object.assign(current_notice_task, res.result)
    }
    task_loading.value = false
    router.push({
        name: 'user_notice_detail',
        query: {
            task_id: current_notice_task.id
        }
    })

}

export function check_html_valid(){
    try {
        const sanitizedContent =  DOMPurify.sanitize(current_notice_task.notice_template)
        if (!sanitizedContent) {
            throw new Error('内容为空或不合法');
        }
        previewContent.value = sanitizedContent
        current_notice_template_valid.value = true
    } catch (e) {

        current_notice_template_valid.value = false
    }

}

export function valid_plan_time(rule: any, value: any, callback: any){

    if (current_notice_task.plan_begin_time && current_notice_task.plan_finish_time){
        if (current_notice_task.plan_begin_time > current_notice_task.plan_finish_time){
            return callback(new Error('计划开始时间不能大于计划结束时间'))
        }
    }
    if (!value && !current_notice_task.run_now){
        return callback(new Error('请选择是否立即执行或者计划开始时间'))
    }
    callback()
}

export function valid_right_now(rule: any, value: any, callback: any){
    if (!value && !current_notice_task.plan_begin_time){
        return callback(new Error('请选择是否立即执行或者计划开始时间'))
    }
    callback()
}

export function valid_template(rule: any, value: any, callback: any){
    if (!value){
        return callback(new Error('请输入通知内容'))
    }
    try {
        const sanitizedContent =  DOMPurify.sanitize(current_notice_task.notice_template)
        if (!sanitizedContent) {
            throw new Error('内容为空或不合法');
        }
        previewContent.value = sanitizedContent
        current_notice_template_valid.value = true
    } catch (e) {

        current_notice_template_valid.value = false
        return callback(new Error('请输入正确的通知内容'))
    }
    callback()
}

export function valid_notice_params(rule: any, value: any, callback: any){
    if (!value){
        return callback(new Error('请选择通知范围'))
    }
    // 不能全为空
    if (!value.all_user && !value.all_company_user
        && !value.all_person_user && !value.all_subscribe_email
        && !value.target_companies?.length && !value.target_departments?.length && !value.target_users?.length){
        return callback(new Error('请选择通知范围'))
    }
    callback()
}


export async function search_company(val:string){
    if (!val){
        return
    }
    let params = {
        keyword: val
    }
    let res = await search_notice_company(params)
    if (!res.error_status){
        area_company_options.value = res.result.data
    }

}

export function handle_notice_company_change(val:any){
    current_notice_task.notice_params.target_companies = val
}
export function handle_notice_department_change(val:any){
    current_notice_task.notice_params.target_departments = val
}
export function handle_notice_user_change(val:any){
    current_notice_task.notice_params.target_users = val

}
export async function search_department(val:string){
    if (!val){
        return
    }
    let params = {
        keyword: val
    }
    let res = await search_notice_department(params)
    if (!res.error_status){
        area_department_options.value = res.result.data
    }

}
export async function search_user(val:string){
    if (!val){
        return
    }
    let params = {
        keyword: val
    }
    let res = await search_notice_user(params)
    if (!res.error_status){
        area_user_options.value = res.result.data
    }
}
export function handle_notice_area_change(val:any){
    current_notice_task.notice_params.all_user = !!val.includes('all_user');
    current_notice_task.notice_params.all_company_user = !!val.includes('all_company_user');
    current_notice_task.notice_params.all_person_user = !!val.includes('all_person_user');
    current_notice_task.notice_params.all_subscribe_email = !!val.includes('all_subscribe_email');
    current_notice_task.notice_params.target_company = !!val.includes('target_company');
    current_notice_task.notice_params.target_department = !!val.includes('target_department');
    current_notice_task.notice_params.target_user = !!val.includes('target_user');
}
export async function delete_current_task(){
    if (current_notice_task.task_status == "执行中") {
        ElMessage.warning({
            message: '运行中的任务不能删除！请先暂停或者终止',
            duration: 5000
        })
        return
    }
    let res = await delete_task({
        task_id: current_notice_task.id,

    })
    if(!res.error_status){
        ElMessage.success({
            message: '删除成功',
            duration: 3000
        })
        await get_notification_data()
        current_notice_task.id = null
    }
    await router.push({'name':'user_notification_list'})
}

export async function start_notice_task(){
    await update_current_task()
    let res = await notice_task_Ref.value?.validate()
    if (!res){
        return
    }
    check_html_valid()
    if (!current_notice_template_valid.value){
        return
    }
    task_loading.value = true
    loading_text.value = '任务提交中...'
    let params = {
        task_id: current_notice_task.id
    }
    let task_res = await start_task(params)
    if (!res.error_status){
        Object.assign(current_notice_task, task_res.result)
    }
    ElMessage.success({
        message: '任务提交成功！',
        duration: 3000
    })
    task_loading.value = false
    // 开始刷新任务详情
    if (refresh_interval.value){
        clearInterval(refresh_interval.value)
    }
    refresh_interval.value = setInterval(refresh_task_detail, 2000)
}

export async function refresh_task_detail(){
    if (current_notice_task?.task_status != "执行中" && refresh_interval.value){
        clearInterval(refresh_interval.value)
        return
    }
    let res = await get_task_detail({
        task_id: current_notice_task.id
    })
    if (!res.error_status){
        current_notice_task.task_status = res.result.task_status
        current_notice_task.task_progress = res.result.task_progress
        current_notice_task.begin_time = res.result.begin_time
        current_notice_task.finish_time = res.result.finish_time
        current_notice_task.task_instance_total = res.result.task_instance_total
        current_notice_task.task_instance_success = res.result.task_instance_success
        current_notice_task.task_instance_failed = res.result.task_instance_failed
    }
}

export async function pause_notice_task(){
    let res = await pause_task({
        task_id: current_notice_task.id,
    })
    if (!res.error_status){
        if (res.error_message){
            ElMessage.warning({
                message: res.error_message,
                duration: 3000
            })
        }
        Object.assign(current_notice_task, res.result)
        if (refresh_interval.value){
            clearInterval(refresh_interval.value)
        }
    }
}
export async function resume_notice_task(){
    let res = await resume_task({
        task_id: current_notice_task.id,
    })
    if (!res.error_status){
        Object.assign(current_notice_task, res.result)
        if (refresh_interval.value){
            clearInterval(refresh_interval.value)
        }
        refresh_interval.value = setInterval(refresh_task_detail, 2000)
    }
}
export async function stop_notice_task(){
    let res = await stop_task({
        task_id: current_notice_task.id,
    })
    if (!res.error_status){
        Object.assign(current_notice_task, res.result)
    }
}

