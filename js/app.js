// Helpers
const $ = (q, c=document) => c.querySelector(q);
const $$ = (q, c=document) => [...c.querySelectorAll(q)];
document.documentElement.classList.remove('no-js');

// Year
$("#year") && ($("#year").textContent = new Date().getFullYear());

// Theme toggle (persisted)
const root = document.documentElement;
const savedTheme = localStorage.getItem('theme');
if(savedTheme){ root.classList.toggle('light', savedTheme === 'light'); }
$("#themeToggle")?.addEventListener('click', ()=>{
  const isLight = root.classList.toggle('light');
  localStorage.setItem('theme', isLight ? 'light' : 'dark');
});

// Mobile menu
const menu = $("#mainNav");
const menuBtn = $("#menuToggle");
if(menu && menuBtn){
  const closeMenu = () => { menu.classList.remove('open'); menuBtn.setAttribute('aria-expanded', 'false'); };
  const openMenu  = () => { menu.classList.add('open'); menuBtn.setAttribute('aria-expanded', 'true'); };
  menuBtn.addEventListener('click', ()=>{
    const open = menu.classList.toggle('open');
    menuBtn.setAttribute('aria-expanded', String(open));
  });
  // Close on link click
  menu.addEventListener('click', (e)=>{
    if(e.target.tagName.toLowerCase() === 'a'){ closeMenu(); }
  });
  // Close on escape
  window.addEventListener('keydown', (e)=>{ if(e.key === 'Escape') closeMenu(); });
}

// Reveal on scroll
const io = ('IntersectionObserver' in window) ? new IntersectionObserver((entries)=>{
  entries.forEach(en=>{ if(en.isIntersecting){ en.target.classList.add('visible'); io.unobserve(en.target); } });
}, { rootMargin: '0px 0px -10% 0px' }) : null;
if(io){ $$('.reveal').forEach(el=>io.observe(el)); } else { $$('.reveal').forEach(el=>el.classList.add('visible')); }

// Diplomas loader
async function loadDiplomas(){
  try{
    const res = await fetch('data/diplomas.json');
    const list = await res.json();
    const wrap = $("#diplomasGrid");
    if(!wrap) return;
    list.forEach(item=>{
      const tile = document.createElement('article');
      tile.className = 'diploma-tile reveal';
      tile.innerHTML = `
        <div class="thumb" aria-hidden="true"></div>
        <div>
          <div class="title">${item.title || 'Diploma'}</div>
          <div class="meta">${item.year || ''}</div>
        </div>
      `;
      tile.addEventListener('click', ()=> openLightbox(item));
      wrap.appendChild(tile);
      io && io.observe(tile);
    });
  }catch(e){
    console.error('Error cargando diplomas', e);
  }
}

function openLightbox(item){
  const box = $("#lightbox");
  const img = $("#lightbox-img");
  const link = $("#lightbox-link");
  if(!box || !img || !link) return;
  // Use the PDF directly; thumbnails could be added later.
  img.src = 'assets/icons/pdf.svg';
  link.href = item.file;
  box.showModal();
}

$("#lightboxClose")?.addEventListener('click', ()=> $("#lightbox")?.close());
document.addEventListener('keydown', (e)=>{
  if(e.key === 'Escape'){ $("#lightbox")?.close(); }
});

loadDiplomas();
