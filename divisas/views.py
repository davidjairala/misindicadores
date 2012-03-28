from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.simple import direct_to_template
from django.contrib import messages
from numpy import *
from misindicadores.globals.functions import *
from misindicadores.divisas.models import *

# Portada
def portada(request):
  return direct_to_template(request, 'divisas/portada.html', {})

# Tabla comparativa
def tabla_comparativa(request):
  if(request.GET and request.GET['_d'] and request.GET['_m'] and request.GET['_y']):
    fecha = "%s-%s-%s" % (request.GET['_y'], request.GET['_m'], request.GET['_d'])
  else:
    last_dolar = Dolar.objects.all().order_by('-fecha')[0]
    fecha = last_dolar.fecha.strftime("%Y-%m-%d")
  
  dolars = Dolar.objects.filter(fecha__lte=fecha).order_by('-fecha')[:30]
  
  if(len(dolars) > 0):
    euros = Euro.objects.filter(fecha__lte=fecha).order_by('-fecha')[:30]
    libras = Libra.objects.filter(fecha__lte=fecha).order_by('-fecha')[:30]
    degs = Deg.objects.filter(fecha__lte=fecha).order_by('-fecha')[:30]
    yens = Yen.objects.filter(fecha__lte=fecha).order_by('-fecha')[:30]
  
    valores = []
  
    valores_dolars = []
    valores_euros = []
    valores_libras = []
    valores_degs = []
    valores_yens = []
  
    chart_dolars = []
    chart_euros = []
    chart_libras = []
    chart_degs = []
    chart_yens = []
  
    chart_categories = []
  
    cont = 0
  
    for dolar in dolars:
      valores.append({'fecha':dolar.fecha, 'dolar':dolar.valor, 'euro':euros[cont].valor, 'libra':libras[cont].valor, 'deg':degs[cont].valor, 'yen':yens[cont].valor})
      valores_dolars.append(dolar.valor)
      valores_euros.append(euros[cont].valor)
      valores_libras.append(libras[cont].valor)
      valores_degs.append(degs[cont].valor)
      valores_yens.append(yens[cont].valor)
    
      chart_dolars.append(str(dolar.valor))
      chart_euros.append(str(euros[cont].valor))
      chart_libras.append(str(libras[cont].valor))
      chart_degs.append(str(degs[cont].valor))
      chart_yens.append(str(yens[cont].valor))
    
      chart_categories.append('"' + doDate(dolar.fecha.strftime("%Y-%m-%d")) + '"')
    
      cont += 1
  
    chart_categories.reverse()
    chart_categories = ','.join(chart_categories)
    chart_dolars.reverse()
    chart_dolars = ','.join(chart_dolars)
    chart_euros.reverse()
    chart_euros = ','.join(chart_euros)
    chart_libras.reverse()
    chart_libras = ','.join(chart_libras)
    chart_degs.reverse()
    chart_degs = ','.join(chart_degs)
    chart_yens.reverse()
    chart_yens = ','.join(chart_yens)
  
    valores_dolars = get_stats(valores_dolars)
    valores_euros = get_stats(valores_euros)
    valores_libras = get_stats(valores_libras)
    valores_degs = get_stats(valores_degs)
    valores_yens = get_stats(valores_yens)
  
    return direct_to_template(request, 'divisas/tabla_comparativa.html', {
      'fecha':fecha,
      'valores':valores,
      'dolars':dolars,
      'euros':euros,
      'degs':degs,
      'libras':libras,
      'yens':yens,
      'valores_dolars':valores_dolars,
      'valores_euros':valores_euros,
      'valores_libras':valores_libras,
      'valores_degs':valores_degs,
      'valores_yens':valores_yens,
      'chart_categories':chart_categories,
      'chart_dolars':chart_dolars,
      'chart_euros':chart_euros,
      'chart_libras':chart_libras,
      'chart_degs':chart_degs,
      'chart_yens':chart_yens,
      'chart_title':'Tabla Comparativa de Divisas',
      'chart_source':'Banco de M&eacute;xico',
      'chart_categories':chart_categories
    })
  else:
    messages.add_message(request, messages.ERROR, 'No encontramos valores para la fecha seleccionada.')
    return HttpResponseRedirect('/divisas/tabla_comparativa/')

# Plata
def plata(request):
  if(request.GET and request.GET['_d'] and request.GET['_m'] and request.GET['_y']):
    fecha = "%s-%s-%s" % (request.GET['_y'], request.GET['_m'], request.GET['_d'])
  else:
    last_plata = Plata.objects.all().order_by('-fecha')[0]
    fecha = last_plata.fecha.strftime("%Y-%m-%d")
  
  platas = Plata.objects.filter(fecha__lte=fecha).order_by('-fecha')[:30]
  
  if(len(platas) > 0):
    onza_troy_compras = []
    onza_troy_ventas = []
    plata_libertad_compras = []
    plata_libertad_ventas = []
  
    chart_onza_troy_compras = []
    chart_onza_troy_ventas = []
    chart_plata_libertad_compras = []
    chart_plata_libertad_ventas = []
  
    chart_categories = []
  
    for plata in platas:
      onza_troy_compras.append(plata.onza_troy_compra)
      onza_troy_ventas.append(plata.onza_troy_venta)
      plata_libertad_compras.append(plata.plata_libertad_compra)
      plata_libertad_ventas.append(plata.plata_libertad_venta)
    
      chart_onza_troy_compras.append(str(plata.onza_troy_compra))
      chart_onza_troy_ventas.append(str(plata.onza_troy_venta))
      chart_plata_libertad_compras.append(str(plata.plata_libertad_compra))
      chart_plata_libertad_ventas.append(str(plata.plata_libertad_venta))
    
      chart_categories.append('"' + doDate(plata.fecha.strftime("%Y-%m-%d")) + '"')
  
    chart_categories.reverse()
    chart_categories = ','.join(chart_categories)
    chart_onza_troy_compras.reverse()
    chart_onza_troy_compras = ','.join(chart_onza_troy_compras)
    chart_onza_troy_ventas.reverse()
    chart_onza_troy_ventas = ','.join(chart_onza_troy_ventas)
    chart_plata_libertad_compras.reverse()
    chart_plata_libertad_compras = ','.join(chart_plata_libertad_compras)
    chart_plata_libertad_ventas.reverse()
    chart_plata_libertad_ventas = ','.join(chart_plata_libertad_ventas)
  
    onza_troy_compras = get_stats(onza_troy_compras)
    onza_troy_ventas = get_stats(onza_troy_ventas)
    plata_libertad_compras = get_stats(plata_libertad_compras)
    plata_libertad_ventas = get_stats(plata_libertad_ventas)
  
    return direct_to_template(request, 'divisas/plata.html', {
      'fecha':fecha,
      'platas':platas,
      'onza_troy_compras':onza_troy_compras,
      'onza_troy_ventas':onza_troy_ventas,
      'plata_libertad_compras':plata_libertad_compras,
      'plata_libertad_ventas':plata_libertad_ventas,
      'chart_categories':chart_categories,
      'chart_onza_troy_compras':chart_onza_troy_compras,
      'chart_onza_troy_ventas':chart_onza_troy_ventas,
      'chart_plata_libertad_compras':chart_plata_libertad_compras,
      'chart_plata_libertad_ventas':chart_plata_libertad_ventas,
      'chart_title':'Plata',
      'chart_source':'Banamex',
      'chart_categories':chart_categories
    })
  else:
    messages.add_message(request, messages.ERROR, 'No encontramos valores para la fecha seleccionada.')
    return HttpResponseRedirect('/divisas/plata/')

