// Vérifie l'intégrité du bundle v3 au démarrage.
// Compare le SHA-256 du bundle chargé vs integrity.json.
// Non bloquant : warn en console si mismatch, pas d'arrêt de l'app.

/**
 * @returns {Promise<{ok: boolean, details?: string}>}
 */
export async function verifyIntegrity() {
  try {
    const manifest = await fetch('integrity.json', { cache: 'no-cache' })
      .then((r) => (r.ok ? r.json() : null));
    if (!manifest) return { ok: false, details: 'integrity.json absent' };

    const bundleUrl = 'dist/v3-modules.js';
    const expected = manifest.files?.[`site/${bundleUrl}`];
    if (!expected) return { ok: false, details: 'hash bundle manquant' };

    const bundle = await fetch(bundleUrl, { cache: 'no-cache' })
      .then((r) => (r.ok ? r.arrayBuffer() : null));
    if (!bundle) return { ok: false, details: 'bundle introuvable' };

    const hashBuf = await crypto.subtle.digest('SHA-256', bundle);
    const hashHex = Array.from(new Uint8Array(hashBuf))
      .map((b) => b.toString(16).padStart(2, '0'))
      .join('');

    if (hashHex !== expected) {
      return { ok: false, details: `mismatch: ${hashHex.slice(0, 16)} ≠ ${expected.slice(0, 16)}` };
    }
    return { ok: true };
  } catch (err) {
    return { ok: false, details: err?.message || 'error' };
  }
}
