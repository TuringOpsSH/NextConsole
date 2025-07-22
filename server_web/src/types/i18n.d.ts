import { TLangTypes } from '@/locales/zh';

export type TObjKeysToUnion<T, P extends string = ''> = T extends object
  ? { [K in keyof T]: TObjKeysToUnion<T[K], P extends '' ? K : `${P}.${K}`> }[keyof T]
  : P;

// 声明全局类型
declare module 'vue' {
  // eslint-disable-next-line @typescript-eslint/naming-convention
  interface ComponentCustomProperties {
    $t(key: TObjKeysToUnion<TLangTypes>): string;
  }
}
