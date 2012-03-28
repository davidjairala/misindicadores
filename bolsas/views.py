from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.simple import direct_to_template
from django.contrib import messages
from django.db.models import Q
from numpy import *
from misindicadores.globals.functions import *
from misindicadores.bolsas.models import *

# Portada
def portada(request):
  return direct_to_template(request, 'bolsas/portada.html', {})

# Latinoamerica
def latinoamerica(request):
  if(request.GET and request.GET['_d'] and request.GET['_m'] and request.GET['_y']):
    fecha = "%s-%s-%s" % (request.GET['_y'], request.GET['_m'], request.GET['_d'])
  else:
    last_bovespa = Bovespa.objects.all().order_by('-fecha')[0]
    fecha = last_bovespa.fecha.strftime("%Y-%m-%d")
  
  bovespas = Bovespa.objects.filter(fecha__lte=fecha).order_by('-fecha')[:30]
  ipsas = Ipsa.objects.filter(fecha__lte=fecha).order_by('-fecha')[:30]
  mervals = Merval.objects.filter(fecha__lte=fecha).order_by('-fecha')[:30]
  bvgs = Bvg.objects.filter(fecha__lte=fecha).order_by('-fecha')[:30]
  igbvls = Igbvl.objects.filter(fecha__lte=fecha).order_by('-fecha')[:30]
  colcaps = Colcap.objects.filter(fecha__lte=fecha).order_by('-fecha')[:30]
  ibcs = Ibc.objects.filter(fecha__lte=fecha).order_by('-fecha')[:30]
  
  if(len(bovespas) > 0):
    cont = 0
    rows = []
    valores_promedios = []
    valores_bovespas = []
    valores_ipsas = []
    valores_mervals = []
    valores_bvgs = []
    valores_igbvls = []
    valores_colcaps = []
    valores_ibcs = []
  
    chart_promedios = []
    chart_bovespas = []
    chart_ipsas = []
    chart_mervals = []
    chart_bvgs = []
    chart_igbvls = []
    chart_colcaps = []
    chart_ibcs = []
    chart_categories = []

    for bovespa in bovespas:
      try:
        # Sacamos promedios
        promedio = (bovespas[cont].valor + ipsas[cont].valor + mervals[cont].valor + bvgs[cont].bvg + igbvls[cont].valor + colcaps[cont].igbc + ibcs[cont].ibc) / 7
      
        cells = {
          'fecha':bovespas[cont].fecha,
          'promedio':promedio,
          'bovespa':bovespas[cont].valor,
          'ipsa':ipsas[cont].valor,
          'merval':mervals[cont].valor,
          'bvg':bvgs[cont].bvg,
          'igbvl':igbvls[cont].valor,
          'colcap':colcaps[cont].igbc,
          'ibc':ibcs[cont].ibc,
        }
        rows.append(cells)
      
        valores_promedios.append(promedio)
        valores_bovespas.append(bovespas[cont].valor)
        valores_ipsas.append(ipsas[cont].valor)
        valores_mervals.append(mervals[cont].valor)
        valores_bvgs.append(bvgs[cont].bvg)
        valores_igbvls.append(igbvls[cont].valor)
        valores_colcaps.append(colcaps[cont].igbc)
        valores_ibcs.append(ibcs[cont].ibc)
      
     
        chart_promedios.append(str("%.2f" % promedio))
        chart_bovespas.append(str(bovespas[cont].valor))
        chart_ipsas.append(str(ipsas[cont].valor))
        chart_mervals.append(str(mervals[cont].valor))
        chart_bvgs.append(str(bvgs[cont].bvg))
        chart_igbvls.append(str(igbvls[cont].valor))
        chart_colcaps.append(str(colcaps[cont].igbc))
        chart_ibcs.append(str(ibcs[cont].ibc))
        chart_categories.append('"' + doDate(bovespas[cont].fecha.strftime("%Y-%m-%d")) + '"')
      except:
        pass
      cont += 1
    
    valores_promedios = get_stats(valores_promedios)
    valores_bovespas = get_stats(valores_bovespas)
    valores_ipsas = get_stats(valores_ipsas)
    valores_mervals = get_stats(valores_mervals)
    valores_bvgs = get_stats(valores_bvgs)
    valores_igbvls = get_stats(valores_igbvls)
    valores_colcaps = get_stats(valores_colcaps)
    valores_ibcs = get_stats(valores_ibcs)
  
    chart_categories.reverse()
    chart_categories = ','.join(chart_categories)
    chart_promedios.reverse()
    chart_promedios = ','.join(chart_promedios)
    chart_bovespas.reverse()
    chart_bovespas = ','.join(chart_bovespas)
    chart_ipsas.reverse()
    chart_ipsas = ','.join(chart_ipsas)
    chart_mervals.reverse()
    chart_mervals = ','.join(chart_mervals)
    chart_bvgs.reverse()
    chart_bvgs = ','.join(chart_bvgs)
    chart_igbvls.reverse()
    chart_igbvls = ','.join(chart_igbvls)
    chart_colcaps.reverse()
    chart_colcaps = ','.join(chart_colcaps)
    chart_ibcs.reverse()
    chart_ibcs = ','.join(chart_ibcs)
  
    return direct_to_template(request, 'bolsas/latinoamerica.html', {
      'chart_title':'Latinoam&eacute;rica',
      'slug':'latinoamerica',
      'fecha':fecha,
      'rows':rows,
      'bovespas':bovespas,
      'ipsas':ipsas,
      'mervals':mervals,
      'bvgs':bvgs,
      'igbvls':igbvls,
      'colcaps':colcaps,
      'ibcs':ibcs,
      'valores_promedios':valores_promedios,
      'valores_bovespas':valores_bovespas,
      'valores_ipsas':valores_ipsas,
      'valores_mervals':valores_mervals,
      'valores_bvgs':valores_bvgs,
      'valores_igbvls':valores_igbvls,
      'valores_colcaps':valores_colcaps,
      'valores_ibcs':valores_ibcs,
      'chart_categories':chart_categories,
      'chart_promedios':chart_promedios,
      'chart_bovespas':chart_bovespas,
      'chart_ipsas':chart_ipsas,
      'chart_mervals':chart_mervals,
      'chart_bvgs':chart_bvgs,
      'chart_igbvls':chart_igbvls,
      'chart_colcaps':chart_colcaps,
      'chart_ibcs':chart_ibcs,
    })
  else:
    messages.add_message(request, messages.ERROR, 'No encontramos valores para la fecha seleccionada.')
    return HttpResponseRedirect("/bolsas/latinoamerica/")

