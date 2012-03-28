from django.http import HttpResponseRedirect
from django.views.generic.simple import direct_to_template
from django.contrib import messages
from misindicadores.globals.functions import *
from misindicadores.foros.models import *
from django.core.paginator import Paginator
from django.contrib import messages

# Nuevo topico
def nuevo_topico(request, nombre_limpio):
  categoria = Categoria.objects.filter(nombre_limpio=nombre_limpio)[0]
  
  # Checamos si tenemos que crear topico
  if(request.POST):
    if(request.user.is_authenticated()):
      try:
        titulo = request.POST['titulo']
        mensaje = request.POST['mensaje']
        
        if(titulo != "" and mensaje != ""):
          if(request.user.is_staff and request.POST['fake_user'] != ""):
            mensaje_user = User.objects.get(pk=request.POST['fake_user'])
          else:
            mensaje_user = request.user
          
          # Creamos topicos
          topico = Topico(user=mensaje_user, categoria=categoria, titulo=titulo)
          topico.save()
        
          # Creamos mensaje
          mensaje = Mensaje(user=mensaje_user, topico=topico, mensaje=mensaje)
          mensaje.save()
        
          messages.add_message(request, messages.SUCCESS, 'El t&oacute;pico se ha creado correctamente.')
          return HttpResponseRedirect('/foros/' + categoria.nombre_limpio + '/' + str(topico.id) + '/')
        else:
          messages.add_message(request, messages.ERROR, 'Por favor llena todos los campos.')
      except:
        messages.add_message(request, messages.ERROR, 'Por favor llena todos los campos.')
    else:
      messages.add_message(request, messages.ERROR, 'Tienes que hacer login para crear un t&oacute;pico.')
      return HttpResponseRedirect('/login/')
  
  # Sacamos usuarios falsos
  if(request.user.is_staff):
    fake_users = User.objects.filter(email__icontains="davidjairala").order_by("username")
  else:
    fake_users = None
  
  return direct_to_template(request, 'foros/nuevo_topico.html', {
    'categoria': categoria,
    'fake_users': fake_users,
  })
  

# Ver topico
def ver_topico(request, nombre_limpio, id):
  from django.contrib.auth.models import User
  
  try:
    pnum = int(request.GET['page'])
  except:
    pnum = 1
  
  perpage = 20
  
  categoria = Categoria.objects.filter(nombre_limpio=nombre_limpio)[0]
  topico = Topico.objects.get(pk=id)
  
  # Checamos si hay que crear respuesta
  if(request.user.is_authenticated() and request.POST):
    pmensaje = request.POST['mensaje']
    if(pmensaje != ''):
      if(request.user.is_staff and request.POST['fake_user'] != ""):
        mensaje_user = User.objects.get(pk=request.POST['fake_user'])
      else:
        mensaje_user = request.user
      nmensaje = Mensaje(user=mensaje_user, topico=topico, mensaje=pmensaje)
      nmensaje.save()
      
      messages.add_message(request, messages.SUCCESS, 'El mensaje se ha creado correctamente.')
    else:
      messages.add_message(request, messages.ERROR, 'Por favor introduce un mensaje para comentar sobre el tema.')
  
  mensajes = Mensaje.objects.filter(topico=topico).order_by('fecha')
  
  p = Paginator(mensajes, perpage)
  page = p.page(pnum)
  
  # Sacamos usuarios falsos
  if(request.user.is_staff):
    fake_users = User.objects.filter(email__icontains="davidjairala").order_by("username")
  else:
    fake_users = None
  
  return direct_to_template(request, 'foros/ver_topico.html', {
    'categoria':categoria,
    'topico':topico,
    'mensajes':page,
    'pnum':pnum,
    'fake_users':fake_users
  })

# Ver categoria
def ver_categoria(request, nombre_limpio):
  try:
    pnum = int(request.GET['page'])
  except:
    pnum = 1
  
  perpage = 20
  
  categoria = Categoria.objects.filter(nombre_limpio=nombre_limpio)[0]
  
  topicos = Topico.objects.filter(categoria=categoria).order_by('-id')
  
  p = Paginator(topicos, perpage)
  page = p.page(pnum)
  
  return direct_to_template(request, 'foros/ver_categoria.html', {
    'categoria':categoria,
    'topicos':page,
    'pnum':pnum
  })

# Portada
def index(request):
  categorias = Categoria.objects.all().order_by('nombre')
  
  return direct_to_template(request, 'foros/index.html', {
    'categorias':categorias
  })
