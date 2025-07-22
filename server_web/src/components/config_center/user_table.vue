<script setup lang="ts" >
// 分页组件参数
import {onMounted, reactive, ref, watch} from "vue";
// 修改用户密码
import {ElNotification, FormInstance, FormRules, UploadInstance, UploadUserFile} from 'element-plus'
import {ElMessage, ElTable, genFileId, UploadProps, UploadRawFile} from "element-plus";
import {create_user_by_excel, delete_user, search_user, update_user} from '../../api/user_center.js';
// 新增用户表单
import {UploadFilled} from '@element-plus/icons-vue'
import Cookies from "js-cookie";
import {api} from '../../api/user_center.js'
const todo_warning = () => {
    ElMessage({
        message: '此功能开发中，敬请期待',
        type: 'warning',
    })
}


// 分页组件函数
const currentPage = ref(1)
const pageSize = ref(50)
const total = ref(500)
const pageSizer = ref([10, 50, 100, 500, 1000])
const small = ref(false)
const background = ref(true)
const hideOne = ref(false)
const disabled = ref(false)
const pagerCount = ref(9)
const selectedUser = ref([])
const user_cnt = ref(18)
const handleSelectionChange = (val) => {
    const selectedID = ref([])
    val.forEach((user, index) => {
        // 在这里你可以访问到数组中的每一个对象document，并使用它的属性
        selectedID.value.push(user.id);

    })
    selectedUser.value = selectedID.value;
}
const handleSizeChange = (val: number) => {
    pageSize.value = val
    searchUsers()
}
const handleCurrentChange = (val: number) => {
    currentPage.value = val
    searchUsers()
}
// 获取用户数据
const tableData = ref([])
const searchCondition = reactive({
    "page_size": 100,
    "page_num": 1,
    "user_id": [],
    "user_gender": [],
    "user_department": [],
    "user_last_login_time": [],
    "user_create_time": [],
    "user_age": "",
    "user_status": [],
    "user_name": "",
    "user_email": "",
    "user_phone": ""
})
async function searchUsers() {
    let data = await search_user({
        "page_size": pageSize.value,
        "page_num": currentPage.value,
        "user_id": [],
        "user_gender": [],
        "user_department": [],
        "user_last_login_time": [],
        "user_create_time": [],
        "user_age": "",
        "user_status": [],
        "user_name": "",
        "user_email": "",
        "user_phone": ""
    });
    tableData.value = data.result.data;
    total.value = data.result.cnt;
    user_cnt.value = data.result.cnt;

}
// 新增用户

const dialog_v_user_add_model = ref(false)
const dialog_v_user_add_model_excel = ref(false)
const user_excel_file_name = ref("")
const user_excel_file_size = ref("")
const user_excel_file_flag = ref(false)
const user_excel_file_progress = ref(0)
const user_excel_file_status = ref("")
const user_excel_file_result = ref("")
const user_add_model = ref(0)
const uploadRef = ref<UploadInstance>()
const user_excel_file = ref<UploadUserFile[]>()
const user_excel_file_result_str = ref("")
watch(user_excel_file_result, (newVal) => {
    user_excel_file_result_str.value = JSON.stringify(newVal, null, 2);
});
async function downloadUserTemplate(){
      let data = create_user_by_excel(
          {},"get"
      )
    console.log(data)

}
function getToken(){
    const token = Cookies.get('next_console_token');
    return {"Authorization": "Bearer " + token}
}
function getFileInfo(file) {
    user_excel_file_name.value=file.name
    user_excel_file_size.value=(file.size / 1024).toFixed(2) + "KB"
    user_excel_file_flag.value=true
}

