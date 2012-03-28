from django.http import HttpResponseRedirect
from django.views.generic.simple import direct_to_template
from django.contrib import messages
from numpy import *
from misindicadores.globals.functions import *
from misindicadores.desempeno.models import *

# Portada
def portada(request):
  return direct_to_template(request, 'desempeno/portada.html', {})

# Afores
def afores(request):
  from operator import itemgetter
  
  # Comara dos afores por rendimiento neto
  def comp_afores(a, b):
    return cmp(a['rendimiento_neto'], b['rendimiento_neto'])
  
  try:
    tipo = int(request.GET['tipo'])
  except:
    tipo = 5
  
  last_afore = Afore.objects.latest('fecha')
  last_fecha = last_afore.fecha
  
  afores = Afore.objects.filter(fecha=last_fecha).filter(tipo=tipo)
  final_afores = []
  
  chart_categories = []
  chart_rendimientos = []
  chart_rendimientos_netos = []
  chart_comision = []
  afores_nombres = []
  promedios = {}
  promedios_final = {}
  promedios_short = {}
  
  for afore in afores:
    rendimiento_neto = afore.rendimiento - afore.comision
    
    try:
      afores_nombres.index(afore.afore)
    except:
      afores_nombres.append(afore.afore)
      chart_categories.append(afore.afore[:10])
      chart_rendimientos.append(afore.rendimiento)
      chart_rendimientos_netos.append(rendimiento_neto)
      chart_comision.append(afore.comision)
      promedios[afore.afore] = []
    
    final_afores.append({
      'afore':afore.afore,
      'rendimiento':afore.rendimiento,
      'comision':afore.comision,
      'rendimiento_neto':rendimiento_neto
    })
  
  final_afores.sort(comp_afores)
  final_afores.reverse()
  
  # Recorremos lista de nombres para sacar rendimientos netos promedio
  for afore in afores_nombres:
    past_afores = Afore.objects.filter(afore=afore).order_by('-fecha')[:15]
    
    for past_afore in past_afores:
      rendimiento_neto = past_afore.rendimiento - past_afore.comision
      promedios[past_afore.afore].append(rendimiento_neto)
  
  for promedio in promedios:
    promedios_final[promedio] = get_promedio(promedios[promedio])
  
  promedios_final = sorted(promedios_final.iteritems(), key=itemgetter(1), reverse=True)
  
  promedios_short_old = promedios_short
  promedios_short = []
  
  cont_promedios = 0
  for promedio in promedios_final:
    promedios_short.append({
      'afore':promedio[0],
      'promedio':promedio[1],
    })
    
    cont_promedios += 1
    if(cont_promedios > 2):
      break
  
  promedios_final_old = promedios_final
  promedios_final = []
  
  # Formato de promedios_final
  for promedio in promedios_final_old:
    promedios_final.append({
      'afore':promedio[0],
      'promedio':promedio[1],
    })
  
  return direct_to_template(request, 'desempeno/afores.html', {
    'fecha':last_fecha,
    'afores':final_afores,
    'chart_title':'Afores',
    'chart_source':'CONSAR',
    'chart_categories':chart_categories,
    'chart_rendimientos':chart_rendimientos,
    'chart_rendimientos_netos':chart_rendimientos_netos,
    'chart_comision':chart_comision,
    'promedios_short':promedios_short,
    'promedios':promedios_final,
  })

