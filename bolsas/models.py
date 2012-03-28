from django.db import models

class Bmv(models.Model):
  emisora = models.CharField(max_length=255)
  serie = models.CharField(max_length=255)
  fecha = models.DateField()
  hora = models.CharField(max_length=255)
  ultimo = models.FloatField()
  ppp = models.FloatField()
  anterior = models.FloatField()
  maximo = models.FloatField()
  minimo = models.FloatField()
  volumen = models.FloatField()
  importe = models.FloatField()
  ops = models.FloatField()
  puntos = models.FloatField()
  porcentaje = models.FloatField()
  tendencia = models.FloatField(null=True, blank=True)
  tendencia_relativa = models.FloatField(null=True, blank=True)
  tendencia_relativa_acumulada = models.FloatField(null=True, blank=True)
  cambio_promedio = models.FloatField(null=True, blank=True)
  prediccion_lineal = models.FloatField(null=True, blank=True)
  error_promedio = models.FloatField(null=True, blank=True)
  
  def __unicode__(self):
    return "%s - %s : %s : %s" % (self.emisora, self.serie, str(self.fecha), str(self.ultimo))
  
  def get_emisora_slug(self):
    from django.template.defaultfilters import iriencode

    slug = iriencode(self.emisora.lower())
    return slug

  def get_link(self):
    return "/bolsas/bmv/emisora/%s/" % self.get_emisora_slug()

  def get_emisora_link(self):
    link = self.get_link()
    return '<a href="%s">%s</a>' % (link, self.emisora)

  def get_tendencia(self):
    if(self.tendencia > 0):
      return "Alza"
    elif(self.tendencia < 0):
      return "Baja"
    else:
      return "Mantiene"

  def get_tendencia_color(self):
    if(self.tendencia > 0):
      return "green"
    elif(self.tendencia < 0):
      return "red"
    else:
      return "black"
  
  def get_porcentaje_color(self):
    if(self.porcentaje > 0):
      return "green"
    elif(self.porcentaje < 0):
      return "red"
    else:
      return "black"

class BmvDia(models.Model):
  emisora = models.CharField(max_length=255)
  serie = models.CharField(max_length=255)
  fecha = models.DateField()
  hora = models.CharField(max_length=255)
  ultimo = models.FloatField()
  ppp = models.FloatField()
  anterior = models.FloatField()
  maximo = models.FloatField()
  minimo = models.FloatField()
  volumen = models.FloatField()
  importe = models.FloatField()
  ops = models.FloatField()
  puntos = models.FloatField()
  porcentaje = models.FloatField()
  tendencia = models.FloatField(null=True, blank=True)
  tendencia_relativa = models.FloatField(null=True, blank=True)
  tendencia_relativa_acumulada = models.FloatField(null=True, blank=True)
  cambio_promedio = models.FloatField(null=True, blank=True)
  prediccion_lineal = models.FloatField(null=True, blank=True)
  error_promedio = models.FloatField(null=True, blank=True)

  def __unicode__(self):
    return "%s - %s : %s : %s" % (self.emisora, self.serie, str(self.fecha), str(self.ultimo))
  
  def get_emisora_slug(self):
    from django.template.defaultfilters import iriencode

    slug = iriencode(self.emisora.lower())
    return slug

  def get_link(self):
    return "/bolsas/bmv/emisora/%s/" % self.get_emisora_slug()

  def get_emisora_link(self):
    link = self.get_link()
    return '<a href="%s">%s</a>' % (link, self.emisora)
  
  def get_tendencia(self):
    if(self.tendencia > 0):
      return "Alza"
    elif(self.tendencia < 0):
      return "Baja"
    else:
      return "Mantiene"
  
  def get_tendencia_color(self):
    if(self.tendencia > 0):
      return "green"
    elif(self.tendencia < 0):
      return "red"
    else:
      return "black"
  
  def get_porcentaje_color(self):
    if(self.porcentaje > 0):
      return "green"
    elif(self.porcentaje < 0):
      return "red"
    else:
      return "black"

