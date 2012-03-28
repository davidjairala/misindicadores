from django.db import models
from django.utils.encoding import smart_unicode
from django.contrib.auth.models import User
from misindicadores.globals.functions import *

class Boletin(models.Model):
  user = models.ForeignKey(User)
  activo = models.BooleanField()
  periocidad = models.CharField(max_length=255)
  dia = models.CharField(max_length=255)
  hora = models.IntegerField()
  
  def __unicode__(self):
    return smart_unicode(self.user.username) + " : " + self.periocidad
  
  def get_dias(self):
    return get_dias_ing()
  
  def get_rand_dia(self):
    import random
    
    return self.get_dias()[random.randint(0, 6)]
  
  def get_rand_hora(self):
    import random
    
    return random.randint(8, 17)
  
  def get_horas(self):
    return range(0, 24)