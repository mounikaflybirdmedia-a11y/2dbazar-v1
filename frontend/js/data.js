// ============================================================
// 2DBazaar — MOCK DATA & GLOBAL STATE (localStorage backed)
// ============================================================

const API_URL = '/api/api.php';
const LEADS_URL = 'http://72.61.230.47/api/leads.php';

const DB = {
  get: (key) => { const d = localStorage.getItem('2dbazar_'+key); return d ? JSON.parse(d) : []; },
  set: (key, val) => {
    // Never write private session keys to localStorage or MySQL
    if (PRIVATE_KEYS.includes(key)) {
      sessionStorage.setItem('2dbazar_'+key, JSON.stringify(val));
      return;
    }
    localStorage.setItem('2dbazar_'+key, JSON.stringify(val));
    fetch(API_URL + '?action=set&key=' + key, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(val)
    }).catch(e => console.error("Sync error:", e));
  },
  init: (key, fallback) => {
    if(!localStorage.getItem('2dbazar_'+key)) {
        if(['services', 'jobs', 'products', 'properties'].includes(key)) {
            fallback = fallback.map(item => ({ approval_status: 'Approved', ...item }));
        }
        localStorage.setItem('2dbazar_'+key, JSON.stringify(fallback));
        sessionStorage.setItem('needs_reload', 'true');
    } else {
        if(['services', 'jobs', 'products', 'properties'].includes(key)) {
            try {
                let current = localStorage.getItem('2dbazar_'+key);
                let parsed = JSON.parse(current);
                let migrated = false;
                parsed = parsed.map(item => {
                    if(!item.approval_status) {
                        item.approval_status = 'Approved';
                        migrated = true;
                    }
                    return item;
                });
                if(migrated) {
                    localStorage.setItem('2dbazar_'+key, JSON.stringify(parsed));
                }
            } catch(e) { console.error(e); }
        }
    }
  },
  reset: () => { localStorage.clear(); location.reload(); }
};

// PRIVATE_KEYS: never synced to MySQL, never stored in shared localStorage
// current_user is per-tab via sessionStorage only
const PRIVATE_KEYS = ['current_user'];

// Force remove any legacy localStorage session to prevent persistent auto-login
localStorage.removeItem('2dbazar_current_user');

// Initial Sync from Live DB
function syncFromLiveDB() {
  fetch(API_URL + '?action=get_all')
    .then(r => r.json())
    .then(data => {
      if(data.status === 'success' && data.db) {
         for(const key in data.db) {
            if(PRIVATE_KEYS.includes(key)) continue; // NEVER touch session keys
            const local = localStorage.getItem('2dbazar_'+key);
            const remote = JSON.stringify(data.db[key]);
            if(local !== remote) {
               localStorage.setItem('2dbazar_'+key, remote);
               // NOTE: NO page reload here — reload breaks sessionStorage and logs users out
            }
         }
      }
    }).catch(e => console.error("Sync error:", e));
}
syncFromLiveDB();

// ── SEED DATA ──────────────────────────────────────────────

