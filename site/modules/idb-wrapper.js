// Wrapper IndexedDB via la lib `idb` (3 KB).
// Fournit les stores v3 : courseCoords, holeStats, equipment, mapTiles.

import { openDB } from 'idb';

const DB_NAME = 'ca_swingue_v3';
const DB_VERSION = 1;

/**
 * Schéma des stores :
 *  - courseCoords : {key: courseId+holeNum, value: {lat, lng, source, ts}}
 *  - holeStats    : {key: gameId+hole+pi,   value: {fir, gir, putts, notes}}
 *  - equipment    : {key: playerId+itemId,  value: {type, addedAt, usage}}
 *  - mapTiles     : {key: tileUrl,          value: {blob, fetchedAt}}
 */

let _dbPromise = null;

function getDB() {
  if (!_dbPromise) {
    _dbPromise = openDB(DB_NAME, DB_VERSION, {
      upgrade(db, oldV, newV) {
        if (!db.objectStoreNames.contains('courseCoords')) {
          db.createObjectStore('courseCoords');
        }
        if (!db.objectStoreNames.contains('holeStats')) {
          db.createObjectStore('holeStats');
        }
        if (!db.objectStoreNames.contains('equipment')) {
          db.createObjectStore('equipment');
        }
        if (!db.objectStoreNames.contains('mapTiles')) {
          db.createObjectStore('mapTiles');
        }
      },
    });
  }
  return _dbPromise;
}

/** @param {string} store @param {string} key */
export async function get(store, key) {
  return (await getDB()).get(store, key);
}

/** @param {string} store @param {any} value @param {string} key */
export async function put(store, value, key) {
  return (await getDB()).put(store, value, key);
}

/** @param {string} store */
export async function all(store) {
  return (await getDB()).getAll(store);
}

/** @param {string} store @param {string} key */
export async function del(store, key) {
  return (await getDB()).delete(store, key);
}

/** @param {string} store */
export async function clear(store) {
  return (await getDB()).clear(store);
}

/** @param {string} store @param {string} prefix */
export async function keysWithPrefix(store, prefix) {
  const db = await getDB();
  const keys = await db.getAllKeys(store);
  return keys.filter((k) => typeof k === 'string' && k.startsWith(prefix));
}

export const DB = { get, put, all, del, clear, keysWithPrefix };
