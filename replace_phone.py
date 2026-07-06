import os

target_dir = r"d:\2dbazar"

replacements = {
    "919999999999": "919885929818",
    "9999999999": "9885929818",
    "+91 99999 99999": "+91 98859 29818",
    "+91 9999999999": "+91 9885929818"
}

for root, dirs, files in os.walk(target_dir):
    for file in files:
        if file.endswith(".html") or file.endswith(".js"):
            file_path = os.path.join(root, file)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            new_content = content
            # apply replacements in order
            for old, new in replacements.items():
                new_content = new_content.replace(old, new)
            
            if new_content != content:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"Updated {file_path}")
