from django.contrib import admin
from misindicadores.foros.models import *
from django.contrib import admin

class TopicoAdmin(admin.ModelAdmin):
  model = Topico
  raw_id_fields = (
    "user",
  )

class MensajeAdmin(admin.ModelAdmin):
  model = Mensaje
  raw_id_fields = (
    "user",
    "topico",
  )

admin.site.register(Categoria)
admin.site.register(Topico, TopicoAdmin)
admin.site.register(Mensaje, MensajeAdmin)