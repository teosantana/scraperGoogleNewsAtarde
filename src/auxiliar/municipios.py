import pandas as pd
import functools

df = pd.read_excel('src\\data\\municipios_metadata.xlsx', sheet_name='municipios_bahia')

codigos_municipios = df['Município'].tolist()
municipios = df['Nome_Município'].tolist()

@functools.lru_cache()
def get_municipios_metadata():
    return {municipio: codigo for municipio, codigo in zip(municipios, codigos_municipios)}

#print(get_municipios_metadata())