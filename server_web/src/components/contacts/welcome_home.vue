<script setup lang="ts">

import {user_info} from "@/components/user_center/user";
</script>

<template>
  <el-container>
    <el-main style="height: calc(100vh - 120px) ; padding: 0 !important;">
      <div id="center-box">
        <div id="center-area">
          <div id="hello-world">
            <div class="">
              <el-text class="hello-text">
                你好，{{user_info?.user_nick_name}}
              </el-text>
            </div>
            <div>
              <el-text  class="hello-text"> 美好的生活值得期待！</el-text>
            </div>

          </div>
          <div id="recommend-area">

          </div>
        </div>
      </div>

    </el-main>

  </el-container>
</template>

<style scoped>
#center-box{
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  width: calc(100% - 48px);
  padding: 0 20px;

}
#center-area{
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: flex-start;
  gap: 32px;
}
#hello-world{
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: flex-start;
  gap: 12px;
  width: 100%;
}
.hello-text{
  font-size: 24px;
  line-height: 32px;
  font-weight: 600;
  color: #101828;
}
</style>
