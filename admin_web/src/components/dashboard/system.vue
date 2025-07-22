<script setup lang="ts">
import {Search} from "@element-plus/icons-vue";
import {useRoute} from "vue-router";
import {ref} from "vue";
const route = useRoute();
const current_index = route.path
const filteredComponents = ref([
  {
    name: "用户活跃度",
    url: "/dashboard/user_activity"
  }
  ,{
    name: "系统稳定性",
    url: "/dashboard/system"
  },{
    name: "成本费用",
    url: "/dashboard/cost_expenses"
  },
])
</script>

<template>
  <el-container style="height: 100vh">
    <el-header height="61px">
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
          <el-empty description="火热开发中"/>
    </el-main>
    <el-footer >

    </el-footer>
  </el-container>
</template>

<style scoped>
.el-header {
  padding: 0 !important;
}
</style>
