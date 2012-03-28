from misindicadores.divisas.models import *
from misindicadores.bolsas.models import *
from misindicadores.inflacion.models import *
from misindicadores.tasas.models import *
from misindicadores.desempeno.models import *
from misindicadores.globals.functions import *

def get_valores_boletin(fecha):
  dolar = Dolar.objects.filter(fecha__lte=fecha).order_by('-fecha')[0]
  euro = Euro.objects.filter(fecha__lte=fecha).order_by('-fecha')[0]
  deg = Deg.objects.filter(fecha__lte=fecha).order_by('-fecha')[0]
  libra = Libra.objects.filter(fecha__lte=fecha).order_by('-fecha')[0]
  metal = Metal.objects.filter(fecha__lte=fecha).order_by('-fecha')[0]
  oro = Oro.objects.filter(fecha__lte=fecha).order_by('-fecha')[0]
  petroleo = Petroleo.objects.filter(fecha__lte=fecha).order_by('-fecha')[0]
  plata = Plata.objects.filter(fecha__lte=fecha).order_by('-fecha')[0]
  yen = Yen.objects.filter(fecha__lte=fecha).order_by('-fecha')[0]
  
  bmv = BmvIpcDia.objects.filter(fecha__lte=fecha).order_by('-fecha')[0]
  dow = Dow.objects.filter(fecha__lte=fecha).order_by('-fecha')[0]
  sp500 = Sp500.objects.filter(fecha__lte=fecha).order_by('-fecha')[0]
  nikkei = Nikkei.objects.filter(fecha__lte=fecha).order_by('-fecha')[0]
  
  inpc = Inpc.objects.filter(fecha__lte=fecha).order_by('-fecha')[0]
  cpi = Cpi.objects.filter(fecha__lte=fecha).order_by('-fecha')[0]
  udis = Udis.objects.filter(fecha__lte=fecha).order_by('-fecha')[0]
  
  imi = Imi.objects.filter(fecha__lte=fecha).order_by('-fecha')[0]
  cpp = Cpp.objects.filter(fecha__lte=fecha).order_by('-fecha')[0]
  
  last_cete = Cetes.objects.all().order_by('-fecha')[0]
  cetes = Cetes.objects.filter(fecha=last_cete.fecha).order_by('plazo')
  
  last_tiie = Tiie.objects.all().order_by('-fecha')[0]
  tiies = Tiie.objects.filter(fecha=last_tiie.fecha).order_by('plazo')
  
  valores_tiie_28 = []
  valores_tiie_91 = []
  
  for tiie in tiies:
    if(tiie.plazo == 28):
      valores_tiie_28.append(tiie.postura)
    else:
      valores_tiie_91.append(tiie.postura)
  
  tiie_28_promedio = get_promedio(valores_tiie_28)
  tiie_91_promedio = get_promedio(valores_tiie_91)
  
  desempleo = Desempleo.objects.all().order_by('-year', '-month')[0]
  pib = Pib.objects.all().order_by('-year', '-trimestre')[0]
  reserva = Reserva.objects.filter(fecha__lte=fecha).order_by('-fecha')[0]
  
  return {
    'dolar':dolar,
    'euro':euro,
    'deg':deg,
    'libra':libra,
    'metal':metal,
    'oro':oro,
    'petroleo':petroleo,
    'plata':plata,
    'yen':yen,
    'bmv':bmv,
    'dow':dow,
    'sp500':sp500,
    'nikkei':nikkei,
    'inpc':inpc,
    'cpi':cpi,
    'udis':udis,
    'imi':imi,
    'cpp':cpp,
    'cetes':cetes,
    'tiie_28_promedio':tiie_28_promedio,
    'tiie_91_promedio':tiie_91_promedio,
    'desempleo':desempleo,
    'pib':pib,
    'reserva':reserva,
  }

