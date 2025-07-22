import {ref} from "vue";
import {ElNotification, genFileId, UploadRawFile, UploadUserFile} from "element-plus";
import {
    CurrentKg,
    download_loading,
    get_current_kg,
    kg_batch_upload_progress,
    show_kg_batch_upload_result,
} from "@/components/kg/kg_process";
import {download_kg, get_kg_upload_template, kg_ref_build, update_kg_json_schema} from "@/api/kg_center";
import {Editor} from "vditor/dist/ts/sv";
import {search_kg_docs} from "@/components/kg/doc_process";
import {current_script_tags} from "@/components/kg/code_kg/code_script_process";


export const update_button_ref =ref()
export const upload_script_loading = ref(false)
export const kg_script_list = ref<UploadUserFile[]>([])
export const kg_scripts_ref = ref(null)
export const kg_batch_script_ref = ref()
export const dialog_v_upload_kg_script = ref(false)
export const kg_add_scripts_model = ref('file')
export const script_schema_show = ref(true)
export const script_schema = ref(
    {
        "type": "object",
        "properties": {
            "script_name": {
                "type": "string",
                "title": "脚本名称",
                "description": "脚本名称"
            },
            "os_type": {
                "type": "string",
                "title": "操作系统",
                "description": "操作系统"
            },
            "script_desc": {
                "type": "string",
                "title": "脚本描述",
                "description": "脚本描述"
            },
            "script_author": {
                "type": "string",
                "title": "脚本作者",
                "description": "脚本作者"
            },
            "script_scene": {
                "type": "string",
                "title": "脚本场景",
                "description": "脚本场景"
            },
            "script_version": {
                "type": "string",
                "title": "脚本版本",
                "description": "脚本版本"
            },
            "script_content": {
                "type": "string",
                "title": "脚本内容",
                "description": "脚本内容"
            },
            "script_params": {
                "type": "object",
                "properties": {},
                "x-apifox-orders": [],
                "title": "脚本参数",
                "description": "脚本参数"
            }
        },
        "required": [
            "script_name",
            "os_type",
            "update_author",
            "script_scene",
            "script_version",
            "script_content",
            "script_params"
        ],
        "meta": {
            "embedding": [
                "script_name", "os_type", "script_desc", "script_scene", "script_content"
            ],
            "code": "script_content"
        }

    }
)
export const accept_languages = ".py, .java, .class, .jar, .js, .ts, .c, .h, .cpp, .hpp, .cs, .rb, .php, .html, .htm, .css, .go, .rs, .swift, .kt, .sql, .sh, .pl, .m, .scala, .r, .asm, .bashrc, .bash_profile, .bash_logout, .xml, .json, .yml, .yaml, .ini, .cfg, .conf, .md, .txt, .bat, .cmd, .ps1, .vbs, .vb, .vbproj, .wsf, .wsdl, .log, .sln, .vcxproj, .xaml, .resx, .config, .tsx, .jsx, .toml, .dic, .dat, .pth, .mk, .gradle, .npmrc, .tsconfig, .dockerfile, .makefile, .gitignore"
export const current_kg_json_schema_has_err = ref(false)
export const update_script_schema_dialog = ref(false)
export const json_editor_vue_ref =ref()
export const kg_batch_upload_logs = ref('')
export async function turn_on_upload_script_dialog(){
    if (!CurrentKg.value.kg_code) {
        return
    }
    await get_current_kg(CurrentKg.value.kg_code)
    kg_script_list.value = []
    show_kg_batch_upload_result.value = false
    kg_batch_upload_progress.value = 0
    kg_batch_upload_logs.value = ''
    dialog_v_upload_kg_script.value = true
    current_script_tags.value = {}
}

export async function turn_off_upload_script_dialog(){
    dialog_v_upload_kg_script.value = false
}

export function switch_script_schema_show(){
    script_schema_show.value = !script_schema_show.value
}
export async function upload_script_dialog_commit(){
    if (kg_add_scripts_model.value === 'csv'){
        await upload_script_dialog_batch_commit()
        return
    }
    if (!kg_script_list.value?.length){
        ElNotification.warning({
            title: "系统消息",
            message: "请上传脚本文档！",
            duration: 1500
        })
        return
    }
    // 校验表单必填字段
    for (let i=0; i < CurrentKg.value.kg_json_schema.required.length ;i ++  ){
        let name = CurrentKg.value.kg_json_schema.required[i]
        if (!current_script_tags.value?.[name]?.length) {
            ElNotification.warning(
                {
                    title:"系统通知",
                    message:"请完善必填字段",
                    duration: 2000
                }
            )
            return
        }
    }

    // 提交单个脚本
    upload_script_loading.value = true
    await kg_scripts_ref.value!.submit() // 提交上传

}

