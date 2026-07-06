import os
import glob

pages_dir = r'd:\2dbazar\frontend\pages'
index_file = r'd:\2dbazar\frontend\index.html'

# The broken pattern in all pages (with ✉️ emoji that renders as square box)
OLD_EMAIL = '<a href="mailto:2dbazaar.com@gmail.com">\u2709\ufe0f 2dbazaar.com@gmail.com</a>'

# Fixed version - no broken emoji, proper flex alignment, icon-text on same line
NEW_EMAIL = '<a href="mailto:2dbazaar.com@gmail.com" style="display:flex;align-items:flex-start;gap:6px;line-height:1.5;"><span style="flex-shrink:0;margin-top:1px;">&#128140;</span><span>2dbazaar.com@gmail.com</span></a>'

# Also fix the version in index.html that was already partially fixed
OLD_EMAIL_2 = '''<a href="mailto:2dbazaar.com@gmail.com" style="display:flex;align-items:center;gap:6px;word-break:break-all;">
          <span style="flex-shrink:0;">&#9993;</span> 2dbazaar.com@gmail.com
        </a>'''

NEW_EMAIL_2 = '<a href="mailto:2dbazaar.com@gmail.com" style="display:flex;align-items:flex-start;gap:6px;line-height:1.5;"><span style="flex-shrink:0;margin-top:1px;">&#128140;</span><span>2dbazaar.com@gmail.com</span></a>'

all_files = glob.glob(os.path.join(pages_dir, '*.html')) + [index_file]

fixed = []
for f in all_files:
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    
    original = content
    content = content.replace(OLD_EMAIL, NEW_EMAIL)
    content = content.replace(OLD_EMAIL_2, NEW_EMAIL_2)
    
    if content != original:
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(content)
        fixed.append(os.path.basename(f))

print(f"Fixed {len(fixed)} files:")
for f in fixed:
    print(f"  - {f}")
print("Done!")
