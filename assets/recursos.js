document.querySelectorAll('[data-lead-form]').forEach(form=>{form.addEventListener('submit',event=>{event.preventDefault();const email=form.querySelector('input[type="email"]');if(!email?.checkValidity()){email?.reportValidity();return}const guide=form.dataset.guide||'recursos';try{localStorage.setItem('kitViajeroLead',JSON.stringify({email:email.value.trim(),guide,date:new Date().toISOString()}))}catch{}form.querySelectorAll('[data-download]').forEach(link=>link.classList.add('visible'));const message=form.querySelector('.form-message');if(message)message.textContent='¡Listo! Tus guías ya están disponibles para descargar.';form.querySelector('button').textContent='Guías desbloqueadas';form.querySelector('button').disabled=true})});

// Al abrir el sitio directamente desde el disco, los navegadores no siempre
// resuelven una carpeta a su index.html. Este ajuste mantiene operativa la
// navegación local sin cambiar las URLs limpias usadas por GitHub Pages.
if(location.protocol==='file:')document.querySelectorAll('a[href$="/"]').forEach(link=>{link.href=link.href+'index.html'});
