<script setup lang="ts">
import { format, parseISO } from 'date-fns';
import * as echarts from 'echarts';
import gsap from 'gsap';
import { onMounted, ref, reactive, watch } from 'vue';
import { onBeforeUnmount } from 'vue-demi';
import { useRoute } from 'vue-router';
import { getDashboardIndex, getAllCompany } from '@/api/dashboard';

import router from '@/router';
import { useUserInfoStore } from '@/stores/userInfoStore';
import { ICompany } from '@/types/contacts';
const props = defineProps({
  tab: {
    type: String,
    default: 'user'
  }
});
const route = useRoute();
const currentIndex = route.path;
const filteredComponents = ref([
  {
    name: '运营指标',
    url: '/next-console/dashboard/user_activity'
  }
]);
const userInfoStore = useUserInfoStore();
const userCompanyList = ref<ICompany[]>([]);
const selectedTimeRange = ref('month');
const refreshRate = ref(600000);
const refreshInterval = ref(null);
const targetCompany = ref('');
const indexBeginTime = ref();
const currentTab = ref('user');

const echartsData = reactive({
  user: {
    dnu: {
      ref: null,
      options: {
        title: {
          text: '每日新增注册用户数'
        },
        tooltip: {
          trigger: 'axis'
        },
        xAxis: {
          type: 'category',
          data: null,
          axisLabel: {
            formatter: function (value) {
              return value.substring(0, 10); // 显示到小时
            },
            rotate: 45 // 标签旋转45度以防止重叠
          }
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            data: null,
            type: 'line',
            smooth: true,
            name: '新增用户数'
          }
        ],
        toolbox: {
          show: true,
          feature: {
            dataView: { readOnly: false },
            magicType: { type: ['line', 'bar'] },
            saveAsImage: {}
          }
        }
      }
    },
    dnu_sd: {
      ref: null,
      options: {
        title: {
          text: '每日新增用户来源渠道'
        },
        tooltip: {
          trigger: 'axis',
          showContent: false
        },
        legend: {
          data: ['营销推荐', '官网注册', '用户推荐', '未知渠道']
        },
        dataset: {
          source: []
        },
        xAxis: {
          type: 'category',
          axisLabel: {
            formatter: function (value) {
              return value.substring(0, 10); // 显示到小时
            },
            rotate: 45 // 标签旋转45度以防止重叠
          }
        },
        yAxis: { gridIndex: 0 },
        grid: { top: '55%' },
        series: [
          {
            name: '营销推荐',
            type: 'line',
            smooth: true,
            seriesLayoutBy: 'row',
            emphasis: { focus: 'series' }
          },
          {
            name: '官网注册',
            type: 'line',
            smooth: true,
            seriesLayoutBy: 'row',
            emphasis: { focus: 'series' }
          },
          {
            name: '用户推荐',
            type: 'line',
            smooth: true,
            seriesLayoutBy: 'row',
            emphasis: { focus: 'series' }
          },
          {
            name: '未知渠道',
            type: 'line',
            smooth: true,
            seriesLayoutBy: 'row',
            emphasis: { focus: 'series' }
          },
          {
            type: 'pie',
            id: 'pie',
            radius: '30%',
            center: ['50%', '25%'],
            emphasis: {
              focus: 'self'
            },
            label: {
              formatter: '{b}: {@[1]} ({d}%)'
            },
            encode: {
              itemName: 'source_channel',
              value: '1',
              tooltip: '1'
            }
          }
        ]
      }
    },
    d1_retention: {
      ref: null,
      options: {
        title: {
          text: '新增用户一日留存'
        },
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: ['一日后留存用户', '当日新增用户']
        },
        xAxis: {
          type: 'category',
          data: [],
          axisLabel: {
            formatter: function (value) {
              return value.substring(0, 10); // 显示到小时
            },
            rotate: 45 // 标签旋转45度以防止重叠
          }
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            data: [],
            type: 'line',
            smooth: true,
            name: '一日后留存用户'
          },
          {
            data: [],
            type: 'line',
            smooth: true,
            name: '当日新增用户'
          }
        ],
        toolbox: {
          show: true,
          feature: {
            dataView: { readOnly: false },
            magicType: { type: ['line', 'bar'] },

            saveAsImage: {}
          }
        }
      }
    },
    all_cvr: {
      ref: null,
      options: {
        title: {
          text: '整体转化率'
        },
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b} : {c}%'
        },
        toolbox: {
          feature: {
            dataView: { readOnly: false },

            saveAsImage: {}
          }
        },
        legend: {
          data: ['所有注册用户', 'AI工作台', '资源库', '全部使用']
        },
        series: [
          {
            name: '用户转化率',
            type: 'funnel',
            left: '10%',
            top: 60,
            bottom: 60,
            width: '80%',
            min: 0,
            max: 100,
            minSize: '0%',
            maxSize: '100%',
            sort: 'descending',
            gap: 2,
            label: {
              show: true,
              position: 'inside'
            },
            labelLine: {
              length: 10,
              lineStyle: {
                width: 1,
                type: 'solid'
              }
            },
            itemStyle: {
              borderColor: '#fff',
              borderWidth: 1
            },
            emphasis: {
              label: {
                fontSize: 20
              }
            },
            data: [
              { value: 60, name: '所有注册用户' },
              { value: 40, name: 'AI工作台' },
              { value: 100, name: '资源库' },
              { value: 100, name: '全部使用' }
            ]
          }
        ]
      }
    },
    new_cvr: {
      ref: null,
      options: {
        title: {
          text: '新增转化率'
        },
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b} : {c}%'
        },
        toolbox: {
          feature: {
            dataView: { readOnly: false },

            saveAsImage: {}
          }
        },
        legend: {
          data: ['所有注册用户', 'AI工作台', '资源库', '全部使用']
        },
        series: [
          {
            name: '用户转化率',
            type: 'funnel',
            left: '10%',
            top: 60,
            bottom: 60,
            width: '80%',
            min: 0,
            max: 100,
            minSize: '0%',
            maxSize: '100%',
            sort: 'descending',
            gap: 2,
            label: {
              show: true,
              position: 'inside'
            },
            labelLine: {
              length: 10,
              lineStyle: {
                width: 1,
                type: 'solid'
              }
            },
            itemStyle: {
              borderColor: '#fff',
              borderWidth: 1
            },
            emphasis: {
              label: {
                fontSize: 20
              }
            },
            data: [
              { value: 60, name: '所有注册用户' },
              { value: 40, name: 'AI工作台' },
              { value: 100, name: '资源库' },
              { value: 100, name: '全部使用' }
            ]
          }
        ]
      }
    }
  },
  workbench: {
    uv_hour: {
      ref: null,
      options: {
        title: {
          text: '每小时问答用户数'
        },
        tooltip: {
          trigger: 'axis'
        },
        xAxis: {
          type: 'category',
          data: [],
          axisLabel: {
            formatter: function (value) {
              return value.substring(0, 13); // 显示到小时
            },
            rotate: 45 // 标签旋转45度以防止重叠
          }
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            data: [],
            type: 'line',
            smooth: true
          }
        ],
        toolbox: {
          show: true,
          feature: {
            dataView: { readOnly: false },
            magicType: { type: ['line', 'bar'] },

            saveAsImage: {}
          }
        }
      }
    },
    uv_day: {
      ref: null,
      options: {
        title: {
          text: '每天问答用户数'
        },
        tooltip: {
          trigger: 'axis'
        },
        xAxis: {
          type: 'category',
          data: [],
          axisLabel: {
            formatter: function (value) {
              return value.substring(0, 10); // 显示到小时
            },
            rotate: 45 // 标签旋转45度以防止重叠
          }
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            data: [],
            type: 'line',
            smooth: true
          }
        ],
        toolbox: {
          show: true,
          feature: {
            dataView: { readOnly: false },
            magicType: { type: ['line', 'bar'] },

            saveAsImage: {}
          }
        }
      }
    },
    avg_qa_retention: {
      ref: null,
      options: {
        title: {
          text: '用户平均问答数'
        },
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: ['当日所有用户', '第1日留存用户', '第7日留存用户', '第15日留存用户', '第30日留存用户']
        },
        xAxis: {
          type: 'category',
          data: [],
          axisLabel: {
            formatter: function (value) {
              return value.substring(0, 13);
            },
            rotate: 45
          }
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            data: [],
            type: 'line',
            smooth: true,
            name: '当日所有用户'
          },
          {
            data: [],
            type: 'line',
            smooth: true,
            name: '第1日留存用户'
          },
          {
            data: [],
            type: 'line',
            smooth: true,
            name: '第7日留存用户'
          },
          {
            data: [],
            type: 'line',
            smooth: true,
            name: '第15日留存用户'
          },
          {
            data: [],
            type: 'line',
            smooth: true,
            name: '第30日留存用户'
          }
        ],
        toolbox: {
          show: true,
          feature: {
            dataView: { readOnly: false },
            magicType: { type: ['line', 'bar'] },

            saveAsImage: {}
          }
        }
      }
    },
    qa_hour: {
      ref: null,
      options: {
        title: {
          text: '每小时新增提问数'
        },
        tooltip: {
          trigger: 'axis'
        },
        xAxis: {
          type: 'category',
          data: [],
          axisLabel: {
            formatter: function (value) {
              return value.substring(0, 13); // 显示到小时
            },
            rotate: 45 // 标签旋转45度以防止重叠
          }
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            data: [],
            type: 'line',
            smooth: true
          }
        ],
        toolbox: {
          show: true,
          feature: {
            dataView: { readOnly: false },
            magicType: { type: ['line', 'bar'] },

            saveAsImage: {}
          }
        }
      }
    },
    qa_day: {
      ref: null,
      options: {
        title: {
          text: '每天新增提问数'
        },
        tooltip: {
          trigger: 'axis'
        },
        xAxis: {
          type: 'category',
          data: [],
          axisLabel: {
            formatter: function (value) {
              return value.substring(0, 10); // 显示到小时
            },
            rotate: 45 // 标签旋转45度以防止重叠
          }
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            data: [],
            type: 'line',
            smooth: true
          }
        ],
        toolbox: {
          show: true,
          feature: {
            dataView: { readOnly: false },
            magicType: { type: ['line', 'bar'] },

            saveAsImage: {}
          }
        }
      }
    },
    avg_session_retention: {
      ref: null,
      options: {
        title: {
          text: '用户平均会话数'
        },
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: ['当日所有用户', '第1日留存用户', '第7日留存用户', '第15日留存用户', '第30日留存用户']
        },
        xAxis: {
          type: 'category',
          data: [],
          axisLabel: {
            formatter: function (value) {
              return value.substring(0, 13);
            },
            rotate: 45
          }
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            data: [],
            type: 'line',
            smooth: true,
            name: '当日所有用户'
          },
          {
            data: [],
            type: 'line',
            smooth: true,
            name: '第1日留存用户'
          },
          {
            data: [],
            type: 'line',
            smooth: true,
            name: '第7日留存用户'
          },
          {
            data: [],
            type: 'line',
            smooth: true,
            name: '第15日留存用户'
          },
          {
            data: [],
            type: 'line',
            smooth: true,
            name: '第30日留存用户'
          }
        ],
        toolbox: {
          show: true,
          feature: {
            dataView: { readOnly: false },
            magicType: { type: ['line', 'bar'] },

            saveAsImage: {}
          }
        }
      }
    },
    all_retention: {
      ref: null,
      options: {
        title: {
          text: '新增用户留存'
        },
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: ['当日活跃用户', '7日留存用户', '15日留存用户', '30日留存用户']
        },
        xAxis: {
          type: 'category',
          data: [],
          axisLabel: {
            formatter: function (value) {
              return value.substring(0, 13);
            },
            rotate: 45
          }
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            data: [],
            type: 'line',
            smooth: true,
            name: '当日活跃用户'
          },
          {
            data: [],
            type: 'line',
            smooth: true,
            name: '7日留存用户'
          },
          {
            data: [],
            type: 'line',
            smooth: true,
            name: '15日留存用户'
          },
          {
            data: [],
            type: 'line',
            smooth: true,
            name: '30日留存用户'
          }
        ],
        toolbox: {
          show: true,
          feature: {
            dataView: { readOnly: false },
            magicType: { type: ['line', 'bar'] },

            saveAsImage: {}
          }
        }
      }
    },
    session_hour: {
      ref: null,
      options: {
        title: {
          text: '每小时新增会话数'
        },
        tooltip: {
          trigger: 'axis'
        },
        xAxis: {
          type: 'category',
          data: [],
          axisLabel: {
            formatter: function (value) {
              return value.substring(0, 13); // 显示到小时
            },
            rotate: 45 // 标签旋转45度以防止重叠
          }
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            data: [],
            type: 'line',
            smooth: true
          }
        ],
        toolbox: {
          show: true,
          feature: {
            dataView: { readOnly: false },
            magicType: { type: ['line', 'bar'] },

            saveAsImage: {}
          }
        }
      }
    },
    session_day: {
      ref: null,
      options: {
        title: {
          text: '每天新增会话数'
        },
        tooltip: {
          trigger: 'axis'
        },
        xAxis: {
          type: 'category',
          data: [],
          axisLabel: {
            formatter: function (value) {
              return value.substring(0, 10); // 显示到小时
            },
            rotate: 45 // 标签旋转45度以防止重叠
          }
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            data: [],
            type: 'line',
            smooth: true
          }
        ],
        toolbox: {
          show: true,
          feature: {
            dataView: { readOnly: false },
            magicType: { type: ['line', 'bar'] },

            saveAsImage: {}
          }
        }
      }
    }
  },
  resource: {
    doc_view_top: {
      ref: null,
      options: {
        title: {
          text: '文档阅读排行'
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'value',
          boundaryGap: [0, 0.01]
        },
        yAxis: {
          type: 'category',
          data: []
        },
        series: [
          {
            data: [],
            type: 'bar'
          }
        ],
        toolbox: {
          show: true,
          feature: {
            dataView: { readOnly: false },
            magicType: { type: ['line', 'bar'] },

            saveAsImage: {}
          }
        }
      }
    },
    user_view_top: {
      ref: null,
      options: {
        title: {
          text: '用户阅读排行'
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'value',
          boundaryGap: [0, 0.01]
        },
        yAxis: {
          type: 'category',
          data: []
        },
        series: [
          {
            data: [],
            type: 'bar'
          }
        ],
        toolbox: {
          show: true,
          feature: {
            dataView: { readOnly: false },
            magicType: { type: ['line', 'bar'] },

            saveAsImage: {}
          }
        }
      }
    },
    doc_download_top: {
      ref: null,
      options: {
        title: {
          text: '文档下载排行'
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'value',
          boundaryGap: [0, 0.01]
        },
        yAxis: {
          type: 'category',
          data: []
        },
        series: [
          {
            data: [],
            type: 'bar'
          }
        ],
        toolbox: {
          show: true,
          feature: {
            dataView: { readOnly: false },
            magicType: { type: ['line', 'bar'] },

            saveAsImage: {}
          }
        }
      }
    },
    user_download_top: {
      ref: null,
      options: {
        title: {
          text: '用户下载排行'
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'value',
          boundaryGap: [0, 0.01]
        },
        yAxis: {
          type: 'category',
          data: []
        },
        series: [
          {
            data: [],
            type: 'bar'
          }
        ],
        toolbox: {
          show: true,
          feature: {
            dataView: { readOnly: false },
            magicType: { type: ['line', 'bar'] },

            saveAsImage: {}
          }
        }
      }
    }
  }
});
const uvCount = ref(0);
const qaCount = ref(0);
const sessionCount = ref(0);
const docReadCount = ref(0);
const docDownloadCount = ref(0);