const SEED_SERVICES = [
  { id:'s1', category:'Plumbing', title:'Expert Plumber - Pipe & Tap Repair', price:300, unit:'hr', location:'Vijayanagaram', badge:'Top Rated', rating:4.8, reviews:124, provider:'Ravi Kumar', img:'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&q=80', status:'active' },
  { id:'s2', category:'Plumbing', title:'Emergency Leak Fixing', price:450, unit:'hr', location:'Vizianagaram', badge:'Popular', rating:4.6, reviews:89, provider:'Suresh Babu', img:'/assets/images/pipe_leak.png', status:'active' },
  { id:'s3', category:'Electrical', title:'Licensed Electrician - Wiring & Repair', price:400, unit:'hr', location:'Vijayanagaram', badge:'Verified', rating:4.9, reviews:210, provider:'Kiran Reddy', img:'https://images.unsplash.com/photo-1621905251189-08b45d6a269e?w=400&q=80', status:'active' },
  { id:'s4', category:'Electrical', title:'Inverter & Solar Panel Setup', price:350, unit:'hr', location:'Bobbili', badge:'Premium', rating:4.7, reviews:67, provider:'Naresh Varma', img:'https://images.unsplash.com/photo-1509391366360-2e959784a276?w=400&q=80', status:'active' },
  { id:'s5', category:'Carpentry', title:'Custom Furniture & Cabinet Maker', price:500, unit:'hr', location:'Vijayanagaram', badge:'Premium', rating:4.8, reviews:155, provider:'Venkat Rao', img:'/assets/images/cabinet_maker.png', status:'active' },
  { id:'s6', category:'Carpentry', title:'Door & Window Repair Specialist', price:250, unit:'hr', location:'Salur', badge:'Popular', rating:4.5, reviews:78, provider:'Prasad Babu', img:'/assets/images/door_window.png', status:'active' },
  { id:'s7', category:'Cleaning', title:'Deep Home Cleaning Service', price:800, unit:'day', location:'Vijayanagaram', badge:'Top Rated', rating:4.9, reviews:302, provider:'CleanPro Team', img:'https://images.unsplash.com/photo-1581578731548-c64695cc6952?w=400&q=80', status:'active' },
  { id:'s8', category:'Cleaning', title:'Sofa & Carpet Steam Cleaning', price:600, unit:'job', location:'Parvathipuram', badge:'Popular', rating:4.6, reviews:92, provider:'Fresh Home Services', img:'/assets/images/sofa_cleaning.png', status:'active' },
  { id:'s9', category:'Painting', title:'Interior Wall Painting (Per Room)', price:1200, unit:'room', location:'Vijayanagaram', badge:'Premium', rating:4.7, reviews:143, provider:'Color Masters', img:'https://images.unsplash.com/photo-1562259949-e8e7689d7828?w=400&q=80', status:'active' },
  { id:'s10', category:'Painting', title:'Exterior House Painting', price:15000, unit:'job', location:'Vizianagaram', badge:'Top Rated', rating:4.8, reviews:55, provider:'Bright Paints', img:'https://images.unsplash.com/photo-1589939705384-5185137a7f0f?w=400&q=80', status:'active' },
  { id:'s11', category:'AC Repair', title:'AC Service & Gas Refilling', price:550, unit:'job', location:'Vijayanagaram', badge:'Verified', rating:4.8, reviews:188, provider:'Cool Tech Services', img:'/assets/images/ac_service.png', status:'active' },
  { id:'s12', category:'AC Repair', title:'AC Installation & Uninstallation', price:800, unit:'job', location:'Bobbili', badge:'Popular', rating:4.5, reviews:76, provider:'Arctic Cool', img:'/assets/images/ac_installation.png', status:'active' },
  { id:'s13', category:'Appliance Repair', title:'Washing Machine Repair Expert', price:350, unit:'job', location:'Vijayanagaram', badge:'Verified', rating:4.7, reviews:134, provider:'Fix It Fast', img:'https://images.unsplash.com/photo-1626806787461-102c1bfaaea1?w=400&q=80', status:'active' },
  { id:'s14', category:'Appliance Repair', title:'Refrigerator & TV Repair', price:400, unit:'job', location:'Salur', badge:'Top Rated', rating:4.6, reviews:98, provider:'Home Fix Pro', img:'/assets/images/refrigerator_tv.png', status:'active' },
];