# Nikkei
def nikkei(request):
  if(request.GET and request.GET['_d'] and request.GET['_m'] and request.GET['_y']):
    fecha = "%s-%s-%s" % (request.GET['_y'], request.GET['_m'], request.GET['_d'])
  else:
    last_nikkei = Nikkei.objects.all().order_by('-fecha')[0]
    fecha = last_nikkei.fecha.strftime("%Y-%m-%d")
  
  nikkeis = Nikkei.objects.filter(fecha__lte=fecha).order_by('-fecha')[:30]
  
  if(len(nikkeis) > 0):
    valores = []
    chart_valores = []
    chart_categories = []
    
    for nikkei in nikkeis:
      valores.append(nikkei.cierre)
      chart_valores.append(str(nikkei.cierre))
      chart_categories.append('"' + doDate(nikkei.fecha.strftime("%Y-%m-%d")) + '"')
    
    chart_categories.reverse()
    chart_categories = ','.join(chart_categories)
    chart_valores.reverse()
    chart_valores = ','.join(chart_valores)
    
    valores = get_stats(valores)
    
    return direct_to_template(request, 'bolsas/bolsa.html', {
      'fecha':fecha,
      'tabla_valores':nikkeis,
      'valores':valores,
      'chart_title':'Nikkei 225',
      'chart_source':'Google Finance',
      'chart_categories':chart_categories,
      'chart_valores':chart_valores,
      'slug':'nikkei'
    })
  else:
    messages.add_message(request, messages.ERROR, 'No encontramos valores para la fecha seleccionada.')
    return HttpResponseRedirect("/bolsas/nikkei/")

# S&P 500
def sp500(request):
  if(request.GET and request.GET['_d'] and request.GET['_m'] and request.GET['_y']):
    fecha = "%s-%s-%s" % (request.GET['_y'], request.GET['_m'], request.GET['_d'])
  else:
    last_sp500 = Sp500.objects.all().order_by('-fecha')[0]
    fecha = last_sp500.fecha.strftime("%Y-%m-%d")
  
  sp500s = Sp500.objects.filter(fecha__lte=fecha).order_by('-fecha')[:30]
  
  if(len(sp500s) > 0):
    valores = []
    chart_valores = []
    chart_categories = []
    
    for sp500 in sp500s:
      valores.append(sp500.cierre)
      chart_valores.append(str(sp500.cierre))
      chart_categories.append('"' + doDate(sp500.fecha.strftime("%Y-%m-%d")) + '"')
    
    chart_categories.reverse()
    chart_categories = ','.join(chart_categories)
    chart_valores.reverse()
    chart_valores = ','.join(chart_valores)
    
    valores = get_stats(valores)
    
    return direct_to_template(request, 'bolsas/bolsa.html', {
      'fecha':fecha,
      'sp500s':sp500s,
      'tabla_valores':sp500s,
      'valores':valores,
      'chart_title':'S&amp;P 500',
      'chart_source':'Google Finance',
      'chart_categories':chart_categories,
      'chart_valores':chart_valores,
      'slug':'sp500'
    })
  else:
    messages.add_message(request, messages.ERROR, 'No encontramos valores para la fecha seleccionada.')
    return HttpResponseRedirect("/bolsas/sp500/")

# NASDAQ
def nasdaq(request):
  if(request.GET and request.GET['_d'] and request.GET['_m'] and request.GET['_y']):
    fecha = "%s-%s-%s" % (request.GET['_y'], request.GET['_m'], request.GET['_d'])
  else:
    last_nasdaq = Nasdaq.objects.all().order_by('-fecha')[0]
    fecha = last_nasdaq.fecha.strftime("%Y-%m-%d")
  
  nasdaqs = Nasdaq.objects.filter(fecha__lte=fecha).order_by('-fecha')[:30]
  
  if(len(nasdaqs) > 0):
    valores = []
    chart_valores = []
    chart_categories = []
    
    for nasdaq in nasdaqs:
      valores.append(nasdaq.cierre)
      chart_valores.append(str(nasdaq.cierre))
      chart_categories.append('"' + doDate(nasdaq.fecha.strftime("%Y-%m-%d")) + '"')
    
    chart_categories.reverse()
    chart_categories = ','.join(chart_categories)
    chart_valores.reverse()
    chart_valores = ','.join(chart_valores)
    
    valores = get_stats(valores)
    
    return direct_to_template(request, 'bolsas/bolsa.html', {
      'fecha':fecha,
      'nasdaqs':nasdaqs,
      'tabla_valores':nasdaqs,
      'valores':valores,
      'chart_title':'NASDAQ',
      'chart_source':'Google Finance',
      'chart_categories':chart_categories,
      'chart_valores':chart_valores,
      'slug':'nasdaq'
    })
  else:
    messages.add_message(request, messages.ERROR, 'No encontramos valores para la fecha seleccionada.')
    return HttpResponseRedirect("/bolsas/nasdaq/")

# Grafica del dow jones
def img_dow(request):
  from django.conf import settings
  from django.core.cache import cache
  import cStringIO
  import matplotlib
  matplotlib.use('Agg')
  import matplotlib.pyplot as plt
  import matplotlib.ticker as ticker
  import matplotlib as mpl
  
  mpl.rcParams['axes.titlesize'] = '8'
  
  img_name = 'img_dow'
  
  # Checamos si hay cache
  ic = cache.get(img_name)
  
  if(ic):
    response = HttpResponse(ic, mimetype='image/png')
  else:
    output = cStringIO.StringIO()
    
    dows = Dow.objects.all().order_by('-id')[:30]
    
    valores = []
    fechas = []
    
    cont = 0
    
    for dow in dows:
      valores.append(dow.valor)
      
      if(cont == 0 or cont == len(dows) - 1):
        fechas.append(doDate(dow.fecha))
      else:
        fechas.append('')
      
      cont += 1
    
    valores.reverse()
    fechas.reverse()

    plot = plt.figure(figsize=[4.5,1.5], dpi=100)
    ax = plot.add_subplot(111)
    plt.title('Dow Jones')
    plt.plot(valores)
    
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

