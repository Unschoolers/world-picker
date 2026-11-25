from pathlib import Path
import re
import subprocess
import tempfile

html = Path('index.html').read_text(encoding='utf-8')
assert '<!doctype html>' in html.lower()
assert 'Apprendre mes pays' in html
scripts = re.findall(r'<script\b[^>]*>(.*?)</script\s*>', html, re.I | re.S)
assert scripts, 'No inline JavaScript found'
with tempfile.TemporaryDirectory() as tmp:
    for i, script in enumerate(scripts):
        path = Path(tmp) / f'script-{i}.js'
        path.write_text(script, encoding='utf-8')
        subprocess.run(['node', '--check', str(path)], check=True)
print('HTML entry point and JavaScript syntax OK')

# Verify the PWA files and actual PNG dimensions.
import json
import struct

manifest = json.loads(Path('manifest.webmanifest').read_text(encoding='utf-8'))
assert manifest['display'] == 'standalone'
assert manifest['start_url'] == manifest['scope'] == './'
assert 'href="./manifest.webmanifest"' in html
assert "register('./sw.js')" in html
for icon in manifest['icons'] + [{'src':'icons/icon-180.png','sizes':'180x180'}]:
    data = Path(icon['src']).read_bytes()
    assert data[:8] == b'\x89PNG\r\n\x1a\n' and data[12:16] == b'IHDR'
    assert struct.unpack('>II', data[16:24]) == tuple(map(int, icon['sizes'].split('x')))
subprocess.run(['node', '--check', 'sw.js'], check=True)
assert '__BUILD_VERSION__' in Path('sw.js').read_text(encoding='utf-8')
print('PWA manifest, icons and service worker syntax OK')