# Petroleo
def petroleo(request):
  if(request.GET and request.GET['_d'] and request.GET['_m'] and request.GET['_y']):
    fecha = "%s-%s-%s" % (request.GET['_y'], request.GET['_m'], request.GET['_d'])
  else:
    last_petroleo = Petroleo.objects.all().order_by('-fecha')[0]
    fecha = last_petroleo.fecha.strftime("%Y-%m-%d")
  
  petroleos = Petroleo.objects.filter(fecha__lte=fecha).order_by('-fecha')[:30]
  
  if(len(petroleos) > 0):
    brents = []
    mezcla_mexicanas = []
    wtis = []
  
    chart_brents = []
    chart_mezcla_mexicanas = []
    chart_wtis = []
  
    chart_categories = []
  
    for petroleo in petroleos:
      brents.append(petroleo.brent)
      mezcla_mexicanas.append(petroleo.mezcla_mexicana)
      wtis.append(petroleo.wti)
    
      chart_brents.append(str(petroleo.brent))
      chart_mezcla_mexicanas.append(str(petroleo.mezcla_mexicana))
      chart_wtis.append(str(petroleo.wti))
    
      chart_categories.append('"' + doDate(petroleo.fecha.strftime("%Y-%m-%d")) + '"')
  
    chart_categories.reverse()
    chart_categories = ','.join(chart_categories)
    chart_brents.reverse()
    chart_brents = ','.join(chart_brents)
    chart_mezcla_mexicanas.reverse()
    chart_mezcla_mexicanas = ','.join(chart_mezcla_mexicanas)
    chart_wtis.reverse()
    chart_wtis = ','.join(chart_wtis)
  
    brents = get_stats(brents)
    mezcla_mexicanas = get_stats(mezcla_mexicanas)
    wtis = get_stats(wtis)
  
    return direct_to_template(request, 'divisas/petroleo.html', {
      'fecha':fecha,
      'petroleos':petroleos,
      'brents':brents,
      'mezcla_mexicanas':mezcla_mexicanas,
      'wtis':wtis,
      'chart_categories':chart_categories,
      'chart_brents':chart_brents,
      'chart_mezcla_mexicanas':chart_mezcla_mexicanas,
      'chart_wtis':chart_wtis,
      'chart_title':'Petr&oacute;leo',
      'chart_source':'CNN Expansi&oacute;n',
      'chart_categories':chart_categories
    })
  else:
    messages.add_message(request, messages.ERROR, 'No encontramos valores para la fecha seleccionada.')
    return HttpResponseRedirect('/divisas/petroleo/')

# Cron petroleo
def cron_petroleo(request):
  from datetime import date
  import urllib2
  from BeautifulSoup import BeautifulSoup
  import re
  
  fecha = date.today().strftime("%Y-%m-%d")
  
  url = 'http://finanzasenlinea.infosel.com/cnnexpansion/Bolsa.aspx?b=ipc'
  f = urllib2.urlopen(url).read()
  soup = BeautifulSoup(f)
  
  cont = 0
  
  brent = 0
  mezcla_mexicana = 0
  wti = 0
  
  for span in soup.findAll('span', id='tablasIpcIndicadoresMezcla'):
    content = clean_string(span.contents[0])
    mezcla_mexicana = float(content)
  
  for span in soup.findAll('span', id='tablasIpcIndicadoresPetroleoWti'):
    content = clean_string(span.contents[0])
    wti = float(content)
  
  # Ahora sacamos petroleo brent
  url = 'http://investing.thisismoney.co.uk/security?csi=100815&action=prices&sub_action=history&username=&ac='
  f = urllib2.urlopen(url).read()
  
  f_arr = f.split('<div class="textHeaderUnderline">Price &amp; RiskGrade History</div>')
  f = f_arr[1]
  f_arr = f.split('<!--MSCONTENT-->')
  f = f_arr[0]
  
  soup = BeautifulSoup(f)
  cont = 0
  
  for td in soup.findAll('td', {"class" : re.compile("dataRegularUlOnR|dataRegularUlOffR")}):
    content = td.contents[0].replace(',', '.').replace('$', '')
    brent = float(content)
    break
      
    cont += 1
  
  if(brent != 0 and mezcla_mexicana != 0 and wti != 0):
    # Checamos si ya existe
    try:
      petroleo = Petroleo.objects.filter(fecha = fecha)[0]
    except IndexError:
      petroleo = Petroleo()
    
    petroleo.fecha = fecha
    petroleo.brent = brent
    petroleo.mezcla_mexicana = mezcla_mexicana
    petroleo.wti = wti
    
    petroleo.save()
  
  return direct_to_template(request, 'ajax.html', {'out':'done'})