function uploadUserExcelFile(){
    if (typeof user_excel_file.value === 'undefined'){
      ElNotification.warning({
        title: "系统消息",
        message: '请上传文件' ,
        duration: 3000
      })
        return false
    }
    uploadRef.value!.submit()
    // uploadRef.value.clearFiles()


}
function updateUserResult(response, file, fileList) {
    // 在这里处理服务器返回的结果

    user_excel_file_name.value=""
    user_excel_file_size.value=""
    user_excel_file_flag.value=false
    user_excel_file_progress.value = response.result.finished_cnt / response.result.total_cnt * 100
    if (user_excel_file_progress.value == 100) {
        user_excel_file_status.value = "success"

    }
    if (user_excel_file_progress.value <60 && user_excel_file_progress.value >= 30) {
        user_excel_file_status.value = "warning"

    }
    if (user_excel_file_progress.value <30) {
        user_excel_file_status.value = "exception"
    }
    user_excel_file_result.value = response.result.trace
    uploadRef.value.clearFiles()
    if (response.error_status) {
        user_excel_file_result.value = response.error_message
    }
    searchUsers()
}
// 修改用户密码
interface RuleForm {
    new_password: string
    new_password_confirm: string
}
const dialog_v_user_update_password = ref(false)
const current_user = ref()
const user_password_form_ref = ref<FormInstance>()
const user_password = reactive<RuleForm>({
    new_password: '',
    new_password_confirm: ''
})
const validatePass2 = (rule: any, value: any, callback: any) => {
    if (value === '') {
        return callback(new Error('请再次输入密码'));
    } else if (value !== user_password.new_password) {
        callback(new Error('两次输入密码不一致!'));
    } else {
        return callback();
    }
}
const user_password_rules = reactive<FormRules<RuleForm>>(
    {
        new_password: [
            {required: true, message: '请输入新密码', trigger: 'blur'},
            {min: 6, max: 20, message: '长度在 6 到 20 个字符', trigger: 'blur'}
        ],
        new_password_confirm: [
            {required: true, message: '请再次输入密码', trigger: 'blur'},
            {min: 6, max: 20, message: '长度在 6 到 20 个字符', trigger: 'blur'},
            {min: 6, max: 20, message: '长度在 6 到 20 个字符', trigger: 'blur'},
            {validator: validatePass2, trigger: 'blur'}
        ]
    }
)
async function updateUserPassWd(formEl: FormInstance) {
    // 先校验数据
    if (!formEl) return
    await formEl.validate((valid, fields) => {
        if (valid) {
            // console.log(user_password.new_password,user_password.new_password_confirm)
            update_user(
                {
                    "user_id": current_user.value,
                    "user_password": user_password.new_password
                }
            ).then(
                (data) => {
                    if (data.error_code == 0) {
                        ElMessage({
                            message: '修改成功!',
                            type: 'success',
                        })
                        dialog_v_user_update_password.value = false
                    } else {
                        ElMessage({
                            message: '修改失败!',
                            type: 'error',
                        })
                    }
                }
            )


        }

    })
    await searchUsers()
}
const resetForm = (formEl: FormInstance) => {
    formEl.resetFields()
}


// 删除用户
const dialog_v_user_delete_confirm = ref(false)
async function deleteUsers() {
    let data = await delete_user({
        "user_ids": [current_user.value],

    });
    if (data.error_code == 0) {
        ElMessage({
            message: '删除成功!',
            type: 'success',
        })
    } else {
        ElMessage({
            message: '删除失败!',
            type: 'error',
        })
    }
    dialog_v_user_delete_confirm.value = false
    await searchUsers()
}

// 初始化流程
onMounted(async () => {
    await searchUsers()

})

</script>

