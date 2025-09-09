import type { TabsPaneContext } from 'element-plus';
import { ref } from 'vue';
import { llmInstanceSearch } from '@/api/config-center';
import router from '@/router';
export const currentPage = ref('llm');
export const CurrentLLMList = ref([]);
export const LLMPageSize = ref(10);
export const LLMPageNum = ref(1);
export const LLMListLoading = ref(false);
export const LLMKeyword = ref('');
export const LLMTotal = ref(0);
export const CurrentLLM = ref({});
export const LLMStatus = ref([]);
export const LLMTypes = ref([]);

export const CurrentSupplierList = ref([]);
export const SupplierPageSize = ref(10);
export const CurrentSupplier = ref({});
export const SupplierTotal = ref(0);
export const SupplierPageNum = ref(1);
export const SupplierListLoading = ref(false);
export const SupplierKeyword = ref('');

export async function SearchLLMList() {
  LLMListLoading.value = true;
  const searchRes = await llmInstanceSearch({});
  if (!searchRes.error_status) {
    CurrentLLMList.value = searchRes.result.data;
    LLMTotal.value = searchRes.result.total;
  }
  LLMListLoading.value = false;
}

export async function SearchSupplierList() {
  SupplierListLoading.value = true;
}

export async function enterLLMDetail() {}

export async function handleTabClick(tab: TabsPaneContext) {
  console.log(tab.paneName);
  if (tab.paneName === 'llm') {
    SearchLLMList();
    router.replace({
      query: {
        ...router.currentRoute.value.query,
        page_num: LLMPageNum.value,
        page_size: LLMPageSize.value
      }
    });
  } else {
    SearchSupplierList();
  }
}
