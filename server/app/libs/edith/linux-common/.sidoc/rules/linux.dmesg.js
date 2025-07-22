;(function(input) {
	var results = []
	if (!input) {
		return {
			results: results
		}
	}
	var ok = true
	for (i = 0; i < input.length; i++) {
		if (input[i].match("No NUMA configuration found")) {
			ok = false
		}
	}

	if (ok) {
		results.push({
			desc: "",
			solution: "开启 NUMA",
			level: "正常",
			effect: "无影响",
			id: "linux.numastat",
			name: "是否开启 NUMA 检查",
			category: "系统健康检查",
			actual: "已开启",
			expected: "开启NUMA"
		})
	} else {
		results.push({
			desc: "",
			effect: "无影响",
			solution: "开启 NUMA",
			level: "中风险",
			id: "linux.numastat",
			name: "是否开启 NUMA 检查",
			category: "系统健康检查",
			actual: "未开启 NUMA",
			expected: "开启 NUMA"
		})
	}
	return {
		results: results
	}
})(input)
