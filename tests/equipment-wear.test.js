import { test } from 'node:test';
import assert from 'node:assert/strict';
import { DEFAULT_THRESHOLDS } from '../site/modules/equipment-wear.js';

test('DEFAULT_THRESHOLDS : toutes les catégories ont au moins un seuil', () => {
  for (const [type, t] of Object.entries(DEFAULT_THRESHOLDS)) {
    assert.ok(t.games || t.holes, `${type} n'a ni seuil games ni holes`);
  }
});

test('DEFAULT_THRESHOLDS : balles = 3 parties', () => {
  assert.equal(DEFAULT_THRESHOLDS.balls.games, 3);
});

test('DEFAULT_THRESHOLDS : gants = 20 parties', () => {
  assert.equal(DEFAULT_THRESHOLDS.gloves.games, 20);
});
