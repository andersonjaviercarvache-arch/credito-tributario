import streamlit as st
import pandas as pd
import io

# Configuración de la página
st.set_page_config(page_title="Calculadora de Crédito Tributario", page_icon="💰")

st.title("💰 Calculadora de Crédito Tributario SRI")
st.write("Sube tu reporte de comprobantes electrónicos para obtener un resumen.")

# 1. Carga de archivo
uploaded_file = st.file_uploader("Sube tu archivo de comprobantes (.txt o .csv)", type=["txt", "csv"])

if uploaded_file is not None:
    try:
        # Ajusta el separador según el formato real de tu archivo del SRI
        # Ejemplo: si es un CSV con punto y coma
        df = pd.read_csv(uploaded_file, sep=';') 
        
        # 2. Procesamiento (Ajustar nombres de columnas según tu archivo)
        # Supongamos que tu archivo tiene columnas 'tipo_comprobante' y 'iva'
        total_comprobantes = len(df)
        total_iva = df['iva'].sum()
        
        # 3. Visualización
        col1, col2 = st.columns(2)
        col1.metric("Comprobantes Recibidos", total_comprobantes)
        col2.metric("Total IVA Recibido", f"${total_iva:,.2f}")
        
        st.write("### Detalle de los datos")
        st.dataframe(df)
        
    except Exception as e:
        st.error(f"Error al procesar el archivo: {e}")
else:
    st.info("Por favor, sube un archivo para comenzar.")
