import {nextTick, reactive, ref} from "vue";
import {assistant, model_instance} from "@/types/assistant";
import {ElInput, ElMessage, genFileId, UploadFile, UploadFiles, UploadInstance, UploadRawFile} from "element-plus";
import {KGMeta} from "@/types/kg";
import {search_kg_list} from "@/api/kg_center";
import {getToken} from "@/utils/auth";
import Clipboard from "clipboard";


export const assistant_choose = reactive<assistant>(
    {
        assistant_publish_shop_id: null,
        comments: undefined,
        assistant_author_avatar: "",
        assistant_author_id: "",
        assistant_author_name: "",
        id: null,
        assistant_name: '',
        assistant_desc: '',
        assistant_status: '创建',
        assistant_tags: [],
        assistant_role_prompt: '',
        assistant_avatar: 'images/logo.svg',
        assistant_avatar_url: '',
        assistant_language: '中文',
        assistant_voice: '',
        assistant_memory_size: 4,
        assistant_model_name: 'deepseek-chat',
        assistant_model_type: 'chat',
        assistant_model_temperature: 1,
        assistant_model_icon: 'images/deep_seek_logo.png',
        create_time: '',
        update_time: '',
        assistant_knowledge_base: [],
        assistant_function_lists: [],
        assistant_source: 1,
        authority_create_time: "",
        authority_value: 0,
        assistant_is_start: false,
        call_cnt: 0,
        is_shop_assistant: false,
        rag_factor: 0.75,
        rag_miss: 1,
        rag_miss_answer: "",
        rag_relevant_threshold: 0.25,

    }
);





export const Current_assistant_kg_list = ref<KGMeta[]>([])
export const Current_assistant_kg_keyword = ref('');

export const dia_assistant_kg_setting_vis = ref(false);

export const model_list = ref<model_instance[]>()
export const assistant_role_prompt_template = `
# Role: 诗人
## Profile
- Author: YZFly
- Version: 0.1
- Language: 中文
- Description: 诗人是创作诗歌的艺术家，擅长通过诗歌来表达情感、描绘景象、讲述故事，具有丰富的想象力和对文字的独特驾驭能力。诗人创作的作品可以是纪事性的，描述人物或故事，如荷马的史诗；也可以是比喻性的，隐含多种解读的可能，如但丁的《神曲》、歌德的《浮士德》。

### 擅长写现代诗
1. 现代诗形式自由，意涵丰富，意象经营重于修辞运用，是心灵的映现
2. 更加强调自由开放和直率陈述与进行“可感与不可感之间”的沟通。

### 擅长写七言律诗
1. 七言体是古代诗歌体裁
2. 全篇每句七字或以七字句为主的诗体
3. 它起于汉族民间歌谣

### 擅长写五言诗
1. 全篇由五字句构成的诗
2. 能够更灵活细致地抒情和叙事
3. 在音节上，奇偶相配，富于音乐美

## Rules
1. 内容健康，积极向上
2. 七言律诗和五言诗要押韵

## Workflow
1. 让用户以 "形式：[], 主题：[]" 的方式指定诗歌形式，主题。
2. 针对用户给定的主题，创作诗歌，包括题目和诗句。

## Initialization
作为角色 <Role>, 严格遵守 <Rules>, 使用默认 <Language> 与用户对话，友好的欢迎用户。然后介绍自己，并告诉用户 <Workflow>。

`;

export const marks = reactive({
    0: '0 精确',
    1: '1 默认',
    2: '2 宽松',
})

export const assistant_avatar_upload_header = {
    Authorization: 'Bearer ' + getToken(),
}
export const assistant_avatar_upload_data = ref(
    {
        assistant_id: assistant_choose.id,
        avatar_name: '',

    }
)
export const assistant_choose_avatar_upload_data = ref(
    {
        assistant_id: null,
        avatar_name: '',
    }
)
export const pick_assistant_role_edit = ref(true);
export const assistant_model_detail_vis = ref(false);


export const system_prompt_example_vis = ref(false);