# Dow Jones
def dow(request):
  if(request.GET and request.GET['_d'] and request.GET['_m'] and request.GET['_y']):
    fecha = "%s-%s-%s" % (request.GET['_y'], request.GET['_m'], request.GET['_d'])
  else:
    last_dow = Dow.objects.all().order_by('-fecha')[0]
    fecha = last_dow.fecha.strftime("%Y-%m-%d")
  
  dows = Dow.objects.filter(fecha__lte=fecha).order_by('-fecha')[:30]
  
  if(len(dows) > 0):
    valores = []
    chart_valores = []
    chart_categories = []
    
    for dow in dows:
      valores.append(dow.cierre)
      chart_valores.append(str(dow.cierre))
      chart_categories.append('"' + doDate(dow.fecha.strftime("%Y-%m-%d")) + '"')
    
    chart_categories.reverse()
    chart_categories = ','.join(chart_categories)
    chart_valores.reverse()
    chart_valores = ','.join(chart_valores)
    
    valores = get_stats(valores)
    
    return direct_to_template(request, 'bolsas/bolsa.html', {
      'fecha':fecha,
      'dows':dows,
      'tabla_valores':dows,
      'tabla_show_volumen':True,
      'valores':valores,
      'chart_title':'Dow Jones',
      'chart_source':'Google Finance',
      'chart_categories':chart_categories,
      'chart_valores':chart_valores,
      'slug':'dow'
    })
  else:
    messages.add_message(request, messages.ERROR, 'No encontramos valores para la fecha seleccionada.')
    return HttpResponseRedirect("/bolsas/dow/")

# Cron bolsas de otros paises
def cron_paises_bolsas(request):
  from datetime import date
  import urllib2
  from BeautifulSoup import BeautifulSoup
  import re
  
  # San Paolo, Santiago de Chile, Buenos Aires
  
  url = 'http://mx.finance.yahoo.com/intlindices?e=americas'
  f = urllib2.urlopen(url).read()
  soup = BeautifulSoup(f)
  
  cont = 0
  fecha = date.today()
  bovespa = 0
  ipsa = 0
  merval = 0
  
  for td in soup.findAll('td'):
    try:
      content = clean_string(td.find('b').contents[0]).replace(',', '')
    except:
      try:
        content = clean_string(td.contents[0]).replace(',', '')
      except:
        content = ""
    
    if(cont == 4):
      bovespa = float(content)
    elif(cont == 14):
      ipsa = float(content)
    elif(cont == 19):
      merval = float(content)
    
    cont += 1
  
  if(bovespa != 0):
    # Checamos si existe
    try:
      n_bovespa = Bovespa.objects.filter(fecha=fecha)[0]
    except:
      n_bovespa = Bovespa()
    n_bovespa.valor = bovespa
    n_bovespa.save()
  
  if(ipsa != 0):
    # Checamos si existe
    try:
      n_ipsa = Ipsa.objects.filter(fecha=fecha)[0]
    except:
      n_ipsa = Ipsa()
    n_ipsa.valor = ipsa
    n_ipsa.save()

  if(merval != 0):
    # Checamos si existe
    try:
      n_merval = Merval.objects.filter(fecha=fecha)[0]
    except:
      n_merval = Merval()
    n_merval.valor = merval
    n_merval.save()

  # Guayaquil, Peru
  
  url = 'http://www.mundobvg.com/bvgsite/indicesbvg.asp'
  f = urllib2.urlopen(url).read()
  soup = BeautifulSoup(f)
  
  cont = 0
  bvg = 0
  ipecu = 0
  igbvl = 0

  for td in soup.findAll('td'):
    try:
      content = clean_string(td.find('font').contents[0]).replace(',', '')
    except:
      try:
        content = clean_string(td.contents[0]).replace(',', '')
      except:
        content = ""

    if(cont == 7):
      bvg = float(content)
    elif(cont == 12):
      ipecu = float(content)
    elif(cont == 22):
      igbvl = float(content)
    
    cont += 1
  
  if(bvg != 0 and ipecu != 0):
    # Checamos si existe
    try:
      n_bvg = Bvg.objects.filter(fecha=fecha)[0]
    except:
      n_bvg = Bvg()
    n_bvg.bvg = bvg
    n_bvg.ipecu = ipecu
    n_bvg.save()

  if(igbvl != 0):
    # Checamos si existe
    try:
      n_igbvl = Igbvl.objects.filter(fecha=fecha)[0]
    except:
      n_igbvl = Igbvl()
    n_igbvl.valor = igbvl
    n_igbvl.save()

  # Colombia

  url = 'http://www.bvc.com.co/pps/tibco/portalbvc'
  f = urllib2.urlopen(url).read()
  f_arr = f.split('<div class="contenedor_tabla">')
  f = f_arr[1]
  soup = BeautifulSoup(f)
  
  cont = 0
  colcap = 0
  col20 = 0
  igbc = 0

  for td in soup.findAll('td', id="textoValorHoyIndice0"):
    try:
      content = clean_string(td.contents[0]).replace(',', '')
    except:
      content = ""

    if(content != ""):
      colcap = float(content)
    
    cont += 1

  for td in soup.findAll('td', id="textoValorHoyIndice1"):
    try:
      content = clean_string(td.contents[0]).replace(',', '')
    except:
      content = ""

    if(content != ""):
      col20 = float(content)
    
    cont += 1

  for td in soup.findAll('td', id="textoValorHoyIndice2"):
    try:
      content = clean_string(td.contents[0]).replace(',', '')
    except:
      content = ""

    if(content != ""):
      igbc = float(content)
    
    cont += 1
  
  if(colcap != 0 and col20 != 0 and igbc != 0):
    # Checamos si existe
    try:
      n_colcap = Colcap.objects.filter(fecha=fecha)[0]
    except:
      n_colcap = Colcap()
    n_colcap.colcap = colcap
    n_colcap.col20 = col20
    n_colcap.igbc = igbc
    n_colcap.save()

  # Caracas

  url = 'http://www.caracasstock.com/esp/textos/indices.jsp'
  f = urllib2.urlopen(url).read()
  soup = BeautifulSoup(f)
  
  cont = 0
  ibc = 0

  for td in soup.findAll('td', {'class':'tex-graficosSmall'}):
    try:
      content = clean_string(td.contents[0]).replace('.', '').replace(',', '.')
    except:
      content = ""

    if(cont == 0):
      ibc = float(content)
    
    cont += 1
  
  if(ibc != 0):
    # Checamos si existe
    try:
      n_ibc = Ibc.objects.filter(fecha=fecha)[0]
    except:
      n_ibc = Ibc()
    n_ibc.ibc = ibc
    n_ibc.save()
  
  return direct_to_template(request, 'ajax.html', {'out':'done'})