<template>
    <div class="user_table">
        <div class="header">
            <el-row>
                <el-col :span="8">
                    <el-row :span="24">
                        <el-col :span="5">
                            <el-text class="user_table_title"> 用户列表</el-text>
                        </el-col>
                        <el-col :span="4">
                            <el-tag effect="light" round>{{ user_cnt }}条</el-tag>
                        </el-col>

                    </el-row>


                </el-col>
                <el-col :span="12">
                    <div style="flex-grow: 1"></div>
                </el-col>
                <el-col :span="4">
                    <el-button type="primary" color="#1570EF" size="large" @click="dialog_v_user_add_model = true">
                        <svg width="20" height="18" viewBox="0 0 20 18" fill="none" xmlns="http://www.w3.org/2000/svg"
                             style="padding: 6px">
                            <path d="M9.99999 11.9167H6.24999C5.08702 11.9167 4.50554 11.9167 4.03237 12.0602C2.96704 12.3834 2.13336 13.217 1.81019 14.2824C1.66666 14.7555 1.66666 15.337 1.66666 16.5M15.8333 16.5V11.5M13.3333 14H18.3333M12.0833 5.25C12.0833 7.32107 10.4044 9 8.33332 9C6.26226 9 4.58332 7.32107 4.58332 5.25C4.58332 3.17893 6.26226 1.5 8.33332 1.5C10.4044 1.5 12.0833 3.17893 12.0833 5.25Z"
                                  stroke="white" stroke-width="1.66667" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>

                        <el-text class="user_add_bot">新增用户</el-text>
                    </el-button>
                </el-col>
            </el-row>


        </div>
        <div class="body">
            <el-table
                    :data="tableData"
                    :default-sort="{ prop: 'date', order: 'descending' }"
                    style="width: 100%;height: 95%"
                    @selection-change="handleSelectionChange"
                    max-height="790"
            >
                <el-table-column type="selection" />
                <el-table-column property="user_name" label="用户名称" />
                <el-table-column property="user_profile" label="头像"  >
                    <template #default="scope">
                        <el-button link type="primary" size="small" @click="">
                            <el-avatar :src="scope.row.user_profile" size="default" fit="cover"
                                       style="background: #D1E9FF"></el-avatar>
                        </el-button>
                        <el-button link type="primary" size="small" @click="">
                            <svg width="19" height="19" viewBox="0 0 19 19" fill="none"
                                 xmlns="http://www.w3.org/2000/svg">
                                <path d="M14 8.33326L10.6667 4.99993M1.08331 17.9166L3.90362 17.6032C4.24819 17.5649 4.42048 17.5458 4.58152 17.4937C4.72439 17.4474 4.86035 17.3821 4.98572 17.2994C5.12702 17.2062 5.2496 17.0836 5.49475 16.8385L16.5 5.83326C17.4205 4.91279 17.4205 3.4204 16.5 2.49993C15.5795 1.57945 14.0871 1.57945 13.1667 2.49992L2.16142 13.5052C1.91627 13.7503 1.79369 13.8729 1.70051 14.0142C1.61784 14.1396 1.55249 14.2755 1.50624 14.4184C1.45411 14.5794 1.43497 14.7517 1.39668 15.0963L1.08331 17.9166Z"
                                      stroke="#475467" stroke-width="1.66667" stroke-linecap="round"
                                      stroke-linejoin="round"/>
                            </svg>
                        </el-button>
                    </template>

                </el-table-column>
                <el-table-column property="user_role" label="角色"  >
                    <template #default="scope">
                        <el-button link type="primary" size="small" @click="">
                            <el-tag effect="light" round>{{ scope.row.user_role }}</el-tag>
                        </el-button>
                        <el-button link type="primary" size="small" @click="">
                            <svg width="19" height="19" viewBox="0 0 19 19" fill="none"
                                 xmlns="http://www.w3.org/2000/svg">
                                <path d="M14 8.33326L10.6667 4.99993M1.08331 17.9166L3.90362 17.6032C4.24819 17.5649 4.42048 17.5458 4.58152 17.4937C4.72439 17.4474 4.86035 17.3821 4.98572 17.2994C5.12702 17.2062 5.2496 17.0836 5.49475 16.8385L16.5 5.83326C17.4205 4.91279 17.4205 3.4204 16.5 2.49993C15.5795 1.57945 14.0871 1.57945 13.1667 2.49992L2.16142 13.5052C1.91627 13.7503 1.79369 13.8729 1.70051 14.0142C1.61784 14.1396 1.55249 14.2755 1.50624 14.4184C1.45411 14.5794 1.43497 14.7517 1.39668 15.0963L1.08331 17.9166Z"
                                      stroke="#475467" stroke-width="1.66667" stroke-linecap="round"
                                      stroke-linejoin="round"/>
                            </svg>
                        </el-button>
                    </template>
                </el-table-column>
                <el-table-column property="user_department" label="公司" sortable  />
                <el-table-column property="user_create_time" label="注册时间" sortable  />
                <el-table-column property="user_email" label="邮箱" sortable />
                <el-table-column fixed="right" label="管理"  >
                    <template #default="scope">
                        <el-button link type="primary" size="small"
                                   @click="dialog_v_user_update_password = true;current_user=scope.row.user_id">
                            <svg width="20" height="10" viewBox="0 0 20 10" fill="none"
                                 xmlns="http://www.w3.org/2000/svg">
                                <path d="M9.99999 5.00016H10.0042M14.1667 5.00016H14.1708M5.83332 5.00016H5.83749M4.33332 0.833496H15.6667C16.6001 0.833496 17.0668 0.833496 17.4233 1.01515C17.7369 1.17494 17.9919 1.42991 18.1517 1.74351C18.3333 2.10003 18.3333 2.56674 18.3333 3.50016V6.50016C18.3333 7.43358 18.3333 7.90029 18.1517 8.25681C17.9919 8.57042 17.7369 8.82538 17.4233 8.98517C17.0668 9.16683 16.6001 9.16683 15.6667 9.16683H4.33332C3.3999 9.16683 2.93319 9.16683 2.57667 8.98517C2.26307 8.82538 2.0081 8.57042 1.84831 8.25681C1.66666 7.90029 1.66666 7.43358 1.66666 6.50016V3.50016C1.66666 2.56674 1.66666 2.10003 1.84831 1.74351C2.0081 1.42991 2.26307 1.17494 2.57667 1.01515C2.93319 0.833496 3.3999 0.833496 4.33332 0.833496ZM10.2083 5.00016C10.2083 5.11522 10.115 5.2085 9.99999 5.2085C9.88493 5.2085 9.79166 5.11522 9.79166 5.00016C9.79166 4.8851 9.88493 4.79183 9.99999 4.79183C10.115 4.79183 10.2083 4.8851 10.2083 5.00016ZM14.375 5.00016C14.375 5.11522 14.2817 5.2085 14.1667 5.2085C14.0516 5.2085 13.9583 5.11522 13.9583 5.00016C13.9583 4.8851 14.0516 4.79183 14.1667 4.79183C14.2817 4.79183 14.375 4.8851 14.375 5.00016ZM6.04166 5.00016C6.04166 5.11522 5.94838 5.2085 5.83332 5.2085C5.71826 5.2085 5.62499 5.11522 5.62499 5.00016C5.62499 4.8851 5.71826 4.79183 5.83332 4.79183C5.94838 4.79183 6.04166 4.8851 6.04166 5.00016Z"
                                      stroke="#475467" stroke-width="1.66667" stroke-linecap="round"
                                      stroke-linejoin="round"/>
                            </svg>
                        </el-button>
                        <el-button link type="primary" size="small"
                                   @click="dialog_v_user_delete_confirm = true;current_user=scope.row.user_id ">
                            <svg width="18" height="20" viewBox="0 0 18 20" fill="none"
                                 xmlns="http://www.w3.org/2000/svg">
                                <path d="M12.3333 4.99984V4.33317C12.3333 3.39975 12.3333 2.93304 12.1517 2.57652C11.9919 2.26292 11.7369 2.00795 11.4233 1.84816C11.0668 1.6665 10.6001 1.6665 9.66667 1.6665H8.33333C7.39991 1.6665 6.9332 1.6665 6.57668 1.84816C6.26308 2.00795 6.00811 2.26292 5.84832 2.57652C5.66667 2.93304 5.66667 3.39975 5.66667 4.33317V4.99984M7.33333 9.58317V13.7498M10.6667 9.58317V13.7498M1.5 4.99984H16.5M14.8333 4.99984V14.3332C14.8333 15.7333 14.8333 16.4334 14.5608 16.9681C14.3212 17.4386 13.9387 17.821 13.4683 18.0607C12.9335 18.3332 12.2335 18.3332 10.8333 18.3332H7.16667C5.76654 18.3332 5.06647 18.3332 4.53169 18.0607C4.06129 17.821 3.67883 17.4386 3.43915 16.9681C3.16667 16.4334 3.16667 15.7333 3.16667 14.3332V4.99984"
                                      stroke="#475467" stroke-width="1.66667" stroke-linecap="round"
                                      stroke-linejoin="round"/>
                            </svg>


                        </el-button>

                    </template>
                </el-table-column>
            </el-table>
            <el-dialog v-model="dialog_v_user_add_model"
                       class="user_add_form"
                       :show-close="false"
                       width="480px" top="30vh"
            >
                <template #header="{ close, titleId, titleClass }">
                    <div class="user-add-form-header">
                        <div>
                            <h4 :id="titleId" :class="titleClass">新增用户</h4>
                        </div>
                        <el-button @click="close">
                            <svg width="14" height="14" viewBox="0 0 14 14" fill="none"
                                 xmlns="http://www.w3.org/2000/svg">
                                <path d="M13 1L1 13M1 1L13 13" stroke="#667085" stroke-width="2" stroke-linecap="round"
                                      stroke-linejoin="round"/>
                            </svg>
                        </el-button>
                    </div>
                </template>
                <div>
                    <el-radio-group v-model="user_add_model" text-color="#175CD3">
                        <el-radio label=1 border class="user_add_model_batch">
                            <el-row>
                                <el-col :span="4">
                                    <el-avatar class="file-mode-icon" fit="contain" size="large"
                                               src="images/file-mode-icon.svg">


                                    </el-avatar>
                                </el-col>
                                <el-col :span="20">
                                    <el-row>
                                        <el-col>
                                            <el-text>文件批量导入</el-text>
                                        </el-col>
                                        <el-col>
                                            <el-text> 通过上传文件进行新增</el-text>
                                        </el-col>
                                    </el-row>


                                </el-col>
                            </el-row>


                        </el-radio>
                        <el-radio label=2 border class="user_add_model_batch" disabled>
                            <el-row>
                                <el-col :span="4">
                                    <el-avatar class="file-mode-icon" fit="fill" size="large">
                                        <svg width="16" height="16" viewBox="0 0 16 16" fill="none"
                                             xmlns="http://www.w3.org/2000/svg">
                                            <path
                                                d="M11.6667 11.3333H4.33333M11.6667 8.66667H4.33333M2 6H14M5.2 2H10.8C11.9201 2 12.4802 2 12.908 2.21799C13.2843 2.40973 13.5903 2.71569 13.782 3.09202C14 3.51984 14 4.0799 14 5.2V10.8C14 11.9201 14 12.4802 13.782 12.908C13.5903 13.2843 13.2843 13.5903 12.908 13.782C12.4802 14 11.9201 14 10.8 14H5.2C4.07989 14 3.51984 14 3.09202 13.782C2.71569 13.5903 2.40973 13.2843 2.21799 12.908C2 12.4802 2 11.9201 2 10.8V5.2C2 4.07989 2 3.51984 2.21799 3.09202C2.40973 2.71569 2.71569 2.40973 3.09202 2.21799C3.51984 2 4.0799 2 5.2 2Z"
                                                stroke="#1570EF" stroke-width="1.33333" stroke-linecap="round"
                                                stroke-linejoin="round"/>
                                        </svg>

                                    </el-avatar>
                                </el-col>
                                <el-col :span="20">
                                    <el-row>
                                        <el-col>
                                            <el-text>前端表单创建</el-text>
                                        </el-col>
                                        <el-col>
                                            <el-text> 通过前端表单进行新增</el-text>
                                        </el-col>
                                    </el-row>
                                </el-col>
                            </el-row>


                        </el-radio>
                    </el-radio-group>


                </div>
                <template #footer="{close}">
                    <div class="user-add-form-header">
                        <el-button type="primary"
                                   @click="dialog_v_user_add_model = false"
                                   class="user_button_passwd"
                                   color="white">
                            <el-text class="user_del_font" style="color:black;">
                                取 消
                            </el-text>
                        </el-button>
                        <el-button type="danger"
                                   @click="dialog_v_user_add_model = false;dialog_v_user_add_model_excel=true"
                                   class="user_button_passwd" color="#1570EF" style="border: #1570EF">
                            <el-text class="user_del_font">
                                确 认
                            </el-text>
                        </el-button>
                    </div>
                </template>
            </el-dialog>
            <el-dialog v-model="dialog_v_user_add_model_excel" class="user_add_form"
                       :show-close="false"
                       width="480px" top="5vh"
                       destroy-on-close
            >
                <template #header="{ close, titleId, titleClass }">
                    <div class="user-add-form-header">
                        <div>
                            <h4 :id="titleId" :class="titleClass">上传excel用户文件</h4>
                        </div>
                        <el-button @click="close">
                            <svg width="14" height="14" viewBox="0 0 14 14" fill="none"
                                 xmlns="http://www.w3.org/2000/svg">
                                <path d="M13 1L1 13M1 1L13 13" stroke="#667085" stroke-width="2" stroke-linecap="round"
                                      stroke-linejoin="round"/>
                            </svg>
                        </el-button>
                    </div>
                </template>
                <el-row>
                    <el-col :span="24">
                        <el-button class="user-template-download" @click="downloadUserTemplate">
                            <el-icon >
                                <svg width="18" height="18" viewBox="0 0 18 18" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M16.5 11.5V12.5C16.5 13.9001 16.5 14.6002 16.2275 15.135C15.9878 15.6054 15.6054 15.9878 15.135 16.2275C14.6002 16.5 13.9001 16.5 12.5 16.5H5.5C4.09987 16.5 3.3998 16.5 2.86502 16.2275C2.39462 15.9878 2.01217 15.6054 1.77248 15.135C1.5 14.6002 1.5 13.9001 1.5 12.5V11.5M13.1667 7.33333L9 11.5M9 11.5L4.83333 7.33333M9 11.5V1.5" stroke="#344054" stroke-width="1.66667" stroke-linecap="round" stroke-linejoin="round"/>
                                </svg>

                            </el-icon>
                            <el-text>
                                下载用户模板文件
                            </el-text>
                        </el-button>
                    </el-col>
                    <el-col :span="24">
                        <div class="user_upload_box">
                            <el-upload
                                class="upload-demo"
                                drag
                                :action="api.create_user_by_excel"
                                method="post"
                                :auto-upload="false"
                                :limit="1"
                                :show-file-list="false"
                                :on-change="getFileInfo"
                                :headers="getToken()"
                                ref="uploadRef"
                                with-credentials
                                v-model:file-list="user_excel_file"
                                :on-success="updateUserResult"
                            >
                                <el-icon class="el-icon--upload"><upload-filled /></el-icon>
                                <div class="el-upload__text">
                                    <em>点击上传</em>或者<em>拖拽文件到此处上传</em>
                                    <br>
                                    <el-text>支持xlsx文件</el-text>
                                </div>

                            </el-upload>
                        </div>

                    </el-col>
                    <el-col :span="24">
                        <div class="user_upload_status_box">
                            <el-row style="width: 100%">
                                <el-col :span="3" class="upload-result" >
                                    <svg width="40" height="40" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
                                        <path d="M7.75 4C7.75 2.20508 9.20508 0.75 11 0.75H27C27.1212 0.75 27.2375 0.798159 27.3232 0.883885L38.1161 11.6768C38.2018 11.7625 38.25 11.8788 38.25 12V36C38.25 37.7949 36.7949 39.25 35 39.25H11C9.20507 39.25 7.75 37.7949 7.75 36V4Z" fill="white" stroke="#D0D5DD" stroke-width="1.5"/>
                                        <path d="M27 0.5V8C27 10.2091 28.7909 12 31 12H38.5" stroke="#D0D5DD" stroke-width="1.5"/>
                                        <rect x="1" y="18" width="28" height="16" rx="2" fill="#099250"/>
                                        <path d="M11.2726 25.2734H9.71724C9.68883 25.0722 9.63083 24.8935 9.54324 24.7372C9.45564 24.5786 9.34319 24.4437 9.20588 24.3324C9.06857 24.2211 8.90995 24.1359 8.73002 24.0767C8.55247 24.0175 8.35952 23.9879 8.15119 23.9879C7.77477 23.9879 7.44688 24.0814 7.16752 24.2685C6.88817 24.4531 6.67155 24.723 6.51767 25.0781C6.36378 25.4309 6.28684 25.8594 6.28684 26.3636C6.28684 26.8821 6.36378 27.3177 6.51767 27.6705C6.67392 28.0232 6.89172 28.2895 7.17108 28.4695C7.45043 28.6494 7.77359 28.7393 8.14054 28.7393C8.3465 28.7393 8.53708 28.7121 8.71227 28.6577C8.88983 28.6032 9.04726 28.5239 9.18457 28.4197C9.32188 28.3132 9.43552 28.1842 9.52548 28.0327C9.61781 27.8812 9.68173 27.7083 9.71724 27.5142L11.2726 27.5213C11.2324 27.8551 11.1318 28.1771 10.9708 28.4872C10.8122 28.795 10.5979 29.0708 10.328 29.3146C10.0605 29.5561 9.74092 29.7479 9.36923 29.8899C8.99991 30.0296 8.58206 30.0994 8.11568 30.0994C7.467 30.0994 6.88699 29.9527 6.37562 29.6591C5.86663 29.3655 5.46416 28.9406 5.16824 28.3842C4.87467 27.8279 4.72789 27.1544 4.72789 26.3636C4.72789 25.5705 4.87704 24.8958 5.17534 24.3395C5.47363 23.7831 5.87846 23.3594 6.38983 23.0682C6.90119 22.7746 7.47647 22.6278 8.11568 22.6278C8.53708 22.6278 8.9277 22.687 9.28755 22.8054C9.64977 22.9238 9.97056 23.0966 10.2499 23.3239C10.5293 23.5488 10.7565 23.8246 10.9317 24.1513C11.1093 24.478 11.2229 24.852 11.2726 25.2734ZM16.3206 24.8189C16.2922 24.5324 16.1702 24.3099 15.9548 24.1513C15.7394 23.9927 15.447 23.9134 15.0777 23.9134C14.8267 23.9134 14.6148 23.9489 14.442 24.0199C14.2692 24.0885 14.1366 24.1844 14.0443 24.3075C13.9543 24.4306 13.9094 24.5703 13.9094 24.7266C13.9046 24.8568 13.9318 24.9704 13.991 25.0675C14.0526 25.1645 14.1366 25.2486 14.2432 25.3196C14.3497 25.3883 14.4728 25.4486 14.6125 25.5007C14.7522 25.5504 14.9013 25.593 15.0599 25.6286L15.7133 25.7848C16.0306 25.8558 16.3218 25.9505 16.5869 26.0689C16.8521 26.1873 17.0817 26.3329 17.2758 26.5057C17.47 26.6785 17.6203 26.8821 17.7268 27.1165C17.8357 27.3509 17.8914 27.6196 17.8937 27.9226C17.8914 28.3677 17.7777 28.7536 17.5528 29.0803C17.3303 29.4046 17.0083 29.6567 16.5869 29.8366C16.1679 30.0142 15.6624 30.103 15.0706 30.103C14.4835 30.103 13.9721 30.013 13.5365 29.8331C13.1032 29.6532 12.7647 29.3868 12.5209 29.0341C12.2794 28.679 12.1527 28.2398 12.1409 27.7166H13.6288C13.6454 27.9605 13.7152 28.1641 13.8383 28.3274C13.9638 28.4884 14.1307 28.6103 14.339 28.6932C14.5497 28.7737 14.7877 28.8139 15.0528 28.8139C15.3132 28.8139 15.5393 28.776 15.7311 28.7003C15.9252 28.6245 16.0756 28.5192 16.1821 28.3842C16.2886 28.2493 16.3419 28.0942 16.3419 27.919C16.3419 27.7557 16.2934 27.6184 16.1963 27.5071C16.1016 27.3958 15.9619 27.3011 15.7773 27.223C15.595 27.1449 15.3712 27.0739 15.1061 27.0099L14.3142 26.8111C13.701 26.6619 13.2169 26.4287 12.8618 26.1115C12.5067 25.7943 12.3303 25.367 12.3327 24.8295C12.3303 24.3892 12.4475 24.0045 12.6842 23.6754C12.9233 23.3464 13.2512 23.0895 13.6679 22.9048C14.0845 22.7202 14.558 22.6278 15.0883 22.6278C15.6281 22.6278 16.0992 22.7202 16.5017 22.9048C16.9065 23.0895 17.2214 23.3464 17.4463 23.6754C17.6712 24.0045 17.7872 24.3857 17.7943 24.8189H16.3206ZM20.2419 22.7273L21.9997 28.2528H22.0672L23.8286 22.7273H25.5331L23.026 30H21.0445L18.5338 22.7273H20.2419Z" fill="white"/>
                                    </svg>
                                </el-col>
                                <el-col :span="1"></el-col>
                                <el-col :span="19">
                                    <el-row style="width: 100%;">
                                            <div style="width: 100%;">
                                                <el-row style="width: 100%;">
                                                    <el-col :span="22">
                                                        {{user_excel_file_name}}
                                                        <br>
                                                        {{user_excel_file_size}}
                                                    </el-col>


                                                    <el-col :span="2" class="default" v-if="user_excel_file_flag">
                                                        <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                                                            <rect x="0.5" y="0.5" width="15" height="15" rx="7.5" fill="#1570EF"/>
                                                            <rect x="0.5" y="0.5" width="15" height="15" rx="7.5" stroke="#1570EF"/>
                                                            <path d="M11.3334 5.5L6.75008 10.0833L4.66675 8" stroke="white" stroke-width="1.66667" stroke-linecap="round" stroke-linejoin="round"/>
                                                        </svg>
                                                    </el-col>
                                                </el-row>




                                            </div>
                                    </el-row>
                                    <el-row>
                                        <el-col :span="24">
                                            <el-progress :percentage="user_excel_file_progress"
                                                         :status="user_excel_file_status"
                                                         striped
                                                         striped-flow
                                                         :duration="10"
                                            />
                                        </el-col>

                                    </el-row>

                                </el-col>
                            </el-row>



                        </div>

                    </el-col>
                    <el-col :span="24">
                        <div class="user_upload_result_title">
                            批量结果
                        </div>

                        <div class="user_upload_result_box">
                            <el-input
                                class="fixed-size-textarea"
                                v-model="user_excel_file_result_str"

                                type="textarea"
                                :autosize="{ minRows: 5 }"
                            />

                        </div>
                    </el-col>
                </el-row>
                <template #footer="{close}">
                    <div class="user-add-form-header">
                        <el-button type="primary"
                                   @click="dialog_v_user_add_model_excel = false;dialog_v_user_add_model= true"
                                   class="user_button_passwd"
                                   color="white">
                            <el-text class="user_del_font" style="color:black;">
                                取 消
                            </el-text>
                        </el-button>
                        <el-button type="danger"
                                   @click="uploadUserExcelFile"
                                   class="user_button_passwd" color="#1570EF" style="border: #1570EF">
                            <el-text class="user_del_font">
                                确 认
                            </el-text>
                        </el-button>
                    </div>
                </template>
            </el-dialog>
            <el-dialog v-model="dialog_v_user_delete_confirm"
                       class="user_delete_confirm"
                       :show-close="false"
                       width="480px" top="30vh"
            >
                <template #header="{ close, titleId, titleClass }">
                    <div class="user-add-form-header">
                        <div>
                            <h4 :id="titleId" :class="titleClass">删除用户</h4>
                        </div>
                        <el-button @click="close">
                            <svg width="14" height="14" viewBox="0 0 14 14" fill="none"
                                 xmlns="http://www.w3.org/2000/svg">
                                <path d="M13 1L1 13M1 1L13 13" stroke="#667085" stroke-width="2" stroke-linecap="round"
                                      stroke-linejoin="round"/>
                            </svg>
                        </el-button>
                    </div>
                    <el-text>
                        是否确认删除用户，删除操作不可逆
                    </el-text>
                </template>
                <template #footer="{close}">
                    <div class="user-add-form-header">
                        <el-button type="primary" @click="dialog_v_user_delete_confirm = false"
                                   class="user_button"
                                   color="white">
                            <el-text class="user_del_font" style="color:black;">
                                取 消
                            </el-text>
                        </el-button>
                        <el-button type="danger" @click="deleteUsers()"
                                   class="user_button" color="red" style="border: red">
                            <el-text class="user_del_font">
                                删 除
                            </el-text>
                        </el-button>
                    </div>
                </template>


            </el-dialog>
            <el-dialog v-model="dialog_v_user_update_password"
                       class="user_add_form"
                       :show-close="false"
                       width="640px" top="30vh"
            >
                <template #header="{ close, titleId, titleClass }">
                    <div class="user-add-form-header">
                        <div>
                            <h4 :id="titleId" :class="titleClass">修改密码</h4>
                        </div>
                        <el-button @click="close">
                            <svg width="14" height="14" viewBox="0 0 14 14" fill="none"
                                 xmlns="http://www.w3.org/2000/svg">
                                <path d="M13 1L1 13M1 1L13 13" stroke="#667085" stroke-width="2" stroke-linecap="round"
                                      stroke-linejoin="round"/>
                            </svg>
                        </el-button>
                    </div>
                </template>

                <el-form :model="user_password" ref="user_password_form_ref" :rules="user_password_rules">
                    <el-form-item prop="new_password">
                        新密码
                        <el-input
                                v-model="user_password.new_password"
                                type="password"
                                placeholder="请输入新密码"
                                show-password


                        />
                    </el-form-item>
                    <el-form-item prop="new_password_confirm">
                        确认密码
                        <el-input
                                v-model="user_password.new_password_confirm"
                                type="password"
                                placeholder="请确认新密码"
                                show-password
                        />
                    </el-form-item>
                </el-form>

                <template #footer="{close}">
                    <div class="user-add-form-header">
                        <el-button type="primary"
                                   @click="resetForm(user_password_form_ref);dialog_v_user_update_password = false"
                                   class="user_button_passwd"
                                   color="white">
                            <el-text class="user_del_font" style="color:black;">
                                取 消
                            </el-text>
                        </el-button>
                        <el-button type="danger" @click="updateUserPassWd(user_password_form_ref)"
                                   class="user_button_passwd" color="#1570EF" style="border: #1570EF">
                            <el-text class="user_del_font">
                                确 认
                            </el-text>
                        </el-button>
                    </div>
                </template>
            </el-dialog>
        </div>
        <div class="footer">
            <el-pagination
                    :small="small"
                    :background="background"
                    :page-size="pageSize"
                    :total="total"
                    :current-page="currentPage"
                    :page-sizes="pageSizer"
                    layout="sizes, prev, pager, next, jumper"
                    :disabled="disabled"
                    @size-change="handleSizeChange"
                    @current-change="handleCurrentChange"
                    :pager-count="pagerCount"
                    :hide-on-single-page="hideOne"
            />

        </div>
    </div>
