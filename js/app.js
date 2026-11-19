// CV web — Juan José Osorio Reyes
// Tema, menú móvil, barra de progreso, aparición al hacer scroll, texto que se escribe solo,
// contadores, línea de tiempo animada, luz que sigue al cursor, filtro de proyectos,
// certificados, copiar correo y botón para volver arriba.
const $ = (s, el = document) => el.querySelector(s);
const $$ = (s, el = document) => Array.from(el.querySelectorAll(s));
const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
const root = document.documentElement;

$('#year').textContent = new Date().getFullYear();

// Las animaciones de aparición solo se activan si este script carga.
// Si falla, no hay IntersectionObserver o la página la visita una herramienta automática
// (capturas, robots), todo el contenido queda visible desde el inicio.
const canAnimate = 'IntersectionObserver' in window && !navigator.webdriver;
root.classList.add('js-ready');           // filtros y "ver todos" activos
// La clase 'anim' (que oculta el contenido hasta que aparece) se añade más abajo,
// solo cuando el observador ya está listo.

// Red de seguridad: si algún error de JS ocurre, se muestra todo el contenido
// en lugar de dejar las secciones invisibles.
addEventListener('error', () => {
  root.classList.remove('anim');
  $$('.reveal').forEach(el => el.classList.add('show'));
});

// ---------- Tema claro / oscuro ----------
const themeBtn = $('#themeToggle');
if (themeBtn){
  const syncTheme = () => themeBtn.setAttribute('aria-label', root.classList.contains('light') ? 'Cambiar a tema oscuro' : 'Cambiar a tema claro');
  themeBtn.addEventListener('click', () => {
    root.classList.toggle('light');
    try { localStorage.setItem('theme', root.classList.contains('light') ? 'light' : 'dark'); } catch (err) {}
    syncTheme();
  });
  syncTheme();
}

// ---------- Menú móvil ----------
const menuBtn = $('#menuToggle');
const nav = $('#main-nav');
if (menuBtn && nav){
  const closeMenu = () => { nav.classList.remove('open'); menuBtn.setAttribute('aria-expanded', 'false'); menuBtn.setAttribute('aria-label', 'Abrir menú'); };
  menuBtn.addEventListener('click', () => {
    const open = !nav.classList.contains('open');
    nav.classList.toggle('open', open);
    menuBtn.setAttribute('aria-expanded', String(open));
    menuBtn.setAttribute('aria-label', open ? 'Cerrar menú' : 'Abrir menú');
  });
  $$('a', nav).forEach(a => a.addEventListener('click', closeMenu));
  addEventListener('keydown', e => { if (e.key === 'Escape' && nav.classList.contains('open')) { closeMenu(); menuBtn.focus(); } });
}

// ---------- Scroll: progreso, cabecera, volver arriba, línea de tiempo ----------
const header = $('.site-header');
const progress = $('.progress');
const toTop = $('.to-top');
const timeline = $('.timeline');
let ticking = false;
function onScroll(){
  const max = root.scrollHeight - innerHeight;
  progress.style.setProperty('--p', max > 0 ? (scrollY / max).toFixed(4) : 0);
  header.classList.toggle('scrolled', scrollY > 10);
  toTop.classList.toggle('show', scrollY > innerHeight * 0.8);
  if (timeline){
    const r = timeline.getBoundingClientRect();
    const t = Math.min(1, Math.max(0, (innerHeight * 0.75 - r.top) / r.height));
    timeline.style.setProperty('--tl', reduceMotion ? 1 : t.toFixed(3));
  }
  ticking = false;
}
addEventListener('scroll', () => { if (!ticking){ requestAnimationFrame(onScroll); ticking = true; } }, { passive: true });
addEventListener('resize', onScroll);
onScroll();
toTop.addEventListener('click', () => { scrollTo({ top: 0, behavior: reduceMotion ? 'auto' : 'smooth' }); $('#nombre').focus({ preventScroll: true }); });
$('#nombre').setAttribute('tabindex', '-1');