# Cron Bolsas
def cron_bolsas(request):
  import urllib2
  from BeautifulSoup import BeautifulSoup
  import re
  
  # Dow Jones
  
  url = 'http://www.google.com/finance/historical?q=INDEXDJX:.DJI'
  f = urllib2.urlopen(url).read()
  soup = BeautifulSoup(f)
  
  cont = 0
  fecha = ""
  valor = 0
  alto = 0
  bajo = 0
  cierre = 0
  volumen = 0
  
  for td in soup.findAll('td'):
    try:
      content = clean_string(td.contents[0]).replace(',', '')
    except:
      content = ""
    
    cont += 1
    
    if(cont == 13):
      fecha = content
    elif(cont == 14):
      valor = float(content)
    elif(cont == 15):
      alto = float(content)
    elif(cont == 16):
      bajo = float(content)
    elif(cont == 17):
      cierre = float(content)
    elif(cont == 18):
      volumen = float(content)
      break
  
  if(fecha != "" and valor != 0 and alto != 0 and bajo != 0 and cierre != 0):
    # Parseamos fecha
    farr = fecha.split(' ')
    
    day = farr[1]
    
    if(int(day) < 10):
      day = "0%s" % day
    
    year = farr[2]
    month = farr[0]
    
    month = getMesNum(month, True, True)
    month = month
    
    if(int(month) < 10):
      month = "0%s" % month
    
    fecha = "%s-%s-%s" % (year, month, day)
    
    # Checamos si existe
    try:
      dow = Dow.objects.filter(fecha=fecha)[0]
    except:
      dow = Dow()
    
    dow.fecha = fecha
    dow.valor = valor
    dow.alto = alto
    dow.bajo = bajo
    dow.cierre = cierre
    dow.volumen = volumen
    dow.save()
  
  # NASDAQ
  
  url = 'http://www.google.com/finance/historical?q=INDEXNASDAQ:.IXIC'
  f = urllib2.urlopen(url).read()
  soup = BeautifulSoup(f)
  
  cont = 0
  fecha = ""
  valor = 0
  alto = 0
  bajo = 0
  cierre = 0
  
  for td in soup.findAll('td'):
    try:
      content = clean_string(td.contents[0]).replace(',', '')
    except:
      content = ""
    
    cont += 1
    
    if(cont == 13):
      fecha = content
    elif(cont == 14):
      valor = float(content)
    elif(cont == 15):
      alto = float(content)
    elif(cont == 16):
      bajo = float(content)
    elif(cont == 17):
      cierre = float(content)
      break
  
  if(fecha != "" and valor != 0 and alto != 0 and bajo != 0 and cierre != 0):
    # Parseamos fecha
    farr = fecha.split(' ')
    
    day = farr[1]
    
    if(int(day) < 10):
      day = "0%s" % day
    
    year = farr[2]
    month = farr[0]
    
    month = getMesNum(month, True, True)
    month = month
    
    if(int(month) < 10):
      month = "0%s" % month
    
    fecha = "%s-%s-%s" % (year, month, day)
    
    # Checamos si existe
    try:
      nasdaq = Nasdaq.objects.filter(fecha=fecha)[0]
    except:
      nasdaq = Nasdaq()
    
    nasdaq.fecha = fecha
    nasdaq.valor = valor
    nasdaq.alto = alto
    nasdaq.bajo = bajo
    nasdaq.cierre = cierre
    nasdaq.save()
  
  # S&P 500
  
  url = 'http://www.google.com/finance/historical?q=INDEXSP:.INX'
  f = urllib2.urlopen(url).read()
  soup = BeautifulSoup(f)
  
  cont = 0
  fecha = ""
  valor = 0
  alto = 0
  bajo = 0
  cierre = 0
  
  for td in soup.findAll('td'):
    try:
      content = clean_string(td.contents[0]).replace(',', '')
    except:
      content = ""
    
    cont += 1
    
    if(cont == 13):
      fecha = content
    elif(cont == 14):
      valor = float(content)
    elif(cont == 15):
      alto = float(content)
    elif(cont == 16):
      bajo = float(content)
    elif(cont == 17):
      cierre = float(content)
      break
  
  if(fecha != "" and valor != 0 and alto != 0 and bajo != 0 and cierre != 0):
    # Parseamos fecha
    farr = fecha.split(' ')
    
    day = farr[1]
    
    if(int(day) < 10):
      day = "0%s" % day
    
    year = farr[2]
    month = farr[0]
    
    month = getMesNum(month, True, True)
    month = month
    
    if(int(month) < 10):
      month = "0%s" % month
    
    fecha = "%s-%s-%s" % (year, month, day)
    
    # Checamos si existe
    try:
      sp500 = Sp500.objects.filter(fecha=fecha)[0]
    except:
      sp500 = Sp500()
    
    sp500.fecha = fecha
    sp500.valor = valor
    sp500.alto = alto
    sp500.bajo = bajo
    sp500.cierre = cierre
    sp500.save()
  
  # Nikkei
  
  url = 'http://www.google.com/finance/historical?q=INDEXNIKKEI:.N225'
  f = urllib2.urlopen(url).read()
  soup = BeautifulSoup(f)
  
  cont = 0
  fecha = ""
  valor = 0
  alto = 0
  bajo = 0
  cierre = 0
  
  for td in soup.findAll('td'):
    try:
      content = clean_string(td.contents[0]).replace(',', '')
    except:
      content = ""
    
    cont += 1
    
    if(cont == 13):
      fecha = content
    elif(cont == 14):
      valor = float(content)
    elif(cont == 15):
      alto = float(content)
    elif(cont == 16):
      bajo = float(content)
    elif(cont == 17):
      cierre = float(content)
      break
  
  if(fecha != "" and valor != 0 and alto != 0 and bajo != 0 and cierre != 0):
    # Parseamos fecha
    farr = fecha.split(' ')
    
    day = farr[1]
    
    if(int(day) < 10):
      day = "0%s" % day
    
    year = farr[2]
    month = farr[0]
    
    month = getMesNum(month, True, True)
    month = month
    
    if(int(month) < 10):
      month = "0%s" % month
    
    fecha = "%s-%s-%s" % (year, month, day)
    
    # Checamos si existe
    try:
      nikkei = Nikkei.objects.filter(fecha=fecha)[0]
    except:
      nikkei = Nikkei()
    
    nikkei.fecha = fecha
    nikkei.valor = valor
    nikkei.alto = alto
    nikkei.bajo = bajo
    nikkei.cierre = cierre
    nikkei.save()
  
  return direct_to_template(request, 'ajax.html', {'out':'done'})

