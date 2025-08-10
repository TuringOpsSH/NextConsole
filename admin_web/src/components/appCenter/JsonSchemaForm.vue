<script setup lang="ts">
import { ArrowDown, ArrowRight, Minus, Plus, QuestionFilled, StarFilled, List } from '@element-plus/icons-vue';
import {ref, defineProps, defineEmits, onMounted, watch, nextTick} from 'vue';
import RefSelect from '@/components/appCenter/refSelect.vue';
import {ElMessage} from "element-plus";
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
  },
  requireDefine: {
    type: Boolean,
    default: false
  }
});
const emits = defineEmits(['update:schema']);
const localSchema = ref();
const localValueDefile = ref(false);
const localReadOnly = ref(false);
const localRequireDefile = ref(false);
const newKeys = ref({});
const errorKeys = ref({});
const allDataType = ['string', 'number', 'boolean', 'object', 'array', 'integer', 'file', 'file-list'];
const showFileEnumFlag = ref(false);
const currentKey = ref('');
function updateSchema() {
  if (localReadOnly.value) {
    return;
  }
  const newSchema = localSchema.value;
  emits('update:schema', newSchema);
}
function checkParamsName(key: string) {
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
function changeAttrName() {
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

  }
  updateSchema()
}
function changeAttrType(typeName: string, key: string, isItem=false) {
  const target = isItem
      ? localSchema.value?.properties?.[key].items || localSchema.value?.items
      : localSchema.value.properties[key];
  target.type = typeName;
  if (typeName === 'array') {
    handleChangeToArray(key, isItem);
  } else if (typeName === 'object') {
    handleChangeToObject(key, isItem);
  } else if (typeName === 'file') {
    handleChangeToFile(key, isItem)
  } else if (typeName === 'file-list') {
    handleChangeToFileList(key, isItem)
  } else if (typeName === 'boolean') {
    handleChangeToBoolean(key, isItem);
  } else {
    delete target.items;
    delete target.properties;
  }

  updateSchema();
}
function handleChangeToArray(key: string, isItem: boolean) {
  const target = isItem
      ? localSchema.value?.properties?.[key].items || localSchema.value?.items
      : localSchema.value.properties[key];
  target.items = {
    type: 'string',
    typeName: 'string',
    description: '',
  };
  delete target.ncOrders;
  delete target.enum;
  delete target.required;
}
function handleChangeToObject(key: string, isItem: boolean) {
  const target = isItem
      ? localSchema.value?.properties?.[key].items || localSchema.value?.items
      : localSchema.value.properties[key];

  const newKey = `tmpAttr${Date.now().toString().split('').reverse().join('')}`;
  const newSubItem = {};
  newSubItem[newKey] = {
    type: 'string',
    typeName: 'string',
    value: '',
    ref: '',
    showSubArea: false,
    description: '',
  };
  target.properties = newSubItem;
  target.ncOrders = [newKey];
  target.attrFixed = false;
  target.valueFixed = false;
  delete target.items;
}
function handleChangeToFile(key: string, isItem: boolean) {
  const target = isItem
      ? localSchema.value?.properties?.[key].items || localSchema.value?.items
      : localSchema.value.properties[key];
  target.type = 'object';
  target.properties = {
    id: {
      type: 'number',
      typeName: 'number',
      value: 0,
      ref: '',
      showSubArea: false,
      description: '文件ID',
      attrFixed: true,
      valueFixed: true,
      typeFixed: true,
    },
    name: {
      type: 'string',
      typeName: 'string',
      value: '',
      ref: '',
      showSubArea: false,
      description: '文件名称',
      attrFixed: true,
      valueFixed: true,
      typeFixed: true,
    },
    size: {
      type: 'number',
      typeName: 'number',
      value: 0,
      ref: '',
      showSubArea: false,
      description: '文件大小',
      attrFixed: true,
      valueFixed: true,
      typeFixed: true,
    },
    format: {
      type: 'string',
      typeName: 'string',
      value: '',
      ref: '',
      showSubArea: false,
      description: '文件类型',
      attrFixed: true,
      valueFixed: true,
      typeFixed: true,
    },
    icon: {
      type: 'string',
      typeName: 'string',
      value: '',
      ref: '',
      showSubArea: false,
      description: '文件图标',
      attrFixed: true,
      valueFixed: true,
      typeFixed: true,
    },
  };
  target.ncOrders = ['id', 'name', 'size', 'format', 'icon'];
  delete target.enum;
  delete target.required;
}
function handleChangeToFileList(key:string, isItem: boolean) {
  const target = isItem
      ? localSchema.value?.properties?.[key].items || localSchema.value?.items
      : localSchema.value.properties[key];

  target.type = 'array';
  target.items = {
    type: 'object',
    typeName: 'file',
    properties: {
      id: {
        type: 'number',
        value: 0,
        ref: '',
        showSubArea: false,
        description: '文件ID',
        typeFixed: true,
        attrFixed: true,
        valueFixed: true,
      },
      name: {
        type: 'string',
        value: '',
        ref: '',
        showSubArea: false,
        description: '文件名称',
        typeFixed: true,
        attrFixed: true,
        valueFixed: true,
      },
      size: {
        type: 'number',
        value: 0,
        ref: '',
        showSubArea: false,
        description: '文件大小',
        typeFixed: true,
        attrFixed: true,
        valueFixed: true,
      },
      format: {
        type: 'string',
        value: '',
        ref: '',
        showSubArea: false,
        description: '文件类型',
        typeFixed: true,
        attrFixed: true,
        valueFixed: true,
      },
      icon: {
        type: 'string',
        value: '',
        ref: '',
        showSubArea: false,
        description: '文件图标',
        typeFixed: true,
        attrFixed: true,
        valueFixed: true,
      }
    },
    ncOrders: ['id', 'name', 'size', 'format', 'icon'],
    typeFixed: true,
    attrFixed: true,
  };
}
function handleChangeToBoolean(key:string, isItem: boolean) {
  const target = isItem
      ? localSchema.value?.properties?.[key].items || localSchema.value?.items
      : localSchema.value.properties[key];
  delete target.items;
  delete target.properties;
  delete target.enum;
  delete target.required;
}
function changeRequired(item) {

  if (localSchema.value.required.includes(item)) {
    const index = localSchema.value.required.indexOf(item);
    if (index > -1) {
      localSchema.value.required.splice(index, 1);
    }
  } else {
    localSchema.value.required.push(item);
  }
  updateSchema()
}
function changeEnum(key: string) {
  // 更新枚举值
  if (localSchema.value.properties[key]) {
    if (localSchema.value.properties[key].type == 'object') {
      localSchema.value.properties[key].type = 'string';
      delete localSchema.value.properties[key]?.properties;

    } else if (localSchema.value.properties[key].type == 'array') {
      localSchema.value.properties[key].type = 'string';
      delete localSchema.value.properties[key]?.items;
    }
  }
  updateSchema();
}

