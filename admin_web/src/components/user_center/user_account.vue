<script setup lang="ts">
import {useRoute} from "vue-router";
import {onMounted, ref} from "vue";
import {show_flag_by_window_width} from "@/components/next_console/console";
import {change_assistant_drawer, dialog_v_assistant_list} from "@/components/next_console/assistant";
import {ArrowLeft, ArrowRight} from "@element-plus/icons-vue";
import {lookup_user_token_sta, lookup_user_token_used_current} from "@/api/user_center";

import {CouponInfo, UserAccount, UserTokenSta} from "@/types/users";

const route = useRoute();
const current_index = route.path
const filteredComponents = ref([
  {
    name: "账户资料",
    url: "/next_console/user_center/user_info"
  },
  {
    name: "费用信息",
    url: "/next_console/user_center/user_account"
  }
])
const CurrentUserAccount = ref<UserAccount>({
  user_id: null,
  create_time: null,
  update_time: null,
  token_used_point_cnt_cycle: null,
  token_used_point_cnt_cycle_str: '',
  token_used_point_cnt_total: null,
  token_point_bal: null,
  token_point_fix_bal: null,

})
const CurrentUserTokenSta = ref<UserTokenSta[]>([])
const CurrentUserTokenStaTotal = ref(0)
const CurrentUserTokenStaPageNum = ref(1)
const CurrentUserTokenStaPageSize = ref(10)
const CurrentCouponInfo = ref<CouponInfo>({
  coupon_id: null,
  coupon_name: null,
  coupon_text: null,
  coupon_desc: null,
  coupon_token_points: null,
  coupon_start_date: null,
  coupon_end_date: null,
  coupon_status: null,
  coupon_type: null,
  coupon_used_cnt_limit: null,
  coupon_used_cnt: null,
  coupon_last_used_time: null,
  create_time: null,
  update_time: null,
})

async function get_user_token_sta() {
  let res = (await lookup_user_token_sta(
      {
        page_num: CurrentUserTokenStaPageNum.value,
        page_size: CurrentUserTokenStaPageSize.value
      }
  )).result
  CurrentUserTokenSta.value = res.data
  CurrentUserTokenStaTotal.value = res.total
  // 格式化数据
  for (let i = 0; i < CurrentUserTokenSta.value.length; i++) {
    CurrentUserTokenSta.value[i].sta_date = format_date(CurrentUserTokenSta.value[i].sta_date)
    CurrentUserTokenSta.value[i].rate_dist_obj = JSON.parse(CurrentUserTokenSta.value[i].rate_dist)
    // 将rate_dist_obj的值转换为百分比
    let sum_all = 0
    for (let key in CurrentUserTokenSta.value[i].rate_dist_obj) {
      sum_all += CurrentUserTokenSta.value[i].rate_dist_obj[key]
    }
    for (let key in CurrentUserTokenSta.value[i].rate_dist_obj) {
      CurrentUserTokenSta.value[i].rate_dist_obj[key] = Number(
          (CurrentUserTokenSta.value[i].rate_dist_obj[key] / sum_all * 100).toFixed(2))
    }


  }

}
const handleSizeChange = (val: number) => {
  CurrentUserTokenStaPageSize.value = val
  get_user_token_sta()
}
const handleCurrentChange = (val: number) => {
  CurrentUserTokenStaPageNum.value = val
  get_user_token_sta()
}

function format_date(date_str: string) {
  try {
    const date = new Date(date_str);
    return new Intl.DateTimeFormat('en-CA', { // 使用'CA'是因为加拿大的日期格式是YYYY-MM-DD
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
    }).format(date)
  }catch (e) {
    return "unknown"
  }
  }


onMounted(async () => {

  CurrentUserAccount.value = (
      await lookup_user_token_used_current({
  })).result
  try {
    CurrentUserAccount.value.token_used_point_cnt_cycle_str = CurrentUserAccount.value.token_used_point_cnt_cycle.toLocaleString('en-US');
  }
  catch (e) {
    console.log(e)
  }

  await get_user_token_sta()
})

</script>

