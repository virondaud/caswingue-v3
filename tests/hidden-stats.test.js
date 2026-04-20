import { test } from 'node:test';
import assert from 'node:assert/strict';
import { statKey, autoGIR } from '../site/modules/hidden-stats.js';

test('statKey : format attendu', () => {
  assert.equal(statKey('g1', 3, 0), 'g1_3_0');
});

test('autoGIR : eagle (score = par - 2) = GIR certain', () => {
  assert.equal(autoGIR(3, 5), true);
});

test('autoGIR : birdie = indéterminé', () => {
  assert.equal(autoGIR(4, 5), null);
});

test('autoGIR : bogey = indéterminé', () => {
  assert.equal(autoGIR(5, 4), null);
});

test('autoGIR : score manquant = null', () => {
  assert.equal(autoGIR(0, 4), null);
  assert.equal(autoGIR(null, 4), null);
});
