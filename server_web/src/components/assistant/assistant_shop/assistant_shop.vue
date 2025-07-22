<script lang="ts"  setup>
import {nextTick, onMounted, ref} from 'vue';
import {ElInput, ElMessage, ElScrollbar} from "element-plus";
import {useRoute, useRouter} from 'vue-router';
import {shop_assistant} from "@/types/assistant";
import {Users} from "@/types/users";
import {
  off_list_shop_assistants,
  shop_assistant_comment,
  shop_assistant_get,
  shop_assistant_search,
  shop_assistant_subscribe,
  shop_assistant_unsubscribe
} from "@/api/assistant_center";
import {getInfo} from "@/utils/auth";
import {Search} from "@element-plus/icons-vue";

const router = useRouter()
const route = useRoute();
const shop_assistant_choose = ref<shop_assistant>();
const shopAssistantList = ref<Array<shop_assistant>>([])
const shopAssistantsCnt = ref(0);
const shop_assistant_order = ref('create_time');
const userinfo = ref<Users>({
  user_account_type: "",
  user_wx_avatar: "",
  user_wx_nickname: "",
  user_wx_union_id: "",
  user_age: 0,
  user_code: "",
  create_time: "",
  user_department: "",
  user_email: "",
  user_gender: "",
  user_id: "",
  last_login_time: "",
  user_name: "",
  user_phone: "",
  user_avatar: "",
  user_company: "",
  user_role: [""],
  user_source: "",
  user_status: "",
  update_time: "",
  user_wx_openid: ""
});
const current_page_num = ref(1);
const current_page_size = ref(20);
const show_cnt_tag = ref(false);
const shop_assistant_view_model = ref(0)
const shop_assistant_search_key_word= ref('')
const shop_assistant_unsubscribe_vis = ref(false)
const user_comment_input = ref('')
const user_comment_level = ref(null)
const colors = ref(['#99A9BF', '#F7BA2A', '#FF9900'])
const shop_assistant_col_map = ref(
    {
      "assistant_author_name" : "创建者",
      "create_time" : "发布时间",
      "docs_cnt" : "文档数量",
      "tools_cnt" : "工具数量",
      "commands_cnt" : "指令数量",
    }
)
async function change_assistant_view_model(view_model: number, shop_assistant_id: number | null = null) {
  // model 0 列表查看模式
  // model 1 详情查看模式
  // model 2 新增助手模式

  if (view_model === 0) {
    await router.push({
      query: {
        view_model: 0
      }
    });
    await get_shop_assistant_list()

  }
  if (view_model === 1) {
    let res = await shop_assistant_get({
      "shop_assistant_id": shop_assistant_id,
    })
    if (!res.error_status) {
      shop_assistant_choose.value = res.result
    }
    await router.push({
      query: {
        ...router.currentRoute.value.query, // 保持既有参数
        view_model: 1,
        choose_shop_assistant_id: shop_assistant_id
      }
    });




  }

  shop_assistant_view_model.value = view_model;
  await nextTick()
}

async function get_shop_assistant_list() {
  let params = {
    "page_num": current_page_num.value,
    "page_size": current_page_size.value,
    'order': shop_assistant_order.value,

  }
  if (shop_assistant_search_key_word.value) {
    params['assistant_name'] = shop_assistant_search_key_word.value
    params['assistant_desc'] = shop_assistant_search_key_word.value
    params['assistant_tags'] = shop_assistant_search_key_word.value
  }
  let res = await shop_assistant_search(params)
  if (!res.error_status) {
    shopAssistantList.value = res.result.data
    shopAssistantsCnt.value = res.result.cnt
  }
}

async function subscribe_shop_assistant(shop_assistant: shop_assistant) {
  let params = {
    "shop_assistant_id": shop_assistant.id,
  }
  let res = await shop_assistant_subscribe(params)
  if (!res.error_status) {

    ElMessage.success({
      message: "订阅成功！",
      type: 'success',
      duration: 600
    })
    shop_assistant.authority_create_time = res.result.create_time
  }

}