# Oro
def oro(request):
  if(request.GET and request.GET['_d'] and request.GET['_m'] and request.GET['_y']):
    fecha = "%s-%s-%s" % (request.GET['_y'], request.GET['_m'], request.GET['_d'])
  else:
    last_oro = Oro.objects.all().order_by('-fecha')[0]
    fecha = last_oro.fecha.strftime("%Y-%m-%d")
  
  oros = Oro.objects.filter(fecha__lte=fecha).order_by('-fecha')[:30]
  
  if(len(oros) > 0):
    azteca_compras = []
    azteca_ventas = []
    centenario_compras = []
    centenario_ventas = []
    hidalgo_compras = []
    hidalgo_ventas = []
    oro_libertad_compras = []
    oro_libertad_ventas = []
  
    chart_azteca_compras = []
    chart_azteca_ventas = []
    chart_centenario_compras = []
    chart_centenario_ventas = []
    chart_hidalgo_compras = []
    chart_hidalgo_ventas = []
    chart_oro_libertad_compras = []
    chart_oro_libertad_ventas = []
  
    chart_categories = []
  
    for oro in oros:
      azteca_compras.append(oro.azteca_compra)
      azteca_ventas.append(oro.azteca_venta)
      centenario_compras.append(oro.centenario_compra)
      centenario_ventas.append(oro.centenario_venta)
      hidalgo_compras.append(oro.hidalgo_compra)
      hidalgo_ventas.append(oro.hidalgo_venta)
      oro_libertad_compras.append(oro.oro_libertad_compra)
      oro_libertad_ventas.append(oro.oro_libertad_venta)
    
      chart_azteca_compras.append(str(oro.azteca_compra))
      chart_azteca_ventas.append(str(oro.azteca_venta))
      chart_centenario_compras.append(str(oro.centenario_compra))
      chart_centenario_ventas.append(str(oro.centenario_venta))
      chart_hidalgo_compras.append(str(oro.hidalgo_compra))
      chart_hidalgo_ventas.append(str(oro.hidalgo_venta))
      chart_oro_libertad_compras.append(str(oro.oro_libertad_compra))
      chart_oro_libertad_ventas.append(str(oro.oro_libertad_venta))
    
      chart_categories.append('"%s"' % doDate(oro.fecha.strftime("%Y-%m-%d")))
  
    chart_categories.reverse()
    chart_categories = ','.join(chart_categories)
  
    chart_azteca_compras.reverse()
    chart_azteca_compras = ','.join(chart_azteca_compras)
    chart_azteca_ventas.reverse()
    chart_azteca_ventas = ','.join(chart_azteca_ventas)
    chart_centenario_compras.reverse()
    chart_centenario_compras = ','.join(chart_centenario_compras)
    chart_centenario_ventas.reverse()
    chart_centenario_ventas = ','.join(chart_centenario_ventas)
    chart_hidalgo_compras.reverse()
    chart_hidalgo_compras = ','.join(chart_hidalgo_compras)
    chart_hidalgo_ventas.reverse()
    chart_hidalgo_ventas = ','.join(chart_hidalgo_ventas)
    chart_oro_libertad_compras.reverse()
    chart_oro_libertad_compras = ','.join(chart_oro_libertad_compras)
    chart_oro_libertad_ventas.reverse()
    chart_oro_libertad_ventas = ','.join(chart_oro_libertad_ventas)
  
    azteca_compras = get_stats(azteca_compras)
    azteca_ventas = get_stats(azteca_ventas)
    centenario_compras = get_stats(centenario_compras)
    centenario_ventas = get_stats(centenario_ventas)
    hidalgo_compras = get_stats(hidalgo_compras)
    hidalgo_ventas = get_stats(hidalgo_ventas)
    oro_libertad_compras = get_stats(oro_libertad_compras)
    oro_libertad_ventas = get_stats(oro_libertad_ventas)
  
    return direct_to_template(request, 'divisas/oro.html', {
      'fecha':fecha,
      'oros':oros,
      'azteca_compras':azteca_compras,
      'azteca_ventas':azteca_ventas,
      'centenario_compras':centenario_compras,
      'centenario_ventas':centenario_ventas,
      'hidalgo_compras':hidalgo_compras,
      'hidalgo_ventas':hidalgo_ventas,
      'oro_libertad_compras':oro_libertad_compras,
      'oro_libertad_ventas':oro_libertad_ventas,
      'chart_azteca_compras':chart_azteca_compras,
      'chart_azteca_ventas':chart_azteca_ventas,
      'chart_centenario_compras':chart_centenario_compras,
      'chart_centenario_ventas':chart_centenario_ventas,
      'chart_hidalgo_compras':chart_hidalgo_compras,
      'chart_hidalgo_ventas':chart_hidalgo_ventas,
      'chart_oro_libertad_compras':chart_oro_libertad_compras,
      'chart_oro_libertad_ventas':chart_oro_libertad_ventas,
      'chart_title':'Oro',
      'chart_source':'Banamex',
      'chart_categories':chart_categories
    })
  else:
    messages.add_message(request, messages.ERROR, 'No encontramos valores para la fecha seleccionada.')
    return HttpResponseRedirect('/divisas/oro/')

# Metales
def metales(request):
  if(request.GET and request.GET['_d'] and request.GET['_m'] and request.GET['_y']):
    fecha = "%s-%s-%s" % (request.GET['_y'], request.GET['_m'], request.GET['_d'])
  else:
    last_metales = Metal.objects.all().order_by('-fecha')[0]
    fecha = last_metales.fecha.strftime("%Y-%m-%d")
  
  metals = Metal.objects.filter(fecha__lte=fecha).order_by('-fecha')[:30]
  
  if(len(metals) > 0):
    aluminios = []
    aluminio_nys = []
    cobre_alambron_nys = []
    platino_nys = []
    plomos = []
    zincs = []
  
    chart_aluminios = []
    chart_aluminio_nys = []
    chart_cobre_alambron_nys = []
    chart_platino_nys = []
    chart_plomos = []
    chart_zincs = []
  
    chart_categories = []
  
    for metal in metals:
      aluminios.append(metal.aluminio)
      aluminio_nys.append(metal.aluminio_ny)
      cobre_alambron_nys.append(metal.cobre_alambron_ny)
      platino_nys.append(metal.platino_ny)
      plomos.append(metal.plomo)
      zincs.append(metal.zinc)
    
      chart_aluminios.append(str(metal.aluminio))
      chart_aluminio_nys.append(str(metal.aluminio_ny))
      chart_cobre_alambron_nys.append(str(metal.cobre_alambron_ny))
      chart_platino_nys.append(str(metal.platino_ny))
      chart_plomos.append(str(metal.plomo))
      chart_zincs.append(str(metal.zinc))
    
      chart_categories.append('"' + doDate(metal.fecha.strftime("%Y-%m-%d")) + '"')
  
    valores_aluminios = aluminios
    valores_aluminio_nys = aluminio_nys
    valores_cobre_alambron_nys = cobre_alambron_nys
    valores_platino_nys = platino_nys
    valores_plomos = plomos
    valores_zincs = zincs
  
    chart_categories.reverse()
    chart_categories = ','.join(chart_categories)
    chart_aluminios.reverse()
    chart_aluminios = ','.join(chart_aluminios)
    chart_aluminio_nys.reverse()
    chart_aluminio_nys = ','.join(chart_aluminio_nys)
    chart_cobre_alambron_nys.reverse()
    chart_cobre_alambron_nys = ','.join(chart_cobre_alambron_nys)
    chart_platino_nys.reverse()
    chart_platino_nys = ','.join(chart_platino_nys)
    chart_plomos.reverse()
    chart_plomos = ','.join(chart_plomos)
    chart_zincs.reverse()
    chart_zincs = ','.join(chart_zincs)
  
    valores_aluminios = get_stats(valores_aluminios)
    valores_aluminio_nys = get_stats(valores_aluminio_nys)
    valores_cobre_alambron_nys = get_stats(valores_cobre_alambron_nys)
    valores_platino_nys = get_stats(valores_platino_nys)
    valores_plomos = get_stats(valores_plomos)
    valores_zincs = get_stats(valores_zincs)
  
    return direct_to_template(request, 'divisas/metales.html', {
      'fecha':fecha,
      'metals':metals,
      'aluminios':aluminios,
      'aluminio_nys':aluminio_nys,
      'cobre_alambron_nys':cobre_alambron_nys,
      'platino_nys':platino_nys,
      'plomos':plomos,
      'zincs':zincs,
      'chart_aluminios':chart_aluminios,
      'chart_aluminio_nys':chart_aluminio_nys,
      'chart_cobre_alambron_nys':chart_cobre_alambron_nys,
      'chart_platino_nys':chart_platino_nys,
      'chart_plomos':chart_plomos,
      'chart_zincs':chart_zincs,
      'valores_aluminios':valores_aluminios,
      'valores_aluminio_nys':valores_aluminio_nys,
      'valores_cobre_alambron_nys':valores_cobre_alambron_nys,
      'valores_platino_nys':valores_platino_nys,
      'valores_plomos':valores_plomos,
      'valores_zincs':valores_zincs,
      'chart_title':'Metales',
      'chart_source':'CNN Expansi&oacute;n',
      'chart_categories':chart_categories
    })
  else:
    messages.add_message(request, messages.ERROR, 'No encontramos valores para la fecha seleccionada.')
    return HttpResponseRedirect('/divisas/metales/')

