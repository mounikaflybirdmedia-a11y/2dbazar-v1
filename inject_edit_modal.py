import re
import os

filepath = r'd:\2dbazar\frontend\pages\admin.html'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Inject the Edit Modal HTML right before <script src="../js/data.js"></script>
modal_html = """
<!-- DYNAMIC EDIT MODAL -->
<div id="editModal" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,0.5);z-index:9999;align-items:center;justify-content:center;padding:16px;">
  <div class="card" style="padding:24px;width:100%;max-width:500px;max-height:90vh;overflow-y:auto;">
    <h2 id="editModalTitle" style="margin-bottom:16px;">Edit Item</h2>
    <div id="editModalBody"></div>
    <div style="display:flex;gap:10px;margin-top:20px;">
      <button class="btn btn-green" style="flex:1;" onclick="saveEdit()">Save Changes</button>
      <button class="btn btn-outline" style="flex:1;" onclick="closeEditModal()">Cancel</button>
    </div>
  </div>
</div>
"""
if 'id="editModal"' not in content:
    content = content.replace('<script src="../js/data.js"></script>', modal_html + '\n<script src="../js/data.js"></script>')

# 2. Replace the prompt-based edit functions with the new modal-based ones
# The old block is from `function editUser(id) {` down to `function editProp(id) { ... }`
# Wait, let's use Regex to replace them.
old_funcs_pattern = r'function editUser\(id\) \{.*?function renderServicesTable'
new_funcs = """
let currentEditType = '';
let currentEditId = '';

function closeEditModal() {
  document.getElementById('editModal').style.display = 'none';
}

function openEditModal(type, id, title) {
  currentEditType = type;
  currentEditId = id;
  const list = DB.get(type);
  const item = list.find(x => x.id === id);
  if (!item) return;

  document.getElementById('editModalTitle').textContent = title;
  
  let html = '';
  const excludeKeys = ['id', 'password', 'avatar']; 
  for (let key in item) {
    if (excludeKeys.includes(key)) continue;
    let val = item[key];
    if (val === null || val === undefined) val = '';
    
    let inputHtml = `<input type="text" id="edit_field_${key}" value="${val}" style="width:100%;padding:10px;border:1px solid #e2e8f0;border-radius:8px;margin-top:4px;font-family:inherit;"/>`;
    
    if (key === 'role') {
        inputHtml = `<select id="edit_field_${key}" style="width:100%;padding:10px;border:1px solid #e2e8f0;border-radius:8px;margin-top:4px;font-family:inherit;">
            <option value="admin" ${val==='admin'?'selected':''}>Admin</option>
            <option value="service_provider" ${val==='service_provider'?'selected':''}>Provider</option>
            <option value="service_receiver" ${val==='service_receiver'?'selected':''}>Customer</option>
            <option value="employer" ${val==='employer'?'selected':''}>Employer</option>
            <option value="job_seeker" ${val==='job_seeker'?'selected':''}>Job Seeker</option>
            <option value="seller" ${val==='seller'?'selected':''}>Seller</option>
            <option value="buyer" ${val==='buyer'?'selected':''}>Buyer</option>
        </select>`;
    } else if (key === 'approval_status') {
        inputHtml = `<select id="edit_field_${key}" style="width:100%;padding:10px;border:1px solid #e2e8f0;border-radius:8px;margin-top:4px;font-family:inherit;">
            <option value="Pending" ${val==='Pending'?'selected':''}>Pending</option>
            <option value="Approved" ${val==='Approved'?'selected':''}>Approved</option>
            <option value="Rejected" ${val==='Rejected'?'selected':''}>Rejected</option>
        </select>`;
    } else if (key === 'desc' || key === 'description') {
        inputHtml = `<textarea id="edit_field_${key}" style="width:100%;padding:10px;border:1px solid #e2e8f0;border-radius:8px;margin-top:4px;font-family:inherit;min-height:80px;">${val}</textarea>`;
    }

    html += `<div class="form-group" style="margin-bottom:12px;text-align:left;">
      <label style="font-size:13px;font-weight:600;text-transform:capitalize;color:#475569;">${key.replace(/_/g, ' ')}</label>
      ${inputHtml}
    </div>`;
  }

  document.getElementById('editModalBody').innerHTML = html;
  document.getElementById('editModal').style.display = 'flex';
}

function saveEdit() {
  const list = DB.get(currentEditType);
  const itemIndex = list.findIndex(x => x.id === currentEditId);
  if (itemIndex === -1) return;

  const item = list[itemIndex];
  const excludeKeys = ['id', 'password', 'avatar']; 
  for (let key in item) {
    if (excludeKeys.includes(key)) continue;
    const el = document.getElementById(`edit_field_${key}`);
    if (el) {
       if (typeof item[key] === 'number') {
           item[key] = Number(el.value) || 0;
       } else {
           item[key] = el.value;
       }
    }
  }

  DB.set(currentEditType, list);
  toast('Item updated successfully!');
  closeEditModal();
  
  if (currentEditType === 'users') { allUsers = DB.get('users'); filterUsers(); }
  if (currentEditType === 'services') renderServicesTable();
  if (currentEditType === 'jobs') renderJobsTable();
  if (currentEditType === 'products') renderProductsTable();
  if (currentEditType === 'properties') renderPropsTable();
  
  renderApprovals();
  init();
}

function editUser(id) { openEditModal('users', id, 'Edit User Details'); }
function editService(id) { openEditModal('services', id, 'Edit Service Details'); }
function editJob(id) { openEditModal('jobs', id, 'Edit Job Details'); }
function editProduct(id) { openEditModal('products', id, 'Edit Product Details'); }
function editProp(id) { openEditModal('properties', id, 'Edit Property Details'); }

function renderServicesTable"""

content = re.sub(old_funcs_pattern, new_funcs, content, flags=re.DOTALL)

# 3. Update editApprovalItem logic to not use prompt for service requests
old_approvals_pattern = r'else if \(type === \'service_requests\'\) \{.*?renderApprovals\(\);\s*\}'
new_approvals = """else if (type === 'service_requests') {
    openEditModal('service_requests', id, 'Edit Service Request');
  }
  else {
    renderApprovals();
  }
}
"""
content = re.sub(old_approvals_pattern, new_approvals, content, flags=re.DOTALL)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print('Dynamic Edit Modal injected successfully.')
