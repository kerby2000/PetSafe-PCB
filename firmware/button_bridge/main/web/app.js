'use strict';
const ui = Object.fromEntries(['token', 'connect', 'press', 'connection', 'output', 'message']
  .map(id => [id, document.getElementById(id)]));
let token = '';
let busy = false;
let polling = false;

async function request(path, options = {}) {
  const response = await fetch(path, {
    ...options,
    cache: 'no-store',
    signal: AbortSignal.timeout(4000),
    headers: {Authorization: `Bearer ${token}`, ...(options.headers || {})},
  });
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || `HTTP ${response.status}`);
  return data;
}

function showStatus(s) {
  ui.connection.textContent = 'Connected';
  ui.output.textContent = s.output_fault ? 'Fault — inspect before restart' : s.button_active ? 'Pressed' : 'Released';
  ui.press.disabled = busy || s.output_fault || s.button_active || s.cooldown_remaining_ms > 0;
  ui.press.textContent = s.cooldown_remaining_ms > 0
    ? `Wait ${Math.ceil(s.cooldown_remaining_ms / 1000)} s` : 'Press PetSafe button';
}

async function refresh() {
  if (!token || busy || polling) return;
  polling = true;
  try { showStatus(await request('/api/status')); }
  catch (error) {
    ui.connection.textContent = 'Unavailable';
    ui.output.textContent = 'Unknown';
    ui.press.disabled = true;
  } finally { polling = false; }
}

ui.connect.addEventListener('click', async () => {
  if (busy) return;
  token = ui.token.value.trim();
  ui.press.disabled = true;
  if (token.length < 32) { ui.message.textContent = 'Enter the access token from setup.'; return; }
  try {
    showStatus(await request('/api/status'));
    ui.token.value = '';
    ui.message.textContent = 'Connected. Ready for an explicit button press.';
  } catch (error) {
    token = '';
    ui.connection.textContent = 'Not connected';
    ui.message.textContent = `Could not connect: ${error.message}`;
  }
});

ui.press.addEventListener('click', async () => {
  if (busy || ui.press.disabled) return;
  busy = true;
  ui.press.disabled = true;
  ui.connect.disabled = true;
  try {
    // A fresh server deadline and boot identifier are fetched for each explicit click.
    const s = await request('/api/status');
    if (s.output_fault || s.button_active || s.cooldown_remaining_ms > 0) {
      ui.message.textContent = s.output_fault ? 'Output fault. Inspect the board before restarting.' : 'Please wait for the previous press to finish.';
      return;
    }
    const result = await request('/api/press', {
      method: 'POST',
      headers: {
        'X-Bridge-Boot': s.boot_id,
        'X-Bridge-Sequence': String(s.next_sequence),
        'X-Bridge-Deadline': String(s.command_deadline_ms),
      },
    });
    ui.message.textContent = result.result === 'pulse_started'
      ? 'Button press started. Observe the PetSafe LED or latch to confirm its mode.'
      : 'This command was already accepted. No additional press was sent.';
  } catch (error) {
    // Never turn a lost response into a second toggle by retrying with a new sequence.
    ui.message.textContent = `Command not confirmed (${error.message}). Do not assume the flap changed state; check it before another press.`;
  } finally {
    busy = false;
    ui.connect.disabled = false;
    await refresh();
  }
});
setInterval(refresh, 1000);
