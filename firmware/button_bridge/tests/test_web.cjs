const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const source = fs.readFileSync(path.join(__dirname, '../main/web/app.js'), 'utf8');

function fixture() {
  const nodes = Object.fromEntries(['token','connect','press','connection','output','message'].map(id => [id, {
    value: '', disabled: id === 'press', textContent: '', handlers: {},
    addEventListener(event, fn) {this.handlers[event] = fn;},
  }]));
  const requests = [];
  const pending = [];
  const context = {
    document: {getElementById: id => nodes[id]},
    AbortSignal: {timeout: () => ({})},
    setInterval() {},
    fetch: async (url, options) => {
      requests.push({url, options});
      const result = pending.shift();
      if (result instanceof Error) throw result;
      assert(result, 'Unexpected request');
      return {ok: true, json: async () => result};
    },
  };
  vm.runInNewContext(source, context);
  return {nodes, requests, pending};
}
const status = {button_active:false, cooldown_remaining_ms:0, boot_id:'boot-one', next_sequence:1, command_deadline_ms:5000};

(async () => {
  const f = fixture();
  assert.equal(f.requests.length, 0, 'Loading page must not send a command');
  f.nodes.token.value = 'x'.repeat(43);
  f.pending.push(status);
  await f.nodes.connect.handlers.click();
  assert.equal(f.requests.length, 1);
  assert.equal(f.requests[0].url, '/api/status');
  assert.equal(f.nodes.token.value, '');
  assert.equal(f.nodes.press.disabled, false);
  f.pending.push(status, {result:'pulse_started'}, {...status, cooldown_remaining_ms:4900});
  const first = f.nodes.press.handlers.click();
  const second = f.nodes.press.handlers.click();
  await Promise.all([first, second]);
  assert.equal(f.requests.filter(r => r.options.method === 'POST').length, 1);
  const command = f.requests.find(r => r.options.method === 'POST');
  assert.equal(command.options.headers['X-Bridge-Boot'], 'boot-one');
  assert.equal(command.options.headers['X-Bridge-Sequence'], '1');
  assert.equal(f.nodes.press.disabled, true);

  // A lost response is reported, never retried as a fresh toggle.
  const g = fixture();
  g.nodes.token.value = 'x'.repeat(43);
  g.pending.push(status);
  await g.nodes.connect.handlers.click();
  g.pending.push(status, new Error('timeout'), {...status, cooldown_remaining_ms:4900});
  await g.nodes.press.handlers.click();
  assert.equal(g.requests.filter(r => r.options.method === 'POST').length, 1);
  assert.match(g.nodes.message.textContent, /Command not confirmed/);
  assert.equal(g.nodes.press.disabled, true);
  const h = fixture();
  h.nodes.token.value = 'x'.repeat(43);
  h.pending.push({...status, output_fault:true});
  await h.nodes.connect.handlers.click();
  assert.equal(h.nodes.press.disabled, true);
  assert.match(h.nodes.output.textContent, /Fault/);
  await h.nodes.press.handlers.click();
  assert.equal(h.requests.filter(r => r.options.method === 'POST').length, 0);
  console.log('Web PASS: no startup press, authentication flow, double-click suppression, cooldown, no retry after timeout');
})().catch(error => {console.error(error); process.exit(1);});