function transTimeRange() {
  //根据selectedTimeRange计算indexBeginTime，end_begin_time
  if (!selectedTimeRange.value) {
    indexBeginTime.value = null;
    return;
  }
  const start = new Date();
  if (selectedTimeRange.value === 'today') {
    start.setHours(0, 0, 0, 0);
  } else if (selectedTimeRange.value === 'week') {
    start.setTime(start.getTime() - 3600 * 1000 * 24 * 7);
  } else if (selectedTimeRange.value === 'month') {
    start.setTime(start.getTime() - 3600 * 1000 * 24 * 31);
  } else if (selectedTimeRange.value === 'quarter') {
    start.setTime(start.getTime() - 3600 * 1000 * 24 * 7 * 31 * 4);
  } else if (selectedTimeRange.value === 'year') {
    start.setTime(start.getTime() - 3600 * 1000 * 24 * 7 * 365);
  }

  indexBeginTime.value = format(parseISO(start.toISOString()), 'yyyy-MM-dd HH:mm:ss');
}
async function changeRefreshRate() {
  if (refreshInterval.value) {
    clearInterval(refreshInterval.value);
  }
  if (refreshRate.value !== 0) {
    refreshInterval.value = setInterval(async () => {
      await handleTabChange(currentTab.value);
    }, refreshRate.value);
  }
}
async function searchAllCompanyOption() {
  let params = {};
  let res = await getAllCompany(params);
  if (!res.error_status) {
    userCompanyList.value = res.result;
  }
}
// 用户相关
async function getDnu() {
  const params = {
    index_name: 'dnu',
    begin_time: indexBeginTime.value,
    top: '',
    company_id: targetCompany.value
  };
  const res = await getDashboardIndex(params);
  if (!res.error_status) {
    echartsData.user.dnu.options.xAxis.data = [];
    echartsData.user.dnu.options.series[0].data = [];
    for (const item of res.result.dnu) {
      echartsData.user.dnu.options.xAxis.data.push(item.day);
      echartsData.user.dnu.options.series[0].data.push(item.dnu);
    }
    if (!echartsData.user.dnu.ref && document.getElementById('dnu')) {
      echartsData.user.dnu.ref = echarts.init(document.getElementById('dnu'), null, { width: 500, height: 300 });
    }
    echartsData.user.dnu.ref?.setOption(echartsData.user.dnu.options);
  }
}
async function getDnuSd() {
  const params = {
    index_name: 'dnu_sd',
    begin_time: indexBeginTime.value,
    top: '',
    company_id: targetCompany.value
  };
  const res = await getDashboardIndex(params);
  if (!res.error_status) {
    echartsData.user.dnu_sd.options.dataset.source = res.result.dnu_sd;
  }
  if (!echartsData.user.dnu_sd.ref && document.getElementById('dnu_sd')) {
    echartsData.user.dnu_sd.ref = echarts.init(document.getElementById('dnu_sd'), null, { width: 800, height: 300 });
  }

  echartsData.user.dnu_sd.ref?.on('updateAxisPointer', function (event: any) {
    const xAxisInfo = event.axesInfo[0];
    if (xAxisInfo) {
      const dimension = xAxisInfo.value + 1;
      echartsData.user.dnu_sd.ref?.setOption({
        series: {
          id: 'pie',
          label: {
            formatter: '{b}: {@[' + dimension + ']} ({d}%)'
          },

          encode: {
            value: dimension,
            tooltip: dimension
          }
        }
      });
    }
  });
  echartsData.user.dnu_sd.ref?.setOption(echartsData.user.dnu_sd.options);
}
async function getAllCvr() {
  const params = {
    index_name: 'all_cvr',
    begin_time: indexBeginTime.value,
    top: '',
    company_id: targetCompany.value
  };
  const res = await getDashboardIndex(params);
  if (!res.error_status) {
    echartsData.user.all_cvr.options.series[0].data = res.result.all_cvr;
  }
  if (!echartsData.user.all_cvr.ref && document.getElementById('all_cvr')) {
    echartsData.user.all_cvr.ref = echarts.init(document.getElementById('all_cvr'), null, { width: 600, height: 300 });
  }
  echartsData.user.all_cvr.ref?.setOption(echartsData.user.all_cvr.options);
}
async function getNewCvr() {
  const params = {
    index_name: 'new_cvr',
    begin_time: indexBeginTime.value,
    top: '',
    company_id: targetCompany.value
  };
  const res = await getDashboardIndex(params);
  if (!res.error_status) {
    echartsData.user.new_cvr.options.series[0].data = res.result.new_cvr;
  }
  if (!echartsData.user.new_cvr.ref && document.getElementById('new_cvr')) {
    echartsData.user.new_cvr.ref = echarts.init(document.getElementById('new_cvr'), null, { width: 600, height: 300 });
  }
  echartsData.user.new_cvr.ref?.setOption(echartsData.user.new_cvr.options);
}
async function getUvCntData() {
  const params = {
    index_name: 'uv',
    begin_time: indexBeginTime.value,
    top: '',
    company_id: targetCompany.value
  };
  const res = await getDashboardIndex(params);
  if (!res.error_status) {
    await gsap.to(uvCount, { duration: 2, value: res.result.uv });
    uvCount.value = res.result.uv;
  }
}
async function getD1Retention() {
  const params = {
    index_name: 'd1_retention',
    begin_time: indexBeginTime.value,
    top: '',
    company_id: targetCompany.value
  };
  const res = await getDashboardIndex(params);
  if (!res.error_status) {
    echartsData.user.d1_retention.options.xAxis.data = [];
    echartsData.user.d1_retention.options.series[0].data = [];
    echartsData.user.d1_retention.options.series[1].data = [];
    for (const item of res.result.d1_retention) {
      echartsData.user.d1_retention.options.series[0].data.push(item.d1_retention);
      echartsData.user.d1_retention.options.series[1].data.push(item.user_cnt);
    }
  }
  if (!echartsData.user.d1_retention.ref && document.getElementById('d1_retention')) {
    echartsData.user.d1_retention.ref = echarts.init(document.getElementById('d1_retention'), null, {
      width: 600,
      height: 300
    });
  }
  echartsData.user.d1_retention.ref?.setOption(echartsData.user.d1_retention.options);
}

