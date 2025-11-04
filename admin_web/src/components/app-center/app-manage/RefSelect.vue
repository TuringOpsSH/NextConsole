<script setup lang="ts">
import { Setting, Close } from '@element-plus/icons-vue';
import { ElMessage } from 'element-plus';
import { defineEmits, defineProps, ref, onMounted, watch } from 'vue';
import JsonSchemaSelect from '@/components/app-center/app-manage/JsonSchemaSelect.vue';
interface IRefNode {
  nodeCode: string;
  nodeName: string;
  nodeIcon: string;
  nodeType: string;
  nodeDesc: string;
  nodeResultFormat: string;
  nodeResultJsonSchema: Record<string, any>; // 使用 Record<string, any> 替代 object
  nodeResultExtractColumns: string[];
}
const props = defineProps({
  upStreamNodes: {
    type: Array as () => IRefNode[] | null,
    default: null
  },
  refValue: {
    type: [Object, String] as () => Record<string, any> | string,
    default: () => ({})
  },
  disabled: {
    type: Boolean,
    default: false,
    required: false
  },
  typeName: {
    type: String,
    default: 'string',
    required: false
  },
  typeFixed: {
    type: Boolean,
    default: false,
    required: false
  }
});
const emits = defineEmits(['update:ref']);
const localRef = ref();
const localNode = ref();
const popRef = ref();
const attrSelectPopRef = ref();
const localTypeName = ref(props.typeName);
const localTypeFixed = ref(false);
function updateRefValue(newValue) {
  // node-icon,node-name,attr-name,attr-type, attr-path
  console.log(localRef.value, newValue);
  const newTypeName = localRef.value?.refAttrTypeNmae || 'string';
  if (localTypeFixed.value && localTypeName.value != newTypeName) {
    if (localTypeName.value == 'integer' && newTypeName == 'string') {
      try {
        emits('update:ref', {
          refAttrType: 'integer',
          value: parseInt(newValue, 10)
        });
        return;
      } catch (e) {
        ElMessage.warning(`属性 ${localTypeName.value} 的数据类型已被锁定，请选择对应类型数据`);
        return;
      }
    } else {
      ElMessage.warning(`属性 ${localTypeName.value} 的数据类型已被锁定，请选择对应类型数据`);
      localRef.value = '';
      return;
    }
  }
  if (newValue?.nodeResultFormat == 'text') {
    localRef.value = {
      nodeCode: newValue?.nodeCode,
      nodeName: newValue?.nodeName,
      nodeIcon: newValue?.nodeIcon,
      nodeType: newValue?.nodeType,
      nodeDesc: newValue?.nodeDesc,
      refAttrName: 'OUTPUT',
      refAttrType: 'string',
      refAttrPath: 'OUTPUT'
    };
  }

  emits('update:ref', localRef.value);
}
function isObject(refValue) {
  return typeof refValue === 'object' && refValue !== null && Object.keys(refValue).length > 0;
}
onMounted(() => {
  localRef.value = props.refValue;
  localNode.value = props.upStreamNodes?.[0];
});
watch(
  () => props.refValue,
  newVal => {
    localRef.value = newVal;
  },
  { immediate: true }
);
watch(
  () => props.typeName,
  newVal => {
    localTypeName.value = newVal;
  },
  { immediate: true }
);
watch(
  () => props.typeFixed,
  newVal => {
    localTypeFixed.value = newVal;
  },
  { immediate: true }
);
function clearInput() {
  localRef.value = '';
  popRef.value?.hide();
  emits('update:ref', '');
}
function getValueByPath(obj, path) {
  const pathParts = path.split('.');
  if (pathParts.length === 0) {
    return undefined;
  }
  let targetObj = obj;
  for (let i = 0; i < pathParts.length; i += 1) {
    const key = pathParts[i];
    if (targetObj?.properties?.[key]) {
      targetObj = targetObj.properties[key];
    } else if (targetObj?.items?.[key]) {
      targetObj = targetObj.items[key];
    }
  }
  return targetObj;
}
function handleClickAttr(node, selectAttr) {
  // 更新attrKeyPath: 添加父节点的属性名称
  for (let k of attrSelectPopRef.value) {
    k?.hide();
  }
  if (localTypeFixed.value && selectAttr.attrTypeName != localTypeName.value) {
    ElMessage.warning(`属性 ${localTypeName.value} 的数据类型已被锁定，无法更改为 ${selectAttr.attrType}`);
    return;
  }
  localRef.value = {
    nodeCode: node?.nodeCode,
    nodeName: node?.nodeName,
    nodeIcon: node?.nodeIcon,
    nodeType: node?.nodeType,
    nodeDesc: node?.nodeDesc,
    refAttrName: selectAttr.attrName,
    refAttrType: selectAttr.attrType,
    refAttrTypeName: selectAttr.attrTypeName,
    refAttrPath: `${node.nodeCode}.${selectAttr.attrKeyPath}`
  };
  if (selectAttr.attrType == 'array') {
    localRef.value.items = getValueByPath(node.nodeResultJsonSchema, selectAttr.attrKeyPath)?.items;
  } else if (selectAttr.attrType == 'object') {
    const tmp = getValueByPath(node.nodeResultJsonSchema, selectAttr.attrKeyPath);
    localRef.value.properties = tmp?.properties;
    localRef.value.ncOrders = tmp?.ncOrders || [];
    try {
      for (let k of Object.keys(localRef.value.properties)) {
        localRef.value.properties[k].valueFixed = true;
      }
    } catch (e) {
      console.log(e);
    }
  }
  emits('update:ref', localRef.value);
}
function getShowRefPath(path: string) {
  // 去除前缀的节点代码
  if (!path || !path.includes('.')) {
    return path;
  }
  const parts = path.split('.');
  if (parts.length > 1) {
    return parts.slice(1).join('.');
  }
}

