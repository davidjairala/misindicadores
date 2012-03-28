from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.simple import direct_to_template
from django.contrib import messages
from numpy import *
from misindicadores.globals.functions import *
from misindicadores.tasas.models import *

# Portada
def portada(request):
  return direct_to_template(request, 'tasas/portada.html', {})

# Grafica del IMI
def img_imi(request):
  from django.conf import settings
  from django.core.cache import cache
  import cStringIO
  import matplotlib
  matplotlib.use('Agg')
  import matplotlib.pyplot as plt
  import matplotlib.ticker as ticker
  import matplotlib as mpl

  mpl.rcParams['axes.titlesize'] = '8'

  img_name = 'img_3'

  # Checamos si hay cache
  ic = cache.get(img_name)

  if(ic):
    response = HttpResponse(ic, mimetype='image/png')
  else:
    output = cStringIO.StringIO()

    imis = Imi.objects.all().order_by('-id')[:30]

    valores = []
    fechas = []

    cont = 0

    for imi in imis:
      valores.append(imi.valor)

      if(cont == 0 or cont == len(imis) - 1):
        fechas.append(doDate(imi.fecha))
      else:
        fechas.append('')

      cont += 1

    valores.reverse()
    fechas.reverse()

    plot = plt.figure(figsize=[4.5,1.5], dpi=100)
    ax = plot.add_subplot(111)
    plt.title('IMI')
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

# IMI
def imi(request):
  if(request.GET and request.GET['_d'] and request.GET['_m'] and request.GET['_y']):
    fecha = "%s-%s-%s" % (request.GET['_y'], request.GET['_m'], request.GET['_d'])
  else:
    last_imi = Imi.objects.all().order_by('-fecha')[0]
    fecha = last_imi.fecha.strftime("%Y-%m-%d")

  imis = Imi.objects.filter(fecha__lte=fecha).order_by('-fecha')[:30]

  if(len(imis) > 0):
    valores = []
    chart_valores = []
    chart_categories = []

    for imi in imis:
      valores.append(imi.valor)
      chart_valores.append(str(imi.valor))
      chart_categories.append('"' + doDate(imi.fecha) + '"')

    chart_categories.reverse()
    chart_categories = ','.join(chart_categories)
    chart_valores.reverse()
    chart_valores = ','.join(chart_valores)

    valores = get_stats(valores)

    return direct_to_template(request, 'tasas/imi.html', {
      'fecha':fecha,
      'arr_valores':imis,
      'valores':valores,
      'chart_title':'&Iacute;ndice Mis Indicadores',
      'chart_source':'Mis Indicadores',
      'chart_categories':chart_categories,
      'chart_valores':chart_valores,
      'slug':'imi'
    })
  else:
    messages.add_message(request, messages.ERROR, 'No encontramos valores para la fecha seleccionada.')
    return HttpResponseRedirect("/tasas/imi/")

# TIIE
def tiie(request):
  from operator import itemgetter
  from datetime import date, timedelta

  try:
    plazo = int(request.GET['plazo'])
  except:
    plazo = 28
  plazo_title = "%s d&iacute;as" % plazo

  try:
    fecha = date(int(request.GET['_y']), int(request.GET['_m']), int(request.GET['_d']))
  except:
    last_tiies = Tiie.objects.all().order_by('-fecha')[0]
    fecha = last_tiies.fecha

  fecha_ini = fecha - timedelta(days=31)

  tiies = Tiie.objects.filter(fecha__lte=fecha, fecha__gte=fecha_ini).order_by('-fecha')

  if(len(tiies) > 0):
    valores = []
    chart_valores = []
    chart_categories = []
    arr_valores = []
    plazos = []

    promedios = {}

    plazos.append(plazo)

    for tiie in tiies:
      if(tiie.plazo == plazo):
        key = int(tiie.fecha.strftime("%Y%m%d"))
        try:
          promedios[key].append(tiie.postura)
        except:
          promedios[key] = []
          promedios[key].append(tiie.postura)

        arr_valores.append({'fecha':tiie.fecha, 'participante':tiie.participante, 'postura':tiie.postura})
      else:
        try:
          i = plazos.index(tiie.plazo)
        except:
          plazos.append(tiie.plazo)

    list_promedios = []

    for k in promedios.keys():
      list_promedios.append({'fecha':k, 'promedio':promedios[k]})

    list_promedios.sort(key=itemgetter('fecha'))

    for promedio in list_promedios:
      k = promedio['fecha']
      v = promedio['promedio']
      promedio = get_promedio(v)
      valores.append(promedio)
      chart_valores.append(str("%.4f" % promedio))
      # Parseamos fecha
      c_fecha = "%s-%s-%s" % (str(k)[:4], str(k)[4:6], str(k)[6:8])
      chart_categories.append('"' + doDate(c_fecha) + '"')

    chart_categories = ','.join(chart_categories)
    chart_valores = ','.join(chart_valores)

    valores.reverse()

    valores = get_stats(valores)

    plazos.sort()

    return direct_to_template(request, 'tasas/tiie.html', {
      'fecha':fecha,
      'tiies':tiies,
      'valores':valores,
      'arr_valores':arr_valores,
      'valores_no_format':True,
      'chart_title':'Tasa de Inter&eacute;s Interbancario de Equilibrio - %s' % plazo_title,
      'chart_source':'Banco de M&eacute;xico',
      'chart_categories':chart_categories,
      'chart_valores':chart_valores,
      'slug':'tiie',
      'plazo':plazo,
      'plazo_title':plazo_title,
      'plazos':plazos
    })
  else:
    messages.add_message(request, messages.ERROR, 'No encontramos valores para la fecha seleccionada.')
    return HttpResponseRedirect('/tasas/tiie/')