# Reservas
def reservas(request):
  try:
    fecha = "%s-%s-%s" % (request.GET['_y'], request.GET['_m'], request.GET['_d'])
  except:
    last_reserva = Reserva.objects.all().order_by('-fecha')[0]
    fecha = last_reserva.fecha.strftime("%Y-%m-%d")
  
  reservas = Reserva.objects.filter(fecha__lte=fecha).order_by('-fecha')[:30]
  
  if(len(reservas) > 0):
    bms = []
    ainps = []
    ainds = []
    cinps = []
    rids = []
    bmps = []
    ainpvs = []
    aindvs = []
    cinpvs = []
    chart_bms = []
    chart_ainps = []
    chart_ainds = []
    chart_cinps = []
    chart_rids = []
    chart_bmps = []
    chart_ainpvs = []
    chart_aindvs = []
    chart_cinpvs = []
    chart_categories = []
  
    for reserva in reservas:
      bms.append(reserva.base_monetaria)
      ainps.append(reserva.activos_internacionales_netos_pesos)
      ainds.append(reserva.activos_internacionales_netos_dolares)
      cinps.append(reserva.credito_interno_neto_pesos)
      rids.append(reserva.reserva_internacional_dolares)
      bmps.append(reserva.base_monetaria_pesos)
      ainpvs.append(reserva.activos_internacionales_netos_pesos_var)
      aindvs.append(reserva.activos_internacionales_netos_dolares_var)
      cinpvs.append(reserva.credito_interno_neto_pesos_var)
    
      chart_bms.append(str(reserva.base_monetaria))
      chart_ainps.append(str(reserva.activos_internacionales_netos_pesos))
      chart_ainds.append(str(reserva.activos_internacionales_netos_dolares))
      chart_cinps.append(str(reserva.credito_interno_neto_pesos))
      chart_rids.append(str(reserva.reserva_internacional_dolares))
      chart_bmps.append(str(reserva.base_monetaria_pesos))
      chart_ainpvs.append(str(reserva.activos_internacionales_netos_pesos_var))
      chart_aindvs.append(str(reserva.activos_internacionales_netos_dolares_var))
      chart_cinpvs.append(str(reserva.credito_interno_neto_pesos_var))
      chart_categories.append('"' + doDate(reserva.fecha) + '"')
  
    chart_categories.reverse()
    chart_categories = ','.join(chart_categories)
    chart_bms.reverse()
    chart_bms = ','.join(chart_bms)
    chart_ainps.reverse()
    chart_ainps = ','.join(chart_ainps)
    chart_ainds.reverse()
    chart_ainds = ','.join(chart_ainds)
    chart_cinps.reverse()
    chart_cinps = ','.join(chart_cinps)
    chart_rids.reverse()
    chart_rids = ','.join(chart_rids)
    chart_bmps.reverse()
    chart_bmps = ','.join(chart_bmps)
    chart_ainpvs.reverse()
    chart_ainpvs = ','.join(chart_ainpvs)
    chart_aindvs.reverse()
    chart_aindvs = ','.join(chart_aindvs)
    chart_cinpvs.reverse()
    chart_cinpvs = ','.join(chart_cinpvs)
  
    bms = get_stats(bms)
    ainps = get_stats(ainps)
    ainds = get_stats(ainds)
    cinps = get_stats(cinps)
    rids = get_stats(rids)
    bmps = get_stats(bmps)
    ainpvs = get_stats(ainpvs)
    aindvs = get_stats(aindvs)
    cinpvs = get_stats(cinpvs)
  
    return direct_to_template(request, 'desempeno/reservas.html', {
      'fecha':fecha,
      'reservas':reservas,
      'bms':bms,
      'ainps':ainps,
      'ainds':ainds,
      'cinps':cinps,
      'rids':rids,
      'bmps':bmps,
      'ainpvs':ainpvs,
      'aindvs':aindvs,
      'cinpvs':cinpvs,
      'chart_title':'Reservas internacionales',
      'chart_source':'Banco de M&eacute;xico',
      'chart_categories':chart_categories,
      'chart_bms':chart_bms,
      'chart_ainps':chart_ainps,
      'chart_ainds':chart_ainds,
      'chart_cinps':chart_cinps,
      'chart_rids':chart_rids,
      'chart_bmps':chart_bmps,
      'chart_ainpvs':chart_ainpvs,
      'chart_aindvs':chart_aindvs,
      'chart_cinpvs':chart_cinpvs,
      'slug':'reservas'
    })
  else:
    messages.add_message(request, messages.ERROR, 'No encontramos valores para la fecha seleccionada.')
    return HttpResponseRedirect('/desempeno/reservas/')

