; (function (input) {
    var okResult = {
        desc: "sda分区表类型检查",
        effect: "MBR分区表不支持容量大于2.2TB的分区, 使用GPT分区表须主板类型为UEFI",
        solution: "主板类型(MBR/UEFI)与sda分区格式配置一致(MSDOS/GPT)",
        level: "正常",
        id: "linux.partition",
        name: "sda分区表类型检查",
        category: "系统健康检查",
        actual: "",
        expected: "主板类型(MBR/UEFI)与sda分区格式一致(MSDOS/GPT)",
    }

    var errResult = {
        desc: "sda分区表类型检查",
        effect: "MBR分区表不支持容量大于2.2TB的分区, 使用GPT分区表须主板类型为UEFI",
        solution: "主板类型(MBR/UEFI)与sda分区格式配置一致(MSDOS/GPT)",
        level: "中风险",
        id: "linux.partition",
        name: "sda分区表类型检查",
        category: "系统健康检查",
        actual: "",
        expected: "主板类型(MBR/UEFI)与sda分区表类型一致(MSDOS/GPT)",
    }

    if (!input) {
        return { results: [errResult] }
    }

    // 主板mbr格式 sda分区 mbr格式(msdos)
    // 主板uefi格式 sda分区gpt格式(gpt) df -h 存在/boot/efi 

    ismsdos = false
    hasbootefi = false

    for (i = 0; i < input.length; i++) {
        if (input[i].match("Partition Table: msdos")) {
            ismsdos = true
        } else if (input[i].match("/boot/efi")) {
            hasbootefi = true
        }
    }

    isok = true
    if (ismsdos) {
        if (hasbootefi) {
            errResult.actual = "主板类型(MBR/UEFI)与sda分区表类型不一致(MSDOS/GPT)"
            isok = false
        }
    } else {
        if (!hasbootefi) {
            errResult.actual = "主板类型(MBR/UEFI)与sda分区表类型不一致(MSDOS/GPT)"
            isok = false
        }
    }

    if (isok) {
        return { results: [okResult] }
    } else {
        return { results: [errResult] }
    }


})(input)
