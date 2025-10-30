import { ref } from 'vue';
import { IResourceItem } from '@/types/resource-type';

export const currentPathTree = ref<IResourceItem[]>([]);
