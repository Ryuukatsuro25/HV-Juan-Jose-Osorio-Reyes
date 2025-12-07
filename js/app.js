// Helpers
const $ = (q, c=document) => c.querySelector(q);
const $$ = (q, c=document) => [...c.querySelectorAll(q)];
document.documentElement.classList.remove('no-js');

// Year
$("#year") && ($("#year").textContent = new Date().getFullYear());

// Theme
const root = document.documentElement;
const savedTheme = localStorage.getItem('theme');
if(savedTheme){
  root.classList.toggle('light', savedTheme === 'light');
}
$("#themeToggle")?.addEventListener('click', ()=>{
  const isLight = root.classList.toggle('light');
  localStorage.setItem('theme', isLight ? 'light' : 'dark');
});

// Reveal on scroll
const revealEls = $$('.reveal');
const onScroll = ()=>{
  const h = window.innerHeight;
  revealEls.forEach(el=>{
    const rect = el.getBoundingClientRect();
    if(rect.top < h - 80){
      el.classList.add('visible');
    }
  });
};
window.addEventListener('scroll', onScroll);
onScroll();

// Diplomas lightbox
async function loadDiplomas(){
  try{
    const res = await fetch('data/diplomas.json');
    const data = await res.json();
    const container = $('#diplomasList');
    if(!container) return;
    container.innerHTML = '';
    data.forEach(item=>{
      const tile = document.createElement('article');
      tile.className = 'tile hoverable reveal';
      tile.innerHTML = `
        <div class="tile-icon">
          <img src="assets/icons/pdf.svg" alt="" class="icon" />
        </div>
        <div class="tile-body">
          <h3>${item.title}</h3>
          <p>${item.institution}</p>
        </div>
      `;
      tile.addEventListener('click', ()=>{
        openLightbox(item);
      });
      container.appendChild(tile);
    });
    onScroll();
  }catch(e){
    console.error('Error cargando diplomas', e);
  }
}

function openLightbox(item){
  const box = $("#lightbox");
  if(!box) return;
  const pdfFrame = $("#lightbox-pdf");
  const img = $("#lightbox-img");
  if(item.type === 'pdf'){
    pdfFrame.style.display = 'block';
    img.style.display = 'none';
    pdfFrame.src = item.src;
  }else{
    pdfFrame.style.display = 'none';
    img.style.display = 'block';
    img.src = item.src;
  }
  box.classList.add('show');
  box.setAttribute('aria-hidden','false');
}

$(".lightbox-close")?.addEventListener('click', ()=>{
  const box = $("#lightbox");
  $("#lightbox-img").src = '';
  $("#lightbox-pdf").src = '';
  box.classList.remove('show');
  box.setAttribute('aria-hidden','true');
});

loadDiplomas();
