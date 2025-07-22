<script setup lang="ts">

import {
  CurrentKg,
  get_upload_headers,
  handle_tag_close,
  handle_upload_kg_avatar,
  handle_upload_kg_avatar_exceed,
  handleKgTagInputConfirm,
  inputKgTagValue,
  inputKgTagVisible,
  showKgTagInput,
  ValidKgMeta,
  ValidKgNameError,
  ValidKgNameErrorMsg
} from "@/components/kg/kg_process";
import {api} from "@/api/kg_center";
import {onMounted} from "vue";
import {check_kg_permission, isAdmin} from "@/components/kg/kg_center_base";


onMounted(async () => {

})
</script>

<template>
  <div class="kg-main-box-detail-body"
       style="height: calc(100vh - 240px); width: calc(100vw - 100px)">

    <div class="kg-main-box-detail-meta" >

      <div class="kg-list-meta-info-box">
        <div>
          <el-text>
            基本信息
          </el-text>
        </div>
        <div class="kg-add-meta-item-box">
          <div class="kg-add-meta-item" >
            <div class="kg-add-meta-item-name">
              <el-text>知识库名称</el-text>
            </div>
            <div class="kg-add-meta-item-value" >
              <el-input v-model="CurrentKg.kg_name" placeholder="填写名称"
                        @change="ValidKgMeta"
                        :disabled="!check_kg_permission(CurrentKg)"
                        :class="ValidKgNameError ? 'kg-add-meta-item-value-error' : 'kg-add-meta-item-value'"
              />
              <el-text v-if="ValidKgNameError" style="color: red">
                {{ValidKgNameErrorMsg}}
              </el-text>
            </div>


          </div>
          <div class="kg-add-meta-item" >
            <div class="kg-add-meta-item-name">
              <el-text>知识库编号</el-text>
            </div>
            <div class="kg-add-meta-item-value" >
              <el-input v-model="CurrentKg.kg_code"
                        readonly
              />

            </div>


          </div>
          <div class="kg-add-meta-item">
            <div class="kg-add-meta-item-name">
              <el-text>知识库描述</el-text>
            </div>
            <div class="kg-add-meta-item-value">
              <el-input v-model="CurrentKg.kg_desc" placeholder="填写描述"
                        clearable
                        class="kg-add-meta-item-value-textarea"
                        type="textarea"
                        rows="4"
                        resize="none"
                        :maxlength="8092"
                        :show-word-limit="true"
                        :disabled="!check_kg_permission(CurrentKg)"
              />
            </div>
            <el-link href="" target="_blank">了解如何更好编写描述</el-link>
          </div>
          <div class="kg-add-meta-item">
            <div class="kg-add-meta-item-name">
              <el-text>知识库检索标签</el-text>
            </div>
            <div class="kg-add-tags-value">
              <el-tag

                  v-for="tag in CurrentKg.kg_tags"
                  :key="tag"
                  :closable="check_kg_permission(CurrentKg)"
                  :disable-transitions="false"
                  @close="handle_tag_close(tag)"
                  style="margin: 8px"
              >
                {{ tag.tag_content ? tag.tag_content : tag}}
              </el-tag>
              <el-input
                  v-if="inputKgTagVisible"
                  ref="InputKgTagRef"
                  v-model="inputKgTagValue"
                  style="width: 100px;height: 20px; margin-top: 8px"
                  size="small"
                  @keyup.enter="handleKgTagInputConfirm"
                  @blur="handleKgTagInputConfirm"
                  :disabled="!check_kg_permission(CurrentKg)"
              />
              <el-button v-else class="button-new-tag" size="small" @click="showKgTagInput"
                         v-if="check_kg_permission(CurrentKg)"
                         style="margin-top: 8px">
                + 新标签
              </el-button>
            </div>
            <el-link href="" target="_blank">了解如何更好编写标签</el-link>
          </div>
          <div class="kg-add-meta-item-icon">
            <div class="kg-add-meta-item-icon-name">
              <el-text>知识库图标</el-text>
              <el-avatar :src="CurrentKg.kg_icon ? CurrentKg.kg_icon : 'images/kg_default_icon.svg'"
                         style="background: #FFFFFF"></el-avatar>
            </div>
            <div class="kg-add-meta-item-icon-value">

              <el-upload
                  ref="upload_kg_avatar"
                  :action="api.kg_icon_upload"
                  :auto-upload="true"
                  :show-file-list="false"
                  :limit="1"
                  name="kg_db_icon"
                  :headers="get_upload_headers()"
                  v-if="check_kg_permission(CurrentKg)"
                  :on-success="handle_upload_kg_avatar"
                  :on-exceed="handle_upload_kg_avatar_exceed"
                  accept=".jpg, .jpeg, .svg, .png"
              >

                <template #trigger>
                  <el-button text style="padding: 12px">
                    <el-text style="font-size: 14px;font-weight: 600;line-height: 20px;color:#475467">
                      上传
                    </el-text>
                  </el-button>
                </template>
              </el-upload>

            </div>
          </div>
        </div>

      </div>
      <div class="kg-list-meta-info-box">
        <div>
          <el-text>可见权限</el-text>
        </div>
        <div class="kg-add-meta-item-box" >
          <el-radio-group v-model="CurrentKg.kg_public">
            <el-radio :label="1" :disabled="!isAdmin">
              <el-popover>
                <template #reference>

                  <el-text>公开</el-text>
                </template>
                <el-text>公开后，所有用户均可查看知识库内容</el-text>
              </el-popover>
            </el-radio>
            <el-radio :label="0" v-if="check_kg_permission(CurrentKg)">私有</el-radio>
          </el-radio-group>
        </div>

      </div>


    </div>
    <div class="kg-main-box-detail-rag-area">
      <el-row>
        <el-col :span="8">
          <div >
            <el-text>检索设置</el-text>
          </div>
        </el-col>
        <el-col :span="16">
          <div>
            <div>
              <div>
                <el-text>混合检索系数（0代表完全偏向字符关键词检索，1代表完全偏向语义相似度检索）</el-text>
                <el-slider v-model="CurrentKg.rag_factor"
                           :max="1" :step="0.01" :disabled="!check_kg_permission(CurrentKg)"
                />
              </div>
            </div>
            <div>
              <div>
                <el-text>最小语义相关度系数（低于这个阈值代表检索到的文本与问题无关）</el-text>
                <el-slider v-model="CurrentKg.rag_relevant_threshold"
                           :max="1" :step="0.01"
                           :disabled="!check_kg_permission(CurrentKg)"
                />
              </div>
            </div>
          </div>
        </el-col>
      </el-row>


    </div>
  </div>
</template>

<style scoped>

</style>
