<template>
  <el-scrollbar view-style="width: 100%" wrap-class="width: 100%">
    <div class="main">

      <div class="body">
        <div class="title">403 error</div>
        <div >
          <el-text class="content">
            滴，前方禁止通行！
          </el-text>
        </div>
        <div class="tip">抱歉，暂无权限访问</div>
        <el-button plain icon="el-icon-back" class="back-btn" @click="goBack">返回首页</el-button>
      </div>


    </div>
  </el-scrollbar>
</template>

<script setup>

import router from "@/router";


async function goBack() {
  router.push({ path: '/' });
}



</script>

<style scoped>
.main {
  width: 100vw;
  height: 100vh;
  white-space: nowrap;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;

  .body{
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: flex-start;
    .title {
      font-size: 16px;
      color: #175CD3;
    }
    .content {
      font-weight: 600;
      font-size: 60px;
      color: #101828;
    }
    .tip {
      font-size: 20px;
      color: #475467;
      margin: 24px 0 48px;
    }
    .back-btn {
      min-width: 164px;
      min-height: 60px;
      font-size: 18px;
    }
    .std-button{
      display: flex;
      width: 80vw;
      padding: 12px 20px 12px 20px;
      gap: 8px;
      border-radius: 8px;
      border: 1px solid #1570EF;
      align-items: center;
      justify-content: center;
      background: #1570EF;
      box-shadow: 0 1px 2px 0 #1018280D;
      cursor: pointer;

    }

  }

}

@media (max-width: 600px) {
  .main {
    width: 100vw;
    height: 100vh;
    white-space: nowrap;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;

    .body{
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: flex-start;
      .title {
        font-size: 16px;
        color: #175CD3;
      }
      .content {
        font-size: 36px;
        font-weight: 600;
        line-height: 44px;
        letter-spacing: -0.02em;
        text-align: left;
        color: #101828;

      }
      .tip {
        font-size: 18px;
        font-weight: 400;
        line-height: 28px;
        text-align: left;
        color: #475467;
        margin: 16px 0 48px;
      }
      .back-btn {
        min-width: 164px;
        min-height: 60px;
        font-size: 18px;
      }
    }

  }
}
</style>
