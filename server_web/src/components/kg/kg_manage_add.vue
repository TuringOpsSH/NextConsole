<script lang="ts"  setup>
import {onBeforeUnmount, onMounted} from 'vue';
import {ElInput, ElScrollbar} from "element-plus";

import './kg_center.scss'
import {
  change_kg_add_stage,
  commit_new_kg,
  CurrentKg,
  CurrentKgDocList,
  CurrentKgDocPageNum,
  CurrentKgDocPageSize,
  CurrentKgType,
  CurrentStage,
  download_loading,
  enter_kg_list,
  get_current_kg,
  get_current_kg_docs,
  get_upload_headers,
  handle_tag_close,
  handle_upload_kg_avatar,
  handle_upload_kg_avatar_exceed,
  handleKgTagInputConfirm,
  InputKgTagRef,
  inputKgTagValue,
  inputKgTagVisible,
  reset_new_kg,
  showKgTagInput,
  upload_loading,
  ValidKgMeta,
  ValidKgNameError,
  ValidKgNameErrorMsg,
} from "@/components/kg/kg_process";
import {turn_on_upload_dialog,} from "@/components/kg/doc_kg/doc_kg_process";
import {CurrentWebSiteViewModel, turn_on_upload_website_dialog,} from "@/components/kg/web_kg/web_kg_process";
import {turn_on_upload_script_dialog} from "@/components/kg/code_kg/code_kg_process";
import {
  handleKgDocCurrentChange,
  handleKgDocSizeChange,
  isAdmin,
  scrollbarHeight,
} from "@/components/kg/kg_center_base";
import {user_info} from "@/components/user_center/user";
import {get_user} from "@/api/user_center";
import {api} from "@/api/kg_center";
import {omit_text} from "@/utils/base";
import {Search} from "@element-plus/icons-vue";
import {
  change_current_preview_doc,
  current_kg_doc_list,
  CurrentKgDocKeyWord,
  CurrentKgDocTotal,
  CurrentPreviewDoc,
  doc_preview_loading,
  download_kg_doc,
  kg_doc_on_remove,
  search_kg_docs
} from "@/components/kg/doc_process";
import Kg_script_preview from "@/components/kg/code_kg/kg_script_preview.vue";
import Kg_code_upload from "@/components/kg/code_kg/kg_upload.vue";
import Kg_doc_upload from "@/components/kg/doc_kg/kg_upload.vue";
import Kg_web_upload from "@/components/kg/web_kg/kg_upload.vue";
import Kg_faq_upload from "@/components/kg/faq_kg/kg_upload.vue";
import {turn_on_upload_faq_dialog} from "@/components/kg/faq_kg/faq_kg_process";
import Kg_faq_preview from "@/components/kg/faq_kg/kg_faq_preview.vue";

const props = defineProps({

  kg_type: {
    type: String,
    required: false,
    default: "file"
  },
  stage : {
    type: String,
    default: "meta",
    required: false
  },
  kg_code:{
    type: String,
    required: false,
    default: ""
  }

});
async function handleResize(){
  scrollbarHeight.value = window.innerHeight - 220
}


onMounted(async () => {
    window.addEventListener('resize', handleResize);
    await handleResize()
    if(!user_info.value){
      user_info.value = (await get_user({})).result
    }

    // add
    CurrentKgType.value = props.kg_type;
    CurrentStage.value = props.stage;
    if (props.kg_code ) {
      await get_current_kg(props.kg_code)
      await get_current_kg_docs(props.kg_code)
    }

  }
)
onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize);
  }
)

</script>

