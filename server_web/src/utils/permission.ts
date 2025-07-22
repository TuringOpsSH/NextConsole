export function checkPermission(userRoles: string[], componentRoles: string[]): boolean {
    if (!componentRoles || componentRoles.length === 0) {
        return true;
    }
    try {
        return userRoles.some(role => componentRoles.includes(role));
    } catch (e) {
        return false;
    }

}