# Cron Metales
def cron_metales(request):
  from datetime import date
  import urllib2
  from BeautifulSoup import BeautifulSoup
  
  fecha = date.today().strftime("%Y-%m-%d")
  
  # Metales
  
  url = 'http://finanzasenlinea.infosel.com/cnnexpansion/metales.aspx'
  f = urllib2.urlopen(url).read()
  soup = BeautifulSoup(f)
  
  cont = 0
  
  aluminio = 0
  aluminio_ny = 0
  cobre_alambron_ny = 0
  platino_ny = 0
  plomo = 0
  zinc = 0

  for span in soup.findAll('span', id='lblAlumny'):
    content = clean_string(span.contents[0])
    aluminio_ny = float(content.replace(',', ''))

  for span in soup.findAll('span', id='lblCobreny'):
    content = clean_string(span.contents[0])
    cobre_alambron_ny = float(content.replace(',', ''))

  for span in soup.findAll('span', id='lblPlomony'):
    content = clean_string(span.contents[0])
    plomo = float(content.replace(',', ''))

  for span in soup.findAll('span', id='lblZincny'):
    content = clean_string(span.contents[0])
    zinc = float(content.replace(',', ''))

  if(aluminio_ny != 0 and cobre_alambron_ny != 0 and plomo != 0 and zinc != 0):
    # Checamos si ya existe
    try:
      metal = Metal.objects.filter(fecha = fecha)[0]
    except IndexError:
      metal = Metal()
    
    metal.fecha = fecha
    metal.aluminio = aluminio
    metal.aluminio_ny = aluminio_ny
    metal.cobre_alambron_ny = cobre_alambron_ny
    metal.platino_ny = platino_ny
    metal.plomo = plomo
    metal.zinc = zinc

    metal.save()
  
  # Oro
  
  url = 'http://www.banamex.com/esp/finanzas/divisas/divisas_metales.jsp'
  f = urllib2.urlopen(url).read()
  soup = BeautifulSoup(f)
  
  cont = 0
  
  azteca_compra = 0
  azteca_venta = 0
  centenario_compra = 0
  centenario_venta = 0
  onza_troy_compra = 0
  onza_troy_venta = 0
  hidalgo_compra = 0
  hidalgo_venta = 0
  plata_libertad_compra = 0
  plata_libertad_venta = 0
  oro_libertad_compra = 0
  oro_libertad_venta = 0
  
  for div in soup.findAll('div', align="right"):
    try:
      content = clean_string(div.contents[0]).replace(',', '')
    except:
      content = ""
    
    if(cont == 4):
      azteca_compra = content
    elif(cont == 5):
      azteca_venta = content
    elif(cont == 7):
      centenario_compra = content
    elif(cont == 8):
      centenario_venta = content
    elif(cont == 10):
      onza_troy_compra = content
    elif(cont == 11):
      onza_troy_venta = content
    elif(cont == 13):
      hidalgo_compra = content
    elif(cont == 14):
      hidalgo_venta = content
    elif(cont == 25):
      plata_libertad_compra = content
    elif(cont == 26):
      plata_libertad_venta = content
    elif(cont == 49):
      oro_libertad_compra = content
    elif(cont == 50):
      oro_libertad_venta = content
      break
    
    cont += 1
  
  if(azteca_compra != 0 and azteca_venta != 0 and centenario_compra != 0 and centenario_venta != 0 and onza_troy_compra != 0 and onza_troy_venta != 0 and hidalgo_compra != 0 and hidalgo_venta != 0 and plata_libertad_compra != 0 and plata_libertad_venta != 0 and oro_libertad_compra != 0 and oro_libertad_venta != 0):
    # Checamos si ya existe oro
    try:
      oro = Oro.objects.filter(fecha = fecha)[0]
    except IndexError:
      oro = Oro()
    
    oro.fecha = fecha
    oro.azteca_compra = azteca_compra
    oro.azteca_venta = azteca_venta
    oro.centenario_compra = centenario_compra
    oro.centenario_venta = centenario_venta
    oro.hidalgo_compra = hidalgo_compra
    oro.hidalgo_venta = hidalgo_venta
    oro.oro_libertad_compra = oro_libertad_compra
    oro.oro_libertad_venta = oro_libertad_venta
    
    oro.save()
    
    # Checamos si ya existe plata
    try:
      plata = Plata.objects.filter(fecha = fecha)[0]
    except IndexError:
      plata = Plata()
    
    plata.fecha = fecha
    plata.onza_troy_compra = onza_troy_compra
    plata.onza_troy_venta = onza_troy_venta
    plata.plata_libertad_compra = plata_libertad_compra
    plata.plata_libertad_venta = plata_libertad_venta
    
    plata.save()
  
  return direct_to_template(request, 'ajax.html', {'out':'done'})

# Yen
def yen(request):
  if(request.GET and request.GET['_d'] and request.GET['_m'] and request.GET['_y']):
    fecha = "%s-%s-%s" % (request.GET['_y'], request.GET['_m'], request.GET['_d'])
  else:
    last_yen = Yen.objects.all().order_by('-fecha')[0]
    fecha = last_yen.fecha.strftime("%Y-%m-%d")
  
  yens = Yen.objects.filter(fecha__lte=fecha).order_by('-fecha')[:30]
  
  if(len(yens) > 0):
    valores = []
  
    chart_valores = []
    chart_categories = []
  
    for yen in yens:
      valores.append(yen.valor)
    
      chart_valores.append(str(yen.valor))
      chart_categories.append('"' + doDate(yen.fecha.strftime("%Y-%m-%d")) + '"')
  
    chart_categories.reverse()
    chart_categories = ','.join(chart_categories)
    chart_valores.reverse()
    chart_valores = ','.join(chart_valores)
  
    valores = get_stats(valores)
  
    return direct_to_template(request, 'divisas/yen.html', {
      'fecha':fecha,
      'yens':yens,
      'arr_valores':yens,
      'valores':valores,
      'valores_no_format':True,
      'chart_title':'Yen',
      'chart_source':'Banco de M&eacute;xico',
      'chart_categories':chart_categories,
      'chart_valores':chart_valores
    })
  else:
    messages.add_message(request, messages.ERROR, 'No encontramos valores para la fecha seleccionada.')
    return HttpResponseRedirect('/divisas/yen/')