// ---------- Menú: resalta la sección visible ----------
const navLinks = $$('.main-nav a');
const spy = 'IntersectionObserver' in window && new IntersectionObserver(entries => {
  entries.forEach(en => {
    if (!en.isIntersecting) return;
    navLinks.forEach(a => {
      const on = a.getAttribute('href') === '#' + en.target.id;
      a.classList.toggle('active', on);
      if (on) a.setAttribute('aria-current', 'true'); else a.removeAttribute('aria-current');
    });
  });
}, { rootMargin: '-45% 0px -50% 0px' });
if (spy) navLinks.map(a => $(a.getAttribute('href'))).filter(Boolean).forEach(s => spy.observe(s));

// ---------- Contadores ----------
function countUp(el){
  const target = parseInt(el.dataset.count, 10);
  if (isNaN(target) || reduceMotion){ el.textContent = el.dataset.count; return; }
  const dur = 1200, t0 = performance.now();
  const step = now => {
    const p = Math.min(1, (now - t0) / dur);
    el.textContent = Math.round(target * (1 - Math.pow(1 - p, 3)));
    if (p < 1) requestAnimationFrame(step);
  };
  requestAnimationFrame(step);
}

// ---------- Aparición al hacer scroll (una sola vez) ----------
const reveal = canAnimate && new IntersectionObserver(entries => {
  entries.forEach(en => {
    if (!en.isIntersecting) return;
    en.target.classList.add('show');
    $$('[data-count]', en.target).forEach(countUp);
    reveal.unobserve(en.target);
  });
}, { rootMargin: '0px 0px -10% 0px', threshold: 0.12 });
$$('.project').forEach((p, i) => { p.classList.add('reveal'); p.style.setProperty('--d', i % 3); });
if (canAnimate){
  root.classList.add('anim'); // apariciones al hacer scroll
  $$('.reveal').forEach(el => reveal.observe(el));
} else {
  $$('.reveal').forEach(el => el.classList.add('show'));
  $$('[data-count]').forEach(el => { el.textContent = el.dataset.count; });
}
// Al imprimir se muestra todo, incluso lo que no se ha desplazado
addEventListener('beforeprint', () => $$('.reveal').forEach(el => el.classList.add('show')));

// ---------- Texto del titular que se escribe y se borra ----------
const typed = $('.typed');
if (typed && !reduceMotion){
  const roles = JSON.parse(typed.dataset.roles);
  let r = 0, c = roles[0].length, deleting = true;
  const tick = () => {
    const word = roles[r];
    c += deleting ? -1 : 1;
    typed.textContent = word.slice(0, c);
    let wait = deleting ? 35 : 70;
    if (!deleting && c === word.length){ deleting = true; wait = 1800; }
    else if (deleting && c === 0){ deleting = false; r = (r + 1) % roles.length; wait = 300; }
    setTimeout(tick, wait);
  };
  setTimeout(tick, 2200);
}

// ---------- Luz que sigue al cursor en las tarjetas ----------
if (matchMedia('(hover: hover)').matches){
  $$('.spot').forEach(card => card.addEventListener('pointermove', e => {
    const r = card.getBoundingClientRect();
    card.style.setProperty('--mx', `${e.clientX - r.left}px`);
    card.style.setProperty('--my', `${e.clientY - r.top}px`);
  }));
}

// ---------- Proyectos: filtro y "ver todos" ----------
const chips = $$('.chip');
const cards = $$('.project');
const status = $('#filter-status');
const showAll = $('#show-all');
let filter = 'all';
let expanded = false;

