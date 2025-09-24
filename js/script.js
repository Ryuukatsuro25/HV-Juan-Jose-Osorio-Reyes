
const themeToggle = document.getElementById('themeToggle');
const storedTheme = localStorage.getItem('theme');
if(storedTheme) document.documentElement.dataset.theme = storedTheme;
themeToggle?.addEventListener('click', ()=>{
  const next = document.documentElement.dataset.theme === 'light' ? 'dark' : 'light';
  document.documentElement.dataset.theme = next;
  localStorage.setItem('theme', next);
});
const hamburger = document.getElementById('hamburger');
const nav = document.getElementById('navLinks');
function toggleNav(force){
  const willOpen = force ?? !nav.classList.contains('open');
  nav.classList.toggle('open', willOpen);
  hamburger?.setAttribute('aria-expanded', String(willOpen));
}
hamburger?.addEventListener('click', ()=> toggleNav());
document.addEventListener('keydown', (e)=>{
  if(e.key === 'Escape' && nav.classList.contains('open')) toggleNav(false);
});
const filterButtons = [...document.querySelectorAll('.filter')];
const cards = [...document.querySelectorAll('.project')];
filterButtons.forEach(btn => {
  btn.addEventListener('click', () => {
    filterButtons.forEach(b => { b.classList.remove('active'); b.setAttribute('aria-selected','false'); });
    btn.classList.add('active'); btn.setAttribute('aria-selected','true');
    const type = btn.dataset.filter;
    cards.forEach(card => {
      const show = type === 'all' || card.dataset.type === type;
      card.hidden = !show;
    });
  });
});
const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
if(!reduceMotion && 'IntersectionObserver' in window){
  const io = new IntersectionObserver((entries)=>{
    entries.forEach(e=>{ if(e.isIntersecting) e.target.classList.add('reveal'); });
  },{threshold:.12});
  document.querySelectorAll('.will-reveal').forEach(el=> io.observe(el));
}