</template>

<style scoped>
.user_table {
    max-width: 1300px;
    min-height: 600px;
    margin: 50px auto auto;
}

.user_table_title {
    font-family: 'Inter', sans-serif;
    font-size: 18px;
    font-weight: 600;
    line-height: 28px;
    letter-spacing: 0;
    text-align: left;

}

.user_add_bot {
    font-family: 'Inter', sans-serif;
    font-size: 14px;
    font-weight: 600;
    line-height: 20px;
    letter-spacing: 0;
    text-align: left;
    color: whitesmoke;
}

.header {
    padding: 0 0 8px 0;
}

.footer {
    margin-top: 20px;
}

.user_add_form {
    width: 480px;
    height: 328px;
}

.user-add-form-header {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
}

.user_delete_confirm {
    max-width: 480px;
    height: 176px;


    border-radius: 12px;
    background: #FFFFFF;
    box-shadow: 0 8px 8px -4px #10182808, 0 20px 24px -4px #10182814;


}

.user_button {
    width: 210px;
    height: 44px;

    padding: 10px 18px;
    border-radius: 8px;
    border: 1px solid #D0D5DD;
    gap: 8px;
    box-shadow: 0 1px 2px 0 rgba(16, 24, 40, 0.08);
}

.user_button_passwd {
    width: 290px;
    height: 44px;
    padding: 10px 18px;
    border-radius: 8px;
    border: 1px solid #D0D5DD;
    gap: 8px;
    box-shadow: 0 1px 2px 0 rgba(16, 24, 40, 0.08);
}

