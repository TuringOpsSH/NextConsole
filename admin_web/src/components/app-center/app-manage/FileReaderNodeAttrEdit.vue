<script setup lang="ts">
import { nodeUpdate } from '@/api/app-center-api';
import { useAppStore } from '@/stores/app-store';
import { useWorkflowStore } from '@/stores/workflow-store';

const emits = defineEmits(['updateNodeInputConfig', 'updateNodeOutputConfig']);
const appInfoStore = useAppStore();
const workflowStore = useWorkflowStore();
const fileSchema = {
  id: {
    type: 'integer',
    typeName: 'integer',
    value: '',
    ref: '',
    showSubArea: true,
    attrFixed: true,
    typeFixed: true,
    valueFixed: true,
    description: '资源ID'
  },
  name: {
    type: 'string',
    typeName: 'string',
    value: '',
    ref: '',
    showSubArea: true,
    attrFixed: true,
    typeFixed: true,
    valueFixed: true,
    description: '资源名称'
  },
  size: {
    type: 'number',
    typeName: 'number',
    value: '',
    ref: '',
    showSubArea: true,
    attrFixed: true,
    typeFixed: true,
    valueFixed: true,
    description: '资源大小'
  },
  format: {
    type: 'string',
    typeName: 'string',
    value: '',
    ref: '',
    showSubArea: true,
    attrFixed: true,
    typeFixed: true,
    valueFixed: true,
    description: '资源格式'
  },
  icon: {
    type: 'string',
    typeName: 'string',
    value: '',
    ref: '',
    showSubArea: true,
    attrFixed: true,
    typeFixed: true,
    valueFixed: true,
    description: '资源图标'
  }
};
async function updateNodeFileReaderConfig() {
  // 修正目标格式为png时的输出格式
  if (
    ['png', 'jpg'].includes(workflowStore.currentNodeDetail.node_file_reader_config?.tgt_format) &&
    workflowStore.currentNodeDetail.node_result_params_json_schema.ncOrders[0] == 'output_resource'
  ) {
    workflowStore.currentNodeDetail.node_input_params_json_schema.properties['input_resources'] = {
      type: 'array',
      typeName: 'file-list',
      value: '',
      ref: '',
      showSubArea: true,
      attrFixed: true,
      typeFixed: true,
      description: '输入文档列表',
      items: {
        type: 'object',
        typeName: 'file',
        value: '',
        ref: '',
        showSubArea: true,
        attrFixed: true,
        typeFixed: true,
        description: '输入文档',
        properties: fileSchema,
        ncOrders: ['id', 'name', 'size', 'format', 'icon']
      }
    };
    delete workflowStore.currentNodeDetail.node_input_params_json_schema.properties['input_resource'];
    workflowStore.currentNodeDetail.node_input_params_json_schema.ncOrders[0] = 'input_resources';

    workflowStore.currentNodeDetail.node_result_params_json_schema.properties['output_resources'] = {
      type: 'array',
      typeName: 'file-list',
      value: '',
      ref: '',
      showSubArea: true,
      attrFixed: true,
      typeFixed: true,
      description: '输出文档内容',
      items: {
        ncOrders: ['id', 'name', 'format', 'size', 'content', 'url'],
        properties: {
          content: {
            description: '文件内容',
            ref: '',
            showSubArea: false,
            type: 'string',
            typeName: 'string',
            value: ''
          },
          format: {
            description: '文件名称',
            ref: '',
            showSubArea: false,
            type: 'string',
            typeName: 'string',
            value: ''
          },
          id: {
            description: '文件ID',
            ref: '',
            showSubArea: false,
            type: 'integer',
            typeName: 'integer',
            value: ''
          },
          name: {
            description: '文件名称',
            ref: '',
            showSubArea: false,
            type: 'string',
            typeName: 'string',
            value: ''
          },
          size: {
            description: '文件大小',
            ref: '',
            showSubArea: false,
            type: 'number',
            typeName: 'number',
            value: ''
          },
          url: {
            description: '文件URL',
            ref: '',
            showSubArea: false,
            type: 'string',
            typeName: 'string',
            value: ''
          }
        },
        required: [],
        type: 'object',
        typeName: 'file'
      }
    };
    delete workflowStore.currentNodeDetail.node_result_params_json_schema.properties['output_resource'];
    workflowStore.currentNodeDetail.node_result_params_json_schema.ncOrders[0] = 'output_resources';
  }

  nodeUpdate({
    app_code: appInfoStore.currentApp.app_code,
    node_code: workflowStore.currentNodeDetail.node_code,
    node_file_reader_config: workflowStore.currentNodeDetail.node_file_reader_config
  });
}