# Buscar emisora
def buscar_emisora(request):
  if(request.GET and request.GET['emisora']):
    emisora = request.GET['emisora']
  else:
    emisora = None
  
  not_found = False
  
  if(emisora):
    emisora_s = emisora.upper().replace('&', '&amp;')
  
    try:
      bmv = BmvDia.objects.filter(emisora__icontains=emisora_s).order_by('-id')[0]
    
      return HttpResponseRedirect(bmv.get_link().replace('&amp;', '&'))
    except:
      not_found = True
  
  if(not_found):
    messages.add_message(request, messages.ERROR, 'No encontramos la emisora.')
    return HttpResponseRedirect('/bolsas/bmv/')

# BMV - Emisora
def bmv_emisora(request, emisora, rango = None):
  emisora_s = emisora.upper().replace('&', '&amp;')
  
  if(not rango or rango == "" or rango == "dia"):
    rango = "dia"
    rango_title = "D&iacute;a"
  elif(rango == "semana"):
    rango_title = "Semana"
  elif(rango == "mes"):
    rango_title = "Mes"
  elif(rango == "3meses"):
    rango_title = "3 Meses"
  else:
    rango_title = "6 Meses"
  
  if(request.GET and request.GET['_d'] and request.GET['_m'] and request.GET['_y']):
    fecha = "%s-%s-%s" % (request.GET['_y'], request.GET['_m'], request.GET['_d'])
  else:
    if(rango == "dia"):
      last_bmv = Bmv.objects.filter(emisora=emisora_s).order_by('-fecha')[0]
    else:
      last_bmv = BmvDia.objects.filter(emisora=emisora_s).order_by('-fecha')[0]
    fecha = last_bmv.fecha.strftime("%Y-%m-%d")
  
  if(rango == "dia"):
    curr_bmv = Bmv.objects.filter(emisora=emisora_s).order_by('-fecha')[0]
    bmvs = Bmv.objects.filter(emisora=emisora_s, fecha=fecha).order_by('-id')
  else:
    if(rango == "semana"):
      limite = 7
    elif(rango == "mes"):
      limite = 31
    elif(rango == "3meses"):
      limite = 90
    else:
      limite = 180
    curr_bmv = BmvDia.objects.filter(emisora=emisora_s).order_by('-fecha')[0]
    bmvs = BmvDia.objects.filter(emisora=emisora_s, fecha__lte=fecha).order_by('-id')[:limite]
  
  valores = []
  chart_categories = []
  chart_valores = []
  
  if(len(bmvs) > 0):
    cont = 0
    
    for bmv in bmvs:
      valores.append(bmv.ultimo)
      chart_valores.append(str(bmv.ultimo))
      
      if(rango == "dia"):
        chart_categories.append('"' + bmv.hora + '"')
      else:
        if(rango == "3meses" or rango == "6meses"):
          if(rango == "3meses"):
            lr = 4
          else:
            lr= 8
          
          if(cont % lr == 0):
            chart_categories.append('"' + doDate(bmv.fecha.strftime("%Y-%m-%d")) + '"')
          else:
            chart_categories.append('"-"')
        else:
          chart_categories.append('"' + doDate(bmv.fecha.strftime("%Y-%m-%d")) + '"')
      
      cont += 1
    
    valores = get_stats(valores)
    
    chart_categories.reverse()
    chart_categories = ','.join(chart_categories)
    chart_valores.reverse()
    chart_valores = ','.join(chart_valores)
    
    return direct_to_template(request, 'bolsas/emisora.html', {
      'fecha':fecha,
      'emisora':emisora,
      'curr_bmv':curr_bmv,
      'bmvs':bmvs,
      'valores':valores,
      'rango':rango,
      'rango_title':rango_title,
      'chart_title':"%s - %s" % (bmv.emisora, rango_title),
      'chart_source':'Fuente: Bolsa Mexicana de Valores',
      'chart_categories':chart_categories,
      'chart_valores':chart_valores
    })
  else:
    messages.add_message(request, messages.ERROR, 'No encontramos valores para la fecha seleccionada.')
    return HttpResponseRedirect("/bolsas/bmv/emisora/%s/" % emisora)

# Grafica del bmv ipc
def img_bmv_ipc(request):
  from django.conf import settings
  from django.core.cache import cache
  import cStringIO
  import matplotlib
  matplotlib.use('Agg')
  import matplotlib.pyplot as plt
  import matplotlib.ticker as ticker
  import matplotlib as mpl
  
  mpl.rcParams['axes.titlesize'] = '8'
  
  img_name = 'img_bmv_ipc'
  
  # Checamos si hay cache
  ic = cache.get(img_name)
  
  if(ic):
    response = HttpResponse(ic, mimetype='image/png')
  else:
    output = cStringIO.StringIO()
    
    last_bmv = BmvIpc.objects.all().order_by('-fecha')[0]
    bmvs = BmvIpc.objects.filter(fecha=last_bmv.fecha).order_by('id')
    
    valores = []
    fechas = []
    
    cont = 0
    
    for bmv in bmvs:
      valores.append(bmv.valor)
      
      if(cont == 0 or cont == len(bmvs) - 1):
        fechas.append(bmv.hora)
      else:
        fechas.append('')
      
      cont += 1
    
    plot = plt.figure(figsize=[4.5,1.5], dpi=100)
    ax = plot.add_subplot(111)
    plt.title('BMV - IPC')
    plt.plot(valores)
    
    xAxis = plt.axes().xaxis
    xAxis.set_major_locator(ticker.FixedLocator([i for i in range(0,len(bmvs))]))
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

