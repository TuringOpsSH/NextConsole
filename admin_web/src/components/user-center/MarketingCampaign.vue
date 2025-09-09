<script setup lang="ts">
import { Search } from '@element-plus/icons-vue';
import { ElMessage } from 'element-plus';
import { onMounted, reactive, ref } from 'vue';
import { createCampaignApi, deleteCampaignApi, searchCampaignApi} from '@/api/user-center';
import router from '@/router';
const campaignList = ref([]);
const campaignListLoading = ref(false);
const campaignListPage = ref(1);
const campaignListPageSize = ref(10);
const campaignListTotal = ref(0);
const campaignKeyword = ref('');
const campaignTargetType = ref([]);
const campaignTargetStatus = ref([]);
const showNewCampaignFlag = ref(false);
const newCampaignForm = reactive({
  campaign_name: '',
  campaign_desc: '',
  campaign_type: '',
  target_audience: '',
  campaign_budget: '',
  marketing_code: '',
  channel: '',
  begin_time: '',
  end_time: '',
  campaign_status: ''
});
const newCampaignFormRef = ref(null);
const newCampaignFormRule = {
  campaign_name: [{ required: true, message: '请输入活动名称', trigger: 'blur' }],
  marketing_code: [{ required: false, pattern: /^[a-zA-Z0-9]+$/, message: '请以字母与数字组织', trigger: 'blur' }]
};
async function searchCampaign() {
  campaignListLoading.value = true;
  const res = await searchCampaignApi({
    page_num: campaignListPage.value,
    page_size: campaignListPageSize.value,
    campaign_keyword: campaignKeyword.value,
    campaign_type: campaignTargetType.value,
    campaign_status: campaignTargetStatus.value
  });
  if (!res.error_status) {
    campaignList.value = res.result.data;
    campaignListTotal.value = res.result.total;
  } else {
    campaignList.value = [];
    campaignListTotal.value = 0;
  }
  campaignListLoading.value = false;
}
async function handleCurrentChange(page) {
  campaignListPage.value = page;
  await searchCampaign();
}
async function handleSizeChange(size) {
  campaignListPageSize.value = size;
  await searchCampaign();
}
async function submitNewCampaign() {
  if (!newCampaignFormRef.value) {
    return;
  }
  if (!(await newCampaignFormRef.value.validate())) {
    return;
  }
  // 提交新活动
  const res = await createCampaignApi({
    ...newCampaignForm
  });
  if (!res.error_status) {
    // 提交成功
    showNewCampaignFlag.value = false;
    newCampaignForm.campaign_name = '';
    newCampaignForm.campaign_desc = '';
    newCampaignForm.campaign_type = '';
    newCampaignForm.target_audience = '';
    newCampaignForm.campaign_budget = '';
    newCampaignForm.channel = '';
    newCampaignForm.begin_time = '';
    newCampaignForm.end_time = '';
    newCampaignForm.campaign_status = '';
    newCampaignForm.marketing_code = '';
    searchCampaign();
    ElMessage.success('新活动创建成功');
  } else {
    // 提交失败
  }
}
async function deleteTargetCampaign(campaignId: number) {
  if (!campaignId) {
    return;
  }
  const res = deleteCampaignApi({
    campaign_id: campaignId
  });
  if (!(await res).error_status) {
    // 删除成功
    ElMessage.success('删除成功');
    searchCampaign();
  }
}
async function editCampaign(campaignId: number) {
  if (!campaignId) {
    return;
  }
  router.push({
    name: 'marketing_campaign_detail',
    params: {
      campaign_id: campaignId
    }
  });
}
onMounted(async () => {
  searchCampaign();
});
</script>

