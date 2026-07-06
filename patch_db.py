import os

new_code = """const API_URL = '/api/api.php';

const DB = {
  get: (key) => { const d = localStorage.getItem('2dbazar_'+key); return d ? JSON.parse(d) : []; },
  set: (key, val) => {
    localStorage.setItem('2dbazar_'+key, JSON.stringify(val));
    fetch(API_URL + '?action=set&key=' + key, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(val)
    }).catch(e => console.error("Sync error:", e));
  },
  init: (key, fallback) => {
    if(!localStorage.getItem('2dbazar_'+key)) {
        localStorage.setItem('2dbazar_'+key, JSON.stringify(fallback));
        sessionStorage.setItem('needs_reload', 'true');
    }
  },
  reset: () => { localStorage.clear(); location.reload(); }
};

// Initial Sync from Live DB
function syncFromLiveDB() {
  fetch(API_URL + '?action=get_all')
    .then(r => r.json())
    .then(data => {
      if(data.status === 'success' && data.db) {
         let changed = false;
         for(const key in data.db) {
            const local = localStorage.getItem('2dbazar_'+key);
            const remote = JSON.stringify(data.db[key]);
            if(local !== remote) {
               localStorage.setItem('2dbazar_'+key, remote);
               changed = true;
            }
         }
         
         if (changed && sessionStorage.getItem('needs_reload')) {
             sessionStorage.removeItem('needs_reload');
             window.location.reload();
         }
      }
    }).catch(e => console.error("Sync error:", e));
}
syncFromLiveDB();"""

def patch_data_js(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # We need to replace the `const DB = { ... };` block with our `new_code`.
    # Let's find the start and end of the DB block.
    start = content.find('const DB = {')
    end = content.find('};', start) + 2
    
    if start != -1 and end != -1:
        updated_content = content[:start] + new_code + content[end:]
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        print(f"Patched {filepath}")
    else:
        print(f"Could not find DB block in {filepath}")

for root, _, files in os.walk('d:\\2dbazar'):
    for file in files:
        if file == 'data.js':
            patch_data_js(os.path.join(root, file))
