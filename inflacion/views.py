from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.simple import direct_to_template
from django.contrib import messages
from django.db.models import Q
from numpy import *
from misindicadores.globals.functions import *
from misindicadores.inflacion.models import *

# Portada
def portada(request):
  return direct_to_template(request, 'inflacion/portada.html', {})

# UDIS
def udis(request):
  if(request.GET and request.GET['_m'] and request.GET['_y']):
    fecha = "%s-%s-01" % (request.GET['_y'], request.GET['_m'])
  else:
    last_udis = Udis.objects.all().order_by('-fecha')[0]
    fecha = last_udis.fecha.strftime("%Y-%m-%d")
  
  udiss = Udis.objects.filter(fecha__lte=fecha).order_by('-fecha')[:30]
  
  if(len(udiss) > 0):
    valores = []
    chart_valores = []
    chart_categories = []
  
    for udis in udiss:
      valores.append(udis.valor)
    
      chart_valores.append(str(udis.valor))
      chart_categories.append('"' + doDate(udis.fecha) + '"')
  
    chart_categories.reverse()
    chart_categories = ','.join(chart_categories)
    chart_valores.reverse()
    chart_valores = ','.join(chart_valores)
  
    valores = get_stats(valores)
  
    return direct_to_template(request, 'inflacion/ver.html', {
      'fecha':fecha,
      'udiss':udiss,
      'arr_valores':udiss,
      'valores':valores,
      'valores_no_format':True,
      'chart_title':'UDIS',
      'chart_source':'Banco de M&eacute;xico',
      'chart_categories':chart_categories,
      'chart_valores':chart_valores,
      'slug':'udis'
    })
  else:
    messages.add_message(request, messages.ERROR, 'No encontramos valores para la fecha seleccionada.')
    return HttpResponseRedirect('/inflacion/udis/')

# CPI
def cpi(request):
  if(request.GET and request.GET['_m'] and request.GET['_y']):
    fecha = "%s-%s-01" % (request.GET['_y'], request.GET['_m'])
  else:
    last_cpi = Cpi.objects.all().order_by('-fecha')[0]
    fecha = last_cpi.fecha.strftime("%Y-%m-%d")
  
  cpis = Cpi.objects.filter(fecha__lte=fecha).order_by('-fecha')[:30]
  
  if(len(cpis) > 0):
    valores = []
    chart_valores = []
    chart_categories = []
  
    for cpi in cpis:
      valores.append(cpi.valor)
    
      chart_valores.append(str(cpi.valor))
      chart_categories.append('"' + doDate(cpi.fecha, 2) + '"')
  
    chart_categories.reverse()
    chart_categories = ','.join(chart_categories)
    chart_valores.reverse()
    chart_valores = ','.join(chart_valores)
  
    valores = get_stats(valores)
  
    return direct_to_template(request, 'inflacion/ver.html', {
      'fecha':fecha,
      'cpis':cpis,
      'arr_valores':cpis,
      'valores':valores,
      'valores_mes_date':True,
      'chart_title':'&Iacute;ndices de Inflaci&oacute;n de EUA',
      'chart_source':'Departamento de Labor de EUA',
      'chart_categories':chart_categories,
      'chart_valores':chart_valores,
      'slug':'cpi'
    })
  else:
    messages.add_message(request, messages.ERROR, 'No encontramos valores para la fecha seleccionada.')
    return HttpResponseRedirect('/inflacion/cpi/')

