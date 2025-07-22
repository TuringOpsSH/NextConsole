<template>
    <el-container style="height: 100vh;">
        <el-aside width="81px">
            <next_console_menu></next_console_menu>
        </el-aside>

        <el-container>
            <el-header style="height:80px;">
                <next_console_page_header :components="component_list"></next_console_page_header>
            </el-header>
            <el-main>
                <router-view></router-view>
            </el-main>
        </el-container>
    </el-container>
</template>


<script setup>
import {ref} from 'vue'
import next_console_menu from '@/components/global/next_console_menu.vue'
import next_console_page_header from '@/components/global/next_console_page_header.vue'
const component_list = [
    {"name":"应用配置","url":"/next_console/config_center/app_config", "role":["admin","super_admin"]},
    {"name":"系统配置","url":"/next_console/config_center/system_config", "role":["admin","super_admin"]},
    {"name":"用户管理","url":"/next_console/config_center/user_manager", "role":["admin","super_admin"]},

]
</script>
<style scoped>
.el-container {
    height: 100vh;
}

.el-aside {
    height: 100%;
}

.el-header {
    height: 60px !important;
}
.el-main {
  --el-main-padding: 0;
  height:  calc(100vh - 80px);
}
</style>