// 工作台报表
async function getUvHourData() {
  const params = {
    index_name: 'uv_hour',
    begin_time: indexBeginTime.value,
    top: '',
    company_id: targetCompany.value
  };
  const res = await getDashboardIndex(params);
  if (!res.error_status) {
    echartsData.workbench.uv_hour.options.xAxis.data = [];
    echartsData.workbench.uv_hour.options.series[0].data = [];
    for (const item of res.result.uv_hour) {
      echartsData.workbench.uv_hour.options.xAxis.data.push(item.hour);
      echartsData.workbench.uv_hour.options.series[0].data.push(item.unique_user_count);
    }
    if (!echartsData.workbench.uv_hour.ref && document.getElementById('uv_hour')) {
      echartsData.workbench.uv_hour.ref = echarts.init(document.getElementById('uv_hour'), null, {
        width: 500,
        height: 300
      });
    }
    echartsData.workbench.uv_hour.ref?.setOption(echartsData.workbench.uv_hour.options);
  }
}
async function getUvDayData() {
  const params = {
    index_name: 'uv_day',
    begin_time: indexBeginTime.value,
    top: '',
    company_id: targetCompany.value
  };
  const res = await getDashboardIndex(params);
  if (!res.error_status) {
    echartsData.workbench.uv_day.options.xAxis.data = [];
    echartsData.workbench.uv_day.options.series[0].data = [];
    for (const item of res.result.uv_day) {
      echartsData.workbench.uv_day.options.xAxis.data.push(item.day);
      echartsData.workbench.uv_day.options.series[0].data.push(item.unique_user_count);
    }
    if (!echartsData.workbench.uv_day.ref && document.getElementById('uv_day')) {
      echartsData.workbench.uv_day.ref = echarts.init(document.getElementById('uv_day'), null, {
        width: 500,
        height: 300
      });
    }
    echartsData.workbench.uv_day.ref?.setOption(echartsData.workbench.uv_day.options);
  }
}
async function getAvgQaRetention() {
  const params = {
    index_name: 'avg_qa_retention',
    begin_time: indexBeginTime.value,
    top: '',
    company_id: targetCompany.value
  };
  const res = await getDashboardIndex(params);
  if (!res.error_status) {
    echartsData.workbench.avg_qa_retention.options.xAxis.data = [];
    echartsData.workbench.avg_qa_retention.options.series[0].data = [];
    for (const item of res.result.avg_qa_retention.avg_qa_retention_series) {
      echartsData.workbench.avg_qa_retention.options.xAxis.data.push(item.day);
      echartsData.workbench.avg_qa_retention.options.series[0].data.push(item.avg_qa_count);
    }
    echartsData.workbench.avg_qa_retention.options.series[1].data = [];
    for (const item of res.result.avg_qa_retention.retention_1) {
      echartsData.workbench.avg_qa_retention.options.series[1].data.push(item);
    }
    echartsData.workbench.avg_qa_retention.options.series[2].data = [];
    for (const item of res.result.avg_qa_retention.retention_7) {
      echartsData.workbench.avg_qa_retention.options.series[2].data.push(item);
    }
    echartsData.workbench.avg_qa_retention.options.series[3].data = [];
    for (const item of res.result.avg_qa_retention.retention_15) {
      echartsData.workbench.avg_qa_retention.options.series[3].data.push(item);
    }
    echartsData.workbench.avg_qa_retention.options.series[4].data = [];
    for (const item of res.result.avg_qa_retention.retention_30) {
      echartsData.workbench.avg_qa_retention.options.series[4].data.push(item);
    }
  }
  if (!echartsData.workbench.avg_qa_retention.ref && document.getElementById('avg_qa_retention')) {
    echartsData.workbench.avg_qa_retention.ref = echarts.init(document.getElementById('avg_qa_retention'), null, {
      width: 900,
      height: 300
    });
  }
  echartsData.workbench.avg_qa_retention.ref?.setOption(echartsData.workbench.avg_qa_retention.options);
}
async function getQaCntData() {
  const params = {
    index_name: 'qa',
    begin_time: indexBeginTime.value,
    top: '',
    company_id: targetCompany.value
  };
  const res = await getDashboardIndex(params);
  if (!res.error_status) {
    await gsap.to(qaCount, { duration: 2, value: res.result.qa });
    qaCount.value = res.result.qa;
  }
}
async function getQaHourData() {
  const params = {
    index_name: 'qa_hour',
    begin_time: indexBeginTime.value,
    top: '',
    company_id: targetCompany.value
  };
  const res = await getDashboardIndex(params);
  if (!res.error_status) {
    echartsData.workbench.qa_hour.options.xAxis.data = [];
    echartsData.workbench.qa_hour.options.series[0].data = [];
    for (const item of res.result.qa_hour) {
      echartsData.workbench.qa_hour.options.xAxis.data.push(item.hour);
      echartsData.workbench.qa_hour.options.series[0].data.push(item.unique_qa_count);
    }
    if (!echartsData.workbench.qa_hour.ref && document.getElementById('qa_hour')) {
      echartsData.workbench.qa_hour.ref = echarts.init(document.getElementById('qa_hour'), null, {
        width: 500,
        height: 300
      });
    }
    echartsData.workbench.qa_hour.ref?.setOption(echartsData.workbench.qa_hour.options);
  }
}
async function getQaDayData() {
  const params = {
    index_name: 'qa_day',
    begin_time: indexBeginTime.value,
    top: '',
    company_id: targetCompany.value
  };
  const res = await getDashboardIndex(params);
  if (!res.error_status) {
    echartsData.workbench.qa_day.options.xAxis.data = [];
    echartsData.workbench.qa_day.options.series[0].data = [];
    for (const item of res.result.qa_day) {
      echartsData.workbench.qa_day.options.xAxis.data.push(item.day);
      echartsData.workbench.qa_day.options.series[0].data.push(item.unique_qa_count);
    }
    if (!echartsData.workbench.qa_day.ref && document.getElementById('qa_day')) {
      echartsData.workbench.qa_day.ref = echarts.init(document.getElementById('qa_day'), null, {
        width: 500,
        height: 300
      });
    }
    echartsData.workbench.qa_day.ref?.setOption(echartsData.workbench.qa_day.options);
  }
}
async function getAvgSessionRetention() {
  const params = {
    index_name: 'avg_session_retention',
    begin_time: indexBeginTime.value,
    top: '',
    company_id: targetCompany.value
  };
  const res = await getDashboardIndex(params);
  if (!res.error_status) {
    echartsData.workbench.avg_session_retention.options.xAxis.data = [];
    echartsData.workbench.avg_session_retention.options.series[0].data = [];
    for (const item of res.result.avg_session_retention.avg_session_retention_series) {
      echartsData.workbench.avg_session_retention.options.xAxis.data.push(item.day);
      echartsData.workbench.avg_session_retention.options.series[0].data.push(item.avg_session_count);
    }
    echartsData.workbench.avg_session_retention.options.series[1].data = [];
    for (const item of res.result.avg_session_retention.retention_1) {
      echartsData.workbench.avg_session_retention.options.series[1].data.push(item);
    }
    echartsData.workbench.avg_session_retention.options.series[2].data = [];
    for (const item of res.result.avg_session_retention.retention_7) {
      echartsData.workbench.avg_session_retention.options.series[2].data.push(item);
    }
    echartsData.workbench.avg_session_retention.options.series[3].data = [];
    for (const item of res.result.avg_session_retention.retention_15) {
      echartsData.workbench.avg_session_retention.options.series[3].data.push(item);
    }
    echartsData.workbench.avg_session_retention.options.series[4].data = [];
    for (const item of res.result.avg_session_retention.retention_30) {
      echartsData.workbench.avg_session_retention.options.series[4].data.push(item);
    }
  }
  if (!echartsData.workbench.avg_session_retention.ref && document.getElementById('avg_session_retention')) {
    echartsData.workbench.avg_session_retention.ref = echarts.init(
      document.getElementById('avg_session_retention'),
      null,
      { width: 900, height: 300 }
    );
  }
  echartsData.workbench.avg_session_retention.ref?.setOption(echartsData.workbench.avg_session_retention.options);
}
async function getAllRetention() {
  const params = {
    index_name: 'all_retention',
    begin_time: indexBeginTime.value,
    top: '',
    company_id: targetCompany.value
  };
  const res = await getDashboardIndex(params);
  if (!res.error_status) {
    echartsData.workbench.all_retention.options.xAxis.data = [];
    echartsData.workbench.all_retention.options.series[0].data = [];
    for (const item of res.result.all_retention.active_user_series) {
      echartsData.workbench.all_retention.options.xAxis.data.push(item.day);
      echartsData.workbench.all_retention.options.series[0].data.push(item.active_user_count);
    }
    echartsData.workbench.all_retention.options.series[1].data = [];
    for (const item of res.result.all_retention.retention_7) {
      echartsData.workbench.all_retention.options.series[1].data.push(item);
    }
    echartsData.workbench.all_retention.options.series[2].data = [];
    for (const item of res.result.all_retention.retention_15) {
      echartsData.workbench.all_retention.options.series[2].data.push(item);
    }
    echartsData.workbench.all_retention.options.series[3].data = [];
    for (const item of res.result.all_retention.retention_30) {
      echartsData.workbench.all_retention.options.series[3].data.push(item);
    }
  }
  if (!echartsData.workbench.all_retention.ref && document.getElementById('all_retention')) {
    echartsData.workbench.all_retention.ref = echarts.init(document.getElementById('all_retention'), null, {
      width: 800,
      height: 400
    });
  }
  echartsData.workbench.all_retention.ref?.setOption(echartsData.workbench.all_retention.options);
}
async function getSessionCntData() {
  const params = {
    index_name: 'session',
    begin_time: indexBeginTime.value,
    top: '',
    company_id: targetCompany.value
  };
  const res = await getDashboardIndex(params);
  if (!res.error_status) {
    await gsap.to(sessionCount, { duration: 2, value: res.result.session });
    sessionCount.value = res.result.session;
  }
}
async function getSessionHourData() {
  const params = {
    index_name: 'session_hour',
    begin_time: indexBeginTime.value,
    top: '',
    company_id: targetCompany.value
  };
  const res = await getDashboardIndex(params);
  if (!res.error_status) {
    echartsData.workbench.session_hour.options.xAxis.data = [];
    echartsData.workbench.session_hour.options.series[0].data = [];
    for (const item of res.result.session_hour) {
      echartsData.workbench.session_hour.options.xAxis.data.push(item.hour);
      echartsData.workbench.session_hour.options.series[0].data.push(item.unique_session_count);
    }
    if (!echartsData.workbench.session_hour.ref && document.getElementById('session_hour')) {
      echartsData.workbench.session_hour.ref = echarts.init(document.getElementById('session_hour'), null, {
        width: 500,
        height: 300
      });
    }
    echartsData.workbench.session_hour.ref?.setOption(echartsData.workbench.session_hour.options);
  }
}
async function getSessionDayData() {
  const params = {
    index_name: 'session_day',
    begin_time: indexBeginTime.value,
    top: '',
    company_id: targetCompany.value
  };
  const res = await getDashboardIndex(params);
  if (!res.error_status) {
    echartsData.workbench.session_day.options.xAxis.data = [];
    echartsData.workbench.session_day.options.series[0].data = [];
    for (const item of res.result.session_day) {
      echartsData.workbench.session_day.options.xAxis.data.push(item.day);
      echartsData.workbench.session_day.options.series[0].data.push(item.unique_session_count);
    }
    if (!echartsData.workbench.session_day.ref && document.getElementById('session_day')) {
      echartsData.workbench.session_day.ref = echarts.init(document.getElementById('session_day'), null, {
        width: 500,
        height: 300
      });
    }
    echartsData.workbench.session_day.ref?.setOption(echartsData.workbench.session_day.options);
  }
}

