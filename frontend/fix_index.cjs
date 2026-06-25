const fs = require('fs');
const htmlContent = '<!DOCTYPE html>\n' +
'<html lang="zh-CN">\n' +
'<head>\n' +
'  <meta charset="UTF-8">\n' +
'  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n' +
'  <title>Marketing Wind Tunnel Platform</title>\n' +
'</head>\n' +
'<body>\n' +
'  <div id="app"></div>\n' +
'  <script type="module" src="/src/main.js"></script>\n' +
'</body>\n' +
'</html>';
fs.writeFileSync('index.html', htmlContent, { encoding: 'utf8' });
console.log('index.html created successfully');