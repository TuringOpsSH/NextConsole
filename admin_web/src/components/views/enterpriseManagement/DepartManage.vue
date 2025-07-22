<template>
  <el-container class="depart-container">
    <el-header class="header-container">
      <el-button type="primary" @click="addDepart">新增部门</el-button>
    </el-header>
    <el-main>
      <el-table
        v-loading="isLoading"
        element-loading-text="加载中..."
        :data="departTreeList"
        header-row-class-name="custom-header-class"
        style="width: 100%; min-height: 600px"
        row-key="id"
        class="depart-table"
        border
        center
        stripe
      >
        <el-table-column
          prop="department_name"
          label="部门名称"
          fixed="left"
          min-width="220"
          sortable
          class-name="cell-depart-name"
        >
          <template #default="scope">
            <el-text class="department-name">{{ scope.row.department_name }}</el-text>
          </template>
        </el-table-column>
        <el-table-column prop="department_desc" label="描述" width="200" sortable>
          <template #default="scope">
            <el-tooltip :content="scope.row.department_desc" placement="top" effect="dark">
              <el-text class="department-desc">{{ scope.row.department_desc }}</el-text>
            </el-tooltip>
          </template>
        </el-table-column>
        <el-table-column prop="department_status" label="状态" width="80" sortable />
        <el-table-column prop="create_time" label="创建时间" width="180" sortable />
        <el-table-column prop="update_time" label="更新时间" width="180" sortable />
        <el-table-column prop="id" label="部门ID" width="100" sortable />
        <el-table-column prop="company_id" label="公司ID" width="100" sortable />
        <el-table-column prop="department_code" label="部门编码" width="120" sortable />
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="scope">
            <el-tag type="primary" class="btn-department-info" @click="editDepart(scope.row)">编辑</el-tag>
            <el-tag type="danger" class="btn-department-info" @click="deleteDepart">删除</el-tag>
          </template>
        </el-table-column>
      </el-table>
    </el-main>

    <el-dialog v-model="showAddDepart" title="新增部门" center width="800px">
      <DepartForm
        v-if="showAddDepart"
        destroy-on-close
        :parentDepartTree="parentDepartTree"
        :companyId="companyId"
        :companyName="companyName"
        @setShowForm="setShowAddDepart"
        @refreshList="getDepartInfo"
      />
    </el-dialog>
    <el-dialog v-model="showEditDepart" title="编辑部门" center width="800px">
      <DepartForm
        v-if="showEditDepart"
        destroy-on-close
        :isEdit="true"
        :editDepartInfo="editDepartInfo"
        :parentDepartTree="parentDepartTree"
        :companyId="companyId"
        :companyName="companyName"
        @setShowForm="setShowEditDepart"
        @refreshList="getDepartInfo"
      />
    </el-dialog>
  </el-container>
</template>

<script setup lang="ts">
import { ElMessage } from 'element-plus';
import { onMounted, ref, toRefs, watch } from 'vue';
import { sendRequest, TRequestParams } from '@/api/dashboard';
import DepartForm from './DepartForm.vue';
import { IDepart, IDepartTree, IParentDepart } from './types';

const departList = ref<IDepart[]>([]);
const departTreeList = ref<IDepartTree[]>([]);
const parentDepartTree = ref<IParentDepart[]>([]);
const isLoading = ref(true);
const showAddDepart = ref(false);
const showEditDepart = ref(false);
const editDepartInfo = ref<IDepart | null>(null);

interface IProps {
  companyId: string;
  companyName: string;
}

const props = defineProps<IProps>();
const { companyId, companyName } = toRefs(props);

watch(companyId, () => {
  getDepartInfo();
});

onMounted(() => {
  getDepartInfo();
});

watch(
  departList,
  newVal => {
    departTreeList.value = buildDepartTree(newVal);
    parentDepartTree.value = buildParentDepartTree(newVal);
  },
  { deep: true }
);

function buildDepartTree(data: IDepart[]): IDepartTree[] {
  // 创建哈希映射表
  const map = new Map<string, IDepartTree>();

  // 第一次遍历：创建所有节点的映射
  data.forEach(item => {
    map.set(item.id.toString(), {
      ...item,
      children: []
    });
  });

  // 第二次遍历：建立父子关系
  const tree: IDepartTree[] = [];
  data.forEach(item => {
    const currentNode = map.get(item.id.toString())!;

    if (item.parent_department_id === null) {
      tree.push(currentNode);
    } else {
      const parentNode = map.get(item.parent_department_id.toString());
      parentNode?.children.push(currentNode);
    }
  });

  return tree;
}

function buildParentDepartTree(data: IDepart[]): IParentDepart[] {
  // 创建哈希映射表
  const map = new Map<string, IParentDepart>();

  // 第一次遍历：创建所有节点的映射
  data.forEach(item => {
    map.set(item.id.toString(), {
      value: item.id.toString(),
      label: item.department_name,
      children: []
    });
  });

  // 第二次遍历：建立父子关系
  const tree: IParentDepart[] = [];
  data.forEach(item => {
    const currentNode = map.get(item.id.toString())!;

    if (item.parent_department_id === null) {
      tree.push(currentNode);
    } else {
      const parentNode = map.get(item.parent_department_id.toString());
      parentNode?.children.push(currentNode);
    }
  });

  return tree;
}

async function getDepartInfo() {
  const params: TRequestParams = {
    url: 'lookupbytwadmin',
    company_id: companyId.value,
    department_status: '正常'
  };
  const res = await sendRequest(params);
  if (!res.error_status) {
    departList.value = res.result?.data || [];
  }
  isLoading.value = false;
}

function editDepart(row: IDepart) {
  editDepartInfo.value = row;
  showEditDepart.value = true;
}

function deleteDepart() {
  ElMessage({
    message: '开发中,敬请期待...',
    type: 'warning'
  });
}
function addDepart() {
  showAddDepart.value = true;
}

function setShowAddDepart(value: boolean) {
  showAddDepart.value = value;
}

function setShowEditDepart(value: boolean) {
  showEditDepart.value = value;
}
</script>

<style scoped lang="scss">
.header-container {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  padding: 0 20px;
}
.company-form-item {
  justify-content: center;
  .el-form-item__content {
    flex: inherit;
  }
}
.company-dialog {
  margin-bottom: 20px;
}
.btn-department-info {
  cursor: pointer;
  margin: 0 8px;
}
.department-name {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.department-desc {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>

<style lang="scss">
.depart-container .el-overlay-dialog {
  top: 10%;
}
.custom-header-class {
  height: 60px;
}
.cell-depart-name {
  .cell {
    display: flex;
    align-items: center;
  }
}
</style>
