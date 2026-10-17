"""Create local-only Wi-Fi credentials and token; no credentials go in git or console logs."""
import getpass
import json
from pathlib import Path
import secrets

ROOT = Path(__file__).resolve().parent


def validate(config):
    ssid = config['ssid']
    password = config['password']
    token = config['token']
    if not isinstance(ssid, str) or not 1 <= len(ssid.encode('utf-8')) <= 32 or '\x00' in ssid:
        raise ValueError('SSID must be 1–32 UTF-8 bytes, with no NUL.')
    if not isinstance(password, str) or not 8 <= len(password.encode('utf-8')) <= 63 or '\x00' in password:
        raise ValueError('Use a WPA2/WPA3 personal passphrase of 8–63 UTF-8 bytes, with no NUL.')
    if not isinstance(token, str) or not 32 <= len(token) <= 128 or not all(
            c in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_' for c in token):
        raise ValueError('Token must be 32–128 letters, digits, hyphens or underscores.')


def c_string(text):
    # Encode every UTF-8 byte as an octal escape: quotes/backslashes cannot become C code.
    return '"' + ''.join(f'\\{byte:03o}' for byte in text.encode('utf-8')) + '"'


def write_header(config, destination):
    validate(config)
    content = '// Generated locally by configure.py. Contains secrets; never commit.\n'
    for name, key in [('BRIDGE_WIFI_SSID', 'ssid'), ('BRIDGE_WIFI_PASSWORD', 'password'),
                      ('BRIDGE_API_TOKEN', 'token')]:
        content += f'#define {name} {c_string(config[key])}\n'
    destination.write_text(content, encoding='utf-8')


def main():
    path = ROOT / 'credentials.local.json'
    if path.exists():
        config = json.loads(path.read_text(encoding='utf-8'))
    else:
        config = {'ssid': input('2.4 GHz Wi-Fi SSID: '),
                  'password': getpass.getpass('Wi-Fi password: '),
                  'token': secrets.token_urlsafe(32)}
    validate(config)
    path.write_text(json.dumps(config, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    write_header(config, ROOT / 'main' / 'credentials.local.h')
    print('Local credentials and generated header saved. Both are git-ignored.')
    print('Open credentials.local.json locally to copy the token into the web page. Rebuild before flashing.')


if __name__ == '__main__':
    main()
