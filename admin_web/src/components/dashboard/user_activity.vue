<script setup lang="ts">

import {useRoute} from "vue-router";
import {onMounted, ref} from "vue";
import {onBeforeUnmount} from "vue-demi";
import {
  changeRefreshRate,
  doc_download_count_tweened, doc_read_count_tweened,
  get_all_data,
  qa_count_tweened,
  refreshInterval,
  refreshRate,
  search_all_company_option,
  selectedTimeRange,
  session_count_tweened,
  targetCompany,
  user_company_list,
  uv_count_tweened,
} from "@/components/dashboard/user_activity";
import {user_is_next_console_admin} from "@/components/user_center/user_manage";
import {getInfo} from "@/utils/auth";

const route = useRoute();
const current_index = route.path
const filteredComponents = ref([
  {
    name: "运营指标",
    url: "/dashboard/user_activity"
  }

])


onMounted(async () => {

  let user_info = await getInfo()
  try{
    if (user_info?.["user_role"].includes("next_console_admin")
        || user_info?.["user_role"].includes("next_console_reader_admin")){
      user_is_next_console_admin.value = true
      await search_all_company_option()
    }
  }catch (e) {

  }

  await get_all_data()

  refreshInterval.value = setInterval(async () => {
    await get_all_data();
  }, refreshRate.value);
});

onBeforeUnmount(() => {
  if (refreshInterval) {
    clearInterval(refreshInterval.value);
  }
});

</script>

<template>
  <el-container style="height: 100vh">
    <el-header >
      <div class="next-console-admin-header">

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

              {{ component.name }}


            </el-menu-item>
          </el-menu>
        </div>
      </div>
    </el-header>
    <el-main>
      <el-scrollbar view-style="width:100%" wrap-style="width:100%">
        <div>
          <el-form :inline="true" class="demo-form-inline">
            <el-form-item label="统计时间" style="min-width: 200px">
              <el-select v-model="selectedTimeRange" placeholder="选择时间范围" @change="get_all_data" clearable >
                <el-option label="当天" value="today"></el-option>
                <el-option label="一周" value="week"></el-option>
                <el-option label="一月" value="month"></el-option>
                <el-option label="一季度" value="quarter"></el-option>
                <el-option label="当年" value="year"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="刷新频率" style="min-width: 200px">
              <el-select v-model="refreshRate" placeholder="选择刷新频率" @change="changeRefreshRate">
                <el-option label="从不" :value="0"></el-option>
                <el-option label="1分钟" :value="60000"></el-option>
                <el-option label="5分钟" :value="300000"></el-option>
                <el-option label="10分钟" :value="600000"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="公司" v-if="user_is_next_console_admin" style="min-width: 200px">
              <el-select v-model="targetCompany" placeholder="目标公司" @change="get_all_data" clearable
                         value-key="id"
              >
                <el-option v-for="(company,_) in user_company_list" :label="company.company_name"
                           :value="company.id"/>
              </el-select>
            </el-form-item>
          </el-form>
        </div>
        <div id="dashboard_area">
          <el-divider>
            用户
          </el-divider>
          <div id="dnu" class="next-console-chart"/>
          <div id="dnu_sd" class="next-console-chart"/>
          <div id="uv" ref="uv" class="next-console-chart-number">
            <div class="std-middle-box" style="width: 100%;justify-content: flex-start">
              <el-text class="chart-number">独立访客数</el-text>
            </div>
            <div class="std-middle-box" style="height: 100%">
              <el-text class="dynamic-number">{{uv_count_tweened.number.toFixed(0)}}</el-text>
            </div>

          </div>
          <div id="d1_retention" class="next-console-chart"/>
          <div id="all_retention" class="next-console-chart"/>
          <el-divider>
            AI工作台
          </el-divider>
          <div id="uv_hour" class="next-console-chart"/>
          <div id="uv_day" class="next-console-chart"/>
          <div id="avg_qa_retention"></div>
          <div id="qa_count" ref="qa" class="next-console-chart-number">
            <div class="std-middle-box" style="width: 100%;justify-content: flex-start">
              <el-text class="chart-number">总问答数</el-text>
            </div>
            <div class="std-middle-box" style="height: 100%">
              <el-text class="dynamic-number">{{qa_count_tweened.number.toFixed(0)}}</el-text>
            </div>

          </div>
          <div id="qa_hour" class="next-console-chart"/>
          <div id="qa_day" class="next-console-chart"/>
          <div id="avg_session_retention"></div>
          <div id="session_count" ref="session" class="next-console-chart-number">
            <div class="std-middle-box" style="width: 100%;justify-content: flex-start">
              <el-text class="chart-number">总会话数</el-text>
            </div>
            <div class="std-middle-box" style="height: 100%">
              <el-text class="dynamic-number">{{session_count_tweened.number.toFixed(0)}}</el-text>
            </div>

          </div>
          <div id="session_hour" class="next-console-chart"/>
          <div id="session_day" class="next-console-chart"/>
          <el-divider>
            资源库
          </el-divider>
          <div id="doc_view_count"  class="next-console-chart-number">
            <div class="std-middle-box" style="width: 100%;justify-content: flex-start">
              <el-text class="chart-number">文档查看数量</el-text>
            </div>
            <div class="std-middle-box" style="height: 100%">
              <el-text class="dynamic-number">{{doc_read_count_tweened.number.toFixed(0)}}</el-text>
            </div>
          </div>
          <div id="doc_view_top" class="next-console-chart"/>
          <div id="user_view_resource_top" class="next-console-chart"/>
          <div id="doc_download_count"  class="next-console-chart-number">
            <div class="std-middle-box" style="width: 100%;justify-content: flex-start">
              <el-text class="chart-number">文档下载数量</el-text>
            </div>
            <div class="std-middle-box" style="height: 100%">
              <el-text class="dynamic-number">{{doc_download_count_tweened.number.toFixed(0)}}</el-text>
            </div>
          </div>
          <div id="doc_download_top" class="next-console-chart"/>
          <div id="user_download_top" class="next-console-chart"/>
        </div>


      </el-scrollbar>
    </el-main>
    <el-footer >

    </el-footer>
  </el-container>
</template>

<style scoped>
.el-header {
  padding: 0 !important;
}
.next-console-chart-number{
  display: flex;
  min-width: 160px !important;
  height: 400px;
  width: 600px;
  padding: 6px;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
.next-console-chart{
  display: flex;
  padding: 6px;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
.dynamic-number{
  color: #1570ef;
  font-size: 48px;
  font-weight: 600;

}
#dashboard_area{
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  width: 100%;
  gap: 12px
}
.std-middle-box{
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
}
.chart-number{
  font-size: 20px;font-weight: 600;color: black
}
</style>
