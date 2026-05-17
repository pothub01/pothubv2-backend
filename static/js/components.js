/* ═══════════════════════════════════════════════
   POTHUB — components.js (shared HTML components)
═══════════════════════════════════════════════ */

function getNavHTML(active = '') {
  return `
  <div id="preloader"><div class="pre-logo">POT<span>HUB</span><div class="pre-bar"></div></div></div>
  <div id="toast-container"></div>
  <button class="back-top" id="back-top" onclick="window.scrollTo({top:0,behavior:'smooth'})">↑</button>
  <button class="dark-toggle" id="dark-toggle" onclick="toggleDark()" title="Toggle dark mode">🌙</button>

  <!-- Drawer Overlay -->
  <div class="drawer-overlay" id="drawer-overlay" onclick="closeCartDrawer()"></div>

  <!-- Cart Drawer -->
  <div class="drawer" id="cart-drawer">
    <div class="drawer-head">
      <div class="drawer-title">Cart <span id="drawer-count" style="font-size:16px;color:var(--mid);font-weight:400">(0)</span></div>
      <button class="drawer-close" onclick="closeCartDrawer()">✕</button>
    </div>
    <div class="drawer-body" id="drawer-body"></div>
    <div class="drawer-foot">
      <div class="drawer-total-row">
        <span class="drawer-total-label">Total</span>
        <span class="drawer-total-amt" id="drawer-total">₱0</span>
      </div>
      <a href="cart.html" class="btn btn-black btn-full" style="margin-bottom:10px;display:flex">View Cart</a>
      <a href="checkout.html" class="btn btn-green btn-full" style="display:flex">Checkout →</a>
    </div>
  </div>

  <!-- Search Modal -->
  <div class="search-modal" id="search-modal">
    <div class="search-inner">
      <div class="search-form">
        <span class="search-ico">🔍</span>
        <input class="search-field" id="search-field" type="text" placeholder="SEARCH POTS..." oninput="handleSearch(this.value)" autocomplete="off">
        <button class="search-x" onclick="closeSearch()">✕</button>
      </div>
      <div class="search-hints">
        <div class="search-hint-label">Press ESC to close</div>
        <div class="search-results" id="search-results"></div>
      </div>
    </div>
  </div>

  <!-- Mobile Menu -->
  <div class="mobile-menu" id="mobile-menu">
    <a href="index.html" class="mm-link" onclick="closeMobile()">Home</a>
    <a href="shop.html" class="mm-link" onclick="closeMobile()">Shop</a>
    <a href="collections.html" class="mm-link" onclick="closeMobile()">Collections</a>
    <a href="about.html" class="mm-link" onclick="closeMobile()">About</a>
    <a href="blog.html" class="mm-link" onclick="closeMobile()">Blog</a>
    <a href="contact.html" class="mm-link" onclick="closeMobile()">Contact</a>
    <div class="mm-footer">
      <div id="mobile-auth">
        <a href="/login" class="btn btn-ghost-dark btn-sm">Login</a>
        <a href="/register" class="btn btn-green btn-sm">Sign Up</a>
      </div>
      <div id="mobile-user" style="display:none;align-items:center;gap:10px">
        <span id="mobile-user-name" style="font-size:13px;font-weight:600"></span>
        <a href="/" onclick="logout();return false;" class="btn btn-ghost-dark btn-sm" style="font-size:12px">Logout</a>
      </div>
    </div>
  </div>

  <!-- Navbar -->
  <nav class="navbar" id="navbar">
    <div class="container">
      <a href="index.html" class="nav-logo">POT<span>HUB</span></a>
      <ul class="nav-links">
        <li><a href="index.html" class="nav-link ${active==='home'?'active':''}">Home</a></li>
        <li><a href="shop.html" class="nav-link ${active==='shop'?'active':''}">Shop</a></li>
        <li><a href="collections.html" class="nav-link ${active==='collections'?'active':''}">Collections</a></li>
        <li><a href="about.html" class="nav-link ${active==='about'?'active':''}">About</a></li>
        <li><a href="blog.html" class="nav-link ${active==='blog'?'active':''}">Blog</a></li>
        <li><a href="contact.html" class="nav-link ${active==='contact'?'active':''}">Contact</a></li>
      </ul>
      <div class="nav-actions">
        <button class="nav-btn" onclick="openSearch()">🔍 Search</button>
        <a href="wishlist.html" class="nav-btn">🤍 <span class="wish-count">0</span></a>
        <a href="/login" class="nav-btn" id="nav-account-btn">👤 Account</a>
        <button class="nav-btn nav-cart-btn" onclick="openCartDrawer()">🌿 Cart <span class="cart-count">0</span></button>
        <button class="nav-mobile-btn" id="mobile-toggle" onclick="toggleMobile()">☰</button>
      </div>
    </div>
  </nav>`;
}

