from django.conf.urls.defaults import *
from django.conf import settings
from misindicadores.feeds import UltimasNoticias

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# Para los feeds
feeds = {
  'noticias': UltimasNoticias,
}

urlpatterns = patterns('',
    # Example:
    # (r'^misindicadores/$', include('misindicadores.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/$', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    
    # Boletin
    (r'^boletin/cron_dos_dia/$', 'misindicadores.boletin.views.cron_dos_dia'),
    (r'^boletin/cron_diario/$', 'misindicadores.boletin.views.cron_diario'),
    (r'^boletin/cron_semanal/$', 'misindicadores.boletin.views.cron_semanal'),
    (r'^boletin/$', 'misindicadores.boletin.views.index'),
    
    # Articulos
    (r'^articulos/update_twitter_indicadores/$', 'misindicadores.articulos.views.update_twitter_indicadores'),
    (r'^articulos/update_twitter/$', 'misindicadores.articulos.views.update_twitter'),
    (r'^articulos/(?P<nombre_limpio>.*)/(?P<id>.*)/$', 'misindicadores.articulos.views.ver_articulo'),
    (r'^articulos/(?P<nombre_limpio>.*)/$', 'misindicadores.articulos.views.ver_categoria'),
    (r'^articulos/$', 'misindicadores.articulos.views.index'),
    
    # Foros
    (r'^foros/(?P<nombre_limpio>.*)/nuevo_topico/$', 'misindicadores.foros.views.nuevo_topico'),
    (r'^foros/(?P<nombre_limpio>.*)/(?P<id>.*)/$', 'misindicadores.foros.views.ver_topico'),
    (r'^foros/(?P<nombre_limpio>.*)/$', 'misindicadores.foros.views.ver_categoria'),
    (r'^foros/$', 'misindicadores.foros.views.index'),
    
    # Medios
    (r'^medios/$', 'misindicadores.medios.views.index'),
    (r'^medios/cron_medios/$', 'misindicadores.medios.views.cron_medios'),
    
    # Desempeno
    (r'^desempeno/afores/$', 'misindicadores.desempeno.views.afores'),
    (r'^desempeno/reservas/$', 'misindicadores.desempeno.views.reservas'),
    (r'^desempeno/pib/$', 'misindicadores.desempeno.views.pib'),
    (r'^desempeno/desempleo/$', 'misindicadores.desempeno.views.desempleo'),
    (r'^desempeno/cron_desempeno/$', 'misindicadores.desempeno.views.cron_desempeno'),
    (r'^desempeno/$', 'misindicadores.desempeno.views.portada'),
    
    # Tasas
    (r'^tasas/img_imi/$', 'misindicadores.tasas.views.img_imi'),
    (r'^tasas/imi/$', 'misindicadores.tasas.views.imi'),
    (r'^tasas/tiie/$', 'misindicadores.tasas.views.tiie'),
    (r'^tasas/cetes/$', 'misindicadores.tasas.views.cetes'),
    (r'^tasas/cpp/$', 'misindicadores.tasas.views.cpp'),
    (r'^tasas/cron_tasas/$', 'misindicadores.tasas.views.cron_tasas'),
    (r'^tasas/$', 'misindicadores.tasas.views.portada'),
    
    # Inflacion
    (r'^inflacion/udis/$', 'misindicadores.inflacion.views.udis'),
    (r'^inflacion/cpi/$', 'misindicadores.inflacion.views.cpi'),
    (r'^inflacion/img_inpc/$', 'misindicadores.inflacion.views.img_inpc'),
    (r'^inflacion/inpc/$', 'misindicadores.inflacion.views.inpc'),
    (r'^inflacion/cron_inflacion/$', 'misindicadores.inflacion.views.cron_inflacion'),
    (r'^inflacion/$', 'misindicadores.inflacion.views.portada'),
    
    # Bolsas
    (r'^bolsas/latinoamerica/$', 'misindicadores.bolsas.views.latinoamerica'),
    (r'^bolsas/cron_paises_bolsas/$', 'misindicadores.bolsas.views.cron_paises_bolsas'),
    (r'^bolsas/nikkei/$', 'misindicadores.bolsas.views.nikkei'),
    (r'^bolsas/sp500/$', 'misindicadores.bolsas.views.sp500'),
    (r'^bolsas/nasdaq/$', 'misindicadores.bolsas.views.nasdaq'),
    (r'^bolsas/img_dow/$', 'misindicadores.bolsas.views.img_dow'),
    (r'^bolsas/dow/$', 'misindicadores.bolsas.views.dow'),
    (r'^bolsas/cron_bolsas/$', 'misindicadores.bolsas.views.cron_bolsas'),
    (r'^bolsas/bmv/buscar_emisora/$', 'misindicadores.bolsas.views.buscar_emisora'),
    (r'^bolsas/bmv/emisora/(?P<emisora>.*)/(?P<rango>.*)/$', 'misindicadores.bolsas.views.bmv_emisora'),
    (r'^bolsas/bmv/emisora/(?P<emisora>.*)/$', 'misindicadores.bolsas.views.bmv_emisora'),
    (r'^bolsas/img_bmv_ipc/$', 'misindicadores.bolsas.views.img_bmv_ipc'),
    (r'^bolsas/bmv/ipc/(?P<rango>.*)/$', 'misindicadores.bolsas.views.bmv_ipc'),
    (r'^bolsas/bmv/ipc/$', 'misindicadores.bolsas.views.bmv_ipc'),
    (r'^bolsas/bmv/$', 'misindicadores.bolsas.views.bmv'),
    (r'^bolsas/cron_bmv/$', 'misindicadores.bolsas.views.cron_bmv'),
    (r'^bolsas/$', 'misindicadores.bolsas.views.portada'),
    
    # Divisas
    (r'^divisas/tabla_comparativa/$', 'misindicadores.divisas.views.tabla_comparativa'),
    (r'^divisas/plata/$', 'misindicadores.divisas.views.plata'),
    (r'^divisas/petroleo/$', 'misindicadores.divisas.views.petroleo'),
    (r'^divisas/cron_petroleo/$', 'misindicadores.divisas.views.cron_petroleo'),
    (r'^divisas/oro/$', 'misindicadores.divisas.views.oro'),
    (r'^divisas/metales/$', 'misindicadores.divisas.views.metales'),
    (r'^divisas/cron_metales/$', 'misindicadores.divisas.views.cron_metales'),
    (r'^divisas/yen/$', 'misindicadores.divisas.views.yen'),
    (r'^divisas/libra/$', 'misindicadores.divisas.views.libra'),
    (r'^divisas/deg/$', 'misindicadores.divisas.views.deg'),
    (r'^divisas/img_euro/$', 'misindicadores.divisas.views.img_euro'),
    (r'^divisas/euro/$', 'misindicadores.divisas.views.euro'),
    (r'^divisas/cron_euro/$', 'misindicadores.divisas.views.cron_euro'),
    (r'^divisas/img_dolar/$', 'misindicadores.divisas.views.img_dolar'),
    (r'^divisas/dolar/$', 'misindicadores.divisas.views.dolar'),
    (r'^divisas/cron_dolar/$', 'misindicadores.divisas.views.cron_dolar'),
    (r'^divisas/$', 'misindicadores.divisas.views.portada'),
    
    # Cuentas
    (r'^rd/$', 'misindicadores.cuentas.views.resumen'),
    (r'^resumen/$', 'misindicadores.cuentas.views.resumen'),
    (r'^invitar/$', 'misindicadores.cuentas.views.invitar'),
    (r'^contacto/$', 'misindicadores.cuentas.views.contacto'),
    (r'^login/$', 'misindicadores.cuentas.views.login_view'),
    (r'^doLogin/$', 'misindicadores.cuentas.views.do_login'),
    (r'^logout/$', 'misindicadores.cuentas.views.logout_view'),
    (r'^registrate/$', 'misindicadores.cuentas.views.registrate'),
    (r'^doRegistro/$', 'misindicadores.cuentas.views.do_registro'),
    (r'^recover/$', 'misindicadores.cuentas.views.recover'),
    (r'^doRecover/$', 'misindicadores.cuentas.views.do_recover'),
    (r'^post_recover/(?P<shash>.*)/$', 'misindicadores.cuentas.views.post_recover'),
    (r'^chngpwd/$', 'misindicadores.cuentas.views.chngpwd'),
    (r'^do_chngpwd/$', 'misindicadores.cuentas.views.do_chngpwd'),
    (r'^about/$', 'misindicadores.cuentas.views.about'),
    (r'^ayuda/$', 'misindicadores.cuentas.views.ayuda'),
    (r'^indicadores/$', 'misindicadores.cuentas.views.indicadores'),
    
    # Feeds
    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
    
    # Root
    (r'^$', 'misindicadores.cuentas.views.home'),

    # Para media estatica
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

    # Para media estatica del admin
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.ADMIN_FILES_ROOT}),
)