# CETES
def cetes(request):
  try:
    plazo = int(request.GET['plazo'])
  except:
    plazo = 28
  plazo_title = "%s d&iacute;as" % plazo

  try:
    fecha = "%s-%s-%s" % (request.GET['_y'], request.GET['_m'], request.GET['_d'])
  except:
    last_cetes = Cetes.objects.all().order_by('-fecha')[0]
    fecha = last_cetes.fecha.strftime("%Y-%m-%d")

  cetes = Cetes.objects.filter(fecha__lte=fecha).order_by('-fecha')[:30]

  if(len(cetes) > 0):
    valores = []
    chart_valores = []
    chart_categories = []
    arr_valores = []
    plazos = []

    plazos.append(plazo)

    for cete in cetes:
      if(cete.plazo == plazo):
        valores.append(cete.actual)
        arr_valores.append({'fecha':cete.fecha, 'valor':cete.actual})

        chart_valores.append(str(cete.actual))
        chart_categories.append('"' + doDate(cete.fecha) + '"')
      else:
        try:
          i = plazos.index(cete.plazo)
        except:
          plazos.append(cete.plazo)

    chart_categories.reverse()
    chart_categories = ','.join(chart_categories)
    chart_valores.reverse()
    chart_valores = ','.join(chart_valores)

    valores = get_stats(valores)

    plazos.sort()

    return direct_to_template(request, 'tasas/cetes.html', {
      'fecha':fecha,
      'cetes':cetes,
      'valores':valores,
      'arr_valores':arr_valores,
      'valores_no_format':True,
      'chart_title':'CETES - %s' % plazo_title,
      'chart_source':'Banco de M&eacute;xico',
      'chart_categories':chart_categories,
      'chart_valores':chart_valores,
      'slug':'cetes',
      'plazo':plazo,
      'plazo_title':plazo_title,
      'plazos':plazos
    })
  else:
    messages.add_message(request, messages.ERROR, 'No encontramos valores para la fecha seleccionada.')
    return HttpResponseRedirect('/tasas/cetes/')

