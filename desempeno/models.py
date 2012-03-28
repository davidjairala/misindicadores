from django.db import models

class Desempleo(models.Model):
  year = models.IntegerField()
  month = models.IntegerField()
  total = models.FloatField()
  hombres = models.FloatField()
  mujeres = models.FloatField()
  
  def __unicode__(self):
    return str(year) + " : " + str(month) + " : " + str(total)
  
  def get_fecha(self):
    return "%s-%s-01" % (self.year, self.month)

class Pib(models.Model):
  year = models.IntegerField()
  trimestre = models.IntegerField()
  total = models.FloatField()
  primarias = models.FloatField()
  secundarias = models.FloatField()
  terciarias = models.FloatField()
  
  def __unicode__(self):
    return str(self.year) + " : " + str(self.trimestre) + " : " + str(self.total)
  
  def get_trimestre(self):
    if(self.trimestre == 1):
      trimestre = "I"
    elif(self.trimestre == 2):
      trimestre = "II"
    elif(self.trimestre == 3):
      trimestre = "III"
    elif(self.trimestre == 4):
      trimestre = "IV"
    return trimestre
  
  def get_fecha(self):
    return "%s - %s" % (self.year, self.get_trimestre())

class Reserva(models.Model):
  fecha = models.DateField()
  base_monetaria = models.FloatField()
  activos_internacionales_netos_pesos = models.FloatField()
  activos_internacionales_netos_dolares = models.FloatField()
  credito_interno_neto_pesos = models.FloatField()
  reserva_internacional_dolares = models.FloatField()
  base_monetaria_pesos = models.FloatField()
  activos_internacionales_netos_pesos_var = models.FloatField()
  activos_internacionales_netos_dolares_var = models.FloatField()
  credito_interno_neto_pesos_var = models.FloatField()
  
  def __unicode__(self):
    return str(fecha) + " : " + str(base_monetaria)

class Afore(models.Model):
  AFORE_TIPOS = (
    (5, u'5 - 26 y menores'),
    (4, u'4 - entre 27 y 36'),
    (3, u'3 - entre 37 y 45'),
    (2, u'2 - entre 46 y 55'),
    (1, u'1 - 56 y mayores'),
  )
  
  tipo = models.IntegerField(choices=AFORE_TIPOS)
  afore = models.CharField(max_length=255)
  rendimiento = models.FloatField()
  comision = models.FloatField()
  fecha = models.DateField(auto_now_add=True)
  
  def __unicode__(self):
    return str(self.tipo) + ' : ' + str(self.fecha) + ' : ' + self.afore
  
  class Meta:
    ordering = ['-rendimiento']