# BMV - IPC
def bmv_ipc(request, rango = "dia"):
  if(rango == "dia"):
    rango_title = "D&iacute;a"
  elif(rango == "semana"):
    rango_title = "Semana"
    limite = 7
  elif(rango == "mes"):
    rango_title = "Mes"
    limite = 30
  elif(rango == "3meses"):
    rango_title = "3 meses"
    limite = 90
  elif(rango == "6meses"):
    rango_title = "6 meses"
    limite = 180
  
  if(request.GET and request.GET['_d'] and request.GET['_m'] and request.GET['_y']):
    fecha = "%s-%s-%s" % (request.GET['_y'], request.GET['_m'], request.GET['_d'])
  else:
    if(rango == "dia"):
      last_bmv = BmvIpc.objects.all().order_by('-fecha')[0]
    else:
      last_bmv = BmvIpcDia.objects.all().order_by('-fecha')[0]
    fecha = last_bmv.fecha.strftime("%Y-%m-%d")
  
  bmvs = BmvIpc.objects.filter(fecha=fecha).order_by('-id')
  
  # Checamos si encontramos bmvs para la fecha, sino agarramos de la siguiente fecha anterior
  if(len(bmvs) > 0):
    if(rango == "dia"):
      last_bmv = BmvIpc.objects.all().order_by('-fecha')[0]
    else:
      last_bmv = BmvIpcDia.objects.all().order_by('-fecha')[0]
    fecha = last_bmv.fecha.strftime("%Y-%m-%d")
    
    if(rango == "dia"):
      bmvs = BmvIpc.objects.filter(fecha=fecha).order_by('-id')
    else:
      bmvs = BmvIpcDia.objects.filter(fecha__lte=fecha).order_by('-fecha')[:limite]
  
  if(len(bmvs) > 0):
    valores = []
    arr_valores = []
    chart_categories = []
    chart_valores = []
    
    cont = 0
    
    for bmv in bmvs:
      arr_valores.append(bmv.valor)
      valores.append(bmv.valor)
      chart_valores.append(str(bmv.valor))
      
      if(rango == "3meses" or rango == "6meses"):
          if(rango == "3meses"):
            lr = 4
          else:
            lr= 8
          
          if(cont % lr == 0):
            chart_categories.append('"' + doDate(bmv.fecha.strftime("%Y-%m-%d")) + '"')
          else:
            chart_categories.append('"-"')
      else:
        if(rango == "dia"):
          chart_categories.append('"' + bmv.hora + '"')
        else:
          chart_categories.append('"' + doDate(bmv.fecha.strftime("%Y-%m-%d")) + '"')
      
      cont += 1
    
    chart_categories.reverse()
    chart_categories = ','.join(chart_categories)
    chart_valores.reverse()
    chart_valores = ','.join(chart_valores)
    
    valores = get_stats(valores)
    
    return direct_to_template(request, 'bolsas/bmv_ipc.html', {
      'fecha':fecha,
      'bmvs':bmvs,
      'arr_valores':bmvs,
      'valores_show_hora':True,
      'valores':valores,
      'rango_title':rango_title,
      'rango':rango,
      'chart_title':"BMV - IPC - %s" % rango_title,
      'chart_source':'Fuente: Bolsa Mexicana de Valores',
      'chart_categories':chart_categories,
      'chart_valores':chart_valores
    })
  else:
    messages.add_message(request, messages.ERROR, 'No encontramos valores para la fecha seleccionada.')
    return HttpResponseRedirect("/bolsas/bmv/")

# BMV
def bmv(request):
  if(request.GET and request.GET['_d'] and request.GET['_m'] and request.GET['_y']):
    fecha = "%s-%s-%s" % (request.GET['_y'], request.GET['_m'], request.GET['_d'])
  else:
    last_bmv = BmvDia.objects.all().order_by('-fecha')[0]
    fecha = last_bmv.fecha.strftime("%Y-%m-%d")
  
  bmvs = BmvDia.objects.filter(fecha=fecha).order_by('emisora')
  
  try:
    bmv_ipc = BmvIpcDia.objects.filter(fecha__lte=fecha).order_by('-fecha')[0]
  except:
    messages.add_message(request, messages.ERROR, 'No encontramos valores del IPC para la fecha seleccionada.')
    return HttpResponseRedirect("/bolsas/bmv/")
  
  if(len(bmvs) > 0):
    return direct_to_template(request, 'bolsas/bmv.html', {
      'fecha':fecha,
      'bmvs':bmvs,
      'bmv_ipc':bmv_ipc,
      'small_table':True
    })
  else:
    messages.add_message(request, messages.ERROR, 'No encontramos valores para la fecha seleccionada.')
    return HttpResponseRedirect("/bolsas/bmv/")

