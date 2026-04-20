// Build esbuild minimal pour Ça Swingue v3
// Bundle le code ES modules de site/modules/ en un seul fichier chargeable
// depuis golf_manager.html via <script type="module">.

import * as esbuild from 'esbuild';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');

const config = {
  entryPoints: [path.join(ROOT, 'site/modules/index.js')],
  bundle: true,
  format: 'esm',
  target: 'es2022',
  minify: true,
  sourcemap: true,
  outfile: path.join(ROOT, 'site/dist/v3-modules.js'),
  logLevel: 'info',
  metafile: true,
};

const result = await esbuild.build(config);
const sizes = Object.entries(result.metafile.outputs).map(([file, info]) => {
  const kb = (info.bytes / 1024).toFixed(1);
  return `  ${path.basename(file).padEnd(30)} ${kb} KB`;
});

console.log('\n✅ Bundle v3 construit :');
console.log(sizes.join('\n'));
