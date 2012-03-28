from django.db import models
from django.utils.encoding import smart_unicode
from django.contrib.auth.models import User
from misindicadores.globals.functions import *

class Categoria(models.Model):
  nombre = models.CharField(max_length=255)
  nombre_limpio = models.CharField(max_length=255)
  descripcion = models.TextField()
  
  def __unicode__(self):
    return smart_unicode(self.nombre)

class Topico(models.Model):
  user = models.ForeignKey(User)
  categoria = models.ForeignKey(Categoria)
  titulo = models.CharField(max_length=500)
  fecha = models.DateTimeField(auto_now_add=True)
  
  def __unicode__(self):
    return smart_unicode(self.categoria.nombre) + " : " + smart_unicode(self.titulo)

class Mensaje(models.Model):
  user = models.ForeignKey(User)
  topico = models.ForeignKey(Topico, related_name='mensaje_topico')
  mensaje = models.TextField()
  fecha = models.DateTimeField(auto_now_add=True)
  
  def __unicode__(self):
    return smart_unicode(self.topico.categoria.nombre) + " : " + smart_unicode(self.topico.titulo) + " : " + smart_unicode(self.mensaje)
  
  def format_date(self):
    from django.utils import dateformat
    
    dformat = 'r'
    
    return dateformat.format(self.fecha, dformat)[:-9]
  
  def excerpt(self):
    if(len(self.mensaje) > 100):
      ending = '...'
    else:
      ending = ''
    
    return '%(mensaje)s %(ending)s (<a href="/foros/%(cat)s/%(topico_id)s/">leer m&aacute;s</a>)' % {
      'mensaje': self.mensaje[:100],
      'ending': ending,
      'cat': self.topico.categoria.nombre_limpio,
      'topico_id': str(self.topico.id),
    }