from pathlib import Path
import json
import re
from urllib.parse import urljoin

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://viajescasal-sketch.github.io/elkitdelviajero/"
DATE = "2026-07-19"

# Cada página responde a una intención distinta; no se repite una misma palabra clave en todo el sitio.
SEO = {
    "index.html": ("Accesorios de viaje y checklists | El Kit del Viajero", "Encuentra accesorios de viaje, mochilas de cabina, organizadores, adaptadores y checklists gratuitos para preparar tu equipaje y viajar mejor."),
    "blog/index.html": ("Guías de viaje, equipaje y checklists | Viajes Casal", "Consulta guías de viaje, listas de equipaje y consejos para viajar en avión, a Europa, Cancún o en familia con una preparación más sencilla."),
    "guias/index.html": ("Checklists de viaje gratis en PDF | Viajes Casal", "Descarga checklists de viaje gratis en PDF para Europa, playa, Disney, vuelos internacionales, viajes con niños y mochila de cabina."),
    "mochilas/index.html": ("Mochilas de cabina para viajar: guía y opciones", "Compara mochilas de cabina para viajar y aprende a revisar medidas, capacidad, apertura, comodidad y compatibilidad con la tarifa de tu aerolínea."),
    "powerbanks/index.html": ("Power banks para viajar: capacidad y carga rápida", "Compara power banks para viajar y conoce qué capacidad, potencia, puertos y reglas de transporte aéreo debes revisar antes de elegir una batería portátil."),
    "adaptadores/index.html": ("Adaptadores universales de viaje: guía para elegir", "Aprende a elegir un adaptador universal de viaje según el país, tipo de enchufe, puertos USB y voltaje para cargar tus dispositivos en el extranjero."),
    "candados-tsa/index.html": ("Candados TSA para maletas: guía de compra", "Descubre cómo elegir candados TSA para maletas y mochilas, qué revisar en la combinación y cuándo resultan útiles para proteger tu equipaje."),
    "organizadores/index.html": ("Organizadores de maleta: cómo elegir y empacar", "Compara organizadores de maleta y aprende a separar ropa, calzado y accesorios para aprovechar mejor el espacio y mantener ordenado tu equipaje."),
    "blog/accesorios-indispensables-para-viajar/index.html": ("Accesorios indispensables para viajar: lista práctica", "Conoce los accesorios indispensables para viajar cómodo y organizado: mochila de cabina, organizadores, báscula, adaptador, power bank y candado TSA."),
    "blog/checklist-para-viajar-en-avion/index.html": ("Checklist para viajar en avión: guía antes del vuelo", "Sigue esta checklist para viajar en avión: documentos, equipaje, check-in, líquidos, dispositivos y pendientes desde 48 horas antes del abordaje."),
    "blog/como-evitar-pagar-sobrepeso/index.html": ("Cómo evitar pagar sobrepeso de equipaje en el avión", "Aprende cómo evitar pagar sobrepeso de equipaje: revisa tu tarifa, pesa la maleta, distribuye mejor la ropa y deja margen antes de llegar al aeropuerto."),
    "blog/como-organizar-una-maleta/index.html": ("Cómo organizar una maleta y aprovechar el espacio", "Aprende cómo organizar una maleta paso a paso, combinar prendas, usar organizadores y distribuir el peso para encontrar todo con facilidad."),
    "blog/equipaje-permitido-por-aerolinea/index.html": ("Equipaje permitido por aerolínea: medidas y peso", "Consulta cómo verificar el equipaje permitido por tu aerolínea, las medidas y el peso incluidos en la tarifa, además de líquidos y objetos restringidos."),
    "blog/mejores-mochilas-de-cabina/index.html": ("Mejores mochilas de cabina: qué revisar antes de comprar", "Compara las mejores mochilas de cabina según capacidad, apertura, compartimento para laptop, comodidad y medidas permitidas por la aerolínea."),
    "blog/mejores-power-banks-para-viajar/index.html": ("Mejores power banks para viajar: guía de elección", "Descubre cómo elegir los mejores power banks para viajar según capacidad, potencia, puertos, cables integrados y reglas para transportarlos en avión."),
    "blog/que-llevar-a-cancun/index.html": ("Qué llevar a Cancún: lista de equipaje para playa", "Descubre qué llevar a Cancún con una lista práctica de ropa, protector solar, documentos, accesorios de playa y artículos útiles para clima tropical."),
    "blog/que-llevar-a-europa/index.html": ("Qué llevar a Europa: lista de equipaje y documentos", "Consulta qué llevar a Europa: documentos, ropa por capas, calzado cómodo, adaptador, conectividad y accesorios para recorrer varias ciudades."),
    "blog/que-llevar-si-viajas-con-ninos/index.html": ("Qué llevar si viajas con niños: checklist familiar", "Revisa qué llevar si viajas con niños: documentos, cambios de ropa, medicamentos, snacks, entretenimiento y accesorios para trayectos más tranquilos."),
    "blog/que-puedo-llevar-en-mochila-de-cabina-y-europa/index.html": ("Qué llevar en mochila de cabina y viaje a Europa", "Conoce qué puedes llevar en una mochila de cabina, las reglas de líquidos y objetos restringidos, más una lista práctica de equipaje para Europa."),
}

