import os
import re

directory = r'd:\2dbazar\frontend'
for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # This regex will correctly replace ${encodeURIComponent(variable)} with ${variable}
            new_content = re.sub(r'\$\{encodeURIComponent\(([^)]+)\)\}', r'${\1}', content)
            
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f'Updated {filepath}')
