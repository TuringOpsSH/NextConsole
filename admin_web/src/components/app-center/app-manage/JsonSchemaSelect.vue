<script setup lang="ts">
import { ArrowDown, ArrowRight } from '@element-plus/icons-vue';
import { defineEmits, defineProps, onMounted, ref, watch } from 'vue';
const props = defineProps<{
  schemaCode: {
    type: string | null;
    default: null;
  };
  jsonSchema: {
    type: object;
    default: Record<string, any>;
  };
}>();
const emits = defineEmits(['click:attr']);
const localSchema = ref({
  type: 'object',
  properties: {}
});
const localSchemaCode = ref<string | null>(null);
onMounted(() => {
  localSchema.value = props.jsonSchema;
  if (!localSchema.value) {
    localSchema.value = {
      type: 'object',
      properties: {}
    };
  }
  // 设置所有属性的可见性
  for (const key in localSchema.value.properties) {
    if (localSchema.value.properties[key].type === 'object' || localSchema.value.properties[key].type === 'array') {
      localSchema.value.properties[key].showSubArea = true;
    } else {
      localSchema.value.properties[key].showSubArea = false;
    }
  }
});

watch(
  () => props.jsonSchema,
  newVal => {
    localSchema.value = newVal;
    if (!localSchema.value) {
      localSchema.value = {
        type: 'object',
        properties: {}
      };
    }
  },
  { immediate: true }
);
watch(
  () => props.schemaCode,
  newVal => {
    if (newVal) {
      localSchemaCode.value = newVal;
    }
  },
  { immediate: true }
);
function selectAttr(key) {
  // 触发父组件的click:attr事件
  // node-icon,node-name,attr-name,attr-type, attr-key-path
  emits('click:attr', {
    attrName: key,
    attrNameCursor: localSchemaCode.value,
    attrType: localSchema.value?.properties[key]?.type,
    attrTypeName: localSchema.value?.properties[key]?.typeName,
    attrKeyPath: key,
    schemaCode: localSchemaCode.value
  });
}
function handleClickAttr(selectAttr) {
  // 更新attrKeyPath: 添加父节点的属性名称
  const cursorItem = localSchema.value.properties?.[selectAttr.attrNameCursor];
  if (cursorItem) {
    const newSelectAttr = {
      attrName: selectAttr.attrName,
      attrType: selectAttr.attrType,
      attrTypeName: selectAttr.attrTypeName,
      attrKeyPath: `${selectAttr.attrNameCursor}.${selectAttr.attrKeyPath}`,
      attrNameCursor: localSchemaCode.value
    };
    // 如果当前属性是对象或数组，则需要更新attrKeyPath
    if (cursorItem.type === 'array') {
      newSelectAttr.attrType = 'array';
      newSelectAttr.attrTypeName = 'array[' + selectAttr.attrType + ']';
    }

    emits('click:attr', newSelectAttr);
  }
}
</script>

<template>
  <el-scrollbar>
    <div class="form-main">
      <div v-for="key in localSchema?.ncOrders" :key="key" class="form-item-object">
        <div v-show="localSchema?.properties[key]?.type == 'object'" class="config-arrow-box">
          <el-icon
            v-if="localSchema?.properties[key]?.showSubArea"
            class="config-arrow"
            @click="localSchema.properties[key].showSubArea = false"
          >
            <ArrowDown />
          </el-icon>
          <el-icon v-else class="config-arrow" @click="localSchema.properties[key].showSubArea = true">
            <ArrowRight />
          </el-icon>
        </div>
        <el-tooltip :content="localSchema.properties[key].description" placement="top">
          <div class="form-item" @click="selectAttr(key)">
            <div class="attr-name">
              <el-text>{{ key }}</el-text>
            </div>
            <div class="attr-type">
              <el-tag type="primary">{{ localSchema.properties[key].typeName }}</el-tag>
            </div>
          </div>
        </el-tooltip>
        <div
          v-if="localSchema.properties[key]?.type == 'object'"
          v-show="localSchema.properties[key].showSubArea"
          class="form-item-body"
        >
          <JsonSchemaSelect
            :schema-code="key"
            :json-schema="localSchema.properties[key]"
            @click:attr="handleClickAttr"
          />
        </div>
        <div
          v-else-if="localSchema.properties[key]?.type == 'array'"
          v-show="localSchema.properties[key].showSubArea"
          class="form-item-body"
        >
          <JsonSchemaSelect
            :schema-code="key"
            :json-schema="localSchema.properties[key].items"
            @click:attr="handleClickAttr"
          />
        </div>
      </div>
    </div>
  </el-scrollbar>
</template>

<style scoped>
.form-main {
  display: flex;
  flex-direction: column;
  width: 100%;
  gap: 4px;
  max-height: 60vh;
}
.std-middle-box {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: row;
  height: 100%;
  width: 100%;
}
.form-item-object {
  position: relative;
}
.form-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-direction: row;
  height: calc(100% - 12px);
  width: calc(100% - 12px);
  padding: 6px;
  cursor: pointer;
}
.form-item:hover {
  background-color: #f5f5f5;
}
.config-arrow-box {
  position: absolute;
  left: -8px;
  top: 16px;
  z-index: 22;
}
.config-arrow {
  width: 12px;
  height: 12px;
}
.form-item-body {
  padding-left: 12px;
}
</style>