# Libra
def libra(request):
  if(request.GET and request.GET['_d'] and request.GET['_m'] and request.GET['_y']):
    fecha = "%s-%s-%s" % (request.GET['_y'], request.GET['_m'], request.GET['_d'])
  else:
    last_libra = Libra.objects.all().order_by('-fecha')[0]
    fecha = last_libra.fecha.strftime("%Y-%m-%d")
  
  libras = Libra.objects.filter(fecha__lte=fecha).order_by('-fecha')[:30]
  
  if(len(libras) > 0):
    valores = []
  
    chart_valores = []
    chart_categories = []
  
    for libra in libras:
      valores.append(libra.valor)
    
      chart_valores.append(str(libra.valor))
      chart_categories.append('"' + doDate(libra.fecha.strftime("%Y-%m-%d")) + '"')
  
    chart_categories.reverse()
    chart_categories = ','.join(chart_categories)
    chart_valores.reverse()
    chart_valores = ','.join(chart_valores)
  
    valores = get_stats(valores)
  
    return direct_to_template(request, 'divisas/libra.html', {
      'fecha':fecha,
      'libras':libras,
      'arr_valores':libras,
      'valores':valores,
      'chart_title':'Libra',
      'chart_source':'Banco de M&eacute;xico',
      'chart_categories':chart_categories,
      'chart_valores':chart_valores
    })
  else:
    messages.add_message(request, messages.ERROR, 'No encontramos valores para la fecha seleccionada.')
    return HttpResponseRedirect('/divisas/libra/')

# DEG
def deg(request):
  if(request.GET and request.GET['_d'] and request.GET['_m'] and request.GET['_y']):
    fecha = "%s-%s-%s" % (request.GET['_y'], request.GET['_m'], request.GET['_d'])
  else:
    last_deg = Deg.objects.all().order_by('-fecha')[0]
    fecha = last_deg.fecha.strftime("%Y-%m-%d")
  
  degs = Deg.objects.filter(fecha__lte=fecha).order_by('-fecha')[:30]
  
  if(len(degs) > 0):
    valores = []
  
    chart_valores = []
    chart_categories = []
  
    for deg in degs:
      valores.append(deg.valor)
    
      chart_valores.append(str(deg.valor))
      chart_categories.append('"' + doDate(deg.fecha.strftime("%Y-%m-%d")) + '"')
  
    chart_categories.reverse()
    chart_categories = ','.join(chart_categories)
    chart_valores.reverse()
    chart_valores = ','.join(chart_valores)
  
    valores = get_stats(valores)
  
    return direct_to_template(request, 'divisas/deg.html', {
      'fecha':fecha,
      'degs':degs,
      'arr_valores':degs,
      'valores':valores,
      'chart_title':'Derecho Especial de giro',
      'chart_source':'Banco de M&eacute;xico',
      'chart_categories':chart_categories,
      'chart_valores':chart_valores
    })
  else:
    messages.add_message(request, messages.ERROR, 'No encontramos valores para la fecha seleccionada.')
    return HttpResponseRedirect('/divisas/deg/')

# Grafica del euro
def img_euro(request):
  from django.conf import settings
  from django.core.cache import cache
  import cStringIO
  import matplotlib
  matplotlib.use('Agg')
  import matplotlib.pyplot as plt
  import matplotlib.ticker as ticker
  import matplotlib as mpl
  
  mpl.rcParams['axes.titlesize'] = '8'
  
  img_name = 'img_euro'
  
  # Checamos si hay cache
  ic = cache.get(img_name)
  
  if(ic):
    response = HttpResponse(ic, mimetype='image/png')
  else:
    output = cStringIO.StringIO()
    
    euros = Euro.objects.all().order_by('-id')[:30]
    
    valores = []
    compras = []
    ventas = []
    fechas = []
    
    cont = 0
    
    for euro in euros:
      valores.append(euro.valor)
      compras.append(euro.promedio_compra)
      ventas.append(euro.promedio_venta)
      
      if(cont == 0 or cont == len(euros) - 1):
        fechas.append(doDate(euro.fecha))
      else:
        fechas.append('')
      
      cont += 1
    
    valores.reverse()
    compras.reverse()
    ventas.reverse()
    fechas.reverse()

    plot = plt.figure(figsize=[4.5,1.5], dpi=100)
    ax = plot.add_subplot(111)
    plt.title('Euro')
    ax.plot(valores)
    ax.plot(compras)
    ax.plot(ventas)
    
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

# Euro
def euro(request):
  if(request.GET and request.GET['_d'] and request.GET['_m'] and request.GET['_y']):
    fecha = "%s-%s-%s" % (request.GET['_y'], request.GET['_m'], request.GET['_d'])
  else:
    last_euro = Euro.objects.all().order_by('-fecha')[0]
    fecha = last_euro.fecha.strftime("%Y-%m-%d")
  
  euros = Euro.objects.filter(fecha__lte=fecha).order_by('-fecha')[:30]
  
  if(len(euros) > 0):
    valores = []
    valores_compras = []
    valores_ventas = []
    valores_bancomer_compras = []
    valores_bancomer_ventas = []
    valores_banorte_compras = []
    valores_banorte_ventas = []
    valores_banamex_compras = []
    valores_banamex_ventas = []
    valores_santander_compras = []
    valores_santander_ventas = []
  
    chart_valores = []
    chart_categories = []
    chart_compras = []
    chart_ventas = []
  
    for euro in euros:
      valores.append(euro.valor)
      valores_compras.append(euro.promedio_compra)
      valores_ventas.append(euro.promedio_venta)
      valores_bancomer_compras.append(euro.bancomer_compra)
      valores_bancomer_ventas.append(euro.bancomer_venta)
      valores_banorte_compras.append(euro.banorte_compra)
      valores_banorte_ventas.append(euro.banorte_venta)
      valores_banamex_compras.append(euro.banamex_compra)
      valores_banamex_ventas.append(euro.banamex_venta)
      valores_santander_compras.append(euro.santander_compra)
      valores_santander_ventas.append(euro.santander_venta)
    
      chart_valores.append(str(euro.valor))
      chart_compras.append(str(euro.promedio_compra))
      chart_ventas.append(str(euro.promedio_venta))
      chart_categories.append('"' + doDate(euro.fecha.strftime("%Y-%m-%d")) + '"')
  
    chart_categories.reverse()
    chart_categories = ','.join(chart_categories)
    chart_valores.reverse()
    chart_valores = ','.join(chart_valores)
    chart_compras.reverse()
    chart_compras = ','.join(chart_compras)
    chart_ventas.reverse()
    chart_ventas = ','.join(chart_ventas)
  
    valores = get_stats(valores)
    valores_compras = get_stats(valores_compras)
    valores_ventas = get_stats(valores_ventas)
    valores_bancomer_compras = get_stats(valores_bancomer_compras)
    valores_bancomer_ventas = get_stats(valores_bancomer_ventas)
    valores_banorte_compras = get_stats(valores_banorte_compras)
    valores_banorte_ventas = get_stats(valores_banorte_ventas)
    valores_banamex_compras = get_stats(valores_banamex_compras)
    valores_banamex_ventas = get_stats(valores_banamex_ventas)
    valores_santander_compras = get_stats(valores_santander_compras)
    valores_santander_ventas = get_stats(valores_santander_ventas)
  
    return direct_to_template(request, 'divisas/euro.html', {
      'fecha':fecha,
      'euros':euros,
      'valores':valores,
      'valores_compras':valores_compras,
      'valores_ventas':valores_ventas,
      'valores_bancomer_compras':valores_bancomer_compras,
      'valores_bancomer_ventas':valores_bancomer_ventas,
      'valores_banorte_compras':valores_banorte_compras,
      'valores_banorte_ventas':valores_banorte_ventas,
      'valores_banamex_compras':valores_banamex_compras,
      'valores_banamex_ventas':valores_banamex_ventas,
      'valores_santander_compras':valores_santander_compras,
      'valores_santander_ventas':valores_santander_ventas,
      'chart_title':'Euro',
      'chart_source':'Banco de M&eacute;xico',
      'chart_categories':chart_categories,
      'chart_valores':chart_valores,
      'chart_compras':chart_compras,
      'chart_ventas':chart_ventas
    })
  else:
    messages.add_message(request, messages.ERROR, 'No encontramos valores para la fecha seleccionada.')
    return HttpResponseRedirect('/divisas/euro/')

