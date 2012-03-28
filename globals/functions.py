from numpy import *
from scipy.stats import mode, skew, sem, kurtosis

# Quita entidades de html o xml de un string y regresa el string puro encodificado correctamente
def unescape(text):
  import re, htmlentitydefs

  def fixup(m):
    text = m.group(0)
    if text[:2] == "&#":
      # character reference
      try:
        if text[:3] == "&#x":
          return unichr(int(text[3:-1], 16))
        else:
          return unichr(int(text[2:-1]))
      except ValueError:
        pass
    else:
      # named entity
      try:
        text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
      except KeyError:
        pass
    return text # leave as is
  return re.sub("&#?\w+;", fixup, text)

# Html header simmple
def simple_header():
  html = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"\
  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\
  <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">\
  <head>\
    <meta http-equiv="content-type" content="text/html;charset=UTF-8" />\
    <title>Mis Indicadores</title>\
    <link rel="shortcut icon" href="/site_media/images/fav.ico" />\
    <link rel="stylesheet" href="/site_media/css/style.css" type="text/css" />\
  </head>\
  <body>\
    <a href="/" title="Mis Indicadores"><img src="/site_media/images/logo.png" alt="Mis Indicadores" /></a>'

  return html

# Html footer simple
def simple_footer():
  html = '</body></html>'

  return html

# Helper de addNumComas
def _commafy(s):
	r = []
	for i, c in enumerate(reversed(s)):
		if i and (not (i % 3)):
			r.insert(0, ',')
		r.insert(0, c)
	return ''.join(r)

# Agrega comas a un numero
def addNumComas(format, value):
	import re
	re_digits_nondigits = re.compile(r'\d+|\D+')
	parts = re_digits_nondigits.findall(format % (value,))
	for i in xrange(len(parts)):
		s = parts[i]
		if s.isdigit():
			parts[i] = _commafy(s)
			break
	return ''.join(parts)

# Formato de dinero
def dinero(num, decimales = 2):
  try:
    format = "%." + str(decimales) + "f"
    return addNumComas(format, float(num))
  except:
    return 0

# URL de la app
def get_app_url():
  return "http://misindicadores.com/"

# Dias en ingles
def get_dias_ing():
  return ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Stopwords
def stopwords():
  return ['de','a','hasta','ni','mil','un','una','unas','unos','uno','sobre','todo','tambien','tras','otro','algun','alguno','alguna','algunos','algunas','ser','es','soy','eres','somos','sois','estoy','esta','estamos','estais','estan','como','en','para','atras','porque','por que','estado','estaba','ante','antes','siendo','ambos','pero','por','poder','puede','puedo','podemos','podeis','pueden','fui','fue','fuimos','fueron','hacer','hago','hace','hacemos','haceis','hacen','cada','fin','incluso','primero','desde','conseguir','consigo','consigue','consigues','conseguimos','consiguen','ir','voy','va','vamos','vais','van','vaya','gueno','ha','tener','tengo','tiene','tenemos','teneis','tienen','el','la','lo','las','los','su','aqui','mio','tuyo','ellos','ellas','nos','nosotros','vosotros','vosotras','si','dentro','solo','solamente','saber','sabes','sabe','sabemos','sabeis','saben','ultimo','largo','bastante','haces','muchos','aquellos','aquellas','sus','entonces','tiempo','verdad','verdadero','verdadera','cierto','ciertos','cierta','ciertas','intentar','intento','intenta','intentas','intentamos','intentais','intentan','dos','bajo','arriba','encima','usar','uso','usas','usa','usamos','usais','usan','emplear','empleo','empleas','emplean','ampleamos','empleais','valor','muy','era','eras','eramos','eran','modo','bien','cual','cuando','donde','mientras','quien','con','entre','sin','trabajo','trabajar','trabajas','trabaja','trabajamos','trabajais','trabajan','podria','podrias','podriamos','podrian','podriais','yo','aquel']

# Pasa un string a palabras buscables
def searchify(txt):
  from django.template.defaultfilters import slugify

  sws = stopwords()

  txt = slugify(txt)

  txt_arr = txt.split('-')

  out_arr = []

  for s in txt_arr:
    if(len(s) >= 3 and not (s in sws)):
      out_arr.append(s)

  txt = ' '.join(out_arr)

  return txt

# Agrega un cero a un numero si lo necesita
def addNumCero(n):
  if(n < 10):
    n = "0%d" % (n)
  else:
    n = str(n)

  return n

# Quita tags de html de un string
def strip_tags_script(txt):
  import re

  p = re.compile(r'<script(.*)<\/script>', re.IGNORECASE)
  return p.sub('', txt)

# Quita parrafos vacios de un texto y regresa primer parrafo
def get_first_parragraph(txt):
  txt_arr = txt.split('\n')
  parrafo = None

  for p in txt_arr:
    if(parrafo is None and len(p) > 5):
      parrafo = p

  return parrafo

# Quita tabs de un string
def strip_tabs(txt):
  import re

  p = re.compile(r'\t')
  return p.sub('', txt)

