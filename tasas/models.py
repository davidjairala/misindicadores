from django.db import models

class Cpp(models.Model):
  fecha = models.DateField()
  pesos = models.FloatField()
  udis = models.FloatField()
  dolares = models.FloatField()
  promedio = models.FloatField()
  ti_pesos = models.FloatField()
  
  def __unicode__(self):
    return str(self.fecha) + " : " + str(self.promedio)

class Cetes(models.Model):
  fecha = models.DateField()
  plazo = models.IntegerField()
  solicitado = models.FloatField()
  colocado = models.FloatField()
  actual = models.FloatField()
  variacion = models.FloatField()
  
  def __unicode__(self):
    return str(self.fecha) + " : " + str(self.plazo) + " : " + str(self.actual)

class Tiie(models.Model):
  fecha = models.DateField()
  plazo = models.IntegerField()
  postura = models.FloatField()
  monto = models.FloatField()
  participante = models.CharField(max_length=255)
  
  def __unicode__(self):
    return str(self.fecha) + " : " + str(self.plazo) + " : " + str(self.participante) + " : " + str(self.postura)

class Imi(models.Model):
  fecha = models.DateField()
  valor = models.FloatField()
  
  def __unicode__(self):
    return str(self.fecha) + " : " + str(self.valor)
  
  def dif_dia(self):
    try:
      anterior = Imi.objects.filter(fecha__lt=self.fecha).order_by('-fecha')[0]
      
      dif = 100 - ((100 * self.valor) / anterior.valor)
      dif *= -1
      
      return dif
    except:
      return 0
  
  def dif_dia_color(self):
    dif = self.dif_dia()
    
    if(dif > 0):
      return "green"
    elif(dif < 0):
      return "red"
    else:
      return "black"
  
  def dif_semana(self):
    from datetime import datetime, timedelta
    
    try:
      fecha_ant = self.fecha - timedelta(days=7)
      anterior = Imi.objects.filter(fecha__lte=fecha_ant).order_by('-fecha')[0]

      dif = 100 - ((100 * self.valor) / anterior.valor)
      dif *= -1

      return dif
    except:
      return 0
  
  def dif_semana_color(self):
    dif = self.dif_semana()

    if(dif > 0):
      return "green"
    elif(dif < 0):
      return "red"
    else:
      return "black"
  
  def dif_mes(self):
    from datetime import datetime, timedelta

    try:
      fecha_ant = self.fecha - timedelta(days=30)
      anterior = Imi.objects.filter(fecha__lte=fecha_ant).order_by('-fecha')[0]

      dif = 100 - ((100 * self.valor) / anterior.valor)
      dif *= -1

      return dif
    except:
      return 0
  
  def dif_mes_color(self):
    dif = self.dif_mes()

    if(dif > 0):
      return "green"
    elif(dif < 0):
      return "red"
    else:
      return "black"