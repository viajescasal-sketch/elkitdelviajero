from pathlib import Path

root = Path(__file__).resolve().parents[1]

blog = root / "blog" / "index.html"
text = blog.read_text(encoding="utf-8")
card = '<article class="card has-image"><img class="card-image" src="https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=1200&q=84" alt="Mochila preparada para viajar en avión" loading="lazy"><div class="card-content"><span class="kicker" style="color:var(--turquoise)">Equipaje · Europa</span><h3>Qué llevar en una mochila de cabina y a Europa</h3><p>Reglas de líquidos, objetos restringidos y una lista práctica actualizada.</p><span class="meta">9 min de lectura · Actualizado 2026</span><a href="que-puedo-llevar-en-mochila-de-cabina-y-europa/index.html">Leer guía →</a></div></article>'
needle = "</div></div></section></main><footer"
if "que-puedo-llevar-en-mochila-de-cabina-y-europa" not in text:
    text = text.replace(needle, card + needle, 1)
blog.write_text(text, encoding="utf-8")

text = blog.read_text(encoding="utf-8")
whatsapp_cta = '<section class="whatsapp-channel"><div class="container"><div class="whatsapp-channel-box"><div class="whatsapp-channel-icon" aria-hidden="true">💬</div><div class="whatsapp-channel-copy"><span class="kicker">Comunidad Viajes Casal</span><h2>Más tips de viaje en nuestro canal de WhatsApp</h2><p>Recibe noticias, recomendaciones prácticas y promociones especiales directamente en WhatsApp.</p></div><a class="button whatsapp-channel-button" href="https://whatsapp.com/channel/0029VbDHt3IB4hdQ0VezRG0Y" target="_blank" rel="noopener">Unirme al canal</a></div></div></section>'
if "0029VbDHt3IB4hdQ0VezRG0Y" not in text:
    text = text.replace("</main><footer", whatsapp_cta + "</main><footer", 1)
blog.write_text(text, encoding="utf-8")

guides = root / "guias" / "index.html"
text = guides.read_text(encoding="utf-8")
text = text.replace("5 guías en PDF", "6 guías en PDF", 1).replace("las cinco descargas", "las seis descargas", 1)
text = text.replace(" Tu configuración de email marketing puede conectarse después en <code>assets/recursos.js</code>.", " Recibirás el acceso por correo y podrás descargar cada archivo desde esta página.", 1)
guide_card = '<article class="card has-image"><img class="card-image" src="https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=1200&q=84" alt="Guía de mochila de cabina y Europa" loading="lazy"><div class="card-content"><span class="category-icon">📄</span><h3>Mochila de cabina y Europa</h3><p>Qué llevar, qué evitar y una lista completa para empacar.</p><span class="meta">PDF gratuito · 5 páginas</span></div></article>'
section_needle = '</div></div></section><section class="section alt">'
if "Mochila de cabina y Europa</h3>" not in text:
    text = text.replace(section_needle, guide_card + section_needle, 1)
download = '<a class="download-link" data-download href="../output/pdf/guia-mochila-cabina-europa.pdf" download>Descargar guía Mochila de cabina y Europa →</a>'
download_needle = "</div></form></div>"
if "guia-mochila-cabina-europa.pdf" not in text:
    text = text.replace(download_needle, download + download_needle, 1)
guides.write_text(text, encoding="utf-8")