# CPP
def cpp(request):
  if(request.GET and request.GET['_m'] and request.GET['_y']):
    fecha = "%s-%s-01" % (request.GET['_y'], request.GET['_m'])
  else:
    last_cpp = Cpp.objects.all().order_by('-fecha')[0]
    fecha = last_cpp.fecha.strftime("%Y-%m-%d")

  cpps = Cpp.objects.filter(fecha__lte=fecha).order_by('-fecha')[:30]

  if(len(cpps) > 0):
    pesos = []
    udis = []
    dolares = []
    promedios = []
    ti_pesos = []
    chart_pesos = []
    chart_udis = []
    chart_dolares = []
    chart_promedios = []
    chart_ti_pesos = []
    chart_categories = []

    for cpp in cpps:
      pesos.append(cpp.pesos)
      udis.append(cpp.udis)
      dolares.append(cpp.dolares)
      promedios.append(cpp.promedio)
      ti_pesos.append(cpp.ti_pesos)

      chart_pesos.append(str(cpp.pesos))
      chart_udis.append(str(cpp.udis))
      chart_dolares.append(str(cpp.dolares))
      chart_promedios.append(str(cpp.promedio))
      chart_ti_pesos.append(str(cpp.ti_pesos))
      chart_categories.append('"' + doDate(cpp.fecha, 2) + '"')

    chart_categories.reverse()
    chart_categories = ','.join(chart_categories)
    chart_pesos.reverse()
    chart_pesos = ','.join(chart_pesos)
    chart_udis.reverse()
    chart_udis = ','.join(chart_udis)
    chart_dolares.reverse()
    chart_dolares = ','.join(chart_dolares)
    chart_promedios.reverse()
    chart_promedios = ','.join(chart_promedios)
    chart_ti_pesos.reverse()
    chart_ti_pesos = ','.join(chart_ti_pesos)

    pesos = get_stats(pesos)
    udis = get_stats(udis)
    dolares = get_stats(dolares)
    promedios = get_stats(promedios)
    ti_pesos = get_stats(ti_pesos)

    return direct_to_template(request, 'tasas/cpp.html', {
      'fecha':fecha,
      'cpps':cpps,
      'pesos':pesos,
      'udis':udis,
      'dolares':dolares,
      'promedios':promedios,
      'ti_pesos':ti_pesos,
      'valores_no_format':True,
      'chart_title':'Costos de Captaci&oacute;n',
      'chart_source':'Banco de M&eacute;xico',
      'chart_categories':chart_categories,
      'chart_pesos':chart_pesos,
      'chart_udis':chart_udis,
      'chart_dolares':chart_dolares,
      'chart_promedios':chart_promedios,
      'chart_ti_pesos':chart_ti_pesos,
      'slug':'cpp'
    })
  else:
    messages.add_message(request, messages.ERROR, 'No encontramos valores para la fecha seleccionada.')
    return HttpResponseRedirect('/tasas/cpp/')