# Cron BMV desde version PHP
def cron_bmv(request):
  from datetime import date
  import urllib2
  from BeautifulSoup import BeautifulSoup
  import re
  
  url = 'http://misindicadores.kebum.com/?m=bmv&c=api_bmv'
  f = urllib2.urlopen(url).read()
  
  f_arr = f.split('|START|')
  ipc = f_arr[0]
  emisoras = f_arr[1]
  
  # Sacamos IPC
  ipc_parts = ipc.split('|')
  
  fecha = ipc_parts[0]
  hora = ipc_parts[1]
  valor = float(ipc_parts[2])
  
  # Checamos si ya existe
  try:
    bmv_alr = BmvIpc.objects.filter(fecha=fecha, hora=hora).order_by('-id')[0]
  except:
    bmv_alr = False
  
  # Ultimo agregaddo
  try:
    bmv_last = BmvIpc.objects.all().order_by('-id')[0]
  except:
    bmv_last = False
  
  if(not bmv_alr and (not bmv_last or bmv_last.hora != hora)):
    new_bmv_ipc = BmvIpc(hora=hora, valor=valor, fecha=fecha)
    new_bmv_ipc.save()
  
  # Ahora para valor del dia
  try:
    bmv_alr = BmvIpcDia.objects.filter(fecha=fecha).order_by('-id')[0]
  except:
    bmv_alr = False
  
  if(not bmv_alr):
    bmv_alr = BmvIpcDia(valor=valor, fecha=fecha, hora=hora)
  else:
    bmv_alr.valor = valor
    bmv_alr.hora = hora
  
  bmv_alr.save()
  
  # Agregamos emisoras
  emisoras = emisoras.split('\n')
  
  for c_emisora in emisoras:
    if(c_emisora != ''):
      parts = c_emisora.split('|')
      
      emisora = parts[0]
      serie = parts[1]
      fecha = parts[2]
      hora = parts[3]
      ultimo = parts[4]
      ppp = parts[5]
      anterior = parts[6]
      maximo = parts[7]
      minimo = parts[8]
      volumen = parts[9]
      importe = parts[10]
      ops = parts[11]
      puntos = parts[12]
      porcentaje = parts[13]
      tendencia = parts[14]
      tendencia_relativa = parts[15]
      tendencia_relativa_acumulada = parts[16]
      cambio_promedio = parts[17]
      prediccion_lineal = parts[18]
      error_promedio = parts[19]
      
      # Checamos si ya existe
      try:
        alr_bmv = Bmv.objects.filter(emisora=emisora, serie=serie, fecha=fecha, hora=hora).order_by('-id')[0]
      except:
        new_bmv = Bmv(
          emisora=emisora,
          serie=serie,
          fecha=fecha,
          hora=hora,
          ultimo=ultimo,
          ppp=ppp,
          anterior=anterior,
          maximo=maximo,
          minimo=minimo,
          volumen=volumen,
          importe=importe,
          ops=ops,
          puntos=puntos,
          porcentaje=porcentaje,
          tendencia=tendencia,
          tendencia_relativa=tendencia_relativa,
          tendencia_relativa_acumulada=tendencia_relativa_acumulada,
          cambio_promedio=cambio_promedio,
          prediccion_lineal=prediccion_lineal,
          error_promedio=error_promedio
        )
        new_bmv.save()
      
        # Agregamos a tabla del dia
        try:
          bmv_dia = BmvDia.objects.filter(emisora=emisora, serie=serie, fecha=fecha).order_by('-id')[0]
        except:
          bmv_dia = BmvDia()

        bmv_dia.emisora = emisora
        bmv_dia.serie = serie
        bmv_dia.fecha = fecha
        bmv_dia.hora = hora
        bmv_dia.ultimo = ultimo
        bmv_dia.ppp = ppp
        bmv_dia.anterior = anterior
        bmv_dia.maximo = maximo
        bmv_dia.minimo = minimo
        bmv_dia.volumen = volumen
        bmv_dia.importe = importe
        bmv_dia.ops = ops
        bmv_dia.puntos = puntos
        bmv_dia.porcentaje = porcentaje
        bmv_dia.tendencia = new_bmv.tendencia
        bmv_dia.tendencia_relativa = new_bmv.tendencia_relativa
        bmv_dia.tendencia_relativa_acumulada = new_bmv.tendencia_relativa_acumulada
        bmv_dia.cambio_promedio = new_bmv.cambio_promedio
        bmv_dia.prediccion_lineal = new_bmv.prediccion_lineal
        bmv_dia.error_promedio = new_bmv.error_promedio
        bmv_dia.save()
  
  return direct_to_template(request, 'ajax.html', {'out':'done'})