# Cron Euro
def cron_euro(request):
  from datetime import date
  import urllib2
  from BeautifulSoup import BeautifulSoup
  
  fecha = date.today().strftime("%Y-%m-%d")
  
  url = 'http://www.banxico.org.mx/SieInternet/consultarDirectorioInternetAction.do?accion=consultarCuadroAnalitico&idCuadro=CA91&sector=6&locale=es'
  f = urllib2.urlopen(url).read()
  farr = f.split('</form>')
  f = '<html><body>' + farr[1]
  
  soup = BeautifulSoup(f)
  
  fechas = []
  euros = []
  degs = []
  libras = []
  yens = []
  
  cont = 0
  
  for tr in soup.findAll('tr', {"class" : "cd_titulos_tabla"}):
    cont += 1
    
    for td in tr.findAll('td'):
      if(cont == 2):
        content = clean_string(td.contents[0])
        
        fechas.append(content)
      elif(cont > 2):
        break
        break
  
  cont = 0
  
  for tr in soup.findAll('tr', {"class" : "cd_tabla_renglon"}):
    cont += 1
    td_cont = 0
    
    for td in tr.findAll('td'):
      td_cont += 1
      
      content = clean_string(td.contents[0])
      
      if(cont == 2 and td_cont > 1):
        yens.append(float(content))
      elif(cont == 3 and td_cont > 1):
        degs.append(float(content))
  
  cont = 0
  
  for tr in soup.findAll('tr', {"class" : "cd_tabla_renglon_subrayado"}):
    cont += 1
    td_cont = 0
    
    for td in tr.findAll('td'):
      td_cont += 1
      
      content = clean_string(td.contents[0])
      
      if(cont == 1 and td_cont > 1):
        euros.append(float(content))
      elif(cont == 2 and td_cont > 1):
        libras.append(float(content))
  
  if(euros[0] != 0 and degs[0] != 0 and libras[0] != 0 and yens[0] != 0):
    # Euro
    # Checamos si ya existe
    try:
      euro = Euro.objects.filter(fecha = fecha)[0]
    except IndexError:
      euro = Euro()
    
    euro.fecha = fecha
    euro.valor = euros[0]
    
    euro.save()
    
    # DEG
    # Checamos si ya existe
    try:
      deg = Deg.objects.filter(fecha = fecha)[0]
    except IndexError:
      deg = Deg()
    
    deg.fecha = fecha
    deg.valor = degs[0]
    
    deg.save()
    
    # Libra
    # Checamos si ya existe
    try:
      libra = Libra.objects.filter(fecha = fecha)[0]
    except IndexError:
      libra = Libra()
    
    libra.fecha = fecha
    libra.valor = libras[0]
    
    libra.save()
    
    # Yen
    # Checamos si ya existe
    try:
      yen = Yen.objects.filter(fecha = fecha)[0]
    except IndexError:
      yen = Yen()
    
    yen.fecha = fecha
    yen.valor = yens[0]
    
    yen.save()
    
    # Bancos
    
    promedio_compra = []
    promedio_venta = []
    
    # Banorte
    
    url = 'http://www.banorte.com/portal/portlets/bursatil/change.do?trends=23g&wlw-select_key:{actionForm.filter}OldValue=true&wlw-select_key:{actionForm.filter}=7'
    f = urllib2.urlopen(url).read()
    soup = BeautifulSoup(f)
    
    cont = 0
    
    banorte_compra = 0
    banorte_venta = 0
    
    for div in soup.findAll('div', align="center"):
      try:
        content = clean_string(div.contents[0])
      except:
        content = ""
      
      if(cont == 5):
        banorte_compra = float(content)
      elif(cont == 6):
        banorte_venta = float(content)
        break
      
      cont += 1
    
    if(banorte_compra != 0 and banorte_venta != 0):
      euro.banorte_compra = banorte_compra
      euro.banorte_venta = banorte_venta
      
      promedio_compra.append(banorte_compra)
      promedio_venta.append(banorte_venta)
    
    # Bancomer
    
    url = 'http://bbv.terra.com.mx/bancomerindicators/mainboard5.html'
    f = urllib2.urlopen(url).read()
    soup = BeautifulSoup(f)
    
    cont = 0
    
    bancomer_compra = 0
    bancomer_venta = 0
    
    for link in soup.findAll('a', {'class':'tx_ind3'}):
      content = clean_string(link.contents[0])
      
      if(cont == 9):
        bancomer_compra = float(content)
      elif(cont == 11):
        bancomer_venta = float(content)
        break
      
      cont += 1
    
    if(bancomer_compra != 0 and bancomer_venta != 0):
      euro.bancomer_compra = bancomer_compra
      euro.bancomer_venta = bancomer_venta

      promedio_compra.append(bancomer_compra)
      promedio_venta.append(bancomer_venta)
    
    # Banamex
    
    url = 'http://www.banamex.com/esp/finanzas/divisas/divisas.html'
    banamex_compra = 0
    banamex_venta = 0
    try:
      f = urllib2.urlopen(url).read()
      soup = BeautifulSoup(f)
      
      cont = 0
      
      for td in soup.findAll('td', align="right"):
        content = clean_string(td.contents[0])
      
        if(cont == 10):
          banamex_compra = float(content)
        elif(cont == 11):
          banamex_venta = float(content)
          break
        
        cont += 1
    except:
      pass

    
    euro.banamex_compra = banamex_compra
    euro.banamex_venta = banamex_venta

    if(banamex_compra != 0 and banamex_venta != 0):
      promedio_compra.append(banamex_compra)
      promedio_venta.append(banamex_venta)
    
    # Santander

    url = 'http://feed.efinf.com/ds/santander/index.jsp'
    f = urllib2.urlopen(url).read()
    soup = BeautifulSoup(f)

    cont = 0

    santander_compra = 0
    santander_venta = 0
    
    for p in soup.findAll('p'):
      content = clean_string(p.contents[0])
      
      if(cont == 33):
        santander_compra = float(content)
      elif(cont == 34):
        santander_venta = float(content)
        break
      
      cont += 1
    
    if(santander_compra != 0 and santander_venta != 0):
      euro.santander_compra = santander_compra
      euro.santander_venta = santander_venta

      promedio_compra.append(santander_compra)
      promedio_venta.append(santander_venta)
    
    # Guardamos
    euro.promedio_compra = array(promedio_compra).mean()
    euro.promedio_venta = array(promedio_venta).mean()
    
    euro.save()
  
  return direct_to_template(request, 'ajax.html', {'out':'done'})

