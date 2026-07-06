import re

filepath = r'd:\2dbazar\frontend\pages\admin.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

pattern = r'<button class="btn btn-sm" style="background:#ef4444;color:#fff;" onclick="(edit[A-Za-z]+)\((.*?)\)" style="margin-right:5px;">Edit</button><button class="btn btn-sm" style="background:#ef4444;color:#fff;" onclick="(delete[A-Za-z]+)\((.*?)\)">Remove</button>'

replacement = r'<div style="display:flex;gap:6px;justify-content:center;"><button class="btn btn-sm" style="background:#3b82f6;color:#fff;" onclick="\1(\2)">Edit</button><button class="btn btn-sm" style="background:#ef4444;color:#fff;" onclick="\3(\4)">Remove</button></div>'

new_content = re.sub(pattern, replacement, content)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(new_content)

print('Buttons fixed in admin.html')
