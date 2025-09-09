<script setup lang="ts">
import { ElMessage } from 'element-plus';
import { reactive, ref, watch } from 'vue';
import { getCampaignApi, searchCampaignDataApi, updateCampaignApi } from '@/api/user-center';
import router from "@/router";
const currentPane = ref('属性');
const props = defineProps({
  campaignId: {
    type: Number,
    default: 0
  },
  viewPane: {
    type: String,
    default: 'meta'
  }
});
const currentCampaignForm = reactive({
  id: null,
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
const currentCampaignFormRule = {
  campaign_name: [{ required: true, message: '请输入活动名称', trigger: 'blur' }],
  marketing_code: [{ required: false, pattern: /^[a-zA-Z0-9]+$/, message: '请以字母与数字组织', trigger: 'blur' }]
};
const currentCampaignFormRef = ref(null);
const editorModel = ref(false);
const currentCampaignData = ref<any[]>([]);
const currentPageSize = ref(50);
const currentPageNum = ref(1);
const currentTotal = ref(0);
async function getCurrentCampaignDetail(campaignId: number) {
  const res = await getCampaignApi({
    campaign_id: campaignId
  });
  if (!res.error_status) {
    Object.assign(currentCampaignForm, res.result);
  }
}
async function cancelUpdate() {
  editorModel.value = false;
  const res = await getCampaignApi({
    campaign_id: props.campaignId
  });
  if (!res.error_status) {
    Object.assign(currentCampaignForm, res.result);
  }
}
async function saveUpdate() {
  const res = await updateCampaignApi({
    campaign_id: props.campaignId,
    ...currentCampaignForm
  });
  if (!res.error_status) {
    editorModel.value = false;
    Object.assign(currentCampaignForm, res.result);
    ElMessage({
      message: '更新成功',
      type: 'success'
    });
  }
}
async function searchCampaignData(campaignId: number) {
  const res = await searchCampaignDataApi({
    campaign_id: campaignId,
    page_size: currentPageSize.value,
    page_num: currentPageNum.value
  });
  if (!res.error_status) {
    currentCampaignData.value = res.result.data;
    currentTotal.value = res.result.total;
  } else {
    currentCampaignData.value = [];
    currentTotal.value = 0;
  }
}
async function handlePaneChange(name: string) {
  if (name == 'data') {
    searchCampaignData(props.campaignId);
  } else if (name == 'meta') {
    getCurrentCampaignDetail(props.campaignId);
  }
  router.replace({
    query: {
      viewPane: name
    }
  });
}
async function handleSizeChange(newSize: number) {
  currentPageSize.value = newSize;
  searchCampaignData(props.campaignId);
}
async function handleNumberChange(newPage: number) {
  currentPageNum.value = newPage;
  searchCampaignData(props.campaignId);
}
watch(
  () => props.campaignId,
  newVal => {
    getCurrentCampaignDetail(newVal);
  },
  { immediate: true }
);
watch(
  () => props.viewPane,
  newVal => {
    currentPane.value = newVal;
    handlePaneChange(newVal);
  },
  { immediate: true }
);
</script>

<template>
  <el-container>
    <el-main>
      <el-tabs v-model="currentPane" @tab-change="handlePaneChange">
        <el-tab-pane name="meta" label="属性">
          <el-scrollbar>
            <div class="pane-area">
              <el-form ref="currentCampaignFormRef" :model="currentCampaignForm" :rules="currentCampaignFormRule">
                <el-form-item prop="id" label="活动ID">
                  <el-input v-model="currentCampaignForm.id" disabled />
                </el-form-item>
                <el-form-item prop="campaign_name" label="活动名称" required>
                  <el-input
                    v-model="currentCampaignForm.campaign_name"
                    placeholder="活动名称"
                    clearable
                    :disabled="!editorModel"
                  />
                </el-form-item>
                <el-form-item prop="marketing_code" label="营销代码">
                  <el-input
                    v-model="currentCampaignForm.marketing_code"
                    placeholder="不输入则系统自动生成"
                    clearable
                    :disabled="!editorModel"
                  />
                </el-form-item>
                <el-form-item prop="campaign_desc" label="活动描述">
                  <el-input
                    v-model="currentCampaignForm.campaign_desc"
                    placeholder="活动描述"
                    clearable
                    type="textarea"
                    :rows="5"
                    :disabled="!editorModel"
                  />
                </el-form-item>
                <el-form-item prop="campaign_type" label="活动类型">
                  <el-select
                    v-model="currentCampaignForm.campaign_type"
                    placeholder="请选择或者创建活动类型"
                    clearable
                    filterable
                    allow-create
                    :disabled="!editorModel"
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
                    v-model="currentCampaignForm.target_audience"
                    placeholder="请选择或者创建目标客群"
                    clearable
                    filterable
                    allow-create
                    :disabled="!editorModel"
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
                    v-model="currentCampaignForm.campaign_budget"
                    :max="1000000"
                    :min="0"
                    :step="50"
                    show-input
                    :show-input-controls="false"
                    :disabled="!editorModel"
                  />
                </el-form-item>
                <el-form-item prop="channel" label="活动渠道">
                  <el-select
                    v-model="currentCampaignForm.channel"
                    placeholder="请选择或者创建活动渠道"
                    clearable
                    filterable
                    allow-create
                    :disabled="!editorModel"
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
                    v-model="currentCampaignForm.begin_time"
                    type="datetime"
                    placeholder="选择日期时间"
                    :clearable="true"
                    :disabled="!editorModel"
                  />
                </el-form-item>
                <el-form-item prop="end_time" label="活动结束时间">
                  <el-date-picker
                    v-model="currentCampaignForm.end_time"
                    type="datetime"
                    placeholder="选择日期时间"
                    :clearable="true"
                    :disabled="!editorModel"
                  />
                </el-form-item>
                <el-form-item prop="campaign_status" label="活动状态">
                  <el-select
                    v-model="currentCampaignForm.campaign_status"
                    placeholder="请选择活动状态"
                    clearable
                    :disabled="!editorModel"
                  >
                    <el-option label="待启动" value="待启动" />
                    <el-option label="进行中" value="进行中" />
                    <el-option label="已结束" value="已结束" />
                    <el-option label="已暂停" value="已暂停" />
                    <el-option label="已取消" value="已取消" />
                  </el-select>
                </el-form-item>
              </el-form>
            </div>
          </el-scrollbar>
          <div>
            <el-button v-show="!editorModel" type="primary" text @click="editorModel = true"> 编辑 </el-button>
            <el-button v-show="editorModel" type="info" text @click="cancelUpdate"> 取消 </el-button>
            <el-popconfirm title="确认更新属性数据？" @confirm="saveUpdate">
              <template #reference>
                <el-button type="primary" text> 保存 </el-button>
              </template>
            </el-popconfirm>
          </div>
        </el-tab-pane>
        <el-tab-pane name="data" label="数据">
          <el-table :data="currentCampaignData" border height="calc(100vh - 240px)" stripe>
            <el-table-column prop="id" label="ID" width="120" />
            <el-table-column prop="invite_type" label="入口地址" width="180" />
            <el-table-column prop="view_user_id" label="用户ID" width="120" />
            <el-table-column prop="view_client_id" label="浏览器指纹" width="280" />
            <el-table-column prop="invite_status" label="状态" width="120" />
            <el-table-column prop="begin_register" label="开始注册" width="120" />
            <el-table-column prop="finish_register" label="完成注册" width="120" />
            <el-table-column prop="create_time" label="创建时间" width="180" />
            <el-table-column prop="update_time" label="更新时间" width="180" />
          </el-table>
          <el-pagination
            size="small"
            :page-size="currentPageSize"
            :page-sizes="[10, 50, 100, 200]"
            :current-page="currentPageNum"
            :total="currentTotal"
            layout="total, sizes, prev, pager, next"
            style="margin-top: 24px"
            @size-change="handleSizeChange"
            @current-change="handleNumberChange"
          />
        </el-tab-pane>
      </el-tabs>
    </el-main>
  </el-container>
</template>

<style scoped>
.pane-area {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 200px);
}
</style>
