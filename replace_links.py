import os

frontend_dir = r"d:\2dbazar\frontend"

pages = [
    "admin", "admin-login", "dashboard-buyer", "dashboard-employer", "dashboard-provider",
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
                new_content = new_content.replace(f"{page}.html", page)
                
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                modified += 1
                print(f"Updated: {filepath}")

print(f"Total modified: {modified}")
