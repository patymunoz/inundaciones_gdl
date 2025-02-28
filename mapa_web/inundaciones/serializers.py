from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import VistaInundaciones

class VistaInundacionesSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = VistaInundaciones
        geo_field = "geom"  # Geo field exact name
        fields = ('tipo', 'fecha', 'anio', 'full_text', 'video_url')  # Cols of model
