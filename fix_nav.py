import os, glob, re

for filepath in glob.glob('d:/2dbazar/frontend/**/*.html', recursive=True):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if 'nav-inner' not in content:
        continue
        
    orig = content
    
    # 1. Add id="navLinks"
    content = content.replace('<div class="nav-links">', '<div class="nav-links" id="navLinks">')
    
    # 2. Insert button before the closing div of nav-inner.
    if 'nav-menu-btn' not in content:
        # In most files, there is:
        #   </div>
        # </nav>
        content = re.sub(r'(</div>\s*</nav>)', r'  <button class="nav-menu-btn" onclick="toggleMobileNav()">☰</button>\n\1', content)

    if orig != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Fixed", filepath)
