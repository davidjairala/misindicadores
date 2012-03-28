from django.http import HttpResponseRedirect
from django.views.generic.simple import direct_to_template
from django.contrib import messages
from misindicadores.globals.functions import *
from misindicadores.medios.models import *

# Index
def index(request):
  from django.core.paginator import Paginator
  
  try:
    pnum = int(request.GET['page'])
  except:
    pnum = 1
  
  perpage = 20
  
  articulos = Articulo.objects.filter(padre__isnull=True).order_by('-fecha', '-puntos', '-id')
  
  p = Paginator(articulos, perpage)
  page = p.page(pnum)
  
  return direct_to_template(request, 'medios/index.html', {
    'articulos':page,
    'pnum':pnum
  })

# Cron Medios
def cron_medios(request):
  import feedparser
  from datetime import date, timedelta
  import re
  
  lmp = re.compile('leer m(.*)s')
  
  fecha = date.today().strftime("%Y-%m-%d")
  th = 7
  
  # Checamos ultimo
  try:
    rss_last = RssLast.objects.all().order_by('-id')[0]
  except:
    rss_last = RssLast()
    
    # Sacamos primer rss
    first_rss = Rss.objects.all().order_by('id')[0]
    rss_last.rss = first_rss
  
  # Agarramos rss
  channels = feedparser.parse(rss_last.rss.url)
  
  url = ''
  summary = ''
  title = ''
  
  for entry in channels.entries:
    try:
      url = unicode(entry.link, channels.encoding)
      summary = unicode(entry.description, channels.encoding)
      title = unicode(entry.title, channels.encoding)
    except:
      url = entry.link
      summary = entry.description
      title = entry.title
    
    title = lmp.sub('', clean_string(title))
    summary = clean_string(summary)
    
    if(title != "" and summary != "" and url != ""):
      # Checamos si existe
      try:
        articulo = Articulo.objects.filter(url=url)[0]
      except:
        # No existe, creamos
        articulo = Articulo()
      
        articulo.rss = rss_last.rss
        articulo.titulo = title
        articulo.url = url
        articulo.descripcion = summary
        articulo.vistas = 0
        articulo.puntos = 0
      
        articulo.save()
      
        # Intentamos sacar padre
        try:
          slug = searchify(title)
        
          padre = Articulo.objects.raw('SELECT * FROM medios_articulo WHERE MATCH (titulo, descripcion) AGAINST ("%s") > %s AND id != %s AND fecha = "%s" ORDER BY MATCH (titulo, descripcion) AGAINST ("%s") DESC LIMIT 1' % (slug, th, articulo.id, fecha, slug))[0]
        
          articulo.padre = padre
        
          articulo.save()
        
          # Aumentamos puntos del padre
          padre.puntos += 1
        
          padre.save()
        except:
          pass
  
  # Siguiente RSS
  try:
    rss = Rss.objects.filter(id__gt=rss_last.rss.id)[0]
  except:
    rss = Rss.objects.all().order_by('id')[0]
  
  rss_last.rss = rss
  
  rss_last.save()
  
  return direct_to_template(request, 'ajax.html', {'out':'done'})
