// Suivi d'usure du matériel.
// Stockage IndexedDB `equipment`, clé = `${playerId}_${itemId}`.

import { DB } from './idb-wrapper.js';

/**
 * @typedef {'balls'|'gloves'|'tees'|'grips'|'spikes'|'bag'|'rangefinder'} ItemType
 * @typedef {Object} EquipmentItem
 * @property {string} id
 * @property {ItemType} type
 * @property {string} brand
 * @property {string} model
 * @property {number} addedAt       Date d'achat (ms)
 * @property {number} gamesCount   Nb de parties jouées avec
 * @property {number} holesCount   Nb de trous joués avec
 * @property {number} [replacedAt] Date de remplacement éventuel
 */

/** Seuils par défaut pour alertes */
export const DEFAULT_THRESHOLDS = {
  balls: { games: 3, holes: 54 },
  gloves: { games: 20 },
  tees: { games: 30 },
  grips: { games: 150 },
  spikes: { games: 60 },
  bag: { games: 500 },
  rangefinder: { games: 300 },
};

/** @param {string} playerId @param {string} itemId */
function key(playerId, itemId) { return `${playerId}_${itemId}`; }

/** @param {string} playerId @param {EquipmentItem} item */
export async function addItem(playerId, item) {
  await DB.put('equipment', item, key(playerId, item.id));
  return item;
}

/** @param {string} playerId @param {string} itemId */
export function getItem(playerId, itemId) {
  return DB.get('equipment', key(playerId, itemId));
}

/** @param {string} playerId */
export async function listItems(playerId) {
  const keys = await DB.keysWithPrefix('equipment', playerId + '_');
  const items = [];
  for (const k of keys) {
    const v = await DB.get('equipment', k);
    if (v) items.push(v);
  }
  return items;
}

/**
 * À appeler à la fin d'une partie pour incrémenter les compteurs
 * de tous les items actifs du joueur.
 * @param {string} playerId @param {number} holesPlayed
 */
export async function bumpAfterGame(playerId, holesPlayed = 18) {
  const items = await listItems(playerId);
  for (const item of items) {
    if (item.replacedAt) continue;
    item.gamesCount = (item.gamesCount || 0) + 1;
    item.holesCount = (item.holesCount || 0) + holesPlayed;
    await DB.put('equipment', item, key(playerId, item.id));
  }
}

/**
 * Retourne les items qui dépassent leur seuil d'usure.
 * @param {string} playerId
 * @returns {Promise<Array<{item: EquipmentItem, reason: string}>>}
 */
export async function getAlerts(playerId) {
  const items = await listItems(playerId);
  const alerts = [];
  for (const item of items) {
    if (item.replacedAt) continue;
    const t = DEFAULT_THRESHOLDS[item.type];
    if (!t) continue;
    if (t.games && item.gamesCount >= t.games) {
      alerts.push({ item, reason: `${item.gamesCount} parties (seuil ${t.games})` });
    } else if (t.holes && item.holesCount >= t.holes) {
      alerts.push({ item, reason: `${item.holesCount} trous (seuil ${t.holes})` });
    }
  }
  return alerts;
}
