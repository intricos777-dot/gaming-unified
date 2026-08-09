import { test } from 'node:test';
import assert from 'node:assert';
import { seal, unseal, LAYER_NAMES, layerPassphrase, derivePersonalLayerKey, status, wrapLayer, unwrapLayer } from '../src/layered-enochian.js';

test('status reports 7 layers', () => {
  const s = status();
  assert.strictEqual(s.layers.length, 7);
  assert.deepStrictEqual(s.layers, LAYER_NAMES);
});

test('seal/unseal roundtrip preserves plaintext', () => {
  const secret = process.env.QE_TEST_SECRET || "test-secret";
  const context = 'roundtrip';
  const plaintext = 'quantum enochian layered roundtrip';
  const sealed = seal(plaintext, secret, context);
  const recovered = unseal(sealed, secret, context);
  assert.strictEqual(recovered, plaintext);
});

test('different contexts change output', () => {
  const secret = process.env.QE_TEST_SECRET || "test-secret";
  const ctx1 = seal('x', secret, 'ctx-a');
  const ctx2 = seal('x', secret, 'ctx-b');
  assert.notStrictEqual(ctx1, ctx2);
});

test('layer passphrase is deterministic', () => {
  const a = layerPassphrase(0, 'secret', 'ctx');
  const b = layerPassphrase(0, 'secret', 'ctx');
  assert.strictEqual(a, b);
});

test('personal layer key derivation is deterministic', () => {
  const a = derivePersonalLayerKey(2, 'name', 'entropy');
  const b = derivePersonalLayerKey(2, 'name', 'entropy');
  assert.strictEqual(a, b);
});

test('wrong secret fails unseal', async () => {
  const sealed = seal('data', 'correct', 'ctx');
  let failed = false;
  try {
    unseal(sealed, 'wrong', 'ctx');
  } catch {
    failed = true;
  }
  assert.strictEqual(failed, true);
});

test('layer 0 wrapLayer/unwrapLayer preserves bytes', () => {
  const data = Buffer.from('layer-zero-check', 'utf8');
  const wrapped = wrapLayer(data, 0, 'secret', 'ctx');
  const recovered = Buffer.from(unwrapLayer(wrapped, 0, 'secret', 'ctx'), 'utf8');
  assert.deepStrictEqual(recovered, data);
});