<template>

  <el-container style="height: 100vh">
    <el-header height="61px" v-if="show_flag_by_window_width">
      <div class="next-console-header">

        <div class="component-box">
          <el-menu
              :default-active="current_index"
              class="el-menu-demo"
              mode="horizontal"
              router
              :ellipsis="false"

          >
            <el-menu-item v-for="component in filteredComponents"

                          :index=component.url
                          class="menu-header-item"
            >
              <el-text class="component-name">
                {{ component.name }}
              </el-text>

            </el-menu-item>
          </el-menu>
        </div>


        <div class="right-box">
          <el-menu :default-active="current_index"
                   class="el-menu-demo"
                   mode="horizontal"
                   :ellipsis="false"
          >
            <el-menu-item index="1">
              <el-image src="images/notice.svg" style="display: flex;align-items: center;width: 20px;height: 20px"/>
            </el-menu-item>

          </el-menu>

        </div>



      </div>
    </el-header>

    <el-main>
      <el-scrollbar wrap-style="width: 100%" view-style="width: 100%">
        <div class="user-account-main-box">

          <div class="user-account-main">
            <div class="user-account-header">
              <div class="user-account-header-info">
                <div>
                  <el-text class="user-account-article">
                    公测期间免费100万Token点数，用完需要重置Token点数，请积极参与运营活动，赢取丰厚活跃礼券！
                  </el-text>
                </div>
                <div>
                  <el-button class="reset-bottom">
                    <el-text class="reset-bottom-text">
                      重置
                    </el-text>
                  </el-button>
                </div>
              </div>
              <div class="user-account-header-summary">
                <div>
                  <el-text>到期时间 2024-12-31 ，距离到期还有 200 天</el-text>
                </div>
                <div>
                  <el-progress :percentage="CurrentUserAccount.token_used_point_cnt_cycle / 1000000 * 100"
                               color="#079455"/>
                </div>
                <div>
                  <el-text>
                    已用 {{CurrentUserAccount.token_used_point_cnt_cycle_str}} Token 点数/ 总计 1,000,000 Token 点数
                  </el-text>
                </div>
              </div>

            </div>
            <div class="user-account-detail">
              <div class="user-account-detail-title">
                <el-text class="user-account-detail-title-text">费用详情</el-text>
                <el-tag round style="margin-left: 8px">
                  {{CurrentUserTokenStaTotal}} 条
                </el-tag>
              </div>
              <div class="user-account-detail-table" >
                <el-table  style="width: 100%" :highlight-current-row="true"
                           :data="CurrentUserTokenSta"

                >
                  <el-table-column prop="sta_date" label="时间"   />
                  <el-table-column prop="qa_cnt" label="日问答对数"   />
                  <el-table-column prop="rag_cnt" label="日RAG调用数" />
                  <el-table-column prop="msg_token_used_cnt" label="日消耗Token数" />
                  <el-table-column prop="msg_token_used_point_cnt" label="日消耗Token点数" />
                  <el-table-column prop="rag_token_used_cnt" label="日RAG 消耗Token数" />
                  <el-table-column prop="rag_token_used_point_cnt" label="日RAG 消耗Token点数" />
                  <el-table-column prop="rate_dist" label="Token 倍率分布" >
                    <template #default="{row}">

                        <div v-if="row.rate_dist_obj" style="display: flex;gap: 3px;flex-direction: column">
                          <el-progress v-for="(value, key) in row.rate_dist_obj" :text-inside="true"
                                       :stroke-width="18"
                                       type="line"
                                       :striped="true"
                                       :striped-flow="true"
                                       :duration="10"
                                       :percentage="value">
                            <template #default="{percentage}">
                              {{key}}: {{percentage}}%
                            </template>

                          </el-progress>


                      </div>
                    </template>
                  </el-table-column>
                </el-table>
              </div>

            </div>
          </div>

        </div>
      </el-scrollbar>
    </el-main>

    <el-footer>
      <div class="user-account-detail-pagination">
        <el-pagination
            layout=" prev, pager, next"
            :total="CurrentUserTokenStaTotal"
            :page-size="CurrentUserTokenStaPageSize"
            :current-page="CurrentUserTokenStaPageNum"
            @update:page-size="handleSizeChange"
            @update:current-page="handleCurrentChange"
        />
      </div>
    </el-footer>
  </el-container>

</template>

<style scoped>
.el-header {
  padding: 0 !important;
}

.el-main {
  padding: 0 !important;

}
.el-menu--horizontal.el-menu{
  border-bottom: 0;
}

.user-account-main-box{
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: row;

}
.user-account-main{


  display: flex;
  flex-direction: column;

}
.user-account-header{
  border-bottom: 1px solid #D0D5DD;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.user-account-header-info{
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}
.user-account-article{

  font-size: 20px;
  font-weight: 600;
  line-height: 30px;
  text-align: left;
  color: #101828;
}
.reset-bottom{
  width: 56px;
  height: 36px;
  background: #1570EF;

  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  box-shadow: 0 1px 2px 0 #1018280D;
  border: 1px solid #1570EF;
}
.reset-bottom-text{
  color: #FFFFFF;
  font-size: 14px;
  font-weight: 600;
  line-height: 20px;
  text-align: left;
}
.user-account-detail{
  display: flex;
  flex-direction: column;
  gap: 24px;
}
.user-account-detail-title{
  border-bottom: 1px solid #EAECF0;
  padding: 16px;
}
.user-account-detail-title-text{
  font-size: 18px;
  font-weight: 600;
  line-height: 28px;
  text-align: left;
  color: #101828;

}
.user-account-detail-table{
  min-height: 400px;
}
.user-account-detail-pagination{
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
