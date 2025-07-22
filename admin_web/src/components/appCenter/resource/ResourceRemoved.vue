<script setup lang="ts">
import { ElMessageBox } from 'element-plus';
import { onMounted } from 'vue';
onMounted(() => {
  console.log('🚀 mounted');
  setTimeout(() => {
    ElMessageBox.alert('该功能已下架', '提示', {
      confirmButtonText: '确认',
      callback: () => {
        history.go(-2);
      }
    });
  }, 100);
});
</script>

<style lang="scss" scoped>
.resource-removed {
  height: 100vh;
  background-color: #fff;
}
</style>
