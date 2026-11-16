// CV web — Juan José Osorio Reyes
// Funciones: tema claro/oscuro, menú que marca la sección visible, aparición suave al hacer scroll,
// filtro de proyectos, certificados del diplomado en un visor y video que se reproduce al pasar el cursor.
const $ = (s, el = document) => el.querySelector(s);
const $$ = (s, el = document) => Array.from(el.querySelectorAll(s));

$('#year').textContent = new Date().getFullYear();

// ---------- Tema ----------
const root = document.documentElement;
const themeBtn = $('#theme');
function currentTheme(){
  if (root.dataset.theme) return root.dataset.theme;
  return matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
}
function syncThemeLabel(){
  const next = currentTheme() === 'dark' ? 'claro' : 'oscuro';
  themeBtn.setAttribute('aria-label', `Cambiar a tema ${next}`);
}
themeBtn.addEventListener('click', () => {
  const next = currentTheme() === 'dark' ? 'light' : 'dark';
  root.dataset.theme = next;
  try { localStorage.setItem('theme', next); } catch (err) {}
  syncThemeLabel();
});
syncThemeLabel();

// ---------- Cabecera: borde al hacer scroll ----------
const header = $('.top');
const onScroll = () => header.classList.toggle('scrolled', scrollY > 8);
addEventListener('scroll', onScroll, { passive: true });
onScroll();

// ---------- Menú: marca la sección visible ----------
const navLinks = $$('.nav a');
const spy = new IntersectionObserver(entries => {
  entries.forEach(en => {
    if (!en.isIntersecting) return;
    navLinks.forEach(a => {
      const on = a.getAttribute('href') === '#' + en.target.id;
      if (on) a.setAttribute('aria-current', 'true'); else a.removeAttribute('aria-current');
    });
  });
}, { rootMargin: '-40% 0px -55% 0px' });
navLinks.map(a => $(a.getAttribute('href'))).filter(Boolean).forEach(s => spy.observe(s));

// ---------- Aparición suave (una sola vez por sección) ----------
const reveal = new IntersectionObserver(entries => {
  entries.forEach(en => {
    if (en.isIntersecting){ en.target.classList.add('in'); reveal.unobserve(en.target); }
  });
}, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });
$$('.reveal').forEach(el => reveal.observe(el));

// ---------- Filtro de proyectos ----------
const chips = $$('.chip');
const projects = $$('.project');
const status = $('#filter-status');
chips.forEach(chip => chip.addEventListener('click', () => {
  const f = chip.dataset.filter;
  chips.forEach(c => {
    const on = c === chip;
    c.classList.toggle('is-on', on);
    c.setAttribute('aria-pressed', String(on));
  });
  let shown = 0;
  projects.forEach(p => {
    const show = f === 'all' || p.dataset.area === f;
    p.hidden = !show;
    if (show) shown++;
  });
  if (status) status.textContent = `${shown} proyectos visibles`;
}));

// ---------- Certificados del diplomado ----------
const lightbox = $('#lightbox');
const lbImg = $('#lightbox-img');
const lbPdf = $('#lightbox-pdf');
let lastFocus = null;

function openLightbox(item){
  lastFocus = document.activeElement;
  if (item.type === 'pdf'){
    lbImg.hidden = true; lbPdf.hidden = false; lbPdf.src = item.file;
  } else {
    lbPdf.hidden = true; lbImg.hidden = false; lbImg.src = item.file; lbImg.alt = item.title;
  }
  lightbox.hidden = false;
  document.body.style.overflow = 'hidden';
  $('.lightbox-close', lightbox).focus();
}
function closeLightbox(){
  lightbox.hidden = true;
  lbPdf.src = 'about:blank';
  document.body.style.overflow = '';
  if (lastFocus) lastFocus.focus();
}
$('.lightbox-close', lightbox).addEventListener('click', closeLightbox);
lightbox.addEventListener('click', e => { if (e.target === lightbox) closeLightbox(); });
addEventListener('keydown', e => { if (e.key === 'Escape' && !lightbox.hidden) closeLightbox(); });

let diplomasLoaded = false;
async function loadDiplomas(){
  if (diplomasLoaded) return;
  diplomasLoaded = true;
  const grid = $('#diploma-grid');
  if (!grid) return;
  try {
    const res = await fetch('data/diplomas.json');
    const list = await res.json();
    list.forEach(item => {
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'diploma';
      b.setAttribute('aria-label', `Ver certificado: ${item.title}`);
      b.innerHTML = `<img src="${item.thumb}" alt="" loading="lazy"><span>${item.title}</span>`;
      b.addEventListener('click', () => openLightbox(item));
      grid.appendChild(b);
    });
  } catch (err) {
    grid.innerHTML = '<p>No se pudieron cargar los certificados. Revisa que exista data/diplomas.json.</p>';
  }
}
// Se cargan al abrir el desplegable, para no pesar en la carga inicial
const dipDetails = $('#diploma-grid')?.closest('details');
if (dipDetails){
  dipDetails.addEventListener('toggle', () => { if (dipDetails.open) loadDiplomas(); });
  if (dipDetails.open) loadDiplomas();
}

// ---------- Video del portafolio: se reproduce al pasar el cursor o enfocar ----------
$$('video.hover-play').forEach(v => {
  const fig = v.closest('figure') || v;
  const play = () => v.play().catch(() => {});
  const stop = () => v.pause();
  fig.addEventListener('mouseenter', play);
  fig.addEventListener('mouseleave', stop);
  v.addEventListener('focus', play);
  v.addEventListener('blur', stop);
});
