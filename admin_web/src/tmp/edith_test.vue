<script setup lang="ts">
import {onMounted, ref} from 'vue';
const target_url = ref('https://www.baidu.com');
onMounted(()=>{
  target_url.value = 'http://127.0.0.1:5173/#/next_console/home/next_console';
  let token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxMDkwMjU5MiwianRpIjoiY2JhYWMxMTctZmQxOS00MmM5LTk3NmYtZWQ1MWE1NWU3Mzk5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MzAzLCJuYmYiOjE3MTA5MDI1OTIsImV4cCI6MTcxMzQ5NDU5MiwidXNlcl9pZCI6MzAzLCJyb2xlX25hbWUiOlsidXNlciJdLCJ1c2VyX2NvZGUiOiI4MTVhZWM1MDEyYTFhNjVjOGQyNzcwMjNlYzNkNjVmYjNlZTNkMWMwMDc3ZjE5Yzc3NDM0YTU4ZmFkNjc1N2ExIn0.7sACFiffEwSWVjoiYk80H_KKMvd7QGvIgecu11hbWUA"
  target_url.value += '?authToken=' + token;
})

</script>

<template>
<div class="main">
  <div class="left">
    <el-text> 左边的内容</el-text>
  </div>
  <div class="right">

    <iframe :src="target_url" class="my-iframe"></iframe>
  </div>
</div>
</template>

<style scoped>
.main{
  width: 100vw;
  height: 100vh;
  display: flex;
  flex-direction: row;
}
.left{
  width: 50%;
  height: 100%;
  background-color: #f0f0f0;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 20px;
  color: #333;
  font-weight: bold;
  border-right: 1px solid #ccc;
}
.right{
  width: 50%;
  height: 100%;
  background-color: #f0f0f0;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 20px;
  color: #333;
  font-weight: bold;
}
.my-iframe{
  width: 100%;
  height: 100%;
  border: none;
}
</style>