function deepEqual(obj1:object, obj2:object) {
    if (obj1 === obj2) {
        return true;
    }

    const keys1 = Object.keys(obj1);
    const keys2 = Object.keys(obj2);

    if (keys1.length !== keys2.length) {
        return false;
    }

    for (const key of keys1) {
        if (!keys2.includes(key) || !deepEqual(obj1[key], obj2[key])) {
            return false;
        }
    }

    return true;
}
//@ts-ignore
export function pre_check_script_schema(editor:Editor, errors: ValidationError[]){
    current_kg_json_schema_has_err.value = !!errors.length;
}
export async function update_script_schema(){
    // 验证schema是否合法
    if (!CurrentKg.value.kg_json_schema){
        ElNotification.error({
            title: '系统通知',
            message: "schema不可为空！",
            duration: 3000,
        })
        return
    }
    if (current_kg_json_schema_has_err.value) {
        ElNotification.error({
            title: '系统通知',
            message: "schema格式异常！",
            duration: 3000,
        })
        return
    }
    if(deepEqual(script_schema.value, CurrentKg.value.kg_json_schema)) {

        ElNotification.success(
            {
                title: '系统通知',
                message: 'schema相同，无需更新',
                duration: 3666,
            }
        )
        return
    }


    update_script_schema_dialog.value = true

}
export async function download_script_kg(){
    download_loading.value = true
    await download_kg({
        kg_code: CurrentKg.value.kg_code
    })
    ElNotification.success({
        title: '系统通知',
        message: '下载成功！',
        duration: 6666
    })
    download_loading.value = false
}
export async function download_script_template(){
    await get_kg_upload_template({
        kg_code: CurrentKg.value.kg_code
    })

    ElNotification.success({
        title: '系统通知',
        message: '下载成功！',
        duration: 6666
    })
}
export async function upload_script_dialog_remove(file: UploadRawFile ) {
    kg_scripts_ref.value?.handleRemove(file)
}
export async function upload_script_template_remove(file:UploadRawFile){
    kg_batch_script_ref.value?.handleRemove(file)
    kg_batch_upload_progress.value = 0
    kg_batch_upload_logs.value = ''
}
export async function update_script_schema_commit(){


    // 提交更新
    let params = {
        kg_code : CurrentKg.value.kg_code,
        kg_json_schema: CurrentKg.value.kg_json_schema,
    }
    let res = await update_kg_json_schema(params)
    if (!res.error_status){
        ElNotification.success({
            title: '系统通知',
            message: '更新成功！',
            duration: 6666
        })
    }

    update_script_schema_dialog.value = false
}
export async function kg_exceed_template(files){
    kg_batch_script_ref.value?.clearFiles()
    const file = files[0] as UploadRawFile
    file.uid = genFileId()
    kg_batch_script_ref.value?.handleStart(file)
}
export async function kg_exceed_single_script(files){
    kg_scripts_ref.value?.clearFiles()
    const file = files[0] as UploadRawFile
    file.uid = genFileId()
    kg_scripts_ref.value?.handleStart(file)
    current_script_tags.value = {}
    if (CurrentKg.value?.kg_json_schema?.properties){
        for (let k in CurrentKg.value?.kg_json_schema?.properties){
            current_script_tags.value[k] = ""
        }
    }

}
export async function upload_script_dialog_batch_commit(){
    // 提交批量csv
    upload_script_loading.value = true
    show_kg_batch_upload_result.value = true
    await kg_batch_script_ref.value?.submit()
    // 获取提交与解析结果

}
export async function upload_script_dialog_batch_on_success(response: any, file: UploadRawFile){
    upload_script_loading.value = false
    if (!response.error_status){
        kg_batch_upload_progress.value = response.result.progress
        kg_batch_upload_logs.value = response.result.logs
        ElNotification.success(
            {
                title: "系统通知",
                message:"上传完成",
                duration: 5000
            }
        )
        let params2 = {
            kg_db_code: CurrentKg.value.kg_code
        }
        let response2 = await kg_ref_build(params2)
        search_kg_docs()

    } else {
        ElNotification.error({
            title: "系统通知",
            message:"上传失败",
            duration: 5000
        })
    }
}
