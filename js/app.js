// Helpers
const $ = (q, c=document) => c.querySelector(q);
const $$ = (q, c=document) => [...c.querySelectorAll(q)];
document.documentElement.classList.remove('no-js');

// Year
$("#year") && ($("#year").textContent = new Date().getFullYear());

// Theme
const root = document.documentElement;
const savedTheme = localStorage.getItem('theme');
if(savedTheme){ root.classList.toggle('light', savedTheme === 'light'); }
$("#themeToggle")?.addEventListener('click', ()=>{
  const isLight = root.classList.toggle('light');
  localStorage.setItem('theme', isLight ? 'light' : 'dark');
});

// Copy to clipboard (correo, etc.)
$$('[data-copy]').forEach(btn => {
  btn.addEventListener('click', async () => {
    const text = btn.getAttribute('data-copy') || '';
    if(!text) return;
    const original = btn.textContent;
    try{
      await navigator.clipboard.writeText(text);
      btn.textContent = 'Copiado ✓';
    }catch{
      // Fallback
      const ta = document.createElement('textarea');
      ta.value = text;
      ta.style.position = 'fixed';
      ta.style.opacity = '0';
      document.body.appendChild(ta);
      ta.select();
      document.execCommand('copy');
      document.body.removeChild(ta);
      btn.textContent = 'Copiado ✓';
    }
    setTimeout(()=>{ btn.textContent = original; }, 1400);
  });
});

// Reveal on scroll
const io = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if(e.isIntersecting){
      e.target.classList.add('show');
      io.unobserve(e.target);
    }
  });
}, { threshold: .15 });
$$('.reveal').forEach(el => io.observe(el));

// Diplomas
async function loadDiplomas(){
  try{
    const res = await fetch('data/diplomas.json', {cache:'no-store'});
    const list = await res.json();
    const wrap = $("#diploma-grid");
    wrap.innerHTML = '';
    list.forEach(item => {
      const tile = document.createElement('article');
      tile.className = 'tile diploma-tile hoverable reveal';
      tile.innerHTML = `
        <div class="thumb" aria-hidden="true">
          <img src="${item.thumb}" alt="Vista previa de ${item.title}" loading="lazy">
        </div>
        <div class="content">
          <div class="title">${item.title}</div>
          <div class="meta">${item.institution || ''} ${item.date ? '· '+item.date : ''}</div>
          <div style="margin-top:8px">
            <a class="card-link" href="${item.file}" target="_blank" rel="noopener">Abrir</a>
          </div>
        </div>
      `;
      tile.addEventListener('click', (e)=>{
        if(e.target.tagName.toLowerCase() === 'a') return;
        openLightbox(item);
      });
      wrap.appendChild(tile);
      io.observe(tile);
    });
  }catch(e){
    console.error('Error cargando diplomas', e);
  }
}

function openLightbox(item){
  const box = $("#lightbox");
  const img = $("#lightbox-img");
  const pdf = $("#lightbox-pdf");
  img.style.display = 'none';
  pdf.style.display = 'none';

  if((item.type||'').toLowerCase() === 'image'){
    img.src = item.file;
    img.alt = item.title;
    img.style.display = 'block';
  }else{
    pdf.src = item.file;
    pdf.style.display = 'block';
  }
  box.classList.add('show');
  box.setAttribute('aria-hidden','false');

  // Accesibilidad: llevar el foco al botón de cerrar
  box.querySelector('.lightbox-close')?.focus();
}

function closeLightbox(){
  const box = $("#lightbox");
  $("#lightbox-img").src = '';
  $("#lightbox-pdf").src = '';
  box.classList.remove('show');
  box.setAttribute('aria-hidden','true');
}

$(".lightbox-close")?.addEventListener('click', closeLightbox);

// Cerrar al hacer clic fuera del contenido (en el fondo oscuro)
$("#lightbox")?.addEventListener('click', (e)=>{
  if(e.target === e.currentTarget) closeLightbox();
});

// Cerrar con tecla ESC
document.addEventListener('keydown', (e)=>{
  if(e.key === 'Escape' && $("#lightbox")?.classList.contains('show')){
    closeLightbox();
  }
});

loadDiplomas();
