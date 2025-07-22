<script setup lang="ts">
import { ArrowDown, ArrowRight, Minus, Plus, QuestionFilled } from '@element-plus/icons-vue';
import { ref, defineProps, defineEmits, onMounted, watch } from 'vue';
import RefSelect from '@/components/appCenter/refSelect.vue';
const props = defineProps({
  jsonSchema: {
    type: Object,
    default: null
  },
  isParent: {
    type: Boolean,
    default: true
  },
  valueDefine: {
    type: Boolean,
    default: false
  },
  nodeUpstream: {
    type: Array,
    default: null
  },
  readOnly: {
    type: Boolean,
    default: false
  }
});
const emits = defineEmits(['update:schema']);
const localSchema = ref();
const localValueDefile = ref(false);
const localReadOnly = ref(false);
const newKeys = ref({});
const errorKeys = ref({});
const allDataType = ['string', 'number', 'boolean', 'object', 'array', 'null', 'integer', 'file', 'file-list'];
function updateSchema() {
  if (localReadOnly.value) {
    return;
  }
  for (const key in newKeys.value) {
    const newKeyName = newKeys.value[key];
    // 更新属性名称
    if (newKeyName !== key) {
      const reg = /^[a-zA-Z][a-zA-Z0-9_]*$/;
      if (!reg.test(newKeyName)) {
        return;
      }
      // 新增属性名称
      localSchema.value.properties[newKeyName] = localSchema.value.properties[key];
      // 删除旧属性名称
      delete localSchema.value.properties[key];
      delete newKeys.value[key];
      newKeys.value[newKeyName] = newKeyName;
      if (localSchema.value.ncOrders) {
        const index = localSchema.value.ncOrders.indexOf(key);
        if (index > -1) {
          localSchema.value.ncOrders[index] = newKeyName;
        }
      }
    }
    // 属性改为array，需要添加items
    if (localSchema.value.properties[newKeyName]?.type === 'array') {
      handleChangeToArray(newKeyName);
    }
    // 属性改为object，需要添加properties
    if (
        localSchema.value.properties[newKeyName]?.type === 'object' &&
        !localSchema.value.properties[newKeyName]?.properties
    ) {
      handleChangeToObject(newKeyName);
    }
  }
  if (localSchema.value?.items) {
    initArrayItem();
  }
  const newSchema = localSchema.value;
  emits('update:schema', newSchema);
}
function handleChangeToArray(newKeyName: string) {
  console.log(localSchema.value.properties[newKeyName]);
  if (localSchema.value.properties[newKeyName]?.ref) {
    localSchema.value.properties[newKeyName].items = localSchema.value.properties[newKeyName]?.ref?.items;
    return;
  }
  if (!localSchema.value.properties[newKeyName]?.items) {
    localSchema.value.properties[newKeyName].items = {
      type: 'string'
    };
  } else {
    if (localSchema.value.properties[newKeyName]?.items?.type === 'object') {
      if (
          !localSchema.value.properties[newKeyName]?.items?.properties ||
          !Object.keys(localSchema.value.properties[newKeyName]?.items?.properties)?.length
      ) {
        localSchema.value.properties[newKeyName].items.properties = {
          tmpAttr: {
            type: 'string'
          }
        };
      }
    } else if (localSchema.value.properties[newKeyName]?.items?.type === 'array') {
      if (
          !localSchema.value.properties[newKeyName]?.items?.items ||
          !Object.keys(localSchema.value.properties[newKeyName]?.items?.items)?.length
      ) {
        localSchema.value.properties[newKeyName].items.items = {
          type: 'string'
        };
      }
    }
  }
}
function handleChangeToObject(newKeyName: string) {
  if (localSchema.value.properties[newKeyName]?.ref) {
    localSchema.value.properties[newKeyName].properties = localSchema.value.properties[newKeyName]?.ref?.properties;
    return;
  }
  const newKey = `newAttr_${Date.now().toString().split('').reverse().join('')}`;
  const newSubItem = {};
  newSubItem[newKey] = {
    type: 'string',
    value: '',
    ref: '',
    showSubArea: false
  };
  localSchema.value.properties[newKeyName].properties = newSubItem;
  localSchema.value.properties[newKeyName].ncOrders = [newKey];
}
function initArrayItem() {
  if (localSchema.value.items.type === 'object') {
    if (!localSchema.value.items.properties || !Object.keys(localSchema.value.items.properties)?.length) {
      localSchema.value.items.properties = {
        tmpAttr: {
          type: 'string'
        }
      };
    }
  } else if (localSchema.value.items.type === 'array') {
    if (!localSchema.value.items.items || !Object.keys(localSchema.value.items.items)?.length) {
      localSchema.value.items.items = {
        type: 'string'
      };
    }
  }
}
function minusParams(key) {
  // 删除属性
  if (localSchema.value.properties[key]) {
    delete localSchema.value.properties[key];
    if (localSchema.value.ncOrders) {
      const index = localSchema.value.ncOrders.indexOf(key);
      if (index > -1) {
        localSchema.value.ncOrders.splice(index, 1);
      }
    }
    delete newKeys.value[key];
    updateSchema();
  }
}
function addSubPrams(key, event) {
  event.preventDefault();
  // 添加属性
  const newKey = `newAttr_${Date.now().toString().split('').reverse().join('')}`;
  if (localSchema.value.properties[key]) {
    if (!localSchema.value.properties[key].properties) {
      const newItem = {};
      newItem[newKey] = {
        type: 'string',
        value: '',
        ref: '',
        showSubArea: false
      };
      localSchema.value.properties[key].properties = newItem;
      localSchema.value.ncOrders = [newKey];
    } else {
      localSchema.value.properties[key].properties[newKey] = {
        type: 'string',
        value: '',
        ref: '',
        showSubArea: false
      };
      localSchema.value.properties[key].ncOrders.push(newKey);
    }
    updateSchema();
  } else if (key == 'root') {
    localSchema.value.properties[newKey] = {
      type: 'string',
      value: '',
      ref: '',
      showSubArea: true
    };
    if (!localSchema.value.ncOrders) {
      localSchema.value.ncOrders = [];
    }
    localSchema.value.ncOrders.push(newKey);
    newKeys.value[newKey] = newKey;
    updateSchema();
  }
}
function checkParamsName(key) {
  // 节点名称限制为英文字符、数字、下划线，必须以英文字符开头

  const reg = /^[a-zA-Z][a-zA-Z0-9_-]*$/;
  if (!reg.test(newKeys.value[key])) {
    errorKeys.value[key] = true;
    return;
  }
  if (errorKeys.value?.[key]) {
    delete errorKeys.value[key];
  }
}
function updateRef(key, newRef) {
  // 更新引用
  if (localSchema.value.properties[key]) {
    localSchema.value.properties[key].ref = newRef;
    // 更新数据类型
    localSchema.value.properties[key].type = newRef?.refAttrType;
  }
  updateSchema();
}
onMounted(() => {
  localSchema.value = props.jsonSchema;
  localValueDefile.value = props.valueDefine;
  localReadOnly.value = props.readOnly;
  if (!localSchema.value) {
    localSchema.value = {
      type: 'object',
      properties: {},
      ncOrders: []
    };
  }
  // 设置所有属性的可见性
  for (const key in localSchema.value.properties) {
    if (localSchema.value.properties[key].type === 'object' || localSchema.value.properties[key].type === 'array') {
      localSchema.value.properties[key].showSubArea = true;
    } else {
      localSchema.value.properties[key].showSubArea = false;
    }
    newKeys.value[key] = key;
  }
  // console.log( props.jsonSchema)
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
        newKeys.value = {};
      }
      for (const key in localSchema.value.properties) {
        if (localSchema.value.properties[key].type === 'object' || localSchema.value.properties[key].type === 'array') {
          localSchema.value.properties[key].showSubArea = true;
        } else {
          localSchema.value.properties[key].showSubArea = false;
        }
        newKeys.value[key] = key;
        // console.log('newKeys', newKeys.value);
      }
    }
);
watch(
    () => props.valueDefine,
    newVal => {
      localValueDefile.value = newVal;
    }
);
watch(
    () => props.readOnly,
    newVal => {
      localReadOnly.value = newVal;
    }
);
</script>

