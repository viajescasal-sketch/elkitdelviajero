from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output'/'pdf';OUT.mkdir(parents=True,exist_ok=True)
guides={
'checklist-playa':('Checklist para playa',[('Documentos',['Identificación y reservas','Seguro y contactos','Dinero y tarjeta']),('Equipaje',['Trajes de baño','Ropa ligera','Sandalias y calzado cómodo','Bolsa para ropa húmeda']),('Sol y agua',['Protector solar','Sombrero y lentes','Botella reutilizable','Repelente']),('Tecnología',['Power bank','Cargadores','Funda impermeable'])]),
'checklist-internacional':('Checklist internacional',[('Documentos',['Pasaporte vigente','Visas o autorizaciones','Seguro de viaje','Copias digitales']),('Dinero',['Avisar al banco','Tarjeta alternativa','Moneda para llegada']),('Conectividad',['eSIM o roaming','Adaptador universal','Power bank']),('Antes de salir',['Check-in','Traslado al aeropuerto','Reservas sin conexión'])]),
'checklist-europa':('Checklist Europa',[('Ruta',['Reservas de transporte','Entradas con horario','Mapas sin conexión']),('Equipaje',['Prendas por capas','Impermeable compacto','Calzado ya probado','Mochila de día']),('Tecnología',['Adaptador compatible','Power bank','Cable extra']),('Documentos',['Pasaporte','Seguro','Copias de reservas'])]),
'checklist-disney':('Checklist Disney',[('Antes del parque',['Entradas y reservas','Aplicación actualizada','Plan de transporte']),('Mochila',['Botella reutilizable','Protector solar','Poncho compacto','Snacks permitidos']),('Tecnología',['Power bank','Cable corto','Espacio en el teléfono']),('Familia',['Identificación para niños','Cambio de ropa','Punto de encuentro'])]),
'checklist-viaje-con-ninos':('Checklist viaje con niños',[('Documentos',['Identificaciones','Permisos necesarios','Seguro y contactos']),('Trayecto',['Snacks','Agua','Entretenimiento sin conexión','Audífonos infantiles']),('Equipaje',['Cambio completo accesible','Organizadores por persona','Bolsa para ropa usada']),('Salud',['Medicamentos','Recetas','Toallitas y gel'])]),
}

navy=HexColor('#06324a');deep=HexColor('#021f31');aqua=HexColor('#08a9b5');cream=HexColor('#f6f3ea');muted=HexColor('#5e7280')

def footer(c,page):
 c.setFillColor(deep);c.rect(0,0,A4[0],38,fill=1,stroke=0);c.setFillColorRGB(1,1,1);c.setFont('Helvetica',8);c.drawString(40,15,'El Kit del Viajero by Viajes Casal');c.drawRightString(A4[0]-40,15,f'Página {page}')

for slug,(title,sections) in guides.items():
 p=OUT/f'{slug}.pdf';c=canvas.Canvas(str(p),pagesize=A4,title=title,author='Viajes Casal')
 c.setFillColor(deep);c.rect(0,0,A4[0],A4[1],fill=1,stroke=0);c.setFillColor(aqua);c.setFont('Helvetica-Bold',11);c.drawString(44,A4[1]-80,'EL KIT DEL VIAJERO · GUÍA GRATUITA')
 c.setFillColorRGB(1,1,1);c.setFont('Helvetica-Bold',30);y=A4[1]-145
 for line in title.split(' para '): c.drawString(44,y,line);y-=38
 c.setFont('Helvetica',13);c.setFillColor(HexColor('#c7e8ed'));c.drawString(44,y-18,'Marca cada punto y viaja con más tranquilidad.')
 c.setFillColor(cream);c.roundRect(44,150,A4[0]-88,150,18,fill=1,stroke=0);c.setFillColor(navy);c.setFont('Helvetica-Bold',16);c.drawString(66,265,'Cómo usar esta checklist')
 c.setFont('Helvetica',11);c.setFillColor(muted);c.drawString(66,235,'1. Revísala al reservar y elimina lo que no aplica.');c.drawString(66,210,'2. Marca lo preparado una semana antes.');c.drawString(66,185,'3. Haz una revisión final 24 horas antes de salir.')
 footer(c,1);c.showPage()
 c.setFillColorRGB(1,1,1);c.rect(0,0,A4[0],A4[1],fill=1,stroke=0);c.setFillColor(navy);c.setFont('Helvetica-Bold',22);c.drawString(44,A4[1]-66,title);y=A4[1]-108
 for heading,items in sections:
  c.setFillColor(aqua);c.setFont('Helvetica-Bold',13);c.drawString(44,y,heading.upper());y-=24
  for item in items:
   c.setStrokeColor(HexColor('#b9cbd2'));c.rect(48,y-3,11,11,fill=0,stroke=1);c.setFillColor(muted);c.setFont('Helvetica',11);c.drawString(70,y,item);y-=25
  y-=12
 c.setFillColor(cream);c.roundRect(44,74,A4[0]-88,58,12,fill=1,stroke=0);c.setFillColor(navy);c.setFont('Helvetica-Bold',10);c.drawString(60,108,'REVISIÓN FINAL');c.setFont('Helvetica',9);c.drawString(60,89,'Documentos · reservas · clima · equipaje permitido · traslado')
 footer(c,2);c.save()
print(f'Generated {len(guides)} PDF guides in {OUT}')
