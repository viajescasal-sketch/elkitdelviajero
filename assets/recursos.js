const SUBSCRIPTION_ENDPOINT='https://kit-viajero-brevo.viajesbumerancasal.workers.dev/suscribir';
document.querySelectorAll('[data-lead-form]').forEach(form=>{
  const downloads=form.querySelector('.download-list');
  const consent=document.createElement('label');
  consent.className='privacy-consent';
  consent.innerHTML='<span class="consent-row"><input type="checkbox" name="privacyAccepted" required> <span>Acepto el <a href="../aviso-privacidad.html" target="_blank" rel="noopener">Aviso de Privacidad</a> y autorizo el uso de mi correo para recibir las guías solicitadas.</span></span><span class="consent-row"><input type="checkbox" name="promoAccepted"> <span>También deseo recibir promociones, novedades y recomendaciones de viaje. Esta autorización es opcional.</span></span><input class="website-field" type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">';
  form.insertBefore(consent,downloads);
  form.addEventListener('submit',async event=>{
    event.preventDefault();
    if(!form.reportValidity())return;
    const email=form.querySelector('input[type="email"]');
    const button=form.querySelector('button');
    const message=form.querySelector('.form-message');
    button.disabled=true;button.textContent='Registrando…';message.textContent='';
    try{
      const response=await fetch(SUBSCRIPTION_ENDPOINT,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email:email.value.trim(),privacyAccepted:form.elements.privacyAccepted.checked,promoAccepted:form.elements.promoAccepted.checked,website:form.elements.website.value})});
      if(!response.ok)throw new Error('subscription_failed');
      try{localStorage.setItem('kitViajeroLead',JSON.stringify({email:email.value.trim(),guide:form.dataset.guide||'recursos',date:new Date().toISOString()}))}catch{}
      form.querySelectorAll('[data-download]').forEach(link=>link.classList.add('visible'));
      message.textContent='¡Listo! Tus guías están disponibles y enviamos una copia a tu correo.';
      button.textContent='Guías desbloqueadas';
    }catch{
      message.textContent='No pudimos registrar tu correo. Intenta nuevamente en unos minutos.';
      button.disabled=false;button.textContent='Desbloquear guías';
    }
  });
});

// Al abrir el sitio directamente desde el disco, los navegadores no siempre
// resuelven una carpeta a su index.html. Este ajuste mantiene operativa la
// navegación local sin cambiar las URLs limpias usadas por GitHub Pages.
if(location.protocol==='file:')document.querySelectorAll('a[href$="/"]').forEach(link=>{link.href=link.href+'index.html'});

// Convierte las categorías del blog en un menú compacto con destinos útiles.
const resourceDestinations=[
  'accesorios-indispensables-para-viajar/index.html',
  'que-llevar-a-cancun/index.html',
  'que-llevar-a-europa/index.html',
  'que-llevar-si-viajas-con-ninos/index.html',
  'checklist-para-viajar-en-avion/index.html',
  'mejores-mochilas-de-cabina/index.html',
  'checklist-para-viajar-en-avion/index.html',
  'como-evitar-pagar-sobrepeso/index.html'
];
const resourceLabels=['Accesorios esenciales','Lista para Cancún','Guía para Europa','Viajar con niños','Checklist de avión','Mochilas de cabina','Antes de abordar','Evita el sobrepeso'];
const resourceGrid=document.querySelector('.section.alt .grid');
if(resourceGrid){
  resourceGrid.className='resource-menu';
  [...resourceGrid.children].forEach((card,index)=>{
    const icon=card.querySelector('.category-icon')?.textContent||'→';
    const title=card.querySelector('h3')?.textContent||'Recurso';
    const link=document.createElement('a');
    link.className='resource-menu-item';
    link.href=resourceDestinations[index]||'index.html';
    link.setAttribute('aria-label',`${title}: ${resourceLabels[index]||'ver guía'}`);
    link.innerHTML=`<span class="category-icon" aria-hidden="true">${icon}</span><span class="resource-menu-copy"><strong>${title}</strong><small>${resourceLabels[index]||'Ver guía'}</small></span><span class="resource-menu-arrow" aria-hidden="true">→</span>`;
    card.replaceWith(link);
  });
}

// Buscador contextual para Blog y Guías. Se abre solo cuando el usuario lo necesita.
const searchableCarousel=document.querySelector('.article-carousel');
if(searchableCarousel){
  const isGuideLibrary=location.pathname.includes('/guias/');
  const searchLabel=isGuideLibrary?'Buscar guía':'Buscar artículo';
  const searchPlaceholder=isGuideLibrary?'Ej. playa, Europa, niños...':'Ej. equipaje, Cancún, documentos...';
  const search=document.createElement('div');
  search.className='context-search';
  search.innerHTML=`<button class="context-search-toggle" type="button" aria-expanded="false">🔍 ${searchLabel}</button><div class="context-search-field"><input type="search" placeholder="${searchPlaceholder}" aria-label="${searchLabel}"><button class="context-search-close" type="button" aria-label="Cerrar búsqueda">×</button></div>`;
  searchableCarousel.parentElement.insertBefore(search,searchableCarousel);
  const empty=document.createElement('p');
  empty.className='context-search-empty';
  empty.textContent='No encontramos coincidencias. Prueba con otra palabra o explora las categorías disponibles.';
  searchableCarousel.insertAdjacentElement('afterend',empty);
  const toggle=search.querySelector('.context-search-toggle');
  const input=search.querySelector('input');
  const normalize=value=>value.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().trim();
  const filterContent=()=>{
    const query=normalize(input.value);
    let visible=0;
    searchableCarousel.querySelectorAll('.card').forEach(card=>{
      const match=!query||normalize(card.textContent).includes(query);
      card.classList.toggle('search-filtered',!match);
      if(match)visible++;
    });
    document.querySelectorAll('.resource-menu-item').forEach(item=>item.classList.toggle('search-filtered',!!query&&!normalize(item.textContent).includes(query)));
    empty.classList.toggle('is-visible',visible===0);
    searchableCarousel.scrollTo({left:0,behavior:'smooth'});
  };
  toggle.addEventListener('click',()=>{search.classList.add('is-open');toggle.setAttribute('aria-expanded','true');input.focus()});
  search.querySelector('.context-search-close').addEventListener('click',()=>{input.value='';search.classList.remove('is-open');toggle.setAttribute('aria-expanded','false');filterContent()});
  input.addEventListener('input',filterContent);
}
