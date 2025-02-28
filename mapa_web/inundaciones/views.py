#from django.shortcuts import render

# Create your views here.
#from django.http import HttpResponse

#def index(request):
#    return HttpResponse("¡Bienvenido a la aplicación de Inundaciones!")

from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Count
from .models import VistaInundaciones, ConteoPuntosPorColonia

def home(request):
    """
    Render the default map view.
    """
    return render(request, 'inundaciones/map.html')

# API to return flood data in GeoJSON format
def vista_inundaciones_geojson(request):
    """
    Retrieve and return flood event data in GeoJSON format.
    Filters data by year if the 'anio' parameter is provided.
    """
    anio = request.GET.get('anio')

    if anio:
        objetos = VistaInundaciones.objects.filter(anio=anio)
    else:
        objetos = VistaInundaciones.objects.all()

    # Construct GeoJSON structure
    data = {
        "type": "FeatureCollection",
        "features": []
    }

    # Populate GeoJSON with feature data
    for obj in objetos:
        if obj.geometry:  # Ensure geometry exists
            data["features"].append({
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        obj.geometry.x,  # Longitude
                        obj.geometry.y   # Latitude
                    ]
                },
                "properties": {
                    "tipo": obj.tipo,
                    "fecha": obj.fecha.isoformat() if obj.fecha else None,
                    "anio": obj.anio,
                    "video_url": obj.video_url
                }
            })

    return JsonResponse(data, safe=False)

# Render the map page
def mapa_view(request):
    """
    Render the map template.
    """
    return render(request, 'inundaciones/map.html')

# API to return available years
def anios_disponibles(request):
    """
    Retrieve and return a list of unique years with recorded flood data.
    """
    anios = VistaInundaciones.objects.values_list('anio', flat=True).distinct().order_by('anio')
    return JsonResponse(list(anios), safe=False)

# API to return data for charts
def datos_grafico(request):
    """
    Retrieve and return flood event counts per year for visualization in charts.
    """
    datos_por_anio = VistaInundaciones.objects.values('anio').annotate(total=Count('anio')).order_by('anio')
    
    # Format data for Chart.js
    labels = [dato['anio'] for dato in datos_por_anio]
    values = [dato['total'] for dato in datos_por_anio]
    
    return JsonResponse({'labels': labels, 'values': values})

# API to return flood point counts by neighborhood in GeoJSON format
def puntos_por_colonia(request):
    """
    Retrieve and return flood point counts grouped by neighborhood (colonia) in GeoJSON format.
    """
    colonias = ConteoPuntosPorColonia.objects.all()

    # Construct GeoJSON structure
    data = {
        "type": "FeatureCollection",
        "features": []
    }

    for colonia in colonias:
        if colonia.geometry:
            data["features"].append({
                "type": "Feature",
                "geometry": {
                    "type": "MultiPolygon",
                    "coordinates": colonia.geometry.coords
                },
                "properties": {
                    "colonia_id": colonia.colonia_id,
                    "nombre": colonia.colonia_nombre,
                    "total_puntos": colonia.total_puntos
                }
            })

    return JsonResponse(data)