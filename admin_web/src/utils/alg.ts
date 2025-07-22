import pinyin from "pinyin";

export function handleUserName (input: string, n:number){
    if (!input) return "";
    const firstNChar = input.substring(0, n);
    const reg = new RegExp("[\u4e00-\u9fa5]+","g");


    let res = '';

    for (let i = 0; i < firstNChar.length; i++) {

        if (firstNChar.charAt(i).match(reg)) {
            const py = pinyin(firstNChar.charAt(i), {
                style: pinyin.STYLE_FIRST_LETTER,
                heteronym: false
            });
            res += py.join('').toUpperCase();
        }
        else {

            res += firstNChar.charAt(i).toUpperCase();
        }
    }
    return res;
}
