from django.db import models
from django.utils.encoding import smart_unicode

class Categoria(models.Model):
  nombre = models.CharField(max_length=255)
  nombre_limpio = models.CharField(max_length=255)
  
  def __unicode__(self):
    return smart_unicode(self.nombre)

class Articulo(models.Model):
  categoria = models.ForeignKey(Categoria)
  titulo = models.CharField(max_length=255)
  contenido = models.TextField()
  fecha = models.DateField(auto_now_add=True)
  
  def __unicode__(self):
    return smart_unicode(self.categoria.nombre) + " : " + smart_unicode(self.titulo)
  
  def excerpt_no_link(self):
    from misindicadores.globals.functions import strip_tags, strip_tabs, get_first_parragraph
    
    contenido = get_first_parragraph(strip_tabs(strip_tags(smart_unicode(self.contenido))))
    
    return '%(contenido)s...' % {
      'contenido': contenido,
    }
  
  def excerpt(self):
    contenido = self.excerpt_no_link()
    
    return '%(contenido)s (<a href="/articulos/%(cat)s/%(id)s/">leer m&aacute;s</a>)' % {
      'contenido': contenido,
      'cat': smart_unicode(self.categoria.nombre_limpio),
      'id': str(self.id),
    }
  
  def get_absolute_url(self):
    return "/articulos/%(cat)s/%(id)s/" % {
      'cat': self.categoria.nombre_limpio,
      'id': str(self.id),
    }

class AlreadyTwitted(models.Model):
  articulo = models.ForeignKey(Articulo)
  
  def __unicode__(self):
    return smart_unicode(self.articulo.categoria.nombre) + " : " + smart_unicode(self.articulo.titulo)