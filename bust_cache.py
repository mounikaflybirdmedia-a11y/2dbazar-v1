import os
import time
import re

v = str(int(time.time()))

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Match <script src="../js/data.js..."></script> or similar, preserving path prefix
    pattern = r'<script\s+src="((?:\.\./)*js/data\.js)(?:\?v=\d+)?"\s*></script>'
    
    def repl(match):
        path = match.group(1)
        return f'<script src="{path}?v={v}"></script>'

    if re.search(pattern, content):
        content = re.sub(pattern, repl, content)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed cache-busting in {filepath} (v={v})")

for root, _, files in os.walk('d:\\2dbazar'):
    for file in files:
        if file.endswith('.html'):
            fix_file(os.path.join(root, file))