async function unsubscribe_shop_assistant(shop_assistant: shop_assistant) {
  let params = {
    "shop_assistant_id": shop_assistant.id,
  }
  let res = await shop_assistant_unsubscribe(params)
  if (!res.error_status) {

    ElMessage.success({
      message: "取消订阅成功！",
      type: 'success',
      duration: 600
    })
    shop_assistant.authority_create_time = null

  }
  shop_assistant_unsubscribe_vis.value = false

}

async function off_listing_shop_assistant(shop_assistant: shop_assistant) {
  let params = {
    "shop_assistant_id" : shop_assistant.id
  }
  let res = await off_list_shop_assistants(params)
  if (!res.error_status) {

    ElMessage.success({
      message: "下架成功！",
      type: 'success',
      duration: 600
    })
    await get_shop_assistant_list()
  }
  await router.push({
    query: {
      view_model: 0
    }
  });
  shop_assistant_view_model.value = 0
}


function change_page(step: number) {
  let max_page = Math.ceil(shopAssistantsCnt.value / current_page_size.value)
  if (current_page_num.value + step > max_page || current_page_num.value + step < 1) {
    ElMessage.info({
      message: '到头啦！',
      type: 'info',
      duration: 600
    })
    return
  }
  current_page_num.value += step;
  get_shop_assistant_list()
  nextTick()

}
function handle_current_change(val: number) {
  current_page_num.value = val;
  get_shop_assistant_list()
  nextTick()
}

function change_order(order: string) {
  shop_assistant_order.value = order;
  show_cnt_tag.value = order === 'call_cnt';
  get_shop_assistant_list()
  nextTick()
}

function omit_shop_assistant_desc(shop_assistant_desc:string ,n = 8){
  if (shop_assistant_desc.length > n){
    return shop_assistant_desc.slice(0,n) + '...'
  }
  return shop_assistant_desc
}
const scrollbar_height = ref(0)

async function publish_user_comment() {
  let params = {
    "shop_assistant_id": shop_assistant_choose.value.id,
    "comment_level": user_comment_level.value,
    "comment_content": user_comment_input.value
  }
  let res = await shop_assistant_comment(params)
  if (!res.error_status) {
    ElMessage.success({
          message: "评论成功！",
          type: 'success',
          duration: 800
        }
    )
    shop_assistant_choose.value.comments.push({
      assistant_id: 0,
      id: 0,
      update_time: "",
      user_id: 0,
      comment_level: user_comment_level.value,
      comment_content: user_comment_input.value,
      create_time: new Date().toLocaleString(),
      user_avatar: userinfo.value.user_avatar,
      user_name: userinfo.value.user_name
    })
    user_comment_input.value = ''
    user_comment_level.value = null

  }
}
async function handleResize(){
  scrollbar_height.value = window.innerHeight - 72 - 67;

}

const props = defineProps({
  view_model: {
    type:  Number,
    required: false,
    default: 0
  },
  choose_shop_assistant_id: {
    type: Number,
    default: null,
    required: false
  }
});

onMounted(async () => {
  // 监听窗口变化
  window.addEventListener('resize', handleResize);
  await handleResize()
  // 获取用户信息
  userinfo.value = await getInfo()
  await get_shop_assistant_list()

  shop_assistant_view_model.value = props.view_model
  if (props.choose_shop_assistant_id) {
    let res = await shop_assistant_get({
      "shop_assistant_id": props.choose_shop_assistant_id,
    })
    if (!res.error_status) {
      shop_assistant_choose.value = res.result
      await nextTick()
    }

  }
  if (route.query.choose_shop_assistant_id) {
    let res = await shop_assistant_get({
      "shop_assistant_id": route.query.choose_shop_assistant_id,
    })
    if (!res.error_status) {
      shop_assistant_choose.value = res.result

      await nextTick()
    }

  }
  if (route.query.view_model){
    shop_assistant_view_model.value = Number(route.query.view_model)
  }



})
</script>

