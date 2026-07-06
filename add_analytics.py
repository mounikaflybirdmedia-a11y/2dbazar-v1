import os
import re

ANALYTICS_TAG = """<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-KTW607FH1F"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-KTW607FH1F');
</script>"""

def inject_analytics(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Check if already has Google Analytics
    if "G-KTW607FH1F" in content:
        print(f"Skipping (already has tag): {file_path}")
        return False
        
    # Find <head> tag and insert right after it
    match = re.search(r'<head\b[^>]*>', content, re.IGNORECASE)
    if match:
        insert_pos = match.end()
        # Add new line before and after tag for clean format
        new_content = content[:insert_pos] + "\n" + ANALYTICS_TAG + content[insert_pos:]
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Successfully injected tag into: {file_path}")
        return True
    else:
        print(f"Could not find <head> in: {file_path}")
        return False

def main():
    target_dir = "frontend"
    count = 0
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                if inject_analytics(file_path):
                    count += 1
    print(f"\nDone! Injected Google Analytics tag into {count} HTML files.")

if __name__ == "__main__":
    main()
