<template>
  <el-form ref="companyFormRef" :model="localCompanyInfo" label-width="120px">
    <el-form-item
      v-for="(value, key) in localCompanyInfo"
      v-show="key !== 'id'"
      :key="key"
      :label="companyText[key]"
      :prop="key"
      class="company-form-item"
      style="height: 40px"
      :required="['code', 'name'].includes(key)"
    >
      <el-input v-model="localCompanyInfo[key]" style="width: 400px" />
    </el-form-item>
    <el-form-item style="height: 80px" class="company-form-item">
      <el-button type="primary" @click="submitCompany">提交</el-button>
      <el-button type="primary" @click="resetCompany">取消</el-button>
    </el-form-item>
  </el-form>
</template>

<script setup lang="ts">
import { ElMessage, type FormInstance } from 'element-plus';
import { ref, toRefs, watch } from 'vue';
import { sendRequest, TRequestParams } from '@/api/dashboard';
import { ICompanyInfo } from './types';

const defaultInfo = {
  id: '',
  code: '',
  name: '',
  country: '',
  area: '',
  address: '',
  desc: '',
  status: '',
  type: '',
  industry: '',
  scale: '',
  phone: '',
  email: '',
  website: ''
};
const props = defineProps<IProps>();
const { isEdit = ref(false), companyInfo } = toRefs(props);
const companyFormRef = ref<FormInstance>();
const emit = defineEmits<IEmits>();
const localCompanyInfo = ref(defaultInfo);

watch(
  companyInfo,
  newVal => {
    if (newVal) {
      localCompanyInfo.value = { ...localCompanyInfo.value, ...newVal };
    }
  },
  { immediate: true, deep: true }
);
const companyText = ref({
  code: '公司编码',
  name: '公司名称',
  country: '国家',
  area: '地区',
  address: '地址',
  industry: '行业',
  scale: '规模',
  desc: '描述',
  status: '状态',
  type: '类型',
  phone: '联系电话',
  email: '企业邮箱',
  website: '官网'
});

interface IProps {
  isEdit?: boolean;
  companyInfo?: ICompanyInfo;
}
interface IEmits {
  (e: 'refresh-list'): void;
  (e: 'setShowForm', show: boolean): void;
}

async function submitCompany() {
  const params: TRequestParams = {
    url: isEdit.value ? 'updateCompany' : 'addCompany',
    company_address: localCompanyInfo.value.address,
    company_area: localCompanyInfo.value.area,
    company_code: localCompanyInfo.value.code,
    company_country: localCompanyInfo.value.country,
    company_desc: localCompanyInfo.value.desc,
    company_email: localCompanyInfo.value.email,
    company_industry: localCompanyInfo.value.industry,
    company_name: localCompanyInfo.value.name,
    company_phone: localCompanyInfo.value.phone,
    company_scale: localCompanyInfo.value.scale,
    company_type: localCompanyInfo.value.type,
    company_website: localCompanyInfo.value.website,
    parent_company_id: null,
    company_logo: ''
  };
  if (isEdit.value) {
    params.company_id = localCompanyInfo.value.id;
  }
  const res = await sendRequest(params);
  if (!res.error_status) {
    ElMessage.success(`${isEdit.value ? '编辑公司' : '新建公司'}成功`);
    resetCompany();
    emit('refresh-list');
  }
}

function resetCompany() {
  companyFormRef.value.resetFields();
  emit('setShowForm', false);
}
</script>