def get_boletin_html(fecha):
  valores = get_valores_boletin(fecha)
  
  html = simple_header()
  
  html += '<h1>\
    Bolet&iacute;n de <a href="' + get_app_url() + '">Mis Indicadores</a>: \
    ' + doDate(fecha) + '\
  </h1>\
  \
  <div class="hr"><!-- i --></div>\
  \
  <h2>\
    <a href="' + get_app_url() + 'divisas/dolar/">D&oacute;lar</a>\
  </h2>\
  \
  <table>\
    <tr>\
      <th class="bordered_right"><!-- i --></th>\
      <th class="bordered_right">\
        FIX\
      </th>\
      <th class="bordered_right">\
        Promedio\
      </th>\
      <th class="bordered_right">\
        Bancomer\
      </th>\
      <th class="bordered_right">\
        Banorte\
      </th>\
      <th class="bordered_right">\
        Banamex\
      </th>\
      <th class="bordered_right">\
        Santander\
      </th>\
      <th class="bordered_right">\
        IXE\
      </th>\
    </tr>\
    <tr class="bordered_bottom">\
      <td class="bordered_right">\
        Compra\
      </td>\
      <td class="numero bordered_right">\
      ' + dinero(valores['dolar'].valor) + '\
      </td>\
      <td class="numero bordered_right">\
        ' + dinero(valores['dolar'].promedio_compra) + '\
      </td>\
      <td class="numero bordered_right">\
        ' + dinero(valores['dolar'].bancomer_compra) + '\
      </td>\
      <td class="numero bordered_right">\
        ' + dinero(valores['dolar'].banorte_compra) + '\
      </td>\
      <td class="numero bordered_right">\
        ' + dinero(valores['dolar'].banamex_compra) + '\
      </td>\
      <td class="numero bordered_right">\
        ' + dinero(valores['dolar'].santander_compra) + '\
      </td>\
      <td class="numero bordered_right">\
        ' + dinero(valores['dolar'].ixe_compra) + '\
      </td>\
    </tr>\
    <tr>\
      <td class="bordered_right">\
        Venta\
      </td>\
      <td class="numero bordered_right">\
        N/A\
      </td>\
      <td class="numero bordered_right">\
        ' + dinero(valores['dolar'].promedio_venta) + '\
      </td>\
      <td class="numero bordered_right">\
        ' + dinero(valores['dolar'].bancomer_venta) + '\
      </td>\
      <td class="numero bordered_right">\
        ' + dinero(valores['dolar'].banorte_venta) + '\
      </td>\
      <td class="numero bordered_right">\
        ' + dinero(valores['dolar'].banamex_venta) + '\
      </td>\
      <td class="numero bordered_right">\
        ' + dinero(valores['dolar'].santander_venta) + '\
      </td>\
      <td class="numero bordered_right">\
        ' + dinero(valores['dolar'].ixe_venta) + '\
      </td>\
    </tr>\
  </table>\
  \
  <div class="hr"><!-- i --></div>\
  \
  <h2>\
    <a href="' + get_app_url() + 'divisas/euro/">Euro</a>\
  </h2>\
  \
  <table>\
    <tr>\
      <th class="bordered_right"><!-- i --></th>\
      <th class="bordered_right">\
        FIX\
      </th>\
      <th class="bordered_right">\
        Promedio\
      </th>\
      <th class="bordered_right">\
        Bancomer\
      </th>\
      <th class="bordered_right">\
        Banorte\
      </th>\
      <th class="bordered_right">\
        Banamex\
      </th>\
      <th class="bordered_right">\
        Santander\
      </th>\
    </tr>\
    <tr class="bordered_bottom">\
      <td class="bordered_right">\
        Compra\
      </td>\
      <td class="numero bordered_right">\
        ' + dinero(valores['euro'].valor) + '\
      </td>\
      <td class="numero bordered_right">\
        ' + dinero(valores['euro'].promedio_compra) + '\
      </td>\
      <td class="numero bordered_right">\
        ' + dinero(valores['euro'].bancomer_compra) + '\
      </td>\
      <td class="numero bordered_right">\
        ' + dinero(valores['euro'].banorte_compra) + '\
      </td>\
      <td class="numero bordered_right">\
        ' + dinero(valores['euro'].banamex_compra) + '\
      </td>\
      <td class="numero bordered_right">\
        ' + dinero(valores['euro'].santander_compra) + '\
      </td>\
    </tr>\
    <tr>\
      <td class="bordered_right">\
        Venta\
      </td>\
      <td class="numero bordered_right">\
        N/A\
      </td>\
      <td class="numero bordered_right">\
        ' + dinero(valores['euro'].promedio_venta) + '\
      </td>\
      <td class="numero bordered_right">\
        ' + dinero(valores['euro'].bancomer_venta) + '\
      </td>\
      <td class="numero bordered_right">\
        ' + dinero(valores['euro'].banorte_venta) + '\
      </td>\
      <td class="numero bordered_right">\
        ' + dinero(valores['euro'].banamex_venta) + '\
      </td>\
      <td class="numero bordered_right">\
        ' + dinero(valores['euro'].santander_venta) + '\
      </td>\
    </tr>\
  </table>\
  \
  <div class="hr"><!-- i --></div>\
  \
  <table>\
    <tr>\
      <td>\
        <h2>\
          <a href="' + get_app_url() + 'divisas/deg/">DEG</a>\
        </h2>\
        <p>\
          ' + dinero(valores['deg'].valor) + '\
        </p>\
      </td>\
      <td>\
        &nbsp;\
      </td>\
      <td>\
        <h2>\
          <a href="' + get_app_url() + 'divisas/libra/">Libra</a>\
        </h2>\
        <p>\
          ' + dinero(valores['libra'].valor) + '\
        </p>\
      </td>\
      <td>\
        &nbsp;\
      </td>\
      <td>\
        <h2>\
          <a href="' + get_app_url() + 'divisas/yen/">Yen</a>\
        </h2>\
        <p>\
          ' + dinero(valores['yen'].valor, 4) + '\
        </p>\
      </td>\
    </tr>\
  </table>\
  \
  <div class="hr"><!-- i --></div>\
  \
  <h2>\
    <a href="' + get_app_url() + 'divisas/metales/">Metales</a>\
  </h2>\
  \
  <table>\
    <tr>\
      <th class="bordered_right">\
        Aluminio\
      </th>\
      <th class="bordered_right">\
        Aluminio NY\
      </th>\
      <th class="bordered_right">\
        Cobre alambr&oacute;n NY\
      </th>\
      <th class="bordered_right">\
        Platino NY\
      </th>\
      <th class="bordered_right">\
        Plomo\
      </th>\
      <th class="bordered_right">\
        Zinc\
      </th>\
    </tr>\
    <tr class="bordered_bottom">\
      <td class="bordered_right numero">\
        ' + dinero(valores['metal'].aluminio) + '\
      </td>\
      <td class="bordered_right numero">\
        ' + dinero(valores['metal'].aluminio_ny) + '\
      </td>\
      <td class="bordered_right numero">\
        ' + dinero(valores['metal'].cobre_alambron_ny) + '\
      </td>\
      <td class="bordered_right numero">\
        ' + dinero(valores['metal'].platino_ny) + '\
      </td>\
      <td class="bordered_right numero">\
        ' + dinero(valores['metal'].plomo) + '\
      </td>\
      <td class="bordered_right numero">\
        ' + dinero(valores['metal'].zinc) + '\
      </td>\
    </tr>\
  </table>\
  \
  <div class="hr"><!-- i --></div>\
  \
  <h2>\
    <a href="' + get_app_url() + 'divisas/oro/">Oro</a>\
  </h2>\
  \
  <table>\
    <tr class="bordered_bottom">\
      <th class="bordered_right">\
        <!-- i -->\
      </th>\
      <th class="bordered_right">\
        Azteca\
      </th>\
      <th class="bordered_right">\
        Centenario\
      </th>\
      <th class="bordered_right">\
        Hidalgo\
      </th>\
      <th class="bordered_right">\
        Oro libertad\
      </th>\
    </tr>\
    <tr class="bordered_bottom">\
      <td class="bordered_right">\
        Compra\
      </td>\
      <td class="bordered_right numero">\
        ' + dinero(valores['oro'].azteca_compra) + '\
      </td>\
      <td class="bordered_right numero">\
        ' + dinero(valores['oro'].centenario_compra) + '\
      </td>\
      <td class="bordered_right numero">\
        ' + dinero(valores['oro'].hidalgo_compra) + '\
      </td>\
      <td class="bordered_right numero">\
        ' + dinero(valores['oro'].oro_libertad_compra) + '\
      </td>\
    </tr>\
    <tr class="bordered_bottom">\
      <td class="bordered_right">\
        Venta\
      </td>\
      <td class="bordered_right numero">\
        ' + dinero(valores['oro'].azteca_venta) + '\
      </td>\
      <td class="bordered_right numero">\
        ' + dinero(valores['oro'].centenario_venta) + '\
      </td>\
      <td class="bordered_right numero">\
        ' + dinero(valores['oro'].hidalgo_venta) + '\
      </td>\
      <td class="bordered_right numero">\
        ' + dinero(valores['oro'].oro_libertad_venta) + '\
      </td>\
    </tr>\
  </table>\
  \
  <div class="hr"><!-- i --></div>\
  \
  <h2>\
    <a href="' + get_app_url() + 'divisas/petroleo/">Petr&oacute;leo</a>\
  </h2>\
  \
  <table>\
    <tr class="bordered_bottom">\
      <th class="bordered_right">\
        Brent\
      </th>\
      <th class="bordered_right">\
        Mezcla Mexicana\
      </th>\
      <th class="bordered_right">\
        WTI\
      </th>\
    </tr>\
    <tr class="bordered_bottom">\
      <td class="bordered_right">\
        ' + dinero(valores['petroleo'].brent) + '\
      </td>\
      <td class="bordered_right numero">\
        ' + dinero(valores['petroleo'].mezcla_mexicana) + '\
      </td>\
      <td class="bordered_right numero">\
        ' + dinero(valores['petroleo'].wti) + '\
      </td>\
    </tr>\
  </table>\
  \
  <div class="hr"><!-- i --></div>\
  \
  <h2>\
    <a href="' + get_app_url() + 'divisas/plata/">Plata</a>\
  </h2>\
  \
  <table>\
    <tr class="bordered_bottom">\
      <th class="bordered_right">\
        <!-- i -->\
      </th>\
      <th class="bordered_right">\
        Onza Troy\
      </th>\
      <th class="bordered_right">\
        Plata Libertad\
      </th>\
    </tr>\
    <tr class="bordered_bottom">\
      <td class="bordered_right">\
        Compra\
      </td>\
      <td class="bordered_right numero">\
        ' + dinero(valores['plata'].onza_troy_compra) + '\
      </td>\
      <td class="bordered_right numero">\
        ' + dinero(valores['plata'].plata_libertad_compra) + '\
      </td>\
    </tr>\
    <tr class="bordered_bottom">\
      <td class="bordered_right">\
        Venta\
      </td>\
      <td class="bordered_right numero">\
        ' + dinero(valores['plata'].onza_troy_venta) + '\
      </td>\
      <td class="bordered_right numero">\
        ' + dinero(valores['plata'].plata_libertad_venta) + '\
      </td>\
    </tr>\
  </table>\
  \
  <div class="hr"><!-- i --></div>\
  \
  <h2>\
    <a href="' + get_app_url() + 'bolsas/bmv/">BMV</a>\
  </h2>\
  \
  <table>\
    <tr>\
      <th>\
        <a href="' + get_app_url() + 'bolsas/bmv/ipc/">IPC</a>\
      </th>\
      <th>\
        D&iacute;a\
      </th>\
      <th>\
        Semana\
      </th>\
      <th>\
        Mes\
      </th>\
    </tr>\
    <tr>\
      <td class="numero bordered_right">\
        ' + dinero(valores['bmv'].valor) + '\
      </td>\
      <td class="numero bordered_right ' + valores['bmv'].dif_dia_color() + '\">\
        ' + dinero(valores['bmv'].dif_dia()) + '%\
      </td>\
      <td class="numero bordered_right ' + valores['bmv'].dif_semana_color() + '\">\
        ' + dinero(valores['bmv'].dif_semana()) + '%\
      </td>\
      <td class="numero ' + valores['bmv'].dif_mes_color() + '\">\
        ' + dinero(valores['bmv'].dif_mes()) + '%\
      </td>\
    </tr>\
  </table>\
  \
  <div class="hr"><!-- i --></div>\
  \
  <h2>\
    <a href="' + get_app_url() + 'bolsas/dow/">Dow Jones</a>\
  </h2>\
  \
  <table>\
    <tr class="bordered_bottom">\
      <th class="bordered_right">\
        Apertura\
      </th>\
      <th class="bordered_right">\
        Alto\
      </th>\
      <th class="bordered_right">\
        Bajo\
      </th>\
      <th class="bordered_right">\
        Cierre\
      </th>\
      <th class="bordered_right">\
        Volumen\
      </th>\
    </tr>\
    <tr class="bordered_bottom">\
      <td class="bordered_right numero">\
        ' + dinero(valores['dow'].valor) + '\
      </td>\
      <td class="bordered_right numero">\
        ' + dinero(valores['dow'].alto) + '\
      </td>\
      <td class="bordered_right numero">\
        ' + dinero(valores['dow'].bajo) + '\
      </td>\
      <td class="bordered_right numero">\
        ' + dinero(valores['dow'].cierre) + '\
      </td>\
      <td class="bordered_right numero">\
        ' + dinero(valores['dow'].volumen) + '\
      </td>\
    </tr>\
  </table>\
  \
  <div class="hr"><!-- i --></div>\
  \
  <h2>\
    <a href="' + get_app_url() + 'bolsas/nasdaq/">NASDAQ</a>\
  </h2>\
  \
  <table>\
    <tr class="bordered_bottom">\
      <th class="bordered_right">\
        Apertura\
      </th>\
      <th class="bordered_right">\
        Alto\
      </th>\
      <th class="bordered_right">\
        Bajo\
      </th>\
      <th class="bordered_right">\
        Cierre\
      </th>\
    </tr>\
    <tr class="bordered_bottom">\
      <td class="bordered_right numero">\
        ' + dinero(valores['dow'].valor) + '\
      </td>\
      <td class="bordered_right numero">\
        ' + dinero(valores['dow'].alto) + '\
      </td>\
      <td class="bordered_right numero">\
        ' + dinero(valores['dow'].bajo) + '\
      </td>\
      <td class="bordered_right numero">\
        ' + dinero(valores['dow'].cierre) + '\
      </td>\
    </tr>\
  </table>\
  \
  <div class="hr"><!-- i --></div>\
  \
  <h2>\
    <a href="' + get_app_url() + 'bolsas/sp500/">S&P 500</a>\
  </h2>\
  \
  <table>\
    <tr class="bordered_bottom">\
      <th class="bordered_right">\
        Apertura\
      </th>\
      <th class="bordered_right">\
        Alto\
      </th>\
      <th class="bordered_right">\
        Bajo\
      </th>\
      <th class="bordered_right">\
        Cierre\
      </th>\
    </tr>\
    <tr class="bordered_bottom">\
      <td class="bordered_right numero">\
        ' + dinero(valores['sp500'].valor) + '\
      </td>\
      <td class="bordered_right numero">\
        ' + dinero(valores['sp500'].alto) + '\
      </td>\
      <td class="bordered_right numero">\
        ' + dinero(valores['sp500'].bajo) + '\
      </td>\
      <td class="bordered_right numero">\
        ' + dinero(valores['sp500'].cierre) + '\
      </td>\
    </tr>\
  </table>\
  \
  <div class="hr"><!-- i --></div>\
  \
  <h2>\
    <a href="' + get_app_url() + 'bolsas/nikkei/">Nikkei 225</a>\
  </h2>\
  \
  <table>\
    <tr class="bordered_bottom">\
      <th class="bordered_right">\
        Apertura\
      </th>\
      <th class="bordered_right">\
        Alto\
      </th>\
      <th class="bordered_right">\
        Bajo\
      </th>\
      <th class="bordered_right">\
        Cierre\
      </th>\
    </tr>\
    <tr class="bordered_bottom">\
      <td class="bordered_right numero">\
        ' + dinero(valores['nikkei'].valor) + '\
      </td>\
      <td class="bordered_right numero">\
        ' + dinero(valores['nikkei'].alto) + '\
      </td>\
      <td class="bordered_right numero">\
        ' + dinero(valores['nikkei'].bajo) + '\
      </td>\
      <td class="bordered_right numero">\
        ' + dinero(valores['nikkei'].cierre) + '\
      </td>\
    </tr>\
  </table>\
  \
  <div class="hr"><!-- i --></div>\
  \
  <h2>\
    <a href="' + get_app_url() + 'inflacion/inpc/">Inflaci&oacute;n</a>\
  </h2>\
  \
  <table>\
    <tr>\
      <th class="bordered_right">\
        Inflaci&oacute;n \
        ' + doDate(valores['inpc'].fecha, 2) + '\
      </th>\
      <th class="bordered_right">\
        INPC\
      </th>\
    </tr>\
    <tr>\
      <td class="numero bordered_right">\
        ' + dinero(valores['inpc'].get_inflacion()) + '%\
      </td>\
      <td class="numero">\
        ' + dinero(valores['inpc'].valor) + '\
      </td>\
    </tr>\
  </table>\
  \
  <div class="hr"><!-- i --></div>\
  \
  <table>\
    <tr>\
      <td>\
        <h2>\
          <a href="' + get_app_url() + 'inflacion/cpi/">CPI</a>\
        </h2>\
        <p>\
          ' + dinero(valores['cpi'].valor) + '\
        </p>\
      </td>\
      <td>\
        <h2>\
          <a href="' + get_app_url() + 'inflacion/udis/">UDIS</a>\
        </h2>\
        <p>\
          ' + dinero(valores['udis'].valor) + '\
        </p>\
      </td>\
    </tr>\
  </table>\
  \
  <div class="hr"><!-- i --></div>\
  \
  <h2>\
    <a href="' + get_app_url() + 'tasas/imi/">&Iacute;ndice Mis Indicadores</a>\
  </h2>\
  \
  <table>\
    <tr>\
      <th class="bordered_right">\
        IMI\
      </th>\
      <th class="bordered_right">\
        D&iacute;a\
      </th>\
      <th class="bordered_right">\
        Semana\
      </th>\
      <th class="bordered_right">\
        Mes\
      </th>\
    </tr>\
    <tr>\
      <td class="numero bordered_right">\
        ' + dinero(valores['imi'].valor) + '\
      </td>\
      <td class="numero bordered_right ' + valores['imi'].dif_dia_color() + '">\
        ' + dinero(valores['imi'].dif_dia()) + '%\
      </td>\
      <td class="numero bordered_right ' + valores['imi'].dif_semana_color() + '">\
        ' + dinero(valores['imi'].dif_semana()) + '%\
      </td>\
      <td class="numero bordered_right ' + valores['imi'].dif_mes_color() + '">\
        ' + dinero(valores['imi'].dif_mes()) + '%\
      </td>\
    </tr>\
  </table>\
  \
  <div class="hr"><!-- i --></div>\
  \
  <h2>\
    <a href="' + get_app_url() + 'tasas/cpp/">CPP</a>\
  </h2>\
  \
  <table>\
    <tr>\
      <th class="bordered_right">\
        Promedio\
      </th>\
      <th class="bordered_right">\
        Pesos\
      </th>\
      <th class="bordered_right">\
        UDIS\
      </th>\
      <th class="bordered_right">\
        D&oacute;lares\
      </th>\
    </tr>\
    <tr>\
      <td class="bordered_right numero">\
        ' + dinero(valores['cpp'].promedio) + '\
      </td>\
      <td class="bordered_right numero">\
        ' + dinero(valores['cpp'].pesos) + '\
      </td>\
      <td class="bordered_right numero">\
        ' + dinero(valores['cpp'].udis) + '\
      </td>\
      <td class="bordered_right numero">\
        ' + dinero(valores['cpp'].dolares) + '\
      </td>\
    </tr>\
  </table>\
  \
  <div class="hr"><!-- i --></div>\
  \
  <h2>\
    <a href="' + get_app_url() + 'tasas/cetes/">CETES</a>\
  </h2>\
  \
  <table>\
    <tr>'
  
  for cete in valores['cetes']:
    html += '<th class="bordered_right">\
      ' + str(cete.plazo) +' d&iacute;as\
    </th>'
  
  html += '</tr>\
    <tr>'
  
  for cete in valores['cetes']:
    html += '<td class="bordered_right numero">\
      ' + dinero(cete.actual) + '\
    </td>'
  
  html += '</tr>\
  </table>\
  \
  <div class="hr"><!-- i --></div>\
  \
  <h2>\
    <a href="' + get_app_url() + 'tasas/tiie/">TIIE</a>\
  </h2>\
  \
  <table>\
    <tr>\
      <th class="bordered_right">\
        28 d&iacute;as\
      </th>\
      <th class="bordered_right">\
        91 d&iacute;as\
      </th>\
    </tr>\
    <tr>\
      <td class="bordered_right numero">\
        ' + dinero(valores['tiie_28_promedio']) + '\
      </td>\
      <td class="bordered_right numero">\
        ' + dinero(valores['tiie_91_promedio']) + '\
      </td>\
    </tr>\
  </table>\
  \
  <div class="hr"><!-- i --></div>\
  \
  <h2>\
    <a href="' + get_app_url() + 'desempeno/desempleo/">Desempleo</a>\
  </h2>\
  \
  <table>\
    <tr>\
      <th class="bordered_right">\
        Total\
      </th>\
      <th class="bordered_right">\
        Hombres\
      </th>\
      <th class="bordered_right">\
        Mujeres\
      </th>\
    </tr>\
    <tr>\
      <td class="bordered_right numero">\
        ' + dinero(valores['desempleo'].total) + '%\
      </td>\
      <td class="bordered_right numero">\
        ' + dinero(valores['desempleo'].hombres) + '%\
      </td>\
      <td class="bordered_right numero">\
        ' + dinero(valores['desempleo'].mujeres) + '%\
      </td>\
    </tr>\
  </table>\
  \
  <div class="hr"><!-- i --></div>\
  \
  <h2>\
    <a href="' + get_app_url() + 'desempeno/pib/">PIB</a>\
  </h2>\
  \
  <table>\
    <tr>\
      <th class="bordered_right">\
        Total\
      </th>\
      <th class="bordered_right">\
        Primerias\
      </th>\
      <th class="bordered_right">\
        Secundarias\
      </th>\
      <th class="bordered_right">\
        Terciarias\
      </th>\
    </tr>\
    <tr>\
      <td class="bordered_right numero">\
        ' + dinero(valores['pib'].total) + '\
      </td>\
      <td class="bordered_right numero">\
        ' + dinero(valores['pib'].primarias) + '\
      </td>\
      <td class="bordered_right numero">\
        ' + dinero(valores['pib'].secundarias) + '\
      </td>\
      <td class="bordered_right numero">\
        ' + dinero(valores['pib'].terciarias) + '\
      </td>\
    </tr>\
  </table>\
  \
  <h2>\
    <a href="' + get_app_url() + 'desempeno/reservas/">Reservas Internacionales</a>\
  </h2>\
  \
  <table>\
    <tr class="bordered_bottom">\
      <th class="left">\
        Activos\
      </th>\
      <th>\
        <!-- i -->\
      </th>\
    </tr>\
    <tr class="bordered_bottom">\
      <td class="bold">\
        Base monetaria (pesos)\
      </td>\
      <td class="numero">\
        ' + dinero(valores['reserva'].base_monetaria) + '\
      </td>\
    </tr>\
    <tr class="bordered_bottom">\
      <td class="bold">\
        Activos internacionales netos (pesos)\
      </td>\
      <td class="numero">\
        ' + dinero(valores['reserva'].activos_internacionales_netos_pesos) + '\
      </td>\
    </tr>\
    <tr class="bordered_bottom">\
      <td class="bold">\
        Activos internacionales netos (d&oacute;lares E.U.)\
      </td>\
      <td class="numero">\
        ' + dinero(valores['reserva'].activos_internacionales_netos_dolares) + '\
      </td>\
    </tr>\
    <tr class="bordered_bottom">\
      <td class="bold">\
        Cr&eacute;dito interno neto (pesos)\
      </td>\
      <td class="numero">\
        ' + dinero(valores['reserva'].credito_interno_neto_pesos) + '\
      </td>\
    </tr>\
    <tr class="bordered_bottom">\
      <td class="bold">\
        Reserva internacional (d&oacute;lares E.U.)\
      </td>\
      <td class="numero">\
        ' + dinero(valores['reserva'].reserva_internacional_dolares) + '\
      </td>\
    </tr>\
    <tr class="bordered_bottom">\
      <th class="left">\
        Flujos efectivos\
      </th>\
      <th colspan="8">\
        <!-- i -->\
      </th>\
    </tr>\
    <tr class="bordered_bottom">\
      <td class="bold">\
        Base monetaria (pesos)\
      </td>\
      <td class="numero">\
        ' + dinero(valores['reserva'].base_monetaria_pesos) + '\
      </td>\
    </tr>\
    <tr class="bordered_bottom">\
      <td class="bold">\
        Activos internacionales netos (pesos)\
      </td>\
      <td class="numero">\
        ' + dinero(valores['reserva'].activos_internacionales_netos_pesos_var) + '\
      </td>\
    </tr>\
    <tr class="bordered_bottom">\
      <td class="bold">\
        Activos internacionales netos (d&oacute;lares E.U.)\
      </td>\
      <td class="numero">\
        ' + dinero(valores['reserva'].activos_internacionales_netos_dolares_var) + '\
      </td>\
    </tr>\
    <tr class="bordered_bottom">\
      <td class="bold">\
        Cr&eacute;dito interno neto (pesos)\
      </td>\
      <td class="numero">\
        ' + dinero(valores['reserva'].credito_interno_neto_pesos_var) + '\
      </td>\
    </tr>\
  </table>\
  \
  <div class="hr"><!-- i --></div>\
  \
  <br />\
  \
  <p>\
    Este es un bolet&iacute;n autom&aacute;tico.  Si deseas configurarlo o deshabilitarlo, puedes utilizar el enlace:\
    <br />\
    <br />\
    <a href="' + get_app_url() + 'boletin/">' + get_app_url() + 'boletin/</a>\
  </p>'
  
  html += simple_footer()
  
  return html