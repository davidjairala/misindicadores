from django.http import HttpResponseRedirect
from django.views.generic.simple import direct_to_template
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages
from random import Random
import string
from misindicadores.globals.functions import *
from django.conf import settings

# Resumen del dia
def resumen(request):
  from misindicadores.divisas.models import Dolar, Euro, Deg, Libra, Metal, Oro, Petroleo, Plata, Yen
  from misindicadores.bolsas.models import Bmv, BmvDia, BmvIpc, BmvIpcDia, Dow, Nasdaq, Sp500, Nikkei
  from misindicadores.inflacion.models import Inpc, Cpi, Udis
  from misindicadores.tasas.models import Cpp, Cetes, Tiie, Imi
  
  if(request.GET and request.GET['_d'] and request.GET['_m'] and request.GET['_y']):
    fecha = "%s-%s-%s" % (request.GET['_y'], request.GET['_m'], request.GET['_d'])
  else:
    last_dolar = Dolar.objects.all().order_by('-fecha')[0]
    fecha = last_dolar.fecha.strftime("%Y-%m-%d")
  
  dolar = Dolar.objects.filter(fecha__lte=fecha).order_by('-fecha')[0]
  
  euro = Euro.objects.filter(fecha__lte=fecha).order_by('-fecha')[0]
  deg = Deg.objects.filter(fecha__lte=fecha).order_by('-fecha')[0]
  libra = Libra.objects.filter(fecha__lte=fecha).order_by('-fecha')[0]
  yen = Yen.objects.filter(fecha__lte=fecha).order_by('-fecha')[0]
  petroleo = Petroleo.objects.filter(fecha__lte=fecha).order_by('-fecha')[0]
  
  bmv = BmvIpcDia.objects.filter(fecha__lte=fecha).order_by('-fecha')[0]
  dow = Dow.objects.filter(fecha__lte=fecha).order_by('-fecha')[0]
  nasdaq = Nasdaq.objects.filter(fecha__lte=fecha).order_by('-fecha')[0]
  sp500 = Sp500.objects.filter(fecha__lte=fecha).order_by('-fecha')[0]
  nikkei = Nikkei.objects.filter(fecha__lte=fecha).order_by('-fecha')[0]
  
  inpc = Inpc.objects.filter(fecha__lte=fecha).order_by('-fecha')[0]
  
  imi = Imi.objects.filter(fecha__lte=fecha).order_by('-fecha')[0]
  
  return direct_to_template(request, 'cuentas/resumen.html', {
    'cache_time':settings.CACHE_TIME,
    'fecha':fecha,
    'dolar':dolar,
    'euro':euro,
    'deg':deg,
    'libra':libra,
    'yen':yen,
    'petroleo':petroleo,
    'bmv':bmv,
    'dow':dow,
    'nasdaq':nasdaq,
    'sp500':sp500,
    'nikkei':nikkei,
    'inpc':inpc,
    'imi':imi,
  })

# Portada
def home(request):
  from django.core.paginator import Paginator
  from misindicadores.divisas.models import Dolar, Euro, Deg, Libra, Metal, Oro, Petroleo, Plata, Yen
  from misindicadores.bolsas.models import Bmv, BmvDia, BmvIpc, BmvIpcDia, Dow, Nasdaq, Sp500, Nikkei
  from misindicadores.inflacion.models import Inpc, Cpi, Udis
  from misindicadores.tasas.models import Cpp, Cetes, Tiie, Imi
  from misindicadores.medios.models import Articulo
  from misindicadores.articulos.models import Articulo as Noticia
  from misindicadores.foros.models import Topico, Mensaje
  
  perpage = 5
  
  dolar = Dolar.objects.all().order_by('-fecha')[0]
  
  fecha = dolar.fecha
  
  euro = Euro.objects.all().order_by('-fecha')[0]
  deg = Deg.objects.all().order_by('-fecha')[0]
  libra = Libra.objects.all().order_by('-fecha')[0]
  yen = Yen.objects.all().order_by('-fecha')[0]
  petroleo = Petroleo.objects.all().order_by('-fecha')[0]
  
  bmv = BmvIpcDia.objects.all().order_by('-fecha')[0]
  dow = Dow.objects.all().order_by('-fecha')[0]
  nasdaq = Nasdaq.objects.all().order_by('-fecha')[0]
  sp500 = Sp500.objects.all().order_by('-fecha')[0]
  nikkei = Nikkei.objects.all().order_by('-fecha')[0]
  
  inpc = Inpc.objects.all().order_by('-fecha')[0]
  
  imi = Imi.objects.all().order_by('-fecha')[0]
  
  articulos = Articulo.objects.filter(padre__isnull=True).order_by('-fecha', '-puntos', '-id')
  
  topicos = Topico.objects.all().order_by('-id')[:7]
  mensajes = Mensaje.objects.all().order_by('-id')[:5]
  
  p = Paginator(articulos, perpage)
  page = p.page(1)
  
  noticias = Noticia.objects.filter(categoria__nombre_limpio='blog').order_by('-id')[:5]
  notas = Noticia.objects.filter(categoria__nombre_limpio='notas').order_by('-id')[:5]
  
  return direct_to_template(request, 'cuentas/index.html', {
    'cache_time':settings.CACHE_TIME,
    'fecha':fecha,
    'dolar':dolar,
    'euro':euro,
    'deg':deg,
    'libra':libra,
    'yen':yen,
    'petroleo':petroleo,
    'bmv':bmv,
    'dow':dow,
    'nasdaq':nasdaq,
    'sp500':sp500,
    'nikkei':nikkei,
    'inpc':inpc,
    'imi':imi,
    'articulos':page,
    'noticias':noticias,
    'notas':notas,
    'topicos':topicos,
    'mensajes':mensajes,
  })