H1 = {
    "index.html": "Prepara mejor tu próximo viaje.",
    "blog/index.html": "Guías de viaje, equipaje y checklists para viajar mejor",
    "guias/index.html": "Checklists de viaje gratis para tu próximo destino",
}

CONTENT = {
    "blog/accesorios-indispensables-para-viajar/index.html": '<section class="seo-content" data-seo-content><h2>Accesorios de viaje que resuelven problemas reales</h2><p>Un buen kit no se mide por la cantidad de productos, sino por los inconvenientes que evita. La báscula ayuda a controlar el peso; los organizadores separan ropa limpia y usada; el adaptador permite conectar equipos en otros países y el power bank mantiene disponibles mapas y reservaciones durante traslados.</p><h3>Cómo priorizar tu compra</h3><ul><li>Primero elige lo obligatorio para tu destino y medio de transporte.</li><li>Después agrega lo que mejore organización, descanso o seguridad.</li><li>Evita duplicar funciones y revisa cuánto espacio ocupará cada accesorio.</li></ul></section>',
    "blog/checklist-para-viajar-en-avion/index.html": '<section class="seo-content" data-seo-content><h2>Qué revisar antes de viajar en avión</h2><p>Confirma el nombre de los pasajeros, vigencia de documentos, terminal, equipaje incluido y requisitos del destino. Haz el check-in cuando lo permita la aerolínea y guarda el pase de abordar también sin conexión.</p><h3>En la mochila de cabina</h3><ul><li>Documentos, medicamentos y objetos de valor.</li><li>Dispositivos cargados, cables y batería portátil permitida.</li><li>Líquidos preparados conforme a las reglas del aeropuerto.</li><li>Una muda ligera para retrasos o equipaje demorado.</li></ul></section>',
    "blog/como-evitar-pagar-sobrepeso/index.html": '<section class="seo-content" data-seo-content><h2>Cómo reducir el peso de la maleta</h2><p>Pesa la maleta terminada, no vacía, y compara el resultado con la franquicia de tu tarifa. Usa prendas combinables, lleva puestos los artículos más voluminosos y elimina envases grandes que puedas sustituir por presentaciones de viaje.</p><h3>Deja margen para el regreso</h3><p>No empacar hasta el límite reduce el riesgo de cargos por diferencias entre básculas y deja espacio para compras. Si viajan varias personas, revisa si la aerolínea permite distribuir el peso entre piezas antes de reorganizar el equipaje.</p></section>',
    "blog/como-organizar-una-maleta/index.html": '<section class="seo-content" data-seo-content><h2>Método para organizar una maleta por categorías</h2><p>Separa ropa, calzado, aseo, tecnología y documentos antes de guardar cualquier cosa. Forma conjuntos completos, enrolla las prendas flexibles y utiliza espacios interiores del calzado para objetos pequeños que no puedan dañarse.</p><h3>Distribución del peso</h3><p>En una maleta con ruedas, coloca lo más pesado cerca de la base para mejorar la estabilidad. Mantén líquidos dentro de bolsas cerradas y deja accesibles los artículos que necesitarás durante el trayecto. Destina un organizador vacío a la ropa usada.</p></section>',
    "blog/equipaje-permitido-por-aerolinea/index.html": '<section class="seo-content" data-seo-content><h2>Cómo consultar el equipaje incluido en tu tarifa</h2><p>Busca las condiciones dentro de tu reservación, porque una misma aerolínea puede vender tarifas con equipaje diferente. Distingue entre artículo personal, equipaje de mano y maleta documentada; anota las medidas, el peso y el número de piezas.</p><h3>Qué cambia entre vuelos</h3><p>Las reglas pueden variar cuando intervienen varias aerolíneas o vuelos operados por otra compañía. Confirma también baterías, líquidos, equipo deportivo y artículos especiales directamente con el transportista antes de llegar al aeropuerto.</p></section>',
    "blog/mejores-mochilas-de-cabina/index.html": '<section class="seo-content" data-seo-content><h2>Características de una buena mochila de cabina</h2><p>Busca una estructura que conserve sus medidas al llenarse, apertura amplia para empacar, correas acolchadas y un respaldo cómodo. Un compartimento separado facilita extraer la laptop durante el control de seguridad.</p><h3>Capacidad útil frente a tamaño anunciado</h3><p>Los litros orientan, pero no sustituyen las medidas exteriores. Comprueba la mochila llena y considera bolsillos, asas y correas. Si debe funcionar como artículo personal, prioriza un perfil compacto que pueda colocarse debajo del asiento.</p></section>',
    "blog/mejores-power-banks-para-viajar/index.html": '<section class="seo-content" data-seo-content><h2>Cómo elegir un power bank para viajar</h2><p>Relaciona la capacidad con la duración de tus trayectos y el número de dispositivos. La carga USB-C, la potencia compatible y los cables integrados pueden reducir accesorios, mientras que el indicador de batería ayuda a planear las recargas.</p><h3>Power banks en el avión</h3><p>Las baterías portátiles suelen requerir transporte en cabina y están sujetas a límites de capacidad definidos por las autoridades y la aerolínea. Revisa la etiqueta de Wh, protege los puertos y no viajes con baterías dañadas o hinchadas.</p></section>',
    "blog/que-llevar-a-cancun/index.html": '<section class="seo-content" data-seo-content><h2>Lista de equipaje para Cancún</h2><p>Combina ropa ligera y transpirable con dos trajes de baño, sandalias, calzado para caminar y una capa delgada para lugares con aire acondicionado. Añade sombrero, lentes de sol y una bolsa para separar prendas húmedas.</p><h3>Playa, excursiones y clima tropical</h3><p>El contenido cambia según el itinerario: para cenotes o parques acuáticos conviene llevar calzado que pueda mojarse y funda resistente al agua; para excursiones, una mochila pequeña y botella reutilizable. Consulta el pronóstico antes de cerrar la maleta.</p></section>',
    "blog/que-llevar-a-europa/index.html": '<section class="seo-content" data-seo-content><h2>Equipaje para recorrer varias ciudades de Europa</h2><p>Prioriza capas combinables, calzado ya probado y una prenda compacta para lluvia. Revisa el clima de cada ciudad y la disponibilidad de lavandería para evitar cargar conjuntos completos para todos los días.</p><h3>Documentos, enchufes y conectividad</h3><p>Guarda pasaporte, reservaciones, seguro y medios de pago de respaldo. Verifica el tipo de enchufe de cada país y recuerda que un adaptador no convierte voltaje. Descarga mapas y boletos para consultarlos durante traslados sin conexión.</p></section>',
    "blog/que-llevar-si-viajas-con-ninos/index.html": '<section class="seo-content" data-seo-content><h2>Cómo preparar el equipaje cuando viajas con niños</h2><p>Organiza una bolsa accesible con documentos, medicamentos, cambios de ropa, pañuelos, snacks permitidos y entretenimiento silencioso. Divide las porciones y los cambios por trayecto para no deshacer toda la maleta.</p><h3>Una reserva para imprevistos</h3><p>Añade un cambio adicional y suministros para posibles retrasos, pero evita cargar duplicados innecesarios. Confirma con la aerolínea las reglas para carriolas, sillas infantiles, alimentos y líquidos destinados a menores.</p></section>',
}

