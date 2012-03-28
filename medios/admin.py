from django.contrib import admin
from misindicadores.medios.models import *

class ArticuloAdmin(admin.ModelAdmin):
  model = Articulo
  raw_id_fields = (
    "padre",
  )

admin.site.register(Rss)
admin.site.register(RssLast)
admin.site.register(Articulo, ArticuloAdmin)
