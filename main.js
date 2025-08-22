
// Mobile nav
const navToggle = document.querySelector('.nav-toggle');
const navMenu = document.querySelector('.nav-menu');
if (navToggle) {
  navToggle.addEventListener('click', () => navMenu.classList.toggle('show'));
}

// Theme toggle (light/dark)
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

// Contact form (demo only)
const form = document.getElementById('contactForm');
const result = document.querySelector('.form-result');
if(form){
  form.addEventListener('submit', (e)=>{
    e.preventDefault();
    const data = Object.fromEntries(new FormData(form).entries());
    result.textContent = `¡Gracias, ${data.nombre}! Te responderé pronto a ${data.correo}.`;
    form.reset();
  });
}