const SEED_JOBS = [
  { id:'j1', title:'Telecaller - Customer Support', company:'2DBazaar', salary:'₹12,000–15,000/mo', location:'Vijayanagaram', type:'Full Time', shift:'Morning', category:'Telecaller', posted:'2 days ago', perks:['PF','ESI','Incentives'], skills:['Communication','Hindi/Telugu'], openings:5 },
  { id:'j2', title:'Web Developer - React & Node.js', company:'TechSoft Solutions', salary:'₹25,000–40,000/mo', location:'Vizianagaram', type:'Full Time', shift:'Day', category:'IT/Developer', posted:'1 day ago', perks:['Remote','Health Insurance','Bonus'], skills:['React','Node.js','MongoDB'], openings:2 },
  { id:'j3', title:'Office Admin Assistant', company:'Sri Sai Enterprises', salary:'₹10,000–13,000/mo', location:'Vijayanagaram', type:'Full Time', shift:'Day', category:'Admin', posted:'3 days ago', perks:['PF','Lunch'], skills:['MS Office','Communication'], openings:3 },
  { id:'j4', title:'Housekeeping Staff - Hotel', company:'Hotel Vijaya Grand', salary:'₹8,000–10,000/mo', location:'Vijayanagaram', type:'Full Time', shift:'Rotational', category:'Housekeeping', posted:'Today', perks:['Accommodation','Meals'], skills:['Cleaning','Discipline'], openings:8 },
  { id:'j5', title:'Staff Nurse - ICU', company:'District General Hospital', salary:'₹18,000–25,000/mo', location:'Vizianagaram', type:'Full Time', shift:'Rotational', category:'Nursing', posted:'Today', perks:['PF','ESI','Bonus'], skills:['ICU Care','B.Sc Nursing'], openings:4 },
  { id:'j6', title:'Restaurant Manager', company:'Spice Garden Restaurant', salary:'₹20,000–28,000/mo', location:'Vijayanagaram', type:'Full Time', shift:'Day', category:'Manager', posted:'2 days ago', perks:['Meals','PF','Incentives'], skills:['Team Management','Customer Service'], openings:1 },
  { id:'j7', title:'Head Chef - Multi Cuisine', company:'Royal Kitchen', salary:'₹22,000–35,000/mo', location:'Bobbili', type:'Full Time', shift:'Morning', category:'Chef', posted:'4 days ago', perks:['Accommodation','Meals','Bonus'], skills:['Indian/Chinese Cuisine','Kitchen Management'], openings:1 },
  { id:'j8', title:'Security Guard', company:'SafeGuard Services', salary:'₹9,000–11,000/mo', location:'Salur', type:'Full Time', shift:'Night', category:'Security', posted:'Today', perks:['Uniform','PF'], skills:['Discipline','Physical Fitness'], openings:10 },
];

const SEED_PRODUCTS = [
  { id:'p1', category:'Mobiles', name:'Samsung Galaxy S23 - 256GB', price:45000, location:'Vijayanagaram', condition:'Used', age:'6 months', img:'https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?w=400&q=80', seller:'Arun K', contact:'9876543210' },
  { id:'p2', category:'Mobiles', name:'iPhone 13 - 128GB Space Grey', price:52000, location:'Vizianagaram', condition:'Used', age:'1 year', img:'https://images.unsplash.com/photo-1512054502232-10a0a035d672?w=400&q=80', seller:'Priya S', contact:'9123456780' },
  { id:'p3', category:'Electronics', name:'LG 43" 4K Smart TV', price:28000, location:'Vijayanagaram', condition:'Used', age:'2 years', img:'https://images.unsplash.com/photo-1461151304267-38535e780c79?w=400&q=80', seller:'Ravi M', contact:'9988776655' },
  { id:'p4', category:'Electronics', name:'Dell Laptop i5 8GB RAM', price:32000, location:'Bobbili', condition:'Used', age:'1.5 years', img:'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400&q=80', seller:'Suresh L', contact:'9876512345' },
  { id:'p5', category:'Cars', name:'Maruti Swift VXI 2020 - 35000 km', price:550000, location:'Vijayanagaram', condition:'Used', age:'4 years', img:'https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=400&q=80', seller:'Naresh B', contact:'9999888877' },
  { id:'p6', category:'Cars', name:'Hyundai i20 Sportz 2019', price:620000, location:'Vizianagaram', condition:'Used', age:'5 years', img:'https://images.unsplash.com/photo-1542362567-b07e54358753?w=400&q=80', seller:'Kiran R', contact:'9876500001' },
  { id:'p7', category:'Bikes', name:'Royal Enfield Bullet 350 - 2021', price:155000, location:'Vijayanagaram', condition:'Used', age:'3 years', img:'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&q=80', seller:'Venkat P', contact:'9988001122' },
  { id:'p8', category:'Bikes', name:'Honda Activa 6G - 2022', price:68000, location:'Salur', condition:'Used', age:'2 years', img:'https://images.unsplash.com/photo-1449426468159-d96dbf08f19f?w=400&q=80', seller:'Lakshmi V', contact:'9876543999' },
  { id:'p9', category:'Furniture', name:'Teak Wood Sofa Set (3+1+1)', price:18000, location:'Vijayanagaram', condition:'Used', age:'3 years', img:'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=400&q=80', seller:'Ramesh D', contact:'9900112233' },
  { id:'p10', category:'Home Appliances', name:'Samsung 7.5kg Washing Machine', price:14000, location:'Parvathipuram', condition:'Used', age:'2 years', img:'https://images.unsplash.com/photo-1626806787461-102c1bfaaea1?w=400&q=80', seller:'Anjali K', contact:'9876001234' },
];