function getFooterHTML() {
  return `
  <footer>
    <div class="container">
      <div class="footer-grid">
        <div>
          <div class="footer-brand">POT<span>HUB</span></div>
          <div class="footer-tagline">Just Grow It.</div>
          <p class="footer-desc">Premium pots and planters for every plant parent. Handcrafted, curated, and delivered across the Philippines.</p>
          <div class="footer-social" style="margin-top:24px">
            <a class="social-btn" title="Instagram">📸</a>
            <a class="social-btn" title="Facebook">📘</a>
            <a class="social-btn" title="TikTok">🎵</a>
            <a class="social-btn" title="Pinterest">📌</a>
          </div>
        </div>
        <div class="footer-col">
          <h4>Shop</h4>
          <ul>
            <li><a href="shop.html">New Arrivals</a></li>
            <li><a href="shop.html?cat=ceramic">Ceramic Pots</a></li>
            <li><a href="shop.html?cat=hanging">Hanging Planters</a></li>
            <li><a href="shop.html?cat=luxury">Luxury Collection</a></li>
            <li><a href="shop.html?tag=sale">Sale</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h4>Support</h4>
          <ul>
            <li><a href="faq.html">FAQ</a></li>
            <li><a href="faq.html#shipping">Shipping & Returns</a></li>
            <li><a href="faq.html#care">Plant Care Guide</a></li>
            <li><a href="contact.html">Contact Us</a></li>
            <li><a href="faq.html#tracking">Track Order</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h4>Company</h4>
          <ul>
            <li><a href="about.html">About PotHub</a></li>
            <li><a href="about.html#sustainability">Sustainability</a></li>
            <li><a href="blog.html">Blog</a></li>
            <li><a href="#">Press</a></li>
            <li><a href="#">Privacy Policy</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <span>© 2026 PotHub Philippines. All rights reserved.</span>
        <span class="footer-badge">POWERED BY SHOPIFY</span>
      </div>
    </div>
  </footer>`;
}

// Inject into page
function injectComponents(active = '') {
  const navPlaceholder = document.getElementById('nav-placeholder');
  const footerPlaceholder = document.getElementById('footer-placeholder');
  if (navPlaceholder) navPlaceholder.outerHTML = getNavHTML(active);
  if (footerPlaceholder) footerPlaceholder.outerHTML = getFooterHTML();
}

// ── User Session Management ──
function checkUserSession() {
  const user = JSON.parse(localStorage.getItem('pothub_user') || 'null');
  const authButtons = document.getElementById('auth-buttons');
  const userMenu = document.getElementById('user-menu');
  const userName = document.getElementById('user-name');
  const mobileAuth = document.getElementById('mobile-auth');
  const mobileUser = document.getElementById('mobile-user');
  const mobileUserName = document.getElementById('mobile-user-name');

  if (user && user.name) {
    if (authButtons) authButtons.style.display = 'none';
    if (userMenu) { userMenu.style.display = 'flex'; userName.textContent = '👤 ' + user.name; }
    if (mobileAuth) mobileAuth.style.display = 'none';
    if (mobileUser) { mobileUser.style.display = 'flex'; mobileUserName.textContent = '👤 ' + user.name; }
  } else {
    if (authButtons) authButtons.style.display = 'flex';
    if (userMenu) userMenu.style.display = 'none';
    if (mobileAuth) mobileAuth.style.display = 'flex';
    if (mobileUser) mobileUser.style.display = 'none';
  }
}

function logout() {
  localStorage.removeItem('pothub_user');
  localStorage.removeItem('pothub_token');
  showToast('<span class="toast-icon">👋</span> Logged out successfully', 'success');
  setTimeout(() => window.location.reload(), 1000);
}

// Check session on page load
document.addEventListener('DOMContentLoaded', checkUserSession);