# Invita a un amigo
def invitar(request):
  from django.core.mail import mail_admins
  
  if(request.POST):
    try:
      nombre = request.POST['nombre']
      email = request.POST['email']
      nombre_amigo = request.POST['nombre_amigo']
      
      if(nombre != "" and email != "" and nombre_amigo != ""):
        send_mail('%s te ha invitado a conocer Mis Indicadores' % nombre, "Hola %s,\n\nTu amigo %s te ha invitado a conocer Mis Indicadores, el mejor y moderno portal de indicadores economicos y financieros de Mexico.\n\nPara visitarnos, sigue el enlace:\n\n%s\n\nEsperamos verte pronto en Mis Indicadores\nSaludos!" % (nombre_amigo, nombre, get_app_url()), 'info@misindicadores.com', [email], fail_silently=True)
      
        messages.add_message(request, messages.SUCCESS, 'Gracias por invitar a tu amigo.  Le hemos enviado un email para invitarlo a conocer Mis Indicadores.')
        return HttpResponseRedirect("/")
        
      else:
        messages.add_message(request, messages.ERROR, 'Por favor llena todos los campos.')
    except:
      messages.add_message(request, messages.ERROR, 'Ocurri&oacute; un error al intentar de enviar tu invitaci&oacute;n, por favor intenta nuevamente.')
  return direct_to_template(request, 'cuentas/invitar.html', {})

# Contacto
def contacto(request):
  from django.core.mail import mail_admins
  
  if(request.POST):
    try:
      nombre = request.POST['nombre']
      email = request.POST['email']
      comentarios = request.POST['comentarios']
      
      if(nombre != "" and email != "" and comentarios != ""):
        mail_admins('Mis Indicadores - Contacto', "Nombre: %s\nEmail: %s\n\nComentarios:\n%s" % (nombre, email, comentarios), fail_silently=True)
      
        messages.add_message(request, messages.SUCCESS, 'Gracias por contactarnos.  Nos pondremos en contacto contigo a la brevedad posible.')
        return HttpResponseRedirect("/")
      else:
        messages.add_message(request, messages.ERROR, 'Por favor llena todos los campos.')
    except:
      messages.add_message(request, messages.ERROR, 'Ocurri&oacute; un error al intentar de enviar tu forma de contacto, por favor intenta nuevamente.')
  return direct_to_template(request, 'cuentas/contacto.html', {})

# Indicadores
def indicadores(request):
  return direct_to_template(request, 'cuentas/indicadores.html', {})

# Hace logout
def logout_view(request):
  logout(request)
  return direct_to_template(request, 'cuentas/logout.html', {})

# Muestra forma de login
def login_view(request):
  try:
    next = request.GET['next']
  except:
    next = None
  
  return direct_to_template(request, 'cuentas/login.html', {
    "btn":"login",
    'next':next
  })

# Hace el login
def do_login(request):
  if(request.POST):
    username = request.POST['username']
    password = request.POST['clave']
    user = authenticate(username=username, password=password)
    if user is not None:
      if user.is_active:
        login(request, user)
        
        # Checamos si hay next
        try:
          next = request.POST['next']
          
          return HttpResponseRedirect(next)
        except:
          return direct_to_template(request, 'cuentas/logged.html', {})
      else:
        messages.add_message(request, messages.ERROR, 'Tu usuario ha sido deshabilitado por la administraci&oacute;n.')
        return HttpResponseRedirect("/login/")
    else:
      messages.add_message(request, messages.ERROR, 'Nombre de usuario o clave incorrectos.')
      return HttpResponseRedirect("/login/")
  else:
    return HttpResponseRedirect("/login/")

# Muestra forma para registrarse
def registrate(request):
  try:
    next = request.GET['next']
  except:
    next = None
  
  return direct_to_template(request, 'cuentas/registrate.html', {
    'next':next
  })