# Grafica del INPC
def img_inpc(request):
  from django.conf import settings
  from django.core.cache import cache
  import cStringIO
  import matplotlib
  matplotlib.use('Agg')
  import matplotlib.pyplot as plt
  import matplotlib.ticker as ticker
  import matplotlib as mpl
  
  mpl.rcParams['axes.titlesize'] = '8'
  
  img_name = 'img_inpc'
  
  # Checamos si hay cache
  ic = cache.get(img_name)
  
  if(ic):
    response = HttpResponse(ic, mimetype='image/png')
  else:
    output = cStringIO.StringIO()
    
    inpcs = Inpc.objects.all().order_by('-id')[:30]
    
    valores = []
    fechas = []
    
    cont = 0
    
    for inpc in inpcs:
      valores.append(inpc.valor)
      
      if(cont == 0 or cont == len(inpcs) - 1):
        fechas.append(doDate(inpc.fecha, style=2))
      else:
        fechas.append('')
      
      cont += 1

    valores.reverse()
    fechas.reverse()
    
    plot = plt.figure(figsize=[4.5,1.5], dpi=100)
    ax = plot.add_subplot(111)
    plt.title('INPC')
    ax.plot(valores)
    
    xAxis = plt.axes().xaxis
    xAxis.set_major_locator(ticker.FixedLocator([i for i in range(0,30)]))
    formatter = ticker.FuncFormatter(lambda x,pos: fechas[int(x)])
    xAxis.set_major_formatter(formatter)
    
    for tl in xAxis.get_ticklabels():
      tl.set_fontsize(8)
    
    yAxis = plt.axes().yaxis
    
    for tl in yAxis.get_ticklabels():
      tl.set_fontsize(8)
    
    plt.savefig(output)
    
    cache.set(img_name, output.getvalue(), settings.CACHE_TIME)
    
    response = HttpResponse(output.getvalue(), mimetype='image/png')
  
  return response

# INPC
def inpc(request):
  if(request.GET and request.GET['_m'] and request.GET['_y']):
    fecha = "%s-%s-01" % (request.GET['_y'], request.GET['_m'])
  else:
    last_inpc = Inpc.objects.all().order_by('-fecha')[0]
    fecha = last_inpc.fecha.strftime("%Y-%m-%d")
  
  inpcs = Inpc.objects.filter(fecha__lte=fecha).order_by('-fecha')[:30]
  
  last_inpc = inpcs[0]
  
  if(len(inpcs) > 0):
    valores = []
    chart_valores = []
    chart_categories = []
  
    for inpc in inpcs:
      valores.append(inpc.valor)
    
      chart_valores.append(str(inpc.valor))
      chart_categories.append('"' + doDate(inpc.fecha, 2) + '"')
  
    chart_categories.reverse()
    chart_categories = ','.join(chart_categories)
    chart_valores.reverse()
    chart_valores = ','.join(chart_valores)
  
    valores = get_stats(valores)
  
    return direct_to_template(request, 'inflacion/inpc.html', {
      'fecha':fecha,
      'inpcs':inpcs,
      'last_inpc':last_inpc,
      'arr_valores':inpcs,
      'valores':valores,
      'valores_mes_date':True,
      'chart_title':'INPC',
      'chart_source':'Banco de M&eacute;xico',
      'chart_categories':chart_categories,
      'chart_valores':chart_valores,
      'slug':'inpc',
      'valores_no_format':True
    })
  else:
    messages.add_message(request, messages.ERROR, 'No encontramos valores para la fecha seleccionada.')
    return HttpResponseRedirect('/inflacion/inpc/')