# PIB
def pib(request):
  if(request.GET and request.GET['_y']):
    year = int(request.GET['_y'])
  else:
    last_pib = Pib.objects.all().order_by('-year', '-trimestre')[0]
    year = last_pib.year
  
  fecha = "%s-12-01" % (year)
  
  pibs = Pib.objects.filter(year__lte=year).order_by('-year', '-trimestre')[:30]
  
  if(len(pibs) > 0):
    totales = []
    primarias = []
    secundarias = []
    terciarias = []
    chart_totales = []
    chart_primarias = []
    chart_secundarias = []
    chart_terciarias = []
    chart_categories = []
  
    for pib in pibs:
      totales.append(pib.total)
      primarias.append(pib.primarias)
      secundarias.append(pib.secundarias)
      terciarias.append(pib.terciarias)
    
      chart_totales.append(str(pib.total))
      chart_primarias.append(str(pib.primarias))
      chart_secundarias.append(str(pib.secundarias))
      chart_terciarias.append(str(pib.terciarias))
      chart_categories.append('"' + pib.get_fecha() + '"')
  
    chart_categories.reverse()
    chart_categories = ','.join(chart_categories)
    chart_totales.reverse()
    chart_totales = ','.join(chart_totales)
    chart_primarias.reverse()
    chart_primarias = ','.join(chart_primarias)
    chart_secundarias.reverse()
    chart_secundarias = ','.join(chart_secundarias)
    chart_terciarias.reverse()
    chart_terciarias = ','.join(chart_terciarias)
  
    totales = get_stats(totales)
    primarias = get_stats(primarias)
    secundarias = get_stats(secundarias)
    terciarias = get_stats(terciarias)
  
    return direct_to_template(request, 'desempeno/pib.html', {
      'year':year,
      'fecha':fecha,
      'pibs':pibs,
      'totales':totales,
      'primarias':primarias,
      'secundarias':secundarias,
      'terciarias':terciarias,
      'chart_title':'Producto Interno Bruto',
      'chart_source':'INEGI',
      'chart_categories':chart_categories,
      'chart_totales':chart_totales,
      'chart_primarias':chart_primarias,
      'chart_secundarias':chart_secundarias,
      'chart_terciarias':chart_terciarias,
      'slug':'pib'
    })
  else:
    messages.add_message(request, messages.ERROR, 'No encontramos valores para la fecha seleccionada.')
    return HttpResponseRedirect('/desempeno/desempleo/')

# Desempleo
def desempleo(request):
  if(request.GET and request.GET['_y']):
    year = int(request.GET['_y'])
  else:
    last_desempleo = Desempleo.objects.all().order_by('-year', '-month')[0]
    year = last_desempleo.year
  
  fecha = "%s-12-01" % (year)
  
  desempleos = Desempleo.objects.filter(year__lte=year).order_by('-year', '-month')[:30]
  
  if(len(desempleos) > 0):
    totales = []
    hombres = []
    mujeres = []
    chart_totales = []
    chart_hombres = []
    chart_mujeres = []
    chart_categories = []
  
    for desempleo in desempleos:
      totales.append(desempleo.total)
      hombres.append(desempleo.hombres)
      mujeres.append(desempleo.mujeres)
    
      chart_totales.append(str(desempleo.total))
      chart_hombres.append(str(desempleo.hombres))
      chart_mujeres.append(str(desempleo.mujeres))
      chart_categories.append('"' + doDate("%s-%s-01" % (desempleo.year, addNumCero(desempleo.month)), 2) + '"')
  
    chart_categories.reverse()
    chart_categories = ','.join(chart_categories)
    chart_totales.reverse()
    chart_totales = ','.join(chart_totales)
    chart_hombres.reverse()
    chart_hombres = ','.join(chart_hombres)
    chart_mujeres.reverse()
    chart_mujeres = ','.join(chart_mujeres)
  
    totales = get_stats(totales)
    hombres = get_stats(hombres)
    mujeres = get_stats(mujeres)
  
    return direct_to_template(request, 'desempeno/desempleo.html', {
      'year':year,
      'fecha':fecha,
      'desempleos':desempleos,
      'totales':totales,
      'hombres':hombres,
      'mujeres':mujeres,
      'chart_title':'Desempleo',
      'chart_source':'INEGI',
      'chart_categories':chart_categories,
      'chart_totales':chart_totales,
      'chart_hombres':chart_hombres,
      'chart_mujeres':chart_mujeres,
      'slug':'desempleo'
    })
  else:
    messages.add_message(request, messages.ERROR, 'No encontramos valores para la fecha seleccionada.')
    return HttpResponseRedirect('/desempeno/desempleo/')

