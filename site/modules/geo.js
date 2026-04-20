// Helpers de géolocalisation pour la future feature GPS au drapeau.

/**
 * Distance haversine entre 2 points GPS en mètres.
 * @param {number} lat1 @param {number} lng1
 * @param {number} lat2 @param {number} lng2
 * @returns {number} distance en mètres
 */
export function haversine(lat1, lng1, lat2, lng2) {
  const R = 6371000; // rayon Terre en mètres
  const toRad = (d) => (d * Math.PI) / 180;
  const dLat = toRad(lat2 - lat1);
  const dLng = toRad(lng2 - lng1);
  const a =
    Math.sin(dLat / 2) ** 2 +
    Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) * Math.sin(dLng / 2) ** 2;
  return Math.round(R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a)));
}

/**
 * Obtient la position GPS courante via navigator.geolocation.
 * @param {{timeout?: number, maxAge?: number, highAccuracy?: boolean}} [opts]
 * @returns {Promise<{lat: number, lng: number, accuracy: number, ts: number}>}
 */
export function getCurrentPosition(opts = {}) {
  return new Promise((resolve, reject) => {
    if (!('geolocation' in navigator)) {
      reject(new Error('Geolocation non supportée'));
      return;
    }
    navigator.geolocation.getCurrentPosition(
      (pos) =>
        resolve({
          lat: pos.coords.latitude,
          lng: pos.coords.longitude,
          accuracy: pos.coords.accuracy,
          ts: pos.timestamp,
        }),
      (err) => reject(err),
      {
        enableHighAccuracy: opts.highAccuracy ?? true,
        timeout: opts.timeout ?? 10000,
        maximumAge: opts.maxAge ?? 30000,
      },
    );
  });
}

/**
 * Vérifie si des coords sont raisonnables pour la France / zones voisines.
 * Évite d'enregistrer des coords erronées (0,0 par exemple).
 * @param {number} lat @param {number} lng
 */
export function isValidFrCoord(lat, lng) {
  return lat > 35 && lat < 55 && lng > -10 && lng < 15;
}
