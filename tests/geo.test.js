import { test } from 'node:test';
import assert from 'node:assert/strict';
import { haversine, isValidFrCoord } from '../site/modules/geo.js';

test('haversine : même point = 0', () => {
  assert.equal(haversine(47.0, -1.5, 47.0, -1.5), 0);
});

test('haversine : ~111 km pour 1° de latitude', () => {
  const d = haversine(47.0, 0, 48.0, 0);
  assert.ok(d > 110000 && d < 112000, `attendu ~111000, reçu ${d}`);
});

test('haversine : distance courte (100m)', () => {
  // 0.001 degré ≈ 111 m à l'équateur, un peu moins à 47°
  const d = haversine(47.0, -1.5, 47.0, -1.4987);
  assert.ok(d > 80 && d < 120, `attendu ~100m, reçu ${d}`);
});

test('isValidFrCoord : Paris OK', () => {
  assert.equal(isValidFrCoord(48.85, 2.35), true);
});

test('isValidFrCoord : (0,0) rejeté', () => {
  assert.equal(isValidFrCoord(0, 0), false);
});

test('isValidFrCoord : USA rejeté', () => {
  assert.equal(isValidFrCoord(40.7, -74.0), false);
});
