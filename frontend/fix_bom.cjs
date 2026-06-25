const fs = require('fs');
const path = require('path');

const filesToFix = [
  'src/router/index.js',
  'src/main.js',
  'src/store/index.js',
  'src/api/index.js'
];

filesToFix.forEach(filePath => {
  try {
    const content = fs.readFileSync(filePath, { encoding: 'utf8' });
    const bom = content.charCodeAt(0) === 0xFEFF;
    if (bom) {
      const cleanContent = content.slice(1);
      fs.writeFileSync(filePath, cleanContent, { encoding: 'utf8' });
      console.log(`Fixed BOM in: ${filePath}`);
    } else {
      console.log(`No BOM in: ${filePath}`);
    }
  } catch (err) {
    console.error(`Error processing ${filePath}:`, err.message);
  }
});

console.log('BOM fix completed');