<template>
  <div class="shop-assistant-list" >
    <div class="shop-assistant-list-header">
      <div class="step-router">
        <el-button class="step-button" style="height: 40px"
                   :disabled="shop_assistant_view_model === 0"
                   @click="change_assistant_view_model(0)">
          <el-image v-if="shop_assistant_view_model !== 0" src="images/arrow_left_black.svg" style="width: 14px;height: 14px"/>
          <el-image v-else src="images/arrow_left_grey.svg" style="width: 14px;height: 14px"/>
        </el-button>
        <el-button class="step-button" style="height: 40px" disabled>
          <el-image src="images/arrow_right_grey.svg" style="width: 14px;height: 14px"/>
        </el-button>


      </div>
      <div v-if="shop_assistant_view_model === 1 && shop_assistant_choose"
           style="display: flex;align-items: center;padding: 0 12px;gap: 8px">
        <el-avatar :src="shop_assistant_choose.assistant_avatar" style="background: #FFFFFF"></el-avatar>
        <el-text style="font-size: 16px;font-weight: 600;line-height: 24px; color: #101828">
          {{ shop_assistant_choose.assistant_name }}
        </el-text>
      </div>
      <div class="order-button" v-if="shop_assistant_view_model === 0">
        <el-button :class="shop_assistant_order === 'create_time' ? 'order-button-left' : 'order-button-default'"
                   @click="change_order('create_time')">
          <el-image src="images/green_dot.svg"
                    v-if="shop_assistant_order === 'create_time'"
                    style="display: flex;align-items: center;margin: 0 6px 0 6px;"
          />
          <el-text>最近上架</el-text>
        </el-button>
        <el-button :class="shop_assistant_order === 'call_cnt' ? 'order-button-right' : 'order-button-default'"
                   @click="change_order('call_cnt')">
          <el-image src="images/green_dot.svg"
                    v-if="shop_assistant_order === 'call_cnt'"
                    style="display: flex;align-items: center;margin: 0 6px 0 6px;"
          />
          <el-text>最受欢迎</el-text>
        </el-button>
      </div>

      <div class="assistant-detail-info-button-box" v-if="shop_assistant_view_model === 1">
        <el-button class="shop-assistant-card-detail-button"
                   v-if="shop_assistant_choose.assistant_source==4"
                   @click="off_listing_shop_assistant(shop_assistant_choose)">
          <el-text   class="shop-assistant-card-detail-button-text">下架</el-text>
        </el-button>
        <el-button class="shop-assistant-card-detail-button"
                   v-else-if="!shop_assistant_choose.authority_create_time"
                   @click="subscribe_shop_assistant(shop_assistant_choose)">
          <el-text class="shop-assistant-card-detail-button-text">订阅</el-text>
        </el-button>
        <el-button class="shop-assistant-card-detail-button"
                   v-else
                   @click="shop_assistant_unsubscribe_vis=true">
          <el-text class="shop-assistant-card-detail-button-text">取消订阅</el-text>
        </el-button>
        <el-dialog v-model="shop_assistant_unsubscribe_vis" width="480px" >
          <template #header>
            <el-text style="font-size: 18px;font-weight: 600;line-height: 28px;color: #101828">取消订阅</el-text><br>
            <el-text>是否确认取消，将无法继续使用？</el-text>
          </template>
          <template #footer>
            <div style="display: flex;flex-direction: row;gap: 12px; height: 70px;
              align-items: center">
              <el-button @click="shop_assistant_unsubscribe_vis=false" style="
              width: 210px;height:44px;border-radius: 8px;gap: 8px; padding: 10px 18px 10px 18px;
              border: 1px solid #D0D5DD;box-shadow: 0 1px 2px 0 #1018280D;">
                <el-text style="font-size: 16px;font-weight: 600;line-height: 24px;color: #344054">取消</el-text>
              </el-button>
              <el-button @click="unsubscribe_shop_assistant(shop_assistant_choose)" style="
              background: #D92D20;width: 210px;height:44px;border-radius: 8px;gap: 8px; padding: 10px 18px 10px 18px;
              border: 1px solid #D92D20;box-shadow: 0 1px 2px 0 #1018280D;">
                <el-text style="font-size: 16px;font-weight: 600;line-height: 24px;color: #FFFFFF">
                  取消订阅
                </el-text>
              </el-button>
            </div>
          </template>

        </el-dialog>
      </div>
      <div class="right-button-box" v-if="shop_assistant_view_model === 0">
        <el-input :prefix-icon="Search" placeholder="搜索助手" size="large"
                  v-model="shop_assistant_search_key_word"
                  @change="get_shop_assistant_list"
                  clearable
        />


      </div>

    </div>
    <el-scrollbar wrap-style="width:100%" view-style="width:100%"  >
      <div v-if="shop_assistant_view_model === 1" class="shop-assistant-detail-box">
        <div class="shop-assistant-detail-box-left">
          <div class="shop-assistant-detail-score">
            <div>
              <el-text style="color: #FFFFFF">平均评分
                <strong>{{shop_assistant_choose.avg_level}}</strong>
              </el-text>
            </div>
            <div>
              <el-rate v-model="shop_assistant_choose.avg_level" :colors="colors" disabled/>
            </div>
            <div>
              <el-text style="color: #FFFFFF">订阅量排名
                <strong>前{{shop_assistant_choose.subscribe_rank}}%</strong>
              </el-text>
            </div>
            <div>
              <el-tooltip content="订阅用户数占比">
                <el-progress :percentage="shop_assistant_choose.subscribe_range"
                             :stroke-width="19"
                             type="line"
                             :text-inside="true"
                />
              </el-tooltip>

            </div>

          </div>
          <div  class="shop-assistant-detail-base-info">
            <div>
              <h3>基本信息</h3>
            </div>
            <div class="shop-assistant-detail-col-box">
              <div v-for="(attr_name,value) in shop_assistant_col_map" class="shop-assistant-detail-col">
                <div>
                  <el-text style=" font-size: 14px;font-weight: 400;line-height: 20px;color: #475467;">{{attr_name}}</el-text>
                </div>
                <div>
                  <el-text>{{shop_assistant_choose[value]}}</el-text>
                </div>
              </div>
            </div>

          </div>
          <div class="shop-assistant-detail-tag-box">
            <div><h3>特征标签</h3></div>
            <div class="shop-assistant-detail-tags">
              <el-tag type="info" v-for="(item,index) in shop_assistant_choose.assistant_tags">
                {{item}}
              </el-tag>
            </div>

          </div>
        </div>
        <div class="shop-assistant-detail-box-middle">
          <div class="shop-assistant-detail-desc-box">
            <div>
              <h3>助手描述</h3>
            </div>
            <div v-text="shop_assistant_choose.assistant_desc"  v-bind:style="{ 'white-space': 'pre-wrap' }"/>
          </div>

          <br>


        </div>
        <div class="shop-assistant-detail-box-right">
          <div class="shop-assistant-detail-form">
            <div style="display: flex;width: 100%" class="shop-assistant-detail-form-box">
              <el-input v-model="user_comment_input" type="textarea" resize="none" show-word-limit
                        placeholder="请输入您的评价或反馈" maxlength="4096"
                        input-style="border:0 ;border-radius:8px 8px 0 0"
                        rows="8"
                        class = "shop-assistant-detail-form-input"
              />

            </div>
            <div  class="shop-assistant-detail-form-footer">
              <el-rate v-model="user_comment_level" :colors="colors" />
              <el-button style="background-color: #1570ef;border: 1px solid #1570EF;
              box-shadow: 0 1px 2px 0 #1018280D;border-radius: 16px;" @click="publish_user_comment">
                <el-text style="font-size: 14px;font-weight: 600;line-height: 20px; color: white">提交</el-text>
              </el-button>
            </div>
          </div>
          <div class="shop-assistant-detail-comment-box">
            <el-scrollbar>
              <div class="shop-assistant-detail-comment" v-for="comment in shop_assistant_choose.comments">
                <div class="shop-assistant-detail-comment-head">
                  <div class="shop-assistant-comment-user-info">
                    <div>
                      <el-avatar :src="comment.user_avatar" v-if = "comment.user_avatar"/>
                      <el-avatar v-else style="background: #D1E9FF">
                        <el-text style="color:#1570EF;">
                          {{ comment.user_name_py }}
                        </el-text>
                      </el-avatar>
                    </div>
                    <div style="display: flex;flex-direction: column">
                      <div><el-text><strong>{{comment.user_name}}</strong></el-text></div>
                      <div><el-text>{{comment.create_time}}</el-text></div>
                    </div>

                  </div>
                  <div >
                    <el-rate v-model="comment.comment_level" :colors="colors" disabled/>
                  </div>
                </div>
                <div class="shop-assistant-detail-comment-body" v-text="comment.comment_content"
                     v-bind:style="{ 'white-space': 'pre-wrap' }">

                </div>
            </div>
            </el-scrollbar>
          </div>
        </div>

      </div>
      <div v-else class="shop-assistant-list-body">
        <div class="shop-assistant-card" v-for="(item , index) in shopAssistantList">
          <div class="shop-assistant-card-head">
            <div class="shop-assistant-card-info">
              <el-image :src="item.assistant_avatar" style="width: 40px;height: 40px"/>
              <div style="flex: 1">

                <el-tooltip v-if="item.assistant_name.length > 7" effect="light">

                  <el-text style="margin-left: 8px;font-size: 16px;font-weight: 600;line-height: 24px;">

                    {{ omit_shop_assistant_desc(item.assistant_name, 7) }}
                  </el-text>
                  <template #content>
                    <div v-text="item.assistant_name" style="max-width: 400px;display: flex;flex-wrap: wrap">

                    </div>
                  </template>
                </el-tooltip>
                <el-text v-else style="margin-left: 8px;font-size: 16px;font-weight: 600;line-height: 24px;">
                  {{ item.assistant_name }}
                </el-text>
                <br>
                <el-tooltip v-if="item.assistant_desc.length > 10" effect="light">

                  <el-text style="margin-left: 8px;  font-size: 14px; font-weight: 400; line-height: 20px;"
                  >
                    {{ omit_shop_assistant_desc(item.assistant_desc) }}
                  </el-text>
                  <template #content>
                    <div v-text="item.assistant_desc" style="max-width: 400px;display: flex;flex-wrap: wrap">

                    </div>
                  </template>
                </el-tooltip>
                <el-text style="margin-left: 8px;  font-size: 14px; font-weight: 400; line-height: 20px;"
                         v-else
                >
                  {{ item.assistant_desc }}
                </el-text>


              </div>
              <div>
                <el-tag v-if="show_cnt_tag"
                        type="success"
                         style="margin-left: 8px;  font-size: 14px; font-weight: 400; line-height: 20px;">
                  {{ item.call_cnt }}
                </el-tag>
                 <el-tag v-else type="success">
                   {{item.create_time.split(' ')[0]}}
                 </el-tag>
              </div>

            </div>
            <div class="shop-assistant-card-tag">

                <el-tag v-for="(tag , index) in item.assistant_tags.slice(0, 3)" :key="index"
                        type="info"
                        style="margin-right: 8px;">
                  {{ tag }}
                </el-tag>

            </div>
          </div>
          <div class="shop-assistant-card-footer">
            <el-button text class="shop-assistant-card-footer-button"
                       @click="change_assistant_view_model(1, item.id)">
              <el-text class="button-text">详情</el-text>
            </el-button>
            <el-button text color="#175CD3" class="shop-assistant-card-footer-button"
                       v-if="item.assistant_source==4"
                       @click="off_listing_shop_assistant(item)">
              <el-text style="color: #175CD3;" class="button-text">下架</el-text>
            </el-button>
            <el-button text color="#175CD3" class="shop-assistant-card-footer-button"
                       v-else-if="!item.authority_create_time"
                       @click="subscribe_shop_assistant(item)">
              <el-text style="color: #175CD3;" class="button-text">订阅</el-text>
            </el-button>
            <el-button text color="#175CD3" class="shop-assistant-card-footer-button"
                       v-else
                       @click="shop_assistant_choose=item;shop_assistant_unsubscribe_vis=true">
              <el-text style="color: #175CD3;" class="button-text">取消订阅</el-text>
            </el-button>
          </div>

        </div>
        <div v-if="!shopAssistantList.length" style="width: 100%;height: 50vh;
        display: flex;align-items: center;justify-content: center">
          <el-empty description="暂无搜索结果"></el-empty>
        </div>
        <div class="assistant-unsubscribe-confirm-box">
          <el-dialog v-model="shop_assistant_unsubscribe_vis" width="480px" >
            <template #header>
              <el-text style="font-size: 18px;font-weight: 600;line-height: 28px;color: #101828">取消订阅</el-text><br>
              <el-text>是否确认取消，将无法继续使用？</el-text>
            </template>
            <template #footer>
              <div style="display: flex;flex-direction: row;gap: 12px; height: 70px;
              align-items: center">
                <el-button @click="shop_assistant_unsubscribe_vis=false" style="
              width: 210px;height:44px;border-radius: 8px;gap: 8px; padding: 10px 18px 10px 18px;
              border: 1px solid #D0D5DD;box-shadow: 0 1px 2px 0 #1018280D;">
                  <el-text style="font-size: 16px;font-weight: 600;line-height: 24px;color: #344054">取消</el-text>
                </el-button>
                <el-button @click="unsubscribe_shop_assistant(shop_assistant_choose)" style="
              background: #D92D20;width: 210px;height:44px;border-radius: 8px;gap: 8px; padding: 10px 18px 10px 18px;
              border: 1px solid #D92D20;box-shadow: 0 1px 2px 0 #1018280D;">
                  <el-text style="font-size: 16px;font-weight: 600;line-height: 24px;color: #FFFFFF">
                    取消订阅
                  </el-text>
                </el-button>
              </div>
            </template>

          </el-dialog>
        </div>
      </div>
    </el-scrollbar>
    <div class="shop-assistant-list-footer" v-if="shop_assistant_view_model === 0">
      <div class="shop-assistant-list-footer-box">
        <el-button class="shop-assistant-footer-button" @click="change_page(-1)">
          <el-image src="images/arrow_left_black.svg" style="margin-right: 8px"/>
          上一页
        </el-button>
        <el-pagination
            :total="shopAssistantsCnt"
            layout="pager,total"
            :page-size="current_page_size"
            v-model:current-page="current_page_num"
            @current-change="handle_current_change"
        />
        <el-button class="assistant-footer-button" @click="change_page(1)">
          下一页
          <el-image src="images/arrow_right_black.svg" style="margin-left: 8px"/>
        </el-button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.shop-assistant-list {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
}
.shop-assistant-list-header {
  height: 48px;
  border-bottom: 1px solid #D0D5DD;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 24px 12px 24px;
}
.shop-assistant-list-footer {
  height: 80px;
  display: flex;
  align-items: flex-start;
  justify-content: center;
}
.shop-assistant-list-footer-box {
  width: 100%;
  margin: 0 24px;
  border-top: 1px solid #D0D5DD;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  padding: 16px 0 16px 0
}
.shop-assistant-footer-button {
  border: 1px solid #D0D5DD;
  box-shadow: 0 1px 2px 0 #1018280D;
  display: flex;
  justify-content: space-between;
  background: #FFFFFF;

}
.shop-assistant-list-body {
  flex: 1;
  display: flex;
  gap: 16px;
  padding: 16px;
  flex-wrap: wrap;
  align-content: flex-start;
  margin: 0 24px;
}

