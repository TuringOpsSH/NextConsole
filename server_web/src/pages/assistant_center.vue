<template>

  <el-container style="height: 100vh;">


    <el-container class="main_container">
      <el-header height="60px" style="padding: 0">
        <div class="assistant-center-header">
          <div style="margin-left: 24px">
            <el-menu mode="horizontal" :ellipsis="false" :router="true" style="height: 60px">
              <el-menu-item v-for="item in component_list"
                            :key="item.url"
                            :index="item.url" :to="item.url"

              >
                <el-text style="font-size: 16px;font-weight: 600;line-height: 24px;
                 ">
                  {{item.name}}
                </el-text>

              </el-menu-item>
            </el-menu>
          </div>
        </div>
      </el-header>


      <el-main >
        <router-view></router-view>
      </el-main>
    </el-container>
  </el-container>

</template>




<script setup>

import {onMounted} from "vue";
import router from "@/router";
const component_list = [
  {"name":"助手列表","url":"/next_console/assistant/assistant_manage"},
  {"name":"助手商店","url":"/next_console/assistant/assistant_shop"},
]
onMounted(
    () => {
      router.push(component_list[0].url)
    }
)
</script >
<style scoped>


.main_container{
  height: 100vh;
  width: 100vw;
}

.el-main {
  --el-main-padding: 0;
  height:  calc(100vh - 80px);
}


.assistant-center-header{
  height: 60px;
  border-bottom: 1px solid #D0D5DD;
  display: flex;
  justify-content: space-between;
}
.search-box-button-icon{
  border: 0 !important;
  border-radius: 8px !important;
  padding: 0;
  width: 40px;
}
.assistant-center-search {
  width: 560px;
  border-radius: 8px;
  flex-grow: 1;
  height: 40px;
  border: 1px solid #D0D5DD;
  box-shadow: 0 1px 2px 0 #1018280D;

}
.assistant-center-search :deep(.el-input-group__append){
  box-shadow: none;

  background-color: #FFFFFF;
  border-radius: 8px;
}
.assistant-center-search :deep(.el-input-group__prepend){
  box-shadow: none;

  background-color: #FFFFFF;
  border-radius: 8px;
}
.assistant-center-search :deep(.el-input__wrapper){
  box-shadow: none;
}
.el-menu--horizontal.el-menu{
  border-bottom: 0;

}
</style>
