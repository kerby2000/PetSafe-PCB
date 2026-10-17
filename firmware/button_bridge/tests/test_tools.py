import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


def module(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / f'{name}.py')
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded


configure = module('configure')
client = module('press')


class ToolsTest(unittest.TestCase):
    def test_credentials_encoded_not_interpolated(self):
        config = {'ssid': 'wifi"\\é', 'password': 'some"\\password', 'token': 'x' * 43}
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'credentials.h'
            configure.write_header(config, path)
            text = path.read_text()
            self.assertIn('\\042', text)
            self.assertIn('\\303\\251', text)
            self.assertNotIn(config['password'], text)

    def test_invalid_credentials_rejected(self):
        base = {'ssid': 'wifi', 'password': 'valid-password', 'token': 'x' * 43}
        for key, value in [('ssid', ''), ('ssid', 'é' * 17), ('password', 'short'),
                           ('password', 'a' * 64), ('token', 'x' * 31), ('token', 'x' * 32 + '\n')]:
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                configure.validate({**base, key: value})

    def test_client_sends_one_fresh_command(self):
        status = dict(button_active=False, cooldown_remaining_ms=0, boot_id='boot',
                      next_sequence=7, command_deadline_ms=5000)
        with patch.object(client, 'api', side_effect=[status, {'result': 'pulse_started'}]) as api:
            self.assertEqual(client.press('http://board', 'token')['result'], 'pulse_started')
            self.assertEqual(api.call_count, 2)
            self.assertEqual(api.call_args.args[3], {'X-Bridge-Boot': 'boot',
                'X-Bridge-Sequence': '7', 'X-Bridge-Deadline': '5000'})

    def test_client_never_retries_uncertain_press(self):
        status = dict(button_active=False, cooldown_remaining_ms=0, boot_id='boot',
                      next_sequence=7, command_deadline_ms=5000)
        with patch.object(client, 'api', side_effect=[status, TimeoutError('lost reply')]) as api:
            with self.assertRaises(TimeoutError):
                client.press('http://board', 'token')
            self.assertEqual(api.call_count, 2)

    def test_cooldown_is_not_a_queued_command(self):
        for status in [dict(button_active=False, cooldown_remaining_ms=100),
                       dict(button_active=True, cooldown_remaining_ms=0)]:
            with patch.object(client, 'api', return_value=status) as api:
                with self.assertRaises(RuntimeError):
                    client.press('http://board', 'token')
                self.assertEqual(api.call_count, 1)


    def test_output_fault_does_not_send_command(self):
        with patch.object(client, 'api', return_value={'output_fault': True}) as api:
            with self.assertRaisesRegex(RuntimeError, 'Output fault'):
                client.press('http://board', 'token')
            self.assertEqual(api.call_count, 1)


if __name__ == '__main__':
    unittest.main()