CATEGORY_NAMES = {
    "mochilas": "Mochilas de cabina",
    "powerbanks": "Power banks para viajar",
    "adaptadores": "Adaptadores universales",
    "candados-tsa": "Candados TSA",
    "organizadores": "Organizadores de maleta",
    "blog": "Guías de viaje",
    "guias": "Checklists de viaje",
}

def canonical_for(rel):
    if rel == "index.html": return BASE
    return BASE + rel.removesuffix("index.html")

def first_image(text, rel):
    match = re.search(r'<img[^>]+src="([^"]+)"', text, re.I)
    src = match.group(1) if match else "assets/productos/mochila-cabina.webp"
    if src.startswith("http"): return src
    return urljoin(canonical_for(rel), src)

def add_or_replace_meta(text, key, value, prop=False):
    attr = "property" if prop else "name"
    pattern = rf'<meta\s+{attr}="{re.escape(key)}"\s+content="[^"]*"\s*/?>'
    tag = f'<meta {attr}="{key}" content="{value}">'
    if re.search(pattern, text, flags=re.I):
        return re.sub(pattern, tag, text, count=1, flags=re.I)
    return text.replace("</head>", tag + "</head>", 1)

def improve_json_ld(text, image, canonical):
    pattern = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.S)
    def change(m):
        try: data = json.loads(m.group(1))
        except Exception: return m.group(0)
        entities = data.get("@graph", []) if isinstance(data, dict) and "@graph" in data else [data]
        for entity in entities:
            if not isinstance(entity, dict): continue
            if entity.get("@type") in ("Article", "BlogPosting"):
                entity["image"] = image
                entity["dateModified"] = DATE
                entity.setdefault("author", {"@type":"Organization","name":"Viajes Casal","url":BASE})
            if entity.get("@type") in ("WebPage", "CollectionPage"):
                entity.setdefault("primaryImageOfPage", image)
        return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "</script>"
    return pattern.sub(change, text)

