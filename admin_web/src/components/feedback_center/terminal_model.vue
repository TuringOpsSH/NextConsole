<script setup lang="ts">
import {useRoute} from "vue-router";
import {ref} from "vue";

const route = useRoute();
const current_index = route.path
const filteredComponents = ref([
  {
    name: "检索模式",
    url: "/feedback/search_model"
  }
  ,{
    name: "终端模式",
    url: "/feedback/terminal_model"
  },{
    name: "会话模式",
    url: "/feedback/qa_model"
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
                          active-text-color="#175CD3"
            >

                {{ component.name }}


            </el-menu-item>
          </el-menu>
        </div>


      </div>
    </el-header>
    <el-main>
      <el-main>
        <el-scrollbar wrap-style="width: 100%" view-style="width: 100%">
          <el-empty description="火热开发中"></el-empty>
        </el-scrollbar>
      </el-main>
    </el-main>
    <el-footer></el-footer>
  </el-container>
</template>

<style scoped>
.el-header {
  --el-header-padding : 0 !important;
}
</style>
