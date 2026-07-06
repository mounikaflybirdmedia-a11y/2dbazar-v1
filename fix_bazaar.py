import os, glob, re

pages_dir = r'd:\2dbazar\frontend\pages'
html_files = glob.glob(os.path.join(pages_dir, '*.html'))
html_files.append(r'd:\2dbazar\index.html')

for f in html_files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Replace the logo text specifically, handling whitespace
    content = re.sub(r'<span class="logo-badge">2D</span>\s*Bazar', r'<span class="logo-badge">2D</span>Bazaar', content)
    content = re.sub(r'<h2><span>2D</span>\s*Bazar</h2>', r'<h2><span>2D</span>Bazaar</h2>', content)
    
    # Also fix general text references
    content = content.replace('2D Bazaar', '2DBazaar')
    content = content.replace('2D Bazar', '2DBazaar')
    content = content.replace('2Dbazar', '2DBazaar')
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)

print('Updated 2DBazaar globally.')