<template>
  <el-container>
    <el-header style="padding: 0 !important;" height="62px">
      <el-scrollbar>
        <div class="kg-op-header">
          <div class="kg-op-header-left">

              <div class="kg-op-step">
                <div>
                  <el-button class="kg-op-step-button" @click="enter_kg_list()">
                    <el-image src="images/arrow_left_black.svg" style="width: 14px;height: 14px"/>
                  </el-button>

                </div>
                <div>
                  <el-button disabled class="kg-op-step-button">
                    <el-image src="images/arrow_right_grey.svg" style="width: 14px;height: 14px"/>
                  </el-button>
                </div>
              </div>
              <div class="kg-stage-box">
                <el-text style=" font-size: 16px;font-weight: 600;line-height: 24px;text-align: left;color: #101828;">
                  新建知识库
                </el-text>
              </div>

          </div>
          <div class="kg-op-header-middle">

            <div class="kg-op-create-stage" >
              <div class="kg-op-create-stage-item"
                   :class="CurrentStage=='meta' ? 'kg-op-create-stage-item-active': ''">

                <el-text class="kg-op-create-stage-item-text"
                         :class="CurrentStage=='meta' ? 'kg-op-create-stage-item-text-active': ''"
                >1 元信息设置</el-text>

              </div>
              <div class="kg-op-create-stage-item"
                   :class="CurrentStage=='upload' ? 'kg-op-create-stage-item-active': ''">
                <el-text class="kg-op-create-stage-item-text"
                         :class="CurrentStage=='upload' ? 'kg-op-create-stage-item-text-active': ''"
                         v-if="CurrentKgType==='file'"
                >2 文件上传</el-text>
                <el-text class="kg-op-create-stage-item-text"
                         :class="CurrentStage=='upload' ? 'kg-op-create-stage-item-text-active': ''"
                         v-else-if="CurrentKgType==='website'"
                >2 站点同步</el-text>
                <el-text class="kg-op-create-stage-item-text"
                         :class="CurrentStage=='upload' ? 'kg-op-create-stage-item-text-active': ''"
                         v-else-if="CurrentKgType==='script'"
                >2 脚本上传</el-text>
                <el-text class="kg-op-create-stage-item-text"
                         :class="CurrentStage=='upload' ? 'kg-op-create-stage-item-text-active': ''"
                         v-else-if="CurrentKgType==='faq'"
                >2 FAQ上传</el-text>
              </div>
              <div class="kg-op-create-stage-item"
                   :class="CurrentStage=='rag' ? 'kg-op-create-stage-item-active': ''">
                <el-text class="kg-op-create-stage-item-text"
                         :class="CurrentStage=='rag' ? 'kg-op-create-stage-item-text-active': ''"
                >
                  3 检索设置</el-text>
              </div>
            </div>
          </div>
          <div class="kg-op-header-right">

            <div class="kg-op-header-add-box"  >
              <div>
                <el-button class="kg-op-header-add-stage-button" @click="change_kg_add_stage(-1)"
                           :disabled="CurrentStage==='meta'">
                  <div>
                    <el-image src="images/arrow_left_black.svg"
                              class="next-console-image"
                    />
                  </div>
                  <div style="margin-left: 8px">
                    <el-text class="next-console-text-bold">上一步</el-text>
                  </div>

                </el-button>
              </div>
              <div>
                <el-button class="kg-op-header-add-stage-button" @click="change_kg_add_stage(1)"
                           :disabled="CurrentStage==='rag'"

                           style="background-color: #1570ef">
                  <div>
                    <el-image src="images/arrow_right_white.svg"
                              style="width: 14px;height: 14px"
                    />
                  </div>
                  <div style="margin-left: 8px">
                    <el-text class="next-console-text-bold" style="color: #FFFFFF">下一步</el-text>
                  </div>
                </el-button>
              </div>
            </div>
          </div>
        </div>
      </el-scrollbar>
    </el-header>
    <el-main style="height: calc(100vh - 130px)">
      <el-scrollbar wrap-style="width: 100%" view-style="width: 100%"
                    v-loading="download_loading"
                    element-loading-text="下载中，请稍等..."
      >
        <div class="kg-main-box" >
          <div class="kg-main-box-add-meta" v-if="CurrentStage==='meta'">
            <div class="kg-add-meta-info-box">
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
                              :class="ValidKgNameError ? 'kg-add-meta-item-value-error' : 'kg-add-meta-item-value'"
                    />
                    <el-text v-if="ValidKgNameError" style="color: red">
                      {{ValidKgNameErrorMsg}}
                    </el-text>
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
                        closable
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
                        style="width: 100px;height: 20px;margin-top: 8px"
                        size="small"
                        @keyup.enter="handleKgTagInputConfirm"
                        @blur="handleKgTagInputConfirm"
                    />
                    <el-button v-else class="button-new-tag" size="small" @click="showKgTagInput"
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

                        :on-success="handle_upload_kg_avatar"
                        :on-exceed="handle_upload_kg_avatar_exceed"
                        accept=".jpg, .jpeg, .svg, .png"
                    >

                      <template #trigger>
                        <el-button text style="padding: 12px">
                          <el-text style="font-size: 14px;font-weight: 600;line-height: 20px;color:#175CD3">
                            上传
                          </el-text>
                        </el-button>
                      </template>
                    </el-upload>

                  </div>
                </div>
              </div>

            </div>
            <div class="kg-add-meta-info-box">
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
                  <el-radio :label="0">私有</el-radio>
                </el-radio-group>
              </div>

            </div>
          </div>
          <div class="kg-main-box-add-upload" v-else-if="CurrentStage==='upload'"
               v-loading="upload_loading"
               element-loading-text="文件准备中。。。"
          >
            <div class="kg-main-box-add-upload-init" v-if="CurrentKgDocList.length==0">

              <el-button v-if="CurrentKgType==='file'"
                         class="kg-add-stage-upload-button" @click="turn_on_upload_dialog">
                <div>
                  <el-image style="width: 16px;height: 16px" src="images/kg_doc_upload_white.svg"/>
                </div>
                <el-text class="next-console-text-bold" style="color: #FFFFFF;margin-left: 12px;">上传文档</el-text>

              </el-button>
              <el-button v-else-if="CurrentKgType==='website'"
                         class="kg-add-stage-upload-button" @click="turn_on_upload_website_dialog">
                <div>
                  <el-image style="width: 16px;height: 16px" src="images/web_money_blue.svg"/>
                </div>
                <el-text class="next-console-text-bold" style="color: #FFFFFF;margin-left: 12px;">选择站点</el-text>

              </el-button>
              <el-button v-else-if="CurrentKgType==='script'"
                         class="kg-add-stage-upload-button" @click="turn_on_upload_script_dialog()">
                <div>
                  <el-image style="width: 16px;height: 16px" src="images/scripts_white.svg"/>
                </div>
                <el-text class="next-console-text-bold" style="color: #FFFFFF;margin-left: 12px;">上传代码</el-text>
              </el-button>
              <el-button v-else-if="CurrentKgType==='faq'"
                         class="kg-add-stage-upload-button" @click="turn_on_upload_faq_dialog()">
                <div>
                  <el-image style="width: 16px;height: 16px" src="images/faq_white.svg"/>
                </div>
                <el-text class="next-console-text-bold" style="color: #FFFFFF;margin-left: 12px;">上传FAQ</el-text>
              </el-button>
              <div v-else>
                <el-empty description="此功能暂未开放"></el-empty>
              </div>

            </div>
            <div class="kg-main-box-add-upload-list" v-else>
              <div class="kg-add-upload-left">
                <div class="kg-add-upload-head">
                  <div class="kg-add-upload-head-title">
                    <el-text class="next-console-text-bold">文件素材</el-text>
                  </div>
                  <div class="kg-add-upload-sub-head">
                    <div style="width: 100%">
                      <el-input :prefix-icon="Search" v-model="CurrentKgDocKeyWord"
                                placeholder="搜索文档名称"
                                clearable
                                @change="search_kg_docs"
                                style="width: 100%"
                      />
                    </div>
                    <div>
                      <el-button text @click="turn_on_upload_dialog" v-if="CurrentKg.kg_type==='file'">
                        <el-text class="next-console-text-bold" style="color: #1570ef">上传文档</el-text>
                      </el-button>
                      <el-button text @click="turn_on_upload_website_dialog"
                                 v-else-if="CurrentKg.kg_type==='website'">
                        <el-text class="next-console-text-bold" style="color: #1570ef">选择站点</el-text>
                      </el-button>
                      <el-button text @click="turn_on_upload_script_dialog"
                                 v-else-if="CurrentKg.kg_type==='script'">
                        <el-text class="next-console-text-bold" style="color: #1570ef">上传脚本</el-text>
                      </el-button>
                      <el-button text @click="turn_on_upload_faq_dialog"
                                 v-else-if="CurrentKg.kg_type==='faq'">
                        <el-text class="next-console-text-bold" style="color: #1570ef">上传FAQ</el-text>
                      </el-button>
                    </div>
                  </div>

                </div>
                <el-scrollbar wrap-style="width:100%" view-style="width:100%" :height="scrollbarHeight -36">
                  <div class="kg-add-upload-body">
                    <div class="kg-doc-item-box" v-for="(kg_doc,_) in current_kg_doc_list"
                         @click="change_current_preview_doc(kg_doc)"
                         :class="kg_doc.is_chosen ? 'kg-doc-item-box-chosen':'kg-doc-item-box'">
                      <div class="attachment-file-item-left">
                        <div class="attachment-file-icon-box">
                          <el-image src="images/file_format_html_blue.svg" class="attachment-file-icon"
                                    v-if="kg_doc.doc_format==='html'"  />
                          <el-image src="images/file_format_docx_blue.svg" class="attachment-file-icon"
                                    v-else-if="kg_doc.doc_format==='docx' || kg_doc.doc_format==='doc'"/>
                          <el-image src="images/file_format_md.svg" class="attachment-file-icon"
                                    v-else-if="kg_doc.doc_format==='md'"/>
                          <el-image src="images/file_format_txt.svg" class="attachment-file-icon"
                                    v-else-if="kg_doc.doc_format==='txt'"/>
                          <el-image src="images/file_format_pdf.svg" class="attachment-file-icon"
                                    v-else-if="kg_doc.doc_format==='pdf'"/>
                          <el-image src="images/file_format_code.svg" class="attachment-file-icon"
                                    v-else-if="kg_doc.doc_format==='code'"/>
                          <el-image src="images/file_format_faq.svg" class="attachment-file-icon"
                                    v-else-if="kg_doc.doc_format==='faq'"/>
                          <el-image src="images/file_format_other.svg" class="attachment-file-icon"
                                    v-else/>

                        </div>
                        <div class="attachment-file-meta-box" >

                          <div style="max-width: 200px">
                            <el-tooltip  v-if="kg_doc.doc_name && kg_doc.doc_name.length > 30" effect="light">
                              <el-text >{{omit_text(kg_doc.doc_name,30)}}</el-text>
                              <template #content>
                                <div v-text="kg_doc.doc_name" style="max-width: 400px;display: flex;flex-wrap: wrap"/>
                              </template>
                            </el-tooltip>
                            <el-text v-else>{{kg_doc.doc_name}}</el-text>
                          </div>
                          <div><el-text>{{kg_doc.doc_size}} MB</el-text></div>

                        </div>
                      </div>
                      <div class="attachment-file-button-box">

                        <el-image src="images/file_download_02.svg"
                                  style="width: 16px;height: 16px"
                                  @click.stop="download_kg_doc(kg_doc)"/>

                      </div>
                      <div v-if="kg_doc.is_chosen" class="attachment-file-button-box">
                        <el-popconfirm title="确定要删除该文件么?" confirm-button-text="确定"
                                       cancel-button-text="取消" @confirm="kg_doc_on_remove(kg_doc)">
                          <template #reference>

                            <el-image src="images/file_minus_blue.svg"
                                      class="next-console-image"/>

                          </template>
                        </el-popconfirm>

                      </div>
                    </div>
                    <div id="empty-doc-list"  v-if="!current_kg_doc_list || !current_kg_doc_list.length " >
                      <el-empty description="暂无搜索结果"/>
                    </div>

                  </div>

                </el-scrollbar>
                <div class="kg-add-upload-foot">
                  <el-pagination
                      layout=" total, prev, pager, next"
                      :small="true"
                      :pager-count="5"
                      :total="CurrentKgDocTotal"
                      :page-size="CurrentKgDocPageSize"
                      :current-page="CurrentKgDocPageNum"
                      @update:page-size="handleKgDocSizeChange"
                      @update:current-page="handleKgDocCurrentChange"
                  />
                </div>
              </div>
              <el-scrollbar>
                <div class="kg-add-upload-right" v-loading="doc_preview_loading">
                  <div v-if="CurrentPreviewDoc && CurrentPreviewDoc.doc_format ==='html' "
                       class="current-doc-preview-box"
                  >
                    <div   class="current-website-preview-box" >
                      <el-switch
                          v-model="CurrentWebSiteViewModel"
                          class="ml-2"
                          inline-prompt
                          style="--el-switch-on-color: #13ce66; --el-switch-off-color: #ff4949"
                          active-text="预览模式"
                          inactive-text="源码模式"
                      />
                      <iframe :src="CurrentPreviewDoc.doc_url"
                              v-if="CurrentWebSiteViewModel && CurrentPreviewDoc.doc_url"
                              style="width: 100%;height: 100%"/>
                      <el-empty v-else-if="CurrentWebSiteViewModel && !CurrentPreviewDoc.doc_url"
                                description="此网页素材缺失链接数据，无法预览！"/>
                      <div v-else-if="!CurrentWebSiteViewModel" class="current-doc-preview-box"
                           style="flex-direction: column">
                        <div v-if="CurrentPreviewDoc.doc_content" v-text="CurrentPreviewDoc.doc_content"/>
                        <div v-else v-loading="true" style="display: flex;align-items: center;
                            justify-content: center;width: 80%;height: 80%" element-loading-text="源码处理中，请稍候">

                        </div>

                      </div>
                    </div>

                  </div>
                  <div v-else-if="CurrentPreviewDoc && CurrentPreviewDoc.doc_format ==='txt'"
                       class="current-doc-preview-box" v-text="CurrentPreviewDoc.doc_content"
                  >

                  </div>
                  <div v-else-if="CurrentPreviewDoc && CurrentPreviewDoc.doc_format ==='pdf'"
                       class="current-doc-preview-box"
                  >
                    <iframe :src="CurrentPreviewDoc.doc_url"
                            style="width: 100%;height: 100%;border: none"
                    />
                  </div>
                  <div v-else-if="CurrentPreviewDoc && CurrentPreviewDoc.doc_format ==='md'"
                       class="current-doc-preview-box"
                       v-text=" CurrentPreviewDoc.doc_content"
                  >

                  </div>
                  <div v-else-if="CurrentPreviewDoc && CurrentPreviewDoc.doc_format ==='docx'"
                       v-html="CurrentPreviewDoc.doc_content"
                       class="current-doc-preview-box"/>
                  <div v-else-if="CurrentPreviewDoc && CurrentPreviewDoc.doc_format ==='doc'"
                       v-html="CurrentPreviewDoc.doc_content"
                       class="current-doc-preview-box"
                  />
                  <div v-else-if="CurrentPreviewDoc && CurrentPreviewDoc.doc_format ==='code'">
                    <kg_script_preview :code="CurrentPreviewDoc.doc_content" language="python"/>
                  </div>
                  <div v-else-if="CurrentPreviewDoc && CurrentPreviewDoc.doc_format ==='faq'">
                    <kg_faq_preview :answer="CurrentPreviewDoc.doc_content"
                                    :question_pre="CurrentPreviewDoc.doc_desc"
                                    :question="CurrentPreviewDoc.doc_name" />
                  </div>
                  <div v-else class="current-doc-preview-box"
                       style="justify-content: center; align-items: center">
                    <el-empty description="请从左侧列表中选择文件进行预览！"></el-empty>
                  </div>
                </div>
              </el-scrollbar>
            </div>
          </div>
          <div class="kg-main-box-add-rag" v-else-if="CurrentStage==='rag'">
            <div class="kg-main-box-add-rag-area">
              <div>
                <el-text>检索设置</el-text>
              </div>
              <div>
                <div>
                  <div>
                    <el-text>混合检索系数（0代表完全偏向字符关键词检索，1代表完全偏向语义相似度检索）</el-text>
                    <el-slider v-model="CurrentKg.rag_factor"
                               :max="1" :step="0.01"
                    />
                  </div>
                </div>
                <div>
                  <div>
                    <el-text>最小语义相关度系数（低于这个阈值代表检索到的文本与问题无关）</el-text>
                    <el-slider v-model="CurrentKg.rag_relevant_threshold"
                               :max="1" :step="0.01"
                    />
                  </div>
                </div>
              </div>
            </div>
            <div class="kg-main-box-add-commit-area">
              <div>
                <el-text class="next-console-text-bold">
                  共{{ CurrentKgDocTotal }}篇文档，预计索引耗时{{CurrentKgDocList.length*1.5}}s，请确认提交索引构建任务
                </el-text>
              </div>
              <div>
                <el-text>
                  提交后可以离开该页面，任务完成时我们会在通知中心通知你
                </el-text>
              </div>
              <div style="display: flex;flex-direction: row;gap:16px">
                <el-popconfirm title="此操作将会清除之前的进度，确定么？" @confirm="reset_new_kg"
                               confirm-button-text="确定" cancel-button-text="取消"
                >
                  <template #reference>
                    <el-button  class="kg-op-header-add-stage-button" >
                      <el-text class="next-console-text-bold">取消退出</el-text>
                    </el-button>
                  </template>
                </el-popconfirm>

                <el-button class="kg-op-header-add-stage-button" @click="commit_new_kg"
                           style="background-color: #1570ef"
                >
                  <el-text class="next-console-text-bold" style="color: #FFFFFF">确认提交</el-text>
                </el-button>
              </div>
            </div>
          </div>
          <div class="kg-main-box-add-else" v-else>
            <el-empty description="暂无权限！"></el-empty>
          </div>
          <Kg_doc_upload/>
          <Kg_web_upload/>
          <Kg_code_upload/>
          <Kg_faq_upload/>
        </div>
      </el-scrollbar>
    </el-main>
  </el-container>
