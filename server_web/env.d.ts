declare module '*.vue' {
  import { DefineComponent } from 'vue';
  const component: DefineComponent<{}, {}, any>;
  export default component;
}
declare module '*.ts' {}

// vite-env.d.ts
interface ImportMetaEnv {
  readonly NODE_ENV: string;
  readonly VITE_APP_PUBLIC_PATH: string;
  readonly VITE_APP_CORP_ID: string;
  readonly VITE_APP_AGENT_ID: string;
  readonly VITE_APP_WEBSOCKET_URL: string;
  readonly VITE_APP_WPS_APP_ID: string;
  readonly VITE_APP_NEXT_CONSOLE_PATH: string;
  readonly VITE_APP_NODE_ENV: string;
  readonly VITE_APP_NEXT_CONSOLE_URL: string;
  // 在此处添加更多的环境变量定义
  // readonly YOUR_ENV_VARIABLE: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