# Grafica del dolar
def img_dolar(request):
  from django.conf import settings
  from django.core.cache import cache
  import cStringIO
  import matplotlib
  matplotlib.use('Agg')
  import matplotlib.pyplot as plt
  import matplotlib.ticker as ticker
  import matplotlib as mpl
  
  mpl.rcParams['axes.titlesize'] = '8'
  
  img_name = 'img_dolar'
  
  # Checamos si hay cache
  ic = cache.get(img_name)
  
  if(ic):
    response = HttpResponse(ic, mimetype='image/png')
  else:
    output = cStringIO.StringIO()
    
    dolars = Dolar.objects.all().order_by('-id')[:30]
    
    valores = []
    compras = []
    ventas = []
    fechas = []
    
    cont = 0
    
    for dolar in dolars:
      valores.append(dolar.valor)
      compras.append(dolar.promedio_compra)
      ventas.append(dolar.promedio_venta)
      
      if(cont == 0 or cont == len(dolars) - 1):
        fechas.append(doDate(dolar.fecha))
      else:
        fechas.append('')
      
      cont += 1

    valores.reverse()
    compras.reverse()
    ventas.reverse()
    fechas.reverse()
    
    plot = plt.figure(figsize=[4.5,1.5], dpi=100)
    ax = plot.add_subplot(111)
    plt.title('Dolar')
    ax.plot(valores)
    ax.plot(compras)
    ax.plot(ventas)
    
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

# Dolar
def dolar(request):
  if(request.GET and request.GET['_d'] and request.GET['_m'] and request.GET['_y']):
    fecha = "%s-%s-%s" % (request.GET['_y'], request.GET['_m'], request.GET['_d'])
  else:
    last_dolar = Dolar.objects.all().order_by('-fecha')[0]
    fecha = last_dolar.fecha.strftime("%Y-%m-%d")
  
  dolars = Dolar.objects.filter(fecha__lte=fecha).order_by('-fecha')[:30]
  
  if(len(dolars) > 0):
    valores = []
    valores_compras = []
    valores_ventas = []
    valores_bancomer_compras = []
    valores_bancomer_ventas = []
    valores_banorte_compras = []
    valores_banorte_ventas = []
    valores_banamex_compras = []
    valores_banamex_ventas = []
    valores_santander_compras = []
    valores_santander_ventas = []
    valores_ixe_compras = []
    valores_ixe_ventas = []
  
    chart_valores = []
    chart_categories = []
    chart_compras = []
    chart_ventas = []
  
    for dolar in dolars:
      valores.append(dolar.valor)
      valores_compras.append(dolar.promedio_compra)
      valores_ventas.append(dolar.promedio_venta)
      valores_bancomer_compras.append(dolar.bancomer_compra)
      valores_bancomer_ventas.append(dolar.bancomer_venta)
      valores_banorte_compras.append(dolar.banorte_compra)
      valores_banorte_ventas.append(dolar.banorte_venta)
      valores_banamex_compras.append(dolar.banamex_compra)
      valores_banamex_ventas.append(dolar.banamex_venta)
      valores_santander_compras.append(dolar.santander_compra)
      valores_santander_ventas.append(dolar.santander_venta)
      valores_ixe_compras.append(dolar.ixe_compra)
      valores_ixe_ventas.append(dolar.ixe_venta)
    
      chart_valores.append(str(dolar.valor))
      chart_compras.append(str(dolar.promedio_compra))
      chart_ventas.append(str(dolar.promedio_venta))
      chart_categories.append('"' + doDate(dolar.fecha.strftime("%Y-%m-%d")) + '"')
  
    chart_categories.reverse()
    chart_categories = ','.join(chart_categories)
    chart_valores.reverse()
    chart_valores = ','.join(chart_valores)
    chart_compras.reverse()
    chart_compras = ','.join(chart_compras)
    chart_ventas.reverse()
    chart_ventas = ','.join(chart_ventas)
  
    valores = get_stats(valores)
    valores_compras = get_stats(valores_compras)
    valores_ventas = get_stats(valores_ventas)
    valores_bancomer_compras = get_stats(valores_bancomer_compras)
    valores_bancomer_ventas = get_stats(valores_bancomer_ventas)
    valores_banorte_compras = get_stats(valores_banorte_compras)
    valores_banorte_ventas = get_stats(valores_banorte_ventas)
    valores_banamex_compras = get_stats(valores_banamex_compras)
    valores_banamex_ventas = get_stats(valores_banamex_ventas)
    valores_santander_compras = get_stats(valores_santander_compras)
    valores_santander_ventas = get_stats(valores_santander_ventas)
    valores_ixe_compras = get_stats(valores_ixe_compras)
    valores_ixe_ventas = get_stats(valores_ixe_ventas)
  
    return direct_to_template(request, 'divisas/dolar.html', {
      'fecha':fecha,
      'dolars':dolars,
      'valores':valores,
      'valores_compras':valores_compras,
      'valores_ventas':valores_ventas,
      'valores_bancomer_compras':valores_bancomer_compras,
      'valores_bancomer_ventas':valores_bancomer_ventas,
      'valores_banorte_compras':valores_banorte_compras,
      'valores_banorte_ventas':valores_banorte_ventas,
      'valores_banamex_compras':valores_banamex_compras,
      'valores_banamex_ventas':valores_banamex_ventas,
      'valores_santander_compras':valores_santander_compras,
      'valores_santander_ventas':valores_santander_ventas,
      'valores_ixe_compras':valores_ixe_compras,
      'valores_ixe_ventas':valores_ixe_ventas,
      'chart_title':'D&oacute;lar',
      'chart_source':'Banco de M&eacute;xico',
      'chart_categories':chart_categories,
      'chart_valores':chart_valores,
      'chart_compras':chart_compras,
      'chart_ventas':chart_ventas
    })
  else:
    messages.add_message(request, messages.ERROR, 'No encontramos valores para la fecha seleccionada.')
    return HttpResponseRedirect("/divisas/dolar/")

