# 🔍 API Olist - Score de Riesgo de Mala Reseña

Este servicio web proporciona un endpoint predictivo en producción que analiza las transacciones del e-commerce **Olist** para estimar el riesgo (probabilidad de 0 a 1) de que un pedido entregado reciba una baja calificación (1 o 2 estrellas).

## 🛠️ Tecnologías Utilizadas
* **FastAPI:** Framework web ágil y de alto rendimiento para Python.
* **XGBoost Classifier:** Modelo entrenado para la predicción de riesgo.
* **Scikit-Learn Pipeline:** Pipeline automatizado para garantizar consistencia en la transformación de datos.
* **Uvicorn/Gunicorn:** Servidor ASGI para producción.

## 🚀 Estructura del Directorio `api/`
* `main.py`: Punto de entrada de la aplicación FastAPI y definición de endpoints.
* `preparacion.py`: Script con la función de preprocesamiento y extracción de features (`crear_variables`).
* `modelo_riesgo.joblib`: Modelo entrenado serializado.
* `umbral.json`: Umbral correspondiente al top 10% de mayor riesgo histórico.
* `requirements.txt`: Dependencias del entorno de producción.

## 📌 Endpoints Principales

### 1. Estado de la API
* **Método:** `GET`
* **Ruta:** `/`
* **Respuesta:** 
  ```json
  {
    "status": "ok",
    "mensaje": "API de Riesgo Olist activa y lista."
  }
  ```

### 2. Predicción de Riesgo
* **Método:** `POST`
* **Ruta:** `/riesgo`
* **Cuerpo de la Petición (JSON - Contrato de 17 Variables):**
  ```json
  {
    "order_id": "00010242fe8c5a6d1ba2dd792cb16214",
    "order_purchase_timestamp": "2017-09-13 08:59:02",
    "order_approved_at": "2017-09-13 09:45:35",
    "order_delivered_carrier_date": "2017-09-19 18:34:16",
    "order_delivered_customer_date": "2017-09-20 23:43:48",
    "order_estimated_delivery_date": "2017-09-29 00:00:00",
    "estado_cliente": "RJ",
    "n_items": 1.0,
    "n_vendedores": 1.0,
    "precio_total": 58.90,
    "flete_total": 13.29,
    "peso_total_g": 650.0,
    "fotos_promedio": 4.0,
    "categoria": "cool_stuff",
    "estado_vendedor": "SP",
    "tipo_pago": "credit_card",
    "cuotas_max": 2.0
  }
  ```
* **Respuesta Exitosa (JSON):**
  ```json
  {
    "order_id": "00010242fe8c5a6d1ba2dd792cb16214",
    "probabilidad": 0.8337,
    "probabilidad_pct": "83.4%",
    "umbral": 0.2609,
    "riesgo_alto": true,
    "accion_sugerida": "Contactar cliente de inmediato"
  }
  ```
