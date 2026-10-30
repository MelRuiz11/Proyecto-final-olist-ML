import os
import sys
import json
import joblib
import pandas as pd
from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

directorio_actual = os.path.dirname(os.path.abspath(__file__))
if directorio_actual not in sys.path:
    sys.path.insert(0, directorio_actual)

app = FastAPI(
    title="API Olist - Riesgo de Mala Reseña",
    description="Servicio web para predecir la probabilidad de recibir 1 o 2 estrellas."
)

# Carga diferida (lazy loading) para que la API responda inmediatamente a Render en el arranque
modelo = None
UMBRAL = 0.2591

def cargar_recursos():
    global modelo, UMBRAL
    if modelo is None:
        try:
            ruta_modelo = os.path.join(directorio_actual, "modelo_riesgo.joblib")
            modelo = joblib.load(ruta_modelo)

            ruta_umbral = os.path.join(directorio_actual, "umbral.json")
            if os.path.exists(ruta_umbral):
                with open(ruta_umbral, "r") as f:
                    datos_umbral = json.load(f)
                    UMBRAL = float(datos_umbral.get("umbral", 0.2591))
        except Exception as e:
            print(f"Error al cargar recursos: {str(e)}")
            raise RuntimeError(f"No se pudo cargar el modelo en el servidor: {str(e)}")

class PedidoContrato(BaseModel):
    order_id: str
    order_purchase_timestamp: str
    order_approved_at: Optional[str] = None
    order_delivered_carrier_date: Optional[str] = None
    order_delivered_customer_date: Optional[str] = None
    order_estimated_delivery_date: str
    estado_cliente: str
    n_items: float
    n_vendedores: float
    precio_total: float
    flete_total: float
    peso_total_g: Optional[float] = None
    fotos_promedio: Optional[float] = None
    categoria: Optional[str] = None
    estado_vendedor: Optional[str] = None
    tipo_pago: Optional[str] = None
    cuotas_max: Optional[float] = None

@app.get("/")
def home():
    # Render verifica este endpoint para validar el Port Binding. Debe responder ultra rápido.
    return {"status": "ok", "mensaje": "API activa. El modelo se inicializará en la primera llamada de predicción."}

@app.post("/riesgo")
def predecir_riesgo(pedido: PedidoContrato):
    try:
        cargar_recursos()
        df_pedido = pd.DataFrame([pedido.model_dump()])
        probabilidad = float(modelo.predict_proba(df_pedido)[:, 1])
        riesgo_alto = bool(probabilidad >= UMBRAL)

        return {
            "order_id": pedido.order_id,
            "probabilidad": round(probabilidad, 4),
            "probabilidad_pct": f"{round(probabilidad * 100, 1)}%",
            "umbral": round(UMBRAL, 4),
            "riesgo_alto": riesgo_alto,
            "accion_sugerida": "Contactar cliente de inmediato" if riesgo_alto else "Operación normal"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la predicción: {str(e)}")