# Cron Dolar
def cron_dolar(request):
  import re
  import urllib2
  from BeautifulSoup import BeautifulSoup
  
  url = 'http://www.banxico.gob.mx/tipcamb/tipCamMIAction.do?idioma=sp'
  f = urllib2.urlopen(url).read()
  soup = BeautifulSoup(f)
  
  fecha = ""
  valor = ""
  
  for tr in soup.findAll('tr', {"class" : re.compile("renglonNon|reglonPar")}):
    tds = tr.findAll('td')
    
    fecha = clean_string(tds[0].contents[0])
    valor = clean_string(tds[1].contents[0])
    
    farr = fecha.split('/')
    
    fecha = farr[2] + '-' + farr[1] + '-' +farr[0]
    
    break
  
  if(fecha != "" and valor != ""):
    # Checamos si ya existe
    try:
      dolar = Dolar.objects.filter(fecha = fecha)[0]
    except IndexError:
      dolar = Dolar()
    
    dolar.fecha = fecha
    
    # Checamos si es caso especial
    if(valor == "N/E"):
      last_dolar = Dolar.objects.all().order_by('-fecha')[0]
      
      dolar.valor = last_dolar.valor
    else:
      dolar.valor = float(valor)
    
    dolar.save()
    
    # Ahora sacamos valores de los bancos
    
    promedio_compra = []
    promedio_venta = []
    
    # Banorte
    
    url = 'http://www.banorte.com/portal/portlets/bursatil/change.do?trends=23a'
    f = urllib2.urlopen(url).read()
    soup = BeautifulSoup(f)
    
    cont = 0
    
    banorte_compra = 0
    banorte_venta = 0
    
    for div in soup.findAll('div'):
      try:
        content = clean_string(div.contents[0])
      
        if(content == 'Ventanilla'):
          start_banorte = True
        elif(start_banorte):
          cont += 1
          
          if(cont == 1):
            banorte_compra = float(content.replace('$', ''))
          elif(cont == 2):
            banorte_venta = float(content.replace('$', ''))
      except:
        pass
    
    if(banorte_compra != 0 and banorte_venta != 0):
      dolar.banorte_compra = banorte_compra
      dolar.banorte_venta = banorte_venta
      
      promedio_compra.append(banorte_compra)
      promedio_venta.append(banorte_venta)
    
    # Bancomer
    
    url = 'http://bbv.terra.com.mx/bancomerindicators/index.aspx'
    f = urllib2.urlopen(url).read()
    
    # Arreglamos HTML, viene mal
    f_arr = f.split('<table cellSpacing="0" width="100%" border="0" cellPadding="0">')
    f = f_arr[1]
    f_arr = f.split('<html>')
    f = f_arr[0]

    soup = BeautifulSoup(f)
    
    cont = 0
    
    bancomer_compra = 0
    bancomer_venta = 0
    
    start_bancomer = False

    for td in soup.findAll('td'):
      try:
        content = clean_string(td.find('a').contents[0])
      except AttributeError:
        content = clean_string(td.contents[0])
      
      if(not start_bancomer and re.search('compra', content, re.I)):
        cont += 1
        
        start_bancomer = True
        cont = 0
      elif(start_bancomer):
        cont +=1
        
        if(cont == 1):
          bancomer_compra = float(content)
        elif(cont == 6):
          bancomer_venta = float(content)

    if(bancomer_compra != 0 and bancomer_venta != 0):
      dolar.bancomer_compra = bancomer_compra
      dolar.bancomer_venta = bancomer_venta

      promedio_compra.append(bancomer_compra)
      promedio_venta.append(bancomer_venta)
    
    # Banamex
    
    url = 'http://www.banamex.com/esp/finanzas/divisas/divisas.html'
    banamex_compra = 0
    banamex_venta = 0
    try:
      f = urllib2.urlopen(url).read()
        
      soup = BeautifulSoup(f)
      
      cont = 0
      
      start_banamex = False
      
      for td in soup.findAll('td'):
        try:
          content = clean_string(td.contents[0])
        except:
          content = ''
        
        if(not start_banamex and re.search('ventanilla', content, re.I)):
          start_banamex = True
        elif(start_banamex):
          cont += 1
        
          if(cont == 4):
            banamex_compra = float(content)
          if(cont == 5):
            banamex_venta = float(content)
    except:
      pass
    
    dolar.banamex_compra = banamex_compra
    dolar.banamex_venta = banamex_venta

    if(banamex_compra != 0 and banamex_venta != 0):
      promedio_compra.append(banamex_compra)
      promedio_venta.append(banamex_venta)

    # Santander
    
    url = 'http://feed.efinf.com/ds/santander/index.jsp'
    f = urllib2.urlopen(url).read()
    
    soup = BeautifulSoup(f)
    
    cont = 0
    
    santander_compra = 0
    santander_venta = 0
    
    start_santander = False
    
    for tr in soup.findAll('tr', id="evenr"):
      tds = tr.findAll('td')
      
      for td in tds:
        try:
          content = clean_string(td.find('p').contents[0])
        except:
          content = ""
      
        if(not start_santander and content == "DOLAR"):
          start_santander = True
        elif(start_santander):
          if(cont == 0):
            santander_compra = float(content)
          elif(cont == 1):
            santander_venta = float(content)
          else:
            break
          
          cont += 1
    
    if(santander_compra != 0 and santander_venta != 0):
      dolar.santander_compra = santander_compra
      dolar.santander_venta = santander_venta

      promedio_compra.append(santander_compra)
      promedio_venta.append(santander_venta)
    
    # IXE
    
    url = 'http://finanzasenlinea.terra.com.mx/ixe/tabla.aspx'
    f = urllib2.urlopen(url).read()

    soup = BeautifulSoup(f)

    cont = 0

    ixe_compra = 0
    ixe_venta = 0

    start_ixe = False
    
    span = soup.find('span', id="lblCompra")
    ixe_compra = float(clean_string(span.contents[0]))
    
    span = soup.find('span', id="lblVenta")
    ixe_venta = float(clean_string(span.contents[0]))
    
    if(ixe_compra != 0 and santander_venta != 0):
      dolar.ixe_compra = ixe_compra
      dolar.ixe_venta = ixe_venta

      promedio_compra.append(ixe_compra)
      promedio_venta.append(ixe_venta)
    
    # Guardamos datos
    dolar.promedio_compra = array(promedio_compra).mean()
    dolar.promedio_venta = array(promedio_venta).mean()
    
    dolar.save()
  
  return direct_to_template(request, 'ajax.html', {'out':'done'})
