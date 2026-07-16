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