# Cron inflacion
def cron_inflacion(request):
  import urllib2
  from BeautifulSoup import BeautifulSoup
  import re
  from datetime import date
  
  # INPC
  
  url = 'http://www.banxico.gob.mx/SieInternet/consultarDirectorioInternetAction.do?accion=consultarCuadro&idCuadro=CP154&sector=8&locale=es'
  f = urllib2.urlopen(url).read()
  
  f = f.replace(chr(10), '').replace(chr(13), '')
  farr = f.split('<body onload="jstreeAbreRamas(\'jstree.linea\'); scrolledAreaRegistra(); " style="padding: 0px; margin: 0px;" >')
  f = strip_tags_script(farr[1])
  
  farr = f.split('<div id="jstree.linea5.1">')
  
  f = "<html><body>" + farr[0] + "</body></html>"
  
  soup = BeautifulSoup(f)
  
  fecha = ""
  inpc = 0
  
  for td in soup.findAll('td', {'class':'cd_titulos_tabla'}):
    try:
      content = clean_string(td.contents[0]).replace(',', '')
    
      carr = content.split(' ')
    
      try:
        i_carr = int(carr[1])
      except:
        i_carr = 0
    
      if(i_carr):
        fecha = content
        
        # Parseamos fecha
        farr = fecha.split(' ')
        
        m = addNumCero(getMesNum(farr[0], short=True))
        
        fecha = "%s-%s-01" % (farr[1], m)
    except:
      pass
  
  cont = 0
  
  for td in soup.findAll('td', {'class':'cd_tabla_renglon'}):
    cont += 1
    try:
      content = clean_string(td.contents[0]).replace(',', '')
    except:
      content = ""
    
    if(cont == 8):
      inpc = float(content)
      break
  
  if(fecha != "" and inpc != 0):
    # Checamos si ya existe
    try:
      alr_inpc = Inpc.objects.filter(fecha=fecha)[0]
    except:
      alr_inpc = Inpc()
    
    alr_inpc.fecha = fecha
    alr_inpc.valor = inpc
    alr_inpc.save()
  
  # CPI
  
  url = 'ftp://ftp.bls.gov/pub/special.requests/cpi/cpiai.txt'
  f = urllib2.urlopen(url).read()
  
  lines = f.split(chr(10))
  
  year = 0
  fecha = ""
  last = 0
  p = re.compile(r'( )+')
  
  count_years = 0
  count_months = 0
  line_cont = 0
  
  for line in lines:
    line = line.strip()
    
    if(line != ""):
      lines[line_cont] = p.sub('|', line)
      
      parts = lines[line_cont].split('|')
      
      try:
        year = int(parts[0])
      except:
        year = 0
      
      count_months = 0
      
      for part in parts:
        if(fecha == ""):
          fecha = part
        
        try:
          last = float(part)
        except:
          last = None
        
        count_months += 1
    else:
      del lines[line_cont]
    
    line_cont += 1
  
  if(year != 0 and last and last != ""):
    count_months -= 1
    count_months = addNumCero(count_months)
    
    fecha = "%s-%s-01" % (year, count_months)
    
    try:
      alr_cpi = Cpi.objects.filter(fecha=fecha)[0]
    except:
      alr_cpi = Cpi()
    
    alr_cpi.fecha = fecha
    alr_cpi.valor = last
    alr_cpi.save()
  
  # UDIS
  
  yf = date.today().year + 1
  yi = yf - 1
  
  url = 'http://www.banxico.org.mx/SieInternet/consultarDirectorioInternetAction.do?accion=consultarSeries&abreNivelSelect=noop&anoFinal=' + str(yf) + '&anoInicial=' + str(yi) + '&carritoSeriesAgregarActionURL=%2FSieInternet%2FconsultarDirectorioInternetAction.do%3Faccion%3DagregarSeriesAlCarrito&cuadroDescripcion=Valores%20de%20UDIS&formatoDeSalida=1&formatoHorizontal=false&locale=es&sectorDescripcion=%CDndices%20de%20Precios%20al%20Consumidor%20y%20UDIS&seleccionaSeriesSelect=noop&series=SP68257&tipoInformacion=5%2C1&version=2'
  
  f = urllib2.urlopen(url).read()
  soup = BeautifulSoup(f)
  
  fechas = []
  valores = []
  
  for td in soup.findAll('td'):
    try:
      content = clean_string(td.contents[0]).replace(',', '')
      try:
        f_content = float(content)
      except:
        f_content = None
    except:
      content = ""
    
    carr = content.split('/')
    
    if(len(carr) == 3):
      fechas.append("%s-%s-%s" % (carr[2], carr[1], carr[0]))
    elif(f_content and f_content != 0):
      valores.append(f_content)
  
  if(len(fechas) > 0 and len(valores) > 0):
    k = 0
    
    for fecha in fechas:
      try:
        alr_udis = Udis.objects.filter(fecha=fecha)[0]
      except:
        alr_udis = Udis()
      
      alr_udis.fecha = fecha
      alr_udis.valor = valores[k]
      alr_udis.save()
      
      k += 1
  
  return direct_to_template(request, 'ajax.html', {'out':'done'})
