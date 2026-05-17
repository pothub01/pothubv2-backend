/* ═══════════════════════════════════════════════
   POTHUB — app.js  (core shared across all pages)
═══════════════════════════════════════════════ */

/* ── PRODUCTS ── */
let PRODUCTS = [];
const API_BASE = '/api';

async function loadProducts() {
  try {
    const r = await fetch(`${API_BASE}/products`);
    const data = await r.json();
    PRODUCTS = data.products || [];
  } catch (e) {
    console.warn('API unavailable, using local products');
    PRODUCTS = getLocalProducts();
  }
  return PRODUCTS;
}

// API helper functions
async function apiGet(endpoint) {
  try {
    const r = await fetch(`${API_BASE}${endpoint}`);
    if (!r.ok) throw new Error(`HTTP ${r.status}`);
    return await r.json();
  } catch (e) {
    console.error('API error:', e);
    return null;
  }
}

async function apiPost(endpoint, data) {
  try {
    const r = await fetch(`${API_BASE}${endpoint}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    if (!r.ok) throw new Error(`HTTP ${r.status}`);
    return await r.json();
  } catch (e) {
    console.error('API error:', e);
    return null;
  }
}

function getLocalProducts() {
  return [
    { id:1, name:'Nordic Ceramic Pot', price:849, original:1099, category:'ceramic', tags:['indoor','bestseller'], rating:4.8, reviews:124, stock:15, sku:'PH-001', icon:'🏺', badge:'Bestseller', desc:'Handcrafted in Scandinavia. Matte finish with drainage hole.', colors:['White','Sand','Charcoal'], sizes:['Small','Medium','Large'] },
    { id:2, name:'TerraGlow Clay Planter', price:649, original:null, category:'terracotta', tags:['outdoor','new'], rating:4.6, reviews:87, stock:22, sku:'PH-002', icon:'🪴', badge:'New', desc:'Sun-baked terracotta with natural earth tone finish.', colors:['Terra','Rust','Natural'], sizes:['Small','Medium','Large','XL'] },
    { id:3, name:'Hanging Ivy Basket', price:549, original:null, category:'hanging', tags:['hanging','trending'], rating:4.7, reviews:203, stock:8, sku:'PH-003', icon:'🌿', badge:'Trending', desc:'Woven macramé hanging basket with ceramic insert.', colors:['Natural','White','Black'], sizes:['Small','Large'] },
    { id:4, name:'Concrete Urban Planter', price:1299, original:null, category:'concrete', tags:['outdoor','premium'], rating:4.9, reviews:56, stock:5, sku:'PH-004', icon:'🪨', badge:'Premium', desc:'Raw concrete aesthetic for the modern urban home.', colors:['Grey','Dark','White'], sizes:['Medium','Large','XL'] },
    { id:5, name:'Matte Black Succulent Pot', price:449, original:599, category:'ceramic', tags:['indoor','sale'], rating:4.5, reviews:312, stock:30, sku:'PH-005', icon:'⚫', badge:'Sale', desc:'Sleek matte black glaze with a modern cylindrical form.', colors:['Black','Matte Grey'], sizes:['XS','Small','Medium'] },
    { id:6, name:'Scandinavian Oak Planter', price:1599, original:null, category:'luxury', tags:['indoor','luxury'], rating:5.0, reviews:28, stock:3, sku:'PH-006', icon:'🌳', badge:'Luxury', desc:'Oak wood planter with hidden drainage tray.', colors:['Natural Oak','Walnut','Ash'], sizes:['Medium','Large'] },
    { id:7, name:'Golden Rim Luxury Pot', price:2199, original:null, category:'luxury', tags:['indoor','luxury','new'], rating:4.9, reviews:19, stock:7, sku:'PH-007', icon:'✨', badge:'New', desc:'Porcelain pot with hand-painted 24k gold rim.', colors:['White-Gold','Black-Gold'], sizes:['Small','Medium'] },
    { id:8, name:'Marble Luxe Planter', price:1899, original:2399, category:'luxury', tags:['indoor','sale'], rating:4.7, reviews:44, stock:12, sku:'PH-008', icon:'🤍', badge:'Sale', desc:'Italian Carrara marble planter.', colors:['White Marble','Grey Marble'], sizes:['Small','Medium','Large'] },
    { id:9, name:'Eco Bamboo Pot', price:399, original:null, category:'eco', tags:['outdoor','eco'], rating:4.4, reviews:167, stock:45, sku:'PH-009', icon:'🎋', badge:null, desc:'100% biodegradable bamboo fiber pot.', colors:['Natural','Green','Brown'], sizes:['Small','Medium','Large'] },
    { id:10, name:'Vertical Wall Planter', price:749, original:null, category:'hanging', tags:['outdoor','trending'], rating:4.6, reviews:89, stock:18, sku:'PH-010', icon:'🧱', badge:'Trending', desc:'Modular wall-mounted planter system.', colors:['White','Black','Grey'], sizes:['Single','Triple','5-Pack'] },
    { id:11, name:'Rustic Stone Pot', price:999, original:null, category:'concrete', tags:['outdoor','rustic'], rating:4.5, reviews:73, stock:9, sku:'PH-011', icon:'⛰️', badge:null, desc:'Hand-carved stone-finish planter.', colors:['Stone','Slate','Sandstone'], sizes:['Medium','Large','XL'] },
    { id:12, name:'Minimal White Cylinder', price:599, original:null, category:'ceramic', tags:['indoor','minimal'], rating:4.8, reviews:241, stock:28, sku:'PH-012', icon:'⬜', badge:'Bestseller', desc:'Pure white glazed cylinder. Timeless form.', colors:['White','Off-White'], sizes:['XS','Small','Medium','Large'] },
    { id:13, name:'Pebble Texture Planter', price:699, original:null, category:'ceramic', tags:['indoor','textured'], rating:4.6, reviews:58, stock:16, sku:'PH-013', icon:'🫙', badge:null, desc:'Pebble-embossed surface texture. Matte glaze.', colors:['Sand','Sage','Blush'], sizes:['Small','Medium'] },
    { id:14, name:'Modern Arch Vase', price:1199, original:null, category:'luxury', tags:['indoor','designer'], rating:4.9, reviews:35, stock:6, sku:'PH-014', icon:'🫙', badge:'Designer', desc:'Award-winning arch silhouette.', colors:['Clay','Cream','Forest'], sizes:['Medium','Tall'] },
    { id:15, name:'Sage Indoor Pot Set', price:1099, original:1399, category:'ceramic', tags:['indoor','set','sale'], rating:4.7, reviews:148, stock:20, sku:'PH-015', icon:'🌱', badge:'Set', desc:'Set of 3 graduated sage-green ceramic pots.', colors:['Sage','Forest','Moss'], sizes:['Set of 3'] },
  ];
}

/* ── CART ── */
let cart = JSON.parse(localStorage.getItem('pothub_cart') || '[]');

function saveCart() { localStorage.setItem('pothub_cart', JSON.stringify(cart)); updateCartBadge(); }

function addToCart(id, qty = 1, color = '', size = '') {
  const product = PRODUCTS.find(p => p.id === id);
  if (!product) return;
  const key = `${id}-${color}-${size}`;
  const existing = cart.find(i => i.key === key);
  if (existing) existing.qty += qty;
  else cart.push({ ...product, qty, color, size, key });
  saveCart();
  showToast(`<span class="toast-icon">${product.icon}</span> "${product.name}" added to cart`, 'success');
  updateCartBadge();
  renderCartDrawer();
}

function removeFromCart(key) {
  cart = cart.filter(i => i.key !== key);
  saveCart();
  renderCartDrawer();
}

function updateQty(key, delta) {
  const item = cart.find(i => i.key === key);
  if (!item) return;
  item.qty = Math.max(1, item.qty + delta);
  saveCart();
  renderCartDrawer();
}

function getCartTotal() { return cart.reduce((s, i) => s + i.price * i.qty, 0); }
function getCartCount() { return cart.reduce((s, i) => s + i.qty, 0); }

function updateCartBadge() {
  document.querySelectorAll('.cart-count').forEach(el => el.textContent = getCartCount());
}

function renderCartDrawer() {
  const body = document.getElementById('drawer-body');
  if (!body) return;
  if (!cart.length) {
    body.innerHTML = `<div class="drawer-empty"><div class="drawer-empty-icon">🪴</div><p>Your cart is empty</p></div>`;
  } else {
    body.innerHTML = cart.map(item => `
      <div class="cart-item-d">
        <div class="ci-thumb">${item.icon}</div>
        <div class="ci-info">
          <div class="ci-name">${item.name}</div>
          <div class="ci-meta">${[item.color, item.size].filter(Boolean).join(' · ') || item.category}</div>
          <div class="ci-row">
            <div class="ci-qty">
              <button class="qty-btn" onclick="updateQty('${item.key}',-1)">−</button>
              <span class="qty-val">${item.qty}</span>
              <button class="qty-btn" onclick="updateQty('${item.key}',1)">+</button>
            </div>
            <button class="ci-remove" onclick="removeFromCart('${item.key}')">Remove</button>
          </div>
          <div class="ci-row" style="margin-top:8px">
            <div class="ci-price">₱${(item.price * item.qty).toLocaleString()}</div>
          </div>
        </div>
      </div>`).join('');
  }
  const totalEl = document.getElementById('drawer-total');
  if (totalEl) totalEl.textContent = '₱' + getCartTotal().toLocaleString();
  const countEl = document.getElementById('drawer-count');
  if (countEl) countEl.textContent = `(${getCartCount()})`;
}

function openCartDrawer() {
  document.getElementById('cart-drawer')?.classList.add('open');
  document.getElementById('drawer-overlay')?.classList.add('open');
  document.body.style.overflow = 'hidden';
}
function closeCartDrawer() {
  document.getElementById('cart-drawer')?.classList.remove('open');
  document.getElementById('drawer-overlay')?.classList.remove('open');
  document.body.style.overflow = '';
}

/* ── WISHLIST ── */
let wishlist = JSON.parse(localStorage.getItem('pothub_wish') || '[]');

function toggleWishlist(id) {
  const product = PRODUCTS.find(p => p.id === id);
  if (!product) return;
  if (wishlist.some(w => w.id === id)) {
    wishlist = wishlist.filter(w => w.id !== id);
    showToast(`<span class="toast-icon">🤍</span> Removed from wishlist`);
  } else {
    wishlist.push(product);
    showToast(`<span class="toast-icon">❤️</span> "${product.name}" added to wishlist`, 'success');
  }
  localStorage.setItem('pothub_wish', JSON.stringify(wishlist));
  updateWishBtns();
  updateWishBadge();
}

function isWished(id) { return wishlist.some(w => w.id === id); }

function updateWishBtns() {
  document.querySelectorAll('.pc-wish[data-id]').forEach(btn => {
    const id = parseInt(btn.dataset.id);
    btn.classList.toggle('wished', isWished(id));
    btn.title = isWished(id) ? 'Remove from wishlist' : 'Add to wishlist';
  });
}

function updateWishBadge() {
  document.querySelectorAll('.wish-count').forEach(el => el.textContent = wishlist.length);
}

/* ── RECENTLY VIEWED ── */
function addRecentlyViewed(id) {
  let rv = JSON.parse(localStorage.getItem('pothub_rv') || '[]');
  rv = [id, ...rv.filter(i => i !== id)].slice(0, 8);
  localStorage.setItem('pothub_rv', JSON.stringify(rv));
}

/* ── TOAST ── */
let toastTimer;
function showToast(html, type = 'info') {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    document.body.appendChild(container);
  }
  const t = document.createElement('div');
  t.className = 'toast';
  t.style.borderLeftColor = type === 'success' ? 'var(--gl)' : type === 'error' ? 'var(--terra)' : '#555';
  t.innerHTML = html + `<button class="toast-close" onclick="this.parentElement.remove()">✕</button>`;
  container.appendChild(t);
  requestAnimationFrame(() => t.classList.add('show'));
  setTimeout(() => { t.classList.remove('show'); setTimeout(() => t.remove(), 400); }, 3500);
}

/* ── PRODUCT CARD HTML ── */
function productCardHTML(p) {
  const badgeMap = { Bestseller:'badge-green', New:'badge-green', Trending:'badge-terra', Hot:'badge-terra', Sale:'badge-terra', Luxury:'badge-gold', Premium:'badge-gold', Designer:'badge-gold', Set:'badge-black' };
  return `
    <div class="product-card reveal" data-id="${p.id}" onclick="goProduct(${p.id})">
      ${p.badge ? `<div class="pc-badge"><span class="badge ${badgeMap[p.badge]||'badge-black'}">${p.badge}</span></div>` : ''}
      <button class="pc-wish ${isWished(p.id)?'wished':''}" data-id="${p.id}" title="${isWished(p.id)?'Remove from wishlist':'Add to wishlist'}" onclick="event.stopPropagation(); toggleWishlist(${p.id})">
        ${isWished(p.id) ? '❤️' : '🤍'}
      </button>
      <div class="pc-img">
        <div class="pc-img-inner">${p.icon}</div>
        <button class="pc-quick-add" onclick="event.stopPropagation(); addToCart(${p.id}); openCartDrawer()">+ Quick Add</button>
      </div>
      <div class="pc-info">
        <div class="pc-cat">${p.category}</div>
        <div class="pc-name">${p.name}</div>
        <div class="pc-rating">
          <span class="pc-stars">${'★'.repeat(Math.floor(p.rating))}${p.rating % 1 >= .5 ? '½' : ''}</span>
          <span class="pc-reviews">(${p.reviews})</span>
        </div>
        <div class="pc-foot">
          <div>
            <span class="pc-price">₱${p.price.toLocaleString()}</span>
            ${p.original ? `<span class="pc-orig">₱${p.original.toLocaleString()}</span>` : ''}
          </div>
          <button class="pc-add" onclick="event.stopPropagation(); addToCart(${p.id}); openCartDrawer()">+</button>
        </div>
      </div>
    </div>`;
}

function goProduct(id) {
  addRecentlyViewed(id);
  window.location.href = `product.html?id=${id}`;
}

/* ── NAVBAR SETUP ── */
function setupNavbar() {
  const nav = document.getElementById('navbar');
  if (!nav) return;
  window.addEventListener('scroll', () => nav.classList.toggle('scrolled', window.scrollY > 60));

  // Back to top
  const btt = document.getElementById('back-top');
  if (btt) window.addEventListener('scroll', () => btt.classList.toggle('show', window.scrollY > 400));

  // Active nav link
  const path = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-link').forEach(l => {
    const href = l.getAttribute('href') || '';
    if (href === path || (path === '' && href === 'index.html')) l.classList.add('active');
  });
}

/* ── SEARCH ── */
function openSearch() {
  document.getElementById('search-modal')?.classList.add('open');
  setTimeout(() => document.getElementById('search-field')?.focus(), 100);
}
function closeSearch() {
  document.getElementById('search-modal')?.classList.remove('open');
  const sf = document.getElementById('search-field');
  if (sf) sf.value = '';
  const sr = document.getElementById('search-results');
  if (sr) sr.innerHTML = '';
}
function handleSearch(q) {
  const sr = document.getElementById('search-results');
  if (!sr) return;
  if (!q.trim()) { sr.innerHTML = ''; return; }
  const hits = PRODUCTS.filter(p => p.name.toLowerCase().includes(q.toLowerCase()) || p.category.toLowerCase().includes(q.toLowerCase()) || p.tags.some(t => t.includes(q.toLowerCase())));
  if (!hits.length) { sr.innerHTML = '<p style="color:rgba(255,255,255,.3);font-size:12px;letter-spacing:2px;text-transform:uppercase">No results found</p>'; return; }
  sr.innerHTML = hits.slice(0,6).map(p => `
    <div class="search-result-item" onclick="goProduct(${p.id}); closeSearch()">
      <span class="sri-icon">${p.icon}</span>
      <div>
        <div class="sri-name">${p.name}</div>
        <div class="sri-meta">${p.category} · ₱${p.price.toLocaleString()}</div>
      </div>
    </div>`).join('');
}

/* ── MOBILE MENU ── */
let mobileOpen = false;
function toggleMobile() {
  mobileOpen = !mobileOpen;
  document.getElementById('mobile-menu')?.classList.toggle('open', mobileOpen);
  const btn = document.getElementById('mobile-toggle');
  if (btn) btn.textContent = mobileOpen ? '✕' : '☰';
}
function closeMobile() { mobileOpen = false; document.getElementById('mobile-menu')?.classList.remove('open'); const btn = document.getElementById('mobile-toggle'); if (btn) btn.textContent = '☰'; }

/* ── SCROLL REVEAL ── */
function setupReveal() {
  const obs = new IntersectionObserver(entries => {
    entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible'); obs.unobserve(e.target); } });
  }, { threshold: 0.1 });
  document.querySelectorAll('.reveal').forEach(el => obs.observe(el));
}

/* ── NEWSLETTER ── */
function nlSubmit(emailId = 'nl-email', successId = 'nl-success') {
  const v = document.getElementById(emailId)?.value.trim();
  if (v && v.includes('@')) {
    const s = document.getElementById(successId);
    if (s) s.style.display = 'block';
    document.getElementById(emailId).value = '';
    showToast('<span class="toast-icon">🌿</span> Subscribed! Welcome to PotHub.', 'success');
  } else {
    showToast('<span class="toast-icon">⚠️</span> Please enter a valid email.', 'error');
  }
}

/* ── DARK MODE ── */
function toggleDark() {
  document.body.classList.toggle('dark-mode');
  localStorage.setItem('pothub_dark', document.body.classList.contains('dark-mode'));
  const btn = document.getElementById('dark-toggle');
  if (btn) btn.textContent = document.body.classList.contains('dark-mode') ? '☀️' : '🌙';
}

/* ── INIT ── */
document.addEventListener('DOMContentLoaded', async () => {
  // Dark mode
  if (localStorage.getItem('pothub_dark') === 'true') {
    document.body.classList.add('dark-mode');
    const dt = document.getElementById('dark-toggle');
    if (dt) dt.textContent = '☀️';
  }

  // Preloader
  const pre = document.getElementById('preloader');
  if (pre) {
    await loadProducts();
    setTimeout(() => pre.classList.add('hide'), 1200);
  } else {
    await loadProducts();
  }

  setupNavbar();
  updateCartBadge();
  updateWishBadge();
  updateWishBtns();
  renderCartDrawer();

  // ESC key
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') { closeSearch(); closeMobile(); closeCartDrawer(); }
  });

  // Reveal on scroll
  setTimeout(setupReveal, 200);

  // Page-specific init
  if (typeof pageInit === 'function') pageInit();
});
