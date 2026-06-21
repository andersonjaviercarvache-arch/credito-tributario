import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Gestor SRI", page_icon="🧾")

st.title("🧾 Analizador de Comprobantes SRI")
st.write("Sube tu archivo de reportes para calcular el IVA.")

# 1. Carga de archivo
uploaded_file = st.file_uploader("Sube tu archivo (.csv o .xlsx)", type=["csv", "xlsx", "txt"])

if uploaded_file is not None:
    try:
        # Detectar tipo de archivo y leer
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file, sep=None, engine='python')
        elif uploaded_file.name.endswith('.txt'):
            df = pd.read_csv(uploaded_file, sep='\t') # Ajusta si tu .txt usa otro separador
        else:
            df = pd.read_excel(uploaded_file)

        # 2. Búsqueda inteligente de la columna IVA
        # Convertimos nombres a minúsculas para encontrar coincidencias fáciles
        cols_lower = [c.lower() for c in df.columns]
        
        # Intentamos buscar variantes comunes de "IVA"
        indices = [i for i, col in enumerate(cols_lower) if 'iva' in col]
        
        if not indices:
            st.error(f"No encontramos la columna de IVA. Columnas detectadas: {list(df.columns)}")
        else:
            nombre_col_iva = df.columns[indices[0]]
            
            # Limpieza: Convertir a número (reemplazar comas por puntos si existen)
            df[nombre_col_iva] = df[nombre_col_iva].replace({',': '.'}, regex=True)
            df[nombre_col_iva] = pd.to_numeric(df[nombre_col_iva], errors='coerce').fillna(0)
            
            # 3. Cálculos
            total_comprobantes = len(df)
            total_iva = df[nombre_col_iva].sum()
            
            # 4. Mostrar Resultados
            col1, col2 = st.columns(2)
            col1.metric("Total Comprobantes", total_comprobantes)
            col2.metric("Total IVA", f"${total_iva:,.2f}")
            
            st.success("Archivo procesado correctamente")
            with st.expander("Ver detalle de datos"):
                st.dataframe(df)

    except Exception as e:
        st.error(f"Ocurrió un error al procesar el archivo: {e}")
else:
    st.info("Esperando archivo... Por favor, asegúrate de que tu archivo tenga encabezados claros.")
