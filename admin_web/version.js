const fs = require('fs');
const path = require('path');

const version = process.env.npm_package_version;
// 获取当前时间戳
const timestamp = new Date().toISOString().replace(/T/, ' ').replace(/\..+/, '');
// 合成版本号和时间戳
const fullVersion = `${version}_(${timestamp})`.slice(0, -7);
const versionFile = path.join(__dirname, 'public/version.json');
fs.writeFileSync(versionFile, JSON.stringify({ version: fullVersion }, null, 2));

