<script setup lang="ts">

import {CurrentKg,} from "@/components/kg/kg_process";
import {ElInput} from "element-plus";
import {
  CurrentWebSiteError,
  CurrentWebSiteErrorMsg,
  dialog_v_upload_kg_website,
  turn_off_upload_website_dialog,
  validate_web_url,
} from "@/components/kg/web_kg/web_kg_process"
</script>

<template>
  <el-dialog v-model="dialog_v_upload_kg_website" title="在线web站点同步"
             width="480"
             :close-on-click-modal="false">
    <div style="display: flex;flex-direction: column; justify-content:flex-start">
      <div class="kg-add-website-item">
        <div class="kg-add-website-item-col">
          <el-text>站点URL</el-text>
          <el-text style="color: red">*</el-text>

        </div>
        <div class="kg-add-website-item-value">
          <el-input v-model="CurrentKg.kg_url" placeholder="填写url"
                    @change="validate_web_url(CurrentKg.kg_url)"
                    :class="CurrentWebSiteError ? 'kg-add-meta-item-value-error' : ''"
          >
            <template #suffix>
              <el-popover>
                <el-text>请填写站点的URL地址，例如：https://www.baidu.com，后台会自动爬取整个站点</el-text>
                <template #reference>
                  <el-image src="images/help_circle_grey.svg" style="width: 14px; height: 14px;cursor: help"/>
                </template>
              </el-popover>

            </template>

          </el-input>
          <el-text v-if="CurrentWebSiteError" style="color: red">{{CurrentWebSiteErrorMsg}} </el-text>

        </div>
      </div>
      <div class="kg-add-website-item">
        <div>
          <el-text>文档版本选择器</el-text>
        </div>
        <div class="kg-add-website-item-value">
          <el-input disabled placeholder=""/>
        </div>
      </div>
      <div class="kg-add-website-item">
        <div>
          <el-text>导航栏选择器</el-text>
        </div>
        <div class="kg-add-website-item-value">
          <el-input disabled placeholder=""/>
        </div>
      </div>
      <div class="kg-add-website-item">
        <div>
          <el-text>正文选择器</el-text>
        </div>
        <div class="kg-add-website-item-value">
          <el-input disabled placeholder=""/>
        </div>
      </div>
      <div class="kg-add-website-item">
        <div class="kg-add-website-item-col">
          <el-text>同步频率</el-text>
        </div>
        <div class="kg-add-website-item-value">
          <el-select placeholder="从不" v-model="CurrentKg.kg_sync_frequency" style="width: 100%" disabled>
            <el-option label="从不" :value="0"></el-option>
            <el-option label="每日" :value="24"></el-option>
            <el-option label="每周" :value="7*24"></el-option>
            <el-option label="每月" :value="31*24"></el-option>
          </el-select>
        </div>
      </div>

    </div>
    <template #footer>
      <div class="kg-dialog-footer">
        <el-button class="kg-dialog-footer-button" style="background-color: #1570ef;
        border: 1px solid #D0D5DD"
                   @click="turn_off_upload_website_dialog">
          <el-text class="kg-button-text" style="color: #FFFFFF">
            完成
          </el-text>
        </el-button>


      </div>
    </template>
  </el-dialog>
</template>

<style scoped>

</style>