# Quita tags de html de un string
def strip_tags(txt):
  import re

  p = re.compile(r'<[^>]*>')
  txt = p.sub('', txt)
  p = re.compile(r'\&nbsp;')
  txt = p.sub('', txt)

  return txt

# Limpia un string
def clean_string(txt, strip = True):
  import re

  p = re.compile('( )+')

  txt = txt.replace(chr(10), '').replace(chr(13), '').replace('&nbsp;', ' ').replace(chr(9), ' ')
  txt = p.sub(' ', txt).strip()

  if(strip):
    txt = strip_tags(txt)

  return txt

# Lista de meses
def arrMeses():
  return ['', 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

# Lista de meses en ingles
def arrMesesIng():
  return ['', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

# Regresa el nombre de un mes
def getMes(m, short = False):
  meses = arrMeses()

  if(short):
    return meses[m][:3]
  else:
    return meses[m]

# Regresa el numero de un mes
def getMesNum(m, short = False, ingles = False):
  if(ingles):
    meses = arrMesesIng()
  else:
    meses = arrMeses()

  cont = 0

  for mes in meses:
    mes_s = mes
    if(short):
      mes_s = mes[:3]
    if mes_s.lower() == m.lower():
      return cont
    cont += 1

# Formatea una fecha
def doDate(fecha, style = 1):
  try:
    try:
      farr = fecha.split('-')
    except:
      fecha = fecha.strftime("%Y-%m-%d")
      farr = fecha.split('-')

    m = arrMeses()[int(farr[1])]

    if(style == 1):
      fecha = farr[2] + '/' + m[:3] + '/' + farr[0]
    elif(style == 2):
      fecha = m[:3] + '/' + farr[0]
    else:
      fecha = farr[0] + ' de ' + m + ', ' + farr[0]
  except:
    fecha = ''

  return fecha

# Regresa el ultimo valor de una lista
def lastValue(arr):
  return arr[0]

# Regresa el maximo valor de una lista
def get_max(arr):
  return max(array(arr))

# Regresa el minimo valor de una lista
def get_min(arr):
  return min(array(arr))

# Regresa la desv estandar de una lista
def get_desv(arr):
  return std(array(arr))

# Regresa la tendencia de una lista
def get_tendencia(arr):
  delta = lastValue(arr) - arr[len(arr) - 1]

  if(delta > 0):
    return "Alza"
  elif(delta < 0):
    return "Baja"
  else:
    return "Mantiene"

# Regresa el color de la tendencia
def get_tendencia_color(arr):
  delta = lastValue(arr)- arr[len(arr) - 1]

  if(delta > 0):
    return "green"
  elif(delta < 0):
    return "red"
  else:
    return "black"

# Promedio de una lista
def get_promedio(arr):
  return mean(array(arr))

# Media de una lista
def get_media(arr):
  return median(array(arr))

# Varianza de una lista
def get_varianza(arr):
  return var(array(arr))

# Moda de una lista
def get_moda(arr):
  return mode(array(arr))[0]

# Skew (Inclinacion)
def get_skew(arr):
  return skew(array(arr))

# SEM (Error estandar del promedio [mean])
def get_sem(arr):
  return sem(array(arr))

# Kurtosis
def get_kurtosis(arr):
  return kurtosis(array(arr))

# Tendencia relativa
def get_tendencia_relativa(arr):
  last = lastValue(arr)
  try:
    tr = last - arr[1]
  except:
    tr = 0
  return tr

# Tendencia relativa acumulada
def get_tra(arr):
  difs = []
  cont = 0

  for a in arr:
    if(cont > 0):
      dif = arr[cont - 1] - a
      difs.append(dif)
    cont += 1

  return sum(array(difs))

# Error Promedio
def get_ep(arr):
  pred = 0
  dif = 0
  errors = []
  cont = 0

  for val in arr:
    if(cont > 0):
      pred = arr[cont - 1] + (arr[cont - 1] - val)
    if(cont > 1):
      dif = val - pred
      errors.append(dif)
    cont += 1

  return get_promedio(errors)

# Prediccion lineal
def get_pl(arr):
  if(len(arr) > 1):
    tra = get_tra(arr)
    last = lastValue(arr)
    ep = get_ep(arr)

    return last + tra + ep
  else:
    return 0

# Regresa todas las estadisticas para una lista
def get_stats(arr):
  stats = {}

  stats['last_value'] = lastValue(arr)
  stats['max'] = get_max(arr)
  stats['min'] = get_min(arr)
  stats['desv'] = get_desv(arr)
  stats['tendencia'] = get_tendencia(arr)
  stats['tendencia_color'] = get_tendencia_color(arr)
  stats['promedio'] = get_promedio(arr)
  stats['media'] = get_media(arr)
  stats['varianza'] = get_varianza(arr)
  stats['moda'] = get_moda(arr)
  stats['skew'] = get_skew(arr)
  stats['sem'] = get_sem(arr)
  stats['kurtosis'] = get_kurtosis(arr)
  stats['tendencia_relativa'] = get_tendencia_relativa(arr)
  stats['tra'] = get_tra(arr)
  stats['prediccion_lineal'] = get_pl(arr)

  return stats