const SEED_PROPERTIES = [
  { id:'pr1', type:'House', title:'2 BHK Independent House', area:'900 sqft', price:3500000, location:'Vijayanagaram', facing:'East', floors:1, parking:true, img:'https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=400&q=80', owner:'T. Ramaiah', contact:'9876543210' },
  { id:'pr2', type:'Apartment', title:'3 BHK Flat - Gated Community', area:'1350 sqft', price:5200000, location:'Vijayanagaram', facing:'West', floors:4, parking:true, img:'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=400&q=80', owner:'Sri Sai Builders', contact:'9876500000' },
  { id:'pr3', type:'Plot', title:'200 Sq Yd Plot - DTCP Approved', area:'200 sqyd', price:1800000, location:'Vizianagaram', facing:'North', floors:0, parking:false, img:'https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=400&q=80', owner:'N. Babu Rao', contact:'9988776655' },
  { id:'pr4', type:'House', title:'Independent Villa with Garden', area:'2200 sqft', price:8500000, location:'Vijayanagaram', facing:'East', floors:2, parking:true, img:'https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=400&q=80', owner:'K. Venkata Rao', contact:'9876512345' },
  { id:'pr5', type:'Plot', title:'100 Sq Yd Corner Plot', area:'100 sqyd', price:950000, location:'Bobbili', facing:'North-East', floors:0, parking:false, img:'https://images.unsplash.com/photo-1416331108676-a22ccb276e35?w=400&q=80', owner:'B. Nageswara Rao', contact:'9999888877' },
  { id:'pr6', type:'Apartment', title:'2 BHK Ready-to-Move Flat', area:'1050 sqft', price:3200000, location:'Salur', facing:'South', floors:2, parking:true, img:'https://images.unsplash.com/photo-1493809842364-78817add7ffb?w=400&q=80', owner:'Urban Homes Pvt Ltd', contact:'9900112233' },
];

// ── USERS SEED ──────────────────────────────────────────────
const SEED_USERS = [
  { id:'u1', name:'Admin User', email:'admin@2dbazar.com', password:'admin123', role:'admin.html', phone:'9121600133', location:'Vijayanagaram', avatar:'A' },
  { id:'u2', name:'Ravi Provider', email:'provider@2dbazar.com', password:'test123', role:'service_provider', phone:'9876543210', location:'Vijayanagaram', avatar:'R', category:'Plumbing', experience:5, rate:300 },
  { id:'u3', name:'Priya Customer', email:'customer@2dbazar.com', password:'test123', role:'service_receiver', phone:'9876543211', location:'Vijayanagaram', avatar:'P' },
  { id:'u4', name:'TechCorp HR', email:'employer@2dbazar.com', password:'test123', role:'employer', phone:'9876543212', location:'Vizianagaram', company:'TechCorp', avatar:'T' },
  { id:'u5', name:'Arjun Seeker', email:'seeker@2dbazar.com', password:'test123', role:'job_seeker', phone:'9876543213', location:'Vijayanagaram', avatar:'A', skills:['React','Node.js'] },
  { id:'u6', name:'Seller Sam', email:'seller@2dbazar.com', password:'test123', role:'seller', phone:'9876543214', location:'Vijayanagaram', avatar:'S' },
  { id:'u7', name:'Buyer Bala', email:'buyer@2dbazar.com', password:'test123', role:'buyer', phone:'9876543215', location:'Vijayanagaram', avatar:'B' },
];

const SEED_SERVICE_REQUESTS = [
  { id: 'req1', service: 'Plumbing', desc: 'Need fixing for a leaking tap', budget: '300', location: 'Vijayanagaram', date: '2026-05-21', userId: 'u3', status: 'Open', ts: Date.now() - 86400000 },
  { id: 'req2', service: 'Electrical', desc: 'Ceiling fan installation', budget: '500', location: 'Vizianagaram', date: '2026-05-22', userId: 'u7', status: 'Accepted', ts: Date.now() - 172800000 },
];

const SEED_JOB_APPLICATIONS = [
  { id: 'app1', jobTitle: 'Telecaller - Customer Support', applicantName: 'Arjun Seeker', employerName: '2DBazaar', status: 'Applied', ts: Date.now() - 40000000 },
  { id: 'app2', jobTitle: 'Office Admin Assistant', applicantName: 'Sita Rani', employerName: 'Sri Sai Enterprises', status: 'Under Review', ts: Date.now() - 86400000 },
];

