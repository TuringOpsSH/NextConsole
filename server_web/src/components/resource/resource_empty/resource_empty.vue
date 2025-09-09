<script setup lang="ts">
import {
  prepare_upload_files,
  upload_file_content,
  upload_file_list
} from '@/components/resource/resource_upload/resource_upload';
import {
  current_resource_usage_percent,
  init_upload_manager,
  upload_file_Ref
} from '@/components/resource/resource_panel/panel';
import { current_resource } from '@/components/resource/resource_list/resource_list';
import router from '@/router';
import { current_share_resource } from '@/components/resource/share_resources/share_resources';
import { computed } from 'vue';

interface IProps {
  isSearchMode?: boolean;
}

const props = withDefaults(defineProps<IProps>(), {
  isSearchMode: false
});

const showNoSearchResult = computed(
  () =>
    (props.isSearchMode && ['resource_share', 'resource_list'].includes(router.currentRoute.value.name as string)) ||
    router.currentRoute.value.name == 'resource_search'
);
defineOptions({
  name: 'ResourceEmpty'
});
</script>

<template>
  <div v-if="showNoSearchResult" id="show-info-box" style="gap: 16px">
    <div>
      <el-image src="/images/empty_company_logo.svg" style="height: 160px; width: 220px" />
    </div>
    <div class="std-middle-box">
      <el-text style="font-size: 16px; font-weight: 600; color: #101828; line-height: 24px"> 搜索结果为空 </el-text>
    </div>
  </div>
  <div v-else-if="router.currentRoute.value.name == 'resource_share'" id="show-info-box" style="gap: 16px">
    <div>
      <el-image src="/images/empty_company_logo.svg" style="height: 160px; width: 220px" />
    </div>
    <div class="std-middle-box">
      <el-text
        style="font-size: 16px; font-weight: 600; color: #101828; line-height: 24px"
        v-if="!current_share_resource.resource_parent_id"
      >
        共享资源库为空
      </el-text>
      <el-text style="font-size: 16px; font-weight: 600; color: #101828; line-height: 24px" v-else>
        当前文件夹为空
      </el-text>
    </div>
    <div class="std-middle-box">
      <el-text style="font-size: 14px; color: #475467">
        探索共享资源库，发现更多优质资源！ 共享资源库是一个汇聚好友、同事以及公司管理员分享的高质量资源的宝库。 <br />
        在这里，您可以轻松获取他人分享的实用文档、学习资料、工具模板等，同时您分享的资源也会展示在这里。
      </el-text>
      <ul>
        <li>
          <el-text style="font-size: 14px; color: #475467">
            高质量资源汇聚：精选来自好友、同事及管理员分享的优质资源，涵盖运维中的多个领域。
          </el-text>
        </li>
        <li>
          <el-text style="font-size: 14px; color: #475467">
            便捷分享与获取：一键分享您的资源，同时快速获取他人分享的内容，实现资源的高效流通。
          </el-text>
        </li>
        <li>
          <el-text style="font-size: 14px; color: #475467">
            协作与学习：通过共享资源库，与团队成员共同学习、协作，提升工作效率与知识水平。
          </el-text>
        </li>
      </ul>
    </div>
  </div>

  <div v-else-if="router.currentRoute.value.name == 'resource_recycle_bin'" id="show-info-box" style="gap: 16px">
    <div>
      <el-image src="/images/empty_company_logo.svg" style="height: 160px; width: 220px" />
    </div>
    <div class="std-middle-box">
      <el-text style="font-size: 16px; font-weight: 600; color: #101828; line-height: 24px"> 回收站为空 </el-text>
    </div>
  </div>
  <div id="show-info-box" style="gap: 16px" v-else>
    <div>
      <el-image src="/images/empty_company_logo.svg" style="height: 160px; width: 220px" />
    </div>
    <div class="std-middle-box">
      <el-text
        style="font-size: 16px; font-weight: 600; color: #101828; line-height: 24px"
        v-if="!current_resource.resource_parent_id"
      >
        资源库为空
      </el-text>
      <el-text style="font-size: 16px; font-weight: 600; color: #101828; line-height: 24px" v-else>
        当前文件夹为空
      </el-text>
    </div>
    <div class="std-middle-box">
      <el-text style="font-size: 14px; color: #475467">
        资源库是您的专属在线网盘，为您提供便捷的资源存储与管理服务。 <br />
        在这里，您可以上传各类文件资源，包括文档、图片、音频、视频等，轻松实现资源的集中管理与共享。
      </el-text>
      <ul>
        <li>
          <el-text style="font-size: 14px; color: #475467">
            资源上传与管理：支持多种文件格式上传，随时随地存取您的资源。
          </el-text>
        </li>
        <li>
          <el-text style="font-size: 14px; color: #475467">
            智能向量索引
            <el-tooltip>
              <template #content>
                当前支持pdf、doc、docx、xls、xlsx、ppt、pptx、html、txt、md类型的文件构建知识库。
              </template>
              <el-image src="/images/tooltip.svg" style="height: 16px; width: 16px" />
            </el-tooltip>
            ：上传的资源会自动进行向量化处理，构建高效的索引体系，确保快速检索与精准匹配。
          </el-text>
        </li>
        <li>
          <el-text style="font-size: 14px; color: #475467">
            增强问答支持：资源库与工作台的增强问答功能无缝集成，您可以直接在问答中调用资源库中的内容，提升工作效率与准确性。
          </el-text>
        </li>
      </ul>
    </div>
    <el-upload
      multiple
      :show-file-list="false"
      :auto-upload="true"
      name="chunk_content"
      v-model:file-list="upload_file_list"
      :before-upload="prepare_upload_files"
      :on-change="init_upload_manager"
      :http-request="upload_file_content"
      :disabled="current_resource_usage_percent >= 100"
      accept="*"
      ref="upload_file_Ref"
      action=""
    >
      <el-button type="primary">
        <div class="std-middle-box">
          <el-text style="width: 90px; color: white">上传本地资源</el-text>
        </div>
      </el-button>
    </el-upload>
  </div>
</template>

<style scoped>
#show-info-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
  width: 100%;
  height: 100%;
}
</style>
