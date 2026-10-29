import streamlit as st
import requests
import json

st.set_page_config(page_title="Score de Riesgo Olist", layout="wide")
st.title("🔍 Monitoreo de Riesgo de Pedidos - Olist")

st.markdown("""
Esta aplicación permite evaluar el riesgo de recibir una mala calificación (1 o 2 estrellas) 
en pedidos de Olist usando el modelo predictivo desplegado.
""")

# Configuración de URL de la API
url_api = st.sidebar.text_input("URL de la API en Render:", "https://SU-API.onrender.com")

st.subheader("Datos del Pedido")

col1, col2, col3 = st.columns(3)
with col1:
    order_id = st.text_input("ID del Pedido:", "00010242fe8c5a6d1ba2dd792cb16214")
    order_purchase_timestamp = st.text_input("Fecha Compra:", "2017-09-13 08:59:02")
    order_approved_at = st.text_input("Fecha Aprobación:", "2017-09-13 09:05:55")
    order_delivered_carrier_date = st.text_input("Fecha Transportista:", "2017-09-19 18:34:16")

with col2:
    order_delivered_customer_date = st.text_input("Fecha Entrega Real:", "2017-09-20 23:43:48")
    order_estimated_delivery_date = st.text_input("Fecha Estimada:", "2017-09-29 00:00:00")
    estado_cliente = st.text_input("Estado del Cliente (UF):", "RJ")
    n_items = st.number_input("Número de ítems:", min_value=1, value=1)

with col3:
    n_vendedores = st.number_input("Número de vendedores:", min_value=1, value=1)
    precio_total = st.number_input("Precio Total:", min_value=0.0, value=58.90)
    flete_total = st.number_input("Flete Total:", min_value=0.0, value=13.29)
    peso_total_g = st.number_input("Peso Total (g):", min_value=0.0, value=650.0)

with st.expander("Campos Adicionales"):
    col4, col5, col6 = st.columns(3)
    with col4:
        fotos_promedio = st.number_input("Fotos promedio:", min_value=0.0, value=4.0)
        categoria = st.text_input("Categoría:", "cool_stuff")
    with col5:
        estado_vendedor = st.text_input("Estado del Vendedor (UF):", "SP")
        tipo_pago = st.text_input("Tipo de Pago:", "credit_card")
    with col6:
        cuotas_max = st.number_input("Cuotas Máximas:", min_value=1, value=2)

if st.button("Evaluar Riesgo"):
    datos_payload = {
        "order_id": order_id,
        "order_purchase_timestamp": order_purchase_timestamp,
        "order_approved_at": order_approved_at if order_approved_at else None,
        "order_delivered_carrier_date": order_delivered_carrier_date if order_delivered_carrier_date else None,
        "order_delivered_customer_date": order_delivered_customer_date if order_delivered_customer_date else None,
        "order_estimated_delivery_date": order_estimated_delivery_date,
        "estado_cliente": estado_cliente,
        "n_items": float(n_items),
        "n_vendedores": float(n_vendedores),
        "precio_total": float(precio_total),
        "flete_total": float(flete_total),
        "peso_total_g": float(peso_total_g),
        "fotos_promedio": float(fotos_promedio),
        "categoria": categoria,
        "estado_vendedor": estado_vendedor,
        "tipo_pago": tipo_pago,
        "cuotas_max": float(cuotas_max)
    }
    
    try:
        res = requests.post(f"{url_api.rstrip('/')}/riesgo", json=datos_payload)
        if res.status_code == 200:
            resultado = res.json()
            st.success("¡Consulta realizada con éxito!")
            
            if resultado.get("riesgo_alto"):
                st.error(f"🚨 ALTO RIESGO DETECTADO - Probabilidad: {resultado.get('probabilidad_pct')}")
                st.warning(f"Acción Sugerida: {resultado.get('accion_sugerida')}")
            else:
                st.info(f"✅ RIESGO BAJO - Probabilidad: {resultado.get('probabilidad_pct')}")
                st.success(f"Acción Sugerida: {resultado.get('accion_sugerida')}")
                
            st.json(resultado)
        else:
            st.error(f"Error de la API: Código {res.status_code} - {res.text}")
    except Exception as e:
        st.error(f"No se pudo conectar con la API: {e}")
