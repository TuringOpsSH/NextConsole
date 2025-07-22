<script setup lang="ts">
  import {ref} from "vue";
  const is_small_screen = ref(window.innerWidth < 768)
  const wx_program_dia = ref(false)
  const person_version_dia = ref(false)
  const community_dia = ref(false)
  const nodeEnv = import.meta.env.VITE_APP_NODE_ENV
</script>

<template>
  <div v-if="is_small_screen" class="small-search-footer">
    <div class="footer-item">
      <div>
        <el-text class="search-link" @click="wx_program_dia=true">小程序</el-text>
      </div>
      <div>
        <el-text class="search-link" @click="person_version_dia=true">社区版</el-text>
      </div>
      <div>
        <el-text class="search-link" @click="community_dia=true">加入社区</el-text>
      </div>
    </div>
    <div class="footer-item" >
      <div class="std-div" v-show="nodeEnv != 'private'">
        <el-link class="police-link" href="https://beian.miit.gov.cn" :underline="false">
          沪ICP备2024044866号-1
        </el-link>
      </div>
    </div>
  </div>
  <div style="display: flex;align-items: flex-end;justify-content: center;gap: 16px; height: 50px;" v-else>
    <div class="footer-item">
      <div>
        <el-text class="search-link" @click="wx_program_dia=true">小程序</el-text>
      </div>
      <div>
        <el-text class="search-link" @click="person_version_dia=true">社区版</el-text>
      </div>
      <div>
        <el-text class="search-link" @click="community_dia=true">加入社区</el-text>
      </div>
    </div>
    <div class="footer-item" style="border-left: 1px solid #D0D5DD" v-show="nodeEnv != 'private'">
      <div class="std-div" style="margin-left: 6px">
        <div class="std-div" style="margin-left: 12px">
          <el-image src="images/police_06.svg"/>
        </div>
        <div class="std-div" style="height: 100%">
          <el-link class="police-link" href="https://beian.mps.gov.cn/#/query/webSearch?code=31011502401420"
                   :underline="false"
          >
            沪公网安备31011502401420
          </el-link>
        </div>
      </div>
      <div class="std-div" style="margin-left: 12px">
          <el-link class="police-link" href="https://beian.miit.gov.cn" :underline="false">
            沪ICP备2024044866号-1
          </el-link>
      </div>
    </div>
  </div>
  <el-dialog v-model="wx_program_dia" :show-close="false" :modal="false"
             top="calc(50vh - 100px)"
             :width="is_small_screen ? 360: 480" class="self-dialog" >
    <template #header>
      <div class="next-search-dia-head">
        <div>
          <el-text class="search-header-text">NextConsole小程序</el-text>
        </div>
        <div>
          <el-image src="images/hi_todo.svg" style="width: 48px;height: 48px;"></el-image>
        </div>

      </div>
    </template>
    <div>
      <el-text class="search-common-text">即将上线，敬请期待</el-text>
    </div>
    <template #footer>
      <div @click="wx_program_dia=false" class="search-confirm-button">
        <el-text class="search-header-text" style="color: #FFFFFF">确认</el-text>
      </div>
    </template>
  </el-dialog>
  <el-dialog v-model="person_version_dia" :show-close="false" :modal="false"
             :width="is_small_screen ? 360: 480" class="self-dialog" top="calc(50vh - 240px)">
    <template #header>
      <div class="next-search-dia-head">
        <div>
          <el-text class="search-header-text">NextConsole社区版</el-text>
          <br/>
          <el-text class="search-header-text">即将发布，敬请期待</el-text>
        </div>
        <div>
          <el-image src="images/hi_todo.svg" style="width: 48px;height: 48px;"></el-image>
        </div>

      </div>
    </template>
    <template #footer>
      <div @click="person_version_dia=false" class="search-confirm-button">

          <el-text class="search-header-text" style="color: #FFFFFF">确认</el-text>

      </div>
    </template>
  </el-dialog>
  <el-dialog v-model="community_dia" :show-close="false" :modal="false"
             :width="is_small_screen ? 360: 480" class="self-dialog" top="calc(50vh - 180px)">
    <template #header>
      <div class="next-search-dia-head">
        <div>
          <el-text class="search-header-text">欢迎加入NextConsole</el-text>
          <br/>
          <el-text class="search-header-text">微信社区</el-text>
        </div>
        <div>
          <el-image src="images/hi_todo.svg" style="width: 48px;height: 48px;"></el-image>
        </div>

      </div>
    </template>
    <div class="std-div2">
      <div class="std-div2">
        <div class="std-div">
          <div>
            <el-image src="images/wx_logo.svg"></el-image>
          </div>
          <div>
            <el-text style="font-size: 16px;font-weight: 600;line-height: 24px;color: #344054">
              微信扫码添加客服进群
            </el-text>
          </div>
        </div>
        <div class="std-div" style="margin-top: 16px">
          <el-image src="images/community_wx.svg" style="width: 128px; height: 128px"/>
        </div>
      </div>
    </div>
    <template #footer>
      <div @click="community_dia=false" class="search-confirm-button">
        <el-text class="search-header-text" style="color: #FFFFFF">确认</el-text>
      </div>
    </template>
  </el-dialog>
</template>

<style>
.search-link{

  font-size: 14px;
  font-weight: 500;
  line-height: 20px;
  text-align: left;
  color: #175CD3;
  cursor: pointer;

}
.police-link{

  font-size: 12px;
  font-weight: 400;
  line-height: 18px;
  text-align: left;
  color: #475467;
}
.std-div{
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  gap: 4px;
}
.footer-item{
  display: flex;
  flex-direction: row;
  gap: 16px;
  margin-bottom: 16px
}

.next-search-dia-head{
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  height: 48px;
  padding: 16px;
  background: linear-gradient(135deg, #E0C3FC 0%, #8EC5FC 100%);
  border-radius: 8px 8px 0 0;

}

.search-header-text{

  font-size: 16px;
  font-weight: 600;
  line-height: 24px;
  text-align: left;
  color: #101828;
  cursor: pointer;
}
.search-common-text{
  font-size: 14px;
  font-weight: 400;
  line-height: 20px;
  text-align: left;
  color: #101828;
}
.search-confirm-button{
  background-color: #1570ef;
  border: 1px solid #1570EF;
  padding: 6px 12px;
  gap: 8px;
  border-radius: 8px;
  width: 90%;
  box-shadow: 0 1px 2px 0 #1018280D;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;

}
.self-dialog{
  .el-dialog__header{
    padding: 0 !important;
    margin-right: 0 !important;
    border-radius: 8px;
  }
  .el-dialog__body{
    padding: 12px 16px !important;
  }
  .el-dialog__footer{
    border-radius: 8px;
  }
}
.std-div2{
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 20px;
}
.small-search-footer{
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
}
@media (max-width: 600px) {
  .footer-item{
    display: flex;
    flex-direction: row;
    gap: 16px;
    margin-bottom: 0;
  }
  .search-header-text{
    font-size: 14px;
    font-weight: 600;
    line-height: 20px;
    text-align: left;

  }
}
</style>
