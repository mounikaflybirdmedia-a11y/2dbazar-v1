import os

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # The exact string to replace
    old_str = "'${p.contact||'919885929818'}'"
    new_str = "'919885929818'"

    if old_str in content:
        content = content.replace(old_str, new_str)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed {filepath}")

for root, _, files in os.walk('d:\\2dbazar'):
    for file in files:
        if file.endswith('.html'):
            fix_file(os.path.join(root, file))
