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
    }
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
    attrNameCursor: key,
    attrType: localSchema.value?.properties[key]?.type,
    attrKeyPath: key,
    schemaCode: localSchemaCode.value
  });
}
function handleClickAttr(selectAttr) {
  // 更新attrKeyPath: 添加父节点的属性名称
  for (const key in localSchema.value.properties) {
    if (localSchema.value.properties[key].type === 'object') {
      for (const subKey in localSchema.value.properties[key].properties) {
        if (subKey === selectAttr.attrNameCursor && key == selectAttr.schemaCode) {
          const newSelectAttr = {
            attrName: selectAttr.attrName,
            attrType: selectAttr.attrType,
            attrKeyPath: `${key}.${selectAttr.attrKeyPath}`,
            attrNameCursor: key
          };
          emits('click:attr', newSelectAttr);
        }
      }
    } else if (localSchema.value.properties[key].type === 'array') {
      for (const subKey in localSchema.value.properties[key].items.properties) {
        if (subKey === selectAttr.attrNameCursor && key == selectAttr.schemaCode) {
          const newSelectAttr = {
            attrName: selectAttr.attrName,
            attrType: 'array[' + selectAttr.attrType + ']',
            attrKeyPath: `${key}.${selectAttr.attrKeyPath}`,
            attrNameCursor: key
          };
          emits('click:attr', newSelectAttr);
        }
      }
    }
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
        <div class="form-item" @click="selectAttr(key, )">
          <div class="attr-name">
            <el-text>{{ key }}</el-text>
          </div>
          <div class="attr-type">
            <el-tag type="primary">{{ localSchema.properties[key].type }}</el-tag>
          </div>
        </div>
        <div
            v-if="localSchema.properties[key]?.type == 'object'"
            v-show="localSchema.properties[key].showSubArea"
            class="form-item-body"
        >
          <JsonSchemaSelect
              :schema-code="key"
              :jsonSchema="localSchema.properties[key]"
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
              :jsonSchema="localSchema.properties[key].items"
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
