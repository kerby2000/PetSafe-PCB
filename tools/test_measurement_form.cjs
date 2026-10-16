/* Offline behavior tests. No browser security restriction is bypassed. */
const fs=require('fs'),vm=require('vm'),assert=require('assert/strict');
const script=fs.readFileSync('tools/measurement_form.js','utf8');
const queue=JSON.parse(fs.readFileSync('evidence/finishing_measurements.json','utf8'));
// Exercise the archived capacitor form independently of today's empty queue.
// Never reactivate those completed readings to make this test pass.
const fixtureIds=['B86','B87','B88','B89','B90','B91'];
const tests=queue.completed_tests.filter(t=>fixtureIds.includes(t.id));
assert.equal(tests.length,6);
const saved=new Map();
function harness({active=true,blockedStorage=false,blockedClipboard=false,batch='fixture'}={}) {
  const fields=active?Object.fromEntries(tests.map(t=>[t.id,{value:'',dataset:{id:t.id}}])):{};
  const els={reply:{value:'',focus(){},select(){this.selected=true;}},copy:{},select:{},download:{},'draft-status':{},'result-status':{}};
  let copied,downloaded;
  const document={querySelector(s){if(s==='#baseline')return null;if(s.startsWith('#'))return els[s.slice(1)];return fields[s.match(/data-id="([^"]+)"/)[1]];},querySelectorAll(){return Object.values(fields);},body:{appendChild(){}},createElement(){return {click(){downloaded=this.download;},remove(){}};}};
  const localStorage={getItem(k){if(blockedStorage)throw Error('denied');return saved.get(k)||null;},setItem(k,v){if(blockedStorage)throw Error('denied');saved.set(k,v);}};
  const context={document,localStorage,navigator:{clipboard:{async writeText(t){if(blockedClipboard)throw Error('denied');copied=t;}}},Blob,URL:{createObjectURL(){return 'blob:test';},revokeObjectURL(){}},setTimeout(fn){fn();}};
  vm.createContext(context);vm.runInContext(script,context);
  context.initializeMeasurementForm({tests,active,batch,title:'Test only',revision:'v0.9.43',contacts:['tip 1','tip 2']});
  return {fields,els,get copied(){return copied;},get downloaded(){return downloaded;}};
}
(async()=>{
  let h=harness(); h.fields.B86.value='680 pF';h.fields.B86.oninput();
  assert(h.els.reply.value.includes('B86 tip 1 21A / tip 2 21B'));
  assert(h.els.reply.value.includes('680 pF'));
  h=harness();assert.equal(h.fields.B86.value,'680 pF'); // reload preserves draft
  assert.equal(harness({batch:'other'}).fields.B86.value,''); // no cross-batch leakage
  h.fields.B87.value='340 pF';await h.els.copy.onclick(); // collect even absent input event
  assert(h.copied.includes('340 pF'));assert(h.els['result-status'].textContent.startsWith('Copied'));
  h=harness({blockedClipboard:true,blockedStorage:true});h.fields.B86.value='680 pF';h.fields.B86.onchange();await h.els.copy.onclick();
  assert(h.els.reply.selected);assert(h.els['result-status'].textContent.includes('Ctrl+C'));
  assert(h.els['draft-status'].textContent.includes('unavailable'));
  h.els.download.onclick();assert.equal(h.downloaded,'PetSafe-fixture.txt');
  h=harness({active:false});await h.els.copy.onclick();
  for(const t of tests)assert(h.copied.includes(t.result));
  assert.equal(h.copied.split('\n').length,7);
  const html=fs.readFileSync('docs/FINISHING_MEASUREMENTS.html','utf8');
  assert(html.replaceAll('\r\n','\n').includes(script.replaceAll('\r\n','\n')));
  assert(html.includes('FINISHING_CHECKLIST.html'));
  if(queue.tests.length===0)assert(!html.includes('<input data-id='));
  console.log('PASS: draft restore/isolation, input/change and copy collection, blocked storage/clipboard fallback, download, six archived results, generated script. Browser UI not tested.');
})();
