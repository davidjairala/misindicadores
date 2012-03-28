from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from numpy import *
from misindicadores.globals.functions import *
register = template.Library()

@register.filter
def sDate(fecha, style = 1):
  fecha = doDate(fecha, style)
  
  return fecha
sDate.is_safe = True

@stringfilter
@register.filter
def curlize(value):
  from django.utils.html import urlize
  str = mark_safe(urlize(value, nofollow=True, autoescape=True))
  str = mark_safe(str.replace('<a href="', '<a target="_blank" href="'))
  return str

@stringfilter
@register.filter
def currency(value):
  return dinero(value)

@stringfilter
@register.filter
def currency_four(value):
  return addNumComas("%.4f", float(value))

# Agarra una stat de la lista de estadisticas
@register.filter
def get_stat(arr, stat):
  return arr[stat]
get_stat.is_safe = True

# Dibuja select sin dia
@register.filter
def fecha_select_no_day(fecha, name = ""):
  return fecha_select(fecha, name, show_day = False)
fecha_select_no_day.is_safe = True

# Dibuja select sin dia y sin mes
@register.filter
def fecha_select_no_dm(fecha, name = ""):
  return fecha_select(fecha, name, show_day = False, show_month = False)
fecha_select_no_dm.is_safe = True

# Formatea una hora
@register.filter
def format_hora(hora):
  hora = addNumCero(hora)
  
  return "%s:00" % hora
format_hora.is_safe = True

# Dibuja select de fecha
@register.filter
def fecha_select(fecha, name = "", show_day = True, show_month = True):
  try:
    farr = fecha.split('-')
  except:
    fecha = fecha.strftime("%Y-%m-%d")
    farr = fecha.split('-')
  
  year = int(farr[0])
  day = int(farr[2])
  month = int(farr[1])
  
  html = ''
  
  if(show_day):
    html += '<select name="%s_d">' % name
  
    for i in range(1, 32):
      if(i == day):
        sel = 'selected="selected"'
      else:
        sel = ''
      html += '<option value="%s" %s>%d</option>' % (addNumCero(i), sel, i)
  
    html += '</select> '
  
  if(show_month):
    html += '<select name="%s_m">' % name
  
    for i in range(1, 13):
      if(i == month):
        sel = 'selected="selected"'
      else:
        sel = ''
      html += '<option value="%s" %s>%s</option>' % (addNumCero(i), sel, getMes(i, short=True))
  
    html += '</select> '
  
  html += '<select name="%s_y">' % name
  
  for i in range(year - 5, year + 6):
    if(i == year):
      sel = 'selected="selected"'
    else:
      sel = ''
    html += '<option value="%s" %s>%s</option>' % (i, sel, i)
  
  html += '</select>'  
  
  return html
fecha_select.is_safe = True
