// Tema claro/oscuro
const themeToggle = document.getElementById('themeToggle');
const root = document.documentElement;
const storedTheme = localStorage.getItem('theme');
if (storedTheme) root.classList.toggle('light', storedTheme === 'light');

themeToggle?.addEventListener('click', () => {
  const nowLight = !root.classList.contains('light');
  root.classList.toggle('light', nowLight);
  localStorage.setItem('theme', nowLight ? 'light' : 'dark');
});

// Año dinámico
document.getElementById('year')?.appendChild(document.createTextNode(new Date().getFullYear()));

// Menú móvil
const hamburger = document.getElementById('hamburger');
const navLinks = document.getElementById('navLinks');
hamburger?.addEventListener('click', () => navLinks.classList.toggle('open'));

// Filtro de proyectos
const filters = document.querySelectorAll('.filter');
const cards = document.querySelectorAll('.project');
filters.forEach(btn => {
  btn.addEventListener('click', () => {
    filters.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const type = btn.dataset.filter;
    cards.forEach(c => {
      c.style.display = (type === 'all' || c.dataset.type === type) ? '' : 'none';
    });
  });
});

// Botón volver arriba
const toTop = document.getElementById('toTop');
window.addEventListener('scroll', () => {
  if (window.scrollY > 500) toTop.classList.add('show');
  else toTop.classList.remove('show');
});
toTop?.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));

// Animaciones al hacer scroll
const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) entry.target.classList.add('reveal');
  });
}, { threshold: .12 });

document.querySelectorAll('.section .container, .card, .skill').forEach(el => {
  el.classList.add('will-reveal');
  observer.observe(el);
});
