<template>
  <svg aria-hidden="false" :width="width" :height="height" :style="{ opacity }">
    <use v-if="isStroke" :xlink:href="symbolId" :fill="color" :stroke="stroke" :stroke-width="strokeWidth" />
    <use v-else :xlink:href="symbolId" :fill="color" />
  </svg>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps({
  prefix: {
    type: String,
    default: 'icon'
  },
  name: {
    type: String,
    required: true
  },
  color: {
    type: String,
    default: '#333'
  },
  width: {
    type: [String, Number],
    default: 16
  },
  height: {
    type: [String, Number],
    default: 16
  },
  opacity: {
    type: Number,
    default: 1
  },
  isStroke: {
    type: Boolean,
    default: false
  },
  stroke: {
    type: String,
    default: '#475467'
  },
  strokeWidth: {
    type: [String, Number],
    default: 1.6
  }
});

const symbolId = computed(() => `#${props.prefix}-${props.name}`);
</script>
<style scoped lang="scss">
svg {
  outline: none;
}
</style>
