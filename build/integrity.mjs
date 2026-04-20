// Génère integrity.json avec les hashs SHA-256 des fichiers critiques.
// Chargé par l'app au démarrage pour vérifier l'intégrité du déploiement.

import { createHash } from 'node:crypto';
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');

const targets = [
  'site/golf_manager.html',
  'site/index.html',
  'site/dist/v3-modules.js',
];

function sha256(filepath) {
  const abs = path.join(ROOT, filepath);
  if (!existsSync(abs)) return null;
  const buf = readFileSync(abs);
  return createHash('sha256').update(buf).digest('hex');
}

const integrity = {
  generatedAt: new Date().toISOString(),
  version: '3.0.0-alpha.1',
  files: {},
};

for (const t of targets) {
  const h = sha256(t);
  if (h) integrity.files[t] = h;
}

const outputPath = path.join(ROOT, 'site/integrity.json');
writeFileSync(outputPath, JSON.stringify(integrity, null, 2));

console.log('\n🔐 integrity.json généré :');
Object.entries(integrity.files).forEach(([f, h]) => {
  console.log(`  ${f.padEnd(40)} ${h.slice(0, 16)}…`);
});
