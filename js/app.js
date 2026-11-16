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

// Diplomas (se cargan dentro del desplegable de Formación)
async function loadDiplomas(){
  const wrap = $("#diploma-grid");
  if(!wrap) return;
  try{
    const res = await fetch('data/diplomas.json', {cache:'no-store'});
    const list = await res.json();
    wrap.innerHTML = '';
    list.forEach(item => {
      const tile = document.createElement('button');
      tile.type = 'button';
      tile.className = 'tile diploma-tile hoverable';
      tile.setAttribute('aria-label', `Ver certificado: ${item.title}`);
      tile.innerHTML = `
        <div class="thumb" aria-hidden="true">
          <img src="${item.thumb}" alt="" loading="lazy">
        </div>
        <div class="content"><div class="title">${item.title}</div></div>
      `;
      tile.addEventListener('click', ()=> openLightbox(item));
      wrap.appendChild(tile);
    });
  }catch(e){
    console.error('Error cargando diplomas', e);
  }
}

// Videos del portafolio: se reproducen solo al pasar el cursor o al enfocar (ahorra datos en móvil)
$$('video.hover-play').forEach(v => {
  const card = v.closest('.gallery-item') || v;
  const play = () => { v.play().catch(()=>{}); };
  const stop = () => { v.pause(); };
  card.addEventListener('mouseenter', play);
  card.addEventListener('mouseleave', stop);
  card.addEventListener('focusin', play);
  card.addEventListener('focusout', stop);
});

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
