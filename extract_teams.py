import pandas as pd
import uuid

url = ['https://www.espn.cl/futbol/posiciones/_/liga/esp.1',
       'https://www.espn.cl/futbol/posiciones/_/liga/eng.1',
       'https://www.espn.cl/futbol/posiciones/_/liga/ita.1',
       'https://www.espn.cl/futbol/posiciones/_/liga/ger.1',
       'https://www.espn.cl/futbol/posiciones/_/liga/fra.1',
       'https://www.espn.cl/futbol/posiciones/_/liga/por.1',
       'https://www.espn.cl/futbol/posiciones/_/liga/ned.1'
       ]
leagues = ['LA_LIGA', 'PREMIER_LEAGUE','SERIE_A', 'BUNDESLIGA', 'LIGUE_1','PRIMEIRA_LIGA', 'EREDIVISIE']

df_leagues = {
    'League': leagues,
    'URL': url  
}

df_leagues = pd.DataFrame(df_leagues)

dfs = []
for i in range(len(url)):
    df_temp = pd.read_html(df_leagues['URL'][i])[0]
    dfs.append(df_temp)

df = pd.concat(dfs, ignore_index=True)
df.columns = ['Columna1', 'Columna2', 'Columna3']
# Llenar valores nulos en Columna1 y Columna2 con los valores de Columna3 si ambas son nulas
condicion_nulos = df['Columna1'].isna() & df['Columna2'].isna()
df.loc[condicion_nulos, 'Columna1'] = df['Columna3']
df.loc[condicion_nulos, 'Columna2'] = df['Columna3']
# Llenar valores nulos en Columna1 con los valores de Columna2
df['Columna1'].fillna(df['Columna2'], inplace=True)
# Llenar valores nulos en Columna2 con los valores de Columna3
df['Columna2'].fillna(df['Columna3'], inplace=True)
# Eliminar la primera fila (índice 0)
#df = df.drop(0)
# Eliminar las columnas 2 y 3
df = df.drop(columns=['Columna2', 'Columna3'])
# Imprimir el DataFrame resultante
df['Columna1'] = df['Columna1'].apply(lambda x: x[5:] if x[:2].isnumeric()==True else x[4:])
# Agregar una nueva columna 'ID_TEAM' con códigos únicos
df['ID_TEAM'] = [str(uuid.uuid4().hex)[:4] for _ in range(len(df))]
df.rename(columns={'Columna1': 'EQUIPO'}, inplace=True)
print(df)