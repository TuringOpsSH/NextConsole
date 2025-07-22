import { ref } from 'vue';
import { versionGet } from '@/api/base';

export const currentVersion = ref(null);

export function getCurrentTimestamp() {
    const date = new Date();

    const year = date.getFullYear();

    const month = (date.getMonth() + 1).toString().padStart(2, '0');

    const day = date.getDate().toString().padStart(2, '0');

    const hour = date.getHours().toString().padStart(2, '0');

    const minute = date.getMinutes().toString().padStart(2, '0');

    const second = date.getSeconds().toString().padStart(2, '0');

    return year + '-' + month + '-' + day + ' ' + hour + ':' + minute + ':' + second;
}

export async function getVersion() {
    try {
        const res = await versionGet();
        currentVersion.value = res.result.version;
    } catch (error) {
        console.error('无法获取版本信息', error);
    }
}

export async function checkVersion() {
    try {
        const res = await versionGet();
        if (res.result.version && currentVersion.value && res.result.version !== currentVersion.value) {
            window.location.reload();
        }
    } catch (error) {
        console.error('无法获取版本信息', error);
    }
}
