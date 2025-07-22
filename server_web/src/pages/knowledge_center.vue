<template>
  <el-container style="height: 100vh;">


    <el-header v-if="window_width > 600"
               style="padding: 0 !important;">
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
                <!--            <el-menu-item index="1">-->
                <!--              <el-image src="images/notice.svg" style="display: flex;align-items: center;width: 20px;height: 20px"/>-->
                <!--            </el-menu-item>-->

              </el-menu>

            </div>



          </div>
        </el-header>
    <el-main style="padding: 0">
            <router-view></router-view>
    </el-main>

  </el-container>

</template>




<script setup>
import {onMounted, onUnmounted, ref} from "vue";
import router from "@/router";
import {useRoute} from "vue-router";
import {show_flag_by_window_width} from "@/components/next_console/console/console";
const window_width = ref(window.innerWidth);

function updateWidth() {
  window_width.value = window.innerWidth;
}
const route = useRoute();
const current_index = route.path
const filteredComponents = ref([
  {
    name: "知识库管理",
    url: "/next_console/kg/kg_manage/list"
  },

])
onMounted(
    () => {

      window.addEventListener('resize', updateWidth);

    }
)
// 在组件卸载时移除监听器，防止内存泄漏
onUnmounted(() => {
  window.removeEventListener('resize', updateWidth);
});

</script >
<style scoped>


</style>
