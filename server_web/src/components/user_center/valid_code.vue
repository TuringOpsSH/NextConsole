<script setup lang="ts">
import {onBeforeUnmount, onMounted} from "vue";
import {
  copy_valid_code,
  current_input_index,
  input_dict,
  input_ref_0,
  input_ref_1,
  input_ref_2,
  input_ref_3,
  input_ref_4,
  input_ref_5,
  to_next_input,
  to_prev_input,
  valid_loading,
  validCodeForm,
} from "@/components/user_center/valid_code";

const props = defineProps(
    {
      valid_code_func: {
        type: Function,
        required: true,
      }
    }
)
function only_accept_number(value: string | number){
    if (!value){
      return
    }
    if (isNaN(Number(value))){
      input_dict.value[current_input_index.value].clear()
      return
    }
    to_next_input(props.valid_code_func)
 }


 onMounted(
    ()=>{
      // 监听退格键
      document.addEventListener('keydown', (e) => {
        if (e.key === 'Backspace') {
          to_prev_input()
        }
      })
      // 监听ctrl +v 事件自动填充
      document.addEventListener('paste', (e) => {
        copy_valid_code(e, props.valid_code_func)
      })
      // 默认聚焦第一个输入框
      input_ref_0.value.focus()
    }

 )
onBeforeUnmount(
    ()=>{
      document.removeEventListener('keydown', (e) => {
        if (e.key === 'Backspace') {
          to_prev_input()
        }
      })
      document.removeEventListener('paste', (e) => {
        copy_valid_code(e, props.valid_code_func)
      })
    }
)
</script>

<template>
  <el-form id="valid-code-box" :model="validCodeForm" v-loading="valid_loading"
           element-loading-text="验证码验证中，请稍候..."
  >
    <el-form-item prop="valid_code_0">
      <el-input v-model="validCodeForm.valid_code_0" class="valid-code-str" maxlength="1"
                @input="only_accept_number" ref="input_ref_0"/>
    </el-form-item>
    <el-form-item prop="valid_code_1">
      <el-input v-model="validCodeForm.valid_code_1" class="valid-code-str" maxlength="1"
                @input="only_accept_number" ref="input_ref_1"/>
    </el-form-item>
    <el-form-item prop="valid_code_2">
      <el-input v-model="validCodeForm.valid_code_2" class="valid-code-str" maxlength="1"
                @input="only_accept_number" ref="input_ref_2"/>
    </el-form-item>
    <el-form-item>
      <el-text style="font-weight: 500;font-size: 32px;line-height: 32px;color: gray">-</el-text>
    </el-form-item>
    <el-form-item prop="valid_code_3">
      <el-input v-model="validCodeForm.valid_code_3" class="valid-code-str" maxlength="1"
                @input="only_accept_number" ref="input_ref_3"/>
    </el-form-item>

    <el-form-item prop="valid_code_4">
      <el-input v-model="validCodeForm.valid_code_4" class="valid-code-str" maxlength="1"
                @input="only_accept_number" ref="input_ref_4"/>
    </el-form-item>
    <el-form-item prop="valid_code_5">
      <el-input v-model="validCodeForm.valid_code_5" class="valid-code-str" maxlength="1"
                @input="only_accept_number" ref="input_ref_5"/>
    </el-form-item>

  </el-form>

</template>

<style scoped>
#valid-code-box{
  display: flex;
  justify-content: space-between;
  width: 100%;
  height: 100%;
  padding: 12px;
  gap: 6px;
  box-sizing: border-box;
}
.valid-code-str{
  max-width: 80px;
  max-height: 80px;
}
</style>
