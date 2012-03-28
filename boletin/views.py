from django.http import HttpResponseRedirect
from django.views.generic.simple import direct_to_template
from django.contrib import messages
from django.db.models import Q
from misindicadores.globals.functions import *
from misindicadores.boletin.models import *
from misindicadores.boletin.helper import *

# Cron dos dia
def cron_dos_dia(request):
  from datetime import date, datetime
  from django.core.mail import EmailMultiAlternatives
  
  fecha = date.today()
  today = datetime.today()
  
  hora = today.hour
  dia = get_dias_ing()[today.weekday()]
  
  html = ''
  
  subject = 'Mis Indicadores - Boletin - ' + doDate(fecha)
  
  try:
    boletins = Boletin.objects.filter(activo=True, periocidad="dos_dia")
    
    html = get_boletin_html(fecha)
    
    for boletin in boletins:
      msg = EmailMultiAlternatives(subject, html, 'info@misindicadores.com', [boletin.user.email])
      msg.content_subtype = "html"
      msg.send(fail_silently=True)
  except:
    pass
  
  #return direct_to_template(request, 'boletin/out.html', {'out':html})
  return direct_to_template(request, 'ajax.html', {'out':'done'})

# Cron diario
def cron_diario(request):
  from datetime import date, datetime
  from django.core.mail import EmailMultiAlternatives
  
  fecha = date.today()
  today = datetime.today()
  
  hora = today.hour
  dia = get_dias_ing()[today.weekday()]
  
  html = ''
  
  subject = 'Mis Indicadores - Boletin - ' + doDate(fecha)
  
  try:
    boletins = Boletin.objects.filter(activo=True, periocidad="diario", hora=hora)
    
    html = get_boletin_html(fecha)
    
    for boletin in boletins:
      msg = EmailMultiAlternatives(subject, html, 'info@misindicadores.com', [boletin.user.email])
      msg.content_subtype = "html"
      msg.send(fail_silently=True)
  except:
    pass
  
  #return direct_to_template(request, 'boletin/out.html', {'out':html})
  return direct_to_template(request, 'ajax.html', {'out':'done'})

# Cron semanal
def cron_semanal(request):
  from datetime import date, datetime
  from django.core.mail import EmailMultiAlternatives
  
  fecha = date.today()
  today = datetime.today()
  
  hora = today.hour
  dia = get_dias_ing()[today.weekday()]
  
  html = ''
  
  subject = 'Mis Indicadores - Boletin - ' + doDate(fecha)
  
  try:
    boletins = Boletin.objects.filter(activo=True, periocidad="semanal", hora=hora, dia=dia)
    
    html = get_boletin_html(fecha)
    
    for boletin in boletins:
      msg = EmailMultiAlternatives(subject, html, 'info@misindicadores.com', [boletin.user.email])
      msg.content_subtype = "html"
      msg.send(fail_silently=True)
  except:
    pass
  
  #return direct_to_template(request, 'boletin/out.html', {'out':html})
  return direct_to_template(request, 'ajax.html', {'out':'done'})

# Portada
def index(request):
  from datetime import datetime
  
  today = datetime.today()
  hora = today.hour
  minutos = today.minute
  boletin = None
  
  if(request.user.is_authenticated()):
    # Checamos si tenemos que actualizar
    if(request.POST):
      try:
        activo = int(request.POST['activo'])
      except:
        activo = 0
      periocidad = request.POST['periocidad']
      dia = request.POST['dia']
      hora = request.POST['hora']
      
      boletin = Boletin.objects.get(user=request.user)
      
      if(activo == 1):
        boletin.activo = True
      else:
        boletin.activo = False
      
      boletin.periocidad = periocidad
      boletin.dia = dia
      boletin.hora = int(hora)
      
      boletin.save()
      
      messages.add_message(request, messages.SUCCESS, 'Tu bolet&iacute;n se ha configurado correctamente.')
    
    try:
      boletin = Boletin.objects.get(user=request.user)
    except:
      boletin = Boletin(user=request.user, periocidad='semanal', activo=False)
      boletin.dia = boletin.get_rand_dia()
      boletin.hora = boletin.get_rand_hora()
      boletin.save()
  
  return direct_to_template(request, 'boletin/index.html', {
    'boletin': boletin,
    'hora': hora,
    'minutos':minutos,
  })