# Realiza el registro
def do_registro(request):
  from misindicadores.boletin.models import Boletin
  
  username = request.POST['username']
  password1 = request.POST['password1']
  password2 = request.POST['password2']
  email = request.POST['email']
  
  if(username and password1 and password2 and email):
    if(password1 == password2):
      try:
        new_user = User(username=username, email=email)
        new_user.set_password(password1)
        new_user.is_staff = False
        new_user.is_superuser = False
        new_user.save()
        
        # Guardamos boletin para el nuevo usuario
        new_boletin = Boletin(user=new_user, activo=True, periocidad='semanal')
        new_boletin.dia = new_boletin.get_rand_dia()
        new_boletin.hora = new_boletin.get_rand_hora()
        new_boletin.save()
        
        messages.add_message(request, messages.SUCCESS, 'Gracias por registrarte.  Ahora introduce tus datos para entrar:')
        
        try:
          next = '?next=' + request.POST['next']
        except:
          next = ''
        
        return HttpResponseRedirect("/login/%s" % next)
      except:
        messages.add_message(request, messages.ERROR, 'El nombre de usuario o email que elegiste ya esta ocupado, por favor selecciona otro.')
        return HttpResponseRedirect("/registrate/")
    else:
      messages.add_message(request, messages.ERROR, 'La clave y la confirmacion no coinciden.')
      return HttpResponseRedirect("/registrate/")
  else:
    messages.add_message(request, messages.ERROR, 'Por favor llena todos los campos.')
    return HttpResponseRedirect("/registrate/")

# Muestra forma para recuperar clave
def recover(request):
  return direct_to_template(request, 'cuentas/recover.html', {})

# Envia mail con instrucciones para recuperar clave
def do_recover(request):
  email = request.POST['email']
  if(email):
    # Checamos si existe un usuario con ese email
    user = User.objects.filter(email=email)[:1]
    user = user[0]
    if(user):
      # Enviamos mail
      subject = 'Mis Indicadores - Recuperar clave'
      msg = 'Estimado ' + user.username + ':\nHas solicitado recuperar tu clave, para hacerlo, pulsa el siguiente enlace:\n\nhttp://misindicadores.com/post_recover/' + str(user.id) + ':' + user.password + '\n\n(Si no has solicitado recuperar tu clave, haz caso omiso a este correo)\n\nSaludos,\nMis Indicadores\nhttp://misindicadores.com/'
      sfrom = 'info@misindicadores.com'
      send_mail(subject, msg, sfrom,[user.email], fail_silently=True)
      return direct_to_template(request, 'cuentas/do_recover.html', {})
    else:
      messages.add_message(request, messages.ERROR, 'El e-mail no esta ligado a ninguna cuenta en el sistema.')
      return HttpResponseRedirect('/recover/')
  else:
    messages.add_message(request, messages.ERROR, 'Por favor introduce tu e-mail.')
    return HttpResponseRedirect('/recover/')

# Realiza el proceso de reset de clave
def post_recover(request, shash):
  hash_arr = shash.split(':')
  user_id = hash_arr[0]
  pwd = hash_arr[1]
  users = User.objects.filter(password = pwd, id = user_id)
  new_pass = Random().sample(string.letters+string.digits, 6)
  new_pass = string.join(new_pass, '')
  if(users):
    for user in users:
      user.set_password(new_pass)
      user.save()
    return direct_to_template(request, 'cuentas/post_recover.html', {"new_pass":new_pass})
  else:
    messages.add_message(request, messages.ERROR, 'La liga que has introducido no es valida, por favor intenta nuevamente.')
    return HttpResponseRedirect('/recover/')

# Muestra forma para cambiar clave
def chngpwd(request):
  return direct_to_template(request, 'cuentas/chngpwd.html', {})

# Cambia clave para un usuario
def do_chngpwd(request):
  curr_pwd = request.POST['curr_pwd']
  new_pwd = request.POST['new_pwd']
  new_pwd2 = request.POST['new_pwd2']
  user_id = request.user.id
  if(curr_pwd and new_pwd and new_pwd2):
    # Buscamos al usuario con los datos introducidos
    user = User.objects.get(id=user_id)
    if(user):
      if(new_pwd == new_pwd2):
        user.set_password(new_pwd)
        user.save()
        return direct_to_template(request, 'cuentas/do_chngpwd.html', {"new_pwd":new_pwd})
      else:
        messages.add_message(request, messages.ERROR, 'La nueva clave y su confirmacion no son iguales.')
        return HttpResponseRedirect('/chngpwd/')
    else:
      messages.add_message(request, messages.ERROR, 'No encontramos un usuario con los datos especificados.')
      return HttpResponseRedirect('/chngpwd/')
  else:
    messages.add_message(request, messages.ERROR, 'Por favor introduce todos los campos.')
    return HttpResponseRedirect('/chngpwd/')

# Pagina about
def about(request):
  return direct_to_template(request, 'cuentas/about.html', {})

# Pagina de ayuda
def ayuda(request):
  return direct_to_template(request, 'cuentas/ayuda.html', {})
