import os
import re

frontend_dir = r"d:\2dbazar\frontend"

pages = [
    "admin-login", "admin", "dashboard-buyer", "dashboard-employer", "dashboard-provider",
    "dashboard-receiver", "dashboard-seeker", "dashboard-seller", "jobs", "login", 
    "marketplace", "privacy", "properties", "rules", "services", "signup", "terms", "index"
]

modified = 0
for root, dirs, files in os.walk(frontend_dir):
    for file in files:
        if file.endswith('.html') or file.endswith('.js'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content = content
            for page in pages:
                # We need to be careful to not replace if it already has .html
                # Match href="page" or href="../page" or href="pages/page"
                # Match window.location.href='page' or ='../page'
                
                # Replace href="page"
                new_content = re.sub(rf'href="([^"]*?)({page})"', lambda m: f'href="{m.group(1)}{m.group(2)}.html"' if not m.group(0).endswith('.html"') else m.group(0), new_content)
                
                # Replace location.href='page'
                new_content = re.sub(rf"location\.href='([^']*?)({page})'", lambda m: f"location.href='{m.group(1)}{m.group(2)}.html'" if not m.group(0).endswith(".html'") else m.group(0), new_content)
                
                # For data.js and signup.html DASH_MAP
                # e.g. admin:'admin'
                new_content = re.sub(rf":'({page})'", lambda m: f":'{m.group(1)}.html'", new_content)

            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                modified += 1
                print(f"Reverted: {filepath}")

print(f"Total reverted: {modified}")
