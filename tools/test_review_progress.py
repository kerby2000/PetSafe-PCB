"""Synthetic, in-memory progress checks; never add fictitious hardware evidence."""
import copy, hashlib, unittest, contextlib, html, io, json, re, runpy, shutil, tempfile
from pathlib import Path
from current_state import ROOT, read, current_state, validate_issue_register
from audit_physical_evidence import compare
from verify_capacitor_application import canonical_text_sha256, matches_text_digest, verify_receiver_capacitor_metadata
from inventory_contracts import verify_receiver_open_erc
from validate_native import wire_graph, board_net_partitions, verify_diode_functions, verify_button_bridge
import xml.etree.ElementTree as ET

class ReviewProgress(unittest.TestCase):
    def test_bridge_rejects_wrong_terminal_or_supply_join(self):
        xml=ET.parse(ROOT/'output/PetSafe_netlist.xml')
        self.assertEqual(verify_button_bridge(xml,self.model),{'U201','Q201','R201','R202'})
        # Catch C/E inversion, a pull-down before the base resistor, direct GPIO
        # drive, and either positive supply tied to factory copper.
        for source,target in [('Q201.3','S1.1'),('Q201.1','S1.2'),('R202.1','U201.6'),('Q201.2','U201.6'),('U201.11','U1.5'),('U201.13','S1.2'),('U201.6','S1.2')]:
            wrong=copy.deepcopy(xml)
            ref,pin=source.split('.');tr,tp=target.split('.')
            src=next(n for n in wrong.findall('./nets/net') if n.find('node[@ref="'+ref+'"][ @pin="'+pin+'"]') is not None)
            dst=next(n for n in wrong.findall('./nets/net') if n.find('node[@ref="'+tr+'"][ @pin="'+tp+'"]') is not None)
            node=src.find('node[@ref="'+ref+'"][ @pin="'+pin+'"]');src.remove(node);dst.append(node)
            with self.assertRaises(AssertionError,msg=(source,target)):board_net_partitions(wrong,self.model)

    def test_bridge_inventory_and_gpio_are_explicit(self):
        xml=ET.parse(ROOT/'output/PetSafe_netlist.xml')
        for ref in ['U201','Q201','R201','R202']:
            wrong=copy.deepcopy(xml);comp=wrong.find('./components/comp[@ref="'+ref+'"]')
            comp.remove(comp.find('property[@name="exclude_from_board"]'))
            with self.assertRaises(AssertionError):verify_button_bridge(wrong,self.model)
        for key,value in [('gpio','GPIO8'),('gpio_header_pin','8')]:
            wrong=copy.deepcopy(self.model);wrong['external_button_bridge'][key]=value
            with self.assertRaises(AssertionError):verify_button_bridge(xml,wrong)
        wrong=copy.deepcopy(xml);wrong.find('./components/comp[@ref="R201"]/value').text='0'
        with self.assertRaises(AssertionError):verify_button_bridge(wrong,self.model)

    def test_checklist_status_uses_empty_or_active_queue(self):
        # Execute the existing generator against disposable inputs. Synthetic
        # readings never enter the real queue, evidence or generated reports.
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)
            for directory in ['tools','evidence','docs']:(root/directory).mkdir()
            shutil.copyfile(ROOT/'tools/build_completion_audit.py',root/'tools/build_completion_audit.py')
            for file in ['reconstruction.json','remaining_work.json','capacitor_value_review_20261015.json','finalization_audit.json']:
                shutil.copyfile(ROOT/'evidence'/file,root/'evidence'/file)
            original=read('evidence/finishing_measurements.json')
            for active in [False,True]:
                queue=copy.deepcopy(original)
                if active:
                    queue.update(batch_title='Synthetic active check',instructions='One authorized fixture check is pending; see the measurement guide.',tests=[{'id':'SYNTHETIC_ONLY'}])
                (root/'evidence/finishing_measurements.json').write_text(json.dumps(queue),encoding='utf-8')
                with contextlib.redirect_stdout(io.StringIO()):runpy.run_path(str(root/'tools/build_completion_audit.py'),run_name='__main__')
                page=(root/'docs/FINISHING_CHECKLIST.html').read_text(encoding='utf-8')
                card=re.search(r'<div class="card"><b>.*?</div>',page).group()
                self.assertIn(html.escape(queue['batch_title']),card)
                self.assertIn(html.escape(queue['instructions']),card)
                if active:
                    self.assertNotIn('No readings are pending',card)
                    self.assertNotIn('No pending readings',card)
                    self.assertNotIn('RX-3 remains deferred',card)
                else:self.assertIn('No pending readings',card)

    def test_diode_direction_cannot_copy_d2_to_d1_or_d3(self):
        native=ET.parse(ROOT/'output/PetSafe_netlist.xml')
        verify_diode_functions(native,self.model)
        for ref in ['D1','D2','D3']:
            wrong=copy.deepcopy(self.model)
            c=next(c for c in wrong['components'] if c['ref']==ref)
            c['diode_functions']['series_path_native'].reverse()
            with self.assertRaises(AssertionError):verify_diode_functions(native,wrong)
        for ref in ['D1','D3']:
            wrong=copy.deepcopy(native)
            wrong.find('./components/comp[@ref="'+ref+'"]/libsource').set('part','D_Dual_Series_KAC')
            with self.assertRaises(AssertionError):verify_diode_functions(wrong,self.model)

    def test_receiver_capacitor_metadata_rejects_obsolete_topology(self):
        proposal=read('evidence/capacitor_value_review_20261015.json')
        verify_receiver_capacitor_metadata(proposal,self.model)
        for ref in ['C19','C20']:
            wrong=copy.deepcopy(proposal)
            c=next(c for c in wrong['components'] if c['ref']==ref)
            c['nets']=['GND','RX_A_PLUS']
            with self.assertRaises(AssertionError):verify_receiver_capacitor_metadata(wrong,self.model)
            c['nets']=next(c['nets'] for c in proposal['components'] if c['ref']==ref)
            c['basis']=c['historical_rationale']['basis']
            with self.assertRaises(AssertionError):verify_receiver_capacitor_metadata(wrong,self.model)

    def test_external_antenna_cannot_hide_wrong_endpoint(self):
        xml=ET.parse(ROOT/'output/PetSafe_netlist.xml')
        board_net_partitions(xml,self.model)
        wrong=copy.deepcopy(xml)
        a=next(net for net in wrong.findall('./nets/net') if net.find('node[@ref="L101"][@pin="1"]') is not None)
        b=next(net for net in wrong.findall('./nets/net') if net.find('node[@ref="L101"][@pin="2"]') is not None)
        node=b.find('node[@ref="L101"][@pin="2"]');b.remove(node);a.append(node)
        with self.assertRaises(AssertionError):board_net_partitions(wrong,self.model)

    def test_external_antenna_must_stay_off_main_board(self):
        xml=ET.parse(ROOT/'output/PetSafe_netlist.xml')
        for flag in ['exclude_from_bom','exclude_from_board']:
            wrong=copy.deepcopy(xml);comp=wrong.find('./components/comp[@ref="L101"]')
            comp.remove(comp.find('property[@name="'+flag+'"]'))
            with self.assertRaises(AssertionError):board_net_partitions(wrong,self.model)

    def test_native_t_junction_with_unsplit_trunk(self):
        graph=wire_graph([((0,0),(10,0)),((5,0),(5,5))])
        self.assertEqual(graph[(5,0)],{(0,0),(10,0),(5,5)})

    def test_native_crossing_needs_a_junction(self):
        wires=[((0,0),(10,0)),((5,-5),(5,5))]
        self.assertNotIn((5,0),wire_graph(wires))
        self.assertEqual(len(wire_graph(wires,{(5,0)})[(5,0)]),4)

    def test_native_open_tail_is_not_hidden(self):
        graph=wire_graph([((0,0),(10,0)),((5,0),(5,5))])
        pins={(0,0),(10,0)}
        self.assertEqual({p for p,n in graph.items() if len(n)==1 and p not in pins},{(5,5)})

    def test_receiver_erc_cannot_be_hidden_or_expand_unrelated(self):
        erc=read('output/erc.json')
        verify_receiver_open_erc(erc)
        missing=copy.deepcopy(erc)
        target=next(s['violations'] for s in missing['sheets'] if s['violations'])
        target.remove(next(v for v in target if v['type']=='pin_to_pin'))
        with self.assertRaises(AssertionError):verify_receiver_open_erc(missing)
        wrong=copy.deepcopy(erc)
        target=next(s['violations'] for s in wrong['sheets'] if s['violations'])
        next(v for v in target if v['type']=='pin_to_pin')['items'][0]['description']='Symbol U3 Pin 5 [+, Input, Line]'
        with self.assertRaises(AssertionError):verify_receiver_open_erc(wrong)

    def test_capacitor_text_hash_line_endings(self):
        lf=b'{"value": "100nF*"}\n'
        crlf=lf.replace(b'\n', b'\r\n')
        self.assertEqual(canonical_text_sha256(lf), canonical_text_sha256(crlf))
        for recorded in [hashlib.sha256(lf).hexdigest(), hashlib.sha256(crlf).hexdigest()]:
            self.assertTrue(matches_text_digest(lf, recorded))
            self.assertTrue(matches_text_digest(crlf, recorded))
            self.assertFalse(matches_text_digest(lf.replace(b'100nF', b'220nF'), recorded))
            self.assertFalse(matches_text_digest(lf+b' ', recorded))

    def test_evidence_detects_split_and_merge(self):
        edge=lambda a,b:dict(pair=[a,b],source='synthetic test fixture')
        result=compare({'A.1':'a','B.1':'b','C.1':'a'},[edge('A.1','B.1')],[edge('A.1','C.1')],[])
        self.assertEqual(len(result['split_findings']),1)
        self.assertEqual(len(result['incorrect_merge_findings']),1)

    def test_modeled_membership_is_not_evidence(self):
        result=compare({'A.1':'same','B.1':'same','C.1':'same'},
                       [dict(pair=['A.1','B.1'],source='synthetic photo')],[],[])
        self.assertEqual(result['unsupported_join_questions'][0]['groups'],[['A.1','B.1'],['C.1']])

    def test_photo_inventory_gap_is_reported(self):
        result=compare({'A.1':'a'},[],[],[dict(pads=['X.1'],source='synthetic photographed pad')])
        self.assertEqual(result['unmapped_observed_pads'][0]['pad'],'X.1')

    def test_component_path_is_not_inferred(self):
        result=compare({'R5.1':'supply','R5.2':'filtered'},[],[],[])
        self.assertFalse(result['split_findings'])
        self.assertEqual(result['supported_net_groups'],2)

    def setUp(self):
        self.model=read('evidence/reconstruction.json')
        self.work=read('evidence/remaining_work.json')
        self.validation=read('evidence/validation.json')

    def test_closed_issue_remains_in_history(self):
        item=next(i for i in self.work['issues'] if i['id']=='I01')
        item['state']='open'; item.pop('resolution',None)
        original=copy.deepcopy(self.work)
        item.update(state='closed',resolution=dict(date='2099-01-01',result='Synthetic identity completion fixture; not a hardware result.',evidence=['in-memory test fixture']))
        validate_issue_register(self.model,self.work)
        state=current_state(self.model,self.validation,self.work)
        self.assertNotIn('I01',[i['id'] for i in state['items']])
        self.assertEqual(next(i for i in state['closed_items'] if i['id']=='I01')['unknown'],next(i for i in original['issues'] if i['id']=='I01')['unknown'])
        self.assertEqual(len(state['items'])+len(state['closed_items']),len(original['issues']))

    def test_individual_value_update_reduces_unknown_list(self):
        cap=next(c for c in self.model['components'] if c['ref']=='C6')
        cap.update(value='UNKNOWN',value_evidence=dict(state='unknown',source='Synthetic starting state; not a board reading.'))
        before=current_state(self.model,self.validation,self.work)
        cap.update(value='4.7nF',value_evidence=dict(state='measured',source='Synthetic isolated-component LCR fixture, 1 kHz/100 mV; not a board reading.'))
        after=current_state(self.model,self.validation,self.work)
        self.assertIn('C6',before['unknown_ceramic_values'])
        self.assertNotIn('C6',after['unknown_ceramic_values'])
        self.assertEqual(len(before['unknown_ceramic_values'])-1,len(after['unknown_ceramic_values']))
        cap['value_evidence']['state']='estimated'
        self.assertIn('C6',current_state(self.model,self.validation,self.work)['unknown_ceramic_values'])

    def test_unsupported_closure_rejected(self):
        item=next(i for i in self.work['issues'] if i['id']=='I01')
        item['state']='closed'; item.pop('resolution',None)
        with self.assertRaises(AssertionError):validate_issue_register(self.model,self.work)

    def test_closing_issue_cannot_hide_open_pad(self):
        # Explicit fixture stays meaningful after the real D2 connections are recovered.
        if 'D2.L' not in self.model['unresolved_pins']:
            self.model['unresolved_pins'].append('D2.L')
        for issue in self.work['issues']:
            issue['open_pads']=[p for p in issue['open_pads'] if p!='D2.L']
        item=next(i for i in self.work['issues'] if i['id']=='I01')
        item['open_pads'].append('D2.L')
        item.update(state='closed',resolution=dict(date='2099-01-01',result='Synthetic premature closure',evidence=['fixture']))
        with self.assertRaises(AssertionError):validate_issue_register(self.model,self.work)

if __name__=='__main__':
    paths=[ROOT/'evidence/reconstruction.json',ROOT/'evidence/remaining_work.json',ROOT/'evidence/cleanup_verification.json',ROOT/'evidence/finishing_measurements.json',ROOT/'docs/FINISHING_CHECKLIST.html']
    before={p:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(ReviewProgress)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    assert before=={p:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},'Progress tests modified real records'
    raise SystemExit(0 if result.wasSuccessful() else 1)
