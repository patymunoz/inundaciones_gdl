import axios from "axios";

const API_URL = "http://127.0.0.1:8000/inundaciones/api/"; // URL de la API de Django

export const obtenerInundaciones = async () => {
    try {
        const respuesta = await axios.get(API_URL);
        return respuesta.data;
    } catch (error) {
        console.error("Error al obtener los datos:", error);
        return null;
    }
};