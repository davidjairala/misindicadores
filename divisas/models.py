from django.db import models

class Dolar(models.Model):
  fecha = models.DateField()
  valor = models.FloatField()
  bancomer_compra = models.FloatField(null=True, blank=True)
  bancomer_venta = models.FloatField(null=True, blank=True)
  banorte_compra = models.FloatField(null=True, blank=True)
  banorte_venta = models.FloatField(null=True, blank=True)
  banamex_compra = models.FloatField(null=True, blank=True)
  banamex_venta = models.FloatField(null=True, blank=True)
  santander_compra = models.FloatField(null=True, blank=True)
  santander_venta = models.FloatField(null=True, blank=True)
  ixe_compra = models.FloatField(null=True, blank=True)
  ixe_venta = models.FloatField(null=True, blank=True)
  promedio_compra = models.FloatField(null=True, blank=True)
  promedio_venta = models.FloatField(null=True, blank=True)
  
  def __unicode__(self):
    return str(self.fecha) + ' : ' + str(self.valor)

class Euro(models.Model):
  fecha = models.DateField()
  valor = models.FloatField()
  bancomer_compra = models.FloatField(null=True, blank=True)
  bancomer_venta = models.FloatField(null=True, blank=True)
  banorte_compra = models.FloatField(null=True, blank=True)
  banorte_venta = models.FloatField(null=True, blank=True)
  banamex_compra = models.FloatField(null=True, blank=True)
  banamex_venta = models.FloatField(null=True, blank=True)
  santander_compra = models.FloatField(null=True, blank=True)
  santander_venta = models.FloatField(null=True, blank=True)
  promedio_compra = models.FloatField(null=True, blank=True)
  promedio_venta = models.FloatField(null=True, blank=True)
  
  def __unicode__(self):
    return str(self.fecha) + ' : ' + str(self.valor)

class Deg(models.Model):
  fecha = models.DateField()
  valor = models.FloatField()
  
  def __unicode__(self):
    return str(self.fecha) + ' : ' + str(self.valor)

class Libra(models.Model):
  fecha = models.DateField()
  valor = models.FloatField()
  
  def __unicode__(self):
    return str(self.fecha) + ' : ' + str(self.valor)

class Metal(models.Model):
  fecha = models.DateField()
  aluminio = models.FloatField()
  aluminio_ny = models.FloatField()
  cobre_alambron_ny = models.FloatField()
  platino_ny = models.FloatField()
  plomo = models.FloatField()
  zinc = models.FloatField()
  
  def __unicode__(self):
    return str(self.fecha) + ' : ' + str(self.aluminio)

class Oro(models.Model):
  fecha = models.DateField()
  azteca_compra = models.FloatField()
  azteca_venta = models.FloatField()
  centenario_compra = models.FloatField()
  centenario_venta = models.FloatField()
  hidalgo_compra = models.FloatField()
  hidalgo_venta = models.FloatField()
  oro_libertad_compra = models.FloatField()
  oro_libertad_venta = models.FloatField()
  
  def __unicode__(self):
    return str(self.fecha) + ' : ' + str(self.azteca_compra)

class Petroleo(models.Model):
  fecha = models.DateField()
  brent = models.FloatField()
  mezcla_mexicana = models.FloatField()
  wti = models.FloatField()
  
  def __unicode__(self):
    return str(self.fecha) + ' : ' + str(self.brent)

class Plata(models.Model):
  fecha = models.DateField()
  onza_troy_compra = models.FloatField()
  onza_troy_venta = models.FloatField()
  plata_libertad_compra = models.FloatField()
  plata_libertad_venta = models.FloatField()
  
  def __unicode__(self):
    return str(self.fecha) + ' : ' + str(self.onza_troy_compra)

class Yen(models.Model):
  fecha = models.DateField()
  valor = models.FloatField()
  
  def __unicode__(self):
    return str(self.fecha) + ' : ' + str(self.valor)
