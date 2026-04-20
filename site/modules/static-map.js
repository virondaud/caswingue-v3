// Génération d'URLs de cartes satellite/topographiques statiques.
// Utilisé par la future feature F4 (carte du trou).

import { DB } from './idb-wrapper.js';

/**
 * Génère une URL OpenStreetMap statique (via staticmap.openstreetmap.de).
 * Pas de clé API requise, limite ~1 req/sec par IP.
 *
 * @param {number} lat @param {number} lng @param {number} zoom
 * @param {number} width @param {number} height
 */
export function osmStaticUrl(lat, lng, zoom = 17, width = 600, height = 400) {
  return (
    `https://staticmap.openstreetmap.de/staticmap.php` +
    `?center=${lat},${lng}&zoom=${zoom}&size=${width}x${height}` +
    `&maptype=mapnik&markers=${lat},${lng},red-pushpin`
  );
}

/**
 * Récupère le blob d'une carte, avec cache IndexedDB.
 * @param {string} url
 * @returns {Promise<Blob>}
 */
export async function getMapTile(url) {
  const cached = await DB.get('mapTiles', url);
  if (cached?.blob) return cached.blob;
  const resp = await fetch(url);
  if (!resp.ok) throw new Error(`Map fetch ${resp.status}`);
  const blob = await resp.blob();
  await DB.put('mapTiles', { blob, fetchedAt: Date.now() }, url);
  return blob;
}

/** @param {Blob} blob */
export function blobToObjectURL(blob) {
  return URL.createObjectURL(blob);
}