class BmvIpc(models.Model):
  fecha = models.DateField()
  hora = models.CharField(max_length=255)
  valor = models.FloatField()
  
  def __unicode__(self):
    return "%s - %s : %s" % (str(self.fecha), self.hora, str(self.valor))
  
  def dif_dia(self):
    try:
      anterior = BmvIpcDia.objects.filter(fecha__lt=self.fecha).order_by('-fecha')[0]
      
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
      anterior = BmvIpcDia.objects.filter(fecha__lte=fecha_ant).order_by('-fecha')[0]

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
      anterior = BmvIpcDia.objects.filter(fecha__lte=fecha_ant).order_by('-fecha')[0]

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

class BmvIpcDia(models.Model):
  fecha = models.DateField()
  hora = models.CharField(max_length=255)
  valor = models.FloatField()

  def __unicode__(self):
    return "%s - %s : %s" % (str(self.fecha), self.hora, str(self.valor))
  
  def dif_dia(self):
    try:
      anterior = BmvIpcDia.objects.filter(fecha__lt=self.fecha).order_by('-fecha')[0]

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
      anterior = BmvIpcDia.objects.filter(fecha__lte=fecha_ant).order_by('-fecha')[0]

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
      anterior = BmvIpcDia.objects.filter(fecha__lte=fecha_ant).order_by('-fecha')[0]

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

class Dow(models.Model):
  fecha = models.DateField()
  valor = models.FloatField()
  alto = models.FloatField()
  bajo = models.FloatField()
  cierre = models.FloatField()
  volumen = models.FloatField()
  
  def __unicode__(self):
    return "%s - %s" % (str(self.fecha), str(self.cierre))

class Nasdaq(models.Model):
  fecha = models.DateField()
  valor = models.FloatField()
  alto = models.FloatField()
  bajo = models.FloatField()
  cierre = models.FloatField()

  def __unicode__(self):
    return "%s - %s" % (str(self.fecha), str(self.cierre))

class Sp500(models.Model):
  fecha = models.DateField()
  valor = models.FloatField()
  alto = models.FloatField()
  bajo = models.FloatField()
  cierre = models.FloatField()

  def __unicode__(self):
    return "%s - %s" % (str(self.fecha), str(self.cierre))

class Nikkei(models.Model):
  fecha = models.DateField()
  valor = models.FloatField()
  alto = models.FloatField()
  bajo = models.FloatField()
  cierre = models.FloatField()

  def __unicode__(self):
    return "%s - %s" % (str(self.fecha), str(self.cierre))

class Bovespa(models.Model):
  fecha = models.DateField(auto_now_add=True)
  valor = models.FloatField()

  def __unicode__(self):
    return "%s - %s" % (str(self.fecha), str(self.valor))

class Ipsa(models.Model):
  fecha = models.DateField(auto_now_add=True)
  valor = models.FloatField()

  def __unicode__(self):
    return "%s - %s" % (str(self.fecha), str(self.valor))

class Merval(models.Model):
  fecha = models.DateField(auto_now_add=True)
  valor = models.FloatField()

  def __unicode__(self):
    return "%s - %s" % (str(self.fecha), str(self.valor))

class Bvg(models.Model):
  fecha = models.DateField(auto_now_add=True)
  bvg = models.FloatField()
  ipecu = models.FloatField()

  def __unicode__(self):
    return "%s - %s" % (str(self.fecha), str(self.valor))

class Igbvl(models.Model):
  fecha = models.DateField(auto_now_add=True)
  valor = models.FloatField()

  def __unicode__(self):
    return "%s - %s" % (str(self.fecha), str(self.valor))

class Colcap(models.Model):
  fecha = models.DateField(auto_now_add=True)
  colcap = models.FloatField()
  col20 = models.FloatField()
  igbc = models.FloatField()

  def __unicode__(self):
    return "%s - %s" % (str(self.fecha), str(self.colcap))

class Ibc(models.Model):
  fecha = models.DateField(auto_now_add=True)
  ibc = models.FloatField()

  def __unicode__(self):
    return "%s - %s" % (str(self.fecha), str(self.ibc))
