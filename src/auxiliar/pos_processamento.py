import pandas as pd

def processar_linhas(df):
    """
    Função para realizar o pós-processamento dos dados.
    1. Separa linhas que contêm múltiplos municípios na coluna 'municipios_citados'
       (formato esperado: "Nome1 - Cod1, Nome2 - Cod2"). Cada par município-código
       resultará em uma nova linha, repetindo os dados da notícia.
    2. Para cada linha resultante, separa a string "Nome - Codigo" em duas
       novas colunas: 'municipios_citados' (apenas nome) e 'codigo_municipio' (apenas código).

    Args:
        df (pd.DataFrame): DataFrame contendo os dados a serem processados.
                           A coluna 'municipios_citados' deve ter strings como
                           "NomeMunicipio1 - Codigo1, NomeMunicipio2 - Codigo2".

    Returns:
        pd.DataFrame: DataFrame processado com uma linha por município e colunas
                      separadas para nome e código do município.
    """

    novas_linhas_etapa1 = []

    for index, row in df.iterrows():
        municipios_original_str = row.get('municipios_citados', '')

        if isinstance(municipios_original_str, str) and ',' in municipios_original_str:
            municipio_code_pairs = [pair.strip() for pair in municipios_original_str.split(',')]

            for pair_str in municipio_code_pairs:
                nova_linha = row.copy()
                nova_linha['municipios_citados_temp'] = pair_str
                novas_linhas_etapa1.append(nova_linha)
        else:
            nova_linha = row.copy()
            nova_linha['municipios_citados_temp'] = municipios_original_str
            novas_linhas_etapa1.append(nova_linha)

    if not novas_linhas_etapa1:
        expected_cols = df.columns.tolist()
        if 'codigo_municipio' not in expected_cols:
            expected_cols.append('codigo_municipio')
        return pd.DataFrame(columns=expected_cols)

    df_etapa1_concluida = pd.DataFrame(novas_linhas_etapa1).reset_index(drop=True)

    nomes_finais = []
    codigos_finais = []

    for _, row_etapa1 in df_etapa1_concluida.iterrows():
        municipio_code_str = row_etapa1.get('municipios_citados_temp', '')

        if isinstance(municipio_code_str, str) and '-' in municipio_code_str:
            partes = municipio_code_str.split('-', 1)
            nome = partes[0].strip()
            codigo = partes[1].strip() if len(partes) > 1 else ""
            nomes_finais.append(nome)
            codigos_finais.append(codigo)
        else:
            nomes_finais.append(str(municipio_code_str).strip())
            codigos_finais.append("")

    df_etapa1_concluida['municipios_citados_final'] = nomes_finais
    df_etapa1_concluida['codigo_municipio_final'] = codigos_finais

    colunas_para_remover = ['municipios_citados_temp']
    if 'municipios_citados' in df_etapa1_concluida.columns:
         colunas_para_remover.append('municipios_citados')

    df_final = df_etapa1_concluida.drop(columns=colunas_para_remover, errors='ignore')

    df_final = df_final.rename(columns={
        'municipios_citados_final': 'municipios_citados',
        'codigo_municipio_final': 'codigo_municipio'
    })

    if not df.empty:
        original_cols_base = [col for col in df.columns if col != 'municipios_citados']
        final_cols_order = original_cols_base + ['municipios_citados', 'codigo_municipio']
        final_cols_order_existing = [col for col in final_cols_order if col in df_final.columns]
        df_final = df_final[final_cols_order_existing] if final_cols_order_existing else df_final
    elif 'municipios_citados' not in df_final.columns and 'codigo_municipio' in df_final.columns:
        pass

    return df_final
