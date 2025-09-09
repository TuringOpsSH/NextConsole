<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref, reactive } from 'vue';

const props = defineProps({
  validCodeFunc: {
    type: Function,
    required: true
  }
});
const inputRef0 = ref();
const inputRef1 = ref();
const inputRef2 = ref();
const inputRef3 = ref();
const inputRef4 = ref();
const inputRef5 = ref(null);
const inputDict = ref({
  // eslint-disable-next-line @typescript-eslint/naming-convention
  0: inputRef0,
  // eslint-disable-next-line @typescript-eslint/naming-convention
  1: inputRef1,
  // eslint-disable-next-line @typescript-eslint/naming-convention
  2: inputRef2,
  // eslint-disable-next-line @typescript-eslint/naming-convention
  3: inputRef3,
  // eslint-disable-next-line @typescript-eslint/naming-convention
  4: inputRef4,
  // eslint-disable-next-line @typescript-eslint/naming-convention
  5: inputRef5
});
const currentInputIndex = ref(0);
const validCodeForm = reactive({
  valid_code_0: '',
  valid_code_1: '',
  valid_code_2: '',
  valid_code_3: '',
  valid_code_4: '',
  valid_code_5: ''
});
const validLoading = ref(false);
function onlyAcceptNumber(value: string | number) {
  if (!value) {
    return;
  }
  if (isNaN(Number(value))) {
    inputDict.value[currentInputIndex.value].clear();
    return;
  }
  toNextInput(props.validCodeFunc);
}
async function copyValidCode(e, func = null) {
  // @ts-ignore
  let paste = (e.clipboardData || window.clipboardData).getData('text');
  if (paste.length === 6) {
    for (let i = 0; i < 6; i++) {
      validCodeForm['valid_code_' + i] = paste[i];
    }

    currentInputIndex.value = 5;
    inputRef5.value.focus();
    toNextInput(func);
  }
}
async function toNextInput(func = null) {
  // 如果当前输入框为空，不允许跳转
  if (!validCodeForm['valid_code_' + currentInputIndex.value]) {
    return;
  }
  currentInputIndex.value += 1;
  if (currentInputIndex.value > 5) {
    // 验证码输入完成
    validLoading.value = true;
    let code = '';
    for (let i = 0; i < 6; i++) {
      code += validCodeForm['valid_code_' + i];
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
        currentInputIndex.value = 5;
        validLoading.value = false;
      }
    }

    currentInputIndex.value = 5;
    validLoading.value = false;
  }
  inputDict.value[currentInputIndex.value].focus();
}
function toPrevInput() {
  inputDict.value[currentInputIndex.value].clear();
  currentInputIndex.value -= 1;
  if (currentInputIndex.value < 0) {
    currentInputIndex.value = 0;
  }
  inputDict.value[currentInputIndex.value].focus();
}
onMounted(() => {
  // 监听退格键
  document.addEventListener('keydown', e => {
    if (e.key === 'Backspace') {
      toPrevInput();
    }
  });
  // 监听ctrl +v 事件自动填充
  document.addEventListener('paste', e => {
    copyValidCode(e, props.validCodeFunc);
  });
  // 默认聚焦第一个输入框
  inputRef0.value.focus();
});
onBeforeUnmount(() => {
  document.removeEventListener('keydown', e => {
    if (e.key === 'Backspace') {
      toPrevInput();
    }
  });
  document.removeEventListener('paste', e => {
    copyValidCode(e, props.validCodeFunc);
  });
});
</script>

<template>
  <el-form
    id="valid-code-box"
    v-loading="validLoading"
    :model="validCodeForm"
    element-loading-text="验证码验证中，请稍候..."
  >
    <el-form-item prop="valid_code_0">
      <el-input
        ref="inputRef0"
        v-model="validCodeForm.valid_code_0"
        class="valid-code-str"
        maxlength="1"
        @input="onlyAcceptNumber"
      />
    </el-form-item>
    <el-form-item prop="valid_code_1">
      <el-input
        ref="inputRef1"
        v-model="validCodeForm.valid_code_1"
        class="valid-code-str"
        maxlength="1"
        @input="onlyAcceptNumber"
      />
    </el-form-item>
    <el-form-item prop="valid_code_2">
      <el-input
        ref="inputRef2"
        v-model="validCodeForm.valid_code_2"
        class="valid-code-str"
        maxlength="1"
        @input="onlyAcceptNumber"
      />
    </el-form-item>
    <el-form-item>
      <el-text style="font-weight: 500; font-size: 32px; line-height: 32px; color: gray">-</el-text>
    </el-form-item>
    <el-form-item prop="valid_code_3">
      <el-input
        ref="inputRef3"
        v-model="validCodeForm.valid_code_3"
        class="valid-code-str"
        maxlength="1"
        @input="onlyAcceptNumber"
      />
    </el-form-item>

    <el-form-item prop="valid_code_4">
      <el-input
        ref="inputRef4"
        v-model="validCodeForm.valid_code_4"
        class="valid-code-str"
        maxlength="1"
        @input="onlyAcceptNumber"
      />
    </el-form-item>
    <el-form-item prop="valid_code_5">
      <el-input
        ref="inputRef5"
        v-model="validCodeForm.valid_code_5"
        class="valid-code-str"
        maxlength="1"
        @input="onlyAcceptNumber"
      />
    </el-form-item>
  </el-form>
</template>

<style scoped>
#valid-code-box {
  display: flex;
  justify-content: space-between;
  width: 100%;
  height: 100%;
  padding: 12px;
  gap: 6px;
  box-sizing: border-box;
}
.valid-code-str {
  max-width: 80px;
  max-height: 80px;
}
</style>