# Cron Tasas
def cron_tasas(request):
  from misindicadores.divisas.models import Dolar, Deg, Euro, Libra, Yen
  from misindicadores.bolsas.models import BmvIpcDia
  from misindicadores.desempeno.models import Reserva, Pib
  from misindicadores.inflacion.models import Udis
  import urllib2
  from BeautifulSoup import BeautifulSoup
  import re
  from datetime import date

  # CPP

  url = 'http://www.banxico.org.mx/SieInternet/consultarDirectorioInternetAction.do?accion=consultarCuadro&idCuadro=CF112&sector=18&locale=es'
  f = urllib2.urlopen(url).read()

  farr = f.split('<body onload="jstreeAbreRamas(\'jstree.linea\'); scrolledAreaRegistra(); " style="padding: 0px; margin: 0px;" >')
  f = strip_tags_script(farr[1]).replace(chr(10), '').replace(chr(13), '')

  farr = f.split('<p style="padding: 0px; margin: 8px 0px 0px 0px;">')

  f = farr[2]

  farr = f.split('<div id="jstree.linea9.1">')

  f = farr[0]

  f = "<html><body>" + f + "</body></html>"

  soup = BeautifulSoup(f)

  fechas = []
  valores = []

  for td in soup.findAll('td', {'class':'cd_titulos_tabla'}):
    try:
      content = clean_string(td.contents[0])
    except:
      content = ""

    carr = content.split(' ')

    if(len(carr) == 2):
      try:
        y = int(carr[1])
      except:
        y = 0

      if(y != 0):
        month = carr[0]

        m = addNumCero(getMesNum(month, True))

        fechas.append("%s-%s-01" % (y, m))

  for td in soup.findAll('td', {'class':'cd_tabla_renglon'}):
    try:
      content = clean_string(td.contents[0])
    except:
      content = ""

    try:
      if(content == "N/E"):
        content = 0
      content = float(content)

      valores.append(content)
    except:
      content = 0

  if(len(fechas) > 0 and len(valores) > 0):
    vals = {}

    vals[fechas[0]] = {}
    vals[fechas[1]] = {}
    vals[fechas[2]] = {}

    vals[fechas[0]]["pesos"] = valores[0]
    vals[fechas[1]]["pesos"] = valores[1]
    vals[fechas[2]]["pesos"] = valores[2]

    vals[fechas[0]]["udis"] = valores[3]
    vals[fechas[1]]["udis"] = valores[4]
    vals[fechas[2]]["udis"] = valores[5]

    vals[fechas[0]]["dolares"] = valores[6]
    vals[fechas[1]]["dolares"] = valores[7]
    vals[fechas[2]]["dolares"] = valores[8]

    vals[fechas[0]]["promedio"] = valores[9]
    vals[fechas[1]]["promedio"] = valores[10]
    vals[fechas[2]]["promedio"] = valores[11]

    vals[fechas[0]]["ti_pesos"] = valores[12]
    vals[fechas[1]]["ti_pesos"] = valores[13]
    vals[fechas[2]]["ti_pesos"] = valores[14]

    for k, v in vals.items():
      # Checamos si existe
      try:
        cpp = Cpp.objects.filter(fecha=k)[0]
      except:
        cpp = Cpp()

      cpp.fecha = k
      cpp.pesos = v['pesos']
      cpp.udis = v['udis']
      cpp.dolares = v['dolares']
      cpp.promedio = v['promedio']
      cpp.ti_pesos = v['ti_pesos']
      cpp.save()

  # CETES

  url = 'http://www.banxico.org.mx/eInfoFinanciera/InfOportunaMercadosFin/MercadoValores/SubastasValoreGub/ResuSubaPrimaNew-1.html'
  f = urllib2.urlopen(url).read()
  soup = BeautifulSoup(f)

  p = re.compile('( )+')

  for td in soup.findAll('td'):
    try:
      content = clean_string(td.contents[2].replace('$', ''))
    except:
      try:
        content = clean_string(td.contents[0].replace('$', ''))
      except:
        content = ""

    content = p.sub(' ', content)
    carr = content.split(' ')

    try:
      year = int(carr[4])
    except:
      year = 0

    if(year != 0):
      d = addNumCero(int(carr[0]))
      month = addNumCero(getMesNum(carr[2]))

      fecha = "%s-%s-%s" % (year, month, d)
      break

  cont = 0
  tr_cont = 0
  start_linea = False
  vals = {}

  for tr in soup.findAll('tr'):
    for td in tr.findAll('td'):
      try:
        content = clean_string(td.contents[0].replace('$', '').replace('+', ''))
      except:
        content = ''

      if(content == "CETES" and not start_linea):
        start_linea = True
        cont = 0
        tr_cont += 1
        vals[tr_cont] = {}
      elif(start_linea and tr_cont < 5):
        if(cont == 1):
          vals[tr_cont]["plazo"] = int(content)
        elif(cont == 5):
          vals[tr_cont]["solicitado"] = float(content)
        elif(cont == 19):
          vals[tr_cont]["colocado"] = float(content)
        elif(cont == 25):
          vals[tr_cont]["actual"] = float(content)
        elif(cont == 29):
          vals[tr_cont]["variacion"] = float(content)
          start_linea = False
          break

        cont += 1

      cont += 1

  if(len(vals) > 0):
    for k, v in vals.items():
      # Checamos si existe
      try:
        cetes = Cetes.objects.filter(fecha=fecha, plazo=v['plazo'])[0]
      except:
        cetes = Cetes()

      try:
        cetes.fecha = fecha
        cetes.plazo = v["plazo"]
        cetes.solicitado = v["solicitado"]
        cetes.colocado = v["colocado"]
        cetes.actual = v["actual"]
        cetes.variacion = v["variacion"]
        cetes.save()
      except:
        pass

  # TIIE, 28 dias

  url = 'http://www.banxico.org.mx/eInfoFinanciera/InfOportunaMercadosFin/MercadoValores/TasaInteresInterbancaria/04Semanas/TasaInteres4Sem.html'
  f = urllib2.urlopen(url).read()
  soup = BeautifulSoup(f)

  fecha = ""

  for p in soup.findAll('p'):
    try:
      content = clean_string(p.contents[0])
    except:
      content = ""

    carr = content.split('del d&iacute;a ')

    try:
      fecha = carr[1]
    except:
      pass

  if(fecha != ""):
    # Parseamos fecha
    farr = fecha.split(' ')
    day = addNumCero(int(farr[0]))
    month = addNumCero(getMesNum(farr[2].capitalize()))
    year = int(farr[4])

    fecha = "%s-%s-%s" % (year, month, day)

  p = re.compile('renglonPar|renglonNon')

  for tr in soup.findAll('tr', {'class':p}):
    cont = 0
    postura = 0
    monto = 0
    participante = ""

    for td in tr.findAll('td'):
      content = clean_string(td.contents[0])

      if(cont == 0):
        postura = float(content)
      elif(cont == 1):
        monto = float(content)
      elif(cont == 2):
        participante = content

      cont += 1

    # Checamos que todo venga bien
    if(postura != 0 and monto != 0 and participante != ""):
      # Checamos si existe
      try:
        tiie = Tiie.objects.filter(plazo=28, fecha=fecha, participante=participante)[0]
      except:
        tiie = Tiie()

      tiie.plazo = 28
      tiie.fecha = fecha
      tiie.postura = postura
      tiie.monto = monto
      tiie.participante = participante

      tiie.save()

  # TIIE, 91 dias

  url = 'http://www.banxico.org.mx/eInfoFinanciera/InfOportunaMercadosFin/MercadoValores/TasaInteresInterbancaria/04Semanas/TasaInteres4Sem.html'
  f = urllib2.urlopen(url).read()
  soup = BeautifulSoup(f)

  fecha = ""

  for p in soup.findAll('p'):
    try:
      content = clean_string(p.contents[0])
    except:
      content = ""

    carr = content.split('del d&iacute;a ')

    try:
      fecha = carr[1]
    except:
      pass

  if(fecha != ""):
    # Parseamos fecha
    farr = fecha.split(' ')
    day = addNumCero(int(farr[0]))
    month = addNumCero(getMesNum(farr[2].capitalize()))
    year = int(farr[4])

    fecha = "%s-%s-%s" % (year, month, day)

  p = re.compile('renglonPar|renglonNon')

  for tr in soup.findAll('tr', {'class':p}):
    cont = 0
    postura = 0
    monto = 0
    participante = ""

    for td in tr.findAll('td'):
      content = clean_string(td.contents[0])

      if(cont == 0):
        postura = float(content)
      elif(cont == 1):
        monto = float(content)
      elif(cont == 2):
        participante = content

      cont += 1

    # Checamos que todo venga bien
    if(postura != 0 and monto != 0 and participante != ""):
      # Checamos si existe
      try:
        tiie = Tiie.objects.filter(plazo=91, fecha=fecha, participante=participante)[0]
      except:
        tiie = Tiie()

      tiie.plazo = 91
      tiie.fecha = fecha
      tiie.postura = postura
      tiie.monto = monto
      tiie.participante = participante

      tiie.save()

  # IMI

  constante = 10

  dolar = Dolar.objects.all().order_by('-fecha')[0]

  fecha = dolar.fecha
  year = fecha.year

  bmv = BmvIpcDia.objects.filter(fecha__lte=fecha).order_by('-fecha')[0]
  deg = Deg.objects.filter(fecha__lte=fecha).order_by('-fecha')[0]
  euro = Euro.objects.filter(fecha__lte=fecha).order_by('-fecha')[0]
  libra = Libra.objects.filter(fecha__lte=fecha).order_by('-fecha')[0]
  yen = Yen.objects.filter(fecha__lte=fecha).order_by('-fecha')[0]
  reserva = Reserva.objects.filter(fecha__lte=fecha).order_by('-fecha')[0]
  udis = Udis.objects.filter(fecha__lte=fecha).order_by('-fecha')[0]
  pib = Pib.objects.filter(year__lte=year).order_by('-year', '-trimestre')[0]

  promedio_dolar = (dolar.valor + dolar.promedio_compra + dolar.promedio_venta) / 3
  promedio_euro = (euro.valor + euro.promedio_compra + euro.promedio_venta) / 3
  promedio_divisas = (promedio_dolar + promedio_euro + deg.valor + libra.valor + yen.valor) / 5

  valor = ( ( bmv.valor + ( reserva.reserva_internacional_dolares / constante ) + ( pib.total / (constante * 100) ) ) / ( promedio_divisas + udis.valor ) ) * constante

  # Checamos si existe
  try:
    imi = Imi.objects.filter(fecha=fecha)[0]
  except:
    imi = Imi()

  imi.fecha = fecha
  imi.valor = valor

  imi.save()

  return direct_to_template(request, 'ajax.html', {'out':'done'})
