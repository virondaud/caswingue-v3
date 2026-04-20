// Point d'entrée des modules v3.
// Expose les fonctions au monolithe golf_manager.html via window.V3.

import * as idb from './idb-wrapper.js';
import * as geo from './geo.js';
import * as hiddenStats from './hidden-stats.js';
import * as equipment from './equipment-wear.js';
import * as staticMap from './static-map.js';
import { verifyIntegrity } from './integrity-check.js';

/** @type {any} */
const globalAny = typeof window !== 'undefined' ? window : globalThis;

globalAny.V3 = {
  idb,
  geo,
  hiddenStats,
  equipment,
  staticMap,
  verifyIntegrity,
  version: '3.0.0-alpha.1',
};

// Vérifie l'intégrité en arrière-plan (non bloquant)
queueMicrotask(() => {
  verifyIntegrity().catch((err) => {
    console.warn('[V3] integrity check failed:', err?.message || err);
  });
});

console.log('%c⛳ Ça Swingue v3 modules chargés', 'color:#16a34a;font-weight:bold');