def breadcrumb_schema(rel, canonical):
    parts = Path(rel).parts[:-1]
    items = [{"@type":"ListItem","position":1,"name":"Inicio","item":BASE}]
    if not parts: return None
    if parts[0] == "blog":
        items.append({"@type":"ListItem","position":2,"name":"Guías de viaje","item":BASE+"blog/"})
        if len(parts) > 1:
            title = SEO[rel][0].split(" |")[0].split(":")[0]
            items.append({"@type":"ListItem","position":3,"name":title,"item":canonical})
    else:
        items.append({"@type":"ListItem","position":2,"name":CATEGORY_NAMES.get(parts[0], parts[0].replace("-"," ").title()),"item":canonical})
    return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":items}

for rel, (title, desc) in SEO.items():
    path = ROOT / rel
    text = path.read_text(encoding="utf-8")
    canonical = canonical_for(rel)
    image = first_image(text, rel)
    text = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", text, count=1, flags=re.S|re.I)
    text = add_or_replace_meta(text, "description", desc)
    text = add_or_replace_meta(text, "robots", "index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1")
    text = add_or_replace_meta(text, "author", "Viajes Casal")
    text = add_or_replace_meta(text, "og:title", title, True)
    text = add_or_replace_meta(text, "og:description", desc, True)
    text = add_or_replace_meta(text, "og:url", canonical, True)
    text = add_or_replace_meta(text, "og:site_name", "El Kit del Viajero", True)
    text = add_or_replace_meta(text, "og:locale", "es_MX", True)
    text = add_or_replace_meta(text, "og:image", image, True)
    text = add_or_replace_meta(text, "twitter:card", "summary_large_image")
    text = add_or_replace_meta(text, "twitter:title", title)
    text = add_or_replace_meta(text, "twitter:description", desc)
    text = add_or_replace_meta(text, "twitter:image", image)
    if 'rel="alternate" hreflang="es-MX"' not in text:
        text = text.replace("</head>", f'<link rel="alternate" hreflang="es-MX" href="{canonical}"><link rel="alternate" hreflang="x-default" href="{canonical}"></head>', 1)
    if rel in H1:
        text = re.sub(r"(<h1>).*?(</h1>)", rf"\1{H1[rel]}\2", text, count=1, flags=re.S)
    if rel in CONTENT and "data-seo-content" not in text:
        marker = '<div class="product-cta">'
        text = text.replace(marker, CONTENT[rel] + marker, 1)
    text = improve_json_ld(text, image, canonical)
    crumb = breadcrumb_schema(rel, canonical)
    if crumb and '"@type":"BreadcrumbList"' not in text:
        text = text.replace("</head>", '<script type="application/ld+json">'+json.dumps(crumb,ensure_ascii=False,separators=(",",":"))+"</script></head>", 1)
    path.write_text(text, encoding="utf-8")

sitemap = ROOT / "sitemap.xml"
text = sitemap.read_text(encoding="utf-8")
text = re.sub(r"<lastmod>[^<]+</lastmod>", f"<lastmod>{DATE}</lastmod>", text)
sitemap.write_text(text, encoding="utf-8")
print(f"Optimized {len(SEO)} pages")