// 资源库
async function getDocReadCountData() {
  const params = {
    index_name: 'doc_read_count',
    begin_time: indexBeginTime.value,
    top: '',
    company_id: targetCompany.value
  };
  const res = await getDashboardIndex(params);
  if (!res.error_status) {
    await gsap.to(docReadCount, { duration: 2, value: res.result.doc_read_count });
    docReadCount.value = res.result.doc_read_count;
  }
}
async function getDocViewTopData() {
  const params = {
    index_name: 'doc_view_top',
    begin_time: indexBeginTime.value,
    top: '',
    company_id: targetCompany.value
  };
  const res = await getDashboardIndex(params);
  if (!res.error_status) {
    echartsData.resource.doc_view_top.options.yAxis.data = [];
    echartsData.resource.doc_view_top.options.series[0].data = [];
    for (const item of res.result.doc_view_top) {
      echartsData.resource.doc_view_top.options.yAxis.data.push(item.resource_name);
      echartsData.resource.doc_view_top.options.series[0].data.push(item.view_count);
    }
    if (!echartsData.resource.doc_view_top.ref && document.getElementById('doc_view_top')) {
      echartsData.resource.doc_view_top.ref = echarts.init(document.getElementById('doc_view_top'), null, {
        width: 500,
        height: 300
      });
    }
    echartsData.resource.doc_view_top.ref?.setOption(echartsData.resource.doc_view_top.options);
  }
}
async function getUserViewTopData() {
  const params = {
    index_name: 'user_view_resource_top',
    begin_time: indexBeginTime.value,
    top: '',
    company_id: targetCompany.value
  };
  const res = await getDashboardIndex(params);
  if (!res.error_status) {
    echartsData.resource.user_view_top.options.yAxis.data = [];
    echartsData.resource.user_view_top.options.series[0].data = [];
    for (const item of res.result.user_view_resource_top) {
      echartsData.resource.user_view_top.options.yAxis.data.push(item.user_id + ':' + item.user_name);
      echartsData.resource.user_view_top.options.series[0].data.push(item.view_count);
    }
    if (!echartsData.resource.user_view_top.ref && document.getElementById('user_view_resource_top')) {
      echartsData.resource.user_view_top.ref = echarts.init(document.getElementById('user_view_resource_top'), null, {
        width: 500,
        height: 300
      });
    }
    echartsData.resource.user_view_top.ref?.setOption(echartsData.resource.user_view_top.options);
  }
}
async function getDocDownloadCountData() {
  const params = {
    index_name: 'doc_download_count',
    begin_time: indexBeginTime.value,
    top: '',
    company_id: targetCompany.value
  };
  const res = await getDashboardIndex(params);
  if (!res.error_status) {
    await gsap.to(docDownloadCount, { duration: 2, value: res.result.doc_download_count });
    docDownloadCount.value = res.result.doc_download_count;
  }
}
async function getDocDownloadTopData() {
  const params = {
    index_name: 'doc_download_top',
    begin_time: indexBeginTime.value,
    top: '',
    company_id: targetCompany.value
  };
  const res = await getDashboardIndex(params);
  if (!res.error_status) {
    echartsData.resource.doc_download_top.options.yAxis.data = [];
    echartsData.resource.doc_download_top.options.series[0].data = [];
    for (const item of res.result.doc_download_top) {
      echartsData.resource.doc_download_top.options.yAxis.data.push(item.resource_name);
      echartsData.resource.doc_download_top.options.series[0].data.push(item.download_count);
    }
    if (!echartsData.resource.doc_download_top.ref && document.getElementById('doc_download_top')) {
      echartsData.resource.doc_download_top.ref = echarts.init(document.getElementById('doc_download_top'), null, {
        width: 500,
        height: 300
      });
    }
    echartsData.resource.doc_download_top.ref?.setOption(echartsData.resource.doc_download_top.options);
  }
}
async function getUserDownloadTopData() {
  const params = {
    index_name: 'user_download_top',
    begin_time: indexBeginTime.value,
    top: '',
    company_id: targetCompany.value
  };
  const res = await getDashboardIndex(params);
  if (!res.error_status) {
    echartsData.resource.user_download_top.options.yAxis.data = [];
    echartsData.resource.user_download_top.options.series[0].data = [];
    for (const item of res.result.user_download_top) {
      echartsData.resource.user_download_top.options.yAxis.data.push(item.user_id + ':' + item.user_name);
      echartsData.resource.user_download_top.options.series[0].data.push(item.download_count);
    }
    if (!echartsData.resource.user_download_top.ref && document.getElementById('user_download_top')) {
      echartsData.resource.user_download_top.ref = echarts.init(document.getElementById('user_download_top'), null, {
        width: 500,
        height: 300
      });
    }
    echartsData.resource.user_download_top.ref?.setOption(echartsData.resource.user_download_top.options);
  }
}
async function handleTabChange(val: string) {
  router.replace({
    query: { tab: val }
  });
  if (val == 'user') {
    getDnu();
    getDnuSd();
    getAllCvr();
    getNewCvr();
    getUvCntData();
    getD1Retention();
    getAllRetention();
  } else if (val == 'workbench') {
    getUvHourData();
    getUvDayData();
    getAvgQaRetention();
    getQaCntData();
    getQaHourData();
    getQaDayData();
    getAvgSessionRetention();
    getSessionCntData();
    getSessionHourData();
    getSessionDayData();
  } else if (val == 'resources') {
    getDocReadCountData();
    getDocViewTopData();
    getUserViewTopData();
    getDocDownloadCountData();
    getDocDownloadTopData();
    getUserDownloadTopData();
  }
}
onMounted(async () => {
  try {
    if (userInfoStore.userInfo.user_role.includes('next_console_admin')) {
      await searchAllCompanyOption();
    }
  } catch (e) {
    console.log(e);
  }
  transTimeRange();
  await handleTabChange(currentTab.value);

  refreshInterval.value = setInterval(async () => {
    await handleTabChange(currentTab.value);
  }, refreshRate.value);
});