.shop-assistant-card {
  width: 350px;
  min-width: 250px;
  border: 1px solid #D0D5DD;
  box-shadow: 0 1px 2px 0 #1018280D;
  border-radius: 12px;
}

.shop-assistant-card-head {
  height: 94px;
  padding: 24px;
  gap: 24px;
  display: flex;
  flex-direction: column;
}

.shop-assistant-card-info {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 8px;
  justify-content: space-between;

}

.shop-assistant-card-footer {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  border-top: 1px solid #EAECF0;
}



.shop-assistant-card-footer-button {
  width: 80px;
  height: 50px;
  background: #FFFFFF !important;
  border-radius: 16px;

}
.shop-assistant-card-detail-button{
  width: 80px;
  height: 40px;
  border-radius: 8px;
  border: 1px solid #1570EF;
  padding: 10px 16px 10px 16px;
  background: #1570EF;
}
.shop-assistant-card-detail-button-text{
  color: #FFFFFF;
  font-size: 14px;
  font-weight: 600;
  line-height: 20px;


}
.step-button {
  border: 0;
}

.el-button {
  margin-left: 0;
}


.order-button {
  border: 1px solid #D0D5DD;
  box-shadow: 0 1px 2px 0 #1018280D;
  border-radius: 8px;

}

.order-button-left {
  border-width: 0 1px 0 0;
  border-radius: 8px;
  background: #F9FAFB;
  height: 40px
}

