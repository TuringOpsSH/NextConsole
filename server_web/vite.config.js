import {fileURLToPath, URL} from 'node:url'

import {defineConfig} from 'vite'
import vue from '@vitejs/plugin-vue'
import {viteCommonjs} from '@originjs/vite-plugin-commonjs'

// 获取环境变量
const isLocalhost = process.env.NODE_ENV === 'localhost2';
// 根据环境变量设置代理目标地址
const proxyTarget = isLocalhost ? 'http://127.0.0.1:5000' : 'http://116.62.30.184:6688';

export default defineConfig({
  plugins: [
    vue(),viteCommonjs()
  ],
  publicDir: 'public', //
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    proxy: {
      '/dev': {
        // target: 'http://127.0.0.1:5000', // 这里填入你要请求的接口的前缀
        // target: 'http://116.62.30.184:6688', // 这里填入你要请求的接口的前缀
        target: proxyTarget,
        ws: true, // 代理 websocked
        changeOrigin: true, // 虚拟的站点需要更管origin
        rewrite: (path) => path.replace(/^\/dev/, ''), // 重写路径
        secure: true, // 是否https接口
      },
      '/next_console': {
        // target: 'http://116.62.30.184:6688', // 这里填入你要请求的接口的前缀
        target: proxyTarget,
        ws: true, // 代理 websocked
        changeOrigin: true, // 虚拟的站点需要更管origin
        secure: true, // 是否https接口
      },
      '/next_search': {
        // target: 'http://116.62.30.184:6688', // 这里填入你要请求的接口的前缀
        target: proxyTarget,
        ws: true, // 代理 websocked
        changeOrigin: true, // 虚拟的站点需要更管origin
        secure: true, // 是否https接口
      },
      '/web_socket': {
        // target: 'http://116.62.30.184:6688', // 这里填入你要请求的接口的前缀
        target: proxyTarget,
        ws: true, // 代理 websocked
        changeOrigin: true, // 虚拟的站点需要更管origin
        rewrite: (path) => path.replace(/^\/web_socket/, ''), // 重写路径
        secure: true, // 是否https接口
      },
      '/downloads': {
        // target: 'http://116.62.30.184:6688', // 这里填入你要请求的接口的前缀
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
