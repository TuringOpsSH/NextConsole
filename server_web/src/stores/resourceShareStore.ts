import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useShareResourceStore = defineStore('resourceShare', () => {
  const isSearchMode = ref(false);
  const isLoading = ref(true);
  return { isSearchMode, isLoading };
});
