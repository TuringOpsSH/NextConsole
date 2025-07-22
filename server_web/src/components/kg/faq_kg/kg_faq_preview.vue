<template>
  <div class="question-answer-pair">
    <h2>{{ question_pre }}</h2>
    <h4>{{ question }}</h4>
    <p>{{ answer }}</p>
  </div>
</template>

<script setup lang="ts">
import { ref, watchEffect, onMounted } from 'vue';
import hljs from 'highlight.js';

interface QAPreviewProps {
  question: string;
  question_pre:string;
  answer: string;
}

const props = defineProps<QAPreviewProps>();
const question_pre = ref('');
const question = ref<string>('');
const answer = ref<string>('');
function highlightCode (){
  question_pre.value =props.question_pre;
  question.value =props.question;
  answer.value =props.answer;
};

onMounted(highlightCode);

watchEffect(() => {
  if (props.answer) {
    highlightCode();
  }
});
</script>

<style scoped>
/* 你可以根据需要自定义样式 */
pre {
  padding: 15px;
  background: #f5f5f5;
  border: 1px solid #ddd;
  border-radius: 5px;
}
.question-answer-pair {
  margin-bottom: 20px;
  border: 1px solid #ccc;
  padding: 10px;
  border-radius: 5px;
}
</style>
