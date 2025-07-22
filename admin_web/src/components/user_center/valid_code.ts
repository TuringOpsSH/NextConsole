import {nextTick, reactive, ref} from 'vue'

export const count_down = ref(60)
let count_down_interval = null
export function count_down_start(){
    count_down_interval = setInterval(()=>{
        count_down.value -= 1
        if (count_down.value === 0){
            clearInterval(count_down_interval)
        }
    }, 1000)
}
export const valid_loading = ref(false)
export const validCodeForm = reactive({
    valid_code_0: '',
    valid_code_1: '',
    valid_code_2: '',
    valid_code_3: '',
    valid_code_4: '',
    valid_code_5: '',

})
export const current_input_index = ref(0)
export const input_ref_0 = ref()
export const input_ref_1 = ref()
export const input_ref_2 = ref()
export const input_ref_3 = ref()
export const input_ref_4 = ref()
export const input_ref_5 = ref(null)
export const input_dict = ref({
    0: input_ref_0,
    1: input_ref_1,
    2: input_ref_2,
    3: input_ref_3,
    4: input_ref_4,
    5: input_ref_5

})
export async function to_next_input(func = null){
    // 如果当前输入框为空，不允许跳转
    if (!validCodeForm['valid_code_'+current_input_index.value]){
        return
    }
    current_input_index.value += 1;
    if (current_input_index.value > 5){
        // 验证码输入完成
        valid_loading.value = true
        let code = ''
        for (let i = 0; i < 6; i++){
            code += validCodeForm['valid_code_'+i]
        }
        // 执行后续函数

        if (typeof func === 'function') {
            try {
                // 调用 func 并等待结果
                return await func(code);
            } catch (error) {
                // 处理错误
                console.error('Error calling func:', error);
                throw error;
            } finally {
                current_input_index.value = 5
                valid_loading.value = false
            }
        }


        current_input_index.value = 5
        valid_loading.value = false
    }
    input_dict.value[current_input_index.value].focus()
}
export function to_prev_input(){
    input_dict.value[current_input_index.value].clear()
    current_input_index.value -= 1
    if (current_input_index.value < 0){
        current_input_index.value = 0
    }
    input_dict.value[current_input_index.value].focus()
}
export async function copy_valid_code(e, func = null){
    // @ts-ignore
    let paste = (e.clipboardData || window.clipboardData).getData('text')
    if (paste.length === 6){
        for (let i = 0; i < 6; i++){
            validCodeForm['valid_code_'+i] = paste[i]
        }

        current_input_index.value = 5
        input_ref_5.value.focus()
        to_next_input(func)


    }
}