const SEED_ORDERS = [
  { id: 'ORD-1001', date: new Date(Date.now() - 10000000).toLocaleDateString(), userId: 'u7', total: 45000, payment: 'Cash on Delivery', status: 'Pending', items: [{name: 'Samsung Galaxy S23', price: 45000}] },
  { id: 'ORD-1002', date: new Date(Date.now() - 50000000).toLocaleDateString(), userId: 'u7', total: 32000, payment: 'Paid Online', status: 'Delivered', items: [{name: 'Dell Laptop i5', price: 32000}] },
];

// ── INIT DB ─────────────────────────────────────────────────
DB.init('services', SEED_SERVICES);
DB.init('jobs', SEED_JOBS);
DB.init('products', SEED_PRODUCTS);
DB.init('properties', SEED_PROPERTIES);
DB.init('users', SEED_USERS);
DB.init('service_requests', SEED_SERVICE_REQUESTS);
DB.init('job_applications', SEED_JOB_APPLICATIONS);
DB.init('orders', SEED_ORDERS);
DB.init('property_inquiries', []);
DB.init('offers', []);
DB.init('wishlist', []);

// Repair corrupted u4/u2 user data in localStorage if mutated during development tab-mixing
try {
  let storedUsers = localStorage.getItem('2dbazar_users');
  if (storedUsers) {
    let parsedUsers = JSON.parse(storedUsers);
    let modified = false;
    parsedUsers = parsedUsers.map(u => {
      if (u.id === 'u4' && u.email === 'employer@2dbazar.com' && (u.name === 'Ravi Provider' || u.phone === '9876543210')) {
        u.name = 'TechCorp HR';
        u.phone = '9876543212';
        u.location = 'Vizianagaram';
        u.company = 'TechCorp';
        u.avatar = 'T';
        delete u.category;
        delete u.rate;
        delete u.experience;
        delete u.skills;
        delete u.address;
        delete u.bio;
        modified = true;
      }
      return u;
    });
    if (modified) {
      localStorage.setItem('2dbazar_users', JSON.stringify(parsedUsers));
      // Reset any active session that might be corrupted
      const curr = sessionStorage.getItem('2dbazar_current_user');
      if (curr) {
        const parsedCurr = JSON.parse(curr);
        if (parsedCurr.id === 'u4' && parsedCurr.name === 'Ravi Provider') {
          sessionStorage.removeItem('2dbazar_current_user');
        }
      }
    }
  }
} catch (e) {
  console.error("Migration repair error:", e);
}

// ── AUTH HELPERS ─────────────────────────────────────────────
// SESSION DESIGN:
//   sessionStorage → per-tab isolated (each browser tab = independent user)
//   PRIVATE_KEYS   → 'current_user' never synced to MySQL
//
//   Tab 1: Ravi logged in  → Tab 1 sessionStorage = Ravi
//   Tab 2: TechCorp logged in → Tab 2 sessionStorage = TechCorp
//   Refresh Tab 1 → still Ravi ✅  |  Refresh Tab 2 → still TechCorp ✅
//   NO cross-tab contamination ✅
const Auth = {
  login(email, password) {
    const users = DB.get('users');
    const user = users.find(u => u.email === email && u.password === password);
    if (user) {
      sessionStorage.setItem('2dbazar_current_user', JSON.stringify(user));
      return user;
    }
    return null;
  },
  logout() {
    sessionStorage.removeItem('2dbazar_current_user');
  },
  current() {
    let d = sessionStorage.getItem('2dbazar_current_user');
    return d ? JSON.parse(d) : null;
  },
  signup(data) {
    const users = DB.get('users');
    if (users.find(u => u.email === data.email)) return { error: 'Email already exists' };
    const newUser = { ...data, id: 'u' + Date.now(), avatar: data.name[0].toUpperCase() };
    users.push(newUser);
    DB.set('users', users);
    sessionStorage.setItem('2dbazar_current_user', JSON.stringify(newUser));
    return newUser;
  },
  isAdmin() { const u = this.current(); return u && u.role === 'admin'; }
};



