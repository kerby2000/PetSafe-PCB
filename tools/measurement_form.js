/* Local worksheet: no transmission. Clipboard denial must leave a usable fallback. */
function initializeMeasurementForm(config) {
  const data = config.tests;
  if (!data.length) return;
  const reply = document.querySelector('#reply');
  const status = document.querySelector('#result-status');
  const draft = document.querySelector('#draft-status');
  const key = 'petsafe-measurements-v1:' + config.batch + ':' + data.map(t => t.id).join(',');
  const fields = Array.from(document.querySelectorAll('input'));
  const fieldKey = e => e.dataset.id || e.id;
  if (config.active) {
    try {
      const saved = JSON.parse(localStorage.getItem(key) || '{}');
      fields.forEach(e => { if (typeof saved[fieldKey(e)] === 'string') e.value = saved[fieldKey(e)]; });
      draft.textContent = Object.keys(saved).length ? 'Saved draft restored in this browser.' : 'Entries will be saved in this browser when supported.';
    } catch (_) { draft.textContent = 'Browser draft storage unavailable. Copy or download before closing.'; }
  }
  function update(save) {
    const base = document.querySelector('#baseline');
    reply.value = 'PetSafe ' + config.title + ' / ' + config.revision + '\n' +
      (base ? 'Shorted probes: ' + base.value + ' ohms\n' : '') +
      data.map(t => t.id + ' ' + config.contacts[0] + ' ' + t.from + ' / ' + config.contacts[1] + ' ' + t.to +
        (t.state ? ' (' + t.state + ')' : '') + ': ' +
        (config.active ? document.querySelector('[data-id="' + t.id + '"]').value : t.result)).join('\n');
    if (save && config.active) {
      try {
        localStorage.setItem(key, JSON.stringify(Object.fromEntries(fields.map(e => [fieldKey(e), e.value]))));
        draft.textContent = 'Draft saved in this browser. Nothing has been sent.';
      } catch (_) { draft.textContent = 'Browser draft storage unavailable. Copy or download before closing.'; }
    }
  }
  function selectResults() { update(true); reply.focus(); reply.select(); }
  fields.forEach(e => { e.oninput = () => update(true); e.onchange = () => update(true); });
  document.querySelector('#copy').onclick = async () => {
    update(true);
    try {
      if (!navigator.clipboard || !navigator.clipboard.writeText) throw new Error('Clipboard unavailable');
      await navigator.clipboard.writeText(reply.value);
      status.textContent = 'Copied. Paste the results into the chat.';
    } catch (_) {
      selectResults();
      status.textContent = 'Automatic copy is unavailable here. Results are selected: press Ctrl+C, then paste into the chat.';
    }
  };
  document.querySelector('#select').onclick = () => {
    selectResults(); status.textContent = 'Results selected. Press Ctrl+C, then paste into the chat.';
  };
  document.querySelector('#download').onclick = () => {
    update(true);
    const url = URL.createObjectURL(new Blob([reply.value], {type:'text/plain;charset=utf-8'}));
    const link = document.createElement('a');
    link.href = url; link.download = 'PetSafe-' + config.batch + '.txt';
    document.body.appendChild(link); link.click(); link.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
    status.textContent = 'Text download requested. You can attach the saved file to the chat.';
  };
  update(false);
}