async function handleFileReaderTargetFormatChange(val: string) {
  if (
    ['png', 'jpg'].includes(val) &&
    workflowStore.currentNodeDetail.node_file_reader_config?.src_format == 'pdf' &&
    workflowStore.currentNodeDetail.node_file_reader_config?.engine == 'PyMuPDF'
  ) {
    workflowStore.currentNodeDetail.node_result_params_json_schema.properties['output_resources'] = {
      type: 'array',
      typeName: 'file-list',
      value: '',
      ref: '',
      showSubArea: true,
      attrFixed: true,
      typeFixed: true,
      description: '输出文档内容',
      items: {
        ncOrders: ['id', 'name', 'format', 'size', 'content', 'url'],
        properties: {
          content: {
            description: '文件内容',
            ref: '',
            showSubArea: false,
            type: 'string',
            typeName: 'string',
            value: ''
          },
          format: {
            description: '文件名称',
            ref: '',
            showSubArea: false,
            type: 'string',
            typeName: 'string',
            value: ''
          },
          id: {
            description: '文件ID',
            ref: '',
            showSubArea: false,
            type: 'integer',
            typeName: 'integer',
            value: ''
          },
          name: {
            description: '文件名称',
            ref: '',
            showSubArea: false,
            type: 'string',
            typeName: 'string',
            value: ''
          },
          size: {
            description: '文件大小',
            ref: '',
            showSubArea: false,
            type: 'number',
            typeName: 'number',
            value: ''
          },
          url: {
            description: '文件URL',
            ref: '',
            showSubArea: false,
            type: 'string',
            typeName: 'string',
            value: ''
          }
        },
        required: [],
        type: 'object',
        typeName: 'file'
      }
    };
    delete workflowStore.currentNodeDetail.node_result_params_json_schema.properties['output_resource'];
    workflowStore.currentNodeDetail.node_result_params_json_schema.ncOrders[0] = 'output_resources';
  }
  emits('updateNodeOutputConfig');
  updateNodeFileReaderConfig();
}
async function handleFileReaderModeChange(val: string) {
  // 将input_resources 入参进行处理

  if (val == 'single') {
    workflowStore.currentNodeDetail.node_input_params_json_schema.properties['input_resource'] = {
      type: 'object',
      typeName: 'file',
      value: '',
      ref: '',
      showSubArea: true,
      attrFixed: true,
      typeFixed: true,
      description: '输入文档',
      properties: fileSchema,
      ncOrders: ['id', 'name', 'size', 'format', 'icon']
    };
    delete workflowStore.currentNodeDetail.node_input_params_json_schema.properties['input_resources'];
    workflowStore.currentNodeDetail.node_input_params_json_schema.ncOrders[0] = 'input_resource';

    workflowStore.currentNodeDetail.node_result_params_json_schema.properties['output_resource'] = {
      ncOrders: ['id', 'name', 'format', 'size', 'content', 'url'],
      properties: {
        content: {
          description: '文件内容',
          ref: '',
          showSubArea: false,
          type: 'string',
          typeName: 'string',
          value: ''
        },
        format: {
          description: '文件名称',
          ref: '',
          showSubArea: false,
          type: 'string',
          typeName: 'string',
          value: ''
        },
        id: {
          description: '文件ID',
          ref: '',
          showSubArea: false,
          type: 'integer',
          typeName: 'integer',
          value: ''
        },
        name: {
          description: '文件名称',
          ref: '',
          showSubArea: false,
          type: 'string',
          typeName: 'string',
          value: ''
        },
        size: {
          description: '文件大小',
          ref: '',
          showSubArea: false,
          type: 'number',
          typeName: 'number',
          value: ''
        },
        url: {
          description: '文件URL',
          ref: '',
          showSubArea: false,
          type: 'string',
          typeName: 'string',
          value: ''
        }
      },
      required: [],
      type: 'object',
      typeName: 'file'
    };
    delete workflowStore.currentNodeDetail.node_result_params_json_schema.properties['output_resources'];
    workflowStore.currentNodeDetail.node_result_params_json_schema.ncOrders[0] = 'output_resource';
  } else if (val == 'list') {
    workflowStore.currentNodeDetail.node_input_params_json_schema.properties['input_resources'] = {
      type: 'array',
      typeName: 'file-list',
      value: '',
      ref: '',
      showSubArea: true,
      attrFixed: true,
      typeFixed: true,
      description: '输入文档列表',
      items: {
        type: 'object',
        typeName: 'file',
        value: '',
        ref: '',
        showSubArea: true,
        attrFixed: true,
        typeFixed: true,
        description: '输入文档',
        properties: fileSchema,
        ncOrders: ['id', 'name', 'size', 'format', 'icon']
      }
    };
    delete workflowStore.currentNodeDetail.node_input_params_json_schema.properties['input_resource'];
    workflowStore.currentNodeDetail.node_input_params_json_schema.ncOrders[0] = 'input_resources';

    workflowStore.currentNodeDetail.node_result_params_json_schema.properties['output_resources'] = {
      type: 'array',
      typeName: 'file-list',
      value: '',
      ref: '',
      showSubArea: true,
      attrFixed: true,
      typeFixed: true,
      description: '输出文档内容',
      items: {
        ncOrders: ['id', 'name', 'format', 'size', 'content', 'url'],
        properties: {
          content: {
            description: '文件内容',
            ref: '',
            showSubArea: false,
            type: 'string',
            typeName: 'string',
            value: ''
          },
          format: {
            description: '文件名称',
            ref: '',
            showSubArea: false,
            type: 'string',
            typeName: 'string',
            value: ''
          },
          id: {
            description: '文件ID',
            ref: '',
            showSubArea: false,
            type: 'integer',
            typeName: 'integer',
            value: ''
          },
          name: {
            description: '文件名称',
            ref: '',
            showSubArea: false,
            type: 'string',
            typeName: 'string',
            value: ''
          },
          size: {
            description: '文件大小',
            ref: '',
            showSubArea: false,
            type: 'number',
            typeName: 'number',
            value: ''
          },
          url: {
            description: '文件URL',
            ref: '',
            showSubArea: false,
            type: 'string',
            typeName: 'string',
            value: ''
          }
        },
        required: [],
        type: 'object',
        typeName: 'file'
      }
    };
    delete workflowStore.currentNodeDetail.node_result_params_json_schema.properties['output_resource'];
    workflowStore.currentNodeDetail.node_result_params_json_schema.ncOrders[0] = 'output_resources';
  }
  emits('updateNodeInputConfig');
  emits('updateNodeOutputConfig');
  updateNodeFileReaderConfig();
}
</script>