# Cron Desempeno
def cron_desempeno(request):
  import re
  import urllib2
  from BeautifulSoup import BeautifulSoup
  from django.utils.encoding import smart_unicode
  
  # Desempleo
  
  url = 'http://dgcnesyp.inegi.org.mx/cgi-win/bdiecoy.exe/621?s=est&c=12933'
  f = urllib2.urlopen(url).read()
  
  f = f.replace(chr(10), '').replace(chr(13), '')
  
  farr = f.split('n nacional, serie unificada')
  f = '<hmtml><body>' + farr[2]
  
  farr = f.split('Para visualizar mejor este sitio se recomienda el uso de un navegador')
  f = farr[0] + '</body></html>'
  
  soup = BeautifulSoup(f)
  
  year = 0
  mes = 0
  total = 0
  hombres = 0
  mujeres = 0
  
  tr_cont = 0
  td_cont = 0
  
  start_line = False
  
  trs = soup.findAll('tr')
  trs = trs[3:len(trs)]
  
  for tr in trs:
    tds = tr.findAll('td')
    
    try:
      colspan = int(tds[0]['colspan'])
    except:
      colspan = 0
    
    if(colspan == 4):
      start_line = False
    
    if(not start_line and (len(tds) == 1 or colspan == 4)):
      try:
        content = clean_string(tds[0].find('b').contents[0])
        year = int(content)
        start_line = True
      except:
        year = 0
    elif(start_line):
      try:
        mes = getMesNum(clean_string(tds[0].contents[0]), short=False)
        total = float(clean_string(tds[1].find('nobr').contents[0]))
        hombres = float(clean_string(tds[2].find('nobr').contents[0]))
        mujeres = float(clean_string(tds[3].find('nobr').contents[0]))
      except:
        mes = 0
        total = 0
        hombres = 0
        mujeres = 0
      
      if(mes == "" or mes == 'NOTA:'):
        start_line = False
      
      if(mes != "" and total != 0 and hombres != 0 and mujeres != 0):
        # Checamos si existe
        try:
          desempleo = Desempleo.objects.filter(year=year, month=mes, total=total, hombres=hombres, mujeres=mujeres)[0]
        except:
          desempleo = Desempleo()
        
        desempleo.year = year
        desempleo.month = mes
        desempleo.total = total
        desempleo.hombres = hombres
        desempleo.mujeres = mujeres
        desempleo.save()
  
  # PIB
  
  url = 'http://dgcnesyp.inegi.org.mx/cgi-win/bdiecoy.exe/588?s=est&c=12500'
  f = urllib2.urlopen(url).read()
  
  farr = f.split('(Millones de pesos corrientes)')
  
  f = farr[1]
  
  farr = f.split('NOTA:')
  
  f = '<html><body>' + farr[0] + '</body></html>'
  
  soup = BeautifulSoup(f)
  
  year = ""
  trimestre = 0
  total = 0
  primarias = 0
  secundarias = 0
  terciarias = 0
  
  p = re.compile(',|( )+')
  
  for tr in soup.findAll('tr'):
    tds = tr.findAll('td')
    if(len(tds) == 1):
      try:
        year = int(clean_string(tds[0].find('b').contents[0]))
      except:
        year = ""
    elif(year != ""):
      try:
        trimestre = p.sub('', clean_string(tds[0].contents[0]))
        total = p.sub('', clean_string(tds[1].find('nobr').contents[0]))
        primarias = p.sub('', clean_string(tds[2].find('nobr').contents[0]))
        secundarias = p.sub('', clean_string(tds[3].find('nobr').contents[0]))
        terciarias = p.sub('', clean_string(tds[4].find('nobr').contents[0]))
      
        if(trimestre == 'I'):
          trimestre = 1
        elif(trimestre == 'II'):
          trimestre = 2
        elif(trimestre == 'III'):
          trimestre = 3
        elif(trimestre == 'IV'):
          trimestre = 4
      
        # Checamos si existe
        try:
          pib = Pib.objects.filter(year=year, trimestre=trimestre)[0]
        except:
          pib = Pib()
        
        pib.year = year
        pib.trimestre = trimestre
        pib.total = total
        pib.primarias = primarias
        pib.secundarias = secundarias
        pib.terciarias = terciarias
        
        pib.save()
      except:
        pass
  
  # Reservas
  
  url = 'http://www.banxico.org.mx/SieInternet/consultarDirectorioInternetAction.do?accion=consultarCuadro&idCuadro=CF106&sector=4&locale=es'
  f = urllib2.urlopen(url).read()
  
  farr = f.split('<p style="padding: 0px; margin: 8px 0px 0px 0px;">')
  f = farr[2]
  
  farr = f.split('Notas:')
  
  f = '<html><body>' + farr[0] + '</body></html>'
  
  soup = BeautifulSoup(f)
  
  p = re.compile('[0-9]{2}\/[0-9]{2}\/[0-9]{4}')
  pval = re.compile('[0-9]+\.[0-9]+')
  
  fechas = []
  
  for td in soup.findAll('td', {'class':'cd_titulos_tabla'}):
    try:
      content = clean_string(td.contents[0])
      
      if(p.search(content)):
        farr = content.split('/')
        
        fechas.append("%s-%s-%s" % (farr[2], farr[1], farr[0]))
    except:
      pass
  
  cont_td = 0;
  key_fechas = 0;
  cont_val = 0;
  val = ""
  
  reservas = {}
  
  for td in soup.findAll('td', {'class':'cd_tabla_renglon'}):
    try:
      content = clean_string(td.contents[0]).replace(',', '')
    
      if(pval.search(content)):
        if(cont_val == 0):
          val = "base_monetaria"
        elif(cont_val == 1):
          val = "activos_internacionales_netos_pesos"
        elif(cont_val == 2):
          val = "activos_internacionales_netos_dolares"
        elif(cont_val == 3):
          val = "credito_interno_neto_pesos"
        elif(cont_val == 4):
          val = "reserva_internacional_dolares"
        elif(cont_val == 5):
          val = "base_monetaria_pesos"
        elif(cont_val == 6):
          val = "activos_internacionales_netos_pesos_var"
        elif(cont_val == 7):
          val = "activos_internacionales_netos_dolares_var"
        elif(cont_val == 8):
          val = "credito_interno_neto_pesos_var"
      
        try:
          reservas[fechas[key_fechas]][val] = float(content)
        except:
          reservas[fechas[key_fechas]] = {}
          reservas[fechas[key_fechas]][val] = float(content)
      
        key_fechas += 1
      
        if(key_fechas > 2):
          key_fechas = 0
          cont_val += 1
    except:
      pass
  
  for k, v in reservas.items():
    fecha = k
    
    # Checamos si existe
    try:
      reserva = Reserva.objects.filter(fecha=fecha)[0]
    except:
      reserva = Reserva()
    
    reserva.fecha = fecha
    reserva.base_monetaria = v["base_monetaria"]
    reserva.activos_internacionales_netos_pesos = v["activos_internacionales_netos_pesos"]
    reserva.activos_internacionales_netos_dolares = v["activos_internacionales_netos_dolares"]
    reserva.credito_interno_neto_pesos = v["credito_interno_neto_pesos"]
    reserva.reserva_internacional_dolares = v["reserva_internacional_dolares"]
    reserva.base_monetaria_pesos = v["base_monetaria_pesos"]
    reserva.activos_internacionales_netos_pesos_var = v["activos_internacionales_netos_pesos_var"]
    reserva.activos_internacionales_netos_dolares_var = v["activos_internacionales_netos_dolares_var"]
    reserva.credito_interno_neto_pesos_var = v["credito_interno_neto_pesos_var"]
    
    reserva.save()
  
  return direct_to_template(request, 'ajax.html', {'out':'done'})