<template>
  <el-container>
    <el-header height="60px">
      <div class="header">
        <div class="header-left">
          <h3>活动列表</h3>
        </div>
        <div class="header-right">
          <el-input
            v-model="campaignKeyword"
            :prefix-icon="Search"
            placeholder="搜索历史活动"
            clearable
            @clear="searchCampaign"
            @click="searchCampaign"
            @keydown.enter.prevent="searchCampaign"
          />
          <el-button type="primary" @click="showNewCampaignFlag = true">新建活动</el-button>
        </div>
      </div>
    </el-header>
    <el-main>
      <el-table v-loading="campaignListLoading" :data="campaignList" border stripe height="calc(100vh - 240px)">
        <el-table-column type="selection" width="55" />
        <el-table-column prop="id" label="活动ID" width="120" />
        <el-table-column prop="marketing_code" label="营销编码" width="120" />
        <el-table-column prop="campaign_name" label="活动名称" width="180" />
        <el-table-column prop="campaign_status" label="活动状态" width="120" />
        <el-table-column prop="campaign_desc" label="活动描述" width="180" />
        <el-table-column prop="campaign_type" label="活动类型" width="180" />
        <el-table-column prop="target_audience" label="目标客群" width="180" />
        <el-table-column prop="campaign_budget" label="活动预算" width="180" />
        <el-table-column prop="channel" label="活动渠道" width="180" />
        <el-table-column prop="actual_cost" label="实际花费" width="180" />
        <el-table-column prop="begin_time" label="活动开始时间" width="180" />
        <el-table-column prop="end_time" label="活动结束时间" width="180" />
        <el-table-column prop="user_id" label="创建人" width="120" />
        <el-table-column prop="create_time" label="创建时间" width="180" />
        <el-table-column prop="update_time" label="创建时间" width="180" />
        <el-table-column prop="operation" label="操作" width="180" fixed>
          <template #default="{ row }">
            <el-button text type="primary" @click="editCampaign(row.id)">编辑</el-button>
            <el-popconfirm title="确认删除活动信息？" @confirm="deleteTargetCampaign(row.id)">
              <template #reference>
                <el-button text type="danger">删除</el-button>
              </template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>
    </el-main>
    <el-footer>
      <el-pagination
        size="small"
        :current-page="campaignListPage"
        :page-size="campaignListPageSize"
        :total="campaignListTotal"
        :page-sizes="[10, 20, 30, 40]"
        layout="total, sizes, prev, pager, next, jumper"
        @current-change="handleCurrentChange"
        @size-change="handleSizeChange"
      />
    </el-footer>
  </el-container>
  <el-dialog v-model="showNewCampaignFlag" title="创建新活动">
    <el-form ref="newCampaignFormRef" :model="newCampaignForm" :rules="newCampaignFormRule" label-position="top">
      <el-form-item prop="campaign_name" label="活动名称" required>
        <el-input v-model="newCampaignForm.campaign_name" placeholder="活动名称" clearable />
      </el-form-item>
      <el-form-item prop="marketing_code" label="营销代码">
        <el-input v-model="newCampaignForm.marketing_code" placeholder="不输入则系统自动生成" clearable />
      </el-form-item>
      <el-form-item prop="campaign_desc" label="活动描述">
        <el-input v-model="newCampaignForm.campaign_desc" placeholder="活动描述" clearable type="textarea" :rows="5" />
      </el-form-item>
      <el-form-item prop="campaign_type" label="活动类型">
        <el-select
          v-model="newCampaignForm.campaign_type"
          placeholder="请选择或者创建活动类型"
          clearable
          filterable
          allow-create
        >
          <el-option label="新客获取" value="新客获取" />
          <el-option label="老客留存" value="老客留存" />
          <el-option label="促销活动" value="促销活动" />
          <el-option label="季节性活动" value="季节性活动" />
          <el-option label="品牌推广" value="品牌推广" />
          <el-option label="限时抢购" value="限时抢购" />
          <el-option label="拼团活动" value="拼团活动" />
          <el-option label="邀请奖励" value="邀请奖励" />
          <el-option label="内容征集" value="内容征集" />
          <el-option label="会员日" value="会员日" />
          <el-option label="周年庆" value="周年庆" />
          <el-option label="首单优惠" value="首单优惠" />
          <el-option label="满减活动" value="满减活动" />
          <el-option label="积分兑换" value="积分兑换" />
          <el-option label="抽奖活动" value="抽奖活动" />
          <el-option label="新品试用" value="新品试用" />
          <el-option label="节日特惠" value="节日特惠" />
          <el-option label="直播专享" value="直播专享" />
          <el-option label="社群专享" value="社群专享" />
          <el-option label="员工内购" value="员工内购" />
          <el-option label="公益营销" value="公益营销" />
        </el-select>
      </el-form-item>
      <el-form-item prop="target_audience" label="目标客群">
        <el-select
          v-model="newCampaignForm.target_audience"
          placeholder="请选择或者创建目标客群"
          clearable
          filterable
          allow-create
        >
          <el-option label="新用户" value="新用户" />
          <el-option label="老用户" value="老用户" />
          <el-option label="高价值用户" value="高价值用户" />
          <el-option label="潜在用户" value="潜在用户" />
          <el-option label="流失用户" value="流失用户" />
          <el-option label="学生群体" value="学生群体" />
          <el-option label="白领群体" value="白领群体" />
          <el-option label="一线城市" value="一线城市" />
          <el-option label="二三线城市" value="二三线城市" />
          <el-option label="下沉市场" value="下沉市场" />
          <el-option label="VIP会员" value="VIP会员" />
          <el-option label="企业客户" value="企业客户" />
          <el-option label="跨境用户" value="跨境用户" />
          <el-option label="特定行业" value="特定行业" />
          <el-option label="兴趣社群" value="兴趣社群" />
          <el-option label="特定设备用户" value="特定设备用户" />
          <el-option label="特定区域" value="特定区域" />
        </el-select>
      </el-form-item>
      <el-form-item prop="campaign_budget" label="活动预算">
        <el-slider
          v-model="newCampaignForm.campaign_budget"
          :max="1000000"
          :min="0"
          :step="50"
          show-input
          :show-input-controls="false"
        />
      </el-form-item>
      <el-form-item prop="channel" label="活动渠道">
        <el-select
          v-model="newCampaignForm.channel"
          placeholder="请选择或者创建活动渠道"
          clearable
          filterable
          allow-create
        >
          <el-option label="线上渠道" value="线上渠道" />
          <el-option label="线下渠道" value="线下渠道" />
          <el-option label="社交媒体" value="社交媒体" />
          <el-option label="电子邮件" value="电子邮件" />
          <el-option label="短信营销" value="短信营销" />
          <el-option label="搜索引擎" value="搜索引擎" />
          <el-option label="移动应用" value="移动应用" />
          <el-option label="网站推广" value="网站推广" />
          <el-option label="线下活动" value="线下活动" />
        </el-select>
      </el-form-item>
      <el-form-item prop="begin_time" label="活动开始时间">
        <el-date-picker
          v-model="newCampaignForm.begin_time"
          type="datetime"
          placeholder="选择日期时间"
          :clearable="true"
        />
      </el-form-item>
      <el-form-item prop="end_time" label="活动结束时间">
        <el-date-picker
          v-model="newCampaignForm.end_time"
          type="datetime"
          placeholder="选择日期时间"
          :clearable="true"
        />
      </el-form-item>
      <el-form-item prop="campaign_status" label="活动状态">
        <el-select v-model="newCampaignForm.campaign_status" placeholder="请选择活动状态" clearable>
          <el-option label="待启动" value="待启动" />
          <el-option label="进行中" value="进行中" />
          <el-option label="已结束" value="已结束" />
          <el-option label="已暂停" value="已暂停" />
          <el-option label="已取消" value="已取消" />
        </el-select>
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="showNewCampaignFlag = false">取消</el-button>
      <el-button type="primary" @click="submitNewCampaign">确定</el-button>
    </template>
  </el-dialog>
</template>

<style scoped>
.header {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
}
.header-right {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 12px;
}
</style>
