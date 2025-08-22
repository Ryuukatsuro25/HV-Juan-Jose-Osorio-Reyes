
// Mobile nav
const navToggle = document.querySelector('.nav-toggle');
const navMenu = document.querySelector('.nav-menu');
if (navToggle) {
  navToggle.addEventListener('click', () => navMenu.classList.toggle('show'));
}

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

// Load gallery data
async function loadGallery(){
  const res = await fetch('gallery-data.json');
  return res.json();
}

function renderItems(data, filter='all', keyword=''){
  const grid = document.getElementById('portfolioGrid');
  grid.innerHTML = '';

  const cats = Object.keys(data);
  cats.forEach(cat => {
    const section = document.createElement('div');
    section.className = 'category-section';
    const title = document.createElement('h2');
    title.textContent = cat.charAt(0).toUpperCase() + cat.slice(1);
    section.appendChild(title);

    const desc = document.createElement('p');
    desc.className = 'meta';
    desc.textContent = data[cat].description;
    section.appendChild(desc);

    const wrap = document.createElement('div');
    wrap.className = 'grid-3';

    data[cat].items
      .filter(i => (filter === 'all' || filter === cat))
      .filter(i => (i.title.toLowerCase().includes(keyword) || i.description.toLowerCase().includes(keyword)))
      .forEach(item => {
        const card = document.createElement('article');
        card.className = 'card item';
        card.innerHTML = `
          <img src="${item.thumb}" alt="${item.title}">
          <div class="pad">
            <h4>${item.title}</h4>
            <p>${item.description}</p>
          </div>
        `;
        card.addEventListener('click', ()=> openLightbox(item));
        wrap.appendChild(card);
      });

    if (wrap.children.length > 0) {
      section.appendChild(wrap);
      grid.appendChild(section);
    }
  });
}

function openLightbox(item){
  const dlg = document.getElementById('lightbox');
  document.getElementById('lbImage').src = item.thumb;
  document.getElementById('lbTitle').textContent = item.title;
  document.getElementById('lbDesc').textContent = item.description;
  document.getElementById('lbLink').href = item.link || '#';
  if (typeof dlg.showModal === 'function') dlg.showModal(); else alert('Vista previa: ' + item.title);
}
const lbClose = document.getElementById('lbClose');
if (lbClose) lbClose.addEventListener('click', ()=> document.getElementById('lightbox').close());

// Filters and search
const chips = document.querySelectorAll('.chip');
const search = document.getElementById('search');
let currentFilter = 'all';
let currentKeyword = '';

chips.forEach(c => c.addEventListener('click', ()=>{
  currentFilter = c.dataset.filter;
  chips.forEach(x=>x.classList.remove('active'));
  c.classList.add('active');
  loadGallery().then(data => renderItems(data, currentFilter, currentKeyword));
}));

if (search){
  search.addEventListener('input', ()=>{
    currentKeyword = search.value.trim().toLowerCase();
    loadGallery().then(data => renderItems(data, currentFilter, currentKeyword));
  });
}

// Initial render
loadGallery().then(data => renderItems(data));