// ── UTILITY HELPERS ──────────────────────────────────────────
function formatPrice(p) {
  if (p >= 100000) return '₹' + (p/100000).toFixed(1) + ' L';
  if (p >= 1000) return '₹' + (p/1000).toFixed(0) + 'K';
  return '₹' + p;
}
function timeAgo(ts) {
  const d = Math.floor((Date.now() - ts) / 60000);
  if (d < 1) return 'Just now';
  if (d < 60) return d + ' mins ago';
  if (d < 1440) return Math.floor(d/60) + ' hrs ago';
  return Math.floor(d/1440) + ' days ago';
}
function stars(n) { return '★'.repeat(Math.floor(n)) + '☆'.repeat(5 - Math.floor(n)); }
function toast(msg, type='success') {
  const t = document.createElement('div');
  t.className = 'toast toast-' + type;
  t.textContent = msg;
  t.style.cssText = `position:fixed;bottom:90px;right:20px;background:${type==='success'?'#25D366':'#ef4444'};color:#fff;padding:12px 24px;border-radius:10px;font-family:Poppins,sans-serif;font-weight:600;font-size:14px;z-index:9999;box-shadow:0 4px 20px rgba(0,0,0,0.2);animation:slideUp 0.3s ease;`;
  document.body.appendChild(t);
  setTimeout(() => t.remove(), 3000);
}
function getListingContact(item, type) {
  if (!item) return '9121600133';
  if (item.contact) return item.contact;
  if (item.phone) return item.phone;
  if (item.provider_phone) return item.provider_phone;
  
  const users = DB.get('users') || [];
  const clean = (val) => (val || '').toLowerCase().trim();
  
  const findByName = (name) => {
    if (!name) return null;
    const n = clean(name);
    let u = users.find(x => clean(x.name) === n);
    if (u) return u;
    u = users.find(x => clean(x.name).includes(n) || n.includes(clean(x.name)));
    if (u) return u;
    const first = n.split(/\s+/)[0];
    if (first && first.length > 2) {
      u = users.find(x => clean(x.name).split(/\s+/)[0] === first);
      if (u) return u;
    }
    return null;
  };

  if (type === 'services') {
    const u = findByName(item.provider);
    if (u && u.phone) return u.phone;
    const prov = users.find(x => x.role === 'service_provider');
    if (prov && prov.phone) return prov.phone;
    return '9876543210';
  }
  if (type === 'jobs') {
    const c = clean(item.company);
    let u = users.find(x => clean(x.company) === c || clean(x.name) === c);
    if (u && u.phone) return u.phone;
    u = users.find(x => clean(x.company).includes(c) || c.includes(clean(x.company)));
    if (u && u.phone) return u.phone;
    const emp = users.find(x => x.role === 'employer');
    if (emp && emp.phone) return emp.phone;
    return '9876543212';
  }
  if (type === 'products') {
    const u = findByName(item.seller);
    if (u && u.phone) return u.phone;
    const sel = users.find(x => x.role === 'seller');
    if (sel && sel.phone) return sel.phone;
    return '9876543214';
  }
  if (type === 'properties') {
    const u = findByName(item.owner);
    if (u && u.phone) return u.phone;
    const sel = users.find(x => x.role === 'seller');
    if (sel && sel.phone) return sel.phone;
    return '9876543214';
  }
  return '9121600133';
}

function formatWANumber(phone) {
  if (!phone) return '919121600133';
  let clean = phone.toString().replace(/\D/g, '');
  if (clean.length === 10) {
    return '91' + clean;
  }
  return clean;
}