export const assistant_detail_type = ref(1);
export const assistant_view_model = ref(0)
export const inputVisible = ref(false)
export const InputRef = ref<InstanceType<typeof ElInput>>()
export const inputValue = ref('')
export const upload_avatar = ref<UploadInstance>()
export const show_role_base_info = ref(true)
export const show_role_kg_info = ref(true)
export const show_test_console_flag = ref(false)
export const assistant_role_prompt_rows  =ref(40)
export const assistant_role_edit_resize_cnt = ref(0)








export function to_do_something() {
    ElMessage.warning({
        message: '暂不支持',
        type: 'info',
        duration: 600
    })
}




export async function search_assistant_kg_list(){
    let params = {
        page_size:3,
        page_num:1,
        kg_name:Current_assistant_kg_keyword.value,
        kg_desc:Current_assistant_kg_keyword.value,
        kg_tags:[Current_assistant_kg_keyword.value]
    }
    let res = await search_kg_list(params)
    if (!res.error_status) {
        Current_assistant_kg_list.value = res.result.data
    }

}

export function add_assistant_kg(row:KGMeta){
    for (let i = 0; i < assistant_choose.assistant_knowledge_base.length; i++) {
        if (assistant_choose.assistant_knowledge_base[i].kg_code === row.kg_code) {
            ElMessage.info(
                {
                    message: '知识库已成功添加',
                    type: 'info',
                    duration: 600
                }
            )
            return false
        }
    }
    assistant_choose.assistant_knowledge_base.push(row)

}
export function remove_assistant_kg(kg:KGMeta){
    for (let i = 0; i < assistant_choose.assistant_knowledge_base.length; i++) {
        if (assistant_choose.assistant_knowledge_base[i].kg_code === kg.kg_code) {
            assistant_choose.assistant_knowledge_base.splice(i, 1)
            break
        }
    }

}


export function system_prompt_example_copy() {
    Clipboard.copy(assistant_role_prompt_template)
    ElMessage.success({
        message: '复制成功',
        type: 'success',
        duration: 600
    })
}
export function handle_avatar_change(uploadFile: UploadFile, uploadFiles: UploadFiles) {
    if (uploadFiles.length > 0) {
        assistant_choose.assistant_avatar_url = URL.createObjectURL(uploadFiles[0].raw)
        assistant_choose.assistant_avatar = uploadFiles[0].name
        if (assistant_view_model.value === 1) {

            assistant_choose_avatar_upload_data.value.assistant_id = assistant_choose.id
            assistant_choose_avatar_upload_data.value.avatar_name = uploadFiles[0].name
        }
        if (assistant_view_model.value === 2) {
            assistant_avatar_upload_data.value.avatar_name = uploadFiles[0].name
        }
    }

}


export function handle_exceed(files: File[]) {
    upload_avatar.value!.clearFiles()
    const file = files[0] as UploadRawFile
    file.uid = genFileId()
    upload_avatar.value!.handleStart(file)

}

export function handle_tag_close(tag: string) {
    if (assistant_view_model.value === 1) {
        assistant_choose.assistant_tags.splice(assistant_choose.assistant_tags.indexOf(tag), 1)
    }
    if (assistant_view_model.value === 2) {
        assistant_choose.assistant_tags.splice(assistant_choose.assistant_tags.indexOf(tag), 1)
    }
}

export function showInput() {
    if (assistant_view_model.value===2 && assistant_choose.assistant_tags.length >= 5) {
        ElMessage.warning({
            message: '最多添加5个标签',
            type: 'warning',
            duration: 600
        })
        return
    }
    if (assistant_view_model.value===1 && assistant_choose.assistant_tags.length >= 5) {
        ElMessage.warning({
            message: '最多添加5个标签',
            type: 'warning',
            duration: 600
        })
        return
    }
    inputVisible.value = true
    nextTick(() => {
        InputRef.value!.input!.focus()
    })
}

export function handleInputConfirm() {
    if (inputValue.value) {
        if (inputValue.value.length > 100) {
            ElMessage.warning({
                message: '标签过长！请不要超过100个字符',
                type: 'warning',
                duration: 600
            })
            return
        }
        if (assistant_view_model.value === 2) {
            assistant_choose.assistant_tags.push(inputValue.value)
        }
        if (assistant_view_model.value === 1) {
            assistant_choose.assistant_tags.push(inputValue.value)
        }

    }
    inputVisible.value = false
    inputValue.value = ''
}
