<template>
  <el-form ref="departFormRef" :model="departInfo" label-width="120px">
    <el-form-item
      v-for="(_, key) in departInfo"
      :key="key"
      :label="departText[key]"
      :prop="key"
      class="company-form-item"
      style="height: 40px"
      :required="['department_name', 'department_code'].includes(key)"
    >
      <el-input v-model="departInfo[key]" style="width: 400px" :disabled="key === 'company_id'" />
    </el-form-item>
    <el-form-item
      label="所属部门"
      class="company-form-item"
      :props="{ label: 'name', value: 'value', children: 'children' }"
      required
    >
      <el-tree-select
        v-model="parentDepartId"
        :data="parentDepartTree"
        style="width: 400px; height: auto"
        check-strictly
        :render-after-expand="false"
        @change="
          value => {
            parentDepartId = value;
          }
        "
      />
    </el-form-item>
    <el-form-item style="height: 80px" class="company-form-item">
      <el-button type="primary" @click="submitCompany">提交</el-button>
      <el-button type="primary" @click="resetCompany">取消</el-button>
    </el-form-item>
  </el-form>
</template>

<script setup lang="ts">
import { ElMessage } from 'element-plus';
import { onBeforeUnmount, onMounted, ref, toRefs, watch } from 'vue';
import { sendRequest, TRequestParams } from '@/api/dashboard';
import { IDepart, IDepartForm, IParentDepart } from './types';

interface IProps {
  companyId: string;
  companyName: string;
  parentDepartTree: IParentDepart[];
  isEdit?: boolean;
  editDepartInfo?: IDepart;
}
interface IEmits {
  (e: 'setShowForm', value: boolean): void;
  (e: 'refreshList'): void;
}
const parentDepartId = ref<null | string>();
const departFormRef = ref();
const props = defineProps<IProps>();
const { isEdit, editDepartInfo, companyName, companyId, parentDepartTree } = toRefs(props);
const emit = defineEmits<IEmits>();
const departInfo = ref<Omit<IDepartForm, 'parent_department_id'>>({
  department_name: '',
  department_code: '',
  company_id: companyName.value,
  department_status: '',
  department_desc: ''
});
const departText = {
  department_name: '部门名称',
  department_code: '部门编码',
  company_id: '所属公司',
  department_status: '状态',
  department_desc: '部门描述',
  department_logo: '部门logo'
};

watch(
  editDepartInfo,
  newVal => {
    init(newVal);
  },
  {
    deep: true
  }
);

onMounted(() => {
  init(editDepartInfo.value);
});

function init(editDepartInfo: IDepart) {
  if (editDepartInfo) {
    departInfo.value = {
      department_name: editDepartInfo.department_name,
      department_code: editDepartInfo.department_code,
      company_id: companyName.value,
      department_status: editDepartInfo.department_status,
      department_desc: editDepartInfo.department_desc
    };
    parentDepartId.value = editDepartInfo.parent_department_id?.toString() ?? null;
  } else {
    parentDepartId.value = null;
  }
}

function submitCompany() {
  const { department_name, department_code, department_status, department_desc } = departInfo.value;
  const params: TRequestParams = {
    url: isEdit.value ? 'updateDepartment' : 'addDepartment',
    department_name,
    department_code,
    company_id: companyId.value,
    parent_department_id: parentDepartId.value,
    department_status,
    department_desc
  };
  if (isEdit.value) {
    params.department_logo = editDepartInfo.value.department_logo;
    params.department_id = editDepartInfo.value.id;
  }
  sendRequest(params).then(res => {
    if (!res.error_status) {
      ElMessage.success(isEdit.value ? '编辑成功' : '添加成功');
      resetCompany();
      emit('refreshList');
    }
  });
}

function resetCompany() {
  departFormRef.value?.resetFields();
  emit('setShowForm', false);
}
</script>

<style scoped lang="scss"></style>
