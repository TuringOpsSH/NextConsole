<script setup lang="ts">
import {onBeforeMount} from "vue-demi";
import {onMounted, ref} from "vue";
// const iframeUrl = ref('https://www.turingops.com.cn/#/app_center/agent_app/whzy')
const iframeUrl = ref('http://localhost:5173/#/app_center/agent_app/whzy')
onBeforeMount(() => {
  console.log('mounted')
  // const token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0Njc1MjY4OSwianRpIjoiNTQzNmNmYmUtN2ZmNC00ZWQ4LWI4N2EtMWNjYTJjNWJiZjljIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjI1NiIsIm5iZiI6MTc0Njc1MjY4OSwiY3NyZiI6IjlkMWIwOGY4LTBiZjMtNDY1My04YTk5LTU2YWQ1ZWU3M2IyOSIsImV4cCI6MTc0OTM0NDY4OSwidXNlcl9pZCI6MjU2LCJyb2xlX25hbWUiOlsic3VwZXJfYWRtaW4iLCJhZG1pbiIsInVzZXIiLCJuZXh0X2NvbnNvbGVfYWRtaW4iLCJuZXh0X2NvbnNvbGVfcmVhZGVyX2FkbWluIl0sInVzZXJfY29kZSI6IjA1NjNiMTlmLWE1NDctNGU2Yy05M2ZlLTgwNGRkNGE1YjVmMiJ9.jHg8d4I3jEXVB2uKaMUEuQO5CzUL6VjsIdqOa-Q1YTY'
  const token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0Njc1NDMwMSwianRpIjoiNmQ2OTY1MjctZjJkOC00ZDA5LWE3OWYtZTVhNjczZWZlYmIyIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjE2NzgiLCJuYmYiOjE3NDY3NTQzMDEsImNzcmYiOiIwN2QwNTNjYy02ZDE5LTRiMWUtYTI2ZC02YzhmYmRjYjg0ODYiLCJleHAiOjE3NDkzNDYzMDEsInVzZXJfaWQiOjE2NzgsInJvbGVfbmFtZSI6WyJ1c2VyIl0sInVzZXJfY29kZSI6ImExNWM0NmE5LWIzMTgtNGE2Yi05ZDNiLTEyYzFmZDY4MDAwMyJ9.aaVmxNGuzEdC-EpL7xa41PONBWe4nz9Tvwuj32_5irc'
  // const token = ''
  const session_code = ''
  if (session_code){
    iframeUrl.value += '/' + session_code
  }
  if (token){
    iframeUrl.value += '?token=' + token
  }
})


onMounted(() => {
  console.log(iframeUrl.value)
  // 向主页面发送消息
  // 获取 iframe 元素
  const iframe = document.getElementById('next-console');

  // 向 iframe 发送消息

  // 监听来自 iframe 的消息
  window.addEventListener('message', (event) => {
    console.log('Received from iframe:', event.data);
  });

  // 5 秒后向 iframe 发送一条消息
  // setTimeout(sendMessageToIframe, 5000);
  // sendMessageToIframe()
  function sendMessageToIframe() {
    const message = {
      type: 'echo',
      data: {
        type: 'updateWeekGraph',
        data: {
          startDate: '',
          endDate: '',
          spec: '',
          chartOption: {
            legend: {
              data: ['建议零售价', '出货价', '进货价', '批发价'],
              itemGap: 30, // 图例项间隔

              textStyle: {
                fontSize: 12 // 字体大小
              },
              orient: 'horizontal' // 水平排列
            },
            backgroundColor: 'transparent',
            tooltip: {
              trigger: 'axis',
              axisPointer: {
                type: 'none'
              }
            },
            xAxis: {
              type: 'category',
              data: [],
              axisLine: {
                show: false // 不显示 x 轴线
              }
            },
            yAxis: {
              min: 0, // 设置 y 轴最小值
              max: 1000, // 设置 y 轴最大值,
              type: 'value',
              axisLine: {
                show: false // 不显示 x 轴线
              },
              splitLine: {
                show: true,
                lineStyle: {
                  type: 'solid',
                  color: '#FFFFFF19'
                }
              }
            },
            series: [
              {
                name: '批发价', // 为基准线创建一个单独的 series
                type: 'line',
                data: [], // 不需要实际数据
                markLine: {
                  data: [
                    {
                      name: '基准线',
                      // data: data.wholesaleArr,
                      yAxis: 1000, // 水平基准线的值
                      lineStyle: {
                        width: 3, // 加粗基准线
                        color: 'red', // 基准线颜色
                        type: 'dashed' // 虚线样式
                      }
                    }
                  ]
                }
              },
              {
                name: '建议零售价',
                type: 'line',
                data: [],
                itemStyle: {
                  color: '#FCB059FF'
                },
                areaStyle: {
                  color: ''
                }
              },
              {
                name: '出货价',
                type: 'bar',
                data: [],
                itemStyle: {
                  color: ''
                }
              },
              {
                name: '进货价',
                type: 'bar',
                data: [],
                itemStyle: {
                  color: ''
                }
              }
            ]
          }
        }
      }};
    iframe.contentWindow.postMessage(message, '*'); // '*' 表示不限制目标域名
  }
  iframe.onload = () => {
    console.log('iframe loaded')
    sendMessageToIframe()
  }
  setInterval(() => {
    iframe.contentWindow.postMessage({
      type: 'question',
      data: [
        {
          content: '2022年10月31号到11月6号武汉市平均进货价黄鹤楼相关规格与上期对比情况，用柱状图对比表示'
        }
      ]
    }, '*');
  }, 50000)
})
</script>

<template>
  <el-container style="background-color: #999999">
    <el-aside width="30vw">
    </el-aside>
    <el-main>
      <div style="height: 100vh; width: 60vw;">
        <iframe :src="iframeUrl" id="next-console" style="width: 80%; height: calc(100vh - 40px);
        background: transparent; border: none; "
                allow="microphone"
                allowtransparency="true" />
      </div>
    </el-main>

  </el-container>

</template>

<style scoped>

</style>
