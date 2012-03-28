from django.db import models
from django.utils.encoding import smart_unicode

class Rss(models.Model):
  titulo = models.CharField(max_length=255)
  url = models.CharField(max_length=500)
  
  def __unicode__(self):
    return smart_unicode(self.titulo)

class RssLast(models.Model):
  rss = models.ForeignKey(Rss)
  
  def __unicode__(self):
    return smart_unicode(self.rss.titulo)

class Articulo(models.Model):
  rss = models.ForeignKey(Rss)
  padre = models.ForeignKey('self', blank=True, null=True)
  titulo = models.CharField(max_length=500)
  url = models.CharField(max_length=500)
  descripcion = models.TextField()
  vistas = models.IntegerField()
  puntos = models.IntegerField()
  fecha = models.DateField(auto_now_add=True)
  fecha_added = models.DateTimeField(auto_now_add=True)
  
  def __unicode__(self):
    return smart_unicode(self.titulo) + " : " + str(self.fecha)
  
  def linked_title(self):
    return '<a href="%s" target="_blank">%s</a>' % (self.url, self.titulo)
  
  def read_more_link(self):
    return '<a href="%s" target="_blank">%s</a>' % (self.url, "leer m&aacute;s")
  
  def has_hijos(self):
    try:
      hijo = Articulo.objects.filter(padre=self.id)[0]
      
      return True
    except:
      return False
  
  def hijos(self):
    try:
      hijos = Articulo.objects.filter(padre=self.id).order_by('id')
      
      return hijos
    except:
      pass