function minusParams(key: string) {
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
function addSubPrams(key: string, event) {
  event.preventDefault();
  // 添加属性
  const newKey = `tmpAttr${Date.now().toString().split('').reverse().join('')}`;
  if (localSchema.value.properties[key]) {
    if (!localSchema.value.properties[key].properties) {
      const newItem = {};
      newItem[newKey] = {
        type: 'string',
        typeName: 'string',
        value: '',
        ref: '',
        showSubArea: false,
        description: ''
      };
      localSchema.value.properties[key].properties = newItem;
      localSchema.value.ncOrders = [newKey];
    } else {
      localSchema.value.properties[key].properties[newKey] = {
        type: 'string',
        typeName: 'string',
        value: '',
        ref: '',
        showSubArea: false,
        description: ''
      };
      localSchema.value.properties[key].ncOrders.push(newKey);
    }
    updateSchema();
  } else if (key == 'root') {
    localSchema.value.properties[newKey] = {
      type: 'string',
      typeName: 'string',
      value: '',
      ref: '',
      showSubArea: true,
      description: ''
    };
    if (!localSchema.value.ncOrders) {
      localSchema.value.ncOrders = [];
    }
    localSchema.value.ncOrders.push(newKey);
    newKeys.value[newKey] = newKey;
    updateSchema();
  }
}
function updateRef(key: string, newRef) {
  // 更新引用

  if (localSchema.value.properties[key]) {
    // 检验数据类型
    console.log(key, newRef);
    const newType = newRef?.refAttrType || newRef?.refAttrTypeName || 'string';
    // 更新数据类型
    if (!localSchema.value.properties[key].typeFixed) {
      localSchema.value.properties[key].type = newType;
      localSchema.value.properties[key].typeName = newRef?.refAttrTypeName || newRef?.refAttrType || 'string';
    }
    if ( newRef?.value) {
      localSchema.value.properties[key].value = newRef?.value
    } else {
      localSchema.value.properties[key].ref = newRef;
      delete localSchema.value.properties[key].value;
      localSchema.value.properties[key].typeFixed = true;
    }
  }
  updateSchema();
}
function openFileEnumDialog(key:string) {
  if (['file', 'file-list'].includes(localSchema.value.properties?.[key]?.typeName )) {
    currentKey.value = key;
    showFileEnumFlag.value = true;
  } else {
    ElMessage.error('当前属性不是文件类型，无法设置文件格式');
  }
}
watch(
    () => props.jsonSchema,
    newVal => {
      localSchema.value = newVal;
      if (!localSchema.value) {
        localSchema.value = {
          type: 'object',
          properties: {},
          required: []
        };
        newKeys.value = {};
      }
      for (const key in localSchema.value.properties) {
        localSchema.value.properties[key].showSubArea = false;
        newKeys.value[key] = key;
      }
      if (!localSchema.value.required) {
        localSchema.value.required = [];
      }
    },{
      immediate: true
    }
);
watch(
    () => props.valueDefine,
    newVal => {
      localValueDefile.value = newVal;
    },{
      immediate: true
    }
);
watch(
    () => props.readOnly,
    newVal => {
      localReadOnly.value = newVal;
    },{
      immediate: true
    }
);
watch(
    () => props.requireDefine,
    newVal => {
      localRequireDefile.value = newVal;
    },
    { immediate: true }
);
</script>

<template>
  <div class="form-main">
    <div v-if="props.isParent && !localReadOnly && !localSchema?.attrFixed" class="root-button">
      <el-tooltip content="添加变量" placement="top" effect="light">
        <el-icon @click="addSubPrams('root', $event)" class="icon-button">
          <Plus />
        </el-icon>
      </el-tooltip>

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
        <el-col :span="localValueDefile ? 4 : 7">
          <div class="attr-name">
            <el-input
                v-model="newKeys[key]"
                :placeholder="key"
                :class="{'is-error': errorKeys?.[key]}"
                :disabled="localReadOnly || localSchema?.properties?.[key]?.attrFixed"
                @change="changeAttrName"
                @input="checkParamsName(key)"
            />
          </div>
        </el-col>
        <el-col :span="3">
          <div class="attr-desc">
            <el-input v-model="localSchema.properties[key].description"
                :disabled="localReadOnly || localSchema?.properties?.[key]?.attrFixed"
                @change="updateSchema"
            />
          </div>
        </el-col>
        <el-col :span="localRequireDefile ? 5: 7">
          <div class="attr-type">
            <el-select
                v-model="localSchema.properties[key].typeName"
                :disabled="localReadOnly || localSchema?.properties?.[key]?.typeFixed"
                @change="(newTypeName: string) =>changeAttrType(newTypeName, key)"
            >
              <el-option v-for="dataType in allDataType" :key="dataType" :value="dataType" :label="dataType" />
            </el-select>
          </div>
        </el-col>
        <el-col :span="2" v-show="localRequireDefile && !localSchema?.properties?.[key]?.typeFixed">
          <div class="attr-require">
            <el-tooltip content="是否必需" placement="top" effect="light">
              <el-icon :style="{color: localSchema?.required?.includes(key) ? 'red' : 'grey'} "
                       class="icon-button"
                       v-if="!localSchema.properties?.[key]?.valueFixed"
                       size="large" @click="changeRequired(key)">
                <StarFilled />
              </el-icon>
            </el-tooltip>
            <el-popover trigger="click" title="枚举值" width="300px" placement="left">
              <template #reference>
                  <el-icon
                      v-if="![
                          'object', 'array', 'file', 'file-list', 'null', 'boolean'
                      ].includes(localSchema.properties?.[key]?.type)
                      && !localSchema.properties?.[key]?.valueFixed"
                      :style="{color: localSchema.properties?.[key]?.enum?.length > 0 ? 'blue' : 'grey'} "
                           class="icon-button"
                           size="large">
                    <List />
                  </el-icon>
              </template>
              <el-form-item>
                <el-input-tag v-model="localSchema.properties[key].enum"
                              v-if="localSchema.properties[key].type == 'string'
                              || localSchema.properties[key].type == 'number'
                              || localSchema.properties[key].type == 'integer'"
                              placeholder="请输入枚举值,enter键分隔" clearable
                              size="large" tag-type="primary" tag-effect="light"
                              @change="changeEnum(key)"
                />
                <el-select v-else-if="localSchema.properties[key].type == 'boolean'"
                          v-model="localSchema.properties[key].enum"
                          placeholder="请选择枚举值" clearable multiple
                          size="large"
                          @change="changeEnum(key)">
                  <el-option-group>
                    <el-option :value="true" label="true" />
                    <el-option :value="false" label="false" />
                  </el-option-group>
                </el-select>
              </el-form-item>
            </el-popover>
            <el-tooltip content="允许的文件格式" effect="light" placement="top">
              <el-icon
                  v-if="[
                          'file', 'file-list'
                      ].includes(localSchema.properties?.[key]?.typeName)
                      && !localSchema.properties?.[key]?.valueFixed"
                  :style="{color: localSchema.properties?.[key]?.enum?.length > 0 ? 'blue' : 'grey'} "
                  class="icon-button"
                  @click="openFileEnumDialog(key)"
                  size="large">
                <List />
              </el-icon>
            </el-tooltip>
          </div>
        </el-col>
        <el-col v-if="localValueDefile" :span="6">
          <div class="attr-type">
            <RefSelect
                :ref-value="localSchema?.properties?.[key].ref || localSchema?.properties?.[key].value || ''"
                :disabled="localSchema?.properties?.[key]?.valueFixed"
                :type-name="localSchema?.properties?.[key].typeName"
                :typeFixed="localSchema?.properties?.[key].typeFixed"
                :up-stream-nodes="props.nodeUpstream"
                @update:ref="result => updateRef(key, result)"
            />
          </div>
        </el-col>
        <el-col v-if="!localReadOnly" :span="localValueDefile ? 4 : 6">
          <div v-if="!localReadOnly" class="std-middle-box" style="gap: 6px">
            <el-tooltip content="添加子变量" placement="top" effect="light">
              <el-icon v-show="localSchema?.properties?.[key].type == 'object'
              && !localSchema?.properties?.[key]?.ref && !localSchema?.properties?.[key]?.attrFixed"
                       class="icon-button"
                       @click="addSubPrams(key, $event)">
                <Plus />
              </el-icon>
            </el-tooltip>
            <el-tooltip content="移除变量" placement="top" effect="light">
              <el-icon v-show="!localSchema?.properties?.[key].attrFixed"  @click="minusParams(key)"
                       class="icon-button">
                <Minus />
              </el-icon>
            </el-tooltip>
          </div>
        </el-col>
      </el-row>
      <div
          v-if="['array', 'object'].includes(localSchema?.properties?.[key]?.type)"
          v-show="localSchema?.properties?.[key].showSubArea"
          class="form-item-body"
      >
        <JsonSchemaForm
            :jsonSchema="localSchema.properties[key]"
            :is-parent="false"
            :value-define="localValueDefile"
            :require-define="localRequireDefile"
            :node-upstream="props.nodeUpstream"
            :read-only="!!localSchema.properties[key].ref || !!localReadOnly || localSchema.properties[key]?.attrFixed"
            @update:schema="updateSchema"
        />
      </div>
    </div>
    <div v-if="localSchema?.ref" class="form-item-body">
      <JsonSchemaForm
          v-if="localSchema.ref"
          :jsonSchema="localSchema.ref"
          :is-parent="false"
          :value-define="false"
          :node-upstream="props.nodeUpstream"
          :read-only="true"
          :require-define="false"
          style="margin-left: 12px"
          @update:schema="updateSchema"
      />
    </div>
    <div v-else-if="localSchema?.items" class="form-item-body">
      <el-row>
        <el-col :span="8">
          <el-tag> ITEMS </el-tag>
        </el-col>
        <el-col :span="7">
          <el-select v-model="localSchema.items.typeName" :disabled="localReadOnly || localSchema?.items?.attrFixed"
                     @change="(newTypeName: string) =>changeAttrType(newTypeName, 'key', true)">
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
          :read-only="!!localSchema.ref || !!localReadOnly"
          :require-define="localRequireDefile"
          style="margin-left: 12px"
          @update:schema="updateSchema"
      />
    </div>

  </div>
  <el-dialog v-model="showFileEnumFlag" title="可上传的文件类型">
    <el-form style="margin-top: 20px">
      <el-form-item label="文件类型" label-position="top">
        <el-select multiple v-model="localSchema.properties[currentKey].enum" @change="updateSchema" allow-create
                   clearable filterable default-first-option
                   placeholder="请选择或者输入文件格式后缀"
        >
          <el-option-group>
            <el-option value="all" label="所有文件" />
            <el-option value="docx" label="docx" />
            <el-option value="doc" label="doc" />
            <el-option value="xlsx" label="xlsx" />
            <el-option value="xls" label="xls" />
            <el-option value="pptx" label="pptx" />
            <el-option value="pdf" label="pdf" />
            <el-option value="txt" label="txt" />
            <el-option value="md" label="markdown" />
            <el-option value="log" label="log" />
            <el-option value="jpg" label="jpg" />
            <el-option value="png" label="png" />
            <el-option value="gif" label="gif" />
            <el-option value="mp4" label="mp4" />
            <el-option value="mp3" label="mp3" />
            <el-option value="zip" label="zip" />
            <el-option value="rar" label="rar" />
            <el-option value="tar" label="tar" />
            <el-option value="7z" label="7z" />
          </el-option-group>
        </el-select>
      </el-form-item>
    </el-form>
  </el-dialog>
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
.icon-button {
  width: 12px;
  &:hover {
    cursor: pointer;
    color: #409eff;
  }
}
.attr-require {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  height: 100%;
}
</style>