.user_del_font {
    font-size: 16px;
    font-weight: 600;
    line-height: 24px;
    letter-spacing: 0;
    text-align: left;
    color: white;
}

.user_add_model_batch {
    width: 100%;
    height: 70px;
    border: 2px solid #EAECF0;
    border-radius: 12px;
    margin: 5px 0 5px 5px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-direction: row-reverse;
}
.file-mode-icon{
    width: 32px;
    height: 32px;
    padding: 8px;
    border-radius: 28px;
    border: 4px solid #EFF8FF;
    background: linear-gradient(0deg, #D1E9FF, #D1E9FF),
    linear-gradient(0deg, #EFF8FF, #EFF8FF);
}

.user-template-download{
    width: 432px; /* Fill 对应直接设定宽度 */
    min-height: 36px; /* Hug 对应自适应高度，这里设置最小高度  */
    padding: 8px 14px;
    border-radius: 8px;
    border: 1px solid #D0D5DD;
    gap: 8px;
    box-shadow: 0 1px 2px 0 #1018280D;
}

.upload-result{
    display: flex;
    justify-content: space-between;
    align-items: start;
    flex-direction: row-reverse;
}

.upload-demo{
    width: 432px;
    height: auto;
}
.user_upload_box{
    width: 432px;
    height: 202px;
    margin: 20px 0 0 0;
    border-radius: 12px;
    gap: 4px;
    background: linear-gradient(0deg, #FFFFFF, #FFFFFF), linear-gradient(0deg, #EAECF0, #EAECF0);
}
.user_upload_status_box{
    width: 432px;
    max-width: 432px;
    height: 96px;
    margin: 20px 0 0 0;
    border-radius: 12px;
    border: 1px solid #D0D5DD;
    gap: 4px;
    display: flex;
    justify-content: space-between;
    align-items: center;

}
.user_upload_result_title{
    margin-top: 15px;
}
.user_upload_result_box{
    width: 416px;
    height: 126px;
    margin: 0 0 20px 0;
    border-radius: 12px;
    border: 1px solid #D0D5DD;
    gap: 4px;
    padding: 8px;
    overflow: auto
}
.default{
    display: flex;
    justify-content: space-between;
    align-items: center;
}

</style>