</template>
<style scoped>
.el-menu--horizontal.el-menu{
  border-bottom: 0;
}

.el-button {
  margin-left: 0;
}
.kg-add-meta-item-value-textarea :deep(.el-textarea__inner::-webkit-scrollbar){
  width: 6px ;
  height: 6px ;
}
.kg-add-meta-item-value-textarea :deep(.el-textarea__inner::-webkit-scrollbar-thumb) {
  border-radius: 3px ;
  -moz-border-radius: 3px ;
  -webkit-border-radius: 3px ;
  background-color: #c3c3c3 ;
}
.kg-add-meta-item-value-textarea :deep(.el-textarea__inner::-webkit-scrollbar-track) {
  background-color: transparent ;
}
.kg-op-header{
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  padding: 6px 12px;
  border-bottom: 1px solid #D0D5DD;
  width: calc(100% - 24px);
}
.kg-op-header-left{
  min-width: 200px;
  display: flex;
  flex-direction: row;
  gap: 6px;
  align-items: center;
  justify-content: center;

}
.kg-op-header-middle{
  min-width: 600px;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  gap: 6px;
}
.kg-main-box{
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
}
.kg-add-upload-left{
  display: flex;
  flex-direction: column;
  border-right: 1px solid #EAECF0;
  min-width: 240px;
  max-width: 480px;
  height: 100%;
}
#empty-doc-list{
  display: flex;align-items: center;
  justify-content: center;width:100%;height: 50vh
}
.kg-doc-item-box{
  display: flex;
  flex-direction: row;
  border: 1px solid #D0D5DD;
  background-color: #FFFFFF;
  align-items: center;
  justify-content: space-between;
  border-radius: 12px;
  height: 72px;
  padding: 0 12px;
  width: calc(100% - 24px);
  cursor: pointer;
  gap: 6px;
}
.kg-doc-item-box-chosen{
  background-color: #EFF8FF;
  border: 2px #175CD3 solid;

}
.current-doc-preview-box{
  width: calc(100vw - 360px);
  height: calc(100vh - 200px);
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  justify-content: flex-start;
  padding: 6px;
  flex-wrap: wrap;
  white-space: pre-wrap;

}
.kg-add-upload-right{
  width: calc(100% - 24px);
  height: calc(100% - 24px);
  padding: 12px;
  display: flex;
  align-items: flex-start;
  justify-content: flex-start;
}
.kg-add-upload-foot{
  display: flex;
  align-items: center;
  justify-content: center;
  height: 40px;
  width: 100%;

}
</style>
