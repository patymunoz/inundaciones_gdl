from django.contrib.gis.db import models

# Define the database models

class Inundacion(models.Model):
    """
    Model to store flood event data.
    """
    tipo = models.CharField(max_length=255)  # Type of flood information
    fecha = models.DateTimeField()  # Date and time of the event
    anio = models.IntegerField()  # Year of the event
    full_text = models.TextField(blank=True, null=True)  # Descriptive information
    video_url = models.URLField(blank=True, null=True)  # URL to a related video
    geom = models.PointField(srid=4326)  # Spatial field for geographic coordinates (latitude/longitude)

    def __str__(self):
        return f"{self.tipo} - {self.fecha.year}"

class VistaInundaciones(models.Model):
    """
    Model representing a database view that combines flood data.
    """
    id = models.BigIntegerField(primary_key=True)
    tipo = models.CharField(max_length=255)  # Type of flood information
    fecha = models.DateField()  # Date of the event
    anio = models.IntegerField()  # Year of the event
    video_url = models.URLField(null=True, blank=True)  # URL to a related video
    geometry = models.PointField()  # Spatial field for geographic data

    class Meta:
        managed = False  # Django will not manage this table (database view)
        db_table = "vista_inundaciones_combinada"  # Name of the database view

class ConteoPuntosPorColonia(models.Model):
    """
    Model representing a materialized view that counts flood points per neighborhood.
    """
    colonia_id = models.IntegerField(primary_key=True)  # Unique identifier for the neighborhood
    colonia_nombre = models.CharField(max_length=255)  # Name of the neighborhood
    geometry = models.MultiPolygonField(srid=4326)  # Geometric field with SRID 4326
    total_puntos = models.IntegerField()  # Total number of flood points in the neighborhood

    class Meta:
        managed = False  # Django will not manage this table (materialized view)
        db_table = "conteo_puntos_por_colonia"  # Name of the materialized view