function openWA(phone='919121600133', msg='Hello! I found your listing on 2DBazaar.') {
  window.open(`https://wa.me/${phone}?text=${encodeURIComponent(msg)}`, '_blank');
}
function waService(id) {
  const s = DB.get('services').find(x=>x.id===id);
  if(!s) return;
  const msg = `Hello!\nI found your service on *2DBazaar*.\n\n*Service*: ${s.title}\n*Price*: ₹${s.price}/${s.unit}\n*Location*: ${s.location}\n\nCan you please confirm your availability?`;
  const num = formatWANumber(getListingContact(s, 'services'));
  openWA(num, msg);
}
function waProduct(id) {
  const p = DB.get('products').find(x=>x.id===id);
  if(!p) return;
  const msg = `Hello!\nI am interested in your product listed on *2DBazaar*.\n\n*Product*: ${p.name}\n*Price*: ${formatPrice(p.price)}\n*Condition*: ${p.condition}\n*Location*: ${p.location}\n\nIs it still available?`;
  const num = formatWANumber(getListingContact(p, 'products'));
  openWA(num, msg);
}
function waJob(id) {
  const j = DB.get('jobs').find(x=>x.id===id);
  if(!j) return;
  const msg = `Hello!\nI am inquiring about the job opening on *2DBazaar*.\n\n*Role*: ${j.title}\n*Company*: ${j.company}\n*Salary*: ${j.salary}\n*Location*: ${j.location}\n\nI would like to apply for this position. Please let me know the next steps.`;
  const num = formatWANumber(getListingContact(j, 'jobs'));
  openWA(num, msg);
}
function waProperty(id) {
  const pr = DB.get('properties').find(x=>x.id===id);
  if(!pr) return;

  const user = Auth.current();
  const lead = {
    id: 'INQ-' + Date.now(),
    propertyTitle: pr.title,
    propertyId: pr.id,
    userName: user ? user.name : 'Guest',
    userPhone: user ? (user.phone || '') : '',
    userMessage: '',
    date: new Date().toLocaleDateString('en-IN'),
    ts: Date.now(),
    status: 'Properties Selected'
  };

  // Save to MySQL via PHP API (visible to admin across all devices)
  fetch(LEADS_URL + '?action=add_lead', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(lead)
  }).then(r => r.json())
    .then(res => console.log('Lead saved to DB:', res))
    .catch(e => console.error('Lead save error:', e));

  // Also keep in localStorage as fallback
  const inqs = DB.get('property_inquiries') || [];
  inqs.unshift(lead);
  localStorage.setItem('2dbazar_property_inquiries', JSON.stringify(inqs));

  const msg = `Hello!\nI saw your property listing on *2DBazaar*.\n\n*Property*: ${pr.title}\n*Price*: ${formatPrice(pr.price)}\n*Area*: ${pr.area}\n*Location*: ${pr.location}\n\nI'd like to schedule a visit or get more details.`;
  const num = formatWANumber(getListingContact(pr, 'properties'));
  openWA(num, msg);
}
function guardAuth(requiredRole) {
  const user = Auth.current();
  if (!user) {
    if (requiredRole === 'admin') {
      window.location.href = 'admin-login.html';
    } else {
      window.location.href = 'login.html';
    }
    return false;
  }
  if (user.role === 'admin') return true;
  if (requiredRole && user.role !== requiredRole) {
    const dashMap = {
      admin: 'admin',
      service_provider: 'dashboard-provider',
      service_receiver: 'dashboard-receiver',
      employer: 'dashboard-employer',
      job_seeker: 'dashboard-seeker',
      seller: 'dashboard-seller',
      buyer: 'dashboard-buyer'
    };
    const dest = dashMap[user.role] ? dashMap[user.role] + '.html' : '../index.html';
    const currentPage = window.location.pathname.split('/').pop();
    if (currentPage !== dest) {
      window.location.href = dest;
    }
    return false;
  }
  return true;
}

function toggleMobileNav() {
  const nl = document.getElementById('navLinks');
  if (nl) {
    nl.style.display = nl.style.display === 'flex' ? 'none' : 'flex';
    nl.style.flexDirection = 'column';
    nl.style.position = 'absolute';
    nl.style.top = '68px'; 
    nl.style.left = '0'; 
    nl.style.right = '0';
    nl.style.background = '#fff'; 
    nl.style.padding = '10px'; 
    nl.style.boxShadow = '0 4px 10px rgba(0,0,0,0.1)';
    nl.style.zIndex = '999';
  } else {
    const sidebar = document.querySelector('.sidebar');
    if (sidebar) {
      sidebar.classList.toggle('open');
    }
  }
}

// Close sidebar on mobile when clicking outside or on a sidebar item
document.addEventListener('DOMContentLoaded', () => {
  document.addEventListener('click', (e) => {
    const sidebar = document.querySelector('.sidebar');
    if (sidebar && sidebar.classList.contains('open')) {
      const menuBtn = document.querySelector('.nav-menu-btn');
      if (!sidebar.contains(e.target) && (!menuBtn || !menuBtn.contains(e.target))) {
        sidebar.classList.remove('open');
      }
    }
  });

  document.addEventListener('click', (e) => {
    if (e.target.closest('.sidebar-item')) {
      const sidebar = document.querySelector('.sidebar');
      if (sidebar && sidebar.classList.contains('open')) {
        sidebar.classList.remove('open');
      }
    }
  });
});