defineExpose({
  clearInput
});
</script>

<template>
  <div class="ref-select">
    <el-input v-model="localRef" clearable :disabled="props.disabled" @change="updateRefValue">
      <template #append>
        <el-popover trigger="click" placement="top" :disabled="props.disabled" title="上游节点变量">
          <template #reference>
            <el-icon style="cursor: pointer">
              <Setting />
            </el-icon>
          </template>
          <el-scrollbar>
            <div class="pre-node-list">
              <div v-for="node in props.upStreamNodes" :key="node.nodeCode" class="pre-node-item" style="gap: 6px">
                <el-popover
                  ref="attrSelectPopRef"
                  trigger="hover"
                  placement="left-start"
                  max-width="50vw"
                  width="350px"
                >
                  <template #reference>
                    <div class="std-left-box" style="gap: 6px; width: 100%">
                      <div class="std-left-box">
                        <el-image :src="node?.nodeIcon" style="width: 16px; height: 16px" />
                      </div>
                      <div class="std-left-box">
                        <el-text>{{ node?.nodeName }}</el-text>
                      </div>
                    </div>
                  </template>
                  <div>
                    <div v-if="node?.nodeResultFormat == 'text'" class="ref-node" @click="updateRefValue(node)">
                      <div class="ref-node-name">
                        <el-text>OUTPUT</el-text>
                      </div>
                      <div class="ref-node-value">
                        <el-tag type="primary" round size="small">string</el-tag>
                      </div>
                    </div>
                    <div v-else-if="node?.nodeResultFormat == 'json'" class="ref-node-area">
                      <JsonSchemaSelect
                        :schema-code="node.nodeCode"
                        :json-schema="node.nodeResultJsonSchema"
                        @click:attr="result => handleClickAttr(node, result)"
                      />
                    </div>
                  </div>
                </el-popover>
              </div>
            </div>
          </el-scrollbar>
        </el-popover>
      </template>
    </el-input>
    <div v-show="isObject(localRef)">
      <el-popover ref="popRef" width="340px" :hide-after="0" placement="top">
        <template #reference>
          <div v-if="isObject(localRef)" class="ref-obj-reference">
            <div class="std-left-box">
              <el-image :src="localRef?.nodeIcon" style="width: 12px; height: 12px" />
            </div>
            <div class="std-left-box-node">
              <div class="std-left-box">
                <el-text truncated>{{ localRef?.nodeName }}</el-text>
              </div>

              <el-divider direction="vertical" />
              <div class="std-left-box-node">
                <el-text truncated>{{ getShowRefPath(localRef?.refAttrPath) }}</el-text>
              </div>
            </div>
            <div v-if="!props.disabled" @click="clearInput">
              <el-icon>
                <Close />
              </el-icon>
            </div>
          </div>
        </template>
        <div class="ref-obj">
          <div class="std-left-box" style="gap: 4px">
            <div class="std-left-box">
              <el-image :src="localRef?.nodeIcon" style="width: 12px; height: 12px" />
            </div>
            <div class="std-left-box-node">
              <div class="std-left-box">
                <el-text truncated>{{ localRef?.nodeName }}</el-text>
              </div>

              <el-divider direction="vertical" />
              <div class="fixed-width-div">
                {{ getShowRefPath(localRef?.refAttrPath) }}
              </div>
            </div>
          </div>
          <div class="std-left-box">
            <el-tag type="primary" size="small">{{ localRef?.refAttrType }}</el-tag>
          </div>
        </div>
      </el-popover>
    </div>
  </div>
</template>

<style scoped>
.ref-select {
  position: relative;
}
.std-left-box {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
}
.pre-node-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
  max-height: 500px;
}
.pre-node-item {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
}
.pre-node-item:hover {
  background-color: #f5f5f5;
}
.ref-node {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  gap: 6px;
  cursor: pointer;
}
.ref-node:hover {
  background-color: #f5f5f5;
}
:deep(.el-input-group__append, .el-input-group__prepend) {
  padding: 0 4px;
}
.ref-obj {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  gap: 4px;
  cursor: pointer;
  flex-wrap: wrap;
}
.ref-obj-reference {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 4px;
  cursor: pointer;
  position: absolute;
  top: 4px;
  left: 10px;
  z-index: 999;
  background-color: white;
  width: calc(100% - 40px);
  height: 24px;
  overflow: hidden;
}
.std-left-box-node {
  width: 100%;
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: center;
}
.fixed-width-div {
  max-width: 160px;
  /* 允许文字自动换行 */
  word-wrap: break-word;
}
</style>
