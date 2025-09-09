import {fileURLToPath, URL} from 'node:url'
import {defineConfig} from 'vite'
import vue from '@vitejs/plugin-vue'
import {viteCommonjs} from '@originjs/vite-plugin-commonjs'
import { createSvgIconsPlugin } from 'vite-plugin-svg-icons';
import path from "path";
// 获取环境变量
const isLocalhost = process.env.NODE_ENV === 'localhost2' || process.env.NODE_ENV === 'private';

// 根据环境变量设置代理目标地址
let proxyTarget = isLocalhost ? 'http://127.0.0.1:5011' : 'https://dev-admin.turingops.com.cn';

if (process.env.NODE_ENV === 'production') {
  proxyTarget = 'https://admin.turingops.com.cn';
}

export default defineConfig({
  plugins: [
    vue(),viteCommonjs(),
    createSvgIconsPlugin({
      // 指定 SVG 图标目录（绝对路径）
      iconDirs: [path.resolve(process.cwd(), 'src/assets/icons')],
      // 指定 symbolId 格式（可选）
      symbolId: 'icon-[dir]-[name]'
    })
  ],
  publicDir: 'public', //
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    port: 8082,
    proxy: {
      '/next_console_admin': {
        target: proxyTarget, // 这里填入你要请求的接口的前缀
        ws: true, // 代理 websocked
        changeOrigin: true, // 虚拟的站点需要更管origin
        secure: true, // 是否https接口
      },
      '/web_socket': {
        target: proxyTarget,
        ws: true, // 代理 websocked
        changeOrigin: true, // 虚拟的站点需要更管origin
        rewrite: path => path.replace(/^\/web_socket/, ''), // 重写路径
        secure: true // 是否https接口
      },
    },
  },
  base: process.env.VITE_APP_PUBLIC_PATH,
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    sourcemap: false,

    // Rollup 配置（替代 configureWebpack）
    rollupOptions: {
      output: {
        // 代码分割优化
        chunkFileNames: 'assets/js/[name]-[hash].js',
        entryFileNames: 'assets/js/[name]-[hash].js',
        assetFileNames: 'assets/[ext]/[name]-[hash].[ext]',

        // 手动代码分割
        manualChunks: {
          'vue-vendor': ['vue', 'vue-router', 'pinia'],
          'pdf-utils': ['pdfjs-dist'],
          // 根据实际依赖添加
        }
      }
    },

    // 构建大小警告
    chunkSizeWarningLimit: 1000,

    // 压缩配置
    minify: true,
    terserOptions:  {
      compress: {
        drop_console: true, // 生产环境移除 console
        drop_debugger: true
      }
    }
  },
})