function applyProjects(animate = true){
  let shown = 0, k = 0;
  cards.forEach(card => {
    const match = filter === 'all' || card.dataset.area === filter;
    // Con un filtro activo se muestran todos los del área; sin filtro se respeta "ver todos"
    const visible = match && (filter !== 'all' || expanded || !card.classList.contains('is-extra'));
    card.classList.toggle('is-hidden', !visible);
    card.classList.toggle('expanded', visible && card.classList.contains('is-extra'));
    if (visible){
      shown++;
      if (animate) card.classList.add('show'); // al cargar, cada tarjeta espera a entrar en pantalla
      if (animate && !reduceMotion){
        card.classList.remove('pop'); void card.offsetWidth;
        card.style.setProperty('--k', k++); card.classList.add('pop');
      }
    }
  });
  if (showAll) showAll.parentElement.hidden = filter !== 'all';
  if (status) status.textContent = `${shown} proyectos visibles`;
}
chips.forEach(chip => chip.addEventListener('click', () => {
  filter = chip.dataset.filter;
  chips.forEach(c => { const on = c === chip; c.classList.toggle('is-on', on); c.setAttribute('aria-pressed', String(on)); });
  applyProjects();
}));
if (showAll){
  const total = cards.length;
  showAll.addEventListener('click', () => {
    expanded = !expanded;
    showAll.setAttribute('aria-expanded', String(expanded));
    $('span', showAll).textContent = expanded ? 'Ver menos proyectos' : `Ver todos los proyectos (${total})`;
    applyProjects();
    if (!expanded) $('#proyectos').scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth' });
  });
}
applyProjects(false);

// ---------- Certificados del diplomado ----------
const lightbox = $('#lightbox');
const lbImg = $('#lightbox-img');
const lbPdf = $('#lightbox-pdf');
let lastFocus = null;
function openLightbox(item){
  lastFocus = document.activeElement;
  const isPdf = item.type === 'pdf';
  lbImg.hidden = isPdf; lbPdf.hidden = !isPdf;
  if (isPdf) lbPdf.src = item.file; else { lbImg.src = item.file; lbImg.alt = item.title; }
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

const dipBtn = $('#open-diplomas');
const dipPanel = $('#diploma-panel');
let dipLoaded = false;
async function loadDiplomas(){
  if (dipLoaded) return;
  dipLoaded = true;
  const grid = $('#diploma-grid');
  try {
    const list = await (await fetch('data/diplomas.json')).json();
    list.forEach((item, i) => {
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'diploma';
      b.style.setProperty('--i', i);
      b.setAttribute('aria-label', `Ver certificado: ${item.title}`);
      b.innerHTML = `<img src="${item.thumb}" alt="" loading="lazy"><span>${item.title}</span>`;
      b.addEventListener('click', () => openLightbox(item));
      grid.appendChild(b);
    });
  } catch (err) {
    grid.innerHTML = '<p>No se pudieron cargar los certificados.</p>';
  }
}
if (dipBtn){
  dipBtn.addEventListener('click', () => {
    const open = dipPanel.hidden;
    dipPanel.hidden = !open;
    dipBtn.setAttribute('aria-expanded', String(open));
    dipBtn.firstChild.textContent = open ? 'Ocultar certificados' : 'Ver los 8 certificados';
    if (open) loadDiplomas();
  });
}

// ---------- Copiar correo ----------
const toast = $('.toast');
let toastTimer;
function showToast(msg){
  toast.textContent = msg;
  toast.classList.add('show');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove('show'), 2200);
}
const copyBtn = $('#copy-mail');
if (copyBtn){
  copyBtn.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(copyBtn.dataset.mail);
      showToast('Correo copiado');
    } catch (err) {
      showToast('No se pudo copiar. Selecciona el correo y cópialo manualmente.');
    }
  });
}

// ---------- Video del portafolio: se reproduce al pasar el cursor ----------
$$('video.hover-play').forEach(v => {
  const box = v.closest('a') || v;
  box.addEventListener('mouseenter', () => v.play().catch(() => {}));
  box.addEventListener('mouseleave', () => v.pause());
});
