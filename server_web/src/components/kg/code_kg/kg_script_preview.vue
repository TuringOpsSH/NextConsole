<template>
  <pre v-html="highlightedCode" class="hljs"></pre>
</template>

<script setup lang="ts">
import { ref, watchEffect, onMounted } from 'vue';
import hljs from 'highlight.js';

interface CodePreviewProps {
  code: string;
  language: string;
}

const props = defineProps<CodePreviewProps>();

const highlightedCode = ref<string>('');

const highlightCode = () => {
  highlightedCode.value = hljs.highlight(props.language, props.code).value;
};

onMounted(highlightCode);

watchEffect(() => {
  if (props.code) {
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
</style>
