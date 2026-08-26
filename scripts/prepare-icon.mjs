import fs from 'node:fs';
import path from 'node:path';
import sharp from 'sharp';

const root = process.cwd();
const input = path.join(root, 'assets', 'icon.svg');
const output = path.join(root, 'assets', 'icon.png');

if (!fs.existsSync(input)) throw new Error(`Missing ${input}`);
await sharp(input).resize(1024, 1024).png().toFile(output);
console.log(`Generated ${output}`);
