import os

target_dir = r"d:\2dbazar"

replacements = {
    "919885929818": "919121600133",
    "9885929818": "9121600133",
    "+91 98859 29818": "+91 91216 00133",
    "+91 9885929818": "+91 9121600133",
    "info@2dbazaar.com": "2dbazaar.com@gmail.com",
    "info@2dbazar.com": "2dbazaar.com@gmail.com",
}

for root, dirs, files in os.walk(target_dir):
    for file in files:
        if file.endswith(".html") or file.endswith(".js"):
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                new_content = content
                for old, new in replacements.items():
                    new_content = new_content.replace(old, new)
                
                if new_content != content:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    print(f"Updated {file_path}")
            except Exception as e:
                pass
