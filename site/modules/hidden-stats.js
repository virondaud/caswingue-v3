// Agrégation des stats cachées (FIR / GIR / putts) par joueur et par partie.
// Stockage : IndexedDB store `holeStats`, clé = `${gameId}_${hole}_${pi}`.

import { DB } from './idb-wrapper.js';

/**
 * @typedef {Object} HoleStats
 * @property {boolean|null} fir  null si N/A (par 3), sinon true/false
 * @property {boolean} gir
 * @property {number} putts
 * @property {string} [notes]
 */

/** @param {string} gameId @param {number} hole @param {number} pi */
export function statKey(gameId, hole, pi) {
  return `${gameId}_${hole}_${pi}`;
}

/** @param {string} gameId @param {number} hole @param {number} pi @param {HoleStats} stats */
export function saveHoleStats(gameId, hole, pi, stats) {
  return DB.put('holeStats', stats, statKey(gameId, hole, pi));
}

/** @param {string} gameId @param {number} hole @param {number} pi */
export function getHoleStats(gameId, hole, pi) {
  return DB.get('holeStats', statKey(gameId, hole, pi));
}

/**
 * Agrège toutes les stats d'une partie pour un joueur.
 * @param {string} gameId @param {number} pi
 * @param {number} [nHoles]
 * @returns {Promise<{firs: number, firsPossible: number, firPct: number,
 *   girs: number, girsPossible: number, girPct: number,
 *   totalPutts: number, avgPutts: number, holesWithData: number}>}
 */
export async function aggregateForGame(gameId, pi, nHoles = 18) {
  const out = {
    firs: 0, firsPossible: 0, firPct: 0,
    girs: 0, girsPossible: 0, girPct: 0,
    totalPutts: 0, avgPutts: 0, holesWithData: 0,
  };
  for (let h = 0; h < nHoles; h++) {
    const s = await getHoleStats(gameId, h, pi);
    if (!s) continue;
    out.holesWithData++;
    if (s.fir !== null && s.fir !== undefined) {
      out.firsPossible++;
      if (s.fir) out.firs++;
    }
    out.girsPossible++;
    if (s.gir) out.girs++;
    if (typeof s.putts === 'number') out.totalPutts += s.putts;
  }
  out.firPct = out.firsPossible > 0 ? Math.round((out.firs / out.firsPossible) * 100) : 0;
  out.girPct = out.girsPossible > 0 ? Math.round((out.girs / out.girsPossible) * 100) : 0;
  out.avgPutts = out.holesWithData > 0
    ? Math.round((out.totalPutts / out.holesWithData) * 10) / 10
    : 0;
  return out;
}

/**
 * Détection automatique du GIR à partir du score et du par.
 * Si score <= par - 2, GIR est obligatoire.
 * @param {number} score @param {number} par
 * @returns {boolean|null} true si GIR certain, null sinon (l'utilisateur doit choisir)
 */
export function autoGIR(score, par) {
  if (!score || !par) return null;
  const d = score - par;
  if (d <= -2) return true; // eagle ou mieux = GIR + birdie = GIR presque certain
  return null;
}
