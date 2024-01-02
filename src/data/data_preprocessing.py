import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import pytz
import os


def get_excel_file(file_path: str, header: list=None):
    try:
        #Intentar cargar el DataFrame desde el archivo Excel
        if header is not None:
            df_raw =pd.read_excel(file_path, header=None)
            df_raw.columns = header
        else:
            df_raw = pd.read_excel(file_path, header=[1])
        
        return df_raw

    except FileNotFoundError:
        print(f"Error: No se puede encontrar el archivo {file_path}")
    except Exception as e:
        print(f"Error inesperado: {e}")



def total_extras(df_raw):

    df_raw.drop(0, inplace=True)
    df_extras_raw = df_raw[df_raw['Puesto'].str.contains('EXTRA')]
    count_values_per_position = df_extras_raw['Puesto'].value_counts()
    df_count_per_position = pd.DataFrame({'Puesto': count_values_per_position.index, 'Cantidad':count_values_per_position.values})

    dict_df_by_position = {}
    for puesto in df_count_per_position['Puesto']:
        puesto_concatenado = puesto.replace(" ","_")
        # Filtrar el DataFrame original por puesto
        df_by_position = df_extras_raw[df_extras_raw['Puesto'] == puesto].copy()
        
        # Agregando el DataFrame al diccionario
        dict_df_by_position[puesto_concatenado] = df_by_position

    result_df = pd.concat(list(dict_df_by_position.values()), keys=dict_df_by_position.keys())
    result_df.reset_index(drop=True, inplace=True)
    result_df["dias_extras"] = result_df.apply(lambda row: sum(1 for cell in row if str(cell) == '.'), axis=1)

    zona_horaria_zapopan = pytz.timezone('America/Mexico_City')
    #Obteniendo la fecha y hora actual
    fecha_actual_zapopan = datetime.now(zona_horaria_zapopan)

    #Formateando fecha y agregando la hora
    fecha_formateada = fecha_actual_zapopan.strftime('%d%m%Y_%H%M')

    current_directory = os.path.dirname(os.path.abspath(__file__))
    directorio_destino = os.path.join(current_directory, "..", "..", "data", "processed")
    nombre_archivo = f"personas_Con_horas_extras_{fecha_formateada}.xlsx"
    path_completo = os.path.join(directorio_destino, nombre_archivo)

    total_dias_extras = [sum(result_df.iloc[:,-1])]
    df_total_dias_extras = pd.DataFrame({"total dias extras": total_dias_extras})

    # # Crear un objeto ExcelWriter para escribir en el archivo Excel
    # with pd.ExcelWriter(path_completo, engine='xlsxwriter') as writer:
    #     # Guardar el primer DataFrame en la primera hoja (por defecto)
    #     result_df.to_excel(writer, sheet_name='Hoja1', index=False)

    #     # Guardar el segundo DataFrame en otra hoja
    #     df_total_dias_extras.to_excel(writer, sheet_name='Hoja2', index=False)

    print(f"Archivo guardado como {path_completo}")

    return result_df, total_dias_extras


