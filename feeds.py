from django.contrib.syndication.views import Feed
from misindicadores.articulos.models import Articulo
from misindicadores.globals.functions import unescape

class UltimasNoticias(Feed):
  title = unescape("Mis Indicadores - &Uacute;ltimas noticias, notas y art&iacute;culos")
  link = "/"
  description = unescape("Actualizaciones, noticias, &uacute;ltimas notas y art&iacute;culos en Mis Indicadores")

  def items(self):
    return Articulo.objects.order_by('-id')[:20]