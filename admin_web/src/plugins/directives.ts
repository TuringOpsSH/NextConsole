import type { App } from 'vue';

export default {
  install(app: App) {
    // 监听元素大小变化
    app.directive('resize', {
      mounted(el, binding) {
        const observer = new ResizeObserver(entries => {
          binding.value(entries[0].contentRect);
        });
        observer.observe(el);
        el._resizeObserver = observer; // 存储 observer 以便销毁
      },
      unmounted(el) {
        el._resizeObserver?.disconnect();
      }
    });
  }
};