onBeforeUnmount(() => {
  if (refreshInterval.value) {
    clearInterval(refreshInterval.value);
  }
});
watch(
  () => props.tab,
  newVal => {
    currentTab.value = newVal;
  },
  {
    immediate: true
  }
);
</script>

<template>
  <el-container style="height: 100vh">
    <el-header>
      <div class="next-console-admin-header">
        <div class="component-box">
          <el-menu :default-active="currentIndex" class="el-menu-demo" mode="horizontal" router :ellipsis="false">
            <el-menu-item
              v-for="component in filteredComponents"
              :key="component.url"
              :index="component.url"
              class="menu-header-item"
            >
              {{ component.name }}
            </el-menu-item>
          </el-menu>
        </div>
      </div>
    </el-header>
    <el-main>
      <div>
        <el-form :inline="true" class="demo-form-inline">
          <el-form-item label="统计时间" style="min-width: 200px">
            <el-select
              v-model="selectedTimeRange"
              placeholder="选择时间范围"
              clearable
              @change="handleTabChange(currentTab)"
            >
              <el-option label="当天" value="today" />
              <el-option label="一周" value="week" />
              <el-option label="一月" value="month" />
              <el-option label="一季度" value="quarter" />
              <el-option label="当年" value="year" />
            </el-select>
          </el-form-item>
          <el-form-item label="刷新频率" style="min-width: 200px">
            <el-select v-model="refreshRate" placeholder="选择刷新频率" @change="changeRefreshRate">
              <el-option label="从不" :value="0" />
              <el-option label="1分钟" :value="60000" />
              <el-option label="5分钟" :value="300000" />
              <el-option label="10分钟" :value="600000" />
            </el-select>
          </el-form-item>
          <el-form-item
            v-if="userInfoStore.userInfo.user_role.includes('next_console_admin')"
            label="公司"
            style="min-width: 200px"
          >
            <el-select
              v-model="targetCompany"
              placeholder="目标公司"
              clearable
              value-key="id"
              @change="handleTabChange(currentTab)"
            >
              <el-option
                v-for="company in userCompanyList"
                :key="company.id"
                :label="company.company_name"
                :value="company.id"
              />
            </el-select>
          </el-form-item>
        </el-form>
      </div>
      <div id="dashboard_area">
        <el-tabs v-model="currentTab" tab-position="left" @tab-change="handleTabChange">
          <el-tab-pane name="user" label="用户数据">
            <el-scrollbar>
              <div class="pane-area">
                <div id="dnu" class="next-console-chart" />
                <div id="dnu_sd" class="next-console-chart" />
                <div id="uv" ref="uv" class="next-console-chart-number">
                  <div class="std-middle-box" style="width: 100%; justify-content: flex-start">
                    <el-text class="chart-number">独立访客数</el-text>
                  </div>
                  <div class="std-middle-box" style="height: 100%">
                    <el-text class="dynamic-number">
                      {{ uvCount.toFixed(0) }}
                    </el-text>
                  </div>
                </div>
                <div id="all_cvr" class="next-console-chart" />
                <div id="new_cvr" class="next-console-chart" />
                <div id="d1_retention" class="next-console-chart" />
                <div id="all_retention" class="next-console-chart" />
              </div>
            </el-scrollbar>
          </el-tab-pane>
          <el-tab-pane name="workbench" label="AI工作台">
            <el-scrollbar>
              <div class="pane-area">
                <div id="uv_hour" class="next-console-chart" />
                <div id="uv_day" class="next-console-chart" />
                <div id="avg_qa_retention" class="next-console-chart" />
                <div id="qa_count" ref="qa" class="next-console-chart-number">
                  <div class="std-middle-box" style="width: 100%; justify-content: flex-start">
                    <el-text class="chart-number">总问答数</el-text>
                  </div>
                  <div class="std-middle-box" style="height: 100%">
                    <el-text class="dynamic-number">
                      {{ qaCount.toFixed(0) }}
                    </el-text>
                  </div>
                </div>
                <div id="qa_hour" class="next-console-chart" />
                <div id="qa_day" class="next-console-chart" />
                <div id="avg_session_retention" class="next-console-chart" />
                <div id="session_count" ref="session" class="next-console-chart-number">
                  <div class="std-middle-box" style="width: 100%; justify-content: flex-start">
                    <el-text class="chart-number">总会话数</el-text>
                  </div>
                  <div class="std-middle-box" style="height: 100%">
                    <el-text class="dynamic-number">
                      {{ sessionCount.toFixed(0) }}
                    </el-text>
                  </div>
                </div>
                <div id="session_hour" class="next-console-chart" />
                <div id="session_day" class="next-console-chart" />
              </div>
            </el-scrollbar>
          </el-tab-pane>
          <el-tab-pane name="resources" label="AI资源库">
            <el-scrollbar>
              <div class="pane-area">
                <div id="doc_view_count" class="next-console-chart-number">
                  <div class="std-middle-box" style="width: 100%; justify-content: flex-start">
                    <el-text class="chart-number">文档查看数量</el-text>
                  </div>
                  <div class="std-middle-box" style="height: 100%">
                    <el-text class="dynamic-number">
                      {{ docReadCount.toFixed(0) }}
                    </el-text>
                  </div>
                </div>
                <div id="doc_view_top" class="next-console-chart" />
                <div id="user_view_resource_top" class="next-console-chart" />
                <div id="doc_download_count" class="next-console-chart-number">
                  <div class="std-middle-box" style="width: 100%; justify-content: flex-start">
                    <el-text class="chart-number">文档下载数量</el-text>
                  </div>
                  <div class="std-middle-box" style="height: 100%">
                    <el-text class="dynamic-number">
                      {{ docDownloadCount.toFixed(0) }}
                    </el-text>
                  </div>
                </div>
                <div id="doc_download_top" class="next-console-chart" />
                <div id="user_download_top" class="next-console-chart" />
              </div>
            </el-scrollbar>
          </el-tab-pane>
        </el-tabs>
      </div>
    </el-main>
    <el-footer />
  </el-container>
