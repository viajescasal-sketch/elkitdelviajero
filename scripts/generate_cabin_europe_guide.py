from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, KeepTogether

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "pdf" / "guia-mochila-cabina-europa.pdf"
OUT.parent.mkdir(parents=True, exist_ok=True)

NAVY = colors.HexColor("#06324A")
DEEP = colors.HexColor("#021F31")
TEAL = colors.HexColor("#08A9B5")
CREAM = colors.HexColor("#F6F3EA")
INK = colors.HexColor("#173142")
MUTED = colors.HexColor("#5E7280")
GOLD = colors.HexColor("#D7A928")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="CoverTitle", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=30, leading=34, textColor=colors.white, alignment=TA_CENTER, spaceAfter=16))
styles.add(ParagraphStyle(name="CoverSub", parent=styles["BodyText"], fontSize=13, leading=19, textColor=colors.HexColor("#D9F5F6"), alignment=TA_CENTER))
styles.add(ParagraphStyle(name="H1x", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=22, leading=26, textColor=NAVY, spaceAfter=12))
styles.add(ParagraphStyle(name="H2x", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=14, leading=18, textColor=NAVY, spaceBefore=10, spaceAfter=7))
styles.add(ParagraphStyle(name="Bodyx", parent=styles["BodyText"], fontSize=9.8, leading=14.2, textColor=INK, spaceAfter=7))
styles.add(ParagraphStyle(name="Smallx", parent=styles["BodyText"], fontSize=7.6, leading=10.5, textColor=MUTED))
styles.add(ParagraphStyle(name="Boxx", parent=styles["BodyText"], fontSize=9.2, leading=13.5, textColor=INK, backColor=CREAM, borderColor=TEAL, borderWidth=1, borderPadding=10, spaceAfter=12))

def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#DCE7EB"))
    canvas.line(18*mm, 14*mm, 192*mm, 14*mm)
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(18*mm, 9*mm, "El Kit del Viajero by Viajes Casal")
    canvas.drawRightString(192*mm, 9*mm, f"Página {doc.page}")
    canvas.restoreState()

def bullets(items):
    return [Paragraph(f"<b>-</b> {item}", styles["Bodyx"]) for item in items]

doc = SimpleDocTemplate(str(OUT), pagesize=A4, rightMargin=18*mm, leftMargin=18*mm, topMargin=18*mm, bottomMargin=19*mm, title="Guía de mochila de cabina y Europa", author="Viajes Casal")
story = [Spacer(1, 38*mm), Paragraph("EL KIT DEL VIAJERO", ParagraphStyle(name="Eyebrow", parent=styles["BodyText"], alignment=TA_CENTER, fontName="Helvetica-Bold", fontSize=10, textColor=GOLD, tracking=2)), Spacer(1, 8*mm), Paragraph("Mochila de cabina<br/>y viaje a Europa", styles["CoverTitle"]), Paragraph("Qué puedes llevar, qué debes evitar y una lista práctica para empacar sin improvisar.", styles["CoverSub"]), Spacer(1, 22*mm)]
cover = Table([[story]], colWidths=[174*mm], rowHeights=[247*mm])
cover.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),DEEP),("VALIGN",(0,0),(-1,-1),"MIDDLE"),("LEFTPADDING",(0,0),(-1,-1),16*mm),("RIGHTPADDING",(0,0),(-1,-1),16*mm)]))
flow = [cover, PageBreak()]

flow += [Paragraph("1. Antes de empacar: confirma tu tarifa", styles["H1x"]), Paragraph("'Mochila no documentada' puede significar artículo personal o equipaje de mano. No son lo mismo. La aerolínea define cuántas piezas incluye tu tarifa, sus medidas y su peso.", styles["Boxx"])]
flow += bullets(["Abre tu reservación y localiza las reglas de equipaje del vuelo exacto.", "Mide la mochila llena, incluyendo asas, ruedas y bolsillos.", "Pesa el equipaje en casa y deja margen para compras del regreso.", "Guarda documentos, medicinas y objetos de valor en la pieza que permanecerá contigo."])
flow += [Paragraph("Regla de líquidos en aeropuertos de la Unión Europea", styles["H2x"]), Paragraph("Los líquidos de cabina deben ir en envases individuales de hasta 100 ml dentro de una bolsa transparente resellable de hasta 1 litro. Los recipientes mayores normalmente deben documentarse, salvo excepciones como medicamentos y comida para bebé cuando sean necesarios durante el viaje.", styles["Bodyx"]), Paragraph("Incluye geles, cremas, pastas, aerosoles, perfumes y mezclas líquido-sólido. La decisión final corresponde al control de seguridad y pueden pedirte mostrar los artículos por separado.", styles["Bodyx"]), PageBreak()]

