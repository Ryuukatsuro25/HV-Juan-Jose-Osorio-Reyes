
// Mobile nav
const navToggle = document.querySelector('.nav-toggle');
const navMenu = document.querySelector('.nav-menu');
if (navToggle) navToggle.addEventListener('click', () => navMenu.classList.toggle('show'));

// Theme toggle
const root = document.documentElement;
const themeToggle = document.getElementById('themeToggle');
function setTheme(mode){
  if(mode === 'light'){ root.classList.add('light'); localStorage.setItem('theme','light'); }
  else { root.classList.remove('light'); localStorage.setItem('theme','dark'); }
}
setTheme(localStorage.getItem('theme') || 'dark');
if (themeToggle) themeToggle.addEventListener('click', ()=>{
  const isLight = root.classList.contains('light');
  setTheme(isLight ? 'dark' : 'light');
});

// Load data
async function loadData(){ const r = await fetch('gallery-data.json'); return r.json(); }

function card(item){
  const el = document.createElement('article');
  el.className = 'card item';
  el.innerHTML = `
    <img src="${item.thumb}" alt="${item.title}">
    <div class="pad">
      <h4>${item.title}</h4>
      <p class="meta">${item.description}</p>
    </div>
  `;
  el.addEventListener('click', ()=> openLightbox(item));
  el.style.opacity = 0; el.style.transform = 'translateY(12px)';
  requestAnimationFrame(()=>{
    el.style.transition = 'opacity .35s ease, transform .35s ease';
    el.style.opacity = 1; el.style.transform = 'none';
  });
  return el;
}

function render(data, filter='all', q=''){
  const grid = document.getElementById('portfolioGrid');
  grid.innerHTML = '';
  Object.entries(data).forEach(([cat, payload])=>{
    const list = payload.items
      .filter(i => filter === 'all' || filter === cat)
      .filter(i => i.title.toLowerCase().includes(q) || i.description.toLowerCase().includes(q));
    if(!list.length) return;
    const section = document.createElement('section');
    section.className = 'category';
    section.innerHTML = `<h2>${cat.charAt(0).toUpperCase() + cat.slice(1)}</h2>
                         <p class="meta">${payload.description}</p>`;
    const wrap = document.createElement('div');
    wrap.className = 'grid-3';
    list.forEach(item => wrap.appendChild(card(item)));
    section.appendChild(wrap);
    grid.appendChild(section);
  });
}

function openLightbox(item){
  const dlg = document.getElementById('lightbox');
  document.getElementById('lbImage').src = item.thumb;
  document.getElementById('lbTitle').textContent = item.title;
  document.getElementById('lbDesc').textContent = item.description;
  document.getElementById('lbLink').href = item.link || '#';
  if (typeof dlg.showModal === 'function') dlg.showModal(); else alert(item.title);
}
document.getElementById('lbClose').addEventListener('click', ()=> document.getElementById('lightbox').close());

// Filters
const chips = document.querySelectorAll('.chip');
const search = document.getElementById('search');
let current = 'all', keyword = '';
chips.forEach(c=> c.addEventListener('click', ()=> {
  current = c.dataset.filter; chips.forEach(x=>x.classList.remove('active')); c.classList.add('active');
  loadData().then(d => render(d, current, keyword));
}));
if(search) search.addEventListener('input', ()=>{
  keyword = search.value.trim().toLowerCase();
  loadData().then(d => render(d, current, keyword));
});

// Init
loadData().then(d => render(d));