<template>
  <div v-if="workflowStore.currentNodeDetail?.node_type == 'file_reader'" class="config-item">
    <div class="config-area">
      <el-form :model="workflowStore.currentNodeDetail" label-position="top">
        <el-form-item prop="mode" label="模式" style="padding: 0 12px">
          <el-radio-group v-model="workflowStore.currentNodeDetail.node_file_reader_config.mode" @change="handleFileReaderModeChange">
            <el-radio value="single">单文件</el-radio>
            <el-radio value="list">文件列表</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item prop="src_format" label="来源格式" style="padding: 0 12px">
          <el-select
            v-model="workflowStore.currentNodeDetail.node_file_reader_config.src_format"
            filterable
            allow-create
            placeholder="请选择或输入来源格式"
            @change="updateNodeFileReaderConfig"
          >
            <el-option value="pdf" label="pdf" />
            <el-option value="docx" label="docx" />
            <el-option value="doc" label="doc" />
            <el-option value="pptx" label="pptx" />
            <el-option value="xlsx" label="xlsx" />
            <el-option value="xls" label="xls" />
            <el-option value="未知" label="未知" />
          </el-select>
        </el-form-item>
        <el-form-item prop="tat_format" label="目标格式" style="padding: 0 12px">
          <el-select
            v-model="workflowStore.currentNodeDetail.node_file_reader_config.tgt_format"
            filterable
            allow-create
            placeholder="请选择或输入目标格式"
            @change="handleFileReaderTargetFormatChange"
          >
            <el-option value="pdf" label="pdf" />
            <el-option value="text" label="text" />
            <el-option value="png" label="png" />
            <el-option value="jpg" label="jpg" />
            <el-option value="markdown" label="markdown" />
            <el-option value="html" label="html" />
          </el-select>
        </el-form-item>
        <el-form-item prop="engine" label="处理引擎" style="padding: 0 12px">
          <el-select
            v-model="workflowStore.currentNodeDetail.node_file_reader_config.engine"
            filterable
            placeholder="请选择处理引擎"
            @change="updateNodeFileReaderConfig"
          >
            <el-option value="pandoc" label="pandoc" />
            <el-option value="PyMuPDF" label="PyMuPDF" />
            <el-option value="openpyxl" label="openpyxl" />
            <el-option value="python-pptx" label="python-pptx" />
            <el-option value="html2text" label="html2text" />
            <el-option value="liboffice" label="liboffice" disabled />
            <el-option value="tika" label="tika" disabled />
          </el-select>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<style scoped>
.config-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 6px;
  border-bottom: 1px solid #f0f0f0;
}
.config-area {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
</style>