flow += [Paragraph("2. Qué sí llevar en la mochila de cabina", styles["H1x"])]
flow += bullets(["Pasaporte, identificación, tarjetas, reservas y copias digitales protegidas.", "Celular, cámara, audífonos, cargadores y adaptador de enchufe.", "Power bank y baterías de repuesto protegidas contra cortocircuitos; confirma el límite de capacidad con la aerolínea.", "Medicamentos necesarios, idealmente en su empaque y con receta o justificante cuando aplique.", "Una muda ligera, ropa interior, capa térmica o suéter y una prenda impermeable compacta.", "Artículos de aseo que cumplan la regla de 100 ml y la bolsa de 1 litro.", "Snacks sólidos permitidos por el control; revisa las reglas de entrada de alimentos del país de destino."])
flow += [Paragraph("Qué no debes llevar o requiere verificación", styles["H2x"])]
flow += bullets(["Armas, municiones, explosivos, fuegos artificiales y aerosoles de defensa.", "Combustibles, sustancias inflamables, tóxicas o corrosivas.", "Objetos punzocortantes y herramientas que puedan causar lesiones.", "Envases de líquidos mayores de 100 ml fuera de las excepciones permitidas.", "Baterías dañadas, hinchadas o retiradas del mercado."])
flow += [Paragraph("Importante: esta es una guía general. Antes de salir revisa la lista de objetos prohibidos de tu aerolínea, el aeropuerto de conexión y el país de destino.", styles["Boxx"]), PageBreak()]

flow += [Paragraph("3. Lista compacta para Europa", styles["H1x"])]
cols = [[Paragraph("Documentos", styles["H2x"]), Paragraph("Ropa y calzado", styles["H2x"])], [Paragraph("[ ] Pasaporte vigente<br/>[ ] Reservas y boletos<br/>[ ] Seguro de viaje<br/>[ ] Medios de pago<br/>[ ] Copias seguras", styles["Bodyx"]), Paragraph("[ ] Capas combinables<br/>[ ] Zapatos caminables<br/>[ ] Chaqueta ligera<br/>[ ] Ropa interior<br/>[ ] Prenda para lluvia", styles["Bodyx"])], [Paragraph("Tecnología", styles["H2x"]), Paragraph("Uso diario", styles["H2x"])], [Paragraph("[ ] Adaptador europeo<br/>[ ] Cargadores<br/>[ ] Power bank<br/>[ ] eSIM/SIM o roaming<br/>[ ] Mapas sin conexión", styles["Bodyx"]), Paragraph("[ ] Botella vacía<br/>[ ] Mochila de día<br/>[ ] Bolsa para líquidos<br/>[ ] Medicinas<br/>[ ] Lentes y protector solar", styles["Bodyx"])]]
t = Table(cols, colWidths=[84*mm,84*mm])
t.setStyle(TableStyle([("GRID",(0,0),(-1,-1),.6,colors.HexColor("#DCE7EB")),("BACKGROUND",(0,0),(-1,0),CREAM),("BACKGROUND",(0,2),(-1,2),CREAM),("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),10),("RIGHTPADDING",(0,0),(-1,-1),10)]))
flow += [t, Spacer(1,6*mm), Paragraph("Europa en 2026", styles["H2x"]), Paragraph("El Sistema de Entradas y Salidas (EES) está plenamente operativo desde el 10 de abril de 2026. ETIAS está previsto para el último trimestre de 2026; la Unión Europea indica que todavía no hay que solicitarlo hasta que anuncie la fecha exacta. Verifica la información oficial poco antes de viajar.", styles["Boxx"]), PageBreak()]

flow += [Paragraph("4. Revisión final en 10 minutos", styles["H1x"])]
flow += bullets(["Confirma puerta, terminal y hora límite de llegada.", "Revisa nuevamente peso y dimensiones de la mochila.", "Separa líquidos y dispositivos para el control de seguridad.", "Carga el celular y el power bank.", "Descarga mapas, boletos y póliza para consultarlos sin internet.", "Lleva el pasaporte y los medicamentos en un bolsillo seguro y accesible.", "Deja espacio para recuerdos o planea una bolsa plegable."])
flow += [Paragraph("Fuentes oficiales consultadas", styles["H2x"]), Paragraph("Unión Europea - restricciones de equipaje: europa.eu/youreurope/citizens/travel/carry/luggage-restrictions/<br/>Comisión Europea - líquidos, aerosoles y geles: transport.ec.europa.eu/transport-modes/air/aviation-security/aviation-security-policy/liquids-aerosols-and-gels_en<br/>Unión Europea - ETIAS: travel-europe.europa.eu/etias/ltr/about-etias/what-is-etias.html", styles["Smallx"]), Spacer(1,8*mm), Paragraph("¿Quieres seguir preparando tu viaje?", styles["H2x"]), Spacer(1,3*mm), Paragraph("Visita viajescasal-sketch.github.io/elkitdelviajero para consultar productos, artículos y checklists. Viajes Casal puede ayudarte a cotizar tu siguiente experiencia.", styles["Boxx"]), Paragraph("Actualizado el 19 de julio de 2026. Las reglas pueden cambiar; confirma siempre con tu aerolínea, aeropuerto y autoridades del destino.", styles["Smallx"])]

doc.build(flow, onFirstPage=footer, onLaterPages=footer)
print(OUT)