</template>

<style scoped>
.el-header {
  padding: 0 !important;
}
.pane-area {
  display: flex;
  flex-direction: row;
  gap: 8px;
  flex-wrap: wrap;
  padding: 8px;
  height: calc(100vh - 240px);
}
.next-console-chart-number {
  border-radius: 12px;
  padding: 24px;
  color: white;
  text-align: center;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
  min-width: 240px;
}
.next-console-chart {
  position: relative;
  display: flex;
  flex-direction: row;
  align-items: center;
  background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  padding: 8px;
  border: 1px solid #e9ecef;
  transition: all 0.3s ease;
}
.next-console-chart:hover {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
  border-color: #007bff;
}
/* 图表标题样式 */
.next-console-chart::before {
  content: attr(data-title);
  position: absolute;
  top: 12px;
  left: 16px;
  font-size: 14px;
  font-weight: 600;
  color: #2c3e50;
  z-index: 2;
}
.next-console-chart.loading {
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: loading 1.5s infinite;
}
@keyframes loading {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}
/* 错误状态 */
.next-console-chart.error {
  border-color: #dc3545;
  background: linear-gradient(135deg, #fff5f5 0%, #ffe6e6 100%);
}

.next-console-chart.error::after {
  content: '数据加载失败';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #dc3545;
  font-size: 14px;
}

/* 空数据状态 */
.next-console-chart.empty {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
}

.next-console-chart.empty::after {
  content: '暂无数据';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #6c757d;
  font-size: 14px;
}

.dynamic-number {
  font-size: 32px;
  font-weight: 700;
  letter-spacing: 1px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}
#dashboard_area {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  width: 100%;
  gap: 12px;
}
.std-middle-box {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
}
.chart-number {
  font-size: 20px;
  font-weight: 600;
  color: black;
}
</style>
