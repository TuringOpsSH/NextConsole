import {fileURLToPath, URL} from 'node:url'
import {defineConfig} from 'vite'
import vue from '@vitejs/plugin-vue'
import {viteCommonjs} from '@originjs/vite-plugin-commonjs'
import { createSvgIconsPlugin } from 'vite-plugin-svg-icons';
import path from "path";
// 获取环境变量
const isLocalhost = process.env.NODE_ENV === 'localhost2';

// 根据环境变量设置代理目标地址
const proxyTarget = isLocalhost ? 'http://127.0.0.1:5011' : 'https://dev-admin.turingops.com.cn';
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
  configureWebpack: {
    optimization: {
      splitChunks: {
        chunks: 'all'
      }
    }
  }
})
