const fs = require('fs');
const viewsDir = './frontend/src/views';
if (!fs.existsSync(viewsDir)) fs.mkdirSync(viewsDir, { recursive: true });
