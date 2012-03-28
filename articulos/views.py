from django.http import HttpResponseRedirect
from django.views.generic.simple import direct_to_template
from django.contrib import messages
from misindicadores.globals.functions import *
from misindicadores.articulos.models import *

# Updetea feed diario de twitter
def update_twitter_indicadores(request):
  from django.conf import settings
  import tweepy
  from misindicadores.divisas.models import Dolar, Euro
  from misindicadores.bolsas.models import BmvIpcDia
  
  dolar = Dolar.objects.all().order_by('-fecha')[0]
  euro = Euro.objects.all().order_by('-fecha')[0]
  bmv = BmvIpcDia.objects.all().order_by('-fecha')[0]
  
  status = 'Dolar: F:%(dolar_fix)s, C:%(dolar_compra)s, V:%(dolar_venta)s | Euro: F:%(euro_fix)s, C:%(euro_compra)s, V:%(euro_venta)s | BMV:%(bmv_ipc)s | http://misindicadores.com/rd/?_d=%(dia)s&_m=%(mes)s&_y=%(ano)s' % {
    'dolar_fix':dinero(dolar.valor),
    'dolar_compra':dinero(dolar.promedio_compra),
    'dolar_venta':dinero(dolar.promedio_venta),
    'euro_fix':dinero(euro.valor),
    'euro_compra':dinero(euro.promedio_compra),
    'euro_venta':dinero(euro.promedio_venta),
    'bmv_ipc':dinero(bmv.valor),
    'dia':dolar.fecha.day,
    'mes':dolar.fecha.month,
    'ano':dolar.fecha.year
  }
  
  auth = tweepy.OAuthHandler(settings.TWITTER_CONSUMER_TOKEN, settings.TWITTER_CONSUMER_SECRET)
  auth.set_access_token(settings.TWITTER_ACCESS_TOKEN_KEY, settings.TWITTER_ACCESS_TOKEN_SECRET)
  api = tweepy.API(auth)
  api.update_status(status)
  
  return direct_to_template(request, 'ajax.html', {'out':status})

# Agrega un articulo como ya twitteado
def add_already_twitted(already_twitted, articulo):
  if(already_twitted is None):
    already_twitted = AlreadyTwitted(articulo=articulo)
  else:
    already_twitted.articulo = articulo
  already_twitted.save()

# Actualiza twitter
def update_twitter(request):
  from django.conf import settings
  import tweepy
  
  already_twitted = None
  
  articulo = Articulo.objects.all().order_by('-id')[0]
  
  # Checamos si ya hemos twiteado este articulo
  try:
    already_twitted = AlreadyTwitted.objects.get(articulo=articulo)
  except:
    status = "%s: http://misindicadores.com%s" % (articulo.titulo, articulo.get_absolute_url())
  
    try:
      auth = tweepy.OAuthHandler(settings.TWITTER_CONSUMER_TOKEN, settings.TWITTER_CONSUMER_SECRET)
      auth.set_access_token(settings.TWITTER_ACCESS_TOKEN_KEY, settings.TWITTER_ACCESS_TOKEN_SECRET)
      api = tweepy.API(auth)
      api.update_status(status)
      
      add_already_twitted(already_twitted, articulo)
  
      return direct_to_template(request, 'ajax.html', {'out':'Updated: %s' % (status)})
    except:
      pass
  
  add_already_twitted(already_twitted, articulo)
  
  return direct_to_template(request, 'ajax.html', {'out':'Status repetido'})

# Ver articulo
def ver_articulo(request, nombre_limpio, id):
  articulo = Articulo.objects.get(pk=id)
  
  return direct_to_template(request, 'articulos/ver_articulo.html', {
    'articulo':articulo
  })

# Ver categoria
def ver_categoria(request, nombre_limpio):
  from django.core.paginator import Paginator
  
  try:
    pnum = int(request.GET['page'])
  except:
    pnum = 1
  
  perpage = 20
  
  categoria = Categoria.objects.filter(nombre_limpio=nombre_limpio)[0]
  
  articulos = Articulo.objects.filter(categoria=categoria).order_by('-id')
  
  p = Paginator(articulos, perpage)
  page = p.page(pnum)
  
  return direct_to_template(request, 'articulos/ver_categoria.html', {
    'categoria':categoria,
    'articulos':page,
    'pnum':pnum
  })

# Portada
def index(request):
  from django.core.paginator import Paginator
  
  try:
    pnum = int(request.GET['page'])
  except:
    pnum = 1
  
  perpage = 20
  
  articulos = Articulo.objects.all().order_by('-id')
  
  p = Paginator(articulos, perpage)
  page = p.page(pnum)
  
  return direct_to_template(request, 'articulos/index.html', {
    'articulos':page,
    'pnum':pnum
  })