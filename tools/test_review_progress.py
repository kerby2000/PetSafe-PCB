"""Synthetic, in-memory progress checks; never add fictitious hardware evidence."""
import copy, hashlib, unittest
from current_state import ROOT, read, current_state, validate_issue_register

class ReviewProgress(unittest.TestCase):
    def setUp(self):
        self.model=read('evidence/reconstruction.json')
        self.work=read('evidence/remaining_work.json')
        self.validation=read('evidence/validation.json')

    def test_closed_issue_remains_in_history(self):
        item=next(i for i in self.work['issues'] if i['id']=='I02')
        item['state']='open'; item.pop('resolution',None)
        original=copy.deepcopy(self.work)
        item.update(state='closed',resolution=dict(date='2099-01-01',result='Synthetic LED/connector completion fixture; not a hardware result.',evidence=['in-memory test fixture']))
        validate_issue_register(self.model,self.work)
        state=current_state(self.model,self.validation,self.work)
        self.assertNotIn('I02',[i['id'] for i in state['items']])
        self.assertEqual(next(i for i in state['closed_items'] if i['id']=='I02')['unknown'],next(i for i in original['issues'] if i['id']=='I02')['unknown'])
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
        item=next(i for i in self.work['issues'] if i['id']=='I02')
        item['state']='closed'; item.pop('resolution',None)
        with self.assertRaises(AssertionError):validate_issue_register(self.model,self.work)

    def test_closing_issue_cannot_hide_open_pad(self):
        # Explicit fixture stays meaningful after the real D2 connections are recovered.
        if 'D2.L' not in self.model['unresolved_pins']:
            self.model['unresolved_pins'].append('D2.L')
        for issue in self.work['issues']:
            issue['open_pads']=[p for p in issue['open_pads'] if p!='D2.L']
        item=next(i for i in self.work['issues'] if i['id']=='E01')
        item['open_pads'].append('D2.L')
        item.update(state='closed',resolution=dict(date='2099-01-01',result='Synthetic premature closure',evidence=['fixture']))
        with self.assertRaises(AssertionError):validate_issue_register(self.model,self.work)

if __name__=='__main__':
    paths=[ROOT/'evidence/reconstruction.json',ROOT/'evidence/remaining_work.json',ROOT/'evidence/cleanup_verification.json']
    before={p:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(ReviewProgress)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    assert before=={p:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},'Progress tests modified real records'
    raise SystemExit(0 if result.wasSuccessful() else 1)
