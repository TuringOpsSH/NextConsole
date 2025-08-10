import {fileURLToPath, URL} from 'node:url'

import {defineConfig} from 'vite'
import vue from '@vitejs/plugin-vue'
import {viteCommonjs} from '@originjs/vite-plugin-commonjs'

// 获取环境变量
const isLocalhost = process.env.NODE_ENV === 'localhost2';
// 根据环境变量设置代理目标地址
let proxyTarget = isLocalhost ? 'http://127.0.0.1:5123' : 'http://116.62.30.184:6688';

if (process.env.NODE_ENV === 'production') {
  proxyTarget = 'https://www.turingops.com.cn';
  console.log('proxyTarget: ', proxyTarget);
}


export default defineConfig({
  plugins: [
    vue(),viteCommonjs()
  ],
  optimizeDeps: {
    include: ['pdfjs-dist/legacy/build/pdf'],
  },
  publicDir: 'public', //
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    port: 8080,
    proxy: {
      '/dev': {
        target: proxyTarget,
        ws: true, // 代理 websocked
        changeOrigin: true, // 虚拟的站点需要更管origin
        rewrite: (path) => path.replace(/^\/dev/, ''), // 重写路径
        secure: true, // 是否https接口
      },
      '/next_console': {
        target: proxyTarget,
        ws: true, // 代理 websocked
        changeOrigin: true, // 虚拟的站点需要更管origin
        secure: true, // 是否https接口
      },
      '/next_search': {
        target: proxyTarget,
        ws: true, // 代理 websocked
        changeOrigin: true, // 虚拟的站点需要更管origin
        secure: true, // 是否https接口
      },
      '/web_socket': {
        target: proxyTarget,
        ws: true, // 代理 websocked
        changeOrigin: true, // 虚拟的站点需要更管origin
        rewrite: (path) => path.replace(/^\/web_socket/, ''), // 重写路径
        secure: true, // 是否https接口
      },
      '/downloads': {
        target: proxyTarget,
        changeOrigin: true, // 虚拟的站点需要更管origin
        // rewrite: (path) => path.replace(/^\/web_socket/, ''), // 重写路径
        secure: true, // 是否https接口
      }
    },
  },
  base: process.env.VITE_APP_PUBLIC_PATH,
  configureWebpack: {
    optimization: {
      splitChunks: {
        chunks: 'all'
      }
    }
  }
})
