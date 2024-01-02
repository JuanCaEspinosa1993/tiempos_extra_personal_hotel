# app.py
import streamlit as st
import pandas as pd
import base64
import io
from src.data.data_preprocessing import total_extras

def get_table_downloand_link(result_df, total_dias_extras):
    """Enlace de descarga para un DataFrame en formato Excel."""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        # Guardar el primer DataFrame en la primera hoja
        result_df.to_excel(writer, sheet_name='Hoja1', index=False)

        # Guardar el segundo DataFrame en otra hoja
        pd.DataFrame({"total dias extras": total_dias_extras}).to_excel(writer, sheet_name='Hoja2', index=False)

    # Obtener el contenido del archivo Excel
    excel_binary = output.getvalue()
    output.seek(0)

    # Convertir a base64 para el enlace de descarga
    b64 = base64.b64encode(excel_binary).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="resultados.xlsx">Descargar Resultados</a>'
    return href



st.title("Procesamiento de Horas Extras")


# Sección para cargar el archivo Excel
uploaded_file = st.file_uploader("Cargar archivo Excel", type=["xlsx"])

if uploaded_file is not None:
    #Mostrar el contenido del archivo Excel
    st.write("Visualizacion del archivo Excel:")
    df_raw = pd.read_excel(uploaded_file, header=[1])
    st.dataframe(df_raw)

    # Utilizar la caché para evitar ejecutar la función total_extras varias veces
    @st.cache
    def process_data(df):
        result_df, total_dias_extras = total_extras(df)
        return result_df, total_dias_extras

    #Botón para realizar el procesamiento:
    if st.button("Procesar"):
        # Procesamiento de horas extras
        result_df, total_dias_extras = total_extras(df_raw)

        # Mostrar resultados
        st.write("Resultados del procesamiento:")
        st.write("Total días extras:", total_dias_extras[0])
        
        # Mostrar el DataFrame resultante
        st.write("Archivo excel resultante:")
        result_df.columns = result_df.columns.astype(str)  # Convertir nombres de columnas a cadenas
        st.dataframe(result_df)

        # Boton de descarga
        st.markdown(get_table_downloand_link(result_df, total_dias_extras), unsafe_allow_html=True)