// Unified global navigation render
function renderNav() {
  const user = Auth.current();
  const el = document.getElementById('navActions');
  if (!el) return;

  const isPages = window.location.pathname.includes('/pages/');
  const rootPrefix = isPages ? '../' : '';

  if (user) {
    const dashMap = {
      admin: 'admin',
      service_provider: 'dashboard-provider',
      service_receiver: 'dashboard-receiver',
      employer: 'dashboard-employer',
      job_seeker: 'dashboard-seeker',
      seller: 'dashboard-seller',
      buyer: 'dashboard-buyer'
    };
    const dash = dashMap[user.role] || 'index';
    
    let dashLink;
    if (dash === 'index') {
      dashLink = isPages ? '../index.html' : 'index.html';
    } else {
      dashLink = isPages ? dash + '.html' : 'pages/' + dash + '.html';
    }

    const userNameFull = user.name || user.email || 'User';
    const userNameFirst = userNameFull.split(' ')[0];
    const userAvatarChar = user.avatar || userNameFull.charAt(0).toUpperCase();

    el.innerHTML = `
      <div id="userMenu" style="position:relative; display:inline-block;">
        <button onclick="toggleUserDropdown(event)" class="btn btn-sm" id="userBtn" style="background:#f1f5f9; display:flex; align-items:center; gap:8px; border:1px solid #e2e8f0; border-radius:6px; cursor:pointer; font-family:inherit; padding: 6px 12px;">
          <span id="userAvatar" style="background:#25D366;color:#fff;width:28px;height:28px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:13px;">
            ${userAvatarChar}
          </span>
          <span id="userName" style="font-weight:500;color:#1e293b;font-family:inherit;">${userNameFirst}</span> ▾
        </button>
        <div id="userDropdown" class="hidden" style="position:absolute;right:0;top:44px;background:#fff;border-radius:10px;box-shadow:0 8px 30px rgba(0,0,0,0.15);min-width:180px;z-index:999;overflow:hidden;border:1px solid #e2e8f0;">
          <a href="${dashLink}" style="display:block;padding:12px 16px;font-size:14px;font-weight:500;color:#334155;text-decoration:none;border-bottom:1px solid #f1f5f9;font-family:inherit;">⚡ Dashboard</a>
          <a href="${dashLink}?tab=profile" style="display:block;padding:12px 16px;font-size:14px;font-weight:500;color:#334155;text-decoration:none;border-bottom:1px solid #f1f5f9;font-family:inherit;">👤 Profile</a>
          <button onclick="Auth.logout(); window.location.href='${rootPrefix}index.html'; return false;" style="display:block;width:100%;text-align:left;padding:12px 16px;font-size:14px;font-weight:500;background:none;border:none;cursor:pointer;font-family:inherit;color:#ef4444;">🚪 Logout</button>
        </div>
      </div>
    `;
  } else {
    const loginLink = isPages ? 'login.html' : 'pages/login.html';
    const signupLink = isPages ? 'signup.html' : 'pages/signup.html';
    el.innerHTML = `
      <a href="${loginLink}" class="btn btn-outline btn-sm" id="loginBtn" style="margin-right:8px;font-family:inherit;">Login</a>
      <a href="${signupLink}" class="btn btn-green btn-sm" id="signupBtn" ${!isPages ? 'onclick="showPostDisclaimer(event)"' : ''} style="font-family:inherit;">Post Free Ad</a>
    `;
  }
}

function toggleUserDropdown(event) {
  if (event) event.stopPropagation();
  const dd = document.getElementById('userDropdown');
  if (dd) dd.classList.toggle('hidden');
}

window.renderNav = renderNav;
window.toggleUserDropdown = toggleUserDropdown;

// Close dropdown when clicking outside
document.addEventListener('click', (e) => {
  const dd = document.getElementById('userDropdown');
  if (dd && !e.target.closest('#userMenu')) {
    dd.classList.add('hidden');
  }
});

// Run renderNav once DOM is parsed
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', renderNav);
} else {
  renderNav();
}
