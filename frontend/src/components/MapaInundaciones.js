import { useEffect, useState } from "react";
import axios from "axios";
import { MapContainer, TileLayer, Marker, Popup, LayersControl, LayerGroup } from "react-leaflet"; // ⬅️ Asegúrate de incluir LayerGroup
import "leaflet/dist/leaflet.css";
import "../styles/MapaInundaciones.css"; // Para estilos personalizados

const { BaseLayer, Overlay } = LayersControl;

function MapaInundaciones() {
    const [geoData, setGeoData] = useState(null);
    const [modo, setModo] = useState("marcadores");
    const [anioFiltro, setAnioFiltro] = useState("Todos");
    const [aniosDisponibles, setAniosDisponibles] = useState([]);

    useEffect(() => {
        axios.get("http://127.0.0.1:8000/inundaciones/api/anios/")
            .then(response => {
                console.log("Años recibidos desde la API:", response.data);
                setAniosDisponibles(response.data);
            })
            .catch(error => console.error("Error al obtener años:", error));
    }, []);

    const cargarDatos = async () => {
        let url = "http://127.0.0.1:8000/inundaciones/api/";
        if (anioFiltro !== "Todos") {
            url += `?anio=${anioFiltro}`;
        }

        try {
            const response = await axios.get(url);
            console.log("Datos de inundaciones recibidos en React:", response.data);
            setGeoData(response.data);
        } catch (error) {
            console.error("Error al obtener datos:", error);
        }
    };

    useEffect(() => {
        cargarDatos();
    }, [anioFiltro]); // ⬅️ Se incluye `anioFiltro` en la lista de dependencias

    return (
        <div>
            <h2>Mapa de Inundaciones</h2>

            <div className="filtros">
                <label>Modo de visualización:</label>
                <select onChange={(e) => setModo(e.target.value)} value={modo}>
                    <option value="marcadores">Marcadores</option>
                    <option value="heatmap">Mapa de Calor</option>
                    <option value="coropletas">Coropletas</option>
                </select>

                <label>Filtrar por año:</label>
                <select onChange={(e) => setAnioFiltro(e.target.value)} value={anioFiltro}>
                    <option value="Todos">Todos</option>
                    {aniosDisponibles.length > 0 ? (
                        aniosDisponibles.map((anio, index) => (
                            <option key={index} value={anio}>{anio}</option>
                        ))
                    ) : (
                        <option disabled>Cargando...</option>
                    )}
                </select>
            </div>

            <MapContainer center={[20.6767, -103.3478]} zoom={8} style={{ height: "500px", width: "100%" }}>
                <LayersControl position="topright">
                    <BaseLayer checked name="OpenStreetMap">
                        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
                    </BaseLayer>
                    <BaseLayer name="Esri WorldImagery">
                        <TileLayer url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}" />
                    </BaseLayer>

                    {modo === "marcadores" && geoData && geoData.features.length > 0 && (
                        <Overlay checked name="Marcadores">
                            <LayerGroup>
                                {geoData.features.map((feature, index) => {
                                    if (!feature.geometry) return null;

                                    const [lng, lat] = feature.geometry.coordinates;
                                    return (
                                        <Marker key={index} position={[lat, lng]}>
                                            <Popup>
                                                <b>{feature.properties.tipo}</b><br />
                                                Fecha: {feature.properties.fecha}
                                            </Popup>
                                        </Marker>
                                    );
                                })}
                            </LayerGroup>
                        </Overlay>
                    )}
                </LayersControl>
            </MapContainer>
        </div>
    );
}

export default MapaInundaciones;
