import os
import glob
import re

pages_dir = r'd:\2dbazar\frontend\pages'
html_files = glob.glob(os.path.join(pages_dir, '*.html'))
html_files.append(r'd:\2dbazar\index.html')

for f in html_files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # 4) Add location Vizag
    content = content.replace('<option>Vijayanagaram</option>', '<option>Vijayanagaram</option><option>Vizag</option>')
    
    # 2) Save profile logic
    if 'saveProfile()' in content and 'function saveProfile()' in content:
        save_logic = """function saveProfile(){
  const user = Auth.current();
  if(!user) return;
  const nameEl = document.getElementById('sName') || document.getElementById('bName') || document.getElementById('rName') || document.getElementById('cName');
  const phoneEl = document.getElementById('sPhone') || document.getElementById('bPhone') || document.getElementById('rPhone') || document.getElementById('cPhone');
  if(nameEl) user.name = nameEl.value;
  if(phoneEl) user.phone = phoneEl.value;
  const users = DB.get('users');
  const idx = users.findIndex(u => u.id === user.id);
  if(idx !== -1) { users[idx] = user; DB.set('users', users); }
  sessionStorage.setItem('2dbazar_current_user', JSON.stringify(user));
  if(typeof renderNav === 'function') renderNav();
  toast('Profile saved!');
}"""
        content = re.sub(r'function saveProfile\(\)\{.*?\}', save_logic, content, flags=re.DOTALL)
        
    # 3) Image upload logic
    if 'type="url"' in content and 'Img"' in content:
        # Find all inputs with type="url" and id="*Img"
        content = re.sub(r'(<input type="url" id="(\w+Img)".*?>)', r'\1 <input type="file" accept="image/*" style="margin-top:8px;font-size:12px;" onchange="const file=this.files[0];if(file){const reader=new FileReader();reader.onload=e=>document.getElementById(\'\2\').value=e.target.result;reader.readAsDataURL(file);}"/>', content)
        
    # 1) Admin Edit
    if 'admin.html' in f:
        # Add Edit buttons
        content = content.replace('onclick="deleteUser(\'${u.id}\')">Remove', 'onclick="editUser(\'${u.id}\')" style="margin-right:5px;">Edit</button><button class="btn btn-sm" style="background:#ef4444;color:#fff;" onclick="deleteUser(\'${u.id}\')">Remove')
        content = content.replace('onclick="deleteService(\'${s.id}\')">Remove', 'onclick="editService(\'${s.id}\')" style="margin-right:5px;">Edit</button><button class="btn btn-sm" style="background:#ef4444;color:#fff;" onclick="deleteService(\'${s.id}\')">Remove')
        content = content.replace('onclick="deleteJob(\'${j.id}\')">Remove', 'onclick="editJob(\'${j.id}\')" style="margin-right:5px;">Edit</button><button class="btn btn-sm" style="background:#ef4444;color:#fff;" onclick="deleteJob(\'${j.id}\')">Remove')
        content = content.replace('onclick="deleteProduct(\'${p.id}\')">Remove', 'onclick="editProduct(\'${p.id}\')" style="margin-right:5px;">Edit</button><button class="btn btn-sm" style="background:#ef4444;color:#fff;" onclick="deleteProduct(\'${p.id}\')">Remove')
        content = content.replace('onclick="deleteProp(\'${p.id}\')">Remove', 'onclick="editProp(\'${p.id}\')" style="margin-right:5px;">Edit</button><button class="btn btn-sm" style="background:#ef4444;color:#fff;" onclick="deleteProp(\'${p.id}\')">Remove')
        
        edit_funcs = """
function editUser(id) {
  const users = DB.get('users');
  const u = users.find(x => x.id === id);
  if(!u) return;
  const n = prompt('Edit User Name:', u.name);
  if(n) { u.name = n; DB.set('users', users); toast('User updated!'); renderUsers(); }
}
function editService(id) {
  const list = DB.get('services');
  const item = list.find(x => x.id === id);
  if(!item) return;
  const n = prompt('Edit Service Title:', item.title);
  if(n) { item.title = n; DB.set('services', list); toast('Service updated!'); renderServicesTable(); }
}
function editJob(id) {
  const list = DB.get('jobs');
  const item = list.find(x => x.id === id);
  if(!item) return;
  const n = prompt('Edit Job Title:', item.title);
  if(n) { item.title = n; DB.set('jobs', list); toast('Job updated!'); renderJobsTable(); }
}
function editProduct(id) {
  const list = DB.get('products');
  const item = list.find(x => x.id === id);
  if(!item) return;
  const n = prompt('Edit Product Name:', item.name);
  if(n) { item.name = n; DB.set('products', list); toast('Product updated!'); renderProductsTable(); }
}
function editProp(id) {
  const list = DB.get('properties');
  const item = list.find(x => x.id === id);
  if(!item) return;
  const n = prompt('Edit Property Title:', item.title);
  if(n) { item.title = n; DB.set('properties', list); toast('Property updated!'); renderPropsTable(); }
}
"""
        content = content.replace('function renderServicesTable(){', edit_funcs + 'function renderServicesTable(){')

    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)

print('Modifications complete.')
