<script setup lang="ts">

</script>

<template>
  <div id="login-main-box">

    <div id="login-main-image"/>
    <div id="login-main-overlay"></div>
    <div id="login-main-content" v-show="true">
      <div class="std-middle-box">
        <el-image src="images/login_star.svg" style="width: 80px;height: 80px"/>
      </div>
      <div class="std-middle-box">
        <el-text style="font-size: 72px;font-weight: 600;line-height: 90px;color: white">
          Start turning your ideas into reality.
        </el-text>
      </div>
      <div class="std-middle-box">
        <el-text style="font-size: 20px;line-height: 30px;font-weight: 500;color: #B2DDFF">
          Create a free account and get full access to all features for 30-days.
          No credit card needed. Trusted by over 4,000 professionals.
        </el-text>
      </div>
      <div class="std-middle-box">
        <div>
          <el-image src="images/login_sub_view2.svg" ></el-image>
        </div>
        <div>
          <el-image src="images/login_sub_view.svg" ></el-image>
        </div>
      </div>

    </div>

  </div>
</template>

<style scoped>
#login-main-box{
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  width: 50vw;
}
#login-main-image{
  position: absolute;
  top: 0;
  left: 50%;
  width: 50vw;
  height: 100%;
  background-image: url("@/../public/images/login_back.jpg"); /* 替换为你的背景图片URL */
  background-size: cover;
  background-position: center;


}
#login-main-overlay {
  position: absolute;
  top: 0;
  left: 50%;
  width: 50vw;
  height: 100%;
  opacity: 80%;
  background: linear-gradient(135deg, #72EDF2 0%, #5151E5 100%);

}
#login-main-content{
  position: relative;
  z-index: 1;
  color: white;
  text-align: center;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  gap: 48px;
  width: calc(50vw - 120px);

}
</style>
