import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import pytz
import os


def total_extras(df_raw:pd.DataFrame):
    df_raw = pd.read_excel("../data/raw/Propinas 01 al 15 de diciembre de 2023.xlsx", header=[1])
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
    directorio_destino = '../data/processed'
    nombre_archivo = f"personas_Con_horas_extras_{fecha_formateada}.xlsx"
    path_completo = os.path.join(directorio_destino, nombre_archivo)

    total_dias_extras = [sum(result_df.iloc[:,-1])]
    df_total_dias_extras = pd.DataFrame({"total dias extras": total_dias_extras})

    # Crear un objeto ExcelWriter para escribir en el archivo Excel
    with pd.ExcelWriter(path_completo, engine='xlsxwriter') as writer:
        # Guardar el primer DataFrame en la primera hoja (por defecto)
        result_df.to_excel(writer, sheet_name='Hoja1', index=False)

        # Guardar el segundo DataFrame en otra hoja
        df_total_dias_extras.to_excel(writer, sheet_name='Hoja2', index=False)

    print(f"Archivo guardado como {path_completo}")

    return total_dias_extras