import { useSessionStorage } from '@vueuse/core';
import { SessionStorageKeys } from '@/utils/sessionStorageKeys';

type TKeyType = keyof typeof SessionStorageKeys;

export function useManagedSessionStorage<T>(key: TKeyType, defaultValue: T) {
  // 将 Symbol 转换为字符串用于实际存储（Symbol.description 获取描述文本）
  const storageKey = SessionStorageKeys[key].description!;
  return useSessionStorage<T>(storageKey, defaultValue);
}
