from django.db import models

class Inpc(models.Model):
  fecha = models.DateField()
  valor = models.FloatField()
  
  def __unicode__(self):
    return str(self.fecha) + " : " + str(self.valor)
  
  def get_inflacion(self):
    if(self.valor > 0):
      year_ini = self.fecha.year - 1
      fecha_ini = "%s-12-01" % year_ini
      
      try:
        inpc_ini = Inpc.objects.get(fecha=fecha_ini)
        
        inflacion = ((self.valor / inpc_ini.valor) - 1) * 100
        
        return inflacion
      except:
        pass
    
    return 0

class Cpi(models.Model):
  fecha = models.DateField()
  valor = models.FloatField()
  
  def __unicode__(self):
    return str(self.fecha) + " : " + str(self.valor)

class Udis(models.Model):
  fecha = models.DateField()
  valor = models.FloatField()
  
  def __unicode__(self):
    return str(self.fecha) + " : " + str(self.valor)