.order-button-right {
  border-width: 0 0 0 1px;
  border-radius: 8px;
  background: #F9FAFB;
  height: 40px
}

.order-button-default {
  border: 0;
  border-radius: 8px;
  height: 40px
}
.shop-assistant-detail-box{
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: row;
}
.shop-assistant-detail-box-left{

  display: flex;
  flex-direction: column;
  padding: 24px;
  gap: 24px;
}
.shop-assistant-detail-box-middle{
  max-width: 640px;
  min-width: 350px;
  display: flex;
  flex-direction: column;
  padding: 24px 0;
  gap: 10px;
}
.shop-assistant-detail-box-right{
  max-width: 700px;
  min-width: 320px;
  display: flex;
  flex-direction: column;
  padding: 24px;
  gap: 24px;
}

.shop-assistant-detail-score{
  width: 352px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 24px;
  border-radius: 16px;
  background: #2760F6;

}
.shop-assistant-detail-base-info{
  width: 352px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 24px;
  border-radius: 16px;
  background: #FFFFFF;
  border: 1px solid #D0D5DD;
}

.shop-assistant-detail-col-box{
  display: flex;
  flex-direction: row;
  gap: 32px;
  align-content: flex-start;
  flex-wrap: wrap;
}

.shop-assistant-detail-col{

  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 8px;
  min-width: 100px;
}