<template>
  <div class="form-main">
    <div v-if="props.isParent && !localReadOnly" class="root-button">
      <el-button :icon="Plus" size="small" round @click="addSubPrams('root', $event)" />
    </div>
    <div v-if="props.isParent" class="root-tips">
      <el-tooltip
          v-if="Object.keys(errorKeys).length"
          content="参数名称必须以字母开头，且只能包含字母、数字和-或者_"
          effect="dark"
      >
        <el-icon>
          <QuestionFilled style="color: red" />
        </el-icon>
      </el-tooltip>
    </div>
    <div v-for="key in localSchema?.ncOrders" :key="key" class="form-item-object">
      <div
          v-show="localSchema?.properties?.[key]?.type == 'array' || localSchema?.properties?.[key]?.type == 'object'"
          class="config-arrow-box"
      >
        <el-icon
            v-if="localSchema?.properties?.[key]?.showSubArea"
            class="config-arrow"
            @click="localSchema.properties[key].showSubArea = false"
        >
          <ArrowDown />
        </el-icon>
        <el-icon v-else class="config-arrow" @click="localSchema.properties[key].showSubArea = true">
          <ArrowRight />
        </el-icon>
      </div>
      <el-row :gutter="6" class="form-row">
        <el-col :span="localValueDefile ? 7 : 10">
          <div class="attr-name">
            <el-input
                v-model="newKeys[key]"
                :placeholder="key"
                :class="{
                'is-error': errorKeys?.[key]
              }"
                :disabled="localReadOnly || localSchema?.properties?.[key]?.attrFixed"
                @change="updateSchema"
                @input="checkParamsName(key)"
            />
          </div>
        </el-col>
        <el-col :span="7">
          <div class="attr-type">
            <el-select
                v-model="localSchema.properties[key].type"
                :disabled="localReadOnly || localSchema?.properties?.[key]?.typeFixed"
                @change="updateSchema()"
            >
              <el-option v-for="dataType in allDataType" :key="dataType" :value="dataType" :label="dataType" />
            </el-select>
          </div>
        </el-col>
        <el-col v-if="localValueDefile" :span="6">
          <div class="attr-type">
            <RefSelect
                :ref-value="localSchema?.properties?.[key].ref"
                :disabled="localSchema?.properties?.[key]?.valueFixed"
                :up-stream-nodes="props.nodeUpstream"
                @update:ref="result => updateRef(key, result)"
            />
          </div>
        </el-col>
        <el-col v-if="!localReadOnly" :span="localValueDefile ? 4 : 6">
          <div v-if="!localReadOnly" class="std-middle-box">
            <el-button
                v-show="localSchema?.properties?.[key].type == 'object' && !localSchema?.properties?.[key]?.ref"
                :icon="Plus"
                round
                style="width: 14px; height: 14px"
                @click="addSubPrams(key, $event)"
            />
            <el-button
                v-show="!localSchema?.properties?.[key].attrFixed"
                :icon="Minus"
                style="width: 14px; height: 14px"
                @click="minusParams(key)"
            />
          </div>
        </el-col>
      </el-row>
      <div
          v-if="['array', 'object'].includes(localSchema?.properties?.[key]?.type)"
          v-show="localSchema?.properties?.[key].showSubArea"
          class="form-item-body"
      >
        <div v-if="localSchema?.properties?.[key]?.type == 'array' && !localSchema?.properties?.[key].ref">
          <el-row>
            <el-col :span="8">
              <el-tag> ITEMS </el-tag>
            </el-col>
            <el-col :span="7">
              <el-select
                  v-model="localSchema.properties[key].items.type"
                  :disabled="
                  localReadOnly || !!localSchema?.properties?.[key].ref || localSchema?.properties?.[key]?.typeFixed
                "
                  @change="updateSchema"
              >
                <el-option v-for="dataType in allDataType" :key="dataType" :value="dataType" :label="dataType" />
              </el-select>
            </el-col>
          </el-row>
          <JsonSchemaForm
              v-if="
              localSchema?.properties?.[key].items.type == 'object' ||
              localSchema?.properties?.[key].items.type == 'array'
            "
              :jsonSchema="localSchema.properties[key].items"
              :is-parent="localSchema.properties[key].items.type == 'object'"
              :value-define="localValueDefile"
              :node-upstream="props.nodeUpstream"
              :read-only="!!localSchema.properties[key].ref || !!localReadOnly"
              style="margin-left: 12px"
              @update:schema="updateSchema"
          />
        </div>
        <JsonSchemaForm
            v-else-if="localSchema?.properties?.[key]?.type == 'object'"
            :jsonSchema="localSchema.properties[key]"
            :is-parent="false"
            :value-define="localValueDefile"
            :node-upstream="props.nodeUpstream"
            :read-only="!!localSchema.properties[key].ref || !!localReadOnly"
            @update:schema="updateSchema"
        />
      </div>
    </div>
    <div v-if="localSchema?.items" class="form-item-body">
      <el-row>
        <el-col :span="8">
          <el-tag> ITEMS </el-tag>
        </el-col>
        <el-col :span="7">
          <el-select v-model="localSchema.items.type" :disabled="localReadOnly" @change="updateSchema">
            <el-option v-for="dataType in allDataType" :key="dataType" :value="dataType" :label="dataType" />
          </el-select>
        </el-col>
      </el-row>
      <JsonSchemaForm
          v-if="localSchema.items.type == 'object' || localSchema.items.type == 'array'"
          :jsonSchema="localSchema.items"
          :is-parent="localSchema.items.type == 'object'"
          :value-define="localValueDefile"
          :node-upstream="props.nodeUpstream"
          :read-only="!!localSchema.ref"
          style="margin-left: 12px"
          @update:schema="updateSchema"
      />
    </div>
  </div>
</template>

<style scoped>
.form-main {
  display: flex;
  flex-direction: column;
  width: 100%;
  gap: 4px;
  position: relative;
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
.form-row:hover {
  background-color: #f5f7fa;
}
.config-arrow-box {
  position: absolute;
  left: -20px;
  top: 0;
  z-index: 22;
}
.config-arrow {
  width: 12px;
  height: 12px;
}
.form-item-body {
  padding-left: 12px;
  padding-top: 4px;
}
.root-button {
  position: absolute;
  top: -35px;
  right: 16px;
}
.root-tips {
  position: absolute;
  top: -35px;
  left: 60px;
}
.is-error {
  border: 2px solid #f56c6c;
  border-radius: 6px;
}
</style>
