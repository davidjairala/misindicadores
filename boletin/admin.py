from django.contrib import admin
from misindicadores.boletin.models import *

class BoletinAdmin(admin.ModelAdmin):
  model = Boletin
  raw_id_fields = (
    "user",
  )

admin.site.register(Boletin, BoletinAdmin)