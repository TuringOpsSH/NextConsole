<template>
  <el-container class="container">
    <el-header class="header-container">
      <el-button type="primary" @click="addCompany">新建公司</el-button>
    </el-header>
    <el-main>
      <el-table
        v-loading="isLoading"
        element-loading-text="加载中..."
        :data="companyList"
        style="width: 100%"
        border
        center
        stripe
      >
        <el-table-column prop="company_name" label="公司名称" fixed="left" min-width="200" sortable />
        <el-table-column prop="company_code" label="公司编码" width="120" sortable />
        <el-table-column prop="company_scale" label="规模" width="120" sortable />
        <el-table-column prop="company_desc" label="描述" width="180">
          <template #default="scope">
            <el-tooltip :content="scope.row.company_desc" placement="top" effect="dark">
              <el-text class="company-desc">{{ scope.row.company_desc }}</el-text>
            </el-tooltip>
          </template>
        </el-table-column>
        <el-table-column prop="company_status" label="状态" width="80" sortable />
        <el-table-column prop="create_time" label="创建时间" width="180" sortable />
        <el-table-column prop="update_time" label="更新时间" width="180" />
        <el-table-column prop="id" label="公司ID" width="80" sortable />
        <el-table-column prop="parent_company_id" label="母公司ID" width="80" sortable />
        <el-table-column label="地址信息">
          <el-table-column prop="company_country" label="国家" width="120" sortable />
          <el-table-column prop="company_area" label="地区" width="120" sortable />
          <el-table-column prop="company_address" label="地址" width="120" />
        </el-table-column>
        <el-table-column prop="company_industry" label="行业" width="120" sortable />
        <el-table-column prop="company_phone" label="联系电话" width="120" />
        <el-table-column prop="company_email" label="企业邮箱" width="120" />
        <el-table-column prop="company_website" label="官网" width="120" />
        <!-- <el-table-column prop="company_logo" label="logo" /> -->
        <el-table-column prop="company_type" label="类型" width="120" />
        <el-table-column label="操作" fixed="right" width="160">
          <template #default="scope">
            <el-tag class="btn-department-info" @click="viewDepartmentInfo(scope.row)">部门</el-tag>
            <el-tag class="btn-department-info" @click="editCompanyInfo(scope.row)">编辑</el-tag>
          </template>
        </el-table-column>
      </el-table>
    </el-main>
    <el-footer class="footer-container">
      <el-pagination
        size="small"
        layout=" total, sizes, prev, pager, next"
        :total="total"
        :page-sizes="[20, 50, 100, 200]"
        :page-size="pageSize"
        :current-page="pageNum"
        @update:page-size="handlePageSizeChange"
        @update:current-page="handlePageNumChange"
      />
    </el-footer>
  </el-container>
  <el-dialog
    v-model="showAddCompany"
    destroy-on-close
    class="company-dialog"
    center
    title="新建公司"
    width="50%"
    :close-on-click-modal="false"
  >
    <CompanyForm v-if="showAddCompany" @setShowForm="setShowAddCompany" @refresh-list="init" />
  </el-dialog>
  <el-dialog
    v-model="showEditCompany"
    destroy-on-close
    class="company-dialog"
    center
    title="编辑公司"
    width="50%"
    :close-on-click-modal="false"
  >
    <CompanyForm
      v-if="showEditCompany"
      :isEdit="true"
      :companyInfo="companyInfo"
      @setShowForm="setShowEditCompany"
      @refresh-list="init"
    />
  </el-dialog>
  <el-dialog
    v-model="showDepartManage"
    destroy-on-close
    class="depart-dialog"
    center
    title="部门管理"
    width="80%"
    :close-on-click-modal="false"
  >
    <DepartManage ref="departManage" :companyId="companyInfo.id" :companyName="companyInfo.name" />
  </el-dialog>
</template>
<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { sendRequest, TRequestParams } from '@/api/dashboard';
import CompanyForm from './CompanyForm.vue';
import DepartManage from './DepartManage.vue';
import { ICompany, ICompanyInfo } from './types';

defineOptions({
  name: 'EnterpriseManagement'
});
const companyList = ref<ICompany[]>([]);
const companyInfo = ref<ICompanyInfo>({});
const showAddCompany = ref(false);
const showEditCompany = ref(false);
const showDepartManage = ref(false);
const departManage = ref();
const isLoading = ref(true);
const total = ref(0);
const pageNum = ref(1);
const pageSize = ref(20);

function handlePageSizeChange(size: number) {
  pageSize.value = size;
  init();
}

function handlePageNumChange(num: number) {
  pageNum.value = num;
  init();
}

async function init() {
  isLoading.value = true;
  const params: TRequestParams = {
    url: 'getCompanyList',
    page_num: pageNum.value,
    page_size: pageSize.value
  };
  const res = await sendRequest(params);
  if (!res.error_status) {
    companyList.value = res.result?.data ?? [];
    total.value = res.result.total ?? 0;
  }
  isLoading.value = false;
}

function setShowAddCompany(show: boolean) {
  showAddCompany.value = show;
}

function setShowEditCompany(show: boolean) {
  showEditCompany.value = show;
}

function viewDepartmentInfo(row: ICompany) {
  companyInfo.value.id = row.id.toString();
  companyInfo.value.name = row.company_name;
  showDepartManage.value = true;
}

function editCompanyInfo(row: ICompany) {
  companyInfo.value.id = row.id.toString();
  companyInfo.value.address = row.company_address;
  companyInfo.value.area = row.company_area;
  companyInfo.value.code = row.company_code;
  companyInfo.value.country = row.company_country;
  companyInfo.value.desc = row.company_desc;
  companyInfo.value.email = row.company_email;
  companyInfo.value.industry = row.company_industry;
  companyInfo.value.name = row.company_name;
  companyInfo.value.phone = row.company_phone;
  companyInfo.value.scale = row.company_scale;
  companyInfo.value.status = row.company_status;
  companyInfo.value.type = row.company_type;
  companyInfo.value.website = row.company_website;
  showEditCompany.value = true;
}

function addCompany() {
  showAddCompany.value = true;
}

onMounted(async () => {
  await init();
});
</script>

<style scoped lang="scss">
.btn-department-info {
  color: #1677ff;
  cursor: pointer;
  margin: 0 8px;
}
.header-container {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  padding: 0 20px;
}
.container {
  height: calc(100% - 60px);
  overflow-y: auto;
}
.company-desc {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.footer-container {
  padding: 16px;
  display: flex;
  justify-content: center;
  position: fixed;
  bottom: 0;
  width: 100%;
}
</style>
<style lang="scss">
.company-form-item {
  justify-content: center;
  .el-form-item__content {
    flex: inherit;
  }
}
.company-dialog {
  margin-bottom: 20px;
}
.depart-dialog .el-dialog__header {
  margin-bottom: 12px;
}
</style>
