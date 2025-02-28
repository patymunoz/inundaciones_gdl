from django.urls import path
from . import views
from .views import anios_disponibles, datos_grafico, puntos_por_colonia

urlpatterns = [
    path("", views.home, name="home"), 
    path("api/", views.vista_inundaciones_geojson, name="vista_inundaciones_geojson"),
    path("mapa/", views.mapa_view, name="mapa_view"),
    path('api/anios/', anios_disponibles, name='anios_disponibles'),
    path('api/grafico/', datos_grafico, name='datos_grafico'),
    path('api/puntos_por_colonia/', puntos_por_colonia, name='puntos_por_colonia'),
]