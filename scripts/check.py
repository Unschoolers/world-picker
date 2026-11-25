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
