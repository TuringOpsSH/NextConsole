import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useResourceListStore = defineStore('resourceList', () => {
  const isSearchMode = ref(false);
  const resourceId = ref('');
  const isLoading = ref(true);
  return { isSearchMode, resourceId, isLoading };
});