.shop-assistant-detail-tag-box{
  display: flex;
  flex-direction: column;
  gap: 24px;
  padding: 24px;
  align-content: flex-start;
  flex-wrap: wrap;
  background: #FFFFFF;
  border: 1px solid #D0D5DD;
  border-radius: 16px;
}
.shop-assistant-detail-tags{
  display: flex;
  flex-direction: row;
  gap: 16px;
  flex-wrap: wrap;
}
.shop-assistant-detail-desc-box{
  display: flex;
  flex-direction: column;
  gap: 24px;
  padding: 24px;
  align-content: flex-start;
  flex-wrap: wrap;
  background: #FFFFFF;
  border: 1px solid #D0D5DD;
  border-radius: 16px;
  width: calc(100% - 48px);

}
.shop-assistant-detail-form{
  display: flex;
  flex-direction: column;
  align-content: flex-start;
  flex-wrap: wrap;
  background: #FFFFFF;
  border-width: 1px;
  border-style: solid;
  border-color: #D0D5DD;
  border-radius: 8px ;
  min-width: 280px;
}
.shop-assistant-detail-form-footer {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  padding: 10px 16px;
  border-color: #D0D5DD;
  background-color: #F9FAFB;
  border-radius: 0 0 8px 8px;
  border-width: 1px 0 0 0 ;
  border-style: solid;

}
.shop-assistant-detail-form-input :deep(.el-textarea__inner){
  box-shadow: 0 0 0 0;
}
.shop-assistant-detail-form-input :deep(.el-textarea__inner::-webkit-scrollbar){
  width: 6px ;
  height: 6px ;
}
.shop-assistant-detail-form-input :deep(.el-textarea__inner::-webkit-scrollbar-thumb) {
  border-radius: 3px ;
  -moz-border-radius: 3px ;
  -webkit-border-radius: 3px ;
  background-color: #c3c3c3 ;
}
.shop-assistant-detail-form-input :deep(.el-textarea__inner::-webkit-scrollbar-track) {
  background-color: transparent ;
}

.shop-assistant-detail-comment-box{
  display: flex;
  flex-direction: column;
  gap: 10px;
  background: #FFFFFF;
  border: 0 solid #D0D5DD;
  border-radius: 16px;
  min-width: 280px;
  height: 600px;
}

.shop-assistant-detail-comment{
  display: flex;
  flex-direction: column;
  gap: 4px;
  margin-top: 6px;

}
.shop-assistant-detail-comment-head{
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}
.shop-assistant-comment-user-info{
  display: flex;
  flex-direction: row;
  gap: 8px;
  align-items: center;

}



.shop-assistant-detail-comment-body{
  background-color: #F2F4F7;
  padding: 10px 14px;
  border-radius: 0 8px 8px 8px;
  width: calc(100% - 28px);
}

</style>
