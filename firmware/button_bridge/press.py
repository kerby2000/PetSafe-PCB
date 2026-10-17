"""Send one explicit button press; never retry an uncertain toggle automatically."""
import argparse
import getpass
import json
import os
import urllib.error
import urllib.request


def api(base, token, path, headers=None):
    req = urllib.request.Request(base.rstrip('/') + path,
        headers={'Authorization': f'Bearer {token}', **(headers or {})},
        method='POST' if headers else 'GET')
    with urllib.request.urlopen(req, timeout=4) as response:
        return json.load(response)


def press(base, token):
    state = api(base, token, '/api/status')
    if state.get('output_fault'):
        raise RuntimeError('Output fault; no command sent. Inspect before restarting.')
    if state['button_active'] or state['cooldown_remaining_ms'] > 0:
        raise RuntimeError('Cooldown active; no command sent.')
    return api(base, token, '/api/press', {
        'X-Bridge-Boot': state['boot_id'],
        'X-Bridge-Sequence': str(state['next_sequence']),
        'X-Bridge-Deadline': str(state['command_deadline_ms']),
    })


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('url', help='Example: http://192.168.1.50')
    parser.add_argument('--status', action='store_true', help='Read status only; never actuate')
    args = parser.parse_args()
    token = os.environ.get('PETSAFE_BRIDGE_TOKEN') or getpass.getpass('Access token: ')
    try:
        result = api(args.url, token, '/api/status') if args.status else press(args.url, token)
        print(json.dumps(result, indent=2))
    except (OSError, ValueError, RuntimeError, urllib.error.URLError) as error:
        parser.exit(1, f'{error}\nNo automatic retry. If a press request was sent, its outcome may be unknown.\n')


if __name__ == '__main__':
    main()