# Cron BMV viejo
def cron_bmv_old(request):
  from datetime import date
  import urllib2
  from BeautifulSoup import BeautifulSoup
  import re
  
  # Emisoras
  
  fecha = date.today().strftime("%Y-%m-%d")
  fecha_org = fecha
  
  try:
    url = 'http://www.bmv.com.mx/img-bmv/series.html'
    f = urllib2.urlopen(url).read()
  
    farr = f.split('<html>')
    f = farr[2]
    farr = f.split('</html>')
    f = "<html>%s</html>" % farr[0]
  
    soup = BeautifulSoup(f)
  
    for tr in soup.findAll('tr', {'class':re.compile("Tabla1_Renglon_Oscuro|Tabla1_Renglon_Claro")}):
      tds = tr.findAll('td')
    
      emisora = clean_string(tds[0].find('a').contents[0])
      serie = clean_string(tds[1].contents[0])
      hora = clean_string(tds[2].contents[0])
    
      try:
        ultimo = float(clean_string(tds[3].contents[0].replace(',', '')))
      except:
        ultimo = float(clean_string(tds[3].find('span').contents[0].replace(',', '')))
      try:
        ppp = float(clean_string(tds[4].contents[0].replace(',', '')))
      except:
        ppp = 0
      anterior = float(clean_string(tds[5].contents[0].replace(',', '')))
      maximo = float(clean_string(tds[6].contents[0].replace(',', '')))
      minimo = float(clean_string(tds[7].contents[0].replace(',', '')))
      volumen = float(clean_string(tds[8].contents[0].replace(',', '')))
      importe = float(clean_string(tds[9].contents[0].replace(',', '')))
      ops = float(clean_string(tds[10].contents[0].replace(',', '')))
      puntos = float(clean_string(tds[11].contents[0].replace(',', '')))
      porcentaje = float(clean_string(tds[12].contents[0].replace(',', '')))
    
      if(emisora != ""):
        # Checamos caso especial, la hora es 3:00 y es la primera del dia -> pertenece al dia anterior
        if(hora == '03:00'):
          try:
            dia_bmv = Bmv.objects.filter(emisora=emisora, serie=serie, fecha=fecha).order_by('-id')[0]
          except:
            # Si es la primera del dia, la metemos para la ultima fecha
            try:
              bmv_last = Bmv.objects.filter(emisora=emisora, serie=serie).order_by('-id')[0]
              fecha = bmv_last.fecha.strftime("%Y-%m-%d")
            except:
              pass
      
        # Checamos si ya existe
        not_alr_bmv = False
        try:
          alr_bmv = Bmv.objects.filter(emisora=emisora, serie=serie, fecha=fecha, hora=hora).order_by('-id')[0]
        except:
          not_alr_bmv = True
      
        # Checamos tambien si es igual al ultimo introducido (repetido del dia anterior, no queremos)
        not_alr_last_bmv = False
        try:
          alr_last_bmv = Bmv.objects.filter(emisora=emisora, serie=serie, hora=hora).order_by('-id')[0]
        except:
          not_alr_last_bmv = True
      
        if(not_alr_bmv and (not_alr_last_bmv or (alr_last_bmv.fecha.strftime("%Y-%m-%d") != fecha and alr_last_bmv.hora != hora))):
          new_bmv = Bmv(emisora=emisora, serie=serie, fecha=fecha, hora=hora, ultimo=ultimo, ppp=ppp, anterior=anterior, maximo=maximo, minimo=minimo, volumen=volumen, importe=importe, ops=ops, puntos=puntos, porcentaje=porcentaje, tendencia=0, tendencia_relativa=0, tendencia_relativa_acumulada=0, cambio_promedio=0, prediccion_lineal=0, error_promedio=0)
          new_bmv.save()
        
          # Ahora checamos si hay alguno anterior para determinar tendencia y prediccion
          try:
            anterior_bmv = Bmv.objects.filter(emisora=emisora, serie=serie).order_by('-id')
            anterior_bmv = anterior_bmv.filter(~Q(id=new_bmv.id)).order_by('-id')[0]
          
            if(new_bmv.ultimo > anterior_bmv.ultimo):
              tendencia = 1
            elif(new_bmv.ultimo < anterior_bmv.ultimo):
              tendencia = -1
            else:
              tendencia = 0
          
            tendencia_relativa = new_bmv.ultimo - anterior_bmv.ultimo
          
            if(anterior_bmv.tendencia_relativa_acumulada and anterior_bmv.tendencia_relativa_acumulada != 0):
              tendencia_relativa_acumulada = tendencia_relativa + anterior_bmv.tendencia_relativa_acumulada
            else:
              tendencia_relativa_acumulada = tendencia_relativa + anterior_bmv.tendencia_relativa
          
            cambio_promedio = ((new_bmv.ultimo - anterior_bmv.ultimo) + anterior_bmv.cambio_promedio.to_f) / 2
          
            prediccion_lineal = new_bmv.ultimo + cambio_promedio
          
            if(anterior_bmv.prediccion_lineal and anterior_bmv.prediccion_lineal != 0):
              error_promedio = new_bmv.ultimo - anterior_bmv.prediccion_lineal
            else:
              error_promedio = 0
          
              # Actualizamos con datos
              new_bmv.tendencia = tendencia
              new_bmv.tendencia_relativa = tendencia_relativa
              new_bmv.cambio_promedio = cambio_promedio
              new_bmv.prediccion_lineal = prediccion_lineal
              new_bmv.error_promedio = error_promedio
              new_bmv.save()
          except:
            pass
        
          # Agregamos a tabla del dia
          try:
            bmv_dia = BmvDia.objects.filter(emisora=emisora, serie=serie, fecha=fecha).order_by('-id')[0]
          except:
            bmv_dia = BmvDia()

          bmv_dia.emisora = emisora
          bmv_dia.serie = serie
          bmv_dia.fecha = fecha
          bmv_dia.hora = hora
          bmv_dia.ultimo = ultimo
          bmv_dia.ppp = ppp
          bmv_dia.anterior = anterior
          bmv_dia.maximo = maximo
          bmv_dia.minimo = minimo
          bmv_dia.volumen = volumen
          bmv_dia.importe = importe
          bmv_dia.ops = ops
          bmv_dia.puntos = puntos
          bmv_dia.porcentaje = porcentaje
          bmv_dia.tendencia = new_bmv.tendencia
          bmv_dia.tendencia_relativa = new_bmv.tendencia_relativa
          bmv_dia.tendencia_relativa_acumulada = new_bmv.tendencia_relativa_acumulada
          bmv_dia.cambio_promedio = new_bmv.cambio_promedio
          bmv_dia.prediccion_lineal = new_bmv.prediccion_lineal
          bmv_dia.error_promedio = new_bmv.error_promedio
          bmv_dia.save()
  except:
    pass
  
  # IPC
  
  fecha = ""
  
  url = 'http://www.bmv.com.mx/img-bmv/home.html'
  f = urllib2.urlopen(url).read()
  
  farr = f.split('<html>')
  f = farr[2]
  farr = f.split('</html>')
  f = "<html>%s</html>" % farr[0]
  
  soup = BeautifulSoup(f)
  
  valores = []
  
  for span in soup.findAll('span', {'class':'leftalignclass'}):
    valores.append(clean_string(span.contents[0].replace(',', '')))
  
  if(len(valores) > 0):
    valor = float(valores[0])
    
    fecha = valores[4]
    farr = fecha.split('/')
    
    d = farr[0]
    m = addNumCero(getMesNum(farr[1], short=True))
    y = farr[2]
    
    fecha = "%s-%s-%s" % (y, m, d)
    
    hora = valores[5]
    
    if(valor != 0 and hora != ""):
      # Checamos si ya existe
      try:
        bmv_alr = BmvIpc.objects.filter(fecha=fecha, hora=hora).order_by('-id')[0]
      except:
        bmv_alr = False
      
      # Ultimo agregaddo
      try:
        bmv_last = BmvIpc.objects.all().order_by('-id')[0]
      except:
        bmv_last = False
      
      if(not bmv_alr and (not bmv_last or bmv_last.hora != hora)):
        new_bmv_ipc = BmvIpc(hora=hora, valor=valor, fecha=fecha)
        new_bmv_ipc.save()
      
      # Ahora para valor del dia
      try:
        bmv_alr = BmvIpcDia.objects.filter(fecha=fecha).order_by('-id')[0]
      except:
        bmv_alr = False
      
      if(not bmv_alr):
        bmv_alr = BmvIpcDia(valor=valor, fecha=fecha, hora=hora)
      else:
        bmv_alr.valor = valor
        bmv_alr.hora = hora
      
      bmv_alr.save()
  
  return direct_to_template(request, 'ajax.html', {'out':'